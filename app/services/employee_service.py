import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import (
    EmployeeDTO,
    ClientDTO,
    CreateClientReq,
    CreateEmployeeReq,
    LoginEmployeeReq,
    JwtToken
)


async def get_employees() -> List[EmployeeDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_url}/employee")
        response.raise_for_status()
        data = response.json()
        return [EmployeeDTO(**item) for item in data]


async def set_employee_active(employee_id: str, is_active: bool) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/active/{employee_id}",
            params={"is_active": is_active}
        )
        response.raise_for_status()


async def get_clients() -> List[ClientDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_url}/employee/client")
        response.raise_for_status()
        data = response.json()
        return [ClientDTO(**item) for item in data]


async def set_client_active(client_id: str, is_active: bool) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/client/active/{client_id}",
            params={"is_active": is_active}
        )
        response.raise_for_status()


async def create_client(data: CreateClientReq) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/client/create",
            json=data.dict()
        )
        response.raise_for_status()


async def create_employee(data: CreateEmployeeReq) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/create",
            json=data.dict()
        )
        response.raise_for_status()


async def login_employee(data: LoginEmployeeReq) -> JwtToken:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/employee/login",
            json=data.dict()
        )
        response.raise_for_status()
        return JwtToken(**response.json())
