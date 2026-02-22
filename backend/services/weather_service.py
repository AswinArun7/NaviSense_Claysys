"""
weather_service.py — Real weather integration using Open-Meteo.

Free, no API key required.
Uses Open-Meteo geocoding + forecast APIs.
"""

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)
TIMEOUT = 8


def get_weather(destination: str, date: str) -> dict:
    """
    Fetch weather forecast for a destination and date.

    Args:
        destination: City name (e.g. "Goa")
        date:        ISO date string (YYYY-MM-DD)

    Returns:
        dict with temperature, condition, and recommendation.
        Empty dict on failure.
    """
    coords = _geocode(destination)
    if not coords:
        return {}

    forecast = _fetch_forecast(coords["lat"], coords["lon"], date)
    if not forecast:
        return {}

    return {
        "destination": destination,
        "date":        date,
        "temp_max_c":  forecast.get("temperature_2m_max"),
        "temp_min_c":  forecast.get("temperature_2m_min"),
        "rain_mm":     forecast.get("precipitation_sum"),
        "condition":   _describe(forecast),
        "tip":         _tip(forecast),
    }


def _geocode(destination: str) -> Optional[dict]:
    """Resolve destination name to lat/lon via Open-Meteo geocoding."""
    try:
        resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": destination, "count": 1, "language": "en"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            logger.warning(f"No geocoding results for: {destination}")
            return None
        return {"lat": results[0]["latitude"], "lon": results[0]["longitude"]}
    except Exception as e:
        logger.warning(f"Geocoding failed for {destination}: {e}")
        return None


def _fetch_forecast(lat: float, lon: float, date: str) -> Optional[dict]:
    """Fetch daily forecast data for a specific date."""
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude":       lat,
                "longitude":      lon,
                "daily":          "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "start_date":     date,
                "end_date":       date,
                "timezone":       "auto",
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        daily = resp.json().get("daily", {})

        # Extract the first (and only) day
        return {k: v[0] if isinstance(v, list) and v else None for k, v in daily.items()}
    except Exception as e:
        logger.warning(f"Forecast fetch failed ({lat},{lon},{date}): {e}")
        return None


def _describe(forecast: dict) -> str:
    """Map WMO weather code to a human-readable condition string."""
    code = forecast.get("weathercode", 0)
    if code == 0:
        return "Clear sky"
    if code in [1, 2, 3]:
        return "Partly cloudy"
    if code in [45, 48]:
        return "Foggy"
    if code in range(51, 68):
        return "Rainy"
    if code in range(71, 78):
        return "Snowy"
    if code in range(80, 83):
        return "Showers"
    if code in range(95, 100):
        return "Thunderstorms"
    return "Mixed conditions"


def _tip(forecast: dict) -> str:
    """Generate a packing/planning tip from forecast data."""
    rain = forecast.get("precipitation_sum") or 0
    temp = forecast.get("temperature_2m_max") or 25
    code = forecast.get("weathercode", 0)

    if rain > 10:
        return "Heavy rain expected — carry a waterproof jacket and umbrella."
    if rain > 2:
        return "Light rain likely — a compact umbrella is recommended."
    if code in range(95, 100):
        return "Thunderstorms possible — plan indoor activities as backup."
    if temp > 35:
        return "Very hot day — stay hydrated and avoid midday sun."
    if temp > 28:
        return "Warm and sunny — light clothing, sunscreen essential."
    if temp < 15:
        return "Cool temperatures — bring a jacket for evenings."
    return "Pleasant weather — great day for outdoor activities."
