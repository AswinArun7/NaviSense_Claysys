"""
main.py — FastAPI application entry point.

Run from the backend/ directory:
    uvicorn main:app --reload
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.request_models import TravelRequest
from services.logic_service import build_context
from services.scraper import get_destination_data
from services.gemini_service import generate_itinerary
from services.weather_service import get_weather
from utils.cache import get_cached, set_cached
from utils.helpers import build_cache_key

logging.basicConfig(level=logging.INFO, format="%(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Navisense API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health():
    """Health check."""
    return {"status": "ok", "service": "Navisense API"}


@app.post("/generate-plan", tags=["Itinerary"])
def generate_plan(request: TravelRequest):
    """
    Generate a personalized travel itinerary.

    Flow:
    1. Build travel context (season, budget, duration)
    2. Check cache — return if hit
    3. Scrape destination data from Wikipedia
    4. Generate itinerary via Gemini API
    5. Cache result and return
    """
    destination = request.to.strip()
    cache_key   = build_cache_key(destination, request.budget, str(request.nights))

    cached = get_cached(cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_key}")
        return {**cached, "cached": True}

    context          = build_context(request.dict(by_alias=False))
    destination_data = get_destination_data(destination)
    weather          = get_weather(destination, request.start_date)

    if weather:
        logger.info(f"Weather: {weather.get('condition')} {weather.get('temp_max_c')}C")

    itinerary = generate_itinerary(context, destination_data, request.dict(by_alias=False), weather)

    # Only cache successful responses — never cache fallback/error results
    if itinerary.get("days") and not itinerary.get("error"):
        set_cached(cache_key, itinerary)

    return {**itinerary, "cached": False, "weather": weather}


@app.exception_handler(Exception)
def global_error_handler(request: Request, exc: Exception):
    logger.error(f"Error on {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"error": str(exc)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
