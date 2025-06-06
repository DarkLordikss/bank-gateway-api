import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from app.core.config import settings
from prometheus_client import Gauge, Summary


http_requests_seconds_count = Gauge(
    "http_server_requests_active_seconds_count",
    "Total number of HTTP requests attempted",
    ["method", "endpoint", "status"]
)

http_requests_errors_total = Gauge(
    "http_request_errors_total",
    "Total number of failed HTTP requests",
    ["method", "endpoint", "error_type"]
)

http_requests_active_seconds = Summary(
    "http_request_duration_seconds",
    "Time spent on HTTP requests",
    ["method", "endpoint"]
)


@retry(
    stop=stop_after_attempt(settings.retries),
    wait=wait_fixed(settings.wait_seconds)
)
async def http_request_with_retry(method: str, url: str, json: dict = None, params: dict = None) -> httpx.Response:
    labels = {"method": method.lower(), "endpoint": url}

    with http_requests_active_seconds.labels(**labels).time():
        try:
            async with httpx.AsyncClient() as client:
                if method.lower() == "get":
                    response = await client.get(url, params=params)
                elif method.lower() == "post":
                    response = await client.post(url, json=json, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                http_requests_seconds_count.labels(
                    method=method.lower(),
                    endpoint=url,
                    status=str(response.status_code)
                ).inc()

                response.raise_for_status()

                return response
        except Exception as e:
            http_requests_seconds_count.labels(
                method=method.lower(),
                endpoint=url,
                status="500"
            ).inc()

            http_requests_errors_total.labels(
                method=method.lower(),
                endpoint=url,
                error_type=type(e).__name__
            ).inc()
            raise
