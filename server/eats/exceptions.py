class EATSException (Exception):

    """Base class for all EATS-specific exceptions."""

    pass


class EATSExportException (EATSException):

    """Exception raised when there is a problem with an export."""

    pass


class EATSValidationException (EATSException):

    """Exception raised when invalid data is supplied to an EATS
    model."""

    pass
