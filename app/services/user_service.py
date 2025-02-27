import httpx
from app.core.config import settings
from app.models.schemas import LoginReq, RegisterClientReq, JwtToken, ProfileResp


async def login_client(data: LoginReq) -> JwtToken:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.client_service_url}/client/login",
            json=data.dict()
        )
        response.raise_for_status()
        return JwtToken(**response.json())


async def register_client(data: RegisterClientReq) -> JwtToken:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.client_service_url}/client/register",
            json=data.dict()
        )
        response.raise_for_status()
        return JwtToken(**response.json())


async def get_client_profile(client_id: str) -> ProfileResp:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.client_service_url}/client/profile/{client_id}"
        )
        response.raise_for_status()
        return ProfileResp(**response.json())
