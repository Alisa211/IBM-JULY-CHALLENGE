from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MuseEngine API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "supersecretkey_change_in_prod"
    
    # Postgres
    DATABASE_URL: str = "postgresql+asyncpg://muse_user:muse_password@localhost:5432/muse_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Storage
    STORAGE_URL: str = "file:///storage/"
    
    # Watsonx.ai
    WATSONX_API_KEY: str = ""
    WATSONX_PROJECT_ID: str = ""
    WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_MODEL_ID: str = "ibm/granite-4-h-small"
    VISION_PROVIDER: str = "mock"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()
