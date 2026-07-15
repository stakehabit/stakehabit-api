from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_url: str = Field(..., validation_alias="DATABASE_URL")
    jwt_secret_key: str = Field(..., validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def default_settings() -> Settings:
    return Settings()


settings = default_settings()
