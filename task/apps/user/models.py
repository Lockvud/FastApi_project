from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
