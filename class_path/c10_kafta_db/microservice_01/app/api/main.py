from fastapi import APIRouter
from app.api.routes import users , login

api_router = APIRouter()

# api_router.include_router(todos.router, tags=["Todos"])
# api_router.include_router(users.router, tags=["Users"])
# api_router.include_router(login.router, tags=["Login"])
api_router.include_router(login.router, prefix="/api/v1", tags=["Login user"])
api_router.include_router(users.router, prefix="/api/v1", tags=["Users Operations"])
