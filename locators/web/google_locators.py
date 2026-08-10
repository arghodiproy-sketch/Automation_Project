"""
locators/web/google_locators.py

Interview Tip:
    Selenium locator strategies — ranked by reliability:
      By.ID              ← fastest and most specific (Google rarely exposes IDs)
      By.NAME            ← great for form fields (e.g. the search box: name="q")
      By.CSS_SELECTOR    ← preferred for most elements; fast, readable
      By.XPATH           ← most powerful; use for text-matching or complex paths
      By.CLASS_NAME      ← fragile; classes change often (especially on Google)
      By.TAG_NAME        ← too broad; useful only for unique tags (e.g. h1)
      By.LINK_TEXT       ← exact link text (locale-dependent)

    Locators are stored as (By.STRATEGY, "value") tuples so they can be
    passed directly to find_element(*locator) or WebDriverWait(...).until(
    EC.presence_of_element_located(locator)).
"""

from selenium.webdriver.common.by import By

# ── Google Home Page ───────────────────────────────────────────────────────────
SEARCH_INPUT = (By.NAME, "q")           # main search input field
SEARCH_BTN   = (By.NAME, "btnK")        # "Google Search" button
LUCKY_BTN    = (By.NAME, "btnI")        # "I'm Feeling Lucky" button

# ── Google Results Page ────────────────────────────────────────────────────────
RESULTS_STATS        = (By.ID, "result-stats")
# All organic result headings on the results page
RESULT_LINKS         = (By.CSS_SELECTOR, "div#search a h3")
FIRST_RESULT         = (By.CSS_SELECTOR, "div#search a h3:first-of-type")
# Search box on the results page (same name attribute as home page)
SEARCH_INPUT_RESULTS = (By.NAME, "q")
