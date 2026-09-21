"""Command-line WSGI server; authentication remains supplied by the host."""
from __future__ import annotations

import importlib
import os
from wsgiref.simple_server import make_server

from .adapters import InMemoryCoreStore
from .application import CoreService
from .contracts import CoreApi
from .http import create_app


def _load_authenticator(spec: str):
    module_name, separator, attribute = spec.partition(":")
    if not separator:
        raise RuntimeError("CORE_AUTH_MODULE must use package.module:callable")
    return getattr(importlib.import_module(module_name), attribute)


def main() -> None:
    spec = os.environ.get("CORE_AUTH_MODULE")
    if not spec:
        raise RuntimeError("CORE_AUTH_MODULE is required; Core does not invent credentials")
    host = os.environ.get("CORE_HTTP_HOST", "127.0.0.1")
    port = int(os.environ.get("CORE_HTTP_PORT", "8080"))
    api = CoreApi(CoreService(InMemoryCoreStore()))
    with make_server(host, port, create_app(api, _load_authenticator(spec))) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
