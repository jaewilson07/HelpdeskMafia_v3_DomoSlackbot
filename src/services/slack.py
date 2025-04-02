async def validate_bot_auth():
    from src import slack_app

    try:
        auth_test = await slack_app.client.auth_test()

        return {
            "bot_user_id": auth_test["user_id"],
            "bot_username": auth_test["user"],
            "workspace": auth_test["team"],
        }
    except Exception as e:
        return {"error": str(e)}
