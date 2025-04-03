async def validate_bot_auth(client=None):
    if not client:
        from src import slack_app

        client = slack_app.client

    try:
        auth_test = await client.auth_test()

        return {
            "bot_user_id": auth_test["user_id"],
            "bot_username": auth_test["user"],
            "workspace": auth_test["team"],
        }
    except Exception as e:
        return {"error": str(e)}
