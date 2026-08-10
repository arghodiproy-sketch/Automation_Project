"""
locators/desktop/calculator_locators.py

Interview Tip:
    Keeping locators in a SEPARATE FILE from the page object is best
    practice.  When a UI change moves or renames a control, you update
    ONE place — the locator file — and every page/test is instantly fixed.

    pywinauto locators are keyword-argument dictionaries passed to
    window.child_window(**locator).  The most reliable attributes are:
      auto_id      — the AutomationId set by the developer (stable)
      control_type — "Button", "Text", "Edit", etc.
      title        — the accessible name / label (can change with locale!)

    Prefer auto_id over title when it is available.
"""

# ── Result display ─────────────────────────────────────────────────────────────
RESULT_DISPLAY = {"auto_id": "CalculatorResults", "control_type": "Text"}

# ── Number buttons ─────────────────────────────────────────────────────────────
BTN_0 = {"auto_id": "num0Button", "control_type": "Button"}
BTN_1 = {"auto_id": "num1Button", "control_type": "Button"}
BTN_2 = {"auto_id": "num2Button", "control_type": "Button"}
BTN_3 = {"auto_id": "num3Button", "control_type": "Button"}
BTN_4 = {"auto_id": "num4Button", "control_type": "Button"}
BTN_5 = {"auto_id": "num5Button", "control_type": "Button"}
BTN_6 = {"auto_id": "num6Button", "control_type": "Button"}
BTN_7 = {"auto_id": "num7Button", "control_type": "Button"}
BTN_8 = {"auto_id": "num8Button", "control_type": "Button"}
BTN_9 = {"auto_id": "num9Button", "control_type": "Button"}

# ── Operator buttons ───────────────────────────────────────────────────────────
BTN_ADD      = {"auto_id": "plusButton",            "control_type": "Button"}
BTN_SUBTRACT = {"auto_id": "minusButton",           "control_type": "Button"}
BTN_MULTIPLY = {"auto_id": "multiplyButton",        "control_type": "Button"}
BTN_DIVIDE   = {"auto_id": "divideButton",          "control_type": "Button"}
BTN_EQUALS   = {"auto_id": "equalButton",           "control_type": "Button"}
BTN_CLEAR    = {"auto_id": "clearButton",           "control_type": "Button"}
BTN_CE       = {"auto_id": "clearEntryButton",      "control_type": "Button"}
BTN_DECIMAL  = {"auto_id": "decimalSeparatorButton","control_type": "Button"}

# ── Keyboard shortcut map ──────────────────────────────────────────────────────
# Interview Tip: always provide a keyboard fallback — it is faster than
# clicking buttons and mirrors how real users interact with a desktop app.
KEYBOARD_MAP: dict[str, str] = {
    "0": "0",  "1": "1",  "2": "2",  "3": "3",  "4": "4",
    "5": "5",  "6": "6",  "7": "7",  "8": "8",  "9": "9",
    ".": ".",
    "+": "{+}",
    "-": "-",
    "*": "{*}",
    "/": "/",
    "=": "{ENTER}",
    "C": "{ESC}",   # Escape clears the current entry
}
