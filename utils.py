import re
from typing import Union, List
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
import time


class ValidationError(Exception):

    def __init__(self, message):
        super().__init__(message)


async def get_channel_id_from_name(async_slack_app: AsyncSlackApp,
                                   channel_name) -> Union[str, None]:
    """retrieves channel_id from a list of public and private channels"""
    channel_list = await async_slack_app.client.conversations_list(
        types="public_channel,private_channel")

    return next((channel['id'] for channel in channel_list.get('channels', [])
                 if channel['name'] == channel_name), None)


async def get_channel_history(
    async_slack_app: AsyncSlackApp,
    channel_id: str,
    days: int = 7,
    cursor=None,
    messages: list = None,
) -> List[dict]:
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
            oldest=str(oldest),
            latest=str(now))

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
