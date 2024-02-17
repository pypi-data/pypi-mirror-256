"""The `Minder` context manager carries out duties in blocks.

It exits without raising if an error is encountered by recording it as a `Duty`.
"""

from __future__ import annotations


__all__ = ["Minder", "Duty"]


class Minder:
    """Exceptions raised in this ContextManager become stored as `errors`."""

    def __init__(self):
        """Prepare an empty dict as `result` and empty list for `errors`."""
        self.result = {}
        self.errors = []

    def __enter__(self):
        """Make the context manager assignable (`with Minder() as ...:`)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suppress the exception: it was already recorded in `errors`."""
        return exc_type is not None

    def duty(self, where: str, recoverable: bool = False) -> Duty:
        """Prepare to record a `Duty` associated with this result."""
        return Duty(mgr=self, where=where, recoverable=recoverable)

    def record_breach(self, where: str, error: str) -> None:
        """Add the serialised `error` and its location `where` to the `errors` list."""
        self.errors.append({"error": error, "where": where})
        return


class Duty:
    """Ensures any exception is handled and stored in `response` upon early exit."""

    mgr: Minder
    where: str
    recoverable: bool

    def __init__(self, mgr: Minder, where: str, recoverable: bool):
        """Register the `Minder` to report to and how to handle an incident.

        Prepare to report `where` the breach occurred, and whether to suppress the
        exception (if `recoverable` the error will be reported but will not halt further
        execution upon completion and exit of the `Duty` block).
        """
        self.mgr = mgr
        self.where = where
        self.recoverable = recoverable

    def __enter__(self):
        """Do not make the `Duty` instance an assignable value."""
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Handle error serialisation based on exception type.

        Record any such serialised exceptions to the `Minder`.
        """
        if exc_type is None:
            return False
        else:
            match exc_val:
                # from pydantic import ValidationError
                # case ValidationError() as ve:
                #     error = ve.json()
                case _:
                    error = str(exc_val)
            self.mgr.record_breach(error=error, where=self.where)
            return self.recoverable  # Only suppress the exception if it was recoverable
