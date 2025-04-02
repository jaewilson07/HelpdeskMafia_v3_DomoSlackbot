import logging
from slack_bolt.async_app import AsyncSay
from src.services.openai import ChatRequest, openai_agent
from src.services.slack import validate_bot_auth

logger = logging.getLogger(__name__)


async def bot_message_callback(message, say: AsyncSay):
    try:
        print(message)
        user_message = message["text"]

        # Fetch the bot's user ID from the /slack/auth-test route
        auth = await validate_bot_auth()
        bot_user_id = auth.get("bot_user_id")

        # Check if the bot is mentioned in the message
        if bot_user_id not in user_message:
            print("nope", bot_user_id, user_message)
            logger.info("Bot not mentioned in the message. Ignoring.")
            return

        channel_id = message["channel_id"]

        print("going here, channel_id")

        # Call the OpenAI agent to handle the request
        response = await openai_agent.run(
            user_prompt=user_message,
        )

        print({"response": response or "No response from OpenAI"})

        # Extract the bot's reply from the response
        bot_reply = response.get("choices", [{}])[0].get("message", {}).get("content", "No response from OpenAI")

        # Send the bot's reply back to Slack
        await say(bot_reply, channel=channel_id)

    except Exception as e:
        logger.error(f"Error in sample_message_callback: {e}")
        await say("An error occurred while processing your request.")
