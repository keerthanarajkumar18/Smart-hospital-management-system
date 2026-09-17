"""Decorators used by the hospital management system."""

from datetime import datetime
from functools import wraps


def audit_log(function):
    """Record who performed an operation and when."""

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        """Log the operation and then run the function."""

        user = kwargs.get("user")

        if user is None and args:
            user = args[-1]

        if user is None:
            user = "System"

        timestamp = datetime.now()

        self.logger.logger.info(
            "AUDIT | Time: %s | User: %s | Operation: %s",
            timestamp,
            user,
            function.__name__,
        )

        return function(
            self,
            *args,
            **kwargs,
        )

    return wrapper