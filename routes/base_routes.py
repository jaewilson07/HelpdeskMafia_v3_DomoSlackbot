
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(tags=["base"])

def get_template(template_name: str) -> str:
    template_path = Path("templates") / template_name
    with open(template_path, "r") as f:
        return f.read()

@router.get("/")
async def root():
    return HTMLResponse(content=get_template("index.html"), status_code=200)

@router.get("/test-auth")
async def test_auth():
    try:
        auth_test = await slack_app.client.auth_test()
        return {
            "bot_user_id": auth_test['user_id'],
            "bot_username": auth_test['user'],
            "workspace": auth_test['team']
        }
    except Exception as e:
        return {"error": str(e)}
