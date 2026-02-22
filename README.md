# Navisense — Context-Aware AI Travel Planner

A modular AI-powered travel planner that combines live destination intelligence with Gemini AI to generate personalized itineraries.

## Project Structure

```
Navisense/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # API keys & settings
│   ├── models/
│   │   └── request_models.py   # Pydantic request models
│   ├── services/
│   │   ├── scraper.py          # Wikipedia scraping
│   │   ├── gemini_service.py   # Gemini AI integration
│   │   ├── logic_service.py    # Season & budget logic
│   │   └── weather_service.py  # Weather API (placeholder)
│   ├── utils/
│   │   ├── cache.py            # JSON file caching (7-day TTL)
│   │   └── helpers.py          # Shared utilities
│   ├── data/                   # Cached itinerary JSON files
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── README.md
```

## Setup

```bash
# 1. Add your Gemini API key
copy backend\.env.example backend\.env
# Edit .env → set GEMINI_API_KEY

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Start the server (run from backend/ directory)
cd backend
uvicorn main:app --reload
```

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/generate-plan` | Generate travel itinerary |

Interactive docs: **http://localhost:8000/docs**

## Tech Stack

- **Frontend**: HTML + CSS + Vanilla JS
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini API
- **Scraping**: requests + BeautifulSoup (Wikipedia)
- **Caching**: JSON files with 7-day TTL
