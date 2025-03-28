
from slack_bolt.async_app import AsyncAck, AsyncRespond
from logging import Logger

async def auth_test_command_callback(command, ack: AsyncAck, respond: AsyncRespond, client, logger: Logger):
    try:
        await ack()
        # Test the bot's auth
        auth_test = await client.auth_test()
        # Get bot scopes
        auth_info = await client.auth_info()
        
        response = (
            f"Bot User ID: {auth_test['user_id']}\n"
            f"Bot Username: {auth_test['user']}\n"
            f"Bot is in workspace: {auth_test['team']}\n"
            f"Scopes: {auth_info['scope']}"
        )
        
        await respond(response)
    except Exception as e:
        logger.error(f"Error testing auth: {e}")
