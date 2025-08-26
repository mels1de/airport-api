from pydantic import BaseModel,Field,EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6)

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    role: str = "user"

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshIn(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True
