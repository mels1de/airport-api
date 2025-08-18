from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.auth import UserCreate, UserRead
from app.api.dependencies import get_auth_service

router = APIRouter()

@router.post("/register",response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
        payload: UserCreate,
        auth = Depends(get_auth_service)
):
    try:
        return await auth.register(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )