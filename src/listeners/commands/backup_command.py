from src.utils.ValidationError import ValidationError
import src.services.routes.slack.channel as slack_routes  # Fix import for Slack utilities

from slack_bolt.async_app import AsyncAck, AsyncSay
import logging
import json
from typing import Tuple

from src.services.openai_agent import summarize_chat_messages


logger = logging.getLogger(__name__)


async def validate_backup_history_command(client, command: str) -> Tuple[str, str, int]:
    """retrieves channel_id and days to extract from comman"""

    channel_id, channel_name, days = None, None, None

    parts = command.split()

    # Validate command format
    if len(parts) < 2:
        raise ValidationError("Invalid command format. Use: /backup #channel_name days")

    channel_name = parts[0].lstrip("#")
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            raise ValidationError("Please specify a number of days between 1 and 30.")
    except ValueError as e:  # Correctly reference the exception variable
        raise ValidationError("Invalid number of days. Please specify a number between 1 and 30.") from e

    if not channel_name or not days:
        raise ValidationError("Invalid command format. Use: /backup #channel_name days")

    channel_id = await slack_routes.search_channel_by_name(client, channel_name)

    if not channel_id:
        raise ValidationError(f"Could not find channel '{channel_name}'. Make sure the bot is invited to the channel.")

    return channel_id, channel_name, days


async def backup_command_callback(command, ack: AsyncAck, respond, say: AsyncSay, client):

    await ack()

    logger.info(command)

    user_id = command["user_id"]

    channel_id, channel_name, days = None, None, None

    try:
        channel_id, channel_name, days = await validate_backup_history_command(client, command.get("text", "").strip())

    except ValidationError as e:
        await respond(str(e), channel=user_id, response_type="ephemeral")
        return

    # Send initial response
    thread = await say(
        f"Starting backup of #{channel_name} for the last {days} days. This may take a few moments...", channel=user_id
    )

    try:
        messages = await slack_routes.get_channel_history(client=client, channel_id=channel_id, days=days)

        # Prepare backup data
        backup_data = {
            "channel": channel_name,
            "days": days,
            "message_count": len(messages),
            "messages": messages,
        }

        print(thread)

        # Upload backup file
        await client.files_upload_v2(
            filename=f"backup_{channel_name}.json",
            title=f"Channel Backup for #{channel_name}",
            channel=thread["channel"],
            thread=thread["ts"],
            content=json.dumps(backup_data),
            initial_comment=f"Here's your backup of #{channel_name} for the last {days} days. Contains {len(messages)} messages.",
        )

        # Generate chat summary
        response = await summarize_chat_messages(
            messages=messages,
        )

        channel_hyperlink = f"<#{channel_id}|{channel_name}>"

        await say(
            f"<@{user_id}> here is a {days}-day summary of {channel_hyperlink}\n {response.data}",
            channel=thread["channel_id"],
            thread_ts=thread["ts"],
            mrkdwn=True,
        )

    except Exception as e:
        message = f"Error in backup: {str(e)}"
        logger.error(message)
        await respond(message, channel=user_id, channel_id=user_id, response_type="ephemeral")
