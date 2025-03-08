from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
import httpx

from app.dependencies import token_check
from app.models.schemas import CredentialsDTO


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get(
    "/token/decode",
    response_model=CredentialsDTO,
    responses={
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def token_decode_endpoint(user_data: dict = Depends(token_check)):
    try:
        return CredentialsDTO(
            user_id=UUID(user_data['user_id']),
            role=user_data['role']
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
