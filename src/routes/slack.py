from fastapi import APIRouter

router = APIRouter(prefix="/slack", tags=["slack"])


@router.get("/auth-test")
async def auth_test():
    from src import slack_app

    try:
        auth_test = await slack_app.client.auth_test()
        auth_info = await slack_app.client.auth_info()

        return {
            "bot_user_id": auth_test["user_id"],
            "bot_username": auth_test["user"],
            "workspace": auth_test["team"],
            "scopes": auth_info["scope"],
        }
    except Exception as e:
        return {"error": str(e)}
