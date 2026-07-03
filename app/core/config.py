from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    # ==========================================
    # Database
    # ==========================================

    DATABASE_URL: str

    # ==========================================
    # JWT Authentication
    # ==========================================

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ==========================================
    # Admin
    # ==========================================

    SUPER_ADMIN_EMAIL: str

    # ==========================================
    # Redis
    # ==========================================

    REDIS_URL: str

    # ==========================================
    # Celery
    # ==========================================

    CELERY_BROKER_URL: str

    CELERY_RESULT_BACKEND: str

    # ==========================================
    # Environment
    # ==========================================

    ENVIRONMENT: str = "development"

    # ==========================================
    # Pydantic Settings
    # ==========================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # ==========================================
    # Email
    # ==========================================

    SMTP_HOST: str

    SMTP_PORT: int

    SMTP_USERNAME: str
 
    SMTP_PASSWORD: str

    EMAIL_FROM: str
    # ==========================================
# Gemini
# ==========================================

    GEMINI_API_KEY: str
    
settings = Settings()