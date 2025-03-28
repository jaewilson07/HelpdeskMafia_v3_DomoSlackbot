import re


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
