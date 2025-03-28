from slack_bolt.async_app import AsyncAck, AsyncRespond
from logging import Logger


async def sample_command_callback(command, ack: AsyncAck,
                                  respond: AsyncRespond, logger: Logger):
    try:
        await ack()
        await respond(
            f"Responding to the sample command! Your command was: {command['text']}"
        )
    except Exception as e:
        logger.error(e)
