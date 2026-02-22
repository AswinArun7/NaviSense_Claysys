"""
request_models.py — Pydantic request models for the API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TravelRequest(BaseModel):
    from_location: str = Field(..., alias="from", min_length=2)
    to: str            = Field(..., min_length=2)
    start_date: str    = Field(...)
    nights: int        = Field(..., ge=1, le=90)
    budget: str        = Field(...)
    purposes: List[str]              = Field(default=[])
    pace: Optional[str]              = Field(default="moderate")
    checkpoints: Optional[List[str]] = Field(default=[])
    accommodation: Optional[str]     = Field(default=None)
    group_size: Optional[str]        = Field(default="couple")
    special_needs: Optional[str]     = Field(default=None)

    class Config:
        populate_by_name = True
