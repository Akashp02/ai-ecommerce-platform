from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI E-Commerce Analytics Platform"
    app_version: str  = "1.0.0"
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()