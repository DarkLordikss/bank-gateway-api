import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import (
    DoExchangeResp,
    DoExchangeReq,
    UserDTO
)


async def get_currencies() -> List[UserDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.exchange_service_url}/currencies")
        response.raise_for_status()
        data = response.json()
        return data


async def do_exchange(data: DoExchangeReq) -> DoExchangeResp:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.exchange_service_url}/exchange", json=data.dict())
        response.raise_for_status()
        data = response.json()
        return DoExchangeResp(
            amount=data['amount'],
            rate=data['rate']
        )
