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
    login_employee
)
from app.dependencies import token_check  # используем для авторизации

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
async def get_employee(employee_id: str = Depends(token_check)):
    """
    Возвращает список сотрудников.
    Требуется действующий JWT-токен сотрудника.
    """
    try:
        employees = await get_employees()
        return employees
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
    current_employee: str = Depends(token_check)
):
    """
    Обновляет статус активности сотрудника.
    """
    try:
        await set_employee_active(employee_id, is_active)
        return {"message": "Employee status updated successfully"}
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
async def get_clients_endpoint(current_employee: str = Depends(token_check)):
    """
    Возвращает список клиентов.
    """
    try:
        clients = await get_clients()
        return clients
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
    current_employee: str = Depends(token_check)
):
    """
    Обновляет статус активности клиента.
    """
    try:
        await set_client_active(client_id, is_active)
        return {"message": "Client status updated successfully"}
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
    current_employee: str = Depends(token_check)
):
    """
    Создает нового клиента.
    """
    try:
        await create_client(data)
        return {"message": "Client created successfully"}
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
    current_employee: str = Depends(token_check)
):
    """
    Создает нового сотрудника.
    """
    try:
        await create_employee(data)
        return {"message": "Employee created successfully"}
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
