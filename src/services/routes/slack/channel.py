"""
This module provides functions for managing Slack channels, including retrieving
channel lists, searching for channels by name, and fetching channel history.
"""

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
) -> List[dict]:
    """
    Recursively retrieves a list of Slack channels.

    Args:
        client (AsyncSlackApp): The Slack client instance.
        channel_types (str): Comma-separated types of channels to retrieve.
        channel_list (List[dict], optional): A list to accumulate channels. Defaults to None.
        cursor (str, optional): The pagination cursor for fetching the next page. Defaults to None.

    Returns:
        List[dict]: A list of channels retrieved from Slack.
    """
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


async def search_channel_by_name(client, channel_name, cursor: str = None) -> Union[str, None]:
    """
    Searches for a channel by name and retrieves its ID.

    Args:
        client: The Slack client instance.
        channel_name (str): The name of the channel to search for.
        cursor (str, optional): The pagination cursor for fetching the next page. Defaults to None.

    Returns:
        Union[str, None]: The channel ID if found, otherwise None.
    """
    if channel_name.startswith("#"):
        channel_name = channel_name[1:]

    channel_list = await get_channels(client=client, channel_types="public_channel,private_channel,mpim,im", cursor=cursor)

    return next((channel["id"] for channel in channel_list if channel["name"] == channel_name), None)


async def get_channel_history(client, channel_id: str, days: int = 7, cursor=None, messages: list = None) -> List[dict]:
    """
    Retrieves the message history of a Slack channel, including threaded replies.

    Args:
        client: The Slack client instance.
        channel_id (str): The ID of the Slack channel.
        days (int, optional): Number of days to look back. Defaults to 7.
        cursor: Pagination cursor. Defaults to None.
        messages (list, optional): A list to accumulate messages. Defaults to None.

    Returns:
        List[dict]: A list of messages retrieved from the channel.
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
