"""
tests/mobile/test_mobile_calculator.py — Android Calculator tests.

Interview Tip — Mobile-specific concepts:

  Prerequisites to run these tests:
    1. Start Appium server:        appium
    2. Boot Android emulator:      emulator -avd <AVD_NAME>
                                   (or connect a physical device via ADB)
    3. Verify device visible:      adb devices
    4. Run tests:                  pytest tests/mobile/ -m mobile

  Skip mobile tests in a desktop-only run:
    pytest -m "not mobile"

  @pytest.mark.mobile:
    Registered in pytest.ini — prevents PytestUnknownMarkWarning.
    Allows selective execution: pytest -m mobile

  Why results are stripped of spaces:
    Android's AOSP Calculator sometimes formats numbers with thin spaces
    for thousand separators (e.g. "1 000" instead of "1000").
    result.replace(" ", "") normalises this before asserting.
"""

import pytest

from pages.mobile.calculator_page import MobileCalculatorPage


@pytest.mark.mobile
def test_addition(mobile_driver):
    """Addition on the Android calculator."""
    page = MobileCalculatorPage(mobile_driver)
    page.clear()
    result = page.calculate("1+1=")
    assert result.replace(" ", "") == "2", (
        f"[FAIL] 1+1=: expected '2', got '{result}'"
    )
