from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from .question_command import question_command_callback
from .sample_command import sample_command_callback


def register(app: AsyncSlackApp):
    app.command("/question")(question_command_callback)
    # app.command("/sample-command")(sample_command_callback)
