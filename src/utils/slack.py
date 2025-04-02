import re
from typing import Union, List
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
import time


class ValidationError(Exception):

    def __init__(self, message):
        super().__init__(message)


async def get_channel_list(
    client: AsyncSlackApp,
    channel_types="public_channel,private_channel,mpim,im",
    channel_list: List[dict] = None,
    cursor: str = None,
) -> List[str]:

    if not channel_list:
        channel_list = []

    try:
        result = await client.conversations_list(channel_types=channel_types, cursor=cursor, limit=100)

    except Exception as e:
        raise ValidationError(f"Error getting channel list: {str(e)}")

    channel_list.extend(result["channels"])

    next_cursor = result.get("response_metadata", {}).get("next_cursor")

    if next_cursor:
        return await get_channel_list(client, channel_types=channel_types, channel_list=channel_list, cursor=next_cursor)
    return channel_list


async def get_channel_id_from_name(client, channel_name, cursor: str = None) -> Union[str, None]:
    """Retrieves channel_id from a list of public and private channels recursively"""

    if channel_name.startswith("#"):
        channel_name = channel_name[1:]

    channel_list = await get_channel_list(
        client=client, channel_types="public_channel,private_channel,mpim,im", cursor=cursor
    )

    return next((channel["id"] for channel in channel_list if channel["name"] == channel_name), None)


async def get_channel_history(
    client,
    channel_id: str,
    days: int = 7,
    cursor=None,
    messages: list = None,
) -> List[dict]:
    """
    Retrieves channel history from Slack using the conversations.history method.

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
            limit=100,  # Adjust limit as needed
            cursor=cursor,
            oldest=oldest,
            # latest=now
        )

        messages.extend(result["messages"])

        next_cursor = result.get("response_metadata", {}).get("next_cursor")

        if next_cursor:
            await get_channel_history(client=client, channel_id=channel_id, cursor=next_cursor, messages=messages)

        return messages

    except Exception as e:
        print(f"Error retrieving channel history: {e}")
        return []


def remove_slack_user_mentions(text):
    """
    Removes Slack user mentions (e.g., <@U08HGSAP9K9>) from a text string.

    Args:
        text (str): The input text containing potential Slack user mentions.

    Returns:
        str: The text with Slack user mentions removed.
    """
    pattern = r"<@U[A-Z0-9]+>"

    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text
