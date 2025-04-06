from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import List
import httpx

from app.dependencies import token_check
from app.models.schemas import AccountDTO, TransactionDTO, TransferByAccountNumberReq, \
    TransferByPhoneNumberReq, TransferByAccountReq
from app.services.account_service import (
    get_client_accounts,
    create_debit_account,
    withdraw_account,
    get_transactions,
    deposit_account,
    delete_account, set_primary_account, transfer_funds_by_account_number, transfer_funds_by_client,
    transfer_funds_by_account,
)
from app.services.client_service import get_account_id_by_phone

router = APIRouter(
    prefix="/accounts",
    tags=["Account"]
)


@router.get(
    "",
    response_model=List[AccountDTO],
    responses={
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def client_accounts(user_data: dict = Depends(token_check)):
    try:
        accounts = await get_client_accounts(user_data['user_id'], user_data['role'])
        return accounts
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get(
    "/concrete",
    response_model=List[AccountDTO],
    responses={
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def client_accounts_concrete(client_id: UUID, user_data: dict = Depends(token_check)):
    try:
        if user_data['role'] == 'EMPLOYEE':
            accounts = await get_client_accounts(str(client_id), user_data['role'])
            return accounts
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "",
    responses={
        200: {"description": "Account created"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def create_account(currency_type: str, user_data: dict = Depends(token_check)):
    try:
        await create_debit_account(currency_type, user_data['user_id'], user_data['role'])
        return {"message": "Account created successfully"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/{account_id}/withdraw",
    responses={
        400: {"description": "Insufficient funds"},
        403: {"description": "Client is not owner of account"},
        404: {"description": "Account not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def withdraw(
        account_id: str = Path(..., description="ID счета"),
        user_data: dict = Depends(token_check),
        amount: float = Query(..., description="Сумма для снятия")
):
    try:
        await withdraw_account(account_id, user_data['user_id'], amount, user_data['role'])
        return {"message": "Withdrawal successful"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/{account_id}/transactions",
    response_model=List[TransactionDTO],
    responses={
        403: {"description": "Client is not owner of account"},
        404: {"description": "Account not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def transactions(
        account_id: str = Path(..., description="ID счета"),
        user_data: dict = Depends(token_check)
):
    try:
        txs = await get_transactions(account_id, user_data['user_id'], user_data['role'])
        return txs
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/{account_id}/deposit",
    responses={
        403: {"description": "Client is not owner of account"},
        404: {"description": "Account not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def deposit(
        account_id: str = Path(..., description="ID счета"),
        user_data: dict = Depends(token_check),
        amount: float = Query(..., description="Сумма для пополнения")
):
    try:
        await deposit_account(account_id, user_data['user_id'], amount, user_data['role'])
        return {"message": "Deposit successful"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.delete(
    "/{account_id}",
    responses={
        400: {"description": "Account not empty"},
        403: {"description": "Client is not owner of account"},
        404: {"description": "Account not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def close_account(
        account_id: str = Path(..., description="ID счета"),
        user_data: dict = Depends(token_check)
):
    try:
        await delete_account(account_id, user_data['user_id'], user_data['role'])
        return {"message": "Account closed successfully"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/{account_id}/set_primary",
    responses={
        200: {"description": "Primary account set successful"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def set_primary_account_endpoint(account_id: str = Path(..., description="ID счета"),
                                       user_data: dict = Depends(token_check)
                                       ):
    try:
        await set_primary_account(account_id, user_data['user_id'], user_data['role'])
        return {"message": "Primary account set successful"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/{account_id}/transfer/by-account",
    responses={
        200: {"description": "Transfer processed successfully or is in processing"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def transfer_by_account(
    account_id: UUID = Path(..., description="ID счета отправителя"),
    data: TransferByAccountReq = Depends(),
    user_data: dict = Depends(token_check)
):
    try:
        message = await transfer_funds_by_account(
            from_account_id=str(account_id),
            to_account_id=str(data.to_account),
            client_id=user_data['user_id'],
            amount=data.amount,
            role=user_data['role']
        )
        return {"message": message}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "/{account_id}/transfer/by-phone-number",
    responses={
        200: {"description": "Transfer processed successfully or is in processing"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def transfer_by_phone_number(
    account_id: UUID = Path(..., description="ID счета отправителя"),
    data: TransferByPhoneNumberReq = Depends(),
    user_data: dict = Depends(token_check)
):
    try:
        user_id = await get_account_id_by_phone(data.phone_number)

        message = await transfer_funds_by_client(
            from_account_id=str(account_id),
            to_client_id=str(user_id),
            client_id=user_data['user_id'],
            amount=data.amount,
            role=user_data['role']
        )
        return {"message": message}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "/{account_id}/transfer/by-account-number",
    responses={
        200: {"description": "Transfer processed successfully or is in processing"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def transfer_by_account_number(
    account_id: UUID = Path(..., description="ID счета отправителя"),
    data: TransferByAccountNumberReq = Depends(),
    user_data: dict = Depends(token_check)
):
    try:
        message = await transfer_funds_by_account_number(
            from_account_id=str(account_id),
            to_account_number=str(data.to_account_number),
            client_id=user_data['user_id'],
            amount=data.amount,
            role=user_data['role']
        )
        return {"message": message}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
