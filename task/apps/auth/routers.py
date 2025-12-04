from fastapi import APIRouter, Depends, HTTPException
from apps.auth.schemas import LoginSchema, Token, RefreshSchema
from apps.auth.services import AuthService
from apps.auth.repository import AuthRepository
from apps.user.store import user_store_connection
from apps.user.store_singleton import user_store
from apps.user.schemas import UserCreate
from apps.user.models import UserOut
from utils.jwt import decode_token, create_access_token, create_refresh_token

router = APIRouter()


def get_auth_service():
    with user_store_connection(user_store):
        repo = AuthRepository(user_store)
        svc = AuthService(repo)
        yield svc


@router.post("/register")
def register(payload: UserCreate, svc: AuthService = Depends(get_auth_service)):
    return svc.register(payload)


@router.post("/login", response_model=Token)
def login(payload: LoginSchema, svc: AuthService = Depends(get_auth_service)):
    return svc.login(payload.username, payload.password)


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshSchema, svc: AuthService = Depends(get_auth_service)):

    refresh_token = payload.refresh_token
    decoded = decode_token(refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    sub = decoded.get("sub")
    access = create_access_token({"sub": sub})
    refresh_t = create_refresh_token({"sub": sub})

    return {"access_token": access, "refresh_token": refresh_t, "token_type": "bearer"}

