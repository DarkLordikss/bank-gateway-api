import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from app.core.config import settings


@retry(
    stop=stop_after_attempt(settings.retries),
    wait=wait_fixed(settings.wait_seconds)
)
async def http_request_with_retry(method: str, url: str, json: dict = None, params: dict = None) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        if method == "get":
            response = await client.get(url, params=params)
        elif method == "post":
            response = await client.post(url, json=json, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()
        return response
