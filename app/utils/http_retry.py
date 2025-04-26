import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from app.core.config import settings
from prometheus_client import Counter, Summary


http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests attempted",
    ["method", "endpoint"]
)

# Считаем количество ошибок
http_requests_errors_total = Counter(
    "http_requests_errors_total",
    "Total number of failed HTTP requests",
    ["method", "endpoint", "error_type"]
)

# Считаем длительность активных запросов
http_requests_duration_seconds = Summary(
    "http_requests_duration_seconds",
    "Duration of HTTP requests in seconds",
    ["method", "endpoint"]
)


@retry(
    stop=stop_after_attempt(settings.retries),
    wait=wait_fixed(settings.wait_seconds)
)
async def http_request_with_retry(method: str, url: str, json: dict = None, params: dict = None) -> httpx.Response:
    labels = {"method": method.lower(), "endpoint": url}

    http_requests_total.labels(**labels).inc()

    with http_requests_duration_seconds.labels(**labels).time():
        try:
            async with httpx.AsyncClient() as client:
                if method.lower() == "get":
                    response = await client.get(url, params=params)
                elif method.lower() == "post":
                    response = await client.post(url, json=json, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                response.raise_for_status()
                return response
        except Exception as e:
            http_requests_errors_total.labels(
                method=method.lower(),
                endpoint=url,
                error_type=type(e).__name__
            ).inc()
            raise
