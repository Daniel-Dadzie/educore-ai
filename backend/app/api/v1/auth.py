from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import RegisterRequest, UserResponse
from app.services.auth import (
    EmailAlreadyRegisteredError,
    RegistrationConflictError,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: DbSession,
) -> UserResponse:
    try:
        user = register_user(
            db,
            email=str(payload.email),
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            organization_name=payload.organization_name,
        )
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from exc
    except RegistrationConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The registration conflicts with existing data.",
        ) from exc

    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
