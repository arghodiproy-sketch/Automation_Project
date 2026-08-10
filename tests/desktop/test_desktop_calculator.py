"""
tests/desktop/test_desktop_calculator.py — Windows Calculator tests.

Interview Tip — Test design fundamentals:

  1. AAA Pattern (Arrange, Act, Assert):
       Arrange  → set up the page object and any preconditions
       Act      → call the action under test
       Assert   → verify the expected outcome

  2. One assertion per test (ideally):
       Each test has ONE reason to fail — easier to diagnose.

  3. Descriptive test names: test_<scenario>_<expected_outcome>
       Bad:   test_1(), test_add()
       Good:  test_addition_of_two_positive_numbers_returns_correct_sum()

  4. @pytest.mark.parametrize — run same logic with multiple data sets:
       Avoids copy-paste; each data row becomes a separate test case in the report.

  5. Fixture injection:
       desktop_window is defined in tests/conftest.py — pytest finds it
       automatically from the function parameter name.
"""

import pytest

from pages.desktop.calculator_page import DesktopCalculatorPage


@pytest.mark.desktop
def test_addition(desktop_window):
    """Addition expression evaluates to the correct sum."""
    page = DesktopCalculatorPage(desktop_window)
    page.clear()
    result = page.calculate("1+1=")
    assert result == "2", f"[FAIL] 1+1=: expected '2', got '{result}'"
