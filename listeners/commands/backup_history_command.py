import time
from logging import Logger
from slack_bolt.async_app import AsyncAck, AsyncApp as AsyncSlackApp, AsyncSay,


async def get_channel_history(
    async_slack_app: AsyncSlackApp,
    channel_id,
    days: int = 7,
    cursor=None,
    messages: list = None,
):
    """
    Retrieves channel history from Slack using the conversations.history method.
    
    Args:
        async_slack_app: The Slack app instance
        channel_id: The channel ID to fetch history from
        days: Number of days to look back (default: 7)
        cursor: Pagination cursor
        messages: List to accumulate messages
    """
    if not messages:
        messages = []
    try:
        # Calculate timestamps for filtering
        now = int(time.time())
        oldest = now - (days * 24 * 60 * 60)  # Convert days to seconds
        
        result = await async_slack_app.client.conversations_history(
            channel=channel_id,
            limit=100,  # Adjust limit as needed
            cursor=cursor,
            oldest=oldest,
            latest=now)

        messages.extend(result["messages"])

        next_cursor = result.get("response_metadata", {}).get("next_cursor")

        if next_cursor:
            await get_channel_history(async_slack_app,
                                      channel_id,
                                      next_cursor,
                                      messages=messages)

        return messages
    except Exception as e:
        print(f"Error retrieving channel history: {e}")
        return []


async def get_channel_id(async_slack_app: AsyncSlackApp, channel_name) -> str:
    """retrieves channel_id from a list of public and private channels"""
    channel_list = await async_slack_app.client.conversations_list(
        types="public_channel,private_channel")

    return next((channel['id'] for channel in channel_list.get('channels', [])
                 if channel['name'] == channel_name), None)


async def backup_command_callback(command, ack: AsyncAck, say: AsyncSay,
                                  app: AsyncSlackApp, logger: Logger):

    await ack()

    logger.info(command)

    user_id = command["user_id"]
    command_text = command.get('text', '').strip()
    parts = command_text.split()

    # Validate command format
    if len(parts) < 2:
        await say("Invalid command format. Use: /backup #channel_name days",
                  channel=user_id)
        return

    channel_name = parts[0].lstrip('#')
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            await say("Please specify a number of days between 1 and 30.",
                      channel=user_id)
            return
    except ValueError:
        await say(
            "Invalid number of days. Please specify a number between 1 and 30.",
            channel=user_id)
        return

    # Send initial response
    await say(
        f"Starting backup of #{channel_name} for the last {days} days. This may take a few moments...",
        channel=user_id)

    try:
        # Get channel ID
        channel_id = await get_channel_id(app, channel_name)

        if not channel_id:
            await say(
                f"Could not find channel '{channel_name}'. Make sure the bot is invited to the channel.",
                channel=user_id)
            return

        # Perform backup
        backup_data, found_channel_name = await ba(
            channel_id, days)

        # Upload backup file
        await slack_client.files_upload_v2(
            channel=user_id,
            filename=f"backup_{found_channel_name}.json",
            content=backup_data,
            title=f"Channel Backup for #{found_channel_name}",
            initial_comment=
            f"Here's your backup of #{found_channel_name} for the last {days} days. Contains {backup_data['message_count']} messages."
        )

    except Exception as e:
        logger.error(f"Error in backup: {str(e)}")
        await say(f"Error processing backup: {str(e)}", channel=user_id)


def register(app):
    app.command("/backup")(backup_command_callback)
