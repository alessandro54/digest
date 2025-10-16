# apps/api/app/core/errors.py
"""
Domain-level error definitions for Digest backend.

These exceptions should be raised inside services and caught
by routes (controllers) to return appropriate HTTP responses.
"""


class NotFoundError(Exception):
    """Raised when a requested entity does not exist in the database."""

    pass


class ConflictError(Exception):
    """Raised when a unique constraint is violated or duplicate data is detected."""

    pass


class DisabledError(Exception):
    """Raised when an entity is disabled and an operation cannot proceed."""

    pass


class UpstreamError(Exception):
    """Raised when an external service (e.g., RSS/HTTP/API) fails or returns invalid data."""

    pass


class ValidationError(Exception):
    """Raised when input data fails domain-level validation."""

    pass
