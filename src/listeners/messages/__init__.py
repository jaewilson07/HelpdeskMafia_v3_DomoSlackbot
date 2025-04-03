from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from .bot_message import bot_message_callback

# from .sample_message import sample_message_callback


def register(app: AsyncSlackApp):
    # app.message()(sample_message_callback)
    app.message()(bot_message_callback)
