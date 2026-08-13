# Senior SDET Study Guide — Python, pytest, OOP & Automation Architecture
### Tied to your `Automation_Desktop_Mobile_Web` framework | Target: 10–15 years experience level

---

## Table of Contents
1. [Python — Beyond the Basics](#1-python--beyond-the-basics)
2. [OOP — SOLID Principles & Real Application](#2-oop--solid-principles--real-application)
3. [Design Patterns — Used & Recognisable](#3-design-patterns--used--recognisable)
4. [pytest — Production-Grade Usage](#4-pytest--production-grade-usage)
5. [Selenium & WebDriver — Deep Dive](#5-selenium--webdriver--deep-dive)
6. [Allure Reporting — Enterprise Usage](#6-allure-reporting--enterprise-usage)
7. [Appium & Mobile Strategy](#7-appium--mobile-strategy)
8. [Desktop Automation (pywinauto)](#8-desktop-automation-pywinauto)
9. [Framework Architecture — How to Defend Every Decision](#9-framework-architecture--how-to-defend-every-decision)
10. [Test Strategy & Quality Thinking](#10-test-strategy--quality-thinking)
11. [CI/CD & DevOps Awareness](#11-cicd--devops-awareness)
12. [Senior-Level Interview Q&A — 75 Questions](#12-senior-level-interview-qa--75-questions)
13. [Quick Reference Cheat Sheet](#13-quick-reference-cheat-sheet)

---

## 1. Python — Beyond the Basics

### 1.1 How Python Resolves Names (LEGB Rule)
Python looks up a name in this order:
**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

```python
BROWSER = "chrome"               # Global

class WebDriver:
    def start(self):
        browser = self.browser   # Local — shadows Global BROWSER
```
**Interview answer:** *"When Python sees `browser`, it first checks the local scope of `start()`, then any enclosing function, then the module global, then Python built-ins. This is why a local variable named `list` would shadow the built-in `list`."*

---

### 1.2 Mutable Default Arguments — a Classic Trap
```python
# WRONG — list is created ONCE at function definition time
def add_result(item, results=[]):
    results.append(item)
    return results

# RIGHT
def add_result(item, results=None):
    if results is None:
        results = []
    results.append(item)
    return results
```
This framework correctly uses `None` as defaults everywhere. Mutable defaults (list, dict, set) are a **very common Python interview trap**.

---

### 1.3 Decorators — What They Really Are
```python
# A decorator is just a function that takes a function and returns a function.
# @pytest.fixture is a decorator. @allure.feature is a decorator.

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)   # call the original
        print("After")
        return result
    return wrapper

@my_decorator
def test_something():
    pass

# Equivalent to: test_something = my_decorator(test_something)
```
`@pytest.mark.web`, `@allure.feature("Google")`, `@abstractmethod`, `@property` — all decorators.
A senior SDET must be able to **write** one from scratch.

---

### 1.4 Context Managers — `__enter__` and `__exit__`
```python
# allure.step() is a context manager:
with allure.step("Open Google homepage"):
    page.open()
# __enter__ called → step starts
# __exit__ called → step ends (even if exception raised)

# You can write your own:
class Timer:
    def __enter__(self):
        import time; self.start = time.time(); return self
    def __exit__(self, *args):
        print(f"Elapsed: {time.time() - self.start:.2f}s")

with Timer():
    results_page.wait_for_results()
```
`with` guarantees cleanup — identical to `try/finally` but expressive.
Used for file handles, DB connections, browser sessions.

---

### 1.5 Generators and `yield`
```python
# pytest fixtures use yield for setup/teardown:
@pytest.fixture
def web_driver(request):
    driver = WebDriver().start()
    yield driver          # execution PAUSES here; test runs; then resumes
    driver.quit()         # teardown

# yield also creates generators — lazy sequences:
def read_test_data(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()   # produces one line at a time; no memory overhead
```
**Interview answer:** *"A generator function returns a generator object. Each call to `next()` resumes execution until the next `yield`. pytest fixtures use `yield` to split setup from teardown in a single function — everything before yield is setup, everything after is teardown."*

---

### 1.6 `*args` and `**kwargs` — Practical Use
```python
# find_elements(*RESULT_LINKS) — positional unpacking
RESULT_LINKS = (By.CSS_SELECTOR, "div#search a h3")
driver.find_elements(*RESULT_LINKS)
# Same as: driver.find_elements(By.CSS_SELECTOR, "div#search a h3")

# **kwargs — keyword unpacking
capabilities = {"platformName": "Android", "deviceName": "emulator"}
options.load_capabilities(**capabilities)
```
`*` unpacks iterables. `**` unpacks dicts into keyword arguments.

---

### 1.7 `@property` — Controlled Attribute Access
```python
# pages/web/google_results_page.py
@property
def title(self) -> str:
    return self.driver.title       # called as results.title — no ()

@property
def current_url(self) -> str:
    return self.driver.current_url

# Add a setter to make it writable:
@title.setter
def title(self, value):
    raise AttributeError("title is read-only")
```
Properties enforce the **Uniform Access Principle** — callers use `results.title` regardless of
whether it is a stored value or a computed one.

---

### 1.8 Type Hints and `TypeVar`
```python
# utils/helpers.py
from typing import Callable, TypeVar
T = TypeVar("T")

def retry(func: Callable[[], T], attempts: int = 3, delay: float = 1.0) -> T:
    ...
```
- `TypeVar("T")` is a generic type variable — it captures the actual type at the call site
- If `func` returns `str`, then `retry(func)` returns `str`
- Type hints are **not enforced at runtime** — Python ignores them; they exist for IDEs and `mypy`

---

### 1.9 Logging vs print()
```python
# core/logger.py
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
# %(name)s → the module name passed to get_logger(__name__)
```

| `print()` | `logging` |
|---|---|
| Always outputs | Filtered by level |
| No metadata | Timestamp, level, source module |
| No destination control | File, console, CloudWatch |
| CI noise | Redirectable to artifacts |

**Rule:** No `print()` in a professional automation framework. Ever.

---

### 1.10 `__name__`, `__file__`, `__init__.py`
```python
# config/settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                                                               ^
#                              Full path to settings.py at runtime

# get_logger(__name__)
# __name__ = "drivers.web_driver" in web_driver.py
# __name__ = "__main__" when a file is run directly
```
`__init__.py` in every package folder tells Python "this directory is a package."
Without it, `from pages.web.google_home_page import GoogleHomePage` fails.

---

## 2. OOP — SOLID Principles & Real Application

### The SOLID Principles — With Framework Evidence

### 2.1 S — Single Responsibility Principle
> Every class should have **one reason to change**.

| Class | Responsibility | What it does NOT do |
|---|---|---|
| `WebDriver` | Creates/destroys a browser session | Does not interact with page elements |
| `GoogleHomePage` | Models the Google home page | Does not create the driver |
| `get_logger()` | Returns a configured logger | Does not write tests |
| `normalize_number()` | Cleans calculator output | Does not touch the UI |

**Violation example:** A `TestGoogleSearch` class that also creates its own driver, owns
locators, and parses results — it has 4 reasons to change.

---

### 2.2 O — Open/Closed Principle
> Open for **extension**, closed for **modification**.

```python
# BaseDriver is CLOSED for modification:
class BaseDriver(ABC):
    @abstractmethod
    def start(self): ...

# But OPEN for extension — add a new platform:
class IOSDriver(BaseDriver):     # new subclass — no changes to BaseDriver
    def start(self): ...
    def quit(self): ...
```
Adding Safari browser support requires a new `_build_safari()` method in `WebDriver` —
it does NOT require modifying `BaseDriver`, `BasePage`, or any test.

---

### 2.3 L — Liskov Substitution Principle
> Subclasses must be usable wherever the parent is expected.

```python
def run_test(driver: BaseDriver):
    d = driver.start()
    driver.quit()

run_test(WebDriver())     # works
run_test(MobileDriver())  # works
run_test(DesktopDriver()) # works
```
If `MobileDriver.quit()` raised `NotImplementedError` instead of closing the session, it
would violate LSP — the parent promised the method works; the child breaks that promise.

---

### 2.4 I — Interface Segregation Principle
> Clients should not be forced to depend on methods they do not use.

`BaseDriver` has only `start()` and `quit()` — not 20 methods.
Each Page Object adds only the methods relevant to **that** page:
- `GoogleHomePage` — `open()`, `search()`
- `GoogleResultsPage` — `wait_for_results()`, `get_result_titles()`

Neither page has the other page's methods. Clean, minimal interfaces.

---

### 2.5 D — Dependency Inversion Principle
> High-level modules should not depend on low-level modules. Both should depend on **abstractions**.

```python
# HIGH-LEVEL: test code depends on BasePage abstraction
def test_homepage(web_driver):
    page = GoogleHomePage(web_driver)   # depends on abstraction, not selenium.webdriver.Chrome

# LOW-LEVEL: WebDriver implements BaseDriver abstraction
class WebDriver(BaseDriver):
    def start(self): ...
```
If you replace Selenium with Playwright tomorrow, you only change `WebDriver` —
no test files change.

---

### 2.6 Inheritance vs Composition — When to Choose

| Use **Inheritance** when | Use **Composition** when |
|---|---|
| "IS-A" relationship | "HAS-A" relationship |
| `WebDriver` IS-A `BaseDriver` | `GoogleHomePage` HAS-A `WebDriverWait` |
| Enforcing a contract (ABC) | Building flexible behaviour |
| Hierarchy is shallow (1–2 levels) | Need to mix multiple behaviours |

This framework correctly uses **composition** in Page Objects (`self._wait = WebDriverWait(...)`)
and **inheritance** only for the driver/page contract.

---

### 2.7 Key `__dunder__` Methods
```python
class WebDriver:
    def __init__(self): ...       # constructor — called on WebDriver()
    def __repr__(self): ...       # developer string: repr(obj)
    def __str__(self): ...        # user string: str(obj) / print(obj)
    def __enter__(self): ...      # context manager: with WebDriver() as d:
    def __exit__(self, *a): ...   # context manager cleanup
    def __len__(self): ...        # len(obj)
    def __eq__(self, other): ...  # obj1 == obj2
```
A senior SDET should be able to implement `__enter__`/`__exit__` to make a driver
usable as a context manager (`with WebDriver() as driver:`).

---

## 3. Design Patterns — Used & Recognisable

### 3.1 Page Object Model (POM) — The Core Pattern
```
PROBLEM:  Locators scattered in tests → one UI change breaks 50 tests.
SOLUTION: Each screen = one class. Locators and actions in the class.
          Tests call methods, not find_element().

NON-NEGOTIABLE RULES:
  1. No assertions inside Page Objects
  2. No raw find_element() calls in tests
  3. One class per logical page/screen
  4. Methods return self (for chaining) OR data (for assertion) — never both
  5. Locators in a separate file (this framework: locators/ folder)
```

---

### 3.2 Factory Method
```python
# drivers/web_driver.py
def start(self):
    if self.browser == "chrome":
        self.driver = self._build_chrome()
    elif self.browser == "firefox":
        self.driver = self._build_firefox()
```
Callers use `WebDriver(browser="firefox").start()` — they never call
`selenium.webdriver.Firefox()` directly. Adding Edge support = add `_build_edge()` only.

---

### 3.3 Template Method
```python
# BaseDriver DEFINES the algorithm skeleton:
class BaseDriver(ABC):
    @abstractmethod
    def start(self): ...   # Step 1 — subclass fills in
    @abstractmethod
    def quit(self):  ...   # Step 2 — subclass fills in

# Subclasses FILL IN the steps:
class WebDriver(BaseDriver):
    def start(self): # Selenium implementation
    def quit(self):  # Selenium cleanup
```
Parent defines the "what" (shape of algorithm); subclasses define the "how."

---

### 3.4 Strategy Pattern (Know for Discussion)
```python
# Current: if/elif in start()
# Better (Strategy): inject the browser strategy as an object

class BrowserStrategy(ABC):
    @abstractmethod
    def build(self, headless: bool): ...

class ChromeStrategy(BrowserStrategy):
    def build(self, headless):
        options = ChromeOptions()
        if headless: options.add_argument("--headless=new")
        return webdriver.Chrome(service=ChromeService(...), options=options)

class WebDriver(BaseDriver):
    def __init__(self, strategy: BrowserStrategy):
        self.strategy = strategy
    def start(self):
        self.driver = self.strategy.build(headless=False)
```
Adding a new browser = new Strategy class, zero changes to `WebDriver`.
**Mention this to show architectural awareness beyond basic POM.**

---

### 3.5 Singleton-like Logger
```python
# core/logger.py
logger = logging.getLogger(name)  # returns the SAME object for the same name
if not logger.handlers:           # prevents duplicate handler registration
    logger.addHandler(handler)
```
Python's `logging` module maintains a global registry of named loggers.
The guard prevents duplicate log lines when a module is reimported.

---

### 3.6 Observer Pattern — pytest Hooks
```python
# tests/conftest.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield        # OBSERVE the test result
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("web_driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(), ...)
```
pytest fires events (`pytest_runtest_makereport`); conftest subscribes.
`tryfirst=True` means this hook runs before all others.

---

### 3.7 Builder Pattern — Appium Capabilities
```python
# config/mobile_config.py — options built piece by piece
options = UiAutomator2Options()
options.platform_name       = "Android"
options.automation_name     = "UiAutomator2"
options.app_package         = "com.android.calculator2"
options.app_activity        = "com.android.calculator2.Calculator"
options.no_reset            = True
options.new_command_timeout = 60
# Final object passed to webdriver.Remote(options=options)
```
The Builder pattern constructs complex objects step by step without a
constructor with 10 positional parameters.

---

## 4. pytest — Production-Grade Usage

### 4.1 Fixture Lifecycle — Exact Execution Order
```
pytest collects test_google_homepage_loads_successfully(web_driver)
    │
    ├─ conftest.py: web_driver fixture SETUP
    │    drv = WebDriver()
    │    driver = drv.start()       ← browser opens
    │    yield driver               ← PAUSE; test receives driver
    │
    ├─ TEST BODY RUNS
    │    page = GoogleHomePage(driver)
    │    page.open()
    │    assert "Google" in driver.title
    │
    └─ conftest.py: yield RESUMES → TEARDOWN
         drv.quit()                 ← browser closes
         (runs even if test FAILED or raised exception)
```

---

### 4.2 Fixture Scope — The Right Choice Every Time
```python
@pytest.fixture(scope="function")  # new browser per test (default)
@pytest.fixture(scope="module")    # one browser for whole .py file
@pytest.fixture(scope="session")   # one browser for entire test run
```

| Scope | Pro | Con |
|---|---|---|
| `function` | Fully isolated | Slowest (new browser each test) |
| `module` | Faster, reuses browser per file | Tests must not mutate shared state |
| `session` | Fastest | One crash affects all tests |

**Production rule:** Use `function` scope for write operations.
Use `module`/`session` for read-only smoke tests.

---

### 4.3 Fixture Dependency Chain
```python
@pytest.fixture(scope="session")
def browser_config(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="function")
def web_driver(browser_config):   # requests browser_config fixture
    drv = WebDriver(browser=browser_config)
    driver = drv.start()
    yield driver
    drv.quit()
```
pytest resolves the dependency graph automatically.
A `function`-scope fixture CAN depend on a `session`-scope fixture.

---

### 4.4 `conftest.py` Hierarchy — Scope Control
```
tests/
  conftest.py          ← fixtures for ALL tests (web_driver, mobile_driver)
  web/
    conftest.py        ← web-only fixtures (GoogleHomePage instance, base URL)
  mobile/
    conftest.py        ← mobile-only fixtures (Appium URL, device caps)
```
Place fixtures at the **lowest level that shares them.**
Don't put a `web_driver` fixture in root if only web tests use it.

---

### 4.5 Important pytest Hooks
```python
def pytest_configure(config):
    """Startup — register markers, plugins."""

def pytest_collection_modifyitems(items, config):
    """Reorder or deselect tests after collection."""

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each phase — attach screenshots, log results."""

def pytest_sessionfinish(session, exitstatus):
    """After all tests — send Slack notification, upload report."""
```

---

### 4.6 Parametrize — Advanced Patterns
```python
# Named IDs in report
@pytest.mark.parametrize("browser", ["chrome", "firefox"], ids=["Chrome", "Firefox"])

# Indirect — passes value through fixture
@pytest.mark.parametrize("web_driver", ["chrome", "firefox"], indirect=True)
def test_homepage(web_driver): ...

# Combined with marks
@pytest.mark.parametrize("query, expected", [
    pytest.param("Python", "python.org", id="python", marks=pytest.mark.web),
    pytest.param("Selenium", "selenium.dev", id="selenium", marks=pytest.mark.slow),
])
```

---

### 4.7 Custom Markers with Conditions
```python
# Skip on CI:
@pytest.mark.skipif(os.getenv("CI") == "true", reason="No display in CI")
@pytest.mark.desktop
def test_calculator(): ...

# Expected failure (known bug):
@pytest.mark.xfail(reason="Known bug JIRA-1234", strict=False)
def test_flaky_scenario(): ...
```

---

## 5. Selenium & WebDriver — Deep Dive

### 5.1 W3C WebDriver Protocol
```
Test (Python) → Selenium bindings → HTTP POST /session → ChromeDriver → Chrome
                                     HTTP GET  /element
                                     HTTP POST /element/{id}/click
```
Every Selenium call is an **HTTP request** to ChromeDriver. This explains:
- Why `find_element` is slow (network round-trip even on localhost)
- Why `execute_script` can bypass waits (direct JS execution)
- Why parallel tests need separate driver instances (separate HTTP sessions)

---

### 5.2 Explicit Waits — Production Rules
```python
# THIS FRAMEWORK — correctly uses explicit waits:
self._wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)
element = self._wait.until(EC.element_to_be_clickable(SEARCH_INPUT))

# KNOWN ISSUE in this framework:
# implicitly_wait(10) is also set in WebDriver.start()
# FIX: change to driver.implicitly_wait(0) — never mix both
```
**Why mixing breaks things:**
`EC.invisibility_of_element_located` waits until element disappears.
If implicit wait is 10s, Selenium waits 10s finding the element that's already gone.
The two mechanisms are unaware of each other — **doubled timeouts**.

---

### 5.3 Expected Conditions — Full Reference
```python
EC.presence_of_element_located(locator)           # exists in DOM
EC.visibility_of_element_located(locator)          # visible + in DOM
EC.invisibility_of_element_located(locator)        # hidden or gone
EC.element_to_be_clickable(locator)                # visible + enabled
EC.text_to_be_present_in_element(locator, text)    # element text contains
EC.text_to_be_present_in_element_value(locator, t) # input value contains
EC.title_contains("Google")
EC.url_contains("search?q=")
EC.staleness_of(element)                           # old reference is stale
EC.number_of_windows_to_be(2)                      # popup handling
EC.frame_to_be_available_and_switch_to_it(locator) # iframe handling
```

---

### 5.4 Advanced Interactions
```python
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)

actions.move_to_element(menu).perform()             # hover
actions.drag_and_drop(source, target).perform()     # drag and drop
actions.context_click(element).perform()            # right-click
actions.double_click(element).perform()             # double-click
actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
```

---

### 5.5 JavaScript Execution
```python
driver.execute_script("arguments[0].scrollIntoView(true);", element)
driver.execute_script("arguments[0].click();", element)          # bypass overlaps
driver.execute_script("arguments[0].value = arguments[1];", el, "value")
page_title = driver.execute_script("return document.title;")
```

---

### 5.6 Handling Special Scenarios
```python
# iFrames:
driver.switch_to.frame("frame_name")
driver.switch_to.default_content()

# Alerts:
alert = driver.switch_to.alert
alert.accept(); alert.dismiss(); alert.send_keys("text")

# New tabs:
original = driver.current_window_handle
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
for handle in driver.window_handles:
    if handle != original:
        driver.switch_to.window(handle)

# Dropdowns:
from selenium.webdriver.support.ui import Select
Select(driver.find_element(By.ID, "country")).select_by_visible_text("India")
```

---

### 5.7 Locator Strategy — Decision Guide
```
Unique ID?                    → By.ID (fastest)
Form input with name="x"?     → By.NAME
Describable with CSS?         → By.CSS_SELECTOR (preferred)
Need text content matching?   → By.XPATH → //button[text()='Submit']
Exact link text?              → By.LINK_TEXT

XPath axes:
  //div[@class='r']//a           → descendant
  //input[@name='q']/..          → parent
  //label[text()='Name']/following-sibling::input  → sibling
```

---

## 6. Allure Reporting — Enterprise Usage

### 6.1 Full Decorator Reference
```python
@allure.epic("Search Platform")           # highest grouping (product area)
@allure.feature("Google Web Search")      # feature within the epic
@allure.story("Homepage Navigation")      # user story
@allure.title("Homepage loads with correct browser title")
@allure.description("""
    GIVEN the user navigates to google.com
    WHEN the page finishes loading
    THEN the browser title should contain 'Google'
""")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "regression")
@allure.link("https://jira.company.com/PROJ-123", name="JIRA Ticket")
```

---

### 6.2 Severity Levels — When to Use Each
| Level | Use for | Impact of failure |
|---|---|---|
| `BLOCKER` | Login, homepage, checkout flow | Entire release blocked |
| `CRITICAL` | Core features — search, add to cart | Major functionality broken |
| `NORMAL` | Standard features — filters, sort | Partial degradation |
| `MINOR` | Edge cases — empty states, tooltips | Minor UX issue |
| `TRIVIAL` | Cosmetic — tooltips, pixel alignment | No business impact |

---

### 6.3 Steps and Attachments
```python
def test_search_returns_at_least_one_result(web_driver):
    with allure.step("Navigate to Google"):
        home = GoogleHomePage(web_driver)
        home.open()
        allure.attach(web_driver.get_screenshot_as_png(),
                      name="Homepage loaded",
                      attachment_type=allure.attachment_type.PNG)

    with allure.step("Perform search"):
        home.search("Python automation testing")

    with allure.step("Verify results are present"):
        results = GoogleResultsPage(web_driver)
        results.wait_for_results()
        titles = results.get_result_titles()
        allure.attach("\n".join(titles),
                      name="Search Results",
                      attachment_type=allure.attachment_type.TEXT)
        assert len(titles) > 0
```

---

### 6.4 Screenshot on Failure — The Hook Explained
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield                     # run the actual test phase
    report  = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("web_driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )
```
- `tryfirst=True` — runs before other plugins
- `hookwrapper=True` — `yield` is where the wrapped hook runs
- `report.when` — `"setup"`, `"call"`, or `"teardown"`

---

### 6.5 Running Reports
```bash
# Run tests + collect JSON results
pytest tests/web/ --alluredir=allure-results

# Serve live report (CORRECT — fixes blank page from file://)
allure serve allure-results

# Generate static HTML (for CI artifacts)
allure generate allure-results --clean -o allure-report

# Open static report via server (not file://)
allure open allure-report
```

---

## 7. Appium & Mobile Strategy

### 7.1 Architecture
```
Python Test
    │  HTTP (W3C WebDriver Protocol)
    ▼
Appium Server (Node.js, port 4723)
    │  ADB commands
    ▼
UiAutomator2 (APK on device)
    │  Android Accessibility API
    ▼
Calculator App
```

### 7.2 Key Capabilities — What Each Does
```python
ANDROID_OPTIONS = {
    "platformName":      "Android",
    "automationName":    "UiAutomator2",   # engine (XCUITest for iOS)
    "deviceName":        "Android Emulator",
    "appPackage":        "com.android.calculator2",
    "appActivity":       "com.android.calculator2.Calculator",
    "noReset":           True,             # keep app data between sessions
    "newCommandTimeout": 60,               # session timeout seconds
}
```

### 7.3 Reset Strategies
| Option | Behaviour | Speed |
|---|---|---|
| `noReset=True` | Keep data + state | Fastest |
| `noReset=False` | Clear data, don't uninstall | Medium |
| `fullReset=True` | Uninstall + reinstall APK | Slowest |

### 7.4 Appium 1.x vs 2.x
```python
# Appium 1.x — requires /wd/hub base path (this framework's setup)
APPIUM_SERVER_URL = "http://127.0.0.1:4723/wd/hub"

# Appium 2.x — no base path
APPIUM_SERVER_URL = "http://127.0.0.1:4723"
```

### 7.5 Mobile Locator Strategies
```python
# Android — preferred:
(MobileBy.ACCESSIBILITY_ID, "accessibility_id")          # stable, fast
(MobileBy.ID, "com.android.calculator2:id/digit_1")      # resource ID
(By.XPATH, '//android.widget.Button[@text="1"]')         # text matching

# iOS — preferred:
(MobileBy.ACCESSIBILITY_ID, "1")
(MobileBy.IOS_PREDICATE, 'label == "1"')
```

---

## 8. Desktop Automation (pywinauto)

### 8.1 Backend Choice
```python
Application(backend="uia")   # UI Automation — modern apps (UWP, WPF)
Application(backend="win32") # legacy MFC/WinForms apps

# Windows Calculator (UWP) → always use "uia"
```

### 8.2 Window Identification
```python
# By title:
window = Desktop(backend="uia").window(title="Calculator")

# By class (most stable — doesn't change with localisation):
window = Desktop(backend="uia").window(class_name="ApplicationFrameWindow")

# Inspect tools: "Accessibility Insights for Windows" or "Inspect.exe"
```

### 8.3 Control Interaction
```python
window.type_keys("1{+}1{ENTER}", set_foreground=True)
window.child_window(title="One", control_type="Button").click()
result = window.child_window(auto_id="CalculatorResults").window_text()
# Returns: "Display is 2" → needs normalize_number() from utils/helpers.py
```

---

## 9. Framework Architecture — How to Defend Every Decision

### 9.1 "Walk me through your framework" — Model Answer
> *"The framework follows a strict 5-layer separation. Bottom layer is config — all environment-specific values in one place. Above that, core contains abstract base classes that define the contract every driver and page must fulfil. The drivers layer implements those contracts for three platforms: Selenium for web, Appium for mobile, and pywinauto for desktop. Above drivers, the pages layer implements the Page Object Model — each page class owns its locators and user actions, injecting the driver through the constructor. At the top, tests contain only assertions and high-level workflow logic. This means a locator change requires editing one file; adding a new platform requires only a new driver and page class with zero changes to tests."*

---

### 9.2 Design Decision Tradeoffs
| Decision | Alternative | Why this choice |
|---|---|---|
| ABC for BaseDriver | Duck typing | Enforces contract at class definition — fails early |
| Separate locators file | Locators inside page class | Locators change more often than actions |
| Function-scope fixtures | Session-scope | Each test fully isolated — no state leak |
| WebDriverWait per page | Global implicit wait | Predictable timeout; no implicit/explicit mixing |
| `yield` fixture | `setup_method` | Teardown guaranteed even if setup raises exception |
| `get_logger(__name__)` | Single root logger | Per-module attribution |

---

### 9.3 Honest Gaps — Answer Confidently
When asked *"what would you improve?"*:

1. **Implicit + explicit wait mix** — `implicitly_wait(10)` should be `0`
2. **No retry logic** — `pytest-rerunfailures` for flaky network tests
3. **No CI/CD pipeline** — GitHub Actions for automated PR runs
4. **No environment switching** — `TEST_ENV=staging pytest` pattern
5. **Mobile/desktop lack Allure decorators** — only web tests have them
6. **No API test layer** — test pyramid is incomplete

*"These are the next iterations. The architecture already supports them — none require structural changes, only additions."*

---

## 10. Test Strategy & Quality Thinking

### 10.1 The Test Pyramid
```
         /\
        /  \        E2E / UI Tests       (few, slow, expensive — this framework)
       /────\
      / API  \      API / Integration    (medium count, fast)
     /────────\
    /  Unit    \    Unit Tests           (many, very fast, cheap)
   /────────────\
```
**Senior answer:** *"UI tests are expensive — slow, brittle, require running infrastructure.
I use them for critical user journeys only. The bulk of coverage is at unit and API layers."*

---

### 10.2 Test Categories
| Category | Purpose | Frequency |
|---|---|---|
| **Smoke** | App is alive (homepage loads) | Every deployment |
| **Sanity** | Core features after a change | After every PR |
| **Regression** | Nothing existing is broken | Nightly / pre-release |
| **Exploratory** | Find unexpected defects | Manual, sprint cycles |
| **Performance** | Load and stress testing | Pre-release |

---

### 10.3 What Makes a Good Test
```python
# A good test:
# 1. Tests exactly ONE scenario
# 2. Is independent — doesn't rely on another test's state
# 3. Is deterministic — same result every run
# 4. Has a clear failure message
# 5. Follows AAA: Arrange → Act → Assert

def test_search_returns_at_least_one_result(web_driver):
    # ARRANGE
    home = GoogleHomePage(web_driver)
    home.open()
    # ACT
    home.search("Python automation testing")
    results = GoogleResultsPage(web_driver)
    results.wait_for_results()
    # ASSERT
    assert len(results.get_result_titles()) > 0, "Expected results, got none."
```

---

### 10.4 Flaky Tests — How to Handle
```python
# 1. Retry (last resort — masks root cause)
# pytest --reruns 2 --reruns-delay 1  (pip install pytest-rerunfailures)

# 2. Fix root cause:
#    - Replace time.sleep() with explicit waits
#    - Fix timing with EC.staleness_of()
#    - Isolate test data

# 3. Quarantine until fixed:
@pytest.mark.xfail(reason="Flaky — JIRA-789", strict=False)
def test_known_flaky(): ...
```

---

## 11. CI/CD & DevOps Awareness

### 11.1 GitHub Actions — Conceptual Pipeline
```yaml
name: Web Regression
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: pytest tests/web/ -m web --alluredir=allure-results --headless
      - uses: actions/upload-artifact@v4
        with: { name: allure-results, path: allure-results/ }
```

---

### 11.2 Environment Strategy
```python
ENV = os.getenv("TEST_ENV", "staging")

BASE_URLS = {
    "dev":     "http://dev.internal.company.com",
    "staging": "https://staging.google.com",
    "prod":    "https://www.google.com",
}

BASE_URL = BASE_URLS.get(ENV, BASE_URLS["staging"])

# Run: TEST_ENV=prod pytest tests/web/
```

---

### 11.3 What a Senior SDET Owns in CI
- Owns the pipeline config — not just runs tests in it
- Fail-fast strategy — smoke tests first; if they fail, stop
- Parallel execution — `pytest-xdist` with `-n auto`
- Report publishing — Allure results as build artifacts
- Notification — Slack/Teams webhook on failure
- Scheduled runs — nightly regression, weekly full suite

---

## 12. Senior-Level Interview Q&A — 75 Questions

### Python (15 Questions)

**Q1: What is the GIL and how does it affect test parallelism?**
The Global Interpreter Lock prevents true multi-threading for CPU-bound work in CPython.
For I/O-bound tests (browser automation), `threading` works fine.
For true parallelism: use `pytest-xdist` which spawns separate **processes** (each with own GIL).

**Q2: What is the difference between `deepcopy` and `copy`?**
`copy.copy()` — shallow copy; nested objects still share references.
`copy.deepcopy()` — recursively copies all nested objects.
Relevant when sharing capability dicts between tests — shallow copy means modifying one modifies all.

**Q3: Explain Python's `@property` vs a regular attribute.**
A regular attribute is stored in `__dict__`. A `@property` is a descriptor — it runs code on access.
`results.title` calls `driver.title` each time — the driver is the single source of truth.

**Q4: What happens when you import the same module twice?**
Python caches modules in `sys.modules`. The second import returns the cached object — the file
is not re-executed. This is why `get_logger(__name__)` returns the same logger every time.

**Q5: What is `__slots__` and when would you use it?**
Replaces per-instance `__dict__` with fixed attribute slots. Less memory, faster access.
Use in frameworks where thousands of page object instances are created.

**Q6: What is the difference between `is` and `==`?**
`is` checks identity (same memory address). `==` checks value equality.
`None` checks: always `if driver is None` — never `== None`.

**Q7: What is a descriptor protocol?**
An object implementing `__get__`, `__set__`, `__delete__`. `@property` is a descriptor.
Used to implement reusable attribute logic across classes.

**Q8: Explain MRO (Method Resolution Order).**
Python uses C3 linearisation for multiple inheritance. `ClassName.__mro__` shows the order.
In this framework all classes use single inheritance — MRO is `WebDriver → BaseDriver → ABC → object`.

**Q9: What is a metaclass?**
A class whose instances are classes. `ABC` uses `ABCMeta` as metaclass to register abstract methods.
Rarely written directly — but understanding it explains how `@abstractmethod` works.

**Q10: How does `pytest.raises` work internally?**
Context manager. On `__enter__`: registers expected exception. On `__exit__`: if expected exception
was raised, suppresses it (pass). Otherwise raises `Failed`.

**Q11: What is `functools.wraps` and why does it matter in decorators?**
Without `@wraps`, decorated functions lose `__name__`, `__doc__`. pytest uses function names for
test IDs — without `@wraps`, all decorated tests would show as `wrapper`.

**Q12: What is the difference between `assertRaises` and `pytest.raises`?**
`assertRaises` is unittest-style. `pytest.raises` is a context manager — provides access to
the exception via `excinfo.value`. More Pythonic, integrates with Allure steps.

**Q13: When would you use `@classmethod` over `__init__`?**
Alternative constructors. `WebDriver.from_config()` reads config and calls `cls(browser=BROWSER)`.
Use when an object can be created from multiple sources without polluting `__init__` with parameters.

**Q14: What is a `namedtuple` and when is it better than a dict?**
Immutable, memory-efficient tuple with named fields. Good for locator definitions:
`Locator = namedtuple("Locator", ["by", "value"])`. Access by name is clearer than by string key.

**Q15: How does Python handle multiple return values?**
Returns a tuple. `return driver, config` → `(driver, config)`. Destructuring: `d, c = func()`.
Used in parametrize: each row is a tuple of argument values.

---

### OOP & Design (15 Questions)

**Q16: What is LSP with a concrete violation example?**
If `MobileDriver.quit()` logged an error and returned without closing the session (device stays
locked), it violates LSP — the parent promised the method closes the session; the child doesn't.

**Q17: Composition over inheritance — automation example.**
`GoogleHomePage HAS-A WebDriverWait` (composition) not IS-A.
`self._wait = WebDriverWait(driver, timeout)` — the page doesn't need to inherit wait behaviour; it uses an instance.

**Q18: Abstract class vs interface in Python.**
Python has no `interface` keyword. An ABC with only `@abstractmethod` acts as a pure interface.
An ABC can also have concrete methods — partial implementation. `BaseDriver` acts as a pure interface.

**Q19: How would you implement the Observer pattern for test notifications?**
pytest's hook system IS the Observer pattern. `pytest_runtest_makereport` is the event.
`conftest.py` subscribes with `@pytest.hookimpl`. Custom: `EventBus.subscribe("TEST_FAILED", slack_notify)`.

**Q20: What is the Facade pattern in automation context?**
A `TestSession` class wrapping driver creation, Allure setup, and logging in a single `start()` call.
Tests use `TestSession.start()` instead of 3 separate calls. Hides subsystem complexity.

**Q21: Strategy vs Template Method — key difference.**
Template Method: algorithm steps defined in parent, filled in by subclass (inheritance).
Strategy: algorithm injected as an object (composition). Strategy is more flexible — swap at runtime.

**Q22: What is cohesion and coupling?**
Cohesion — how related responsibilities within a class are. **High cohesion = good.**
Coupling — how much classes depend on each other. **Low coupling = good.**
`WebDriver` doesn't import anything from `pages/` — low coupling example.

**Q23: What is method overloading in Python?**
Python doesn't support it. Use default arguments or `*args`/`**kwargs` instead.
`search(query, submit=True)` handles multiple call signatures with one method.

**Q24: Explain multiple inheritance and the diamond problem.**
Class D inherits B and C, both from A — which `A.__init__` runs? Python's MRO resolves this.
Fix: always call `super().__init__()` — not the parent directly. `super()` follows MRO.

**Q25: What is monkey patching and when is it acceptable?**
Replacing a class/method at runtime. Acceptable in tests to replace expensive operations.
In pytest: use `monkeypatch` fixture or `unittest.mock.patch`. Avoid in production code.

**Q26: `isinstance` vs `type` — which to prefer?**
`type(obj) == WebDriver` fails for subclasses. `isinstance(obj, BaseDriver)` is True for any subclass.
Always prefer `isinstance` — respects inheritance hierarchy.

**Q27: What are dataclasses and where do they fit?**
`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__`. Perfect for config objects:
`@dataclass class BrowserConfig: browser: str = "chrome"; headless: bool = False`.

**Q28: What is `__init_subclass__`?**
Called when a subclass is **defined** — not when instantiated.
`ABC` uses it to register abstract methods. Useful for plugin registration systems.

**Q29: How would you implement a context manager without `contextlib`?**
```python
class BrowserSession:
    def __enter__(self):
        self.driver = WebDriver().start()
        return self.driver
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        return False  # don't suppress exceptions
```

**Q30: What is the difference between `__repr__` and `__str__`?**
`__repr__` for developers — unambiguous, ideally `eval(repr(obj)) == obj`.
`__str__` for users — human-readable. If only `__repr__` defined, Python uses it for both.

---

### pytest (15 Questions)

**Q31: Fixture vs setup method — key differences.**
`setup_method` can't return a value, can't be reused across files, no scopes.
Fixtures: injectable by name, 4 scopes, reusable via conftest, teardown guaranteed via `yield`.

**Q32: How to share data between fixtures?**
Fixtures can depend on other fixtures — pytest injects them by parameter name.
`session`-scope `browser_config` consumed by `function`-scope `web_driver`.

**Q33: pytest.ini vs pyproject.toml.**
`pytest.ini` — explicit, only pytest reads it. `pyproject.toml` — modern Python standard
(`[tool.pytest.ini_options]`). This framework uses `pytest.ini` — clearest for a test-only project.

**Q34: How do you run a single test?**
```bash
pytest tests/web/test_google_search.py::test_google_homepage_loads_successfully
pytest tests/web/ -k "homepage"     # keyword match
pytest --collect-only               # see what would run
```

**Q35: What is `indirect=True` in parametrize?**
Passes parameter through a fixture instead of directly to the test.
`@pytest.mark.parametrize("web_driver", ["chrome", "firefox"], indirect=True)` — fixture reads `request.param`.

**Q36: How would you implement test ordering?**
`pip install pytest-ordering`. Use `@pytest.mark.run(order=1)`. But: tests should be order-independent.
Ordering requirement signals state coupling between tests — a design smell.

**Q37: What is `capfd` fixture?**
Captures stdout/stderr. `capsys.readouterr()` returns `(out, err)`.
Useful for testing logger output contains expected messages.

**Q38: How do you fail a test with a custom message without `assert`?**
`pytest.fail("Expected element visible after 10s")` — raises `Failed` immediately.
More explicit than `assert` for complex multi-condition failures.

**Q39: What is `tmp_path` fixture?**
pytest built-in providing a `pathlib.Path` temp directory unique to each test.
Use for tests that write screenshots or downloads — no manual cleanup code needed.

**Q40: `@pytest.mark.usefixtures` vs parameter injection?**
`usefixtures` runs the fixture but test doesn't receive the return value.
Use for side-effect fixtures (set env vars, start a server) rather than value-providing ones.

**Q41: What is `pytest-xdist`?**
Runs tests in parallel using separate processes. `-n auto` detects CPU count.
**Critical caveat:** tests must be truly independent — no shared state, no port conflicts.

**Q42: `request.addfinalizer` vs `yield`.**
`addfinalizer` registers multiple cleanup callbacks independently — each runs even if others fail.
`yield` is cleaner and readable. Use `addfinalizer` when multiple conditional cleanups needed.

**Q43: How does pytest discover `conftest.py`?**
Walks up from the test file to rootdir, collecting all `conftest.py` files.
Fixtures scoped to the directory and all subdirectories below it.

**Q44: How to implement retry for flaky tests?**
`pytest-rerunfailures` plugin: `--reruns 3 --reruns-delay 2`.
Integrates with Allure — retried attempts show as separate runs in the report.

**Q45: What are `pytest` built-in fixtures?**
`tmp_path`, `capsys`, `capfd`, `monkeypatch`, `request`, `tmpdir`, `recwarn`.
`request` is the most important — access to test metadata, config, parametrize values.

---

### Selenium & Automation (15 Questions)

**Q46: StaleElementReferenceException — cause and fix.**
DOM updated after element was found. Fix: re-find element, or `EC.staleness_of(old_el)` then find new.
The `retry()` in `utils/helpers.py` handles transient staleness.

**Q47: `driver.close()` vs `driver.quit()`.**
`close()` — current window only; session continues. `quit()` — all windows, session terminated.
Always use `quit()` in teardown — leaking sessions exhausts system resources.

**Q48: File uploads in Selenium.**
`input_element.send_keys("/absolute/path/to/file.txt")` — no special handling.
For remote grid: use `driver.file_detector_context(LocalFileDetector)`.

**Q49: Shadow DOM — how to interact.**
`find_element` can't reach inside shadow roots. Use JavaScript:
`driver.execute_script("return arguments[0].shadowRoot.querySelector('input')", host_el)`.

**Q50: CAPTCHA in automated tests.**
You don't solve CAPTCHAs. Instead: disable via feature flag in test env, use test accounts with
bypass, or mock the endpoint. Solving production CAPTCHAs violates terms of service.

**Q51: Page Factory vs this framework's POM.**
Page Factory (Java) uses `@FindBy` annotations — lazy element initialisation at page creation.
This framework: lazily finds elements on method calls — more robust for dynamic pages. No Python equivalent of `@FindBy`.

**Q52: Cross-browser parallel tests.**
`pytest-xdist` + indirect parametrize on `web_driver` fixture.
`pytest -n 2` runs Chrome and Firefox simultaneously in separate processes.

**Q53: What is Selenium Grid?**
Distributes execution across machines. Hub receives requests; nodes have different OS/browser combos.
Use when: 50+ parallel tests, testing Safari from Linux CI, shared test infrastructure.

**Q54: Certificate errors in Chrome automation.**
`options.add_argument("--ignore-certificate-errors")` — for internal staging with self-signed certs.
Never do this for production URLs — masks real security issues.

**Q55: `find_element` vs `find_elements`.**
`find_element` — returns one; raises `NoSuchElementException` if not found.
`find_elements` — returns list; empty list if none. Use `find_elements` to check existence.

**Q56: Element-level vs full-page screenshot.**
`element.screenshot("el.png")` — just the element.
`driver.save_screenshot("page.png")` — visible viewport.
Allure: `allure.attach(driver.get_screenshot_as_png(), attachment_type=PNG)`.

**Q57: Chrome options for headless CI.**
`--headless=new`, `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu`, `--window-size=1920,1080`.

**Q58: `ActionChains` vs regular `click()`.**
`click()` teleports cursor. `move_to_element().click()` simulates real mouse movement.
Needed for hover-activated menus, drag-and-drop, right-click.

**Q59: Verify file downloaded.**
Set Chrome download path in prefs. Poll `os.path.exists()` with timeout.
Fail test if file not present within `timeout` seconds.

**Q60: `execute_cdp_cmd` in Selenium 4.**
Direct Chrome DevTools Protocol access. Network throttling, intercept requests, emulate devices.
`driver.execute_cdp_cmd("Network.emulateNetworkConditions", {"latency": 100, ...})`.

---

### Architecture & Strategy (15 Questions)

**Q61: How would you onboard a new team member to this framework?**
STUDY_GUIDE → architecture top-down walkthrough → pair program one test end-to-end →
review their first PR focused on POM correctness and wait strategy.
Goal: independently add a page and test within one sprint.

**Q62: How do you measure automation ROI?**
(Manual test time saved per cycle) × (cycles per year) vs (build + maintenance time).
40h saved × 24 releases = 960h/year. If build cost 200h, ROI positive from release 1.

**Q63: When would you NOT automate?**
One-time scenarios. Inherently visual tests (use visual regression tools). Features under active
development. Physical hardware (NFC, biometric). Exploration-heavy discovery testing.

**Q64: What is shift-left testing?**
Moving testing earlier in the dev cycle — unit tests at commit, API tests before UI is ready.
Automation supports it: desktop/API tests don't need a full UI build.

**Q65: Locator changes with every release — what do you do?**
Negotiate stable `data-testid` attributes with developers. Use text-based XPath as interim.
Use accessibility IDs on mobile — stable by design. Centralise in `locators/` — one fix, all tests.

**Q66: Test isolation in CI — why it matters.**
Tests run in arbitrary order across parallel workers. If test A creates data test B depends on,
tests fail randomly in parallel. Function-scope fixtures in this framework ensure clean state each test.

**Q67: Authentication spanning multiple tests.**
Session-scope: login once, save cookies, inject into each test's browser.
Function-scope: login in setup fixture. Never share a logged-in session between tests.

**Q68: Contract testing vs integration testing.**
Contract (Pact): verifies interface agreement between consumer/provider independently. No real server needed.
Integration: runs both together. Contract is faster, more targeted, pinpoints which side broke.

**Q69: Adding API coverage to this framework.**
`tests/api/` folder with `requests` library. `api_client` fixture with `requests.Session`.
Same Allure decorators, same markers (`@pytest.mark.api`). Architecture supports it already.

**Q70: What metrics do you track?**
Pass rate, execution time trend, flakiness rate, user journey coverage %, mean time to detect
regression, false positive rate (automation failures not caused by actual bugs).

**Q71: How to prioritise what to automate first?**
Risk × frequency. Login → core transactions → past critical bug scenarios → smoke → edge cases.

**Q72: What is visual regression testing?**
Baseline screenshots compared pixel-by-pixel on each run.
Tools: Percy, Applitools, BackstopJS. Add alongside Selenium — Page Objects unchanged.

**Q73: Test passes locally, fails in CI — debug checklist.**
1. Headless differences — add screenshot every step
2. Timing — CI is slower; increase waits
3. Viewport — set `window-size=1920,1080` explicitly
4. Environment — wrong BASE_URL, missing env vars
5. Data — CI database missing seed data
6. Run locally with `--headless` to reproduce

**Q74: Code review checklist for a new test PR.**
No raw `find_element` in tests. No `time.sleep()`. No assertions in Page Objects.
Descriptive test name. Allure decorators present. AAA structure. New locators in `locators/` folder.
Fixture for setup, not repeated code.

**Q75: 15-minute interview demo — what to show.**
Architecture diagram (90 sec) → run `pytest tests/web/ --alluredir=allure-results` →
while running: walk one test file showing Allure decorators → `allure serve` walkthrough →
`conftest.py` fixture lifecycle + screenshot hook → `core/base_driver.py` ABC contract.
Close with: *"Web, mobile, desktop. Add a platform: one driver, one page base, zero test changes."*

---

## 13. Quick Reference Cheat Sheet

### Run Commands
```powershell
# Web tests
python -m pytest tests/web/ -m web -v

# Desktop tests
python -m pytest tests/desktop/ -m desktop -v

# With Allure results
python -m pytest tests/web/ --alluredir=allure-results

# Serve Allure report (fixes blank page)
$env:JAVA_HOME = "C:\Automation_Desktop_Mobile_Web\tools\jdk17\jdk-17.0.18+8"
$env:PATH = "$env:JAVA_HOME\bin;C:\Automation_Desktop_Mobile_Web\tools\allure\allure-2.30.0\bin;$env:PATH"
allure serve allure-results

# Headless (for CI simulation)
python -m pytest tests/web/ --headless

# Specific browser
python -m pytest tests/web/ --browser=firefox

# Parallel (requires pytest-xdist)
python -m pytest tests/web/ -n auto
```

### Key Import Map
```python
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from appium.options.android import UiAutomator2Options
import allure
import pytest
import logging
import os
from typing import Callable, TypeVar
```

### SOLID — One-Line Summary
```
S — One class, one reason to change
O — Extend with new classes; don't modify existing ones
L — Subclasses must honour parent's contract
I — Keep interfaces small and focused
D — Depend on abstractions (ABC), not concrete classes
```

### Allure Severity
```
BLOCKER  → homepage, login, checkout    (release blocked)
CRITICAL → core features                (major functionality broken)
NORMAL   → standard features            (partial degradation)
MINOR    → edge cases                   (minor UX issue)
TRIVIAL  → cosmetic                     (no business impact)
```

### pytest Scope Decision Tree
```
Each test modifies state?             → function scope
Read-only within one file?            → module scope
Extremely expensive setup (10+ s)?    → session scope (with isolation care)
```

### Test Pyramid — What to Automate
```
UI/E2E     → critical user journeys only (this framework)
API        → all service contracts + data validation
Unit       → all business logic, algorithms, utilities
```

---

*Every concept in this guide maps to a specific file in your Automation_Desktop_Mobile_Web project.
Open the file alongside this guide — reading both together is the fastest path to interview confidence.*
