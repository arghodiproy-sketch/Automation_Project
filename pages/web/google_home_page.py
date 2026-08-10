"""
pages/web/google_home_page.py — Google Home Page Object.

Interview Tip — Explicit Waits (the MOST important Selenium concept):
    NEVER use time.sleep() in tests — it makes suites slow and fragile.
    Use WebDriverWait with ExpectedConditions (EC) instead.

    Most-used EC matchers (memorise these for interviews):
      EC.presence_of_element_located(locator)    → element exists in DOM
      EC.visibility_of_element_located(locator)  → element is visible
      EC.element_to_be_clickable(locator)        → visible AND enabled
      EC.text_to_be_present_in_element(locator)  → specific text in element
      EC.title_contains("text")                  → page title check
      EC.url_contains("text")                    → URL check
      EC.staleness_of(element)                   → element removed from DOM

    Rule: set implicit_wait to 0 in production frameworks and rely
    entirely on explicit waits for predictable, debuggable behaviour.
"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_WAIT_TIMEOUT
from config.web_config import BASE_URL
from core.base_page import BasePage
from core.logger import get_logger
from locators.web.google_locators import SEARCH_INPUT

log = get_logger(__name__)


class GoogleHomePage(BasePage):
    """
    Page Object for https://www.google.com

    Represents the landing page where users type their search query.
    """

    URL = BASE_URL

    def __init__(self, driver):
        super().__init__(driver)
        # WebDriverWait is created once and reused — avoids repeated instantiation
        self._wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self) -> "GoogleHomePage":
        """Navigate to the Google home page."""
        log.info("Opening: %s", self.URL)
        self.driver.get(self.URL)
        return self

    # ── Page actions ──────────────────────────────────────────────────────────

    def enter_search_query(self, query: str) -> "GoogleHomePage":
        """
        Wait for the search box, clear it, and type the query.

        Args:
            query: The text to search for.
        """
        log.info("Typing query: '%s'", query)
        search_box = self._wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
        search_box.clear()
        search_box.send_keys(query)
        return self

    def submit_search(self) -> "GoogleHomePage":
        """Press Enter to submit the search form."""
        log.info("Submitting search.")
        search_box = self._wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
        search_box.send_keys(Keys.RETURN)
        return self

    def search(self, query: str) -> "GoogleHomePage":
        """
        Convenience method: enter a query and submit in one call.

        Returns self so tests can chain further calls if needed.
        """
        return self.enter_search_query(query).submit_search()
