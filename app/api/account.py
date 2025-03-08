from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import List
import httpx

from app.dependencies import token_check
from app.models.schemas import AccountDTO, TransactionDTO
from app.services.account_service import (
    get_client_accounts,
    create_debit_account,
    withdraw_account,
    get_transactions,
    deposit_account,
    delete_account,
)

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
        accounts = await get_client_accounts(str(client_id), user_data['role'])
        return accounts
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
async def create_account(user_data: dict = Depends(token_check)):
    try:
        await create_debit_account(user_data['user_id'], user_data['role'])
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
