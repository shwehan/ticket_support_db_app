"""Small Lakebase connection helper using the Day 1 secret convention."""

import base64
import os
from contextlib import contextmanager

import psycopg2
from databricks.sdk import WorkspaceClient
from psycopg2.extras import RealDictCursor


def lakebase_url() -> str:
    """Use a local env var locally; use a Databricks secret after deployment."""
    if os.environ.get("LAKEBASE_URL"):
        return os.environ["LAKEBASE_URL"]

    scope = os.environ.get("LAKEBASE_SECRET_SCOPE", "database")
    key = os.environ.get("LAKEBASE_SECRET_KEY", "lakebase-url")
    secret = WorkspaceClient().secrets.get_secret(scope=scope, key=key)
    return base64.b64decode(secret.value).decode("utf-8")


@contextmanager
def get_connection():
    conn = psycopg2.connect(lakebase_url(), cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

