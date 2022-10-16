from fastapi import APIRouter

from .auth import route_login
from .users import route_users

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
