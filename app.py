from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import os
import uvicorn
import asyncio
from dotenv import load_dotenv

assert load_dotenv(override=True)

from src import slack_app, get_api


async def start_socket_mode():
    socket_handler = AsyncSocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()


async def start_http():
    api = get_api()  # Initialize `api` lazily
    config = uvicorn.Config(api, host="0.0.0.0", port=5000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_socket_mode(), start_http())


if __name__ == "__main__":
    asyncio.run(main())
