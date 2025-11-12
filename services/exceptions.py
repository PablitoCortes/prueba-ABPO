class NotFoundError(Exception):
    """Raised when a requested resource is not found."""
    pass


class BadRequestError(Exception):
    """Raised when the input data is invalid or the request cannot be processed."""
    pass
