
from fastapi import APIRouter, Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

router = APIRouter(prefix="/slack", tags=["slack"])

def init_slack_routes(slack_app: AsyncApp):
    handler = AsyncSlackRequestHandler(slack_app)
    
    @router.get("/auth-test")
    async def auth_test():
        try:
            auth_test = await slack_app.client.auth_test()
            auth_info = await slack_app.client.auth_info()
            
            return {
                "bot_user_id": auth_test['user_id'],
                "bot_username": auth_test['user'],
                "workspace": auth_test['team'],
                "team_id": auth_test['team_id'],
                "enterprise_id": auth_test.get('enterprise_id'),
                "url": auth_test['url'],
                "scopes": auth_info['scope'],
                "token_type": auth_info['token_type']
            }
        except Exception as e:
            return {"error": str(e)}

    @router.post("/events")
    async def slack_events(request: Request):
        return await handler.handle(request)
    
    return router
