"""Database connection helper for the gym-app API."""

import os

import psycopg2


def get_connection():
    # Opens a database connection using settings from the environment,
    # so the API and the database always agree on how to talk to each other.
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )
