from logging import Logger
from slack_bolt.async_app import AsyncAck, AsyncApp as AsyncSlackApp, AsyncSay
import json
from typing import Union, Tuple
import src.utils.slack as utsl


async def validate_backup_history_command(client, command: str) -> Tuple[str, str, int]:
    """retrieves channel_id and days to extract from comman"""

    channel_id, channel_name, days = None, None, None

    parts = command.split()

    print(command, parts)

    # Validate command format
    if len(parts) < 2:
        raise utsl.ValidationError("Invalid command format. Use: /backup #channel_name days")

    channel_name = parts[0].lstrip("#")
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            raise utsl.ValidationError("Please specify a number of days between 1 and 30.")

    except ValueError:
        raise utsl.ValidationError("Invalid number of days. Please specify a number between 1 and 30.")

    if not channel_name or not days:
        raise utsl.ValidationError("Invalid command format. Use: /backup #channel_name days")

    channel_id = await utsl.get_channel_id_from_name(client, channel_name)

    if not channel_id:
        raise utsl.ValidationError(f"Could not find channel '{channel_name}'. Make sure the bot is invited to the channel.")

    return channel_id, channel_name, days


async def backup_command_callback(command, ack: AsyncAck, say: AsyncSay, client, logger: Logger):

    await ack()

    logger.info(command)
    print(command)

    user_id = command["user_id"]

    channel_id, channel_name, days = None, None, None

    try:
        channel_id, channel_name, days = await validate_backup_history_command(client, command.get("text", "").strip())

    except utsl.ValidationError as e:
        await say(str(e), channel=user_id, response_type="ephemeral")
        return

    # Send initial response
    await say(
        f"Starting backup of #{channel_name} for the last {days} days. This may take a few moments...", channel=user_id
    )

    try:

        messages = await utsl.get_channel_history(client=client, channel_id=channel_id, days=days)

        # Prepare backup data
        backup_data = {"channel": channel_name, "days": days, "message_count": len(messages), "messages": messages}

        print(f"upload {user_id}")

        # Upload backup file
        await client.files_upload_v2(
            filename=f"backup_{channel_name}.json",
            title=f"Channel Backup for #{channel_name}",
            channel=command["channel_id"],
            content=json.dumps(backup_data),
            initial_comment=f"Here's your backup of #{channel_name} for the last {days} days. Contains {len(messages)} messages.",
        )

    except Exception as e:
        logger.error(f"Error in backup: {str(e)}")
        await say(f"Error processing backup: {str(e)}", channel=user_id)
