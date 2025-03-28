
import utils

async def question_command_callback(ack, body, logger, say):
    await ack()
    logger.info(body)
    print(body)

    user_id = body["user_id"]
    channel_id = body["channel_id"]
    question = utils.remove_slack_user_mentions(body["text"])
    response_url = body["response_url"]

    await say(
        f'<@{user_id}> asked: "{question}"\nGive me a sec to think about it.  🌈'
    )

def register(app):
    app.command("/question")(question_command_callback)
