import asyncio
import json
import uuid

import httpx
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from app.core.config import settings
from app.models.schemas import AccountDTO, TransactionDTO
import aio_pika
from aio_pika import Message, DeliveryMode

from app.utils.http_retry import http_request_with_retry


RETRIES = settings.retries
WAIT_SECONDS = settings.wait_seconds


@retry(stop=stop_after_attempt(RETRIES), wait=wait_fixed(WAIT_SECONDS), retry=retry_if_exception_type(aio_pika.exceptions.AMQPException))
async def _transfer_funds(transfer_data: dict) -> str:
    try:
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_account_host,
            port=int(settings.rabbitmq_account_port),
            login=settings.rabbitmq_account_login,
            password=settings.rabbitmq_account_password
        )
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(settings.transfer_queue_name, durable=True)
            callback_queue = await channel.declare_queue(exclusive=True)

            correlation_id = str(uuid.uuid4())
            message_body = json.dumps(transfer_data).encode()
            message = Message(
                message_body,
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            await channel.default_exchange.publish(
                message,
                routing_key=settings.transfer_queue_name
            )

            await asyncio.sleep(3)
            try:
                response_message = await asyncio.wait_for(callback_queue.get(), timeout=3)
                response_body = response_message.body.decode()
                response_data = json.loads(response_body)
                if not response_data.get("result"):
                    return f"Transfer failed"
                return f"Transfer successful"
            except (asyncio.TimeoutError, aio_pika.exceptions.QueueEmpty):
                return "Transfer is being processed"
    except Exception as exc:
        raise Exception(f"Transfer failed: {exc}")


async def get_client_accounts(client_id: str, role: str) -> List[AccountDTO]:
    response = await http_request_with_retry(
        method="get",
        url=f"{settings.account_service_url}/accounts",
        params={"clientId": client_id, "role": role}
    )
    data = response.json()
    return [AccountDTO(**item) for item in data]


async def create_debit_account(currency_type: str, client_id: str, role: str) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.account_service_url}/accounts",
        params={"clientId": client_id, "role": role, "currencyType": currency_type}
    )


async def withdraw_account(account_id: str, client_id: str, amount: float, role: str) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.account_service_url}/accounts/{account_id}/withdraw",
        params={"clientId": client_id, "amount": amount, "role": role}
    )


async def get_transactions(account_id: str, client_id: str, role: str) -> List[TransactionDTO]:
    response = await http_request_with_retry(
        method="post",
        url=f"{settings.account_service_url}/accounts/{account_id}/transactions",
        params={"clientId": client_id, "role": role}
    )
    data = response.json()
    return [TransactionDTO(**item) for item in data]


async def deposit_account(account_id: str, client_id: str, amount: float, role: str) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.account_service_url}/accounts/{account_id}/deposit",
        params={"clientId": client_id, "amount": amount, "role": role}
    )


async def delete_account(account_id: str, client_id: str, role: str) -> None:
    await http_request_with_retry(
        method="delete",
        url=f"{settings.account_service_url}/accounts/{account_id}",
        params={"clientId": client_id, "role": role}
    )


async def set_primary_account(account_id: str, client_id: str, role: str) -> None:
    await http_request_with_retry(
        method="post",
        url=f"{settings.account_service_url}/accounts/{account_id}/primary",
        params={"clientId": client_id, "role": role}
    )


async def transfer_funds_by_account(from_account_id: str, to_account_id: str, client_id: str, amount: float,
                                    role: str) -> str:
    transfer_data = {
        "from_account": from_account_id,
        "to_account": to_account_id,
        "from_clientId": client_id,
        "amount": amount,
        "role": role
    }
    return await _transfer_funds(transfer_data)


async def transfer_funds_by_client(from_account_id: str, to_client_id: str, client_id: str, amount: float,
                                   role: str) -> str:
    transfer_data = {
        "from_account": from_account_id,
        "to_clientId": to_client_id,
        "from_clientId": client_id,
        "amount": amount,
        "role": role
    }
    return await _transfer_funds(transfer_data)


async def transfer_funds_by_account_number(from_account_id: str, to_account_number: str, client_id: str, amount: float,
                                           role: str) -> str:
    transfer_data = {
        "from_account": from_account_id,
        "to_account_number": to_account_number,
        "from_clientId": client_id,
        "amount": amount,
        "role": role
    }
    return await _transfer_funds(transfer_data)
