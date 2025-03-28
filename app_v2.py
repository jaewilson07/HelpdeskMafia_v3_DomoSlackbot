import os
import asyncio
from fastapi import FastAPI, Request
import uvicorn

from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler
import utils

api = FastAPI()


# Initializes your app with your bot token and signing secret
async_slack_app = AsyncSlackApp(
    token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(async_slack_app)


# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@async_slack_app.message("hello")
async def message_hello(message, say):
    print(message)
    # say() sends a message to the channel where the event was triggered
    await say(f"Hey there <@{message['user']}>!")


@api.get("/")
async def root():
    return {"message": "Slack Bot API is running"}


@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


@async_slack_app.event("app_mention")
async def handle_app_mention_events(event, say):
    message_id = event["ts"]
    user_id = event["user"]

    channel_id = event["channel"]
    question = event["text"]
    clean_question = utils.remove_slack_user_mentions(question)

    said = await say(
        f'<@{user_id}> asked: "{clean_question}"\nGive me a sec to think about it.  But in the meantime, have you tried googling it?',
        thread_ts=message_id,
    )  # Send the response back to Slack


@async_slack_app.command("/question")
async def handle_some_command(ack, body, logger, say):
    await ack()  # acknwledge to slack that message received

    logger.info(body)
    print(body)

    user_id = body["user_id"]
    channel_id = body["channel_id"]

    question = utils.remove_slack_user_mentions(body["text"])
    response_url = body["response_url"]

    said = await say(
        f'<@{user_id}> asked: "{question}"\nGive me a sec to think about it.  🌈'
    )  # Send the response back to Slack


async def main():
    socket_handler = AsyncSocketModeHandler(async_slack_app, os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()

    uvicorn.run(api, host="0.0.0.0", port=5000)


# Start your app
if __name__ == "__main__":
    asyncio.run(main())
