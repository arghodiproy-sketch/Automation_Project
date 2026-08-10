"""
drivers/mobile_driver.py — Android automation driver using Appium.

Interview Tip:
    Appium acts as an HTTP server that translates WebDriver Wire Protocol
    commands into native mobile gestures.  Key concepts:

    UiAutomator2  — Google's Android UI testing framework; Appium wraps it.
    Session       — each test run = one Appium session (like a browser tab).
    Capabilities  — JSON object describing device + app to automate.

    Common interview questions:
      Q: What is the difference between noReset, fullReset, and fastReset?
      A: noReset=True  → keep app data, don't reinstall (fastest)
         noReset=False → clear app data before session (default)
         fullReset=True → uninstall + reinstall app (slowest, cleanest)
"""

from urllib.error import URLError
from urllib.request import Request, urlopen

from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.mobile_config import ANDROID_OPTIONS, APPIUM_SERVER_URL
from core.base_driver import BaseDriver
from core.logger import get_logger

log = get_logger(__name__)


class MobileDriver(BaseDriver):
    """
    Creates and manages an Appium session for Android.
    """

    def __init__(self, server_url: str = APPIUM_SERVER_URL):
        self.server_url = server_url
        self.driver     = None

    # ── BaseDriver contract ───────────────────────────────────────────────────

    def start(self):
        """
        Validate Appium is reachable, then open a new session.

        Returns:
            appium.webdriver.Remote — the active Appium driver instance.
        """
        self._check_appium_server()
        log.info("Starting Appium session at %s", self.server_url)

        options = UiAutomator2Options()
        options.platform_name        = ANDROID_OPTIONS["platformName"]
        options.automation_name      = ANDROID_OPTIONS["automationName"]
        options.device_name          = ANDROID_OPTIONS["deviceName"]
        options.app_package          = ANDROID_OPTIONS["appPackage"]
        options.app_activity         = ANDROID_OPTIONS["appActivity"]
        options.no_reset             = ANDROID_OPTIONS["noReset"]
        options.new_command_timeout  = ANDROID_OPTIONS["newCommandTimeout"]

        self.driver = webdriver.Remote(
            command_executor=self.server_url,
            options=options,
        )
        log.info("Appium session started  id=%s", self.driver.session_id)
        return self.driver

    def quit(self):
        """End the Appium session and release the device."""
        if self.driver:
            try:
                self.driver.quit()
                log.info("Appium session closed.")
            except Exception as exc:
                log.warning("Error closing Appium driver: %s", exc)
            finally:
                self.driver = None

    # ── Pre-flight check ──────────────────────────────────────────────────────

    def _check_appium_server(self):
        """
        Fail fast with a clear error if Appium is not reachable.
        Prevents a confusing 'connection refused' from deep inside Appium.
        """
        status_url = self.server_url.rstrip("/") + "/status"
        try:
            req = Request(status_url, headers={"User-Agent": "python"})
            with urlopen(req, timeout=5) as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        f"Appium server returned HTTP {resp.status} — "
                        "check that Appium is running."
                    )
        except URLError as exc:
            raise RuntimeError(
                f"Cannot reach Appium at {status_url}.\n"
                f"  Start Appium with: appium\n"
                f"  Original error: {exc}"
            ) from exc
