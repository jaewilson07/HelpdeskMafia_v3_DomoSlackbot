from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from typing import List
import logging

logger = logging.getLogger(__name__)


async def get_files(client: AsyncSlackApp = None, canvas_list: List[dict] = None, cursor=None):
    """
    Recursively fetches canvases using Slack's files.list method.
    """

    if not canvas_list:
        canvas_list = []
    logger.info(f"Fetching page with cursor: {'None' if not cursor else cursor[:10]+'...'}")

    result = await client.files_list(cursor=cursor, types="canvases")

    if not result["ok"]:
        logger.error(f"API Error fetching page: {result['error']} (Cursor: {cursor})")
        # Stop recursion on API error for this branch
        return []

    canvas_list.extend(result.get("files", []))

    next_cursor = result.get("response_metadata", {}).get("next_cursor")

    if next_cursor:
        return await get_files(client=client, canvas_list=canvas_list, cursor=next_cursor)

    return canvas_list
