"""
drivers/desktop_driver.py — Windows application driver using pywinauto.

Interview Tip:
    pywinauto works through the Windows Accessibility framework.
    Two backends exist:
      'uia'   — UI Automation API  (modern apps, UWP, WPF)
      'win32' — legacy Win32/MFC apps

    The Windows 10/11 Calculator is a UWP app → always use 'uia'.

    Desktop(backend='uia').window(...) is preferred over
    app.top_window() because it finds the window by stable attributes
    (title, class_name) rather than z-order position.
"""

from pywinauto import Application, Desktop

from config.desktop_config import (
    BACKEND,
    CALCULATOR_APP,
    CALCULATOR_WINDOW_CLASS,
    CALCULATOR_WINDOW_TITLE,
)
from config.settings import DEFAULT_WAIT_TIMEOUT
from core.base_driver import BaseDriver
from core.logger import get_logger

log = get_logger(__name__)


class DesktopDriver(BaseDriver):
    """
    Manages launching and closing a Windows desktop application.

    Inherits from BaseDriver — enforces start() and quit() contract.
    """

    def __init__(self, app_path: str = CALCULATOR_APP):
        self.app_path = app_path
        self.app      = None
        self.window   = None

    # ── BaseDriver contract ───────────────────────────────────────────────────

    def start(self):
        """
        Launch the application and return the focused window handle.

        Returns:
            pywinauto.WindowSpecification — the main Calculator window.
        """
        log.info("Launching desktop app: %s", self.app_path)
        self.app = Application(backend=BACKEND).start(self.app_path)

        # Desktop.window() locates the window system-wide by stable attributes.
        self.window = Desktop(backend=BACKEND).window(
            title=CALCULATOR_WINDOW_TITLE,
            class_name=CALCULATOR_WINDOW_CLASS,
            found_index=0,
        )
        self.window.wait("visible enabled ready", timeout=DEFAULT_WAIT_TIMEOUT)
        self.window.set_focus()
        log.info("Calculator window is ready.")
        return self.window

    def quit(self):
        """Kill the application process if it is still running."""
        if self.app:
            try:
                self.app.kill()
                log.info("Desktop application closed.")
            except Exception as exc:
                log.warning("Could not kill application: %s", exc)
            finally:
                self.app   = None
                self.window = None
