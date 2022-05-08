# -*- coding: utf-8 -*-
"""Utility module for the ``commandio`` package.
"""
import os

from time import time
from typing import Optional

from logutil import LogFile
from tmpfile import TmpFile


# Globlally define (temporary) log file object
with TmpFile(tmp_dir=os.getcwd(), ext=".log") as tmpf:
    log: LogFile = LogFile(log_file=tmpf.src)


def timeops(log: Optional[LogFile] = None) -> callable:
    """Decorator function that times some operation and writes that time to
    a log file object.

    Usage example:
        >>> from logutil import LogFile
        >>> log = LogFile('my_log_file.log')
        >>>
        >>> @timeops(log)
        >>> def my_func(args*, log):
        ...     for i in args:
        ...         log.log(f"This is an arg: {i}")
        ...     return None
        ...
        >>> # The length of time to complete the operation
        >>> # should be written to the log file.
        >>> myfunc(args*, log)

    Args:
        log: Log file object to be written to.

    Returns:
        Callable function/class
    """

    def decor(func: callable) -> callable:
        """Inner decorated function that accepts functions."""

        def timed(*args, **kwargs) -> callable:
            """Nested decorator function that performs timing of an operation."""
            start: float = time()
            if log:
                log.log(f"BEGIN: {func.__name__}", use_header=True)
            result: callable = func(*args, **kwargs)
            end: float = time()
            if log:
                log.log(
                    f"END: {func.__name__}  |  Time elapsed: {(end - start):2f} sec.",
                    use_header=True,
                )
            return result

        return timed

    return decor
