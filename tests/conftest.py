"""
conftest.py — pytest fixtures shared across ALL test modules.

Interview Tip — conftest.py fundamentals:
    • Automatically discovered by pytest — no imports needed in test files.
    • Fixtures defined here are available to every test in this directory
      AND all sub-directories (desktop/, mobile/, web/).
    • The conftest.py hierarchy allows you to scope fixtures:
        root conftest     → shared by everything
        tests/conftest    → shared by all tests
        tests/web/conftest → shared only by web tests

Fixture scopes — key interview topic:
    function  (default) → new instance per test function
    class               → shared within a test class
    module              → shared within one .py file
    session             → shared for the entire pytest run

    Use session scope for expensive setup (launching a browser/emulator
    once) but ONLY when tests do NOT modify shared state.
    Use function scope when tests create/delete data to avoid pollution.

Yield fixtures:
    Everything BEFORE yield = setup (like setUp in unittest).
    Everything AFTER yield  = teardown (like tearDown / finally).
    Teardown always runs — even if the test or setup raises an exception.
"""

import pytest

from drivers.desktop_driver import DesktopDriver
from drivers.mobile_driver import MobileDriver
from drivers.web_driver import WebDriver


# ── Custom CLI options ────────────────────────────────────────────────────────
# Interview Tip: addoption lets you pass runtime parameters to fixtures
# without hardcoding values.  Usage: pytest --browser=firefox --headless

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser for web tests: chrome (default) | firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (no UI window).",
    )
    parser.addoption(
        "--appium-url",
        default="http://127.0.0.1:4723/wd/hub",
        help="Appium server URL for mobile tests.",
    )


# ── Desktop fixture ───────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def desktop_window():
    """
    Launch Windows Calculator and yield the window handle.

    Scope = function: a fresh Calculator is launched for EACH test.
    This prevents one test's state (e.g. a running total) from
    affecting the next test.

    Teardown: the app is killed after the test regardless of pass/fail.
    """
    drv = DesktopDriver()
    window = drv.start()
    yield window           # ← the fixture value received by the test
    drv.quit()             # ← always runs (teardown)


# ── Mobile fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def mobile_driver(request):
    """
    Open an Appium session for the Android Calculator and yield the driver.

    Prerequisites:
        1. Start Appium:     appium
        2. Boot emulator:    emulator -avd <AVD_NAME>

    The Appium server URL can be overridden on the CLI:
        pytest --appium-url=http://192.168.1.10:4723
    """
    server_url = request.config.getoption("--appium-url")
    drv = MobileDriver(server_url=server_url)
    driver = drv.start()
    yield driver
    drv.quit()


# ── Web fixture ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def web_driver(request):
    """
    Create a Selenium WebDriver instance and yield it.

    Browser and headless mode can be set via CLI:
        pytest --browser=firefox --headless

    Scope = function: a new browser is opened for EACH test.
    For faster runs, change to scope="module" or scope="session"
    when tests are read-only (no data mutation between tests).
    """
    browser  = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drv = WebDriver(browser=browser, headless=headless)
    driver = drv.start()
    yield driver
    drv.quit()
