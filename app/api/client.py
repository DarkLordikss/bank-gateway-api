import httpx
from fastapi import APIRouter, HTTPException, Depends

from app.dependencies import token_check
from app.models.schemas import LoginReq, RegisterClientReq, JwtToken, ProfileResp
from app.services.client_service import login_client, register_client, get_client_profile

router = APIRouter(
    prefix="/client",
    tags=["Client"]
)


@router.post(
    "/login",
    response_model=JwtToken,
    responses={
        400: {"description": "User bad credentials"},
        422: {"description": "Validation error - invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def login(data: LoginReq):
    try:
        token = await login_client(data)
        return token
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post(
    "/register",
    response_model=JwtToken,
    responses={
        400: {"description": "User already exists or bad request"},
        422: {"description": "Validation error - invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def register(data: RegisterClientReq):
    try:
        token = await register_client(data)
        return token
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get(
    "/profile",
    response_model=ProfileResp,
    responses={
        401: {"description": "Bad token"},
        404: {"description": "User not found"},
        422: {"description": "Validation error - invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def get_profile(client_data: dict = Depends(token_check)):
    """
    Эндпойнт получения профиля пользователя.
    Для доступа требуется валидный токен.
    """
    try:
        profile = await get_client_profile(client_data['user_id'])
        return profile
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
