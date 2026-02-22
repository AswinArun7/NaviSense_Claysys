"""
config.py — Application settings loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL:   str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    import logging
    logging.getLogger(__name__).warning("GEMINI_API_KEY is not set.")
