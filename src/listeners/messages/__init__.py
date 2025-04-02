from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from .hello_message import hello_message_callback
from .bot_message import bot_message_callback


def register(app: AsyncSlackApp):
    app.message("hello")(hello_message_callback)
    # app.message()(bot_message_callback)
