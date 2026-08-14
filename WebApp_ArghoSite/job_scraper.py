"""
job_scraper.py — Search LinkedIn Jobs and Naukri for relevant openings.

Both sites are scraped via public search pages (no login required).
Requests are rate-limited and use a realistic User-Agent header.
"""
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

TIMEOUT = 10   # seconds per request


# ── LinkedIn ────────────────────────────────────────────────────────────────

def search_linkedin(query: str, location: str = "India", max_results: int = 10) -> list[dict]:
    """
    Scrape LinkedIn public job listings (no login required).
    URL: https://www.linkedin.com/jobs/search/?keywords=...&location=...
    """
    jobs = []
    url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={requests.utils.quote(query)}"
        f"&location={requests.utils.quote(location)}"
        "&sortBy=DD"
    )
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "lxml")

        cards = soup.select("div.base-card")[:max_results]
        for card in cards:
            title_el   = card.select_one("h3.base-search-card__title")
            company_el = card.select_one("h4.base-search-card__subtitle")
            location_el = card.select_one("span.job-search-card__location")
            link_el    = card.select_one("a.base-card__full-link")
            date_el    = card.select_one("time")

            if not title_el:
                continue

            jobs.append({
                "source":   "LinkedIn",
                "title":    title_el.get_text(strip=True),
                "company":  company_el.get_text(strip=True) if company_el else "N/A",
                "location": location_el.get_text(strip=True) if location_el else location,
                "link":     link_el["href"] if link_el else url,
                "posted":   date_el.get("datetime", "")[:10] if date_el else "",
                "description": "",
            })
    except Exception as exc:
        print(f"[LinkedIn] Scrape error: {exc}")

    return jobs


# ── Naukri ───────────────────────────────────────────────────────────────────

def search_naukri(query: str, location: str = "india", max_results: int = 10) -> list[dict]:
    """
    Scrape Naukri.com public job search results.
    URL: https://www.naukri.com/{query-slug}-jobs-in-{location}
    """
    jobs = []
    slug     = query.lower().replace(" ", "-")
    loc_slug = location.lower().replace(" ", "-")
    url = f"https://www.naukri.com/{slug}-jobs-in-{loc_slug}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "lxml")

        cards = soup.select("article.jobTuple")[:max_results]
        if not cards:
            # Try alternate selector used in newer Naukri layouts
            cards = soup.select("div.list li.jobTupleHeader")[:max_results]

        for card in cards:
            title_el   = card.select_one("a.title")
            company_el = card.select_one("a.subTitle") or card.select_one("span.subTitle")
            location_el = card.select_one("li.location span") or card.select_one("span.location")
            exp_el      = card.select_one("li.experience span") or card.select_one("span.expwdth")
            link        = title_el["href"] if title_el and title_el.get("href") else url

            if not title_el:
                continue

            jobs.append({
                "source":      "Naukri",
                "title":       title_el.get_text(strip=True),
                "company":     company_el.get_text(strip=True) if company_el else "N/A",
                "location":    location_el.get_text(strip=True) if location_el else location,
                "experience":  exp_el.get_text(strip=True) if exp_el else "",
                "link":        link,
                "posted":      "",
                "description": "",
            })
    except Exception as exc:
        print(f"[Naukri] Scrape error: {exc}")

    return jobs


# ── Combined search ──────────────────────────────────────────────────────────

def search_all_jobs(query: str, location: str = "India", max_per_source: int = 10) -> list[dict]:
    """
    Search LinkedIn and Naukri in sequence and return combined results.
    A short delay between requests avoids rate limiting.
    """
    print(f"[Scraper] Searching LinkedIn for: {query!r} in {location!r}")
    linkedin_jobs = search_linkedin(query, location, max_per_source)
    time.sleep(1)

    print(f"[Scraper] Searching Naukri for: {query!r} in {location!r}")
    naukri_jobs = search_naukri(query, location, max_per_source)

    all_jobs = linkedin_jobs + naukri_jobs
    print(f"[Scraper] Total jobs found: {len(all_jobs)}")
    return all_jobs
