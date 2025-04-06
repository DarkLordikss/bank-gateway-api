from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, Path
import httpx
from typing import List
from app.models.schemas import (
    CreateUserReq, UserDTO, CreateCreditTariffDTO, CreateCreditTariffAPIDTO, EditCreditTariffDTO, UuidDTO
)
from app.services.credit_service import edit_tariff, add_tariff, delete_tariff
from app.services.employee_service import (
    get_employees,
    get_clients,
    set_user_active,
    create_user, get_users
)
from app.dependencies import token_check

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.get(
    "",
    response_model=List[UserDTO],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def get_employee(user_data: dict = Depends(token_check)):
    """
    Возвращает список сотрудников.
    Требуется действующий JWT-токен сотрудника.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            employees = await get_employees()
            return employees
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get(
    "/users",
    response_model=List[UserDTO],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def get_users_endpoint(user_data: dict = Depends(token_check)):
    """
    Возвращает список пользователей.
    Требуется действующий JWT-токен сотрудника.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            users = await get_users()
            return users
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get(
    "/clients",
    response_model=List[UserDTO],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def get_clients_endpoint(user_data: dict = Depends(token_check)):
    """
    Возвращает список клиентов.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            clients = await get_clients()
            return clients
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/user/active/{user_id}",
    responses={
        200: {"description": "User status updated"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    }
)
async def user_set_active(
    user_id: str = Path(..., description="ID пользователя"),
    is_active: bool = Query(..., description="Статус активности"),
    user_data: dict = Depends(token_check)
):
    """
    Обновляет статус активности пользователя.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await set_user_active(user_id, is_active)
            return {"message": "User status updated successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/client/create",
    responses={
        200: {"description": "User created"},
        400: {"description": "User already exists"},
        500: {"description": "Internal server error"}
    }
)
async def create_user_endpoint(
    data: CreateUserReq,
    user_data: dict = Depends(token_check)
):
    """
    Создает нового пользователя.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await create_user(data)
            return {"message": "User created successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post("/tariffs", response_model=UuidDTO)
async def api_add_tariff(data: CreateCreditTariffDTO, user_data: dict = Depends(token_check)):
    """
    Добавляет новый кредитный тариф.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            api_data = CreateCreditTariffAPIDTO(
                **data.dict(),
                employee_id=UUID(user_data['user_id'])
            )

            return await add_tariff(api_data)
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.put("/tariffs/{tariff_id}", response_model=UuidDTO)
async def api_edit_tariff(tariff_id: UUID, data: EditCreditTariffDTO, user_data: dict = Depends(token_check)):
    """
    Редактирует существующий кредитный тариф.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            return await edit_tariff(data, tariff_id)
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.delete("/tariffs/{tariff_id}", response_model=UuidDTO)
async def api_delete_tariff(tariff_id: UUID, user_data: dict = Depends(token_check)):
    """
    Удаляет кредитный тариф по его ID.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            return await delete_tariff(tariff_id)
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
