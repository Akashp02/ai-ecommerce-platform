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

    secret_key: str = "my_super_secret_key_12345"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()