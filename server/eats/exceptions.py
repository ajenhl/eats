class EATSException (Exception):

    """Base class for all EATS-specific exceptions."""

    pass


class EATSValidationException (EATSException):

    """Exception raised when invalid data is supplied to an EATS
    model."""

    pass
