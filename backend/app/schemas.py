"""
Pydantic (v2) schemas for request & response bodies.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field


# ───────── Common ──────────────────────────────────────────
class Timestamp(BaseModel):
    created_at: datetime
    updated_at: datetime


# ───────── User ────────────────────────────────────────────
class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["student@gla.ac.uk"])
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase, Timestamp):
    id: uuid.UUID
    is_active: bool


# ───────── Auth / Token ────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ───────── Course & Enrollment ─────────────────────────────
class CourseRead(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    price_cents: int


class EnrollmentRead(BaseModel):
    id: int
    course: CourseRead
    paid: bool
    created_at: datetime


# ───────── Sponsor tiers ───────────────────────────────────
class SponsorTierRead(BaseModel):
    id: int
    name: str
    price_gbp: int
    perks: dict[str, Any]

