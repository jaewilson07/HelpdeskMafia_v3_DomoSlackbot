from fastapi import APIRouter, Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

import utils.slack as utsl

router = APIRouter(prefix="/slack", tags=["slack"])


def init_slack_routes(slack_app: AsyncApp):
    handler = AsyncSlackRequestHandler(slack_app)

    @router.get("/auth-test")
    async def auth_test():
        try:
            await utsl.test_slack_auth(client=slack_app.client)
        except Exception as e:
            return {"error": str(e)}

    @router.post("/events")
    async def slack_events(request: Request):
        return await handler.handle(request)

    return router
