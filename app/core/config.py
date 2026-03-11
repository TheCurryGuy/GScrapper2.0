from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = Field(default="Academic Publication API")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    SERPAPI_KEY: str = Field(default="5f319270da27b09d5b02d543072ee24992beab9418ddf6476debe37dcf5e7c87")
    SERPAPI_KEY_BACKUP: str = Field(default="389e15d06ef652330f8a85cec85dabac792adb2ba5995020df9f459ada770b8e")
    SERPAPI_KEY_BACKUP2: str = Field(default="3d76f73e45dd4101751fb446a805e6293e23034ea6350b739e67f59b596c1730")
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = Field(default=None)
    OPENALEX_EMAIL: str = Field(default="")
    CROSSREF_MAILTO: str = Field(default="")
    ORCID_CLIENT_ID: Optional[str] = Field(default=None)
    ORCID_CLIENT_SECRET: Optional[str] = Field(default=None)
    
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    CACHE_TTL: int = Field(default=3600)
    
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_PER_MINUTE: int = Field(default=30)
    RATE_LIMIT_PER_HOUR: int = Field(default=500)
    
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/app.log")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
