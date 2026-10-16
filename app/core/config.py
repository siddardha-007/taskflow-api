from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    # Defaults to an empty list if not provided in .env
    CORS_ORIGINS: List[str] = []

    # Automatically parse comma-separated strings or JSON lists from .env into a Python list
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        import json
        try:
            return json.loads(v)
        except Exception:
            return []

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
