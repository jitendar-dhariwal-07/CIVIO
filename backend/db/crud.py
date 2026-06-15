"""
CRUD (Create-Read-Update-Delete) operations for all ORM models.
Every function accepts an AsyncSession and returns domain objects.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy import and_, desc, asc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    ComplaintORM,
    DepartmentORM,
    HotspotORM,
    SchemeORM,
    UserORM,
)


# ════════════════════════════════════════════════════════════════════════
# User CRUD
# ════════════════════════════════════════════════════════════════════════

async def create_user(db: AsyncSession, **kwargs: Any) -> UserORM:
    user = UserORM(**kwargs)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserORM]:
    result = await db.execute(select(UserORM).where(UserORM.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[UserORM]:
    result = await db.execute(select(UserORM).where(UserORM.id == user_id))
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: str, data: Dict[str, Any]) -> Optional[UserORM]:
    data["updated_at"] = datetime.utcnow()
    await db.execute(update(UserORM).where(UserORM.id == user_id).values(**data))
    await db.flush()
    return await get_user_by_id(db, user_id)


async def get_user_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(UserORM.id)))
    return result.scalar() or 0


# ════════════════════════════════════════════════════════════════════════
# Scheme CRUD
# ════════════════════════════════════════════════════════════════════════

async def create_scheme(db: AsyncSession, **kwargs: Any) -> SchemeORM:
    scheme = SchemeORM(**kwargs)
    db.add(scheme)
    await db.flush()
    await db.refresh(scheme)
    return scheme


async def get_scheme_by_id(db: AsyncSession, scheme_id: str) -> Optional[SchemeORM]:
    result = await db.execute(select(SchemeORM).where(SchemeORM.id == scheme_id))
    return result.scalars().first()


async def list_schemes(
    db: AsyncSession,
    *,
    category: Optional[str] = None,
    level: Optional[str] = None,
    state: Optional[str] = None,
    is_active: Optional[bool] = True,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[Sequence[SchemeORM], int]:
    query = select(SchemeORM)
    count_query = select(func.count(SchemeORM.id))

    conditions = []
    if category:
        conditions.append(SchemeORM.category == category)
    if level:
        conditions.append(SchemeORM.level == level)
    if state:
        conditions.append(or_(SchemeORM.state == state, SchemeORM.level == "central"))
    if is_active is not None:
        conditions.append(SchemeORM.is_active == is_active)
    if search:
        search_pattern = f"%{search}%"
        conditions.append(
            or_(
                SchemeORM.name.ilike(search_pattern),
                SchemeORM.description.ilike(search_pattern),
                SchemeORM.benefits.ilike(search_pattern),
            )
        )

    if conditions:
        query = query.where(and_(*conditions))
        count_query = count_query.where(and_(*conditions))

    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(desc(SchemeORM.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all(), total


async def get_all_schemes(db: AsyncSession, is_active: bool = True) -> Sequence[SchemeORM]:
    result = await db.execute(
        select(SchemeORM).where(SchemeORM.is_active == is_active)
    )
    return result.scalars().all()


async def get_scheme_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(SchemeORM.id)))
    return result.scalar() or 0


# ════════════════════════════════════════════════════════════════════════
# Complaint CRUD
# ════════════════════════════════════════════════════════════════════════

async def create_complaint(db: AsyncSession, **kwargs: Any) -> ComplaintORM:
    complaint = ComplaintORM(**kwargs)
    db.add(complaint)
    await db.flush()
    await db.refresh(complaint)
    return complaint


async def get_complaint_by_id(db: AsyncSession, complaint_id: str) -> Optional[ComplaintORM]:
    result = await db.execute(
        select(ComplaintORM).where(ComplaintORM.id == complaint_id)
    )
    return result.scalars().first()


async def get_complaint_by_tracking_id(db: AsyncSession, tracking_id: str) -> Optional[ComplaintORM]:
    result = await db.execute(
        select(ComplaintORM).where(ComplaintORM.tracking_id == tracking_id)
    )
    return result.scalars().first()


async def list_complaints(
    db: AsyncSession,
    *,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    department_id: Optional[str] = None,
    user_id: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 20,
) -> Tuple[Sequence[ComplaintORM], int]:
    query = select(ComplaintORM)
    count_query = select(func.count(ComplaintORM.id))

    conditions = []
    if status:
        conditions.append(ComplaintORM.status == status)
    if priority:
        conditions.append(ComplaintORM.priority == priority)
    if category:
        conditions.append(ComplaintORM.category == category)
    if state:
        conditions.append(ComplaintORM.state == state)
    if district:
        conditions.append(ComplaintORM.district == district)
    if department_id:
        conditions.append(ComplaintORM.department_id == department_id)
    if user_id:
        conditions.append(ComplaintORM.user_id == user_id)
    if date_from:
        conditions.append(ComplaintORM.created_at >= date_from)
    if date_to:
        conditions.append(ComplaintORM.created_at <= date_to)
    if search:
        search_pattern = f"%{search}%"
        conditions.append(
            or_(
                ComplaintORM.title.ilike(search_pattern),
                ComplaintORM.description.ilike(search_pattern),
                ComplaintORM.tracking_id.ilike(search_pattern),
            )
        )

    if conditions:
        query = query.where(and_(*conditions))
        count_query = count_query.where(and_(*conditions))

    total = (await db.execute(count_query)).scalar() or 0

    # Sorting
    sort_column = getattr(ComplaintORM, sort_by, ComplaintORM.created_at)
    order_func = desc if sort_order == "desc" else asc
    query = query.order_by(order_func(sort_column))

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all(), total


async def update_complaint(
    db: AsyncSession, complaint_id: str, data: Dict[str, Any]
) -> Optional[ComplaintORM]:
    data["updated_at"] = datetime.utcnow()
    if data.get("status") == "resolved" and "resolved_at" not in data:
        data["resolved_at"] = datetime.utcnow()
    await db.execute(
        update(ComplaintORM).where(ComplaintORM.id == complaint_id).values(**data)
    )
    await db.flush()
    return await get_complaint_by_id(db, complaint_id)


async def get_complaints_with_embeddings(db: AsyncSession) -> Sequence[ComplaintORM]:
    result = await db.execute(
        select(ComplaintORM).where(ComplaintORM.embedding.isnot(None))
    )
    return result.scalars().all()


async def get_complaints_with_location(db: AsyncSession) -> Sequence[ComplaintORM]:
    result = await db.execute(
        select(ComplaintORM).where(
            and_(
                ComplaintORM.latitude.isnot(None),
                ComplaintORM.longitude.isnot(None),
            )
        )
    )
    return result.scalars().all()


async def get_complaint_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(ComplaintORM.id)))
    return result.scalar() or 0


async def get_complaint_count_by_status(db: AsyncSession) -> Dict[str, int]:
    result = await db.execute(
        select(ComplaintORM.status, func.count(ComplaintORM.id))
        .group_by(ComplaintORM.status)
    )
    return {row[0]: row[1] for row in result.all()}


async def get_complaint_count_by_priority(db: AsyncSession) -> Dict[str, int]:
    result = await db.execute(
        select(ComplaintORM.priority, func.count(ComplaintORM.id))
        .group_by(ComplaintORM.priority)
    )
    return {row[0]: row[1] for row in result.all()}


async def get_complaint_count_by_category(db: AsyncSession) -> Dict[str, int]:
    result = await db.execute(
        select(ComplaintORM.category, func.count(ComplaintORM.id))
        .group_by(ComplaintORM.category)
    )
    return {row[0]: row[1] for row in result.all()}


async def get_complaint_count_by_state(db: AsyncSession) -> Dict[str, int]:
    result = await db.execute(
        select(ComplaintORM.state, func.count(ComplaintORM.id))
        .group_by(ComplaintORM.state)
    )
    return {row[0]: row[1] for row in result.all()}


async def get_avg_resolution_hours(db: AsyncSession) -> float:
    result = await db.execute(
        select(
            func.avg(
                func.extract("epoch", ComplaintORM.resolved_at - ComplaintORM.created_at) / 3600
            )
        ).where(ComplaintORM.resolved_at.isnot(None))
    )
    val = result.scalar()
    return round(float(val), 2) if val else 0.0


# ════════════════════════════════════════════════════════════════════════
# Department CRUD
# ════════════════════════════════════════════════════════════════════════

async def create_department(db: AsyncSession, **kwargs: Any) -> DepartmentORM:
    dept = DepartmentORM(**kwargs)
    db.add(dept)
    await db.flush()
    await db.refresh(dept)
    return dept


async def get_department_by_id(db: AsyncSession, dept_id: str) -> Optional[DepartmentORM]:
    result = await db.execute(
        select(DepartmentORM).where(DepartmentORM.id == dept_id)
    )
    return result.scalars().first()


async def get_department_by_code(db: AsyncSession, code: str) -> Optional[DepartmentORM]:
    result = await db.execute(
        select(DepartmentORM).where(DepartmentORM.code == code)
    )
    return result.scalars().first()


async def list_departments(db: AsyncSession) -> Sequence[DepartmentORM]:
    result = await db.execute(
        select(DepartmentORM).where(DepartmentORM.is_active == True).order_by(DepartmentORM.name)
    )
    return result.scalars().all()


async def get_department_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(DepartmentORM.id)))
    return result.scalar() or 0


async def find_department_by_category(
    db: AsyncSession, category: str, state: Optional[str] = None
) -> Optional[DepartmentORM]:
    """Find the best matching department for a complaint category."""
    query = select(DepartmentORM).where(DepartmentORM.is_active == True)
    result = await db.execute(query)
    departments = result.scalars().all()

    for dept in departments:
        cats = dept.categories or []
        if category in cats:
            if state and dept.state and dept.state != state:
                continue
            return dept

    # Fallback: return first active department
    return departments[0] if departments else None


# ════════════════════════════════════════════════════════════════════════
# Hotspot CRUD
# ════════════════════════════════════════════════════════════════════════

async def upsert_hotspots(db: AsyncSession, hotspots: List[Dict[str, Any]]) -> int:
    """Replace all cached hotspots with new ones."""
    await db.execute(
        HotspotORM.__table__.delete()
    )
    count = 0
    for h in hotspots:
        db.add(HotspotORM(**h))
        count += 1
    await db.flush()
    return count


async def get_hotspots(db: AsyncSession) -> Sequence[HotspotORM]:
    result = await db.execute(
        select(HotspotORM).order_by(desc(HotspotORM.severity_score))
    )
    return result.scalars().all()


# ════════════════════════════════════════════════════════════════════════
# Pagination helper
# ════════════════════════════════════════════════════════════════════════

def paginate_metadata(total: int, page: int, page_size: int) -> Dict[str, Any]:
    total_pages = max(1, math.ceil(total / page_size))
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }
