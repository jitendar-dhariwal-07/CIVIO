"""
Async SQLAlchemy engine, session factory, and dependency helpers.
Uses asyncpg as the underlying PostgreSQL driver for CIVIO.
"""

from __future__ import annotations

from typing import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create async engine for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise


async def init_db():
    """Initialize database tables.
    
    Run this once during startup to create all tables.
    """
    try:
        logger.info("Initializing database tables...")
        async with engine.begin() as conn:
            # Create all tables from Base metadata
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def seed_db():
    """Seed database with sample data.
    
    Useful for development and testing.
    Run this after init_db() to populate sample data.
    """
    try:
        logger.info("Seeding database with sample data...")
        # Sample data seeding will be implemented in db/seed.py
        logger.info("Database seeding completed successfully")
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        raise


async def drop_db():
    """Drop all database tables.
    
    WARNING: This will delete all data. Use only for development/testing.
    """
    try:
        logger.warning("Dropping all database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database drop completed")
    except Exception as e:
        logger.error(f"Failed to drop database: {e}")
        raise


async def close_db():
    """Close database engine and connections."""
    await engine.dispose()
        finally:
            await session.close()


async def init_db() -> None:
    """Create all tables (useful for development/testing)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose of the connection pool."""
    await engine.dispose()
