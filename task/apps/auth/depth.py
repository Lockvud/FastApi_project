from fastapi import Header, HTTPException
from apps.user.store_singleton import user_store
from apps.user.store import user_store_connection
from apps.auth.repository import AuthRepository
from utils.jwt import decode_token


def get_current_user(
    authorization: str = Header(None)
):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Не прошел проверку подлинности")

    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Недействительный токен")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Недействительный токен")

    with user_store_connection(user_store):
        auth_repo = AuthRepository(user_store)
        user = auth_repo.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user