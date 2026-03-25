# Development Plan: LMS Telegram Bot

## Overview

This document outlines the development plan for building a Telegram bot that enables users to interact with the LMS (Learning Management System) backend through natural language chat. The bot will support slash commands for common operations and use an LLM for intent-based routing of plain text queries.

## Architecture

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point (`bot.py`)**: Handles Telegram bot initialization and provides a `--test` CLI mode for offline verification without connecting to Telegram.

2. **Handlers Layer (`handlers/`)**: Contains command handlers that are pure functions taking input and returning text responses. They have no dependency on Telegram, making them testable in isolation.

3. **Services Layer (`services/`)**: Wraps external API clients (LMS Backend API, LLM API) with clean interfaces for handlers to use.

4. **Configuration (`config.py`)**: Loads environment variables from `.env.bot.secret` for API keys and endpoints.

## Task 1: Scaffold and Test Mode

Create the project skeleton with `--test` mode support. The entry point will parse command-line arguments and route to appropriate handlers. Handlers will return placeholder responses initially. This establishes the testable architecture where the same handler functions work both in Telegram mode and CLI test mode.

## Task 2: Backend Integration

Implement real handlers for `/start`, `/help`, `/health`, `/labs`, and `/scores` commands. The `/health` handler will call the backend API to check system status. The `/labs` handler will fetch available labs from the backend. The `/scores` handler will retrieve per-task pass rates. Error handling will ensure backend failures produce friendly messages rather than crashes.

## Task 3: Intent-Based Natural Language Routing

Integrate the LLM to interpret plain text queries and route them to appropriate handlers or API calls. Users will be able to ask questions like "what labs are available" or "show me my score for lab-04" in natural language. The LLM will parse intent and parameters, then invoke the corresponding handler or service method.

## Task 4: Containerization and Deployment

Create a Dockerfile for the bot and add it as a service in `docker-compose.yml`. Document the deployment process in the README. Deploy the bot on the VM alongside the existing backend and frontend services. Verify end-to-end functionality by testing commands in Telegram.

## Testing Strategy

- **Unit Tests**: Test handlers in isolation with mocked services
- **Integration Tests**: Test service layer with mocked API responses
- **CLI Test Mode**: Verify handlers work without Telegram using `--test` flag
- **End-to-End Tests**: Deploy bot and verify real Telegram interactions

## Dependencies

- `aiogram`: Async Telegram Bot API framework
- `httpx`: Async HTTP client for API calls
- `pydantic-settings`: Configuration management with validation
