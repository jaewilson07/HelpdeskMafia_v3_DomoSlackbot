from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from .question_command import question_command_callback
from .backup_command import backup_command_callback
from .upsert_canvas_command import upsert_canvas_command_callback


def register(app: AsyncSlackApp):
    app.command("/question")(question_command_callback)
    app.command("/backup")(backup_command_callback)
    app.command("/upsert-canvas")(upsert_canvas_command_callback)


#     # app.command("/sample-command")(sample_command_callback)
