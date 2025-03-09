import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import AccountDTO, TransactionDTO


async def get_client_accounts(client_id: str, role: str) -> List[AccountDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.account_service_url}/accounts",
            params={
                "clientId": client_id,
                "role": role
            }
        )
        response.raise_for_status()
        data = response.json()
        return [AccountDTO(**item) for item in data]


async def create_debit_account(client_id: str, role: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts",
            params={
                "clientId": client_id,
                "role": role
            }
        )
        response.raise_for_status()


async def withdraw_account(account_id: str, client_id: str, amount: float, role: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{account_id}/withdraw",
            params={
                "clientId": client_id,
                "amount": amount,
                "role": role
            }
        )
        response.raise_for_status()


async def get_transactions(account_id: str, client_id: str, role: str) -> List[TransactionDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{account_id}/transactions",
            params={
                "clientId": client_id,
                "role": role
            }
        )
        response.raise_for_status()
        data = response.json()
        return [TransactionDTO(**item) for item in data]


async def deposit_account(account_id: str, client_id: str, amount: float, role: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{account_id}/deposit",
            params={
                "clientId": client_id,
                "amount": amount,
                "role": role
            }
        )
        response.raise_for_status()


async def delete_account(account_id: str, client_id: str, role: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{settings.account_service_url}/accounts/{account_id}",
            params={
                "clientId": client_id,
                "role": role
            }
        )
        response.raise_for_status()


async def set_primary_account(account_id: str, client_id: str, role: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{account_id}/primary",
            params={
                "clientId": client_id,
                "role": role
            }
        )
        response.raise_for_status()
