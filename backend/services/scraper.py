"""
scraper.py — Multi-source destination data aggregator.

Sources:
  1. Wikipedia   — baseline facts and attractions (global)
  2. Wikivoyage  — travel-focused See/Do/Eat content (global)
  3. Incredible India — experiential enrichment (Indian destinations only)

All scrapers are timeout-controlled and fail silently.
The only function the backend should call is get_destination_data().
"""

import logging
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from utils.helpers import dedupe_limit

logger  = logging.getLogger(__name__)
HEADERS = {"User-Agent": "NavisenseBot/1.0 (travel planner research tool)"}

# Timeouts (seconds)
WIKI_TIMEOUT    = 3
VOYAGE_TIMEOUT  = 3
INDIA_TIMEOUT   = 2

# Indian destinations that trigger Incredible India scraping
INDIAN_STATES = {
    "goa", "kerala", "karnataka", "rajasthan", "tamil nadu",
    "maharashtra", "delhi", "new delhi", "himachal pradesh",
    "uttarakhand", "jammu", "kashmir", "punjab", "gujara",
    "andhra pradesh", "telangana", "west bengal", "odisha",
    "manali", "shimla", "dharamshala", "jaipur", "udaipur",
    "agra", "varanasi", "mumbai", "bangalore", "bengaluru",
    "hyderabad", "kolkata", "chennai", "kochi", "mysore",
    "rishikesh", "haridwar", "ooty", "coorg", "munnar",
}


# ──────────────────────────────────────────────
# Public entry point
# ──────────────────────────────────────────────

def get_destination_data(destination: str) -> dict:
    """
    Aggregate destination data from all available sources.

    This is the only function main.py should call.

    Args:
        destination: City or region name (e.g. "Goa", "Paris")

    Returns:
        Merged dict with keys: summary, attractions, activities, food
    """
    wiki_data   = {}
    voyage_data = {}
    india_data  = {}

    try:
        wiki_data = scrape_wikipedia(destination)
        logger.info(f"Wikipedia: {len(wiki_data.get('attractions', []))} attractions")
    except Exception as e:
        logger.warning(f"Wikipedia failed for {destination}: {e}")

    try:
        voyage_data = scrape_wikivoyage(destination)
        logger.info(f"Wikivoyage: {len(voyage_data.get('attractions', []))} attractions")
    except Exception as e:
        logger.warning(f"Wikivoyage failed for {destination}: {e}")

    if is_indian_destination(destination):
        try:
            india_data = scrape_incredible_india(destination)
            logger.info(f"Incredible India: {len(india_data.get('attractions', []))} items")
        except Exception as e:
            logger.warning(f"Incredible India failed for {destination}: {e}")

    return merge_destination_data(wiki_data, voyage_data, india_data)


# ──────────────────────────────────────────────
# Wikipedia scraper
# ──────────────────────────────────────────────

WIKI_TRAVEL_SECTIONS = {
    "tourism", "tourist", "attractions", "sights", "places of interest",
    "things to do", "recreation", "culture", "cuisine", "food", "restaurants",
    "shopping", "nightlife", "arts", "music", "festivals",
}

WIKI_SKIP_SECTIONS = {
    "history", "geography", "economy", "politics", "government",
    "demographics", "education", "infrastructure", "transport",
    "references", "see also", "external links", "notes", "further reading",
}


def scrape_wikipedia(destination: str) -> dict:
    """Scrape Wikipedia for destination attractions and food."""
    url  = f"https://en.wikipedia.org/wiki/{quote(destination.replace(' ', '_'))}"
    resp = requests.get(url, headers=HEADERS, timeout=WIKI_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    return {
        "summary":     _wiki_summary(soup),
        "attractions": _wiki_list_items(soup, WIKI_TRAVEL_SECTIONS - {"food", "cuisine", "restaurants"}),
        "activities":  [],
        "food":        _wiki_list_items(soup, {"food", "cuisine", "restaurants", "eat"}),
    }


def _wiki_summary(soup: BeautifulSoup) -> str:
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return ""
    for p in content.find_all("p", recursive=False):
        text = p.get_text(" ", strip=True)
        if len(text) > 80:
            return re.sub(r"\[\d+\]", "", text)[:400]
    return ""


def _wiki_list_items(soup: BeautifulSoup, target_sections: set) -> list:
    """Extract list items from headings whose text matches target_sections."""
    items = []
    for heading in soup.find_all(["h2", "h3"]):
        heading_text = heading.get_text(" ", strip=True).lower()
        if any(kw in heading_text for kw in target_sections):
            if any(kw in heading_text for kw in WIKI_SKIP_SECTIONS):
                continue
            for sib in heading.find_next_siblings():
                if sib.name in ["h2", "h3"]:
                    break
                if sib.name in ["ul", "ol"]:
                    for li in sib.find_all("li"):
                        text = li.get_text(" ", strip=True)
                        text = re.sub(r"\[\d+\]", "", text)
                        if 5 < len(text) < 120:
                            items.append(text)
    return items


# ──────────────────────────────────────────────
# Wikivoyage scraper
# ──────────────────────────────────────────────

VOYAGE_SEE_DO    = {"see", "do", "activities", "sights", "get around"}
VOYAGE_EAT       = {"eat", "drink", "food", "restaurants"}
VOYAGE_SUMMARY   = {"understand", "overview"}


def scrape_wikivoyage(destination: str) -> dict:
    """Scrape Wikivoyage for the See/Do/Eat sections."""
    url  = f"https://en.wikivoyage.org/wiki/{quote(destination.replace(' ', '_'))}"
    resp = requests.get(url, headers=HEADERS, timeout=VOYAGE_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    return {
        "summary":     _voyage_summary(soup),
        "attractions": _voyage_items(soup, VOYAGE_SEE_DO - {"activities"}),
        "activities":  _voyage_items(soup, {"do", "activities"}),
        "food":        _voyage_items(soup, VOYAGE_EAT),
    }


def _voyage_summary(soup: BeautifulSoup) -> str:
    for heading in soup.find_all(["h2", "h3"]):
        if heading.get_text(strip=True).lower() in VOYAGE_SUMMARY:
            for sib in heading.find_next_siblings():
                if sib.name in ["h2", "h3"]:
                    break
                if sib.name == "p":
                    text = sib.get_text(" ", strip=True)
                    if len(text) > 60:
                        return text[:400]
    # fallback: first paragraph in content
    for p in soup.select("#mw-content-text p"):
        t = p.get_text(" ", strip=True)
        if len(t) > 80:
            return t[:400]
    return ""


def _voyage_items(soup: BeautifulSoup, target_sections: set) -> list:
    """Extract listing names and descriptions from Wikivoyage sections."""
    items = []
    for heading in soup.find_all(["h2", "h3"]):
        if heading.get_text(strip=True).lower() in target_sections:
            for sib in heading.find_next_siblings():
                if sib.name in ["h2", "h3"]:
                    break
                # Wikivoyage uses dt for listing names
                for dt in sib.find_all("dt"):
                    name = dt.get_text(" ", strip=True)
                    if 2 < len(name) < 80:
                        items.append(name)
                # Also grab plain list items
                for li in sib.find_all("li"):
                    text = li.get_text(" ", strip=True)
                    if 5 < len(text) < 120:
                        items.append(text)
    return items


# ──────────────────────────────────────────────
# Incredible India scraper
# ──────────────────────────────────────────────

def scrape_incredible_india(destination: str) -> dict:
    """
    Scrape incredibleindia.org for experiential enrichment.
    Only triggered for Indian destinations.
    Timeout hard-capped at INDIA_TIMEOUT seconds.
    """
    slug = destination.lower().replace(" ", "-")
    url  = f"https://www.incredibleindia.gov.in/content/incredible-india/en/{slug}.html"

    resp = requests.get(url, headers=HEADERS, timeout=INDIA_TIMEOUT)
    resp.raise_for_status()

    soup  = BeautifulSoup(resp.text, "html.parser")
    items = []

    # Extract headings and list items from the main content area
    content = soup.select_one(".container main, main, article, .content")
    if not content:
        content = soup

    for tag in content.find_all(["h2", "h3", "h4", "li"]):
        text = tag.get_text(" ", strip=True)
        if 5 < len(text) < 120:
            items.append(text)

    return {
        "summary":     "",          # Incredible India prioritises experiential copy, skip summary
        "attractions": items[:10],
        "activities":  items[10:18],
        "food":        [],
    }


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def is_indian_destination(destination: str) -> bool:
    """Return True if the destination is a known Indian city/state."""
    return destination.strip().lower() in INDIAN_STATES


def merge_destination_data(wiki: dict, voyage: dict, india: dict) -> dict:
    """
    Merge data from all three sources with deduplication and token limits.

    Priority:
      summary    → Wikivoyage > Wikipedia
      attractions → Wikipedia + Wikivoyage + Incredible India (limit 12)
      activities  → Wikivoyage + Incredible India (limit 8)
      food        → Wikivoyage > Wikipedia + Incredible India (limit 8)
    """
    return {
        "summary": (
            voyage.get("summary")
            or wiki.get("summary")
            or ""
        ),
        "attractions": dedupe_limit(
            wiki.get("attractions",   [])
            + voyage.get("attractions", [])
            + india.get("attractions",  []),
            limit=12,
        ),
        "activities": dedupe_limit(
            voyage.get("activities", [])
            + india.get("activities",  []),
            limit=8,
        ),
        "food": dedupe_limit(
            voyage.get("food", [])
            + wiki.get("food",   [])
            + india.get("food",  []),
            limit=8,
        ),
    }
