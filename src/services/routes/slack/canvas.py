from typing import List
import json

from .files import get_files


async def get_channel_canvases(client, channel_id: str) -> List[dict]:
    """
    Retrieves a list of canvases for a given Slack channel.

    Args:
        client: The Slack client instance.
        channel_id: The ID of the Slack channel.

    Returns:
        A list of canvases (if available) or an empty list.
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
    canvases = await get_channel_canvases(client=client, channel_id=channel_id)
    return next((canvas for canvas in canvases if canvas.get("name") == channel_id))


async def create_canvas(
    client, channel_id: str, document_md: str, title: str  # document body as markdown  # canvas title
) -> dict:
    """
    Creates a new canvas in a Slack channel.

    Args:
        client: The Slack client instance.
        channel_id: The ID of the Slack channel.
        document_md: The content of the canvas document.
        title: The title of the canvas.

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
        canvas_id: The ID of the canvas to update.
        changes: A list of changes to apply to the canvas.

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
    Replaces entire canvas or a specific section with new markdown content.
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
    If is_append_if_exists is True, appends content; otherwise replaces it.
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
