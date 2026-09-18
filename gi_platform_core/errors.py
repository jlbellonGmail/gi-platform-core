class CoreError(Exception):
    """Base error exposed by the Core."""


class ValidationError(CoreError):
    pass


class NotFoundError(CoreError):
    pass


class AuthorizationError(CoreError):
    pass


class IsolationError(AuthorizationError):
    pass
