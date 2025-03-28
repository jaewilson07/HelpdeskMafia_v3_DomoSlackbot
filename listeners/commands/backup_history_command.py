import logging
import time
import io
import json
from flask import request, jsonify
from utils.slack_utils import verify_slack_request
from utils.async_utils import run_async_in_thread
from slack_bot import backup_channel_history, slack_client

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def slack_backup_handler():
    """Handle /backup slash command."""
    logger.debug("Received request to slack_backup_handler")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request form data: {dict(request.form)}")

    # Get the command to verify we're handling the correct one
    command = request.form.get('command', '')
    logger.debug(f"Slash command received: {command}")

    # Only handle /backup commands
    if command != '/backup':
        logger.warning(f"Received unsupported command: {command}")
        return jsonify({
            "response_type": "ephemeral",
            "text": f"Unsupported command: {command}. This endpoint only handles /backup."
        })

    # Verify the request is from Slack
    if not verify_slack_request():
        logger.error("Failed to verify request signature for slash command")
        return jsonify({"status": "error", "message": "Invalid request signature"}), 403

    # Parse the slash command
    command_text = request.form.get('text', '').strip()
    user_id = request.form.get('user_id')

    # Log the command details
    logger.info(f"Received backup command: {command_text} from user {user_id}")

    # Parse command parameters: /backup #channel_name 5
    parts = command_text.split()

    if len(parts) < 2:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Invalid command format. Use: /backup #channel_name days"
        })

    # Extract channel name (remove # if present)
    requested_channel_name = parts[0].lstrip('#')

    # Extract number of days
    try:
        days = int(parts[1])
        if days <= 0 or days > 30:
            return jsonify({
                "response_type": "ephemeral",
                "text": "Please specify a number of days between 1 and 30."
            })
    except ValueError:
        return jsonify({
            "response_type": "ephemeral", 
            "text": "Invalid number of days. Please specify a number between 1 and 30."
        })

    # Send immediate response
    immediate_response = {
        "response_type": "ephemeral",
        "text": f"Starting backup of #{requested_channel_name} for the last {days} days. This may take a few moments..."
    }

    # Process the backup in a background thread using our utility function
    run_async_in_thread(
        process_backup_async, 
        channel_name=requested_channel_name, 
        days=days, 
        user_id=user_id
    )

    return jsonify(immediate_response)

async def process_backup_async(channel_name, days, user_id):
    """
    Process the backup request asynchronously.

    Args:
        channel_name (str): Name of the channel to backup
        days (int): Number of days of history to backup
        user_id (str): Slack user ID who requested the backup
    """
    try:
        # Resolve channel name to ID
        try:
            # Try to find the channel by name
            channel_list_response = await slack_client.conversations_list(
                types="public_channel,private_channel"
            )
            channels = channel_list_response.get('channels', [])
            channel_id = None

            # Use the requested channel name as a fallback
            found_channel_name = channel_name

            for channel in channels:
                if channel['name'] == channel_name:
                    channel_id = channel['id']
                    found_channel_name = channel.get('name', channel_name)  # Use channel name from API if available
                    break

            if not channel_id:
                logger.error(f"Could not find channel with name: {found_channel_name}")
                error_message = f"Could not find a channel named '{found_channel_name}'. Make sure the bot is invited to the channel."
                await slack_client.chat_postMessage(
                    channel=user_id,
                    text=error_message
                )
                return

        except Exception as e:
            logger.error(f"Error resolving channel name: {str(e)}")
            error_message = f"Error resolving channel name: {str(e)}"
            await slack_client.chat_postMessage(
                channel=user_id,
                text=error_message
            )
            return

        # Perform the backup
        backup_data, channel_name = await backup_channel_history(channel_id, days)

        # Create a JSON file with the backup data
        timestamp = int(time.time())
        filename = f"backup_{channel_name}_{timestamp}.json"

        # Convert to formatted JSON string
        json_data = json.dumps(backup_data, indent=2)

        # Upload the file to Slack
        upload_response = await slack_client.files_upload_v2(
            channel=user_id,
            filename=filename,
            file=io.BytesIO(json_data.encode('utf-8')),
            file_type="json",
            title=f"Channel Backup for #{channel_name}",
            initial_comment=f"Here's your backup of #{channel_name} for the last {days} days. Contains {backup_data['message_count']} messages."
        )

        logger.info(f"Backup file upload response: {upload_response}")

    except Exception as e:
        logger.error(f"Error in backup: {str(e)}")
        error_message = f"Error processing backup: {str(e)}"
        # Send error message directly to the user
        await slack_client.chat_postMessage(
            channel=user_id,
            text=error_message
        )