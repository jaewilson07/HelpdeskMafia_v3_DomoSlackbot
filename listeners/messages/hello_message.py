
from slack_bolt.async_app import AsyncSlackApp

async def hello_message_callback(message, say):
    print(message)
    await say(f"Hey there <@{message['user']}>!")

def register(app: AsyncSlackApp):
    app.message("hello")(hello_message_callback)
