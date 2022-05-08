# -*- coding: utf-8 -*-
"""Enums module for the ``commandio`` package.
"""
from enum import Enum, unique


@unique
class LogLevel(Enum):
    """Log level enumerators."""

    info: str = "info"
    debug: str = "debug"
    critical: str = "critical"
    error: str = "error"
    warning: str = "warning"
