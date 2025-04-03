from . import SlackError
import time
from typing import List, Union
from slack_bolt.async_app import AsyncApp as AsyncSlackApp

import logging

logger = logging.getLogger(__name__)


async def get_channels(
    client: AsyncSlackApp = None,
    channel_types="public_channel,private_channel,mpim,im",
    channel_list: List[dict] = None,
    cursor: str = None,
) -> List[dict]:  # Corrected return type
    """recursive function for retrieving channels"""

    if client is None:
        from app import slack_app

        client = slack_app.client

    if not channel_list:
        channel_list = []

    try:
        result = await client.conversations_list(channel_types=channel_types, cursor=cursor, limit=100)

    except Exception as e:
        raise SlackError(f"Error getting channel list: {str(e)}") from e

    channel_list.extend(result["channels"])

    next_cursor = result.get("response_metadata", {}).get("next_cursor")

    if next_cursor:
        return await get_channels(client, channel_types=channel_types, channel_list=channel_list, cursor=next_cursor)
    return channel_list


async def search_channel_id_by_name(client, channel_name, cursor: str = None) -> Union[str, None]:
    """Retrieves channel_id from a list of public and private channels recursively"""

    if channel_name.startswith("#"):
        channel_name = channel_name[1:]

    channel_list = await get_channels(client=client, channel_types="public_channel,private_channel,mpim,im", cursor=cursor)

    return next((channel["id"] for channel in channel_list if channel["name"] == channel_name), None)


async def get_channel_history(
    client,
    channel_id: str,
    days: int = 7,
    cursor=None,
    messages: list = None,
) -> List[dict]:
    """
    Retrieves channel history from Slack using the conversations.history method,
    including threaded replies.

    Args:
        client: async client
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

        result = await client.conversations_history(
            channel=channel_id,
            limit=100,
            cursor=cursor,
            oldest=oldest,
        )

        for message in result["messages"]:
            messages.append(message)
            # Check if the message has a thread
            if "thread_ts" in message:
                thread_replies = await client.conversations_replies(
                    channel=channel_id,
                    ts=message["thread_ts"],
                )
                # Append all replies to the messages list
                messages.extend(thread_replies["messages"])

        next_cursor = result.get("response_metadata", {}).get("next_cursor")

        if next_cursor:
            await get_channel_history(client=client, channel_id=channel_id, cursor=next_cursor, messages=messages)

        return messages

    except Exception as e:
        message = f"Error retrieving channel history for {channel_id}: {e}"
        print(message)
        logger.error(message)
        return []
