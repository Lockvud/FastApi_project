from fastapi import HTTPException
from apps.auth.repository import AuthRepository
from utils.security import verify_password, hash_password
from utils.jwt import create_access_token, create_refresh_token
from apps.user.schemas import UserCreate
from apps.user.models import UserOut


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    def authenticate_user(self, username: str, password: str):
        db_user = self.auth_repo.get_user_by_username(username)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    def login(self, username: str, password: str):
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Неверные учетные данные")

        payload = {"sub": user.username}
        access = create_access_token(payload)
        refresh = create_refresh_token(payload)

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
        }

    def register(self, payload: UserCreate):
        if self.auth_repo.get_user_by_username(payload.username):
            raise HTTPException(status_code=400, detail="Username уже существует")

        hashed = hash_password(payload.password)

        created = self.auth_repo.user_repo.create_user(payload, hashed)
        return UserOut(**created.model_dump())
