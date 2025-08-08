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

    class Config:
        orm_mode = True
