"""
scraper.py — Wikipedia destination scraper.

Accepts a destination name, scrapes the Wikipedia tourism section,
extracts attractions and food, returns a structured dictionary.
Unrelated sections (history, economy, politics, etc.) are excluded.
"""

import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from typing import Optional

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Navisense/1.0)",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 10

TOURISM_KEYWORDS = {
    "tourism", "attraction", "landmark", "sights", "culture",
    "cuisine", "food", "restaurant", "dining", "eat", "drink",
    "festival", "event", "park", "beach", "nature", "wildlife",
    "heritage", "museum", "architecture", "shopping", "market",
    "temple", "palace", "castle", "fort", "nightlife", "activities",
}

SKIP_SECTIONS = {
    "history", "economy", "demographics", "politics", "government",
    "education", "infrastructure", "media", "notable people", "sports",
    "sport", "twin towns", "sister cities", "see also", "references",
    "external links", "notes", "footnotes", "bibliography",
}

FOOD_KEYWORDS = {"cuisine", "food", "restaurant", "dining", "eat", "drink", "market"}


def scrape_destination(destination: str) -> dict:
    """
    Scrape Wikipedia for a destination and return structured travel data.

    Returns:
        {
            "destination": str,
            "summary":     str,
            "attractions": list[str],
            "food":        list[str],
        }
    """
    encoded = quote_plus(destination.replace(",", "").strip())

    return {
        "destination": destination,
        "summary":     _get_summary(encoded),
        "attractions": _get_sections(encoded, bucket="attractions"),
        "food":        _get_sections(encoded, bucket="food"),
    }


def _get_summary(encoded: str) -> str:
    """Fetch a 2-sentence overview from the Wikipedia REST API."""
    resp = _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}")
    if resp is None:
        return ""
    text  = resp.json().get("extract", "")
    parts = text.split(". ")
    return ". ".join(parts[:2]) + ("." if len(parts) > 1 else "")


def _get_sections(encoded: str, bucket: str) -> list:
    """
    Parse Wikipedia HTML and return items from tourism sections.

    Args:
        encoded: URL-encoded destination name.
        bucket:  "attractions" or "food".
    """
    resp = _get(f"https://en.wikipedia.org/wiki/{encoded}")
    if resp is None:
        return []

    soup    = BeautifulSoup(resp.text, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return []

    results       = []
    active_bucket = None

    for tag in content.find_all(["h2", "h3", "li", "p"]):
        if tag.name in ["h2", "h3"]:
            active_bucket = _classify_heading(tag.get_text(strip=True))
        elif tag.name in ["li", "p"] and active_bucket == bucket:
            text = tag.get_text(strip=True)
            if len(text) > 10 and len(results) < 8:
                results.append(text[:140])

    return results


def _classify_heading(heading_raw: str) -> Optional[str]:
    """
    Classify a section heading as 'food', 'attractions', or None (skip).
    """
    heading = heading_raw.lower().replace("[edit]", "").strip()

    if any(skip in heading for skip in SKIP_SECTIONS):
        return None
    if any(kw in heading for kw in FOOD_KEYWORDS):
        return "food"
    if any(kw in heading for kw in TOURISM_KEYWORDS):
        return "attractions"
    return None


def _get(url: str) -> Optional[requests.Response]:
    """Make a GET request. Returns None on any failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed ({url}): {e}")
        return None
