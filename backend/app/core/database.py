from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

from .config import settings

# ────────────────────────────────────────────────────────────
# Engine + Session
# ────────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@asynccontextmanager
async def get_db() -> AsyncSession:
    """FastAPI dependency — yields an async SQLAlchemy session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
