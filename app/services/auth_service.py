from typing import Dict
import httpx
from app.core.config import settings
from fastapi import HTTPException


async def token_decode(token: str) -> Dict:
    """
    Проверяет JWT-токен через сервис employee.
    Возвращает user_id, если токен валиден.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/token/check",
            params={"token": token}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    data = response.json()
    return {
        "user_id": data["user_id"],
        "role": data["role"]
    }
