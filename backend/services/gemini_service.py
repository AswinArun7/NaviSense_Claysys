"""
gemini_service.py — Gemini API integration using the new google-genai SDK.

Builds a structured prompt from user context and destination data,
calls Gemini, and returns a parsed itinerary dict.
"""

import json
import logging
from typing import Optional

import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_itinerary(context: dict, destination_data: dict, request: dict, weather: dict = None) -> dict:
    """
    Generate a day-by-day travel itinerary using the Gemini API.

    Args:
        context:          Output of logic_service.build_context()
        destination_data: Output of scraper.scrape_destination()
        request:          Raw request dict
        weather:          Output of weather_service.get_weather() (optional)

    Returns:
        Parsed itinerary dict, or a fallback dict on failure.
    """

    prompt   = _build_prompt(context, destination_data, request, weather or {})
    response = _call_gemini(prompt)

    if response is None:
        return _fallback(request, context)

    return _parse(response)


def _build_prompt(context: dict, data: dict, request: dict, weather: dict = None) -> str:
    """Assemble the Gemini prompt from context, destination data, and weather."""
    weather = weather or {}
    rates       = context["daily_rates"]
    attractions = "\n".join(f"- {a}" for a in data.get("attractions", [])[:8]) or "Not available"
    activities  = "\n".join(f"- {a}" for a in data.get("activities",  [])[:6]) or ""
    food        = "\n".join(f"- {f}" for f in data.get("food",        [])[:6]) or "Not available"

    weather_section = ""
    if weather:
        weather_section = f"""
WEATHER FORECAST (for Day 1 — {request.get('start_date', '')})
- Condition:   {weather.get('condition', 'Unknown')}
- Max Temp:    {weather.get('temp_max_c', '?')}°C
- Min Temp:    {weather.get('temp_min_c', '?')}°C
- Rain:        {weather.get('rain_mm', 0)} mm
- Packing tip: {weather.get('tip', '')}
Use this to suggest weather-appropriate activities and clothing notes."""

    return f"""
You are an expert travel planner. Generate a {context['days']}-day itinerary for {request['to']}.

TRIP DETAILS
- From:     {request.get('from_location', request.get('from', ''))}
- To:       {request['to']}
- Duration: {context['days']} days / {context['nights']} nights
- Season:   {context['season']}
- Budget:   {context['budget_tier']} tier — ₹{context['per_person_per_day']:,}/person/day · ₹{context['total_budget_inr']:,} total for {context['group_count']} {context['group_label']}(s) over {context['days']} days
- Purposes: {', '.join(context['purposes']) or 'general sightseeing'}
- Pace:     {context['pace']}
- Group:    {request.get('group_size', 'couple')}
{f"- Checkpoints: {', '.join(context['checkpoints'])}" if context['checkpoints'] else ""}
{f"- Special needs: {request['special_needs']}" if request.get('special_needs') else ""}
{weather_section}
DESTINATION INTELLIGENCE
Summary: {data.get('summary', '')}

Attractions:
{attractions}
{f"Activities:{chr(10)}{activities}" if activities else ""}
Local Food:
{food}

INSTRUCTIONS
- Match activities to the stated purposes and pace
- Stay within the budget tier
- Include one local food experience per day
- Use the destination data above as factual grounding
- If weather data is provided, suggest weather-appropriate activities
- For EACH activity provide exactly 3 alternatives drawn from the destination data (different category or cost tier)

Return ONLY valid JSON. No markdown. No code fences. No commentary. Just the raw JSON object:
{{
  "destination": "{request['to']}",
  "days": [
    {{
      "day": 1,
      "theme": "string",
      "activities": [
        {{
          "time": "09:00",
          "period": "morning",
          "title": "string",
          "description": "string",
          "category": "sightseeing | food | adventure | culture | relaxation",
          "cost_inr": 0,
          "alternatives": [
            {{
              "title": "string",
              "description": "string",
              "category": "sightseeing | food | adventure | culture | relaxation",
              "cost_inr": 0
            }},
            {{
              "title": "string",
              "description": "string",
              "category": "sightseeing | food | adventure | culture | relaxation",
              "cost_inr": 0
            }},
            {{
              "title": "string",
              "description": "string",
              "category": "sightseeing | food | adventure | culture | relaxation",
              "cost_inr": 0
            }}
          ]
        }}
      ]
    }}
  ],
  "budget_summary": {{
    "accommodation_inr": 0,
    "food_inr": 0,
    "transport_inr": 0,
    "activities_inr": 0,
    "total_inr": 0
  }},
  "seasonal_insight": {{
    "badge_text": "❄️ Winter — Peak Snow Season",
    "badge_color": "#06b6d4 | #ef4444 | #f59e0b | #f97316",
    "description": "Short explanation of why this season is good/bad for this specific destination.",
    "tips": ["tip1", "tip2", "tip3"]
  }},
  "transport_intelligence": {{
    "recommended_mode": "Flight | Train | Bus | Car",
    "approx_reason": "Flight is best for the 1500km distance from {request.get('from', '')} to {request['to']}",
    "nearest_airport": "Name of nearest airport and distance",
    "major_railway_station": "Name of major railway station and distance",
    "road_connectivity": "Notes on highway access or bus routes"
  }},
  "tips": ["tip1", "tip2", "tip3"]
}}
""".strip()


def _call_gemini(prompt: str) -> Optional[str]:
    """Send prompt to Gemini using the google-generativeai SDK."""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        logger.info("Gemini responded successfully.")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini call failed: {e}")
        return None


def _parse(raw: str) -> dict:
    """
    Parse Gemini's text response to a dict.
    Strips markdown code fences if present.
    """
    text = raw
    if text.startswith("```"):
        lines = text.splitlines()
        text  = "\n".join(lines[1:-1]).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error("Failed to parse Gemini response as JSON.")
        return {"error": "Invalid AI response", "raw": raw[:300]}


def _fallback(request: dict, context: dict) -> dict:
    """Return a minimal valid response when Gemini is unavailable."""
    return {
        "destination": request.get("to", ""),
        "error":       "AI generation unavailable. Check GEMINI_API_KEY.",
        "days": [
            {
                "day": i + 1,
                "theme": f"Day {i + 1}",
                "activities": [{
                    "time": "09:00",
                    "period": "morning",
                    "title": "Free exploration",
                    "description": "Explore the destination at your own pace.",
                    "category": "sightseeing",
                    "cost_inr": 0,
                }],
            }
            for i in range(context["days"])
        ],
        "budget_summary": {},
        "tips": [],
    }
