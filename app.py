import os
import asyncio
from fastapi import FastAPI, Request
import uvicorn

from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from listeners import register_listeners

api = FastAPI()

# Initialize Slack app
async_slack_app = AsyncSlackApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

register_listeners(async_slack_app)
# Register listeners

handler = AsyncSlackRequestHandler(async_slack_app)


@api.get("/")
async def root():
    return {"message": "Slack Bot API is running"}


@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


async def main():
    socket_handler = AsyncSocketModeHandler(async_slack_app,
                                            os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()
    uvicorn.run(api, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    asyncio.run(main())
