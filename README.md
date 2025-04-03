-# HelpdeskMafia Slackbot

HelpdeskMafia is a Slackbot designed to enhance team collaboration by integrating with Slack's interactive features and external services like OpenAI and Domo. It provides functionalities such as summarizing conversations, managing canvases, and automating workflows.

## Features

### Commands

- **/question**: Ask a question and trigger a Domo workflow for intelligent responses.
- **/backup**: Backup a channel's history and generate summaries.
- **/upsert-canvas**: Create or update a Slack canvas with specified content.
- **/update-news-canvas**: Summarize recent messages and update the "news" canvas.

### Events

- **App Mentions**: Responds to mentions with helpful guidance.
- **App Home Opened**: Displays a custom home tab for users.

### Messages

- **Bot Messages**: Processes messages mentioning the bot and provides AI-powered responses.

## Services

The Slackbot integrates with the following services:

- **Slack API**: For managing channels, canvases, and messages.
- **OpenAI**: For summarizing conversations and generating intelligent responses.
- **Domo**: For triggering workflows and managing data.
- **File Management**: Uploads and manages files in Slack.

## Technologies

### Backend Frameworks

- **FastAPI**: A modern web framework for building APIs.
- **Slack Bolt**: A framework for building Slack apps.

### AI Integration

- **OpenAI API**: Powers AI-based summarization and responses.
- **pydantic-ai**: Simplifies schema-based AI interactions.

### Slack Integration

- **Slack SDK**: Provides APIs for interacting with Slack features.

### Utilities

- **Domo Library**: For interacting with Domo APIs.
- **Requests and Aiohttp**: For HTTP requests.

### Deployment and Runtime

- **Uvicorn**: ASGI server for FastAPI.
- **dotenv**: Manages environment variables.

### Testing and Linting

- **Pytest**: For unit and integration testing.
- **Flake8**: For linting.
- **Black**: For code formatting.

### CI/CD

- **GitHub Actions**: Automated workflows for testing, linting, and formatting.

## Installation

### Prerequisites

1. A Slack workspace with permissions to install apps.
2. Environment variables:
   - `SLACK_BOT_TOKEN`: Bot token from Slack.
   - `SLACK_APP_TOKEN`: App-level token with `connections:write` scope.

### Steps

1. Clone the repository:
   ```zsh
   git clone https://github.com/slack-samples/bolt-python-starter-template.git
   cd bolt-python-starter-template
   ```
2. Set up a virtual environment:
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
4. Start the server:
   ```zsh
   python3 app.py
   ```

## Linting and Testing

### Linting

```zsh
flake8 *.py && flake8 listeners/
black .
```

## Project Structure

### `/listeners`

Handles Slack interactions:

- **Commands**: Slash commands like `/question` and `/backup`.
- **Events**: Event listeners for app mentions and home tab interactions.
- **Messages**: Processes bot-related messages.

### `/services`

Integrates with external services:

- **Slack**: Manages channels, canvases, and files.
- **OpenAI**: Summarizes and processes messages.
- **Domo**: Triggers workflows.

### `/utils`

Utility functions for Slack and AI integrations.

### `app.py`

Entry point for the application.

## App Distribution

To distribute the app across multiple workspaces, implement OAuth and use a public URL (e.g., via `ngrok`).

```zsh
ngrok http 3000
```

Set the redirect URL in Slack's app configuration to:

```
https://<ngrok-url>/slack/oauth_redirect
```
