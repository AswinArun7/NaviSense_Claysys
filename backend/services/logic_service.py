"""
logic_service.py — Season detection and budget context logic.
"""

from datetime import datetime

SEASONS = {
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Autumn": [9, 10, 11],
    "Winter": [12, 1, 2],
}

BUDGET_RATES = {
    "budget":   {"hotel": 2500,  "food": 1500, "transport": 1200, "activities": 1000},
    "moderate": {"hotel": 7500,  "food": 4000, "transport": 2000, "activities": 2500},
    "premium":  {"hotel": 16000, "food": 8000, "transport": 4000, "activities": 6000},
    "luxury":   {"hotel": 37000, "food": 16000,"transport": 8000, "activities": 12000},
}


def build_context(request: dict) -> dict:
    """
    Build structured travel context from the validated request dict.

    Returns a flat context dict used by the prompt builder.
    """
    return {
        "season":      detect_season(request.get("start_date", "")),
        "budget_tier": request.get("budget", "moderate"),
        "daily_rates": BUDGET_RATES.get(request.get("budget", "moderate"), BUDGET_RATES["moderate"]),
        "nights":      request.get("nights", 5),
        "days":        request.get("nights", 5) + 1,
        "purposes":    request.get("purposes", []),
        "pace":        request.get("pace", "moderate"),
        "checkpoints": request.get("checkpoints", []),
    }


def detect_season(date_str: str) -> str:
    """
    Return season name for a given ISO date string (YYYY-MM-DD).
    Returns 'Unknown' if date is missing or invalid.
    """
    if not date_str:
        return "Unknown"
    try:
        month = datetime.strptime(date_str, "%Y-%m-%d").month
    except ValueError:
        return "Unknown"
    return next(
        (season for season, months in SEASONS.items() if month in months),
        "Unknown",
    )
