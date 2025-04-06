from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
import httpx

from app.dependencies import token_check
from app.models.schemas import (
    CreditTariffDTO,
    TakeCreditDTO,
    CreditDTO, TakeCreditAPIDTO, LimitDTO, UuidDTO, CreditPaymentDTO, ShortCreditTariffDTO
)
from app.services.credit_service import (
    get_tariffs,
    get_tariff,
    get_credit_limits,
    take_credit,
    get_credit, get_credit_payment_history, get_credits
)

router = APIRouter(
    prefix="/credit",
    tags=["Credit"]
)


@router.get("/tariffs", response_model=List[ShortCreditTariffDTO])
async def api_get_tariffs(_: dict = Depends(token_check)):
    """
    Получает список кредитных тарифов.
    """
    try:
        return await get_tariffs()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("/tariffs/{tariff_id}", response_model=CreditTariffDTO)
async def api_get_tariff(tariff_id: UUID, _: dict = Depends(token_check)):
    """
    Получает данные кредитного тарифа по его ID.
    """
    try:
        return await get_tariff(tariff_id)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("/limit", response_model=LimitDTO)
async def api_get_credit_limits(user_data: dict = Depends(token_check)):
    """
    Получает кредитный лимит для заданного пользователя.
    """
    try:
        return await get_credit_limits(UUID(user_data['user_id']))
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post("", response_model=UuidDTO)
async def api_take_credit(data: TakeCreditDTO, user_data: dict = Depends(token_check)):
    """
    Оформляет заявку на кредит.
    """
    try:
        api_data = TakeCreditAPIDTO(
            **data.dict(),
            user_id=UUID(user_data['user_id'])
        )

        return await take_credit(api_data)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("", response_model=List[CreditDTO])
async def api_get_credits(user_data: dict = Depends(token_check)):
    """
    Получает информацию о кредитах пользователя.
    """
    try:
        return await get_credits(UUID(user_data['user_id']))
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("/concrete/{credit_id}", response_model=CreditDTO)
async def api_get_credit(credit_id: UUID, _: dict = Depends(token_check)):
    """
    Получает информацию о конкретном кредите.
    """
    try:
        return await get_credit(credit_id)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("/history/{credit_id}", response_model=List[CreditPaymentDTO])
async def api_get_history(credit_id: UUID, _: dict = Depends(token_check)):
    """
    Получает историю платежей по кредиту
    """
    try:
        return await get_credit_payment_history(credit_id)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
