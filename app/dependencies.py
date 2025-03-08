from typing import Dict

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from app.core.config import settings

security = HTTPBearer()


async def token_check(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
    """
    Проверяет JWT-токен через сервис employee.
    Возвращает user_id, если токен валиден.
    """
    token = credentials.credentials
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
