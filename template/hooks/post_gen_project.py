#!/usr/bin/env python
"""Post-generation hook for cookiecutter template."""

import os
import shutil
import subprocess
import sys

# Get cookiecutter variables
use_frontend = "{{ cookiecutter.use_frontend }}" == "True"
generate_env = "{{ cookiecutter.generate_env }}" == "True"

# Remove frontend folder if not using frontend
if not use_frontend:
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_dir):
        shutil.rmtree(frontend_dir)
        print("Removed frontend/ directory (frontend not enabled)")

# Remove .env files if generate_env is false
if not generate_env:
    backend_env = os.path.join(os.getcwd(), "backend", ".env")
    if os.path.exists(backend_env):
        os.remove(backend_env)
        print("Removed backend/.env (generate_env disabled)")

    frontend_env = os.path.join(os.getcwd(), "frontend", ".env.local")
    if os.path.exists(frontend_env):
        os.remove(frontend_env)
        print("Removed frontend/.env.local (generate_env disabled)")

# Run ruff to auto-fix import sorting and other linting issues
backend_dir = os.path.join(os.getcwd(), "backend")
if os.path.exists(backend_dir):
    ruff_cmd = None

    # Try multiple methods to find/run ruff
    # 1. Check if ruff is in PATH
    ruff_path = shutil.which("ruff")
    if ruff_path:
        ruff_cmd = [ruff_path]
    # 2. Try uvx ruff (if uv is installed)
    elif shutil.which("uvx"):
        ruff_cmd = ["uvx", "ruff"]
    # 3. Try python -m ruff
    else:
        # Test if ruff is available as a module
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "--version"],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            ruff_cmd = [sys.executable, "-m", "ruff"]

    if ruff_cmd:
        print(f"Running ruff to format code (using: {' '.join(ruff_cmd)})...")
        # Run ruff check --fix to auto-fix issues
        subprocess.run(
            [*ruff_cmd, "check", "--fix", "--quiet", backend_dir],
            check=False,
        )
        # Run ruff format for consistent formatting
        subprocess.run(
            [*ruff_cmd, "format", "--quiet", backend_dir],
            check=False,
        )
        print("Code formatting complete.")
    else:
        print("Warning: ruff not found. Run 'ruff format .' in backend/ to format code.")

# Format frontend with prettier if it exists
frontend_dir = os.path.join(os.getcwd(), "frontend")
if use_frontend and os.path.exists(frontend_dir):
    # Try to find bun or npx for running prettier
    bun_cmd = shutil.which("bun")
    npx_cmd = shutil.which("npx")

    if bun_cmd:
        print("Installing frontend dependencies and formatting with Prettier...")
        # Install dependencies first (prettier is a devDependency)
        result = subprocess.run(
            [bun_cmd, "install"],
            cwd=frontend_dir,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            # Format with prettier
            subprocess.run(
                [bun_cmd, "run", "format"],
                cwd=frontend_dir,
                capture_output=True,
                check=False,
            )
            print("Frontend formatting complete.")
        else:
            print("Warning: Failed to install frontend dependencies.")
    elif npx_cmd:
        print("Formatting frontend with Prettier...")
        subprocess.run(
            [npx_cmd, "prettier", "--write", "."],
            cwd=frontend_dir,
            capture_output=True,
            check=False,
        )
        print("Frontend formatting complete.")
    else:
        print("Warning: bun/npx not found. Run 'bun run format' in frontend/ to format code.")

print("Project generated successfully!")
