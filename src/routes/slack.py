from fastapi import APIRouter
from src.services.slack import validate_bot_auth

router = APIRouter(prefix="/slack", tags=["slack"])


@router.get("/auth-test")
async def auth_test():
    return await validate_bot_auth()
