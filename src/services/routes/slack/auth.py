"""
This module provides a function to validate the bot's authentication with Slack.

It uses the Slack API's `auth.test` method to verify the bot's credentials.
"""


async def validate_bot_auth(client=None):
    """
    Validates the bot's authentication with Slack.

    Args:
        client: The Slack client instance. If not provided, it initializes one.

    Returns:
        dict: A dictionary containing bot user ID, username, and workspace information,
              or an error message if validation fails.
    """
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
