# Bolt for Python Template App

This is a generic Bolt for Python template app used to build Slack apps.

Before getting started, ensure you have a development workspace where you have permissions to install apps. If you don’t have one set up, [create one](https://slack.com/create).

## Installation

### Create a Slack App

1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest".
2. Select the workspace where you want to install the application.
3. Copy the contents of [manifest.json](./manifest.json) into the text box labeled `*Paste your manifest code here*` (within the JSON tab) and click _Next_.
4. Review the configuration and click _Create_.
5. Click _Install to Workspace_ and then _Allow_ on the following screen. You will be redirected to the App Configuration dashboard.

### Environment Variables

Before running the app, store the following environment variables:

1. Open your app's configuration page, click **OAuth & Permissions** in the left-hand menu, and copy the Bot User OAuth Token. Store this in your environment as `SLACK_BOT_TOKEN`.
2. Click **Basic Information** in the left-hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Copy this token and store it in your environment as `SLACK_APP_TOKEN`.

```zsh
# Replace with your app token and bot token
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
```

### Set Up Your Local Project

```zsh
# Clone this project onto your machine
git clone https://github.com/slack-samples/bolt-python-starter-template.git

# Change into the project directory
cd bolt-python-starter-template

# Set up your Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Start your local server
python3 app.py
```

### Linting

```zsh
# Run flake8 from the root directory for linting
flake8 *.py && flake8 listeners/

# Run black from the root directory for code formatting
black .
```

### Testing

```zsh
# Run pytest from the root directory for unit testing
pytest .
```

## Project Structure

### `manifest.json`

`manifest.json` contains the configuration for Slack apps. With a manifest, you can create an app with a pre-defined configuration or adjust the configuration of an existing app.

### `app.py`

`app.py` is the entry point for the application and is used to start the server. This file is kept minimal, primarily routing inbound requests.

### `/listeners`

Incoming requests are routed to "listeners". This directory organizes listeners based on Slack Platform features. For example:

- `/listeners/shortcuts` handles incoming [Shortcuts](https://api.slack.com/interactivity/shortcuts) requests.
- `/listeners/views` handles [View submissions](https://api.slack.com/reference/interaction-payloads/views#view_submission).

## App Distribution / OAuth

Implement OAuth only if you plan to distribute your application across multiple workspaces. A separate `app_oauth.py` file contains relevant OAuth settings.

When using OAuth, Slack requires a public URL to send requests. This template uses [`ngrok`](https://ngrok.com/download). Follow [this guide](https://ngrok.com/docs#getting-started-expose) to set it up.

Start `ngrok` to expose the app on an external network and create a redirect URL for OAuth:

```zsh
ngrok http 3000
```

The output will include a forwarding address for `http` and `https` (use `https`). It will look like this:

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:3000
```

Navigate to **OAuth & Permissions** in your app configuration and click **Add a Redirect URL**. Set the redirect URL to your `ngrok` forwarding address with the `slack/oauth_redirect` path appended. For example:

```
https://3cb89939.ngrok.io/slack/oauth_redirect
```
