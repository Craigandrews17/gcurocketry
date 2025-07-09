import uuid
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Course, Enrollment, SponsorTier, User
from .schemas import UserCreate
from .utils.security import get_password_hash


# ── Users ────────────────────────────────────────────────
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalars().first()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ── Courses ──────────────────────────────────────────────
async def list_courses(db: AsyncSession) -> Sequence[Course]:
    res = await db.execute(select(Course).order_by(Course.id))
    return res.scalars().all()


async def enroll_user(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    course_id: int,
    paid: bool = False,
) -> Enrollment:
    enrollment = Enrollment(user_id=user_id, course_id=course_id, paid=paid)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


# ── Sponsor tiers ────────────────────────────────────────
async def list_tiers(db: AsyncSession) -> Sequence[SponsorTier]:
    res = await db.execute(select(SponsorTier).order_by(SponsorTier.order))
    return res.scalars().all()


async def delete_all_tiers(db: AsyncSession) -> None:
    await db.execute(delete(SponsorTier))
    await db.commit()
