from fastapi import FastAPI
from routers.api_v1_router import api_v1_router
from middleware.jwt_middleware import JWTMiddleware

app = FastAPI(
    title="User + Auth API",
    description="Практическая работа FastAPI",
    version="1.0.0",
)

# подключаем все маршруты
app.include_router(api_v1_router)
app.add_middleware(JWTMiddleware)

@app.get("/")
def root():
    return {"message": "API is running"}
