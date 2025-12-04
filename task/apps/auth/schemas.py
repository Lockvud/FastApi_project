from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginSchema(BaseModel):
    username: str
    password: str


class RefreshSchema(BaseModel):
    refresh_token: str