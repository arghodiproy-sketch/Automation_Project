"""
config/mobile_config.py — Appium / Android settings.

Interview Tip:
    Appium Desired Capabilities (now called Options) tell Appium:
      • WHICH device to target    (deviceName, platformName)
      • WHICH app to open         (appPackage, appActivity)
      • HOW to automate it        (automationName)

    noReset=True keeps app data between sessions — much faster for
    repeated test runs but may introduce test-state coupling.
    Use noReset=False when tests must start from a clean slate.
"""

APPIUM_SERVER_URL = "http://127.0.0.1:4723/wd/hub"

ANDROID_APP_PACKAGE  = "com.android.calculator2"
ANDROID_APP_ACTIVITY = "com.android.calculator2.Calculator"

# These keys map directly to UiAutomator2Options attributes.
ANDROID_OPTIONS: dict = {
    "platformName":       "Android",
    "automationName":     "UiAutomator2",
    "deviceName":         "Android Emulator",
    "appPackage":         ANDROID_APP_PACKAGE,
    "appActivity":        ANDROID_APP_ACTIVITY,
    "noReset":            True,
    "newCommandTimeout":  60,
}
