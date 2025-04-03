import logging

from slack_bolt.async_app import AsyncSay
from utils.pydantic_agent_generator import generate_pydantic_agent, generate_agent_dependencies, generate_model
from services.routes.slack.auth import validate_bot_auth

logger = logging.getLogger(__name__)

agent_deps = generate_agent_dependencies()
openai_agent = generate_pydantic_agent(system_prompt="You are a helpful AI assistant for Slack messages.")
openai_model = generate_model()


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

        user_id = message["user"]
        channel_id = message["channel"]
        thread_ts = message["ts"]

        said = await say(f"Give me a sec to think about it.  🌈", thread_ts=thread_ts)

        # Call the OpenAI agent to handle the request
        response = await openai_agent.run(user_prompt=user_message, deps=agent_deps, model=openai_model)

        # Extract the bot's reply from the response
        bot_reply = f"<@{user_id}> {response.data or 'No response from OpenAI'}"

        # Send the bot's reply back to Slack
        await say(bot_reply, channel=channel_id, thread_ts=said["ts"])

    except Exception as e:
        logger.error("Error in bot_message_callback: %s", e)
        await say("An error occurred while processing your request.")
