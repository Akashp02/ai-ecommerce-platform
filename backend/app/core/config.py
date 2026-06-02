from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str
    environment: str

    class Config:
        env_file = ".env"


settings = Settings()