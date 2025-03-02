import httpx
from typing import List
from app.core.config import settings
from app.models.schemas import AccountDTO, TransactionDTO


async def get_client_accounts(clientId: str) -> List[AccountDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.account_service_url}/accounts",
            params={"clientId": clientId}
        )
        response.raise_for_status()
        data = response.json()
        return [AccountDTO(**item) for item in data]


async def create_debit_account(clientId: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts",
            params={"clientId": clientId}
        )
        response.raise_for_status()


async def withdraw_account(accountId: str, clientId: str, amount: float) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{accountId}/withdraw",
            params={"clientId": clientId, "amount": amount}
        )
        response.raise_for_status()


async def get_transactions(accountId: str, clientId: str) -> List[TransactionDTO]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{accountId}/transactions",
            params={"clientId": clientId}
        )
        response.raise_for_status()
        data = response.json()
        return [TransactionDTO(**item) for item in data]


async def deposit_account(accountId: str, clientId: str, amount: float) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.account_service_url}/accounts/{accountId}/deposit",
            params={"clientId": clientId, "amount": amount}
        )
        response.raise_for_status()


async def delete_account(accountId: str, clientId: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{settings.account_service_url}/accounts/{accountId}",
            params={"clientId": clientId}
        )
        response.raise_for_status()
