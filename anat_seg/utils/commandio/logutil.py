# -*- coding: utf-8 -*-
"""Logging utility module.
"""
import logging
from datetime import datetime
from typing import Any, Dict

from fileio import File
from enums import LogLevel


class LogFile(File):
    """Convenience class that creates a log file object for logging purposes.

    Attributes:
        log_file: Log filename.

    Usage examples:
        >>> log = LogFile("file.log",False)
        >>> log
        "file.log"

    Args:
        file: Log filename (need not exist at runtime).
        print_to_screen: If true, prints output to standard output (stdout) as well.
        format_log_str: If true, this formats the logging information with more detail.
        use_root_logger: If true, **ALL** information is written to a single log file.
        level: Logging level. Options include:
            * ``info``
            * ``debug``
            * ``critical``
            * ``error``
            * ``warning``
        exc_info: Adds exception information to the logging message.
        stack_info: Adds stack information to the logging message.
        stacklevel: If greater than 1, the corresponding number of stack
            frames are skipped when computing the line number and function
            name set in the ``LogRecord`` for the logging event.
    """

    def __init__(
        self,
        log_file: str = "",
        print_to_screen: bool = False,
        format_log_str: bool = False,
        use_root_logger: bool = False,
        level: str = "info",
        exc_info: bool = False,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        """Initialization method for the LogFile class. Initiates logging and its associated methods (from the ``logging`` module).

        Usage examples:
            >>> log = LogFile("file.log",False)
            >>> log
            "file.log"

        Args:
            file: Log filename (need not exist at runtime).
            print_to_screen: If true, prints output to standard output (stdout) as well.
            format_log_str: If true, this formats the logging information with more detail.
            use_root_logger: If true, **ALL** information is written to a single log file.
            level: Logging level. Options include:
                * ``info``
                * ``debug``
                * ``critical``
                * ``error``
                * ``warning``
            exc_info: Adds exception information to the logging message.
            stack_info: Adds stack information to the logging message.
            stacklevel: If greater than 1, the corresponding number of stack
                frames are skipped when computing the line number and function
                name set in the ``LogRecord`` for the logging event.
        """
        self.log_file: str = log_file
        level: str = LogLevel(level.lower()).name

        # Define logging
        self.logger = logging.getLogger(__name__)
        super(LogFile, self).__init__(self.log_file)

        # Define logging parameters
        self.params: Dict[str, Any] = {
            "exc_info": bool(exc_info),
            "stack_info": bool(stack_info),
            "stacklevel": int(stacklevel),
        }

        if format_log_str and (level == "debug"):
            FORMAT: str = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            DATEFMT: str = "%m-%d-%y %H:%M:%S"
        elif format_log_str and (level == "info"):
            FORMAT: str = "%(asctime)s %(message)s"
            DATEFMT: str = "%m-%d-%y %H:%M:%S"
        elif format_log_str and (level != "debug"):
            FORMAT: str = "%(asctime)s %(name)s %(message)s"
            DATEFMT: str = "%m-%d-%y %H:%M:%S"
        else:
            FORMAT: str = None
            DATEFMT: str = None

        if level == "info":
            level: logging.INFO = logging.INFO
        elif level == "debug":
            level: logging.DEBUG = logging.DEBUG
        elif level == "critical":
            level: logging.CRITICAL = logging.CRITICAL
        elif level == "error":
            level: logging.ERROR = logging.ERROR
        elif level == "warning":
            level: logging.WARNING = logging.WARNING

        if use_root_logger:
            # Use Basic Config for root level logging
            logging.basicConfig(
                level=level,
                format=FORMAT,
                datefmt=DATEFMT,
                filename=self.log_file,
                filemode="a",
            )
        else:
            # Define logging components
            self.logger.setLevel(level=level)
            file_handler: logging.FileHandler = logging.FileHandler(self.log_file)
            formatter: logging.Formatter = logging.Formatter(FORMAT, DATEFMT)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Define a Handler which writes to the sys.stderr
        if print_to_screen:
            self.console: logging.StreamHandler = logging.StreamHandler()
            self.console.setLevel(level)
            logging.getLogger().addHandler(self.console)

    def info(self, msg: str = "", use_header: bool = False) -> None:
        """Writes information to log file.

        Usage examples:
            >>> log = LogFile("file.log")
            >>> log.info("<str>")

        Args:
            msg: String to be printed to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.logger.info(self._section_header(msg), **self.params)
        else:
            self.logger.info(msg, **self.params)

    def debug(self, msg: str = "", use_header: bool = False) -> None:
        """Writes debug information to file.

        Usage examples:
            >>> log = LogFile("file.log")
            >>> log.debug("<str>")

        Args:
            msg: String to be printed to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.logger.debug(self._section_header(msg), **self.params)
        else:
            self.logger.debug(msg, **self.params)

    def critical(self, msg: str, use_header: bool = False) -> None:
        """Write critical messages/information to file.

        Usage example:
            >>> log = LogFile("file.log")
            >>> log.critical("<str>")

        Args:
            msg: String to be printed to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.logger.critical(self._section_header(msg), **self.params)
        else:
            self.logger.critical(msg, **self.params)

    def error(self, msg: str = "", use_header: bool = False) -> None:
        """Writes error information to file.

        Usage examples:
            >>> log = LogFile("file.log")
            >>> log.error("<str>")

        Args:
            msg: String to be printed to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.logger.error(self._section_header(msg), **self.params)
        else:
            self.logger.error(msg, **self.params)

    def warning(self, msg: str = "", use_header: bool = False) -> None:
        """Writes warnings to file.

        Usage examples:
            >>> log = LogFile("file.log")
            >>> log.warning("<str>")

        Args:
            msg: String to be printed to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.logger.warning(self._section_header(msg), **self.params)
        else:
            self.logger.warning(msg, **self.params)

    def log(self, log_cmd: str = "", use_header: bool = False) -> None:
        """Log function for logging commands and messages to some log file.

        Usage examples:
            >>> log = LogFile("file.log")
            >>> log.log("<str>")

        Args:
            log_cmd: Message to be written to log file.
            use_header: Give log message a section header.
        """
        if use_header:
            self.info(self._section_header(log_cmd))
        else:
            self.info(log_cmd)

    def _section_header(self, msg: str) -> str:
        """Helper function that adds a section header that consists of
        a line break, with the date, time, and message string.

        Usage example:
            >>> _section_header("INFO: This is a test")

            --------------------------------------------------------------------------------------
            Mon Aug 23 13:34:21 2021: INFO: This is a test
            --------------------------------------------------------------------------------------

        Args:
            msg: Message string to have section header.

        Returns:
            String that represents the message with header.
        """
        header: str = f"""\n
--------------------------------------------------------------------------------------
{datetime.now().ctime()}: {msg}
--------------------------------------------------------------------------------------
        """
        return header
