class CoreError(Exception):
    """Base error exposed by the Core."""

    code = "core_error"
    status = 500

    def public(self) -> dict[str, object]:
        return {"code": self.code, "message": str(self), "contract_version": "0.2.0"}


class ValidationError(CoreError):
    code = "validation_error"
    status = 400


class NotFoundError(CoreError):
    code = "not_found"
    status = 404


class AuthorizationError(CoreError):
    code = "authorization_denied"
    status = 403


class IsolationError(AuthorizationError):
    code = "cross_tenant_denied"


class ConflictError(CoreError):
    code = "conflict"
    status = 409
