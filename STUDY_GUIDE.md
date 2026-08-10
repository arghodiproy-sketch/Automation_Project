# Complete Study Guide — Python, pytest & OOP for SDET Interviews
### Based on your `Automation_Desktop_Mobile_Web` framework

---

## Table of Contents
1. [Python Fundamentals](#1-python-fundamentals)
2. [OOP Concepts](#2-oop-concepts)
3. [Design Patterns Used in This Framework](#3-design-patterns)
4. [pytest Deep Dive](#4-pytest-deep-dive)
5. [Selenium & WebDriver Concepts](#5-selenium--webdriver-concepts)
6. [Appium & Mobile Concepts](#6-appium--mobile-concepts)
7. [Desktop Automation (pywinauto)](#7-desktop-automation)
8. [Framework Architecture Walkthrough](#8-framework-architecture)
9. [Top 50 Interview Q&A](#9-top-50-interview-qa)

---

## 1. Python Fundamentals

### 1.1 Modules and Imports
```python
# Every .py file is a module. __init__.py makes a folder a "package".
from pages.web.google_home_page import GoogleHomePage
#    ^package  ^sub-package        ^module            ^class
```
- `from x import y` — imports a specific name from module x
- `import x` — imports the whole module; you use `x.something`
- `__init__.py` — empty or with code; tells Python "this folder is a package"

**In this framework** — every `__init__.py` (e.g. `pages/__init__.py`) is empty.
Its only job is to allow `from pages.web.google_home_page import GoogleHomePage`.

---

### 1.2 Type Hints
```python
# config/settings.py
DEFAULT_WAIT_TIMEOUT: int = 20

# utils/helpers.py
def retry(func: Callable[[], T], attempts: int = 3, delay: float = 1.0) -> T:
```
- Type hints are **optional** — Python doesn't enforce them at runtime
- They serve as documentation and enable IDE auto-complete and type checkers (mypy)
- `Callable[[], T]` means "a function that takes no arguments and returns T"
- `TypeVar("T")` creates a generic placeholder — whatever type `func` returns, `retry` returns the same type

---

### 1.3 Default Arguments
```python
# drivers/web_driver.py
def __init__(self, browser: str = BROWSER, headless: bool = HEADLESS):
```
- If the caller doesn't pass `browser`, it defaults to the value of `BROWSER` from config
- Default values are evaluated **once** at function definition time (important for mutable defaults — never use `def f(x=[])`)

---

### 1.4 `*args` Unpacking
```python
# pages/web/google_results_page.py
elements = self.driver.find_elements(*RESULT_LINKS)
#                                    ^ unpacks the tuple (By.CSS_SELECTOR, "div#search a h3")
#                                      into two positional arguments
```
`RESULT_LINKS = (By.CSS_SELECTOR, "div#search a h3")`

`find_elements(*RESULT_LINKS)` is identical to `find_elements(By.CSS_SELECTOR, "div#search a h3")`

The `*` operator **unpacks** a tuple/list into separate positional arguments.

---

### 1.5 f-strings
```python
log.info("Starting %s (headless=%s)", self.browser, self.headless)  # % style
log.info("Opening: %s", self.URL)                                    # % style

raise ValueError(f"Unsupported browser '{self.browser}'. Choose 'chrome' or 'firefox'.")
# f"..." evaluates expressions inside {} at runtime
```
Both styles are in the framework. Use f-strings for clarity in most code; use `%` style with the `logging` module (it delays string formatting until the log line is actually emitted — a performance benefit).

---

### 1.6 List Comprehensions
```python
# pages/web/google_results_page.py
titles = [el.text for el in elements if el.text]
# equivalent to:
titles = []
for el in elements:
    if el.text:
        titles.append(el.text)
```
Pattern: `[expression for item in iterable if condition]`

---

### 1.7 `@property` Decorator
```python
# pages/web/google_results_page.py
@property
def title(self) -> str:
    return self.driver.title

@property
def current_url(self) -> str:
    return self.driver.current_url
```
- Accessed like an attribute: `results.title` — NO parentheses
- Hides implementation: caller doesn't know or care that it fetches from `driver.title`
- Read-only by default; add `@title.setter` to allow `results.title = "x"`

---

### 1.8 `try / except / finally`
```python
# drivers/web_driver.py
def quit(self):
    if self.driver:
        try:
            self.driver.quit()
            log.info("Browser closed.")
        except Exception as exc:
            log.warning("Error closing browser: %s", exc)
        finally:
            self.driver = None   # ALWAYS runs — even if quit() raised an error
```
- `try` — the risky block
- `except Exception as exc` — catches any exception; `exc` holds the error object
- `finally` — always executes; perfect for cleanup (setting driver to None, closing files)

---

### 1.9 `with` Statement (Context Manager)
```python
# core/logger.py — used inside urllib
with urlopen(req, timeout=5) as resp:
    if resp.status != 200:
        ...
```
- Automatically calls `__exit__` (cleanup) when the block ends, even on error
- Equivalent to try/finally but cleaner
- You can write your own by implementing `__enter__` and `__exit__`

---

### 1.10 `os` Module
```python
# config/settings.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```
- `__file__` — the path of the current .py file
- `os.path.abspath()` — converts to an absolute path
- `os.path.dirname()` — gets the parent directory
- Two `dirname` calls go up two levels: `config/` → `Automation_Desktop_Mobile_Web/`

---

### 1.11 Lambda Functions
```python
# utils/helpers.py — usage example
title = retry(lambda: results_page.get_first_result_title(), attempts=3)
```
- `lambda: expression` — an anonymous one-line function with no arguments
- Used when you need to pass a function as an argument without defining a full `def`

---

## 2. OOP Concepts

### 2.1 Class Definition and `__init__`
```python
class WebDriver(BaseDriver):           # WebDriver inherits from BaseDriver
    def __init__(self, browser: str = BROWSER, headless: bool = HEADLESS):
        self.browser  = browser.lower()   # instance attribute
        self.headless = headless
        self.driver   = None
```
- `class Name(Parent):` — defines a class inheriting from Parent
- `__init__` — the constructor, called when you do `WebDriver()`
- `self` — refers to the specific instance being created; like `this` in Java/C#
- Instance attributes (`self.browser`) belong to each object individually

---

### 2.2 Inheritance
```python
# core/base_driver.py
class BaseDriver(ABC):          # parent / superclass
    ...

# drivers/web_driver.py
class WebDriver(BaseDriver):    # child / subclass
    ...

# drivers/mobile_driver.py
class MobileDriver(BaseDriver): # another child
    ...
```

**Inheritance hierarchy in this framework:**
```
BaseDriver (ABC)
├── WebDriver        → Selenium Chrome/Firefox
├── MobileDriver     → Appium Android
└── DesktopDriver    → pywinauto Windows Calculator

BasePage (ABC)
├── GoogleHomePage
├── GoogleResultsPage
├── DesktopCalculatorPage
└── MobileCalculatorPage
```

- Child class **inherits** all methods and attributes of the parent
- Child can **override** parent methods (provide its own implementation)
- Child can **call** the parent method with `super()`

---

### 2.3 Abstract Classes and Abstract Methods
```python
# core/base_driver.py
from abc import ABC, abstractmethod

class BaseDriver(ABC):           # ABC = Abstract Base Class
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def quit(self):
        ...
```
**Rules:**
- A class with `ABC` as parent cannot be instantiated directly: `BaseDriver()` raises `TypeError`
- Any subclass that does NOT implement all `@abstractmethod` methods also cannot be instantiated
- This **enforces a contract** — every driver MUST have `start()` and `quit()`

**Why it matters in interviews:**
> "ABC is Python's way of defining an interface. It's the foundation of the Liskov Substitution Principle — any concrete driver can replace a BaseDriver reference."

---

### 2.4 `super()`
```python
# pages/web/google_home_page.py
class GoogleHomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)   # calls BasePage.__init__(driver)
        self._wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)
```
- `super()` refers to the parent class
- `super().__init__(driver)` runs the parent's constructor first — stores `self.driver = driver`
- Then the child adds its own setup (`self._wait`)
- **Always call `super().__init__()` in a child's `__init__`** unless you deliberately skip parent setup

---

### 2.5 Encapsulation
```python
# pages/web/google_home_page.py
self._wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)  # "protected" by convention
```
In Python:
- `name` — public (accessible everywhere)
- `_name` — protected by **convention** (accessible but "please don't use externally")
- `__name` — private (name-mangled; harder to access from outside)

No true access modifiers like Java's `private`/`protected`. Convention is enforced by discipline.

---

### 2.6 Fluent Interface (Method Chaining)
```python
# pages/web/google_home_page.py
def enter_search_query(self, query: str) -> "GoogleHomePage":
    ...
    return self                     # ← returns self

def submit_search(self) -> "GoogleHomePage":
    ...
    return self

def search(self, query: str) -> "GoogleHomePage":
    return self.enter_search_query(query).submit_search()  # chaining
```
- Methods return `self` so calls can be chained
- `"GoogleHomePage"` in quotes is a **forward reference** (string annotation) — needed because the class isn't fully defined yet when Python reads the return type

---

### 2.7 Dependency Injection
```python
# core/base_page.py
class BasePage(ABC):
    def __init__(self, driver):
        self.driver = driver        # driver is INJECTED — not created here
```
The page does not create its own driver. The driver is created externally (in a fixture) and **passed in** (injected). This means:
- Pages are reusable with any driver implementation
- Pages can be tested with a mock driver
- The fixture controls the lifecycle (start/quit), not the page

---

### 2.8 Polymorphism
```python
# All three drivers have the same interface:
drv = WebDriver()      # or MobileDriver() or DesktopDriver()
driver = drv.start()   # same method name, different behaviour
drv.quit()             # same method name, different behaviour
```
Polymorphism = same interface, different implementations.

In `conftest.py`, all three fixtures follow the same pattern:
```python
drv = WebDriver(...)
driver = drv.start()
yield driver
drv.quit()
```
You could swap `WebDriver` with `MobileDriver` and the pattern works identically.

---

### 2.9 `@staticmethod` vs `@classmethod` vs instance method
| Type | First param | Has `self`? | Accesses instance state? |
|------|------------|-------------|--------------------------|
| Instance method | `self` | Yes | Yes |
| `@classmethod` | `cls` | No | Class-level only |
| `@staticmethod` | nothing | No | No |

In this framework all methods are instance methods. Example of where static/class methods fit:
```python
# A factory classmethod could be:
@classmethod
def from_config(cls):
    return cls(browser=BROWSER, headless=HEADLESS)
```

---

## 3. Design Patterns

### 3.1 Page Object Model (POM)
**The #1 automation design pattern.**

```
Without POM:                        With POM:
─────────────────────────           ─────────────────────────
test_1.py                           test_1.py
  driver.find_element(By.NAME,"q")    home = GoogleHomePage(driver)
  .send_keys("Python")                home.search("Python")
  .send_keys(Keys.RETURN)
                                    google_home_page.py
test_2.py                             def search(self, query):
  driver.find_element(By.NAME,"q")      box = self._wait.until(...)
  .send_keys("Selenium")               box.send_keys(query)
  .send_keys(Keys.RETURN)              box.send_keys(Keys.RETURN)
```

Change the locator → update `google_locators.py` → all tests fixed automatically.

**3 Rules to recite in interviews:**
1. Page Objects own locators and actions — tests own assertions
2. One class per screen/page
3. Methods return `self` (for chaining) or data (for assertions) — never both

---

### 3.2 Factory Method Pattern
```python
# drivers/web_driver.py
def start(self):
    if self.browser == "chrome":
        self.driver = self._build_chrome()    # factory
    elif self.browser == "firefox":
        self.driver = self._build_firefox()   # factory
    else:
        raise ValueError(...)
```
`start()` decides which concrete object to create based on a parameter. The caller doesn't know or care whether it's Chrome or Firefox — it just gets a `WebDriver` object back.

---

### 3.3 Template Method Pattern
```python
# BaseDriver defines the STEPS (start, quit)
# Subclasses fill in HOW each step works
class BaseDriver(ABC):
    @abstractmethod
    def start(self): ...   # step 1
    @abstractmethod
    def quit(self): ...    # step 2
```
The abstract class defines the skeleton; subclasses provide the flesh.

---

### 3.4 Singleton-like Logger
```python
# core/logger.py
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:       # guard: only configure once
        ...
    return logger
```
`logging.getLogger(name)` returns the **same** logger object every time for the same `name`. The guard `if not logger.handlers` prevents adding duplicate handlers if a module is imported multiple times.

---

## 4. pytest Deep Dive

### 4.1 Test Discovery
pytest automatically finds tests by:
- Files matching `test_*.py` or `*_test.py`
- Functions/methods starting with `test_`
- Classes starting with `Test` (no `__init__` required)

Configured in `pytest.ini`:
```ini
pythonpath = .          # adds project root to sys.path so imports work
addopts = -v --tb=short # applied to every run automatically
```

---

### 4.2 Fixtures — the Core of pytest
```python
# tests/conftest.py
@pytest.fixture(scope="function")
def web_driver(request):
    browser  = request.config.getoption("--browser")   # CLI option
    headless = request.config.getoption("--headless")
    drv = WebDriver(browser=browser, headless=headless)
    driver = drv.start()        # SETUP (everything before yield)
    yield driver                # VALUE given to the test
    drv.quit()                  # TEARDOWN (everything after yield)
```

**How a test receives it:**
```python
def test_google_homepage_loads_successfully(web_driver):   # name must match fixture
    page = GoogleHomePage(web_driver)
```
pytest sees `web_driver` in the function signature and automatically calls the fixture.

---

### 4.3 Fixture Scopes
| Scope | New instance created | Use when |
|-------|---------------------|----------|
| `function` (default) | Per test | Tests modify state (form inputs, data) |
| `class` | Per test class | Tests in a class share setup |
| `module` | Per .py file | Read-only tests; save browser launch time |
| `session` | Once for the whole run | Very expensive setup; tests don't pollute each other |

**This framework uses `function` scope** — a fresh browser/app/emulator for each test. Safest option; prevents test pollution.

---

### 4.4 `conftest.py` — Shared Fixtures
```
tests/
  conftest.py          ← fixtures available to ALL tests below
  web/
    conftest.py        ← fixtures available only to web/ tests
  mobile/
    conftest.py        ← fixtures available only to mobile/ tests
```
pytest automatically discovers `conftest.py`. No imports needed in test files.

---

### 4.5 Markers
```python
# pytest.ini
markers =
    web:     web browser tests (Selenium)
    mobile:  Android tests (Appium)
    desktop: Windows tests (pywinauto)

# In test file
@pytest.mark.web
def test_google_homepage_loads_successfully(web_driver):
    ...
```
**Running specific markers:**
```bash
pytest -m web          # only web tests
pytest -m "not mobile" # everything except mobile
pytest -m "web or desktop"
```

---

### 4.6 Parametrize
```python
@pytest.mark.parametrize("query", [
    "Selenium WebDriver tutorial",
    "Appium mobile testing guide",
    "pytest fixtures explained",
])
def test_search_query_keyword_appears_in_page_title(web_driver, query):
    ...
```
- Runs the same test 3 times with different `query` values
- Each appears as a separate test in the report
- Multiple parameters: `@pytest.mark.parametrize("a, b, expected", [(1,1,"2"), (2,3,"5")])`

---

### 4.7 CLI Options (addoption)
```python
# tests/conftest.py
def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", ...)
    parser.addoption("--headless", action="store_true", default=False, ...)
    parser.addoption("--appium-url", default="http://127.0.0.1:4723/wd/hub", ...)
```
**Usage:**
```bash
pytest tests/web/ --browser=firefox --headless
pytest tests/mobile/ --appium-url=http://192.168.1.10:4723/wd/hub
```
Fixtures read these via `request.config.getoption("--browser")`.

---

### 4.8 `pytest.ini` explained line by line
```ini
[pytest]
pythonpath = .
# Adds '.' (project root) to sys.path so Python finds 'pages', 'config', etc.

addopts = -v --tb=short
# -v          → verbose: prints each test name
# --tb=short  → short traceback on failure (not the full stack)

markers =
    web: ...
    mobile: ...
    desktop: ...
# Registers custom markers — prevents PytestUnknownMarkWarning
```

---

### 4.9 Assertion Messages
```python
assert "Google" in web_driver.title, (
    f"Unexpected page title: '{web_driver.title}'"
)
```
Always provide a message — it's printed when the assertion fails, making debugging instant.

---

## 5. Selenium & WebDriver Concepts

### 5.1 WebDriver Architecture
```
Test Script (Python)
      │
      ▼
Selenium WebDriver (Python bindings)
      │  HTTP (WebDriver Wire Protocol / W3C WebDriver)
      ▼
ChromeDriver / GeckoDriver (bridge)
      │
      ▼
Chrome / Firefox Browser
```

### 5.2 Locator Strategies — Priority Order
```python
# locators/web/google_locators.py
SEARCH_INPUT = (By.NAME, "q")                          # 1. ID/NAME — fastest
RESULTS_STATS = (By.ID, "result-stats")                # 1. ID — most reliable
RESULT_LINKS  = (By.CSS_SELECTOR, "div#search a h3")  # 2. CSS — preferred
FIRST_RESULT  = (By.CSS_SELECTOR, "div#search a h3:first-of-type")
```

| Strategy | Speed | Reliability | When to use |
|----------|-------|-------------|-------------|
| `By.ID` | Fastest | Highest | When elements have unique IDs |
| `By.NAME` | Fast | High | Form inputs |
| `By.CSS_SELECTOR` | Fast | High | Most elements — preferred |
| `By.XPATH` | Slower | High | Text matching, complex paths |
| `By.CLASS_NAME` | Medium | Low | Classes change often |
| `By.LINK_TEXT` | Medium | Medium | Exact link text |

---

### 5.3 Explicit vs Implicit Waits
```python
# IMPLICIT (global, set once)
self.driver.implicitly_wait(10)  # wait up to 10s for every find_element
# Problem: interacts badly with explicit waits

# EXPLICIT (per element, preferred)
wait = WebDriverWait(driver, 20)
element = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
```

**Most-used Expected Conditions:**
```python
EC.presence_of_element_located(locator)    # in DOM (may be invisible)
EC.visibility_of_element_located(locator)  # visible on screen
EC.element_to_be_clickable(locator)        # visible + enabled
EC.text_to_be_present_in_element(locator, "text")
EC.title_contains("Google")
EC.url_contains("search")
EC.staleness_of(element)                   # element removed from DOM
EC.invisibility_of_element_located(locator)
```

**Rule: NEVER mix implicit and explicit waits.** Set `implicitly_wait(0)` in production and use only explicit waits.

---

### 5.4 Keys & Actions
```python
from selenium.webdriver.common.keys import Keys
search_box.send_keys(Keys.RETURN)    # press Enter
search_box.send_keys(Keys.TAB)       # Tab
search_box.send_keys(Keys.CONTROL, "a")  # Ctrl+A
```

---

### 5.5 WebDriver Manager
```python
# drivers/web_driver.py
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(ChromeDriverManager().install())
```
- Automatically downloads the correct ChromeDriver for your installed Chrome version
- Caches in `~/.wdm/` — only re-downloads when Chrome updates
- Without it: manual binary management; common CI breakage

---

### 5.6 Chrome Options
```python
options.add_argument("--headless=new")               # no browser window (CI)
options.add_argument("--disable-gpu")                # Windows headless fix
options.add_argument("--no-sandbox")                 # required in Docker
options.add_argument("--disable-dev-shm-usage")      # Docker shared memory fix
options.add_argument("--disable-blink-features=AutomationControlled")  # hides bot detection
```

---

## 6. Appium & Mobile Concepts

### 6.1 Appium Architecture
```
Test Script (Python + Appium Client)
      │
      ▼
Appium Server (Node.js HTTP server on port 4723)
      │
      ▼
UiAutomator2 (Android automation engine installed on device)
      │
      ▼
Android App (Calculator)
```

### 6.2 Desired Capabilities / Options
```python
# config/mobile_config.py
ANDROID_OPTIONS = {
    "platformName":   "Android",     # which OS
    "automationName": "UiAutomator2",# which engine (UiAutomator2 for Android)
    "deviceName":     "Android Emulator",
    "appPackage":     "com.android.calculator2",    # app's package name
    "appActivity":    "com.android.calculator2.Calculator",  # launch activity
    "noReset":        True,          # keep app data between sessions
    "newCommandTimeout": 60,         # Appium session timeout in seconds
}
```

**Find package/activity of any app:**
```bash
adb shell dumpsys window | findstr "mCurrentFocus"
```

### 6.3 Appium 1.x vs 2.x URL
```python
# Appium 1.x — requires /wd/hub base path
APPIUM_SERVER_URL = "http://127.0.0.1:4723/wd/hub"

# Appium 2.x — no base path needed
APPIUM_SERVER_URL = "http://127.0.0.1:4723"
```

### 6.4 noReset / fullReset / fastReset
| Option | Effect | Speed |
|--------|--------|-------|
| `noReset=True` | Keep app data, don't reinstall | Fastest |
| `noReset=False` (default) | Clear app data before session | Medium |
| `fullReset=True` | Uninstall + reinstall app | Slowest, cleanest |

---

## 7. Desktop Automation

### 7.1 pywinauto Basics
```python
# drivers/desktop_driver.py (WinAppDriver alternative using pywinauto)
from pywinauto import Application
app = Application(backend="uia").start("calc.exe")
window = app.window(title_re="Calculator")
```
- `backend="uia"` — uses Microsoft UI Automation (recommended for modern apps)
- `backend="win32"` — uses older Win32 API

### 7.2 Keyboard Map
```python
# locators/desktop/calculator_locators.py
KEYBOARD_MAP = {
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "=": "{ENTER}",   # pywinauto key code for Enter
}
```
`type_keys("{ENTER}")` presses Enter. `{VK_DELETE}` presses Delete.

---

## 8. Framework Architecture

### 8.1 Full File-to-Concept Map
```
config/
  settings.py        → Global constants (timeouts, BASE_DIR)
  web_config.py      → Browser settings (URL, browser, headless)
  mobile_config.py   → Appium server URL + Android capabilities
  desktop_config.py  → pywinauto / WinAppDriver settings

core/
  base_driver.py     → Abstract Base Class; enforces start()/quit() contract
  base_page.py       → Abstract Base Class; Dependency Injection of driver
  logger.py          → Singleton-like logger; avoids print() in tests

drivers/
  web_driver.py      → Factory: creates Chrome or Firefox WebDriver
  mobile_driver.py   → Creates Appium session; pre-flight Appium health check
  desktop_driver.py  → Creates pywinauto Application + window handle

locators/
  web/google_locators.py          → (By.STRATEGY, "value") tuples
  mobile/calculator_locators.py   → Appium resource-id locators
  desktop/calculator_locators.py  → KEYBOARD_MAP + RESULT_DISPLAY

pages/
  web/google_home_page.py         → open(), search(), enter_search_query()
  web/google_results_page.py      → wait_for_results(), get_result_titles()
  mobile/calculator_page.py       → clear(), press(), calculate(), get_result()
  desktop/calculator_page.py      → clear(), press(), calculate(), get_result()

tests/
  conftest.py                     → Fixtures: web_driver, mobile_driver, desktop_window
  web/test_google_search.py       → @pytest.mark.web tests
  mobile/test_mobile_calculator.py→ @pytest.mark.mobile tests
  desktop/test_desktop_calculator.py → @pytest.mark.desktop tests

utils/
  helpers.py          → retry(), normalize_number() — pure utility functions
```

---

### 8.2 Data Flow for a Web Test
```
pytest collects test_google_homepage_loads_successfully(web_driver)
         │
         ▼
conftest.py: web_driver fixture
  → WebDriver(browser="chrome").start()
      → ChromeDriverManager downloads chromedriver
      → driver.implicitly_wait(10)
      → returns selenium driver
         │
         ▼
test body receives: driver
  → GoogleHomePage(driver).open()
      → driver.get("https://www.google.com")
  → assert "Google" in driver.title
         │
         ▼
fixture teardown: drv.quit()
  → driver.quit() → browser closes
```

---

### 8.3 Why This Structure is Interview Gold

| Concept | Where in framework | Interview answer |
|---------|--------------------|-----------------|
| ABC / Interface | `core/base_driver.py` | "I enforce a contract with ABC so every driver must implement start() and quit()" |
| Inheritance | `WebDriver(BaseDriver)` | "WebDriver inherits BaseDriver's contract and fills in the implementation" |
| POM | `pages/` folder | "Each page class owns its locators and actions; tests only call high-level methods" |
| Dependency Injection | `BasePage.__init__(driver)` | "Driver is injected so pages work with any driver type and can be unit-tested with mocks" |
| Factory Pattern | `WebDriver._build_chrome()` | "The start() method is a factory — it returns Chrome or Firefox based on config" |
| Fixtures | `conftest.py` | "pytest fixtures handle setup/teardown with yield; scope controls how often they run" |
| Explicit Waits | `WebDriverWait + EC` | "I never use sleep(); WebDriverWait polls until a condition is met or timeout is reached" |
| Encapsulation | `self._wait` (underscore) | "Protected by convention; internal detail not meant for external use" |
| Fluent Interface | `return self` in page methods | "Methods return self so actions can be chained: page.open().search('Python')" |

---

## 9. Top 50 Interview Q&A

### Python

**Q1: What is the difference between `==` and `is`?**
- `==` checks value equality: `[1,2] == [1,2]` → True
- `is` checks identity (same object in memory): `[1,2] is [1,2]` → False

**Q2: What are Python's mutable vs immutable types?**
- Immutable: `int`, `float`, `str`, `tuple`, `bool`, `frozenset`
- Mutable: `list`, `dict`, `set`, custom objects

**Q3: What is a decorator?**
A function that wraps another function to add behaviour.
`@pytest.mark.web` and `@abstractmethod` are both decorators.

**Q4: What is `__init__` vs `__new__`?**
- `__new__` creates the object (rarely overridden)
- `__init__` initializes the already-created object (what you always override)

**Q5: What is a generator?**
A function with `yield` that produces values lazily — does not store all in memory.

**Q6: Difference between `*args` and `**kwargs`?**
- `*args` — positional arguments as a tuple
- `**kwargs` — keyword arguments as a dict
- `find_elements(*RESULT_LINKS)` unpacks a tuple into positional args

**Q7: What is a list comprehension vs generator expression?**
- `[x for x in y]` — list (all in memory)
- `(x for x in y)` — generator (lazy, memory-efficient)

**Q8: What is `None` in Python?**
Python's null value. `if self.driver:` is False when `self.driver is None`.

**Q9: What is the difference between `try/except/else/finally`?**
- `try` — risky code
- `except` — runs if an exception is raised
- `else` — runs if NO exception was raised
- `finally` — ALWAYS runs (cleanup)

**Q10: What is a module vs a package?**
- Module = single `.py` file
- Package = folder with `__init__.py`

---

### OOP

**Q11: What are the 4 pillars of OOP?**
1. **Encapsulation** — hiding internal data (`self._wait`)
2. **Inheritance** — `WebDriver(BaseDriver)`
3. **Polymorphism** — `drv.start()` works on any driver type
4. **Abstraction** — `BaseDriver` hides implementation details

**Q12: What is an abstract class?**
A class that cannot be instantiated; it defines a contract (interface) for subclasses. In Python, use `class X(ABC)` with `@abstractmethod`.

**Q13: Difference between abstract class and interface in Python?**
Python has no `interface` keyword. An ABC with only `@abstractmethod` methods serves as an interface. An ABC can also have concrete methods (partial implementation).

**Q14: What is Dependency Injection?**
Instead of a class creating its own dependencies, they are passed in from outside. `BasePage.__init__(self, driver)` — the driver is injected; pages don't create drivers.

**Q15: What is the Liskov Substitution Principle?**
A subclass should be usable wherever its parent is expected, without breaking the program.
`WebDriver`, `MobileDriver`, `DesktopDriver` are all substitutable for `BaseDriver`.

**Q16: What is method overriding?**
A child class provides its own implementation of a method defined in the parent.
`WebDriver.start()` overrides `BaseDriver.start()`.

**Q17: What is `super()` used for?**
To call the parent class's method from a child class.
`super().__init__(driver)` in `GoogleHomePage` runs `BasePage.__init__`.

**Q18: What is a `@property`?**
A method accessed like an attribute. Hides implementation; makes API cleaner.
`results.title` calls `self.driver.title` internally.

**Q19: What is the Factory Pattern?**
A method that creates and returns objects without exposing creation logic.
`WebDriver.start()` returns Chrome or Firefox based on `self.browser`.

**Q20: What is the Singleton Pattern?**
Ensures only one instance exists. `logging.getLogger(name)` returns the same logger for the same name.

---

### pytest

**Q21: What is a pytest fixture?**
A function decorated with `@pytest.fixture` that provides setup, data, or teardown for tests. Injected automatically by parameter name.

**Q22: What is the difference between setup/teardown in unittest vs pytest?**
- unittest: `setUp()`/`tearDown()` methods in a class
- pytest: `yield` fixtures — setup before yield, teardown after yield. More flexible, reusable across files.

**Q23: What are fixture scopes?**
`function` (default), `class`, `module`, `session` — controls how often the fixture is created/destroyed.

**Q24: What is `conftest.py`?**
A special pytest file for shared fixtures. Automatically discovered by pytest; no imports needed.

**Q25: How do you run only specific tests?**
```bash
pytest -m web              # by marker
pytest tests/web/          # by directory
pytest -k "homepage"       # by keyword in test name
pytest tests/web/test_google_search.py::test_google_homepage_loads_successfully  # exact test
```

**Q26: What is `@pytest.mark.parametrize`?**
Runs the same test multiple times with different inputs. Each input set is a separate test case in the report.

**Q27: How do you skip a test?**
```python
@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
```

**Q28: How do you expect a test to raise an exception?**
```python
with pytest.raises(ValueError):
    WebDriver(browser="ie").start()
```

**Q29: What is `--tb=short` in pytest.ini?**
Controls traceback format on failure. `short` shows a brief stack trace. Other options: `long`, `no`, `line`, `auto`.

**Q30: What is the `request` fixture?**
A built-in pytest fixture that gives access to the current test context.
`request.config.getoption("--browser")` reads a custom CLI option.

---

### Selenium

**Q31: What is the WebDriver protocol?**
HTTP-based W3C standard that test scripts use to send commands to browser drivers (ChromeDriver, GeckoDriver).

**Q32: What is the difference between `find_element` and `find_elements`?**
- `find_element` → returns one element; raises `NoSuchElementException` if not found
- `find_elements` → returns a list; returns empty list if none found

**Q33: What is an explicit wait? Why is it better than `time.sleep()`?**
`WebDriverWait` polls until a condition is met or timeout expires. Unlike `sleep()`, it doesn't wait unnecessarily when the element appears early — makes tests faster and more reliable.

**Q34: Name 5 ExpectedConditions.**
`element_to_be_clickable`, `presence_of_element_located`, `visibility_of_element_located`, `text_to_be_present_in_element`, `title_contains`

**Q35: What is the difference between `presence` and `visibility`?**
- `presence` — element exists in the DOM (may be hidden, off-screen, or `display:none`)
- `visibility` — element is in the DOM AND visible (not hidden, has size > 0)

**Q36: What is `driver.find_elements(*locator)` doing with `*`?**
The `*` unpacks the tuple `(By.CSS_SELECTOR, "div#search a h3")` into two separate positional arguments, matching `find_elements(by, value)`.

**Q37: How do you handle dropdowns in Selenium?**
```python
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "dropdown"))
select.select_by_visible_text("Option 1")
select.select_by_value("val1")
select.select_by_index(2)
```

**Q38: How do you switch to an iframe?**
```python
driver.switch_to.frame("frame_name")   # or element
driver.switch_to.default_content()     # back to main page
```

**Q39: How do you take a screenshot?**
```python
driver.save_screenshot("screenshot.png")
element.screenshot("element.png")
```

**Q40: What is `StaleElementReferenceException`?**
Raised when an element reference becomes outdated (e.g. the page reloaded). Fix: re-locate the element. Use `retry()` from `utils/helpers.py`.

---

### Framework & Design

**Q41: What is the Page Object Model?**
A design pattern where each UI screen/page has a corresponding class that encapsulates its locators and user actions. Tests call high-level methods, not raw `find_element` calls.

**Q42: Why do you separate locators from page objects?**
If a locator changes, update one file (`google_locators.py`) and all page objects and tests that use it are fixed automatically.

**Q43: Why use `logging` instead of `print()`?**
Log levels allow filtering. Logs can be written to files for CI artifacts. Each module shows its name. Format is consistent across the framework.

**Q44: Why is `noReset=True` faster for mobile tests?**
Appium doesn't need to clear app data or reinstall the APK between sessions. Useful when tests start from a known state (like pressing Clear).

**Q45: What is webdriver-manager?**
A Python library that automatically downloads and caches the correct ChromeDriver/GeckoDriver version for the installed browser. Eliminates manual binary management.

**Q46: What is the difference between `driver.quit()` and `driver.close()`?**
- `close()` — closes the current browser window/tab
- `quit()` — closes ALL windows and ends the WebDriver session (always use in teardown)

**Q47: How do you run tests in parallel?**
Use `pytest-xdist`: `pytest -n 4` runs tests on 4 workers. Fixtures must be thread-safe.

**Q48: What is headless mode?**
Running the browser without a visible UI. Essential in CI/CD environments (no display). Set via `--headless` CLI flag or `HEADLESS=True` in `web_config.py`.

**Q49: What is the AAA pattern?**
Arrange–Act–Assert. Every test should:
1. **Arrange** — set up the page object and preconditions
2. **Act** — call the action being tested
3. **Assert** — verify the expected outcome

**Q50: How would you add screenshot-on-failure to this framework?**
Add a fixture or hook in `conftest.py`:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("web_driver")
        if driver:
            driver.save_screenshot(f"screenshots/{item.name}.png")
```

---

## Quick Reference Cheat Sheet

### Run Commands
```bash
# Web tests
pytest tests/web/ -m web -v

# Desktop tests
pytest tests/desktop/ -m desktop -v

# Mobile tests (requires Appium server + emulator)
pytest tests/mobile/ -m mobile -v

# All tests
pytest -v

# With specific browser
pytest tests/web/ --browser=firefox --headless

# Generate HTML report (pytest-html installed)
pytest tests/web/ --html=report.html --self-contained-html
```

### Key Import Map
```python
from abc import ABC, abstractmethod            # Abstract classes
from selenium.webdriver.common.by import By    # Locator strategies
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from appium.options.android import UiAutomator2Options
import pytest                                  # Test framework
import logging                                 # Logging
import os                                      # File paths
```

### Locator Quick Reference
```python
(By.ID,           "element-id")
(By.NAME,         "q")
(By.CSS_SELECTOR, "div.class > span#id")
(By.XPATH,        "//div[@class='result']//h3")
(By.CLASS_NAME,   "result-title")
(By.LINK_TEXT,    "Click here")
(By.TAG_NAME,     "input")
```

---

*This guide covers every concept used in your framework. Re-read a section, then open the corresponding file and trace through the code. Doing both together is the fastest path to confident interview answers.*
