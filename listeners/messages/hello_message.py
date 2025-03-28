async def hello_message_callback(message, say):
    print(message)
    await say(f"Hey there <@{message['user']}>!")
