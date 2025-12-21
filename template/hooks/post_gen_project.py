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
    # Try multiple methods to find ruff
    ruff_commands = [
        ["ruff"],  # ruff in PATH
        ["uv", "run", "ruff"],  # via uv
        [sys.executable, "-m", "ruff"],  # via current Python
    ]

    ruff_cmd = None
    for cmd in ruff_commands:
        try:
            result = subprocess.run(
                cmd + ["--version"],
                capture_output=True,
                check=True,
            )
            ruff_cmd = cmd
            break
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

    if ruff_cmd:
        try:
            # First run ruff check --fix to auto-fix issues
            subprocess.run(
                ruff_cmd + ["check", "--fix", "--quiet", backend_dir],
                capture_output=True,
                check=False,
            )
            # Then run ruff format for consistent formatting
            subprocess.run(
                ruff_cmd + ["format", "--quiet", backend_dir],
                capture_output=True,
                check=False,
            )
        except Exception:
            pass

print("Project generated successfully!")
