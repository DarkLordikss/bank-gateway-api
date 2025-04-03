from fastapi import APIRouter, HTTPException, Depends, Query, Path
import httpx
from typing import List
from app.models.schemas import (
    EmployeeDTO,
    ClientDTO,
    CreateClientReq,
    CreateEmployeeReq,
    LoginEmployeeReq,
    JwtToken
)
from app.services.employee_service import (
    get_employees,
    set_employee_active,
    get_clients,
    set_client_active,
    create_client,
    create_employee,
    login_employee, get_employee_profile
)
from app.dependencies import token_check

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.get(
    "",
    response_model=List[EmployeeDTO],
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


@router.post(
    "/active/{employee_id}",
    responses={
        200: {"description": "Employee status updated"},
        404: {"description": "Employee not found"},
        500: {"description": "Internal server error"}
    }
)
async def employee_set_active(
    employee_id: str = Path(..., description="ID сотрудника"),
    is_active: bool = Query(..., description="Статус активности"),
    user_data: dict = Depends(token_check)
):
    """
    Обновляет статус активности сотрудника.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await set_employee_active(employee_id, is_active)
            return {"message": "Employee status updated successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get(
    "/client",
    response_model=List[ClientDTO],
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
    "/client/active/{client_id}",
    responses={
        200: {"description": "Client status updated"},
        404: {"description": "Client not found"},
        500: {"description": "Internal server error"}
    }
)
async def client_set_active(
    client_id: str = Path(..., description="ID клиента"),
    is_active: bool = Query(..., description="Статус активности"),
    user_data: dict = Depends(token_check)
):
    """
    Обновляет статус активности клиента.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await set_client_active(client_id, is_active)
            return {"message": "Client status updated successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/client/create",
    responses={
        200: {"description": "Client created"},
        400: {"description": "User already exists"},
        500: {"description": "Internal server error"}
    }
)
async def create_client_endpoint(
    data: CreateClientReq,
    user_data: dict = Depends(token_check)
):
    """
    Создает нового клиента.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await create_client(data)
            return {"message": "Client created successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/create",
    responses={
        200: {"description": "Employee created"},
        400: {"description": "User already exists"},
        500: {"description": "Internal server error"}
    }
)
async def create_employee_endpoint(
    data: CreateEmployeeReq,
    user_data: dict = Depends(token_check)
):
    """
    Создает нового сотрудника.
    """
    try:
        if user_data['role'] == 'EMPLOYEE':
            await create_employee(data)
            return {"message": "Employee created successfully"}
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.post(
    "/login",
    response_model=JwtToken,
    responses={
        200: {"description": "Successful login"},
        400: {"description": "Bad credentials"},
        403: {"description": "Access forbidden"},
        404: {"description": "User not found"}
    }
)
async def employee_login(data: LoginEmployeeReq):
    """
    Логин сотрудника.
    """
    try:
        token = await login_employee(data)
        return token
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get(
    "/profile",
    response_model=EmployeeDTO,
    responses={
        401: {"description": "Bad token"},
        404: {"description": "User not found"},
        422: {"description": "Validation error - invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def get_profile(employee_data: dict = Depends(token_check)):
    """
    Эндпойнт получения профиля сотрудника.
    Для доступа требуется валидный токен.
    """
    try:
        if employee_data['role'] == 'EMPLOYEE':
            profile = await get_employee_profile(employee_data['user_id'])
            return profile
        else:
            raise HTTPException(status_code=403, detail='No permission')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
