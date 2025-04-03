from slack_bolt.async_app import AsyncSay

# from src.utils.slack import remove_slack_user_mentions


async def app_mention_callback(event, say: AsyncSay):
    message_id = event["ts"]
    user_id = event["user"]
    # question = event["text"]
    # channel_id = event["channel"]
    # clean_question = remove_slack_user_mentions(question)

    await say(
        f"Hello <@{user_id}> instead of asking me a question, use a /slash command!\n\n ```/question #search my llm for the answer to your question.```",
        thread_ts=message_id,
    )
