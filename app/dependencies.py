from fastapi import HTTPException, Query
import httpx
from app.core.config import settings


async def token_check(token: str = Query(...)):
    """
    Зависимость для проверки токена.
    При успешной проверке возвращает идентификатор пользователя (user_id).
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.client_service_url}/token/check",
            params={"token": token}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    data = response.json()
    return data["user_id"]
