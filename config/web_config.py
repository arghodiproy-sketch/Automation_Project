"""
config/web_config.py — Selenium / browser settings.

Interview Tip:
    headless=True is essential in CI/CD (no display available).
    webdriver-manager auto-downloads the matching ChromeDriver so
    you never have to manage binary versions manually — a common
    pain point that interviewers love to discuss.
"""

BASE_URL         = "https://www.google.com"
BROWSER          = "chrome"        # "chrome" | "firefox"
HEADLESS         = False           # set True for CI pipelines
IMPLICIT_WAIT    = 10              # seconds — applied globally to the driver
PAGE_LOAD_TIMEOUT = 30             # seconds
WINDOW_SIZE      = (1920, 1080)    # (width, height) in pixels
