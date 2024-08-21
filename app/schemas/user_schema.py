from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional

class UserCreate(BaseModel):
    handle: str = Field(min_length=1)
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)
    email: EmailStr
    vjudge_handle: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    handle: str
    username: str
    email: EmailStr
    vjudge_handle: Optional[str] = None

    class Config:
        orm_mode = True
