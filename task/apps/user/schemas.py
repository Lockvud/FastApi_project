from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class BulkUsersCreate(BaseModel):
    users: List[UserCreate]


class UserLogin(BaseModel):
    username: str
    password: str
