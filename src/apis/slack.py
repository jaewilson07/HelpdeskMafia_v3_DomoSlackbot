from fastapi import APIRouter
from services.routes.slack.auth import validate_bot_auth

router = APIRouter(prefix="/slack", tags=["slack"])


@router.get("/auth-test")
async def auth_test():
    return await validate_bot_auth()
