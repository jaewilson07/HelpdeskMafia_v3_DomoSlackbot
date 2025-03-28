
from fastapi import APIRouter
from .slack_routes import init_slack_routes

def init_routes(slack_app):
    api_router = APIRouter()
    slack_router = init_slack_routes(slack_app)
    api_router.include_router(slack_router)
    return api_router
