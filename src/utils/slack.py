import re
from typing import Union, List
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
import time


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


def slack_timestamp_to_url(workspace_url: str, channel_id: str, timestamp: str) -> str:
    """
    Converts a Slack timestamp into a message URL.

    Args:
        workspace_url (str): The base URL of the Slack workspace (e.g., 'https://yourworkspace.slack.com').
        channel_id (str): The ID of the Slack channel.
        timestamp (str): The Slack timestamp (e.g., '1681234567.890123').

    Returns:
        str: The URL to the Slack message.
    """
    # Slack timestamps use a dot as a separator, replace it with an underscore for the URL
    ts_url = timestamp.replace(".", "_")
    return f"{workspace_url}/archives/{channel_id}/p{ts_url}"
