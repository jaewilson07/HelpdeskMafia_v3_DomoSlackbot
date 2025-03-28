import logging
from slack_bolt.async_app import AsyncAck, AsyncSay
from utils.slack_utils import verify_slack_request
from slack_bot import backup_channel_history, slack_client

logger = logging.getLogger(__name__)

async def backup_command_callback(command, ack: AsyncAck, say: AsyncSay):
    await ack()
    logger.info(command)

    user_id = command["user_id"]
    command_text = command.get('text', '').strip()
    parts = command_text.split()

    # Validate command format
    if len(parts) < 2:
        await say(
            "Invalid command format. Use: /backup #channel_name days",
            channel=user_id
        )
        return

    channel_name = parts[0].lstrip('#')
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            await say(
                "Please specify a number of days between 1 and 30.",
                channel=user_id
            )
            return
    except ValueError:
        await say(
            "Invalid number of days. Please specify a number between 1 and 30.",
            channel=user_id
        )
        return

    # Send initial response
    await say(
        f"Starting backup of #{channel_name} for the last {days} days. This may take a few moments...",
        channel=user_id
    )

    try:
        # Get channel ID
        channel_list = await slack_client.conversations_list(types="public_channel,private_channel")
        channel_id = None
        for channel in channel_list.get('channels', []):
            if channel['name'] == channel_name:
                channel_id = channel['id']
                break

        if not channel_id:
            await say(
                f"Could not find channel '{channel_name}'. Make sure the bot is invited to the channel.",
                channel=user_id
            )
            return

        # Perform backup
        backup_data, found_channel_name = await backup_channel_history(channel_id, days)

        # Upload backup file
        await slack_client.files_upload_v2(
            channel=user_id,
            filename=f"backup_{found_channel_name}.json",
            content=backup_data,
            title=f"Channel Backup for #{found_channel_name}",
            initial_comment=f"Here's your backup of #{found_channel_name} for the last {days} days. Contains {backup_data['message_count']} messages."
        )

    except Exception as e:
        logger.error(f"Error in backup: {str(e)}")
        await say(
            f"Error processing backup: {str(e)}",
            channel=user_id
        )

def register(app):
    app.command("/backup")(backup_command_callback)