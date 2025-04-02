
# Slack Bot Project Structure

```
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── manifest.json            # Slack app manifest
├── .env                     # Environment variables (git-ignored)
│
├── core/                    # Core application setup
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   └── initialization.py   # App initialization logic
│
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── crawler/           # Crawler service
│   │   ├── __init__.py
│   │   └── crawler.py
│   ├── scraper/          # Scraper service
│   │   ├── __init__.py
│   │   └── scraper.py
│   └── client/           # API clients
│       ├── __init__.py
│       └── mafia.py
│
├── listeners/             # Slack event listeners
│   ├── __init__.py
│   ├── commands/         # Slash command handlers
│   ├── events/           # Event handlers
│   └── messages/         # Message handlers
│
├── routes/               # FastAPI routes
│   ├── __init__.py
│   ├── base_routes.py
│   ├── slack_routes.py
│   └── api/             # API endpoints
│       ├── __init__.py
│       ├── openai.py
│       └── supabase.py
│
├── templates/           # HTML templates
│   └── index.html
│
├── utils/              # Utility functions
│   ├── __init__.py
│   ├── slack.py
│   └── files.py
│
└── tests/             # Test directory
    ├── __init__.py
    ├── conftest.py    # Test configuration
    ├── .flake8        # Linting configuration
    └── listeners/     # Test modules matching main structure
```

## Key Components

### Core
- Application configuration and initialization
- Environment setup
- Core dependencies

### Services
- Business logic implementation
- External service integrations
- API clients and utilities

### Listeners
- Command handlers for slash commands
- Event handlers for mentions and interactions
- Message handlers for channel communications

### Routes
- FastAPI endpoint definitions
- API integrations (OpenAI, Supabase)
- Web interface routes

### Templates
- HTML templates for web interface
- Dashboard and configuration pages

### Utils
- Helper functions
- Common utilities
- File handling
