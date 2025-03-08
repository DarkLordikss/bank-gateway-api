from uuid import UUID

from fastapi import APIRouter, HTTPException
import httpx

from app.models.schemas import CredentialsDTO
from app.services.auth_service import token_decode

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
async def token_decode_endpoint(token: str):
    try:
        credentials = await token_decode(token)

        return CredentialsDTO(
            user_id=UUID(credentials['user_id']),
            role=credentials['role']
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
