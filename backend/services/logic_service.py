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

# Per-person daily rates (INR) used when no total_budget is provided
BUDGET_RATES = {
    "budget":   {"hotel": 2500,  "food": 1500, "transport": 1200, "activities": 1000},
    "moderate": {"hotel": 7500,  "food": 4000, "transport": 2000, "activities": 2500},
    "premium":  {"hotel": 16000, "food": 8000, "transport": 4000, "activities": 6000},
    "luxury":   {"hotel": 37000, "food": 16000,"transport": 8000, "activities": 12000},
}

# Map group_size label → number of travellers
GROUP_COUNTS = {
    "solo":   1,
    "couple": 2,
    "small":  4,
    "medium": 8,
    "large":  12,
}


def build_context(request: dict) -> dict:
    """
    Build structured travel context from the validated request dict.

    Budget logic:
      - If total_budget is provided → divide by group_count and days
        to derive a per-person-per-day constraint for Gemini.
      - Otherwise → use tier daily rates multiplied by group_count
        to give Gemini the total group expense estimate.

    Returns a flat context dict used by the prompt builder.
    """
    days        = request.get("nights", 5) + 1
    budget_tier = request.get("budget", "moderate")
    tier_rates  = BUDGET_RATES.get(budget_tier, BUDGET_RATES["moderate"])
    group_label = request.get("group_size", "couple") or "couple"
    group_count = GROUP_COUNTS.get(group_label, 2)
    total_budget_input = request.get("total_budget")   # optional, full trip budget

    # ── Derive per-person-per-day budget ──────────────────────────────────
    if total_budget_input and total_budget_input > 0:
        # User gave an explicit total → back-calculate per person per day
        per_person_per_day = int(total_budget_input / group_count / days)
        total_budget_inr   = int(total_budget_input)
        budget_source      = "user_input"
    else:
        # No explicit total → estimate from tier rates
        per_person_per_day = sum(tier_rates.values())
        total_budget_inr   = per_person_per_day * group_count * days
        budget_source      = "tier_estimate"

    return {
        "season":             detect_season(request.get("start_date", "")),
        "budget_tier":        budget_tier,
        "daily_rates":        tier_rates,          # per-person tier rates (for prompt context)
        "per_person_per_day": per_person_per_day,  # actual per-person-per-day budget
        "total_budget_inr":   total_budget_inr,    # total for the whole group
        "group_count":        group_count,          # number of travellers
        "group_label":        group_label,
        "budget_source":      budget_source,
        "nights":             request.get("nights", 5),
        "days":               days,
        "purposes":           request.get("purposes", []),
        "pace":               request.get("pace", "moderate"),
        "checkpoints":        request.get("checkpoints", []),
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
