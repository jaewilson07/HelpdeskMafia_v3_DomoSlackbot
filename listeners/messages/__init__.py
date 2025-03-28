from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from .hello_message import hello_message_callback
from .sample_message import sample_message_callback


def register(app: AsyncSlackApp):
    app.message("hello")(hello_message_callback)
    # app.message("hello")(sample_message_callback)
