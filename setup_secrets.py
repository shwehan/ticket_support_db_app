"""One-time setup for the Lakebase connection secret.

This follows the prompt-and-store pattern used by the Databricks Lakebase
example. The URL is hidden while pasted and is never written to a local file.

Usage:
    python setup_secrets.py
"""

import getpass
from urllib.parse import parse_qs, urlparse

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError


SECRET_SCOPE = "ticket-support"
SECRET_KEY = "lakebase-url"


def validate_lakebase_url(value: str) -> None:
    """Validate the URL shape without changing or shortening its value."""
    parsed = urlparse(value)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("URL must begin with postgres:// or postgresql://")
    if not parsed.username:
        raise ValueError("URL must include a PostgreSQL username")
    if not parsed.hostname:
        raise ValueError("URL must include a database hostname")
    if not parsed.path or parsed.path == "/":
        raise ValueError("URL must include a database name")
    if parse_qs(parsed.query).get("sslmode") != ["require"]:
        raise ValueError("URL must include ?sslmode=require")


w = WorkspaceClient()

try:
    w.secrets.create_scope(scope=SECRET_SCOPE)
    print(f"Created secret scope: {SECRET_SCOPE}")
except DatabricksError as exc:
    if getattr(exc, "error_code", None) != "RESOURCE_ALREADY_EXISTS":
        raise
    print(f"Using existing secret scope: {SECRET_SCOPE}")

lakebase_url = getpass.getpass("Paste your Lakebase URL: ").strip()

try:
    validate_lakebase_url(lakebase_url)
except ValueError as exc:
    raise SystemExit(f"Invalid Lakebase URL: {exc}") from exc

w.secrets.put_secret(
    scope=SECRET_SCOPE,
    key=SECRET_KEY,
    string_value=lakebase_url,
)

print(f"Saved Lakebase URL as {SECRET_SCOPE}/{SECRET_KEY}.")
print("In the app's Authorization tab, add this secret with Can read access.")
