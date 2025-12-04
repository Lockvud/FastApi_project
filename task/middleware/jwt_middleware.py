from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from utils.jwt import decode_token
from apps.user.store_singleton import user_store
from apps.user.store import user_store_connection

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_paths = [
            "/docs",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh",
            "/docs/oauth2-redirect",
            "/redoc"
        ]

        if any(request.url.path.startswith(path) for path in open_paths):
            request.state.user = None
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Токен не предоставлен")

        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if not payload or payload.get("type") == "refresh":
            raise HTTPException(status_code=403, detail="Недействительный токен")

        username = payload.get("sub")
        from apps.auth.repository import AuthRepository
        with user_store_connection(user_store):
            auth_repo = AuthRepository(user_store)
            user = auth_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=403, detail="Пользователь не найден")

        request.state.user = user
        return await call_next(request)