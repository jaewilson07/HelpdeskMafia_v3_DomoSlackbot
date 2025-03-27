<<<<<<< HEAD
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
=======
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Heroku!"


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> f263f4b3f0b3e24ed0dff3cb276b912cf8935a56
