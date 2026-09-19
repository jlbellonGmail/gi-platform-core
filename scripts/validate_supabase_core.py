"""Read-only Supabase validation for the GI Platform Core schema.

The script never creates, updates, or deletes data. It checks that the host,
profile, and credentials can read the expected Core tables. Authenticated RLS
checks require SUPABASE_ACCESS_TOKEN and optional expected table assertions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TABLES = (
    "organizations",
    "locations",
    "user_profiles",
    "organization_memberships",
    "roles",
    "permissions",
    "membership_roles",
    "location_access",
    "audit_events",
)

SELECT_COLUMNS = {
    "location_access": "membership_id,location_id",
}


def load_dotenv() -> None:
    path = Path(".env")
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


def read_table(url: str, key: str, token: str, table: str) -> tuple[int, int | None, str | None]:
    query = urlencode({"select": SELECT_COLUMNS.get(table, "id"), "limit": "1"})
    headers = {"apikey": key, "Accept-Profile": "core"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{url.rstrip('/')}/rest/v1/{table}?{query}", headers=headers)
    try:
        with urlopen(request, timeout=15) as response:
            payload = response.read().decode("utf-8")
            rows = json.loads(payload or "[]")
            return response.status, len(rows) if isinstance(rows, list) else None, None
    except HTTPError as exc:
        return exc.code, None, f"HTTP {exc.code}"
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return 0, None, type(exc).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-only", action="store_true", help="Use only the publishable key and skip authenticated assertions")
    parser.add_argument("--expect-visible", action="append", default=[], metavar="TABLE")
    parser.add_argument("--expect-empty", action="append", default=[], metavar="TABLE")
    args = parser.parse_args()
    load_dotenv()

    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    token = "" if args.public_only else os.getenv("SUPABASE_ACCESS_TOKEN", "")
    if not url or not key:
        print("FAIL missing SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY", file=sys.stderr)
        return 2
    if not args.public_only and not token:
        print("FAIL missing SUPABASE_ACCESS_TOKEN for authenticated RLS validation", file=sys.stderr)
        return 2

    failures = 0
    mode = "public" if args.public_only else "authenticated"
    print(f"Supabase Core validation ({mode})")
    for table in TABLES:
        status, count, error = read_table(url, key, token, table)
        suffix = f" rows={count}" if count is not None else f" error={error}"
        print(f"- core.{table}: status={status}{suffix}")
        if status != 200:
            failures += 1
        if table in args.expect_visible and (status != 200 or count == 0):
            print(f"  FAIL expected visible rows in core.{table}", file=sys.stderr)
            failures += 1
        if table in args.expect_empty and (status != 200 or count != 0):
            print(f"  FAIL expected no visible rows in core.{table}", file=sys.stderr)
            failures += 1
    if failures:
        print(f"FAILURES={failures}", file=sys.stderr)
        return 1
    print("PASS Supabase Core read-only validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
