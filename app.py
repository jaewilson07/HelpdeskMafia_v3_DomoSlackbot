import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]

print(slack_bot_token)

# Initializes your app with your bot token and socket mode handler
app = App(token=slack_bot_token)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
