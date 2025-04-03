async def sample_message_callback(event, say):
    print(event)
    channel_id = event["channel"]

    response = f"Hey there <@{event['user']}>!"

    await say(response, channel=channel_id)
