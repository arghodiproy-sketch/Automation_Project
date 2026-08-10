"""
core/base_page.py — Abstract Base Page (foundation of the Page Object Model).

Interview Tip:
    The Page Object Model (POM) is the #1 most-asked design pattern
    in automation interviews.  Key points to articulate:

    PROBLEM it solves:
        Without POM, locators and actions are duplicated across tests.
        One locator change requires updating every test that uses it.

    SOLUTION:
        Each screen / page has ONE class that owns:
          • its locators  (what to find)
          • its actions   (how to interact)
        Tests only call high-level methods like page.search("Python").

    BENEFITS:
        Reusability    — one page class used by many tests
        Maintainability — locator updates in one place only
        Readability    — tests read like plain-English scenarios
        Separation     — UI detail hidden from test logic
"""

from abc import ABC


class BasePage(ABC):
    """
    All Page Object classes inherit from this.

    The driver is injected via the constructor (Dependency Injection).
    This makes pages testable in isolation — you can pass a mock driver.
    """

    def __init__(self, driver):
        # 'driver' is intentionally generic:
        #   desktop → pywinauto WindowSpecification
        #   mobile  → appium.webdriver.Remote
        #   web     → selenium.webdriver (Chrome/Firefox)
        self.driver = driver
