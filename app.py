
import os
from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler

# Initialize FastAPI app
api = FastAPI()

# Initialize Slack Bolt app
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])
handler = SlackRequestHandler(slack_app)

# FastAPI endpoints
@api.get("/")
async def root():
    return {"message": "Slack Bot API is running"}

# Forward Slack events to Bolt app
@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)

# Start both FastAPI and Socket Mode Handler
if __name__ == "__main__":
    # Start Socket Mode Handler in background
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.connect()
    
    # Start FastAPI with uvicorn
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=5000)
