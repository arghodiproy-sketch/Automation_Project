"""
core/logger.py — Centralised logging.

Interview Tip:
    Always use the logging module instead of print().
    Reasons:
      • Log levels (DEBUG, INFO, WARNING, ERROR) let you filter output.
      • In CI, logs can be written to a file and attached as an artefact.
      • Each module passes __name__ so you know exactly which class logged.

    Usage:
        from core.logger import get_logger
        log = get_logger(__name__)
        log.info("Step completed")
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger with a consistent console format.
    Adding handlers only when none exist avoids duplicate output
    when the same module is imported multiple times.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:                # guard against duplicate handlers
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False           # don't bubble up to the root logger

    return logger
