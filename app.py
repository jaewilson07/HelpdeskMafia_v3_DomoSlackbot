from core.initialization import init_slack_app, init_fastapi, register_all_routes
from listeners import register_listeners
import uvicorn

# Initialize applications
slack_app = init_slack_app()
app = init_fastapi()

# Register components
register_all_routes(app, slack_app)
register_listeners(slack_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)