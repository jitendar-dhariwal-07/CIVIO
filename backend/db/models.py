"""
SQLAlchemy ORM models for all CitizenAI database tables.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_tracking_id() -> str:
    """Generate a human-readable tracking ID like CIT-20260615-A3F2."""
    import random
    import string
    date_part = datetime.utcnow().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CIT-{date_part}-{random_part}"


# ════════════════════════════════════════════════════════════════════════
# User
# ════════════════════════════════════════════════════════════════════════

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    date_of_birth: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    annual_income: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    occupation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    education: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)

    is_disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_minority: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bpl: Mapped[bool] = mapped_column(Boolean, default=False)
    is_rural: Mapped[bool] = mapped_column(Boolean, default=False)
    preferred_language: Mapped[str] = mapped_column(String(5), default="en")

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Relationships
    complaints = relationship("ComplaintORM", back_populates="user", lazy="selectin")


# ════════════════════════════════════════════════════════════════════════
# Department
# ════════════════════════════════════════════════════════════════════════

class DepartmentORM(Base):
    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    head_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    categories: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    complaints = relationship("ComplaintORM", back_populates="department", lazy="selectin")


# ════════════════════════════════════════════════════════════════════════
# Scheme
# ════════════════════════════════════════════════════════════════════════

class SchemeORM(Base):
    __tablename__ = "schemes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    name_local: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_local: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    level: Mapped[str] = mapped_column(String(20), nullable=False)  # central / state / district
    ministry: Mapped[str] = mapped_column(String(200), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    benefits: Mapped[str] = mapped_column(Text, nullable=False)
    benefits_amount: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    eligibility_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    eligibility_rules: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    documents_required: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    application_process: Mapped[str] = mapped_column(Text, nullable=False)
    application_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)

    # Embedding for similarity search (stored as JSON array of floats)
    embedding: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    __table_args__ = (
        Index("ix_schemes_category_level", "category", "level"),
    )


# ════════════════════════════════════════════════════════════════════════
# Complaint
# ════════════════════════════════════════════════════════════════════════

class ComplaintORM(Base):
    __tablename__ = "complaints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    tracking_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, default=generate_tracking_id, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="submitted", index=True)

    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Location
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # AI fields
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_category_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Embedding for duplicate detection
    embedding: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    # Department assignment
    department_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("departments.id"), nullable=True
    )
    department_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    admin_remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # User
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    user_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    language: Mapped[str] = mapped_column(String(5), default="en")

    duplicate_of: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user = relationship("UserORM", back_populates="complaints", lazy="selectin")
    department = relationship("DepartmentORM", back_populates="complaints", lazy="selectin")

    __table_args__ = (
        Index("ix_complaints_state_district", "state", "district"),
        Index("ix_complaints_user_status", "user_id", "status"),
    )


# ════════════════════════════════════════════════════════════════════════
# Hotspot (cached cluster data)
# ════════════════════════════════════════════════════════════════════════

class HotspotORM(Base):
    __tablename__ = "hotspots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    cluster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    complaint_count: Mapped[int] = mapped_column(Integer, default=0)
    radius_km: Mapped[float] = mapped_column(Float, default=1.0)
    primary_category: Mapped[str] = mapped_column(String(50), nullable=False)
    categories: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    severity_score: Mapped[float] = mapped_column(Float, default=0.0)
    complaint_ids: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
