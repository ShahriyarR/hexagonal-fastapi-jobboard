from fastapi import APIRouter

from src.jobboard.adapters.entrypoints.api.v1 import (
    route_jobs,
    route_login,
    route_users,
)

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
