from fastapi import APIRouter
from .slack import init_slack_routes
from .base import router as base_router


def init_routes(slack_app):
    api_router = APIRouter()
    slack_router = init_slack_routes(slack_app)
    api_router.include_router(base_router)
    api_router.include_router(slack_router)
    return api_router
