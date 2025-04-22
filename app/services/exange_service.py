from typing import List
from app.core.config import settings
from app.models.schemas import DoExchangeResp, DoExchangeReq, UserDTO
from app.utils.http_retry import http_request_with_retry


async def get_currencies() -> List[UserDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.exchange_service_url}/currencies"
    )
    data = response.json()
    return data


async def do_exchange(data: DoExchangeReq) -> DoExchangeResp:
    response = await http_request_with_retry(
        method="post",
        url=f"{settings.exchange_service_url}/exchange",
        json=data.dict()
    )
    data = response.json()
    return DoExchangeResp(
        amount=data['amount'],
        rate=data['rate']
    )
