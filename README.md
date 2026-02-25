# Navisense — Context-Aware AI Travel Planner

## Overview
Navisense is a full-stack travel planning application that generates structured, customizable itineraries based on user preferences, budget constraints, group size, seasonal timing, and live weather conditions.

The system combines deterministic backend logic with structured LLM generation to produce realistic and context-aware travel plans.

## Problem Statement
Many automated travel planners struggle with:
- Providing generic, hallucinated itineraries
- Ignoring real-world group sizes and actual per-person budget distribution
- Failing to adapt to hyper-local seasonality or live weather
- Offering no interactive modification options after generation
- Relying heavily on brittle booking APIs or static templates

**Navisense solves these issues by:**
- Grounding itinerary generation in scraped real-world data
- Injecting live weather forecasts into the planning context
- Computing strict per-person budget constraints prior to AI generation
- Allowing instant, interactive activity swapping directly on the frontend
- Designing the architecture with graceful failovers to ensure reliability

---

## Key Features

### 1. Multi-Source Data Grounding
Destination context is collected from multiple structured sources:
- **Wikivoyage:** Extracts See/Do/Eat recommendations and local tips.
- **Wikipedia:** Acts as a fallback for core attractions and historical context.
- **Incredible India:** Specialized routing for Indian destinations to pull cultural enrichment.
*Note: Each scraper runs with strict timeouts. Graceful degradation ensures failures in any single source never break the parsing pipeline.*

### 2. Group-Aware Budget Engine
The system ensures financial consistency:
- Accepts a total group budget and specific group size (e.g., Solo, Couple, Family).
- Calculates a strict `per_person_per_day` constraint.
- Feeds exact financial constraints into the AI to ground pricing suggestions.
- Renders an itemized breakdown of group totals and per-person splits locally.

### 3. Seasonal & Location-Aware Planning
Dynamic contextualization based on travel dates:
- Identifies the exact season (e.g., Spring, Winter) and cross-references it with the destination.
- Injects specific insights (e.g., "Winter in Manali = Peak Snow Season", not just generic "Off-Season" assumptions).

### 4. Live Weather Integration
Powered by Open-Meteo:
- Resolves destination geodata to fetch the live 7-day forecast.
- Displays actual temperature and field conditions on the UI.
- Injects weather context into the AI prompt to enforce climate-appropriate activity and packing suggestions.

### 5. Transport Intelligence Layer
Instead of fragile, rate-limited flight-scraping APIs, Navisense uses deterministic routing logic:
- Recommends the optimal travel mode (Flight / Train / Road) based on origin/destination pairs.
- Identifies the nearest airport and major railway station.
- Generates a deep-linked Google Maps route for immediate navigation logic.

### 6. Interactive Activity Modification (Local Customization)
The AI schema forces the generation of 3 distinct alternatives for every single time slot. 
Users can click "Modify" on the frontend to instantly swap activities without triggering expensive or slow backend regeneration calls, strictly maintaining the overall budget profile.

---

## Solution Approach

Navisense follows a layered architecture:

1. **Input Validation Layer**  
   All user inputs are validated using Pydantic models before processing.

2. **Context Aggregation Layer**  
   Destination data is collected from Wikivoyage, Wikipedia, and Incredible India with timeout protection.

3. **Deterministic Logic Layer**  
   Budget distribution, group size handling, seasonal classification, and transport logic are computed using standard Python logic.

4. **Enrichment Layer**  
   Live weather data is retrieved and injected into the planning context.

5. **Structured Generation Layer**  
   A schema-enforced prompt is sent to Gemini to generate a strictly formatted JSON itinerary.

6. **Local Customization Layer**  
   Alternative activities are generated upfront to allow instant frontend modifications without additional API calls.

---

## Architecture

The frontend sends validated user inputs to the FastAPI backend.  
The backend orchestrates scraping, weather retrieval, deterministic computations, caching, and structured LLM generation before returning a finalized itinerary payload.

### Backend Modules
```
backend/
├── main.py                   # FastAPI orchestrator and routing
├── config.py                 # Environment variables
├── models/request_models.py  # Strict Pydantic types
├── services/
│   ├── scraper.py            # Timeout-enforced BeautifulSoup scraping
│   ├── gemini_service.py     # Prompt engineering & strict schema enforcement
│   ├── weather_service.py    # Open-Meteo integration
│   └── logic_service.py      # Deterministic budget/season computations
└── utils/
    ├── cache.py              # TTL JSON cache
    └── helpers.py            # Deduplication formatting
```

### Frontend Modules
```
frontend/
├── index.html       # Hero, wizard, loader, and itinerary result view
├── style.css        # Dependency-free dark mode design system
└── app.js           # API integration, wizard logic, and instant UI modification
```

---

## Technical Design Principles
- **Strict Validation:** Pydantic models reject malformed inputs before processing.
- **Enforced JSON Schemas:** The AI is strictly prompted to return parseable JSON, never raw markdown or code fences.
- **Graceful Degradation:** Scraper and API failures log errors but do not halt itinerary generation.
- **Caching:** 7-day TTL caching to reduce redundant API usage. Errors are *never* cached.
- **Dependency-Free Frontend:** Zero framework bloat (HTML, CSS, Vanilla JS).

## Technologies Used
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3, FastAPI, Pydantic, Uvicorn
- **Data Gathering:** Requests, BeautifulSoup4, Open-Meteo API
- **AI/LLM Engine:** Google Gemini 2.5 Flash

---

## How to Run Locally

1. **Clone the repository and prepare backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

3. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be available at `http://localhost:8000`*

4. **Launch Frontend:**
   Open `frontend/index.html` directly in any modern web browser.

---

## Hosted Version
Frontend: `<Vercel URL>` (Update after deployment)  
Backend: `<Render URL>` (Update after deployment)  
*Note: The first request may take ~20–30 seconds due to free-tier cloud cold starts.*

---

## Design Decision Tradeoffs
- **No Booking APIs:** Deliberately excluded to avoid anti-bot blocks, rate limits, and fragile dependencies during hackathon evaluation.
- **Deterministic vs AI:** Mathematics (budget per person) and hard data (weather/scraped arrays) are handled by standard Python logic. The AI is *only* used for reasoning and formatting, significantly reducing hallucination risk.
- **Local State Swapping:** Emitting alternatives in the initial payload increases the first-load payload size slightly, but enables 0ms latency for user modifications.

## Future Improvements
- Migration to Redis/PostgreSQL for persistent, distributed caching.
- Integration of a Geolocation Matrix API for accurate distance/drive-time estimation between daily activities.
- Hotel/Accommodation specific deep-linking parameters.
- Serverless deployment (Vercel for Frontend, Render/Railway for Backend).

---
*Designed with reliability, structured reasoning, and system stability in mind.*
