
# Slack Bot Project Structure

```
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependencies
├── manifest.json             # Slack app manifest
├── .env                      # Environment variables (git-ignored)
│
├── listeners/                # Slack event listeners
│   ├── __init__.py          # Listener registration
│   ├── commands/            # Slash command handlers
│   │   ├── __init__.py
│   │   └── sample_command.py
│   ├── events/              # Event handlers (mentions, etc)
│   │   ├── __init__.py
│   │   └── app_mention.py
│   └── messages/            # Message handlers
│       ├── __init__.py
│       └── message_handler.py
│
├── routes/                  # FastAPI routes
│   ├── __init__.py         # Route registration
│   ├── base_routes.py      # Core routes (health check, etc)
│   └── slack_routes.py     # Slack-specific endpoints
│
├── templates/              # HTML templates
│   └── index.html         # Main dashboard
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── slack.py          # Slack helper functions
│
└── tests/                # Test directory
    ├── __init__.py
    ├── test_commands.py
    └── test_events.py
```

## Key Components

### App Entry Point (app.py)
- Initializes FastAPI and Slack Bolt app
- Registers routes and listeners
- Handles socket mode configuration

### Listeners
- **commands/**: Slash command handlers
- **events/**: Event subscriptions (mentions, home tab)
- **messages/**: Message handlers and filters

### Routes
- **base_routes.py**: Core web endpoints
- **slack_routes.py**: Slack-specific endpoints

### Templates
- HTML templates for web interface
- Dashboard and configuration pages

### Utils
- Helper functions and utilities
- Slack API wrappers
