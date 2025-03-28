
import utils

async def app_mention_callback(event, say):
    message_id = event["ts"]
    user_id = event["user"]
    channel_id = event["channel"]
    question = event["text"]
    clean_question = utils.remove_slack_user_mentions(question)

    await say(
        f'<@{user_id}> asked: "{clean_question}"\nGive me a sec to think about it. But in the meantime, have you tried googling it?',
        thread_ts=message_id,
    )

def register(app):
    app.event("app_mention")(app_mention_callback)
