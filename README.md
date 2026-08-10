# Automation_Desktop_Mobile_Web

A production-style Python + pytest automation framework covering **three platforms**:

| Platform | App Under Test | Technology |
|----------|---------------|------------|
| Desktop  | Windows Calculator | pywinauto (UIA backend) |
| Mobile   | Android Calculator | Appium + UiAutomator2 |
| Web      | Google Search | Selenium 4 + webdriver-manager |

---

## Project Structure

```
Automation_Desktop_Mobile_Web/
│
├── config/                     ← All configuration (no magic strings in tests)
│   ├── settings.py             ← Global constants & timeouts
│   ├── desktop_config.py       ← Windows app settings
│   ├── mobile_config.py        ← Appium / Android capabilities
│   └── web_config.py           ← Browser / Selenium settings
│
├── core/                       ← Framework foundation (abstract base classes)
│   ├── base_driver.py          ← ABC enforcing start() / quit() contract
│   ├── base_page.py            ← ABC that every Page Object inherits from
│   └── logger.py               ← Centralised logging (never use print())
│
├── drivers/                    ← Platform-specific driver setup
│   ├── desktop_driver.py       ← Launches calc.exe via pywinauto
│   ├── mobile_driver.py        ← Opens Appium session for Android
│   └── web_driver.py           ← Chrome / Firefox driver factory
│
├── locators/                   ← All element locators — ONE place to update
│   ├── desktop/calculator_locators.py
│   ├── mobile/calculator_locators.py
│   └── web/google_locators.py
│
├── pages/                      ← Page Object Model (POM) layer
│   ├── desktop/calculator_page.py
│   ├── mobile/calculator_page.py
│   ├── web/google_home_page.py
│   └── web/google_results_page.py
│
├── tests/                      ← Test suites (one folder per platform)
│   ├── conftest.py             ← Shared fixtures (desktop_window, mobile_driver, web_driver)
│   ├── desktop/test_desktop_calculator.py
│   ├── mobile/test_mobile_calculator.py
│   └── web/test_google_search.py
│
├── utils/
│   └── helpers.py              ← Pure utility functions (retry, normalize_number)
│
├── pytest.ini                  ← Test runner configuration & marker registration
└── requirements.txt
```

---

## Installation

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows

# 2. Install all dependencies
pip install -r requirements.txt
```

---

## Running Tests

### Desktop (Windows Calculator)
```bash
# All desktop tests
pytest tests/desktop/ -m desktop

# Single test
pytest tests/desktop/test_desktop_calculator.py::test_addition
```

### Mobile (Android — Appium)
```bash
# Prerequisites:
#   1. appium                           (start Appium server)
#   2. emulator -avd <AVD_NAME>         (boot emulator)
#   3. adb devices                      (verify device visible)

pytest tests/mobile/ -m mobile

# Custom Appium URL:
pytest tests/mobile/ --appium-url=http://127.0.0.1:4723
```

### Web (Google Search — Selenium)
```bash
# Chrome (default)
pytest tests/web/ -m web

# Firefox
pytest tests/web/ -m web --browser=firefox

# Headless (CI mode — no browser window)
pytest tests/web/ -m web --headless
```

### Run all platforms
```bash
pytest -v
```

### Skip a platform
```bash
pytest -m "not mobile"           # skip mobile
pytest -m "desktop or web"       # run only desktop + web
```

### Generate an HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## Key Design Patterns (Interview Reference)

### 1. Page Object Model (POM)
Every screen has ONE class. Tests call methods, never use locators directly.
```python
# Without POM (bad — locators duplicated in every test):
driver.find_element(By.NAME, "q").send_keys("Python")

# With POM (good — locator lives in GoogleHomePage):
google.enter_search_query("Python")
```

### 2. Abstract Base Classes (ABC)
`BaseDriver` and `BasePage` enforce that every subclass implements required methods.
```python
class BaseDriver(ABC):
    @abstractmethod
    def start(self): ...

    @abstractmethod
    def quit(self): ...
```

### 3. Fixture Scopes
```python
@pytest.fixture(scope="function")   # new driver per test (safest)
@pytest.fixture(scope="module")     # shared within one file (faster)
@pytest.fixture(scope="session")    # shared for entire run (use with care)
```

### 4. Parameterized Tests
```python
@pytest.mark.parametrize("expression, expected", [
    ("1+1=", "2"),
    ("12+7=", "19"),
])
def test_addition(desktop_window, expression, expected):
    ...
```

### 5. Explicit Waits (Selenium)
```python
# NEVER: time.sleep(3)
# ALWAYS: WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "q"))
)
```

### 6. Yield Fixtures (setup + teardown)
```python
@pytest.fixture
def web_driver():
    drv = WebDriver()
    driver = drv.start()   # SETUP
    yield driver           # test runs here
    drv.quit()             # TEARDOWN — always runs
```

---

## Common Interview Questions

| Question | Answer |
|----------|--------|
| What is POM? | Design pattern where each screen = one class owning its locators and actions |
| implicit vs explicit wait? | Implicit: global timeout on every find; Explicit: per-element wait with conditions |
| Why yield in fixtures? | Guarantees teardown runs even if the test raises an exception |
| What is conftest.py? | Auto-loaded pytest plugin file; fixtures defined here are available without importing |
| How do you run only smoke tests? | `pytest -m smoke` |
| Why separate locators from pages? | Single place to update when UI changes; pages stay clean |
| ABC vs Interface? | Python has no `interface` keyword; ABCs (abstract methods) serve the same purpose |
