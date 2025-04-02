# Technology Overview

This project leverages the following technologies and tools:

## Backend Frameworks

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Slack Bolt**: A Python framework for building Slack apps, including event handling and interactive components.

## Deployment and Runtime

- **Uvicorn**: A lightning-fast ASGI server for serving FastAPI applications.
- **Replit**: Configuration for running the project in a Replit environment.
- **Procfile**: Used for specifying commands to run the application in deployment environments.

## Testing and Linting

- **Pytest**: A testing framework for writing and running unit tests.
- **Flake8**: A linting tool to ensure code quality and adherence to Python standards.
- **Black**: A code formatter to enforce consistent code style.

## Slack Integration

- **Slack SDK**: Provides APIs for interacting with Slack, including sending messages and handling events.

## OpenAI Integration

- **OpenAI API**: Used for AI-powered chat completions and other AI functionalities.
- **pydantic-ai**: Simplifies integration with OpenAI by providing schema-based request handling.

## Utilities

- **Domo Library**: A library for interacting with Domo APIs, used for triggering workflows and managing data.
- **Requests and Aiohttp**: Libraries for making synchronous and asynchronous HTTP requests.

## CI/CD

- **GitHub Actions**: Automated workflows for testing, linting, and formatting validation.

## Other Tools

- **dotenv**: For managing environment variables securely.
- **JSON**: Used for handling structured data, such as Slack messages and backups.
