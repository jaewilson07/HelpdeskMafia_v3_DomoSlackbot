from slack_bolt.async_app import AsyncSay
import utils


async def app_mention_callback(event, say: AsyncSay):
    message_id = event["ts"]
    user_id = event["user"]
    channel_id = event["channel"]
    question = event["text"]
    clean_question = utils.remove_slack_user_mentions(question)

    await say(
        f'Hello <@{user_id}> instead of asking me a question, use a /slash command!\n\n ```/question #search my llm for the answer to your question.```',
        thread_ts=message_id)


def register(app):
    app.event("app_mention")(app_mention_callback)
