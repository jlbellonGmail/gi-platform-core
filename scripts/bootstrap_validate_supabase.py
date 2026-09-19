"""Interactive, idempotent bootstrap and RLS validation for Supabase gi-dev.

Secrets are read only into process memory.  Passwords, JWTs and server-side
keys are never written to files, logs, subprocess arguments, or evidence.
The bootstrap creates only the synthetic organization, user profile, and
active membership required by the authenticated Core RLS check.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

# Make the checkout root importable when invoked as ``python scripts/...``.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gi_platform_core import CoreService, SupabaseCoreStore


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


def fail(message: str) -> None:
    raise RuntimeError(message)


def expected_host(url: str, project_ref: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == f"{project_ref}.supabase.co"


def decode_jwt_payload(token: str) -> dict[str, Any]:
    try:
        encoded = token.split(".")[1]
        padded = encoded + "=" * ((4 - len(encoded) % 4) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
    except (IndexError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError("Supabase devolvio un JWT invalido") from exc
    if not isinstance(payload, dict) or not payload.get("sub"):
        fail("El JWT autenticado no contiene sub")
    return payload


def authenticate(url: str, publishable_key: str, email: str, password: str) -> tuple[str, str]:
    request = Request(
        f"{url.rstrip('/')}/auth/v1/token?grant_type=password",
        data=json.dumps({"email": email, "password": password}).encode("utf-8"),
        headers={"apikey": publishable_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        # Do not include the provider response: it can contain sensitive details.
        raise RuntimeError("No se pudo autenticar el usuario de prueba") from exc
    token = body.get("access_token") if isinstance(body, dict) else None
    user = body.get("user") if isinstance(body, dict) else None
    subject = user.get("id") if isinstance(user, dict) else None
    if not token or not subject:
        fail("La autenticacion no devolvio access_token y user.id")
    payload = decode_jwt_payload(token)
    if payload["sub"] != subject:
        fail("El sub del JWT no coincide con user.id")
    return token, subject


def read_authenticated_rows(url: str, publishable_key: str, token: str, table: str, select: str) -> list[dict[str, Any]]:
    query = urlencode({"select": select, "limit": "1000"})
    request = Request(
        f"{url.rstrip('/')}/rest/v1/{table}?{query}",
        headers={
            "apikey": publishable_key,
            "Authorization": f"Bearer {token}",
            "Accept-Profile": "core",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8") or "[]")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"No se pudo leer core.{table} con RLS autenticada") from exc
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        fail(f"Respuesta invalida para core.{table}")
    return payload


def assert_authenticated_isolation(url: str, publishable_key: str, token: str, subject: str, expected_org_id: str, expected_profile_id: str, expected_membership_id: str) -> None:
    profiles = read_authenticated_rows(url, publishable_key, token, "user_profiles", "id,external_subject,active")
    organizations = read_authenticated_rows(url, publishable_key, token, "organizations", "id,active")
    memberships = read_authenticated_rows(url, publishable_key, token, "organization_memberships", "id,user_id,organization_id,active")
    roles = read_authenticated_rows(url, publishable_key, token, "roles", "id,organization_id")
    membership_roles = read_authenticated_rows(url, publishable_key, token, "membership_roles", "id,membership_id")
    location_access = read_authenticated_rows(url, publishable_key, token, "location_access", "membership_id,location_id")
    audits = read_authenticated_rows(url, publishable_key, token, "audit_events", "id,actor_user_id")
    permissions = read_authenticated_rows(url, publishable_key, token, "permissions", "code,active")

    profile_ids = {row.get("id") for row in profiles}
    organization_ids = {row.get("id") for row in organizations}
    membership_ids = {row.get("id") for row in memberships}
    if expected_profile_id not in profile_ids or any(row.get("external_subject") != subject for row in profiles):
        fail("RLS permitio un perfil distinto del usuario autenticado")
    if expected_org_id not in organization_ids:
        fail("RLS no hizo visible la organizacion sintetica")
    if expected_membership_id not in membership_ids:
        fail("RLS no hizo visible la membership sintetica")
    if any(row.get("user_id") not in profile_ids for row in memberships):
        fail("RLS expuso una membership de otro usuario")
    if any(row.get("organization_id") not in organization_ids for row in memberships if row.get("active")):
        fail("RLS expuso una membership activa sin organizacion visible")
    if any(row.get("organization_id") not in organization_ids for row in roles):
        fail("RLS expuso un role fuera de las organizaciones visibles")
    if any(row.get("membership_id") not in membership_ids for row in membership_roles):
        fail("RLS expuso un vinculo de role fuera de memberships visibles")
    if any(row.get("membership_id") not in membership_ids for row in location_access):
        fail("RLS expuso acceso de location fuera de memberships visibles")
    if any(row.get("actor_user_id") not in profile_ids for row in audits):
        fail("RLS expuso un evento de auditoria de otro usuario")
    if any(not row.get("active") for row in permissions):
        fail("RLS expuso permisos inactivos")


def run_read_only_validator(url: str, publishable_key: str, token: str) -> None:
    from scripts import validate_supabase_core

    previous = os.environ.get("SUPABASE_ACCESS_TOKEN")
    os.environ["SUPABASE_URL"] = url
    os.environ["SUPABASE_PUBLISHABLE_KEY"] = publishable_key
    os.environ["SUPABASE_ACCESS_TOKEN"] = token
    try:
        old_argv = sys.argv
        sys.argv = ["validate_supabase_core.py", "--expect-visible", "organizations"]
        result = validate_supabase_core.main()
    finally:
        sys.argv = old_argv
        if previous is None:
            os.environ.pop("SUPABASE_ACCESS_TOKEN", None)
        else:
            os.environ["SUPABASE_ACCESS_TOKEN"] = previous
    if result != 0:
        fail("La validacion autenticada de Supabase fallo")


def bootstrap(service: CoreService, store: SupabaseCoreStore, subject: str) -> tuple[str, str, str, list[str]]:
    marker = hashlib.sha256(subject.encode("utf-8")).hexdigest()[:12]
    organization_name = f"GI DEV RLS TEST {marker}"
    display_name = f"GI DEV RLS TEST USER {marker}"

    organizations = [item for item in store.organizations.values() if item.name == organization_name]
    users = [item for item in store.users.values() if item.external_subject == subject]
    if len(organizations) > 1 or len(users) > 1:
        fail("Hay registros equivalentes duplicados; no se realizan escrituras")
    if organizations and not organizations[0].active:
        fail("La organizacion sintetica existente esta inactiva; no se modifica")
    if users and (not users[0].active or users[0].display_name != display_name):
        fail("Existe un user_profile no sintetico para el usuario; no se modifica")

    organization = organizations[0] if organizations else service.create_organization(organization_name)
    user = users[0] if users else service.create_user(subject, display_name)
    matches = [item for item in store.memberships.values() if item.user_id == user.id and item.organization_id == organization.id]
    if len(matches) > 1:
        fail("Hay memberships sinteticas duplicadas; no se realizan escrituras")
    if matches and not matches[0].active:
        fail("La membership sintetica existente esta inactiva; no se modifica")
    membership = matches[0] if matches else service.add_membership(user.id, organization.id)
    return organization.id, user.id, membership.id, [organization_name, display_name]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Archivo local de configuracion no versionado")
    args = parser.parse_args()
    load_env_file(args.env_file)

    url = os.getenv("SUPABASE_URL", "").strip()
    publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "").strip()
    if not url or not publishable_key:
        print("BLOQUEADO: faltan SUPABASE_URL o SUPABASE_PUBLISHABLE_KEY", file=sys.stderr)
        return 2

    print("Preflight Supabase gi-dev")
    project_ref = input("Project ref verificado de gi-dev (no secreto): ").strip()
    if not project_ref or not expected_host(url, project_ref):
        print("BLOQUEADO: SUPABASE_URL no coincide exactamente con el project ref indicado", file=sys.stderr)
        return 2
    print("Destino verificado")

    email = input("Email del usuario de prueba: ").strip()
    password = getpass.getpass("Password del usuario de prueba (oculta): ")
    token, subject = authenticate(url, publishable_key, email, password)
    del password, email

    server_key = getpass.getpass("Clave server-side exclusiva de gi-dev (oculta): ")
    if not server_key:
        print("BLOQUEADO: falta la clave server-side", file=sys.stderr)
        return 2
    store = SupabaseCoreStore(url, server_key)
    service = CoreService(store)
    organization_id, profile_id, membership_id, labels = bootstrap(service, store, subject)
    del server_key, store, service

    # The labels are intentionally not printed; only non-sensitive counts/status are emitted.
    print("Bootstrap idempotente completado/verificado: organization, user_profile y membership")
    run_read_only_validator(url, publishable_key, token)
    assert_authenticated_isolation(url, publishable_key, token, subject, organization_id, profile_id, membership_id)
    del token, subject, organization_id, profile_id, membership_id, labels
    print("PASS RLS autenticada y aislamiento sintético")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Detenido por el usuario", file=sys.stderr)
        raise SystemExit(130)
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
