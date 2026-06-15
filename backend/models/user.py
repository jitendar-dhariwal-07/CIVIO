"""
Pydantic models for User domain objects.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Category(str, Enum):
    """Government reservation / social category."""
    GENERAL = "general"
    OBC = "obc"
    SC = "sc"
    ST = "st"
    EWS = "ews"


class UserCreate(BaseModel):
    """Payload for user registration."""

    full_name: str = Field(..., min_length=2, max_length=150, description="Full name of the citizen")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{9,14}$", description="Phone number with country code")
    password: str = Field(..., min_length=8, max_length=128, description="Account password")

    # Optional profile fields – can be filled later
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    category: Optional[Category] = None
    annual_income: Optional[float] = Field(None, ge=0, description="Annual household income in INR")
    occupation: Optional[str] = Field(None, max_length=100)
    education: Optional[str] = Field(None, max_length=100)

    # Location
    state: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")

    # Disability & minority flags
    is_disabled: bool = False
    is_minority: bool = False
    is_bpl: bool = False  # Below Poverty Line
    is_rural: bool = False

    preferred_language: str = Field("en", min_length=2, max_length=5)


class UserLogin(BaseModel):
    """Login credentials."""

    email: EmailStr
    password: str


class UserProfile(BaseModel):
    """Detailed user profile returned to authenticated user."""

    id: str
    full_name: str
    email: str
    phone: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    category: Optional[Category] = None
    annual_income: Optional[float] = None
    occupation: Optional[str] = None
    education: Optional[str] = None

    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

    is_disabled: bool = False
    is_minority: bool = False
    is_bpl: bool = False
    is_rural: bool = False
    preferred_language: str = "en"

    is_admin: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Fields that users may update on their own profile."""

    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{9,14}$")
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    category: Optional[Category] = None
    annual_income: Optional[float] = Field(None, ge=0)
    occupation: Optional[str] = Field(None, max_length=100)
    education: Optional[str] = Field(None, max_length=100)

    state: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")

    is_disabled: Optional[bool] = None
    is_minority: Optional[bool] = None
    is_bpl: Optional[bool] = None
    is_rural: Optional[bool] = None
    preferred_language: Optional[str] = Field(None, min_length=2, max_length=5)


class UserResponse(BaseModel):
    """Public-facing user summary (e.g. in complaint author field)."""

    id: str
    full_name: str
    state: Optional[str] = None
    district: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token pair returned after login / registration."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Seconds until the access token expires")
    user: UserProfile
