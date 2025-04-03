from slack_bolt.async_app import AsyncAck, AsyncRespond
from logging import Logger
from typing import Tuple
from src.services.routes.slack.channel import search_channel_by_name
from src.services.routes.slack.canvas import upsert_canvas


async def validate_update_canvas_command(client, command_text: str) -> Tuple[str, str, str]:
    parts = command_text.split()

    if len(parts) < 2:
        raise ValueError("Usage: /upsert-canvas channel_name canvas_name")

    channel_name = parts[0].strip()
    canvas_name = parts[1].strip()

    if channel_name.startswith("#"):
        channel_name = channel_name[1:]  # Remove the '#' prefix if present

    channel_id = await search_channel_by_name(client, channel_name)

    if not channel_id:
        raise ValueError(f"Channel '{channel_name}' not found. Make sure the bot is invited to the channel.")

    # canvas_id = await search_canvas_id_by_name(client, channel_id, canvas_name)
    # if not canvas_id:
    #     raise ValueError(f"Canvas '{canvas_name}' not found in channel '{channel_id}'.")

    return channel_id, channel_name, canvas_name


async def upsert_canvas_command_callback(command, ack: AsyncAck, respond: AsyncRespond, client, logger: Logger):
    """
    Expects the format: /upsert-canvas <channel_name> <canvas_name>
    Upserts the canvas by name with "Hello World".
    """
    await ack()
    channel_id = command.get("channel")
    try:
        try:
            channel_id, channel_name, canvas_name = await validate_update_canvas_command(
                client, command.get("text", "").strip()
            )
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            await respond(str(e), response_type="ephemeral", channel=channel_id)

        await upsert_canvas(client=client, channel_id=channel_id, title=canvas_name, document_md="Hello World")
        logger.info(f"Canvas '{canvas_name}' successfully upserted in channel '{channel_name}'.")
        return await respond(f"Canvas '{canvas_name}' upserted in channel '{channel_name}'.")

    except Exception as e:
        logger.error(f"Error updating canvas: {e}")
        await respond(f"Failed to update the canvas: {str(e)}")
