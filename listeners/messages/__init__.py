
from slack_bolt.async_app import AsyncSlackApp
from .hello_message import hello_message_callback

def register(app: AsyncSlackApp):
    app.message("hello")(hello_message_callback)
