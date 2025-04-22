from app.core.config import settings
from app.models.schemas import LoginReq, RegisterReq, JwtToken, ProfileResp
from app.utils.http_retry import http_request_with_retry


async def login_client(data: LoginReq) -> JwtToken:
    response = await http_request_with_retry(
        method="post",
        url=f"{settings.user_service_url}/login",
        json=data.dict()
    )
    return JwtToken(**response.json())


async def register_client(data: RegisterReq) -> JwtToken:
    response = await http_request_with_retry(
        method="post",
        url=f"{settings.user_service_url}/register",
        json=data.dict()
    )
    return JwtToken(**response.json())


async def get_client_profile(client_id: str) -> ProfileResp:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.user_service_url}/profile/{client_id}"
    )
    return ProfileResp(**response.json())


async def get_account_id_by_phone(phone_number: str) -> None:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.user_service_url}/find",
        params={"phone_number": phone_number}
    )
    return response.json()['id']
