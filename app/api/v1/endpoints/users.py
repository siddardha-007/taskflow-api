from fastapi import APIRouter, HTTPException, status

from app.api.deps import DbSession
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(data: UserCreate, db: DbSession):
    try:
        return UserService(db).create_user(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession):
    try:
        return UserService(db).get_user(user_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc