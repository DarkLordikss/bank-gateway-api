import httpx
from app.core.config import settings
from app.models.schemas import LoginReq, RegisterReq, JwtToken, ProfileResp


async def login_client(data: LoginReq) -> JwtToken:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/login",
            json=data.dict()
        )
        response.raise_for_status()
        return JwtToken(**response.json())


async def register_client(data: RegisterReq) -> JwtToken:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/register",
            json=data.dict()
        )
        response.raise_for_status()
        return JwtToken(**response.json())


async def get_client_profile(client_id: str) -> ProfileResp:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.user_service_url}/profile/{client_id}"
        )
        response.raise_for_status()
        return ProfileResp(**response.json())


async def get_account_id_by_phone(phone_number: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.user_service_url}/find",
            params={
                "phone_number": phone_number
            }
        )
        response.raise_for_status()

        return response.json()['id']
