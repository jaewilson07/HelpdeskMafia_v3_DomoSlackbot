from src.services.routes.slack.channel import search_channel_by_name, get_channel_history
from src.services.routes.slack.canvas import upsert_canvas, update_canvas_title, get_channel_canvases
from src.services.openai_agent import summarize_chat_messages
from src.services.routes.slack.files import get_files

from slack_bolt.async_app import AsyncAck
from logging import Logger
from typing import Tuple
import datetime as dt


async def validate_update_news_canvas_command(client, command_text: str, canvas_title: str) -> Tuple[str, str]:
    """
    Validates the `/update-news-canvas` command and retrieves the channel and canvas details.

    Args:
        client: The Slack client instance.
        command_text (str): The text of the command entered by the user.
        canvas_title (str): The title of the canvas to validate.

    Returns:
        Tuple[str, str]: The channel ID and channel name.

    Raises:
        ValueError: If the command format is invalid or the channel is not found.
    """
    parts = command_text.split()

    if len(parts) < 1:
        raise ValueError("Usage: /update-news-canvas <channel_name>")

    channel_name = parts[0].strip()

    if channel_name.startswith("#"):
        channel_name = channel_name[1:]  # Remove the '#' prefix if present

    channel_id = await search_channel_by_name(client, channel_name)

    if not channel_id:
        raise ValueError(f"Channel '{channel_name}' not found. Make sure the bot is invited to the channel.")

    canvases = await get_channel_canvases(client, channel_id=channel_id)

    print("🌈🌈")

    canvas = next((canvas for canvas in canvases if canvas.get("data").get("title", "").startswith(canvas_title)), None)

    return channel_id, channel_name, canvas and canvas.get("id"), canvas and canvas.get("data", {}).get("file_id")


async def update_news_canvas_command_callback(command, ack: AsyncAck, say, respond, client, logger: Logger):
    """
    Handles the `/update-news-canvas` command to summarize messages and update the 'news' canvas.

    Args:
        command: The Slack command payload.
        ack (AsyncAck): Acknowledges the command request.
        say: Sends a message to the Slack channel.
        respond: Sends a response to the user.
        client: The Slack client instance.
        logger (Logger): Logger instance for logging errors and information.
    """
    await ack()

    canvas_title = "News - "  # Hardcoded canvas name
    days = 5

    thread_ts = command.get("thread_ts") or command.get("ts")
    command_text = command.get("text", "").strip()

    channel_id, channel_name, canvas_id, file_id = None, None, None, None

    try:
        channel_id, channel_name, canvas_id, file_id = await validate_update_news_canvas_command(
            client, command_text=command_text, canvas_title=canvas_title
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return await respond(str(e), response_type="ephemeral")

    said = await say(f"Give me a sec to think about it.  🌈", thread_ts=thread_ts)

    messages = await get_channel_history(client=client, channel_id=channel_id, days=days)

    if not messages:
        message = f"No messages found in channel #{channel_name} for the last 5 days."
        logger.error(message)
        return await respond(message, response_type="ephemeral")

    response = await summarize_chat_messages(messages=messages)

    # Upsert the summary into the canvas
    try:
        canvas_title = f"News - updated{dt.datetime.now().strftime(' %Y-%m-%d %H:%M')}"

        res = await upsert_canvas(
            client=client, channel_id=channel_id, title=canvas_title, document_md=response.data, is_append_if_exists=False
        )

        # canvas_id = res["canvas_id"]

        # await update_canvas_title(
        #     client=client,
        #     canvas_id=canvas_id,
        #     new_title=canvas_title,
        # )

        # Respond with success message
        channel_link = f"<#{channel_id}|{channel_name}>"
        return await say(
            f"Canvas '{canvas_title}' updated with a summary of the last 5 days of messages from {channel_link}.",
            thread_ts=said["ts"],
        )

    except Exception as e:
        message = f"Error updating news canvas: {e}"
        logger.error(message)
        await respond(message, response_type="ephemeral")
