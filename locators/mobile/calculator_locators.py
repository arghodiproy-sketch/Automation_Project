"""
locators/mobile/calculator_locators.py

Interview Tip:
    Android locator strategies — ranked by reliability and speed:
      1. By.ID (resource-id)      ← fastest; use when available
      2. By.ACCESSIBILITY_ID      ← content-desc; good for images/icons
      3. By.CLASS_NAME            ← broad; works when ID is unavailable
      4. By.XPATH                 ← most powerful but SLOWEST; avoid if possible
      5. By.ANDROID_UIAUTOMATOR  ← native Android selector; powerful
      6. By.ANDROID_DATA_MATCHER ← Espresso-style; needs specific setup

    Full resource-id format:  "com.package.name:id/local_id"
    Always use the full ID — Appium does not auto-prefix the package.
"""

APP_PACKAGE = "com.android.calculator2"


def _id(local_id: str) -> str:
    """Build a fully-qualified Android resource ID."""
    return f"{APP_PACKAGE}:id/{local_id}"


# ── Display elements ───────────────────────────────────────────────────────────
RESULT_FORMULA = _id("formula")   # live expression as you type
RESULT_DISPLAY = _id("result")    # final result after pressing =

# ── Number buttons ─────────────────────────────────────────────────────────────
BTN_0 = _id("digit_0")
BTN_1 = _id("digit_1")
BTN_2 = _id("digit_2")
BTN_3 = _id("digit_3")
BTN_4 = _id("digit_4")
BTN_5 = _id("digit_5")
BTN_6 = _id("digit_6")
BTN_7 = _id("digit_7")
BTN_8 = _id("digit_8")
BTN_9 = _id("digit_9")

# ── Operator buttons ───────────────────────────────────────────────────────────
BTN_ADD      = _id("op_add")
BTN_SUBTRACT = _id("op_sub")
BTN_MULTIPLY = _id("op_mul")
BTN_DIVIDE   = _id("op_div")
BTN_EQUALS   = _id("eq")
BTN_CLEAR    = _id("clr")
BTN_DELETE   = _id("del")
BTN_DECIMAL  = _id("dec_point")

# ── Key → locator lookup map ───────────────────────────────────────────────────
# Used by MobileCalculatorPage.press(key) to resolve an expression character
# to the correct button resource ID.
KEY_MAP: dict[str, str] = {
    "0": BTN_0, "1": BTN_1, "2": BTN_2, "3": BTN_3, "4": BTN_4,
    "5": BTN_5, "6": BTN_6, "7": BTN_7, "8": BTN_8, "9": BTN_9,
    "+": BTN_ADD,
    "-": BTN_SUBTRACT,
    "*": BTN_MULTIPLY,
    "/": BTN_DIVIDE,
    "=": BTN_EQUALS,
    "C": BTN_CLEAR,
    ".": BTN_DECIMAL,
}
