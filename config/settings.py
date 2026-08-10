"""
config/settings.py — Framework-wide constants.

Interview Tip:
    Centralising configuration avoids "magic strings" scattered across
    tests.  Change one value here and it affects the whole suite.
    In production frameworks this file often reads from environment
    variables or a YAML/JSON file so CI can override values without
    editing code.
"""

import os

# ── Project root (two levels up from this file) ───────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Default timeouts (seconds) ────────────────────────────────────────────────
DEFAULT_WAIT_TIMEOUT  = 20   # max time to wait for a window/page to be ready
ELEMENT_WAIT_TIMEOUT  = 10   # max time to wait for a single element
PAGE_LOAD_TIMEOUT     = 30   # max time for a browser page to finish loading

# ── Supported platforms ───────────────────────────────────────────────────────
PLATFORMS = ("desktop", "mobile", "web")
DEFAULT_PLATFORM = "desktop"
