# Feature 10 — Package version consistency

## Outcome

Align the package's exported `__version__` with the distributable project version `0.2.1`.

## Scope

Only the package metadata export, its regression test, and the roadmap work-unit record are changed. CoreApi's public contract remains `0.2.0` for compatibility.

## Acceptance

- A clean wheel for project version `0.2.1` imports with `gi_platform_core.__version__ == "0.2.1"`.
- The existing CoreApi contract remains unchanged.
- The full product and circuit suites pass.
