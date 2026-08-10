"""
pages/desktop/calculator_page.py — Windows Calculator Page Object.

Interview Tip — Page Object Model key rules:
  1. A Page Object represents ONE screen / application window.
  2. Methods represent USER ACTIONS ("click add", "get result").
  3. Methods should return 'self' for action chains (fluent interface),
     or return data when a test needs to assert on it.
  4. NEVER put assertions inside page objects — assertions belong in tests.
  5. NEVER use sleep() — use explicit waits.

Two interaction strategies are shown here:
  • keyboard  — fast, realistic, closest to user behaviour
  • click     — explicit, easy to debug when a key mapping is unclear
"""

from pywinauto.keyboard import send_keys

from config.settings import ELEMENT_WAIT_TIMEOUT
from core.base_page import BasePage
from core.logger import get_logger
from locators.desktop.calculator_locators import KEYBOARD_MAP, RESULT_DISPLAY

log = get_logger(__name__)


class DesktopCalculatorPage(BasePage):
    """
    Page Object for the Windows 10/11 Calculator (Standard mode).

    Accepts a pywinauto WindowSpecification as its driver.

    Example usage in a test:
        page = DesktopCalculatorPage(desktop_window)
        page.clear()
        assert page.calculate("12+7=") == "19"
    """

    def __init__(self, window):
        super().__init__(window)     # stores as self.driver

    # ── Low-level helper ──────────────────────────────────────────────────────

    def _send_key(self, key: str) -> None:
        """Map a character to its pywinauto key code and send it."""
        key_code = KEYBOARD_MAP.get(key, key)
        try:
            # type_keys sends to the focused window
            self.driver.type_keys(key_code, set_foreground=True, pause=0.05)
        except Exception:
            # Fallback: send via the global keyboard hook
            send_keys(key_code, pause=0.05, vk_packet=True)

    # ── Page actions ──────────────────────────────────────────────────────────

    def clear(self) -> "DesktopCalculatorPage":
        """
        Press Escape to clear the current entry.
        Returns self for fluent chaining: page.clear().calculate("5+5=")
        """
        log.debug("Clearing calculator.")
        self._send_key("C")
        return self

    def press(self, key: str) -> "DesktopCalculatorPage":
        """Press a single key (digit or operator)."""
        log.debug("Key pressed: %s", key)
        self._send_key(key)
        return self

    def calculate(self, expression: str) -> str:
        """
        Type a complete expression and return the displayed result.

        Args:
            expression: String like "12+7=" or "100/4="
                        Must end with "=" to evaluate.
        Returns:
            The result text shown on the display (e.g. "19").
        """
        log.info("Calculating expression: '%s'", expression)
        for char in expression:
            self.press(char)
        return self.get_result()

    def get_result(self) -> str:
        """
        Read and return the value currently shown on the result display.

        Waits up to ELEMENT_WAIT_TIMEOUT seconds for the element.
        Strips the accessibility prefix "Display is" that Windows adds.
        """
        result_elem = self.driver.child_window(**RESULT_DISPLAY)
        result_elem.wait("visible ready", timeout=ELEMENT_WAIT_TIMEOUT)
        raw_text = result_elem.window_text()
        result = raw_text.replace("Display is", "").strip()
        log.info("Display shows: '%s'", result)
        return result
