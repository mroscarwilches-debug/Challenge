"""Runs automatically before any test in this folder.

Only test_integration.py needs a database connection, but it's
simpler to load the .env values here once instead of repeating that
in every test file.
"""
import os
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def _load_env_file(path):
    # Reads a .env file and sets each KEY=value line as an environment
    # variable, skipping blank lines and comments.
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file(ENV_PATH)

# .env has DB_HOST=db, which only works from inside Docker (it's the
# name of the other container). These tests run directly on your
# machine, not inside a container, so we point them at localhost
# instead, where docker-compose publishes the database port.
os.environ["DB_HOST"] = "localhost"
