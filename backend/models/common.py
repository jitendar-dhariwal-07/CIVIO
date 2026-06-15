"""
Common Pydantic models shared across the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Location(BaseModel):
    """Geographic location with latitude/longitude and address components."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    state: str = Field(..., min_length=1, max_length=100, description="State name")
    district: str = Field(..., min_length=1, max_length=100, description="District name")
    city: Optional[str] = Field(None, max_length=100, description="City name")
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$", description="6-digit PIN code")
    address: Optional[str] = Field(None, max_length=500, description="Full street address")


class Translation(BaseModel):
    """A translated text block."""

    original_text: str
    translated_text: str
    source_language: str = Field(..., min_length=2, max_length=5)
    target_language: str = Field(..., min_length=2, max_length=5)


class PaginatedResponse(BaseModel, Generic[T]):
    """Wrapper for paginated list responses."""

    items: List[T]
    total: int = Field(..., ge=0, description="Total number of items matching the query")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = False
    has_previous: bool = False


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""

    success: bool = True
    message: str = "OK"
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheck(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
    database: str = "connected"
    ai_service: str = "available"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StatsOverview(BaseModel):
    """High-level statistics for the dashboard."""

    total_users: int = 0
    total_complaints: int = 0
    total_schemes: int = 0
    complaints_resolved: int = 0
    complaints_pending: int = 0
    average_resolution_days: float = 0.0
    active_hotspots: int = 0
    departments_count: int = 0


class GeoPoint(BaseModel):
    """Lightweight geographic point for map rendering."""

    lat: float
    lng: float
    label: Optional[str] = None
    count: Optional[int] = None
    category: Optional[str] = None


class DateRange(BaseModel):
    """Date range filter."""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
