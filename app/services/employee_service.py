from typing import List
from app.core.config import settings
from app.models.schemas import CreateUserReq, UserDTO
from app.utils.http_retry import http_request_with_retry


async def get_employees() -> List[UserDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.user_service_url}/employee"
    )
    data = response.json()
    return [UserDTO(**item) for item in data]


async def get_users() -> List[UserDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.user_service_url}/employee/users"
    )
    data = response.json()
    return [UserDTO(**item) for item in data]


async def get_clients() -> List[UserDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.user_service_url}/employee/clients"
    )
    data = response.json()
    return [UserDTO(**item) for item in data]


async def set_user_active(user_id: str, is_active: bool) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.user_service_url}/employee/user/active/{user_id}",
        params={"is_active": is_active}
    )


async def create_user(data: CreateUserReq) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.user_service_url}/employee/create",
        json=data.dict()
    )
