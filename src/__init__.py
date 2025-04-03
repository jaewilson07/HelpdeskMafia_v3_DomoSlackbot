from src.apis import init_routes
from src.listeners import register_listeners

import os
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from fastapi import FastAPI

slack_app = AsyncSlackApp(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

register_listeners(slack_app)


def get_slack_app() -> AsyncSlackApp:
    """Get the Slack app instance.

    This function is used to initialize the Slack app lazily to avoid circular imports.
    """
    return slack_app


# Initialize `api` lazily to avoid circular import
def get_api():
    api = FastAPI()
    api.include_router(init_routes())
    return api
