
from slack_bolt.async_app import AsyncSlackApp
from .app_mention import app_mention_callback
from .app_home_opened import app_home_opened_callback

def register(app: AsyncSlackApp):
    app.event("app_mention")(app_mention_callback)
    app.event("app_home_opened")(app_home_opened_callback)
