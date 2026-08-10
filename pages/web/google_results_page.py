"""
pages/web/google_results_page.py — Google Search Results Page Object.

Interview Tip — Splitting pages by screen:
    Google home page and results page are TWO different Page Objects
    even though they look similar.  This models the user's mental model
    ("I am on the results page now") and prevents page classes from
    growing too large.

    After calling GoogleHomePage.search(), the browser navigates to
    the results page.  The test then creates a GoogleResultsPage object
    passing the SAME driver — no new browser session is opened.
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_WAIT_TIMEOUT
from core.base_page import BasePage
from core.logger import get_logger
from locators.web.google_locators import FIRST_RESULT, RESULT_LINKS, RESULTS_STATS

log = get_logger(__name__)


class GoogleResultsPage(BasePage):
    """
    Page Object for the Google search results page.

    Exposes read-only helpers so tests can assert on what was returned.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)

    # ── Wait helpers ──────────────────────────────────────────────────────────

    def wait_for_results(self) -> "GoogleResultsPage":
        """Block until at least one result heading is present in the DOM."""
        log.info("Waiting for search results…")
        self._wait.until(EC.presence_of_element_located(RESULT_LINKS))
        log.info("Results page loaded.")
        return self

    # ── Data accessors ────────────────────────────────────────────────────────

    def get_result_titles(self) -> list:
        """
        Return a list of all organic result heading texts.

        Example return value: ["Python.org", "Learn Python — Free Tutorial", ...]
        """
        elements = self.driver.find_elements(*RESULT_LINKS)
        titles = [el.text for el in elements if el.text]
        log.info("Found %d result titles.", len(titles))
        return titles

    def get_first_result_title(self) -> str:
        """Return the heading text of the first search result."""
        element = self._wait.until(EC.visibility_of_element_located(FIRST_RESULT))
        title = element.text
        log.info("First result: '%s'", title)
        return title

    def get_results_stats(self) -> str:
        """
        Return the 'About N results (X seconds)' stats line.
        Returns empty string if the element is not present.
        """
        try:
            el = self._wait.until(EC.presence_of_element_located(RESULTS_STATS))
            return el.text
        except Exception:
            return ""

    @property
    def title(self) -> str:
        """The current browser page title (e.g. 'Python - Google Search')."""
        return self.driver.title

    @property
    def current_url(self) -> str:
        """The current browser URL."""
        return self.driver.current_url
