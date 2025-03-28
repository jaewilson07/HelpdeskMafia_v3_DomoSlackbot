
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["base"])

@router.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Slack Bot API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                button { 
                    padding: 10px 20px; 
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover { background-color: #45a049; }
                #result { margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>Slack Bot API</h1>
            <button onclick="testAuth()">Test Auth</button>
            <div id="result"></div>
            <script>
                async function testAuth() {
                    const response = await fetch('/slack/auth-test');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
