from src.services.routes.slack.auth import validate_bot_auth
import asyncio


async def main():
    res = await validate_bot_auth()
    print(res)


if __name__ == "__main__":
    # Test the bot authentication validation

    asyncio.run(main)
