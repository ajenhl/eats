class EATSException (Exception):

    """Base class for all EATS-specific exceptions."""

    pass


class EATSExportException (EATSException):

    """Exception raised when there is a problem with an export."""

    pass


class EATSImportException (EATSException):

    """Exception raised when there is a problem with an import."""

    pass


class EATSMergedIdentifierException (EATSException):

    """Exception raised when an entity identifier that no longer exists
    due to merging is used.

    """

    def __init__ (self, new_id):
        self.new_id = new_id


class EATSMLException (EATSException):

    """Exception raised when there is a problem with an EATSML
    document."""

    pass


class EATSValidationException (EATSException):

    """Exception raised when invalid data is supplied to an EATS
    model."""

    pass
