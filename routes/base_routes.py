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