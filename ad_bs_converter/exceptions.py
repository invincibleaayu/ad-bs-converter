class ADDateOutOfBoundsError(Exception):
    """
    Exception raised when the provided AD date is outside the supported range.

    This exception is raised when:
    1. The date is before the earliest supported date (Reference date)
    2. The date is outside the min/max AD year range
    3. The conversion results in a BS year with no available data
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a message.

        Args:
            message: The error message
        """
        super().__init__(message)
