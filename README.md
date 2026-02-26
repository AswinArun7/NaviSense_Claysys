# Navisense — Context-Aware AI Travel Planner

## Overview

Navisense is a full-stack travel planning application that generates structured, customizable itineraries based on:

* User preferences
* Budget constraints
* Group size
* Seasonal timing
* Live weather conditions

The system combines deterministic backend logic with structured LLM generation to produce realistic, grounded, and context-aware travel plans.

---

## Problem Statement

Many automated travel planners struggle with:

* Providing generic, hallucinated itineraries
* Ignoring real-world group sizes and per-person budget distribution
* Failing to adapt to hyper-local seasonality or live weather
* Offering no interactive modification options after generation
* Relying heavily on brittle booking APIs or static templates

### Navisense solves these issues by:

* Grounding itinerary generation in scraped real-world data
* Injecting live weather forecasts into the planning context
* Computing strict per-person budget constraints prior to AI generation
* Allowing instant, interactive activity swapping directly on the frontend
* Designing the architecture with graceful failovers for reliability

---

## Key Features

### 1. Multi-Source Data Grounding

Destination context is collected from multiple sources:

* **Wikivoyage** – Extracts structured See/Do/Eat recommendations
* **Wikipedia** – Fallback for core attractions and background context
* **Incredible India** – Specialized routing for Indian destinations

Each scraper runs with strict timeouts. If any source fails, the system degrades gracefully without breaking itinerary generation.

---

### 2. Group-Aware Budget Engine

The system enforces financial realism:

* Accepts total group budget
* Maps group size (Solo, Couple, Family, etc.)
* Computes strict `per_person_per_day` constraint
* Feeds precise budget boundaries into the AI
* Renders itemized breakdown of accommodation, food, transport, and activities

---

### 3. Seasonal & Location-Aware Planning

* Detects season from travel dates
* Cross-references with destination context
* Injects dynamic seasonal insight (e.g., “Winter in Manali = Peak Snow Season”)
* Provides contextual travel tips

---

### 4. Live Weather Integration

Powered by Open-Meteo:

* Geocodes destination
* Fetches 7-day forecast
* Displays temperature and conditions
* Injects weather into AI prompt for climate-aware suggestions

---

### 5. Transport Intelligence Layer

Instead of fragile booking APIs, Navisense uses deterministic logic:

* Recommends optimal travel mode (Flight / Train / Road)
* Identifies nearest airport and railway station
* Provides route intelligence and connectivity explanation

---

### 6. Interactive Activity Modification

Each itinerary activity includes 3 structured alternatives.

Users can:

* Click “Modify”
* View alternatives
* Swap instantly
* Maintain budget consistency
* Avoid backend regeneration

This ensures zero-latency customization.

---

## Solution Approach

Navisense follows a layered architecture:

1. **Input Validation Layer**
   Pydantic models validate all incoming requests.

2. **Context Aggregation Layer**
   Scrapers gather structured destination data.

3. **Deterministic Logic Layer**
   Budget, season, and group constraints are computed in Python.

4. **Weather Enrichment Layer**
   Live forecast injected into planning context.

5. **Structured Generation Layer**
   Schema-enforced prompt sent to Gemini.

6. **Local Customization Layer**
   Alternatives generated upfront for instant UI swapping.

---

## System Architecture

Frontend → FastAPI Backend → Cache → Scraper + Weather → Gemini → Structured JSON → Frontend Rendering

---

### Backend Structure

```
backend/
├── main.py                   # FastAPI orchestrator
├── config.py                 # Environment configuration
├── models/request_models.py  # Pydantic validation
├── services/
│   ├── scraper.py            # Multi-source scraping engine
│   ├── gemini_service.py     # Prompt + Gemini integration
│   ├── weather_service.py    # Open-Meteo integration
│   └── logic_service.py      # Budget & seasonal computations
└── utils/
    ├── cache.py              # JSON TTL cache (7 days)
    └── helpers.py            # Deduplication & formatting helpers
```

---

### Frontend Structure

```
frontend/
├── index.html       # Wizard + results UI
├── style.css        # Dark theme design system
└── app.js           # API integration + modification logic
```

---

## Technical Design Principles

* Strict validation via Pydantic
* Enforced JSON schema from AI (no markdown responses)
* Graceful degradation on scraper failures
* 7-day TTL caching (errors never cached)
* Dependency-free frontend (Vanilla JS)
* Deterministic logic separated from AI reasoning

---

## Technologies Used

Frontend:

* HTML5
* CSS3
* Vanilla JavaScript

Backend:

* Python 3.11
* FastAPI
* Pydantic
* Uvicorn

Data:

* Requests
* BeautifulSoup4
* Open-Meteo API

AI:

* Google Gemini 2.5 Flash

Deployment:

* Vercel (Frontend)
* Render (Backend)

---

## Hosted Version

Live Frontend:
[https://navi-sense-claysys.vercel.app](https://navi-sense-claysys.vercel.app)

Backend API:
[https://navisense-claysys.onrender.com](https://navisense-claysys.onrender.com)

Swagger API Documentation:
[https://navisense-claysys.onrender.com/docs](https://navisense-claysys.onrender.com/docs)

Note: First request may take 20–30 seconds due to free-tier cold start.

---

## How to Test (Hosted)

1. Open the frontend URL.
2. Fill trip details.
3. Click “Generate”.
4. Wait for response (cold start may apply).
5. Use “Modify” button to swap activities instantly.
6. Use Swagger UI for direct backend testing if required.

---

## How to Run Locally

### 1. Setup Backend

```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file inside `backend/`:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### 3. Run Backend

```
uvicorn main:app --reload
```

Backend runs at:
[http://localhost:8000](http://localhost:8000)

Swagger available at:
[http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run Frontend

Open:

```
frontend/index.html
```

in a browser.

---

## Design Tradeoffs

* No direct booking APIs (avoids anti-bot and rate limits)
* AI used only for structured reasoning, not raw calculations
* Deterministic financial logic handled outside LLM
* Slightly larger payload to enable instant modification

---

## Future Improvements

* Persistent cache (Redis/PostgreSQL)
* Distance matrix API integration
* Accommodation deep linking
* Train/bus route intelligence expansion
* Production-grade CI/CD

---

## Conclusion

Navisense demonstrates how deterministic backend logic and structured AI generation can be combined to produce reliable, context-aware, and customizable travel itineraries while maintaining system stability and performance.
