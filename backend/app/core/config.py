from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI E-Commerce Analytics Platform"
    app_version: str  = "1.0.0"
    environment: str = "development"

    database_url: str = (
        "postgresql://ecommerce_user:ecommerce_password@localhost:5432/ecommerce_db"
    )

    redis_url: str = (
        "redis://localhost:6379"
    )

    class Config:
        env_file = ".env"


settings = Settings()