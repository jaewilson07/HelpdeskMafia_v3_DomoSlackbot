import os
import asyncio
from fastapi import FastAPI
import uvicorn
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from listeners import register_listeners
from routes import init_routes

api = FastAPI()

# Initialize Slack app
async_slack_app = AsyncSlackApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

register_listeners(async_slack_app)

# Register routes
api.include_router(init_routes(async_slack_app))

@api.get("/")
async def root():
    return {"message": "Slack Bot API is running"}

@api.get("/auth-test")
async def auth_test():
    try:
        auth_test = await async_slack_app.client.auth_test()
        auth_info = await async_slack_app.client.auth_info()
        
        return {
            "bot_user_id": auth_test['user_id'],
            "bot_username": auth_test['user'],
            "workspace": auth_test['team'],
            "scopes": auth_info['scope']
        }
    except Exception as e:
        return {"error": str(e)}


async def main():
    socket_handler = AsyncSocketModeHandler(async_slack_app,
                                            os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()
    uvicorn.run(api, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    asyncio.run(main())