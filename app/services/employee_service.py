import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import (
    CreateUserReq, UserDTO
)


async def get_employees() -> List[UserDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_url}/employee")
        response.raise_for_status()
        data = response.json()
        return [UserDTO(**item) for item in data]


async def get_users() -> List[UserDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_url}/employee/users")
        response.raise_for_status()
        data = response.json()
        return [UserDTO(**item) for item in data]


async def get_clients() -> List[UserDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_url}/employee/clients")
        response.raise_for_status()
        data = response.json()
        return [UserDTO(**item) for item in data]


async def set_user_active(user_id: str, is_active: bool) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/user/active/{user_id}",
            params={"is_active": is_active}
        )
        response.raise_for_status()


async def create_user(data: CreateUserReq) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/create",
            json=data.dict()
        )
        response.raise_for_status()
