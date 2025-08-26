from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.deps import get_current_user
from app.domain.auth import UserCreate, UserRead, TokenRefreshIn, TokenPair
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
@router.post("/login",response_model=TokenPair)
async def login(form: OAuth2PasswordRequestForm = Depends(), auth = Depends(get_auth_service)):
    try:
        return await auth.login(email=form.username, password=form.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(body: TokenRefreshIn, auth=Depends(get_auth_service)):
    try:
        return await auth.refresh(body.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
@router.get("/me", response_model=UserRead)
async def get_me(user=Depends(get_current_user)):
    return user