import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from app.core.config import settings


@retry(
    stop=stop_after_attempt(settings.retries),
    wait=wait_fixed(settings.wait_seconds),
    retry=retry_if_exception_type(httpx.RequestError)
)
async def http_request_with_retry(method: str, url: str, params: dict = None) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await getattr(client, method)(url, params=params)
        response.raise_for_status()
        return response
