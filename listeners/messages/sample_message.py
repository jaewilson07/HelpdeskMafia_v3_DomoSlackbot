from logging import Logger

from slack_bolt import BoltContext
from slack_bolt.async_app import AsyncSay


async def sample_message_callback(context: BoltContext, say: AsyncSay,
                                  logger: Logger):
    try:
        greeting = context["matches"][0]
        await say(f"{greeting}, how are you?")
    except Exception as e:
        logger.error(e)
