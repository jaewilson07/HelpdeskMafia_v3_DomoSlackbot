from logging import Logger
from slack_bolt.async_app import AsyncAck, AsyncApp as AsyncSlackApp, AsyncSay
import json
from typing import Union, Tuple
import utils as ut


async def validate_backup_history_command(client, parts) -> Tuple[str, str, int]:
    """retrieves channel_id and days to extract from comman"""
    
    channel_id,channel_name, days = None, None, None

    # Validate command format
    if len(parts) < 2:
        raise ut.ValidationError(
            "Invalid command format. Use: /backup #channel_name days")

    channel_name = parts[0].lstrip('#')
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            raise ut.ValidationError(
                "Please specify a number of days between 1 and 30.")

    except ValueError:
        raise ut.ValidationError(
            "Invalid number of days. Please specify a number between 1 and 30."
        )

    if not channel_name or not days:
        raise ut.ValidationError(
            "Invalid command format. Use: /backup #channel_name days")

    channel_id = await ut.get_channel_id_from_name(app, channel_name)

    if not channel_id:
        raise ut.ValidationError( f"Could not find channel '{channel_name}'. Make sure the bot is invited to the channel.")
    
    return channel_id, channel_name, days


async def backup_command_callback(command, 
                                  ack: AsyncAck,
                                  say: AsyncSay,
                                  client,
                                  logger: Logger):

    await ack()
    print('app', app)

    logger.info(command)

    user_id = command["user_id"]
    command_text = command.get('text', '').strip()
    parts = command_text.split()

    channel_id,channel_name, days = None, None , None

    try:
        channel_id,channel_name, days = await validate_backup_history_command(client, parts)

    except ut.ValidationError as e:
        await say(e.message, channel=user_id, response_type = 'ephemeral')
        return

    # Send initial response
    await say(
        f"Starting backup of #{channel_name} for the last {days} days. This may take a few moments...",
        channel=user_id)

    try:
        
        messages = await get_channel_history(async_slack_app=app,
                                             channel_id=channel_id,
                                             days=days)

        # Prepare backup data
        backup_data = {
            "channel": channel_name,
            "days": days,
            "message_count": len(messages),
            "messages": messages
        }

        # Upload backup file
        await app.client.files_upload_v2(
            channel=user_id,
            filename=f"backup_{channel_name}.json",
            content=json.dumps(backup_data, indent=2),
            title=f"Channel Backup for #{channel_name}",
            initial_comment=
            f"Here's your backup of #{channel_name} for the last {days} days. Contains {len(messages)} messages."
        )

    except Exception as e:
        logger.error(f"Error in backup: {str(e)}")
        await say(f"Error processing backup: {str(e)}", channel=user_id)


def register(app):
    app.command("/backup")(backup_command_callback)
