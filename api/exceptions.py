class InvalidOpeningHoursError(Exception):
    """Raised when opening hours are provided with invalid format."""


class InvalidStateError(InvalidOpeningHoursError):
    """Raised if :
        - there are two same consecutive states
        - first state is open
        - last state is close
    """


class InvalidIntervalError(InvalidOpeningHoursError):
    """Raised when interval lasted for too long."""
