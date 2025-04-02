
from fastapi import APIRouter, Request
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
async def test_auth(request: Request):
    slack_app = request.app.state.slack_app
    return await utils.test_slack_auth(slack_app.client)
