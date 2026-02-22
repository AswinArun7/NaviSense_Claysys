"""
cache.py — JSON file-based caching with TTL.
"""

import json
import os
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Store cached files in backend/data/
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TTL      = 60 * 60 * 24 * 7   # 7 days


def _path(key: str) -> str:
    """Return the file path for a given cache key."""
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in key)
    return os.path.join(DATA_DIR, f"{safe}.json")


def get_cached(key: str) -> Optional[dict]:
    """
    Load cached data for a key.

    Returns the data dict if found and within TTL, otherwise None.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _path(key)

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            entry = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Cache read error ({key}): {e}")
        return None

    if time.time() - entry.get("saved_at", 0) > TTL:
        os.remove(path)
        return None

    return entry.get("data")


def set_cached(key: str, data: dict) -> None:
    """Save data to cache under the given key."""
    os.makedirs(DATA_DIR, exist_ok=True)
    entry = {"saved_at": time.time(), "data": data}

    try:
        with open(_path(key), "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
    except OSError as e:
        logger.warning(f"Cache write error ({key}): {e}")
