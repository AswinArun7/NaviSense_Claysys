"""
helpers.py — Common utility functions shared across the backend.
"""

from datetime import datetime


def format_inr(amount: int) -> str:
    """Format an integer as an Indian Rupee string. e.g. 15000 → '₹15,000'"""
    return f"₹{amount:,}"


def today_iso() -> str:
    """Return today's date as an ISO string (YYYY-MM-DD)."""
    return datetime.today().strftime("%Y-%m-%d")


def truncate(text: str, max_length: int = 140) -> str:
    """Truncate a string to max_length characters."""
    return text[:max_length] if len(text) > max_length else text


def build_cache_key(*parts: str) -> str:
    """
    Build a safe, consistent cache key from multiple string parts.

    Example: build_cache_key("Paris France", "moderate", "7") → "paris_france_moderate_7"
    """
    joined = "_".join(str(p) for p in parts)
    return "".join(c if c.isalnum() or c == "_" else "_" for c in joined.lower())


def dedupe_limit(items: list, limit: int = 10) -> list:
    """
    Deduplicate a list of strings (case-insensitive) and cap at limit items.

    Safely handles None and whitespace-only entries.
    """
    seen   = set()
    result = []
    for item in items:
        if not item:
            continue
        clean = item.strip()
        key   = clean.lower()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
        if len(result) >= limit:
            break
    return result
