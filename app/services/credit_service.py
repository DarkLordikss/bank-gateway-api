from typing import List
from uuid import UUID

import httpx
from app.core.config import settings
from app.models.schemas import CreditTariffDTO, CreditDTO, CreateCreditTariffAPIDTO, EditCreditTariffDTO, \
    TakeCreditAPIDTO, UuidDTO, LimitDTO, CreditPaymentDTO, ShortCreditTariffDTO, MessageDTO


async def get_tariffs() -> List[ShortCreditTariffDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/tariffs"
        )
        response.raise_for_status()
        return [ShortCreditTariffDTO(**tariff) for tariff in response.json()['tariffs']]


async def get_tariff(tariff_id: UUID) -> CreditTariffDTO:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/tariffs/{tariff_id}"
        )
        response.raise_for_status()
        return [CreditTariffDTO(**tariff) for tariff in response.json()['tariff']][0]


async def add_tariff(data: CreateCreditTariffAPIDTO) -> UuidDTO:
    async with httpx.AsyncClient() as client:
        data = data.dict()
        data['employee_id'] = str(data['employee_id'])

        response = await client.post(
            f"{settings.credit_service_url}/tariffs",
            json=data
        )
        response.raise_for_status()
        return UuidDTO(id=UUID(response.json()['tariff_id']))


async def edit_tariff(data: EditCreditTariffDTO, tariff_id: UUID) -> UuidDTO:
    async with httpx.AsyncClient() as client:
        data = data.dict()
        if data['name'] is None: del data['name']
        if data['interest_rate'] is None: del data['interest_rate']
        if data['months_count'] is None: del data['months_count']

        response = await client.put(
            f"{settings.credit_service_url}/tariffs/{tariff_id}",
            json=data
        )
        response.raise_for_status()
        return UuidDTO(id=UUID(response.json()['updated_id']))


async def delete_tariff(tariff_id: UUID) -> UuidDTO:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{settings.credit_service_url}/tariffs/{tariff_id}"
        )
        response.raise_for_status()
        return UuidDTO(id=UUID(response.json()['deleted_id']))


async def get_credit_limits(user_id: UUID) -> LimitDTO:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/credit-limit/{user_id}"
        )
        response.raise_for_status()
        return LimitDTO(limit=float(response.json()['limit']))


async def take_credit(data: TakeCreditAPIDTO) -> MessageDTO:
    async with httpx.AsyncClient() as client:
        data = data.dict()
        data['user_id'] = str(data['user_id'])
        data['tariff_id'] = str(data['tariff_id'])
        data['write_off_account_id'] = str(data['write_off_account_id'])

        response = await client.post(
            f"{settings.credit_service_url}/credit",
            json=data
        )
        response.raise_for_status()

        response_data = response.json()

        if response_data['success']:
            return MessageDTO(message='Success')
        else:
            return MessageDTO(message='Not approved')


async def get_credit(credit_id: UUID) -> CreditDTO:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/credit/{credit_id}"
        )
        response.raise_for_status()
        return CreditDTO(**response.json()['credit'][0])


async def get_credits(user_id: UUID) -> List[CreditDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/credits/{user_id}"
        )
        response.raise_for_status()
        print(response.json())
        return [CreditDTO(**credit) for credit in response.json()['credits']]


async def get_credit_payment_history(credit_id: UUID) -> List[CreditPaymentDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.credit_service_url}/get-payment-history/{credit_id}"
        )
        response.raise_for_status()
        return [CreditPaymentDTO(**payment) for payment in response.json()['credit_payments']]
