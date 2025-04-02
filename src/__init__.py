from src.routes import init_routes
from src.listeners import register_listeners


import os
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from fastapi import FastAPI

slack_app = AsyncSlackApp(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

register_listeners(slack_app)

api = FastAPI()
api.include_router(init_routes())
