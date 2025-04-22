from typing import List
from uuid import UUID

from app.core.config import settings
from app.models.schemas import CreditTariffDTO, CreditDTO, CreateCreditTariffAPIDTO, EditCreditTariffDTO, \
    TakeCreditAPIDTO, UuidDTO, LimitDTO, CreditPaymentDTO, ShortCreditTariffDTO, MessageDTO
from app.utils.http_retry import http_request_with_retry


async def get_tariffs() -> List[ShortCreditTariffDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/tariffs"
    )
    return [ShortCreditTariffDTO(**tariff) for tariff in response.json()['tariffs']]


async def get_tariff(tariff_id: UUID) -> CreditTariffDTO:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/tariffs/{tariff_id}"
    )
    return [CreditTariffDTO(**tariff) for tariff in response.json()['tariff']][0]


async def add_tariff(data: CreateCreditTariffAPIDTO) -> UuidDTO:
    data = data.dict()
    data['employee_id'] = str(data['employee_id'])
    response = await http_request_with_retry(
        method="post",
        url=f"{settings.credit_service_url}/tariffs",
        json=data
    )
    return UuidDTO(id=UUID(response.json()['tariff_id']))


async def edit_tariff(data: EditCreditTariffDTO, tariff_id: UUID) -> UuidDTO:
    data = data.dict()
    if data['name'] is None: del data['name']
    if data['interest_rate'] is None: del data['interest_rate']
    if data['months_count'] is None: del data['months_count']

    response = await http_request_with_retry(
        method="put",
        url=f"{settings.credit_service_url}/tariffs/{tariff_id}",
        json=data
    )
    return UuidDTO(id=UUID(response.json()['updated_id']))


async def delete_tariff(tariff_id: UUID) -> UuidDTO:
    response = await http_request_with_retry(
        method="delete",
        url=f"{settings.credit_service_url}/tariffs/{tariff_id}"
    )
    return UuidDTO(id=UUID(response.json()['deleted_id']))


async def get_credit_limits(user_id: UUID) -> LimitDTO:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/credit-limit/{user_id}"
    )
    return LimitDTO(limit=float(response.json()['limit']))


async def take_credit(data: TakeCreditAPIDTO) -> MessageDTO:
    data = data.dict()
    data['user_id'] = str(data['user_id'])
    data['tariff_id'] = str(data['tariff_id'])
    data['write_off_account_id'] = str(data['write_off_account_id'])

    response = await http_request_with_retry(
        method="post",
        url=f"{settings.credit_service_url}/credit",
        json=data
    )

    response_data = response.json()

    if response_data['success']:
        return MessageDTO(message='Success')
    else:
        return MessageDTO(message='Not approved')


async def get_credit(credit_id: UUID) -> CreditDTO:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/credit/{credit_id}"
    )
    return CreditDTO(**response.json()['credit'][0])


async def get_credits(user_id: UUID) -> List[CreditDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/credits/{user_id}"
    )
    return [CreditDTO(**credit) for credit in response.json()['credits']]


async def get_credit_payment_history(credit_id: UUID) -> List[CreditPaymentDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.credit_service_url}/get-payment-history/{credit_id}"
    )
    return [CreditPaymentDTO(**payment) for payment in response.json()['credit_payments']]
