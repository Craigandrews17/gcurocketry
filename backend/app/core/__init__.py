from fastapi import APIRouter

from .users import router as users
from .courses import router as courses
from .sponsors import router as sponsors
from .webhooks import router as webhooks

router = APIRouter()
router.include_router(users)
router.include_router(courses)
router.include_router(sponsors)
router.include_router(webhooks)
