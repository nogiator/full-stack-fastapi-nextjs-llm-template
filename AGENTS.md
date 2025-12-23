# AGENTS.md

This file provides guidance for AI coding agents (Codex, Copilot, Cursor, Zed, OpenCode) working with this repository.

## Project Overview

**fastapi-fullstack** is an interactive CLI tool that generates FastAPI projects with Logfire observability integration. It uses Cookiecutter templates to scaffold complete project structures with configurable options for databases, authentication, background tasks, and various integrations.

## Commands

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Linting and formatting
ruff check . --fix
ruff format .

# Type checking
mypy fastapi_gen
```

## CLI Usage

```bash
# Interactive wizard
fastapi-fullstack new

# Quick project creation
fastapi-fullstack create my_project --database postgresql --auth jwt

# Minimal project (no extras)
fastapi-fullstack create my_project --minimal
```

## Architecture

### Core Modules (`fastapi_gen/`)

- **cli.py** - Click-based CLI with commands: `new`, `create`, `templates`
- **config.py** - Pydantic models for configuration options
- **prompts.py** - Interactive prompts using Questionary
- **generator.py** - Cookiecutter invocation and messaging

### Template System (`template/`)

```
template/
├── cookiecutter.json                    # Default context (~75 variables)
├── hooks/post_gen_project.py            # Post-gen cleanup
└── {{cookiecutter.project_slug}}/
    ├── backend/app/                     # FastAPI application
    └── frontend/                        # Next.js 15 (optional)
```

Template files use `{% if cookiecutter.use_jwt %}` style conditionals.

## Key Design Decisions

- All database options except SQLite are async (asyncpg, motor)
- Project names must match pattern `^[a-z][a-z0-9_]*$`
- Generated projects use UV for package management
- Template uses repository pattern for data access

## Where to Find More Info

- Template variables: `template/cookiecutter.json`
- Post-generation logic: `template/hooks/post_gen_project.py`
- Sprint tasks: `notes/sprint_0_1_7/`
