
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from fastapi import FastAPI
from core.config import Config

def init_slack_app() -> AsyncSlackApp:
    return AsyncSlackApp(token=Config.SLACK_BOT_TOKEN)

def init_fastapi() -> FastAPI:
    return FastAPI()

def register_all_routes(app: FastAPI, slack_app: AsyncSlackApp):
    from routes import base_routes, slack_routes
    
    app.state.slack_app = slack_app
    app.include_router(base_routes.router)
    app.include_router(slack_routes.router)
