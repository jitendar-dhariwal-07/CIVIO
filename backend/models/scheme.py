"""
Pydantic models for Government Scheme domain objects.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SchemeLevel(str, Enum):
    CENTRAL = "central"
    STATE = "state"
    DISTRICT = "district"


class SchemeCategory(str, Enum):
    EDUCATION = "education"
    HEALTH = "health"
    AGRICULTURE = "agriculture"
    HOUSING = "housing"
    EMPLOYMENT = "employment"
    SOCIAL_WELFARE = "social_welfare"
    WOMEN_CHILD = "women_and_child"
    MINORITY = "minority"
    DISABILITY = "disability"
    FINANCE = "finance"
    RURAL_DEVELOPMENT = "rural_development"
    SKILL_DEVELOPMENT = "skill_development"
    OTHER = "other"


class SchemeResponse(BaseModel):
    """Full scheme details."""

    id: str
    name: str
    name_local: Optional[str] = None
    description: str
    description_local: Optional[str] = None
    category: SchemeCategory
    level: SchemeLevel
    ministry: str
    state: Optional[str] = None
    benefits: str
    benefits_amount: Optional[str] = None
    eligibility_criteria: str
    eligibility_rules: Optional[Dict[str, Any]] = None
    documents_required: List[str] = Field(default_factory=list)
    application_process: str
    application_url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SchemeFilter(BaseModel):
    """Filter / search parameters for schemes."""

    category: Optional[SchemeCategory] = None
    level: Optional[SchemeLevel] = None
    state: Optional[str] = None
    is_active: Optional[bool] = True
    search: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class EligibilityRequest(BaseModel):
    """Data submitted to check eligibility for a single scheme."""

    scheme_id: str
    # User profile fields – sent inline so un-authenticated checks are possible
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    category: Optional[str] = None
    annual_income: Optional[float] = Field(None, ge=0)
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    is_disabled: bool = False
    is_minority: bool = False
    is_bpl: bool = False
    is_rural: bool = False


class EligibilityResult(BaseModel):
    """Result of an eligibility check against one scheme."""

    scheme_id: str
    scheme_name: str
    is_eligible: bool
    score: float = Field(..., ge=0, le=100, description="Eligibility score 0-100")
    matched_criteria: List[str] = Field(default_factory=list)
    unmatched_criteria: List[str] = Field(default_factory=list)
    explanation: str = ""
    ai_analysis: Optional[str] = None


class SchemeRecommendation(BaseModel):
    """An AI-recommended scheme with relevance info."""

    scheme: SchemeResponse
    relevance_score: float = Field(..., ge=0, le=100)
    match_reasons: List[str] = Field(default_factory=list)
    ai_summary: Optional[str] = None


class SchemeRecommendationRequest(BaseModel):
    """Profile data used to generate scheme recommendations."""

    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    category: Optional[str] = None
    annual_income: Optional[float] = Field(None, ge=0)
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    is_disabled: bool = False
    is_minority: bool = False
    is_bpl: bool = False
    is_rural: bool = False
    interests: List[str] = Field(default_factory=list)


class SimilarScheme(BaseModel):
    """Scheme returned from a similarity search."""

    scheme_id: str
    scheme_name: str
    similarity_score: float
