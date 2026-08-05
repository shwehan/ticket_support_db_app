"""Interactively store the Lakebase connection URL in Databricks Secrets.

The URL is collected with getpass, so it is not echoed to the terminal or
written to a file. Run this script from an authenticated Databricks environment.
"""

from getpass import getpass
from urllib.parse import parse_qs, urlparse

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError


SECRET_SCOPE = "ticket-support"
SECRET_KEY = "lakebase-url"


def prompt_for_lakebase_url() -> str:
    value = getpass("Paste the Lakebase PostgreSQL URL (input hidden): ").strip()
    parsed = urlparse(value)

    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("The URL must begin with postgres:// or postgresql://")
    if not parsed.hostname:
        raise ValueError("The URL must include a database hostname")
    if not parsed.path or parsed.path == "/":
        raise ValueError("The URL must include a database name")
    if parse_qs(parsed.query).get("sslmode") != ["require"]:
        raise ValueError("The URL must include ?sslmode=require")

    return value


def ensure_scope(client: WorkspaceClient) -> None:
    try:
        client.secrets.create_scope(scope=SECRET_SCOPE)
        print(f"Created secret scope: {SECRET_SCOPE}")
    except DatabricksError as exc:
        if getattr(exc, "error_code", None) != "RESOURCE_ALREADY_EXISTS":
            raise
        print(f"Using existing secret scope: {SECRET_SCOPE}")


def main() -> None:
    try:
        lakebase_url = prompt_for_lakebase_url()
    except ValueError as exc:
        raise SystemExit(f"Invalid Lakebase URL: {exc}") from exc

    client = WorkspaceClient()
    ensure_scope(client)
    client.secrets.put_secret(
        scope=SECRET_SCOPE,
        key=SECRET_KEY,
        string_value=lakebase_url,
    )
    print(f"Saved Lakebase URL as {SECRET_SCOPE}/{SECRET_KEY}.")
    print("The URL was not written to a local file.")


if __name__ == "__main__":
    main()
