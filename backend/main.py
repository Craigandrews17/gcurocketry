from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .routers import users, courses, sponsors, webhooks

# ────────────────────────────────────────────────────────────
# FastAPI app
# ────────────────────────────────────────────────────────────
app = FastAPI(
    title="GU Rocketry API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None,
)

# ────────────────────────────────────────────────────────────
# Middleware
# ────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────────────────────────────────────
# Routers
# ────────────────────────────────────────────────────────────
app.include_router(users.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(sponsors.router, prefix="/api")
app.include_router(webhooks.router, prefix="/webhooks", include_in_schema=False)

# ────────────────────────────────────────────────────────────
# Static “/assets” for hero images & PDFs (served in prod by nginx)
# ────────────────────────────────────────────────────────────
ASSET_DIR = Path(__file__).parent.parent / "assets"
if ASSET_DIR.exists():
    app.mount("/assets", StaticFiles(directory=ASSET_DIR), name="assets")

# ────────────────────────────────────────────────────────────
# Health-check
# ────────────────────────────────────────────────────────────
@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
