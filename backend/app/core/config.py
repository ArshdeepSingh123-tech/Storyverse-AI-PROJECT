from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://storyverse:storyverse123@localhost:5432/storyverse_db"
    SECRET_KEY: str = "change-this-secret-key-in-production-must-be-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"

    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:3001","http://127.0.0.1:3000"]'
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB

    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
