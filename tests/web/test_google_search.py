"""
tests/web/test_google_search.py — Google Search web tests.

Interview Tip — Core Selenium skills demonstrated here:

  1. Explicit Waits:
       WebDriverWait + EC avoids flaky tests caused by page load timing.
       Know the difference: presence (in DOM) vs visibility (shown on screen).

  2. Page Object Model:
       GoogleHomePage handles navigation & input.
       GoogleResultsPage handles result reading.
       Tests only call high-level methods — no locators in tests.

  3. Parameterization:
       @pytest.mark.parametrize runs the same scenario with multiple inputs.

  4. Assertions on content, not elements:
       We assert on page.title and result titles (strings), NOT on
       WebElements — this makes assertions clear and side-effect-free.

  Additional Selenium concepts to know for interviews:
    • driver.execute_script("return arguments[0].scrollIntoView()", el)
    • handling iframes: driver.switch_to.frame(el)
    • handling alerts: driver.switch_to.alert.accept()
    • taking screenshots: driver.save_screenshot("name.png")
    • Select dropdowns: from selenium.webdriver.support.ui import Select
"""

import allure
import pytest

from pages.web.google_home_page import GoogleHomePage
from pages.web.google_results_page import GoogleResultsPage


@allure.feature("Google Web Search")
@allure.story("Homepage")
@allure.title("Google homepage loads with correct title")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.web
def test_google_homepage_loads_successfully(web_driver):
    """
    The Google home page should load and the title should contain 'Google'.
    This is a smoke test — verify the site is reachable before deeper tests.
    """
    with allure.step("Open Google homepage"):
        page = GoogleHomePage(web_driver)
        page.open()

    with allure.step("Verify page title contains 'Google'"):
        assert "Google" in web_driver.title, (
            f"Unexpected page title: '{web_driver.title}'"
        )


@allure.feature("Google Web Search")
@allure.story("Search Results")
@allure.title("Search returns at least one result")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.web
def test_search_returns_at_least_one_result(web_driver):
    """Performing a search should load the results page with visible results."""
    with allure.step("Open Google homepage"):
        home = GoogleHomePage(web_driver)
        home.open()

    with allure.step("Search for 'Python automation testing'"):
        home.search("Python automation testing")

    with allure.step("Wait for results page to load"):
        results = GoogleResultsPage(web_driver)
        results.wait_for_results()

    with allure.step("Assert at least one result is returned"):
        titles = results.get_result_titles()
        allure.attach(
            "\n".join(titles),
            name="Result Titles",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert len(titles) > 0, "Expected at least one result heading, got none."
