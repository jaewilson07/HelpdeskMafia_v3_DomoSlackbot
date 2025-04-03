"""
This module provides functions for managing Slack canvases, including retrieving,
creating, updating, and appending content to canvases.
"""

from typing import List
import json

from .files import get_files


async def get_channel_canvases(client, channel_id: str) -> List[dict]:
    """
    Retrieves a list of canvases for a given Slack channel.

    Args:
        client: The Slack client instance.
        channel_id (str): The ID of the Slack channel.

    Returns:
        List[dict]: A list of canvases or an empty list if none are found.
    """
    try:
        # Fetch channel information
        response = await client.conversations_info(channel=channel_id)
        channel_info = response.get("channel", {})

        # Extract canvases if available
        canvases = [obj for obj in channel_info.get("properties", {}).get("tabs", []) if obj.get("type") == "canvas"]

        if not canvases:
            return []

        files = await get_files(client=client)

        result = []

        for canvas in canvases:

            result.append(canvas)

            fi = next((fi for fi in files if canvas.get("data", {}).get("file_id", None) == fi.get("id")), None)
            if not fi:
                continue

            canvas.get("data").update(fi)

        return result

    except Exception as e:
        print(f"Error retrieving canvases for channel {channel_id}: {e}")
        return []


async def search_canvas_id_by_name(client, channel_id):
    """
    Searches for a canvas by name in a given Slack channel.

    Args:
        client: The Slack client instance.
        channel_id: The ID of the Slack channel.

    Returns:
        dict: The canvas object if found, otherwise None.
    """
    canvases = await get_channel_canvases(client=client, channel_id=channel_id)
    return next((canvas for canvas in canvases if canvas.get("name") == channel_id))


async def create_canvas(client, channel_id: str, document_md: str, title: str) -> dict:
    """
    Creates a new canvas in a Slack channel.

    Args:
        client: The Slack client instance.
        channel_id (str): The ID of the Slack channel.
        document_md (str): The content of the canvas in markdown format.
        title (str): The title of the canvas.

    Returns:
        dict: The response from the Slack API.
    """
    try:
        response = await client.canvases_create(
            channel_id=channel_id,
            document_content={"type": "markdown", "markdown": document_md},  # document body as markdown
            title=title,
        )
        return response

    except Exception as e:
        print(f"Error creating canvas in channel {channel_id}: {e}")
        return {}


async def update_canvas(client, canvas_id: str, changes: List[dict]) -> dict:
    """
    Updates an existing canvas in Slack.

    Args:
        client: The Slack client instance.
        canvas_id (str): The ID of the canvas to update.
        changes (List[dict]): A list of changes to apply to the canvas.

    Returns:
        dict: The response from the Slack API.
    """
    try:
        response = await client.canvases_edit(
            canvas_id=canvas_id,
            changes=changes,
        )
        return response
    except Exception as e:
        print(f"Error updating canvas {canvas_id}: {e}")
        return {}


async def append_to_canvas(client, canvas_id: str, markdown_text: str) -> dict:
    """
    Appends new markdown content to the end of the canvas.

    Args:
        client: The Slack client instance.
        canvas_id (str): The ID of the canvas to update.
        markdown_text (str): The markdown content to append.

    Returns:
        dict: The response from the Slack API.
    """
    changes = [
        {
            "operation": "insert_at_end",
            "document_content": {
                "type": "markdown",
                "markdown": markdown_text,
            },
        }
    ]
    return await update_canvas(client, canvas_id, changes)


async def replace_canvas_content(client, canvas_id: str, markdown_text: str, section_id: str = None) -> dict:
    """
    Replaces the entire canvas or a specific section with new markdown content.

    Args:
        client: The Slack client instance.
        canvas_id (str): The ID of the canvas to update.
        markdown_text (str): The new markdown content.
        section_id (str, optional): The ID of the section to replace. Defaults to None.

    Returns:
        dict: The response from the Slack API.
    """
    if section_id:
        changes = [
            {
                "operation": "replace",
                "section_id": section_id,
                "document_content": {
                    "type": "markdown",
                    "markdown": markdown_text,
                },
            }
        ]
    else:
        changes = [
            {
                "operation": "replace",
                "document_content": {
                    "type": "markdown",
                    "markdown": markdown_text,
                },
            }
        ]
    return await update_canvas(client, canvas_id, changes)


async def upsert_canvas(client, channel_id: str, title: str, document_md: str, is_append_if_exists: bool = False) -> dict:
    """
    Creates a new canvas if not found, or updates an existing one.

    Args:
        client: The Slack client instance.
        channel_id (str): The ID of the Slack channel.
        title (str): The title of the canvas.
        document_md (str): The content of the canvas in markdown format.
        is_append_if_exists (bool, optional): Whether to append content if the canvas exists. Defaults to False.

    Returns:
        dict: The response from the Slack API.
    """
    canvases = await get_channel_canvases(client, channel_id)
    found_canvas = next((c for c in canvases if c.get("title") == title), None)

    if not found_canvas:
        return await create_canvas(client, channel_id, document_md, title)
    else:
        if is_append_if_exists:
            return await append_to_canvas(client, found_canvas["id"], document_md)
        else:
            return await replace_canvas_content(client, found_canvas["id"], document_md)


async def update_canvas_title(client, canvas_id: str, new_title: str) -> dict:
    """
    Updates the title of an existing canvas in Slack.

    Args:
        client: The Slack client instance.
        canvas_id (str): The ID of the canvas to update.
        new_title (str): The new title for the canvas.

    Returns:
        dict: The response from the Slack API.
    """
    return await update_canvas(
        client=client,
        canvas_id=canvas_id,
        changes=json.dumps(
            [
                {
                    "operation": "document_metadata_update",
                    "title": new_title,
                }
            ]
        ),
    )
