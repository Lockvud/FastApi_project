from fastapi import APIRouter
from apps.user.routers import router as user_router
from apps.auth.routers import router as auth_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(user_router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])



