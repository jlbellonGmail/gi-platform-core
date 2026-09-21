"""Small WSGI HTTP adapter for Core identity operations.

Authentication is deliberately injected by the host. Core never parses or
trusts body actor/tenant fields; the authenticator returns the authenticated
actor and tenant context established by the host's existing auth provider.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Iterable
from urllib.parse import parse_qs, urlsplit

from .authorization import TenantContext
from .contracts import CoreApi
from .errors import CoreError, NotFoundError, ValidationError


@dataclass(frozen=True)
class AuthenticatedActor:
    user_id: str
    organization_id: str


Authenticator = Callable[[dict[str, str]], AuthenticatedActor | None]


def _json(start_response, status: int, payload: dict) -> list[bytes]:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    start_response(f"{status} {'OK' if status < 300 else 'Error'}", [
        ("Content-Type", "application/json"), ("Content-Length", str(len(body))),
    ])
    return [body]


def create_app(api: CoreApi, authenticate: Authenticator, *, ready: Callable[[], bool] | None = None):
    """Return a dependency-free WSGI application.

    ``authenticate`` must validate the host's bearer/session mechanism. A
    missing authenticator is a configuration error; no credential fallback is
    provided by Core.
    """
    if authenticate is None:
        raise ValueError("an application authenticator is required")

    def app(environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = urlsplit(environ.get("PATH_INFO", "")).path.rstrip("/") or "/"
        if method == "GET" and path == "/healthz":
            return _json(start_response, 200, {"status": "ok"})
        if method == "GET" and path == "/readyz":
            ok = True if ready is None else bool(ready())
            return _json(start_response, 200 if ok else 503, {"status": "ready" if ok else "not_ready"})

        headers = {key[5:].replace("_", "-").title(): value for key, value in environ.items() if key.startswith("HTTP_")}
        actor = authenticate(headers)
        if actor is None:
            return _json(start_response, 401, {"error": {"code": "authentication_required", "message": "authentication required", "contract_version": "0.2.0"}})
        parts = [part for part in path.split("/") if part]
        try:
            if len(parts) == 4 and parts[:3] == ["v1", "organizations", parts[2]] and parts[3] == "identity-validation" and method == "POST":
                organization_id = parts[2]
                if actor.organization_id != organization_id:
                    raise NotFoundError("organization not found")
                payload = _body(environ)
                return _json(start_response, 200, api.validate_identity(organization_id, _required(payload, "user_id"), _required(payload, "external_subject")))
            if len(parts) == 4 and parts[:3] == ["v1", "organizations", parts[2]] and parts[3] == "identity-links" and method == "POST":
                organization_id = parts[2]
                if actor.organization_id != organization_id:
                    raise NotFoundError("organization not found")
                payload = _body(environ)
                return _json(start_response, 201, api.link_identity(actor.user_id, organization_id, _required(payload, "person_id"), _required(payload, "user_id"), _required(payload, "external_subject")))
            if len(parts) == 5 and parts[:3] == ["v1", "organizations", parts[2]] and parts[3] == "identity-links" and method == "DELETE":
                organization_id = parts[2]
                if actor.organization_id != organization_id:
                    raise NotFoundError("organization not found")
                return _json(start_response, 200, api.unlink_identity(actor.user_id, organization_id, parts[4]))
            raise NotFoundError("route not found")
        except CoreError as exc:
            return _json(start_response, getattr(exc, "status", 500), {"error": exc.public()})
        except (ValueError, KeyError) as exc:
            error = ValidationError(str(exc))
            return _json(start_response, 400, {"error": error.public()})

    return app


def _required(payload: dict, field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} is required")
    return value.strip()


def _body(environ) -> dict:
    try:
        length = int(environ.get("CONTENT_LENGTH") or "0")
        payload = json.loads(environ["wsgi.input"].read(length) or b"{}")
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValidationError("request body must be valid JSON") from exc
    if not isinstance(payload, dict):
        raise ValidationError("request body must be a JSON object")
    return payload
