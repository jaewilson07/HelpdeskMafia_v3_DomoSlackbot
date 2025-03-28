
from slack_bolt.async_app import AsyncSlackApp
from .question_command import question_command_callback

def register(app: AsyncSlackApp):
    app.command("/question")(question_command_callback)
