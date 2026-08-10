"""
pages/mobile/calculator_page.py — Android Calculator Page Object.

Interview Tip — Cross-platform consistency:
    Notice that this class exposes the SAME public interface as
    DesktopCalculatorPage: clear(), press(), calculate(), get_result().

    This is the Strategy pattern: the caller (test) doesn't care WHICH
    platform it's running on — it just calls calculate("5+5=") and
    asserts the result.  Swapping platforms = swapping the page object.

    Appium find strategies used here:
      AppiumBy.ID → Android resource-id (fastest, most reliable)
      AppiumBy.ACCESSIBILITY_ID → content-desc (fallback)
"""

from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage
from core.logger import get_logger
from locators.mobile.calculator_locators import KEY_MAP, RESULT_FORMULA

log = get_logger(__name__)


class MobileCalculatorPage(BasePage):
    """
    Page Object for the Android AOSP Calculator app.

    Accepts an Appium webdriver.Remote instance as its driver.

    Example usage in a test:
        page = MobileCalculatorPage(appium_driver)
        page.clear()
        assert page.calculate("12+7=") == "19"
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ── Low-level helper ──────────────────────────────────────────────────────

    def _tap(self, resource_id: str) -> None:
        """Find an element by Android resource ID and tap it."""
        element = self.driver.find_element(AppiumBy.ID, resource_id)
        element.click()

    # ── Page actions ──────────────────────────────────────────────────────────

    def clear(self) -> "MobileCalculatorPage":
        """Tap the Clear (CLR) button to reset the calculator."""
        log.debug("Clearing calculator.")
        self._tap(KEY_MAP["C"])
        return self

    def press(self, key: str) -> "MobileCalculatorPage":
        """
        Tap the button corresponding to the given key character.

        Args:
            key: A single character, e.g. "5", "+", "=", "C"

        Raises:
            ValueError: If the key has no mapped locator.
        """
        resource_id = KEY_MAP.get(key)
        if resource_id is None:
            raise ValueError(
                f"No locator mapped for key '{key}'. "
                f"Available keys: {list(KEY_MAP.keys())}"
            )
        log.debug("Tapping key '%s'  →  %s", key, resource_id)
        self._tap(resource_id)
        return self

    def calculate(self, expression: str) -> str:
        """
        Tap through a full expression and return the displayed result.

        Args:
            expression: e.g. "12+7=" or "50*2="
        Returns:
            The text shown in the formula display.
        """
        log.info("Calculating expression: '%s'", expression)
        for char in expression:
            self.press(char)
        return self.get_result()

    def get_result(self) -> str:
        """Return the current text of the formula/result display."""
        element = self.driver.find_element(AppiumBy.ID, RESULT_FORMULA)
        result = element.text.strip()
        log.info("Display shows: '%s'", result)
        return result
