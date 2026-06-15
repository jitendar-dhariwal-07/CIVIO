"""
Pydantic models for Complaint / Grievance domain objects.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ComplaintStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    IN_PROGRESS = "in_progress"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    CLOSED = "closed"


class ComplaintPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplaintCategory(str, Enum):
    ROADS = "roads"
    WATER_SUPPLY = "water_supply"
    ELECTRICITY = "electricity"
    SANITATION = "sanitation"
    PUBLIC_TRANSPORT = "public_transport"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    POLLUTION = "pollution"
    CORRUPTION = "corruption"
    PUBLIC_SAFETY = "public_safety"
    HOUSING = "housing"
    FOOD_SAFETY = "food_safety"
    TELECOM = "telecom"
    BANKING = "banking"
    GOVERNMENT_SERVICE = "government_service"
    OTHER = "other"


class ComplaintCreate(BaseModel):
    """Payload to submit a new complaint."""

    title: str = Field(..., min_length=5, max_length=300, description="Brief title")
    description: str = Field(..., min_length=20, max_length=5000, description="Detailed description")
    category: Optional[ComplaintCategory] = Field(None, description="If omitted, AI will classify")
    image_url: Optional[str] = Field(None, max_length=500, description="URL or base64 of a supporting image")

    # Location
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    state: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")
    address: Optional[str] = Field(None, max_length=500)

    language: str = Field("en", min_length=2, max_length=5, description="Language of the complaint text")


class ComplaintResponse(BaseModel):
    """Full complaint details returned from API."""

    id: str
    tracking_id: str
    title: str
    description: str
    category: ComplaintCategory
    priority: ComplaintPriority
    status: ComplaintStatus
    image_url: Optional[str] = None

    # Location
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state: str
    district: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    address: Optional[str] = None

    # AI-generated
    ai_summary: Optional[str] = None
    ai_category_confidence: Optional[float] = None
    sentiment_score: Optional[float] = None

    # Assignment
    department_id: Optional[str] = None
    department_name: Optional[str] = None
    assigned_to: Optional[str] = None

    # Metadata
    user_id: str
    user_name: Optional[str] = None
    language: str = "en"
    duplicate_of: Optional[str] = None
    upvotes: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ComplaintUpdate(BaseModel):
    """Fields that can be updated on an existing complaint (by admin / department)."""

    status: Optional[ComplaintStatus] = None
    priority: Optional[ComplaintPriority] = None
    category: Optional[ComplaintCategory] = None
    department_id: Optional[str] = None
    assigned_to: Optional[str] = None
    admin_remarks: Optional[str] = Field(None, max_length=2000)


class ComplaintFilter(BaseModel):
    """Query parameters for listing / searching complaints."""

    status: Optional[ComplaintStatus] = None
    priority: Optional[ComplaintPriority] = None
    category: Optional[ComplaintCategory] = None
    state: Optional[str] = None
    district: Optional[str] = None
    department_id: Optional[str] = None
    user_id: Optional[str] = None
    search: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sort_by: str = Field("created_at", description="Field to sort by")
    sort_order: str = Field("desc", pattern=r"^(asc|desc)$")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ComplaintClassification(BaseModel):
    """AI classification output."""

    category: ComplaintCategory
    confidence: float = Field(..., ge=0, le=1)
    sub_category: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    reasoning: str = ""


class ComplaintSummary(BaseModel):
    """AI-generated summary of a complaint."""

    original_text: str
    summary: str
    key_issues: List[str] = Field(default_factory=list)
    affected_area: Optional[str] = None
    urgency_indicators: List[str] = Field(default_factory=list)


class DuplicateResult(BaseModel):
    """Result from duplicate detection."""

    complaint_id: str
    tracking_id: str
    title: str
    similarity_score: float = Field(..., ge=0, le=1)
    category: ComplaintCategory
    status: ComplaintStatus


class Hotspot(BaseModel):
    """A detected complaint hotspot cluster."""

    cluster_id: int
    latitude: float
    longitude: float
    complaint_count: int
    radius_km: float
    primary_category: ComplaintCategory
    categories: Dict[str, int] = Field(default_factory=dict)
    state: Optional[str] = None
    district: Optional[str] = None
    severity_score: float = Field(0, ge=0, le=100)
    complaints: List[str] = Field(default_factory=list, description="List of complaint IDs in this hotspot")


class ComplaintStats(BaseModel):
    """Aggregate complaint statistics."""

    total: int = 0
    by_status: Dict[str, int] = Field(default_factory=dict)
    by_priority: Dict[str, int] = Field(default_factory=dict)
    by_category: Dict[str, int] = Field(default_factory=dict)
    by_state: Dict[str, int] = Field(default_factory=dict)
    avg_resolution_hours: float = 0.0
    resolution_rate: float = 0.0
