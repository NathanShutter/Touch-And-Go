"""
src/db/config.py
Centralized database configuration for Touch & Go.
Reads credentials from environment variables (see .env.example).
"""

import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME"),
}


def get_connection():
    """Return a new MySQL connection using environment-based config."""
    missing = [k for k, v in DB_CONFIG.items() if not v]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Copy .env.example to .env and fill in your credentials."
        )
    return mysql.connector.connect(**DB_CONFIG)
