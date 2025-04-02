from src import slack_app, api
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import os
import uvicorn
import asyncio


async def start_socket_mode():
    socket_handler = AsyncSocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()


async def start_http():
    config = uvicorn.Config(api, host="0.0.0.0", port=5000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_socket_mode(), start_http())


if __name__ == "__main__":
    asyncio.run(main())
