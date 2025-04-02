from fastapi import APIRouter
from .slack import router as slack_router
from .base import router as base_router


def init_routes():
    api_router = APIRouter()

    api_router.include_router(base_router)
    api_router.include_router(slack_router)

    return api_router
