"""
utils/helpers.py — Reusable, stateless helper functions.

Interview Tip:
    Keep helpers PURE (no side effects, no driver dependency).
    If a helper needs a driver it belongs on the Page Object, not here.

    Helpers here are utility functions that any test or page can use
    without needing to know about the automation framework details.
"""

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(func: Callable[[], T], attempts: int = 3, delay: float = 1.0) -> T:
    """
    Retry a zero-argument callable up to `attempts` times.

    Useful when an action may transiently fail (e.g. stale element,
    network hiccup) and retrying once or twice is acceptable.

    Args:
        func:     Zero-argument callable to retry.
        attempts: Maximum number of tries (default 3).
        delay:    Seconds to wait between retries (default 1.0).

    Returns:
        The return value of the first successful call.

    Raises:
        The last exception raised if all attempts fail.

    Example:
        title = retry(lambda: results_page.get_first_result_title(), attempts=3)
    """
    last_exc: Exception = RuntimeError("retry() called with attempts=0")
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception as exc:
            last_exc = exc
            if attempt < attempts:
                time.sleep(delay)
    raise last_exc


def normalize_number(text: str) -> str:
    """
    Strip display prefixes, whitespace, and thin-space separators from a
    calculator result string so it can be compared to a plain number.

    Handles:
      - Windows "Display is 19" prefix
      - Android thin-space thousand separators "1 000"
      - Leading/trailing whitespace

    Args:
        text: Raw string from a calculator display element.

    Returns:
        Clean numeric string suitable for assertion, e.g. "1000".

    Example:
        assert normalize_number("Display is 1 000") == "1000"
    """
    cleaned = text.replace("Display is", "").replace("\u202f", "").replace(" ", "").strip()
    return cleaned
