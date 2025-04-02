import os

import asyncio
from slack_bolt.async_app import AsyncApp


async def main():
  slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
  app = AsyncApp(token=slack_bot_token,
                 signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
  res = await app.client.auth_test()
  print(res)
  print(slack_bot_token)


if __name__ == "__main__":
  asyncio.run(main())
