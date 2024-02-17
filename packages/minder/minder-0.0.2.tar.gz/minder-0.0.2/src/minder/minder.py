"""The `Minder` context manager is given a `Duty` for the duration of its context block.

It exits without raising if an error is encountered by recording it in `error`.
"""

from __future__ import annotations


__all__ = ["Minder", "Duty"]


class Minder:
    """Exceptions raised in this ContextManager become stored as `error`.

    Attributes:
      result: A dict which holds the result.
      failed: A flag indicating whether the operation failed.
    """

    def __init__(self):
        """Prepare an empty dict as `result` and `failed` as `False`."""
        self.result = {}
        self.failed = False

    def __enter__(self):
        """Make the context manager assignable (`with Minder() as ...:`)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suppress the exception: it was already recorded in `result`."""
        return exc_type is not None

    def duty(self, where: str, recoverable: bool = False) -> Duty:
        """Prepare to record a `Duty` associated with this result."""
        return Duty(mgr=self, where=where, recoverable=recoverable)

    def record_breach(self, where: str, error: str) -> None:
        """Record the serialised `error` message and its location `where` in the `result`."""
        self.failed = True
        self.result = {"error": error, "where": where}
        return

    def record_result(self, result) -> None:
        """Record a positive `result`."""
        self.result = result
        return

    def report(self) -> dict:
        """Provide a simple interface: `result` and `success` bool.

        If the operation failed the `result` will be a dict of an `error` message
        and `where` (the location of the `Duty` in which the exception raised).
        """
        return {"result": self.result, "success": not self.failed}


class Duty:
    """Ensures any exception is handled and stored in `result` upon early exit."""

    mgr: Minder
    where: str
    recoverable: bool

    def __init__(self, mgr: Minder, where: str, recoverable: bool):
        """Register the `Minder` to report to and how to handle an incident.

        Prepare to report `where` the breach occurred, and whether to suppress the
        exception (if `recoverable` the error will not halt further execution upon
        exit of the `Duty` context manager block).
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
            if not self.recoverable:
                self.mgr.record_breach(error=error, where=self.where)
            return self.recoverable  # Suppress the exception if it was recoverable
