import secrets
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    # ───────── App
    DEBUG: bool = Field(False, env="DEBUG")
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    # ───────── Database
    POSTGRES_USER: str = "gurocket"
    POSTGRES_PASSWORD: str = "supersecret"
    POSTGRES_DB: str = "gurocketry"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    # ───────── Auth / JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    ALGORITHM: str = "HS256"

    # ───────── Stripe
    STRIPE_PUBLIC_KEY: str = "pk_test_xxx"
    STRIPE_SECRET_KEY: str = "sk_test_xxx"
    STRIPE_WEBHOOK_SECRET: str = "whsec_xxx"
    STRIPE_PRICE_ID_COURSE: str = "price_xxx"

    # ───────── Email
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str = "GU Rocketry"

    # ───────── Misc
    PROJECT_DIR: Path = Path(__file__).resolve().parents[2]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_uri(cls, v: str | None, values: dict) -> str:
        if isinstance(v, str):
            return v
        return (
            "postgresql+asyncpg://"
            f"{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}"
            f"@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/"
            f"{values['POSTGRES_DB']}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
