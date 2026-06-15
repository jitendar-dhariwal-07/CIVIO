"""
Complaint processing pipeline.

Orchestrates AI classification, priority assignment, summarization, duplicate
detection, department assignment, and hotspot updating for each new complaint.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db import crud
from services import gemini_service, embedding_service

logger = logging.getLogger(__name__)

# ── Category → Department code mapping ──────────────────────────────────
CATEGORY_DEPARTMENT_MAP: Dict[str, str] = {
    "roads": "PWD",
    "water_supply": "PHED",
    "electricity": "ENERGY",
    "sanitation": "ULB",
    "public_transport": "TRANSPORT",
    "healthcare": "HEALTH",
    "education": "EDU",
    "pollution": "PCB",
    "corruption": "ACB",
    "public_safety": "POLICE",
    "housing": "HOUSING",
    "food_safety": "FSSAI",
    "telecom": "TELECOM",
    "banking": "RBI",
    "government_service": "GAD",
    "other": "GAD",
}

DEPARTMENT_DEFAULTS: Dict[str, Dict[str, str]] = {
    "PWD": {"name": "Public Works Department", "code": "PWD"},
    "PHED": {"name": "Public Health Engineering Department", "code": "PHED"},
    "ENERGY": {"name": "Energy Department", "code": "ENERGY"},
    "ULB": {"name": "Urban Local Body / Municipality", "code": "ULB"},
    "TRANSPORT": {"name": "Transport Department", "code": "TRANSPORT"},
    "HEALTH": {"name": "Health & Family Welfare Department", "code": "HEALTH"},
    "EDU": {"name": "Education Department", "code": "EDU"},
    "PCB": {"name": "Pollution Control Board", "code": "PCB"},
    "ACB": {"name": "Anti-Corruption Bureau", "code": "ACB"},
    "POLICE": {"name": "Police Department", "code": "POLICE"},
    "HOUSING": {"name": "Housing & Urban Development", "code": "HOUSING"},
    "FSSAI": {"name": "Food Safety & Standards Authority", "code": "FSSAI"},
    "TELECOM": {"name": "Telecom Regulatory Authority", "code": "TELECOM"},
    "RBI": {"name": "Reserve Bank of India / Banking Ombudsman", "code": "RBI"},
    "GAD": {"name": "General Administration Department", "code": "GAD"},
}


async def process_complaint(
    complaint_text: str,
    complaint_title: str,
    category: Optional[str] = None,
    image_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full AI processing pipeline for a new complaint.

    Steps:
    1. Classify the complaint (if category not provided)
    2. Determine priority
    3. Generate summary
    4. Generate embedding

    Returns a dict of AI-generated fields to be merged into the complaint record.
    """
    combined_text = f"{complaint_title}. {complaint_text}"

    # Step 1: Classification
    if not category:
        classification = await gemini_service.classify_complaint(combined_text, image_url)
        category = classification.get("category", "other")
        ai_confidence = classification.get("confidence", 0.0)
    else:
        ai_confidence = 1.0

    # Step 2: Priority
    priority_result = await gemini_service.generate_priority(combined_text, category)
    priority = priority_result.get("priority", "medium")
    sentiment_score = priority_result.get("score", 50) / 100.0

    # Step 3: Summary
    summary_result = await gemini_service.summarize_complaint(combined_text)
    ai_summary = summary_result.get("summary", "")

    # Step 4: Embedding
    try:
        embedding = embedding_service.generate_embedding(combined_text)
    except Exception as e:
        logger.error("Embedding generation failed: %s", e)
        embedding = None

    return {
        "category": category,
        "priority": priority,
        "ai_summary": ai_summary,
        "ai_category_confidence": ai_confidence,
        "sentiment_score": sentiment_score,
        "embedding": embedding,
    }


async def assign_department(
    db: AsyncSession,
    category: str,
    state: Optional[str] = None,
    district: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Find the appropriate department for a complaint based on its category.

    First tries the DB, then falls back to the hardcoded mapping.
    """
    # Try DB lookup
    dept = await crud.find_department_by_category(db, category, state)
    if dept:
        return {
            "department_id": dept.id,
            "department_name": dept.name,
        }

    # Fallback to default mapping
    dept_code = CATEGORY_DEPARTMENT_MAP.get(category, "GAD")
    dept_info = DEPARTMENT_DEFAULTS.get(dept_code, DEPARTMENT_DEFAULTS["GAD"])

    return {
        "department_id": None,
        "department_name": dept_info["name"],
    }


async def detect_duplicates(
    db: AsyncSession,
    complaint_text: str,
    threshold: float = 0.85,
) -> List[Dict[str, Any]]:
    """
    Check if a new complaint is a potential duplicate of existing complaints.
    """
    existing = await crud.get_complaints_with_embeddings(db)
    if not existing:
        return []

    existing_data = [
        {
            "id": c.id,
            "tracking_id": c.tracking_id,
            "title": c.title,
            "category": c.category,
            "status": c.status,
            "embedding": c.embedding,
        }
        for c in existing
        if c.embedding
    ]

    return embedding_service.find_duplicates(
        new_complaint_text=complaint_text,
        existing_complaints=existing_data,
        threshold=threshold,
    )


async def update_hotspots(db: AsyncSession) -> int:
    """
    Re-compute hotspots from all geo-located complaints and cache them.
    Returns the number of hotspots detected.
    """
    from services.hotspot_service import detect_hotspots

    complaints = await crud.get_complaints_with_location(db)
    if not complaints:
        return 0

    complaint_data = [
        {
            "id": c.id,
            "latitude": c.latitude,
            "longitude": c.longitude,
            "category": c.category,
            "state": c.state,
            "district": c.district,
        }
        for c in complaints
        if c.latitude is not None and c.longitude is not None
    ]

    hotspots = detect_hotspots(complaint_data)

    hotspot_records = [
        {
            "cluster_id": h["cluster_id"],
            "latitude": h["latitude"],
            "longitude": h["longitude"],
            "complaint_count": h["complaint_count"],
            "radius_km": h["radius_km"],
            "primary_category": h["primary_category"],
            "categories": h["categories"],
            "state": h.get("state"),
            "district": h.get("district"),
            "severity_score": h["severity_score"],
            "complaint_ids": h["complaint_ids"],
        }
        for h in hotspots
    ]

    count = await crud.upsert_hotspots(db, hotspot_records)
    logger.info("Updated %d hotspots from %d complaints.", count, len(complaint_data))
    return count
