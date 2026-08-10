"""
config/desktop_config.py — Windows desktop automation settings.

Interview Tip:
    pywinauto supports two backends:
      'uia'   — UI Automation (modern apps, UWP, WPF)  ← preferred
      'win32' — older Win32 / MFC apps
    Always choose 'uia' for the Windows 10/11 Calculator (it is a UWP app).
"""

CALCULATOR_APP          = "calc.exe"
CALCULATOR_WINDOW_TITLE = "Calculator"
CALCULATOR_WINDOW_CLASS = "ApplicationFrameWindow"
BACKEND                 = "uia"
