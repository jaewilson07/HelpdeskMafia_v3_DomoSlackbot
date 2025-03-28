import re
from typing import Union, List
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
import time


class ValidationError(Exception):

    def __init__(self, message):
        super().__init__(message)


async def get_channel_id_from_name(client,
                                   channel_name) -> Union[str, None]:

    if channel_name.startswith('#'):
        channel_name = channel_name[1:]
    
    """retrieves channel_id from a list of public and private channels"""
    channel_list = await client.conversations_list(
        types="public_channel,private_channel,mpim,im")

    channel_id =  next((channel['id'] for channel in channel_list.get('channels', [])
                 if channel['name'] == channel_name), None)

    print(channel_name, channel_id, [channel.get('name') for channel in channel_list.get('channels', [])])
    
    return channel_id


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
            oldest=str(oldest),
            latest=str(now))

        messages.extend(result["messages"])

        next_cursor = result.get("response_metadata", {}).get("next_cursor")

        if next_cursor:
            await get_channel_history(client,
                                      channel_id,
                                      next_cursor,
                                      messages=messages)

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
