from fastapi import APIRouter, HTTPException, Depends, Query, Path
import httpx
from typing import List
from app.models.schemas import (
    DoExchangeResp, DoExchangeReq
)
from app.dependencies import token_check
from app.services.exange_service import get_currencies, do_exchange

router = APIRouter(
    prefix="/currency",
    tags=["Currency"]
)


@router.get(
    "/currencies",
    response_model=List[str],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def get_currencies_endpoint(_: dict = Depends(token_check)):
    """
    Возвращает список валют.
    """
    try:
        currencies = await get_currencies()
        return currencies
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/exchange",
    response_model=DoExchangeResp,
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def exchange_currency(
    data: DoExchangeReq,
    _: dict = Depends(token_check)
):
    """
    Конвертирует валюты.
    """
    try:
        resp = await do_exchange(data)
        return resp
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
