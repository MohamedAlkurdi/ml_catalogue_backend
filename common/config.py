from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    api_title: str = "Unified ML API"
    debug: bool = False
    port: int = 8000
    allowed_origins: List[str] = ["*"]
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()