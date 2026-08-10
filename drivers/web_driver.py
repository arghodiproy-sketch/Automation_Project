"""
drivers/web_driver.py — Cross-browser Selenium WebDriver factory.

Interview Tip:
    A Driver Factory creates the correct driver type based on
    configuration — this is the Factory Method design pattern.

    webdriver-manager (pip install webdriver-manager) automatically
    downloads the correct ChromeDriver / GeckoDriver for the installed
    browser version.  Without it you would manually manage binaries.

    Key Selenium concepts for interviews:
      • implicit wait  — global timeout applied to every find_element call
      • explicit wait  — WebDriverWait with ExpectedConditions per element
      • page load timeout — max time for driver.get() to complete
      Rule: NEVER mix implicit + explicit waits (unpredictable behaviour).
      Best practice: set implicit_wait=0, always use explicit waits.
      (We set implicit_wait here as a beginner-friendly default.)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.web_config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, WINDOW_SIZE
from core.base_driver import BaseDriver
from core.logger import get_logger

log = get_logger(__name__)


class WebDriver(BaseDriver):
    """
    Browser driver factory that supports Chrome and Firefox.

    Usage:
        drv = WebDriver(browser="chrome", headless=False)
        driver = drv.start()
        ...
        drv.quit()
    """

    def __init__(self, browser: str = BROWSER, headless: bool = HEADLESS):
        self.browser  = browser.lower()
        self.headless = headless
        self.driver   = None

    # ── BaseDriver contract ───────────────────────────────────────────────────

    def start(self):
        """
        Build, configure, and return a Selenium WebDriver.

        Returns:
            selenium.webdriver.Remote (or local Chrome/Firefox instance).
        """
        log.info("Starting %s (headless=%s)", self.browser, self.headless)

        if self.browser == "chrome":
            self.driver = self._build_chrome()
        elif self.browser == "firefox":
            self.driver = self._build_firefox()
        else:
            raise ValueError(
                f"Unsupported browser '{self.browser}'. Choose 'chrome' or 'firefox'."
            )

        # Global driver settings
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.driver.set_window_size(*WINDOW_SIZE)
        log.info("%s driver ready.", self.browser.capitalize())
        return self.driver

    def quit(self):
        """Close the browser window and end the WebDriver session."""
        if self.driver:
            try:
                self.driver.quit()
                log.info("Browser closed.")
            except Exception as exc:
                log.warning("Error closing browser: %s", exc)
            finally:
                self.driver = None

    # ── Private factory methods ───────────────────────────────────────────────

    def _build_chrome(self):
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")       # modern headless flag
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")             # required in Docker/CI
        options.add_argument("--disable-dev-shm-usage")  # avoids shm crashes
        # Hide automation banner ("Chrome is being controlled by...")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _build_firefox(self):
        options = FirefoxOptions()
        if self.headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
