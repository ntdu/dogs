
import functools
from typing import Dict, List, Optional, Tuple

from pathlib import Path
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    DB_MASTER_ENABLE: bool = True
    DB_MASTER_ENGINE: str
    DB_MASTER_NAME: str
    DB_MASTER_USERNAME: str
    DB_MASTER_PASSWORD: str
    DB_MASTER_HOST: str
    DB_MASTER_PORT: str

    def get_databases(self):
        return {
            'default': {
                'ENGINE': self.DB_MASTER_ENGINE,
                'NAME': self.DB_MASTER_NAME,
                'USER': self.DB_MASTER_USERNAME,
                'PASSWORD': self.DB_MASTER_PASSWORD,
                'HOST': self.DB_MASTER_HOST,
                'PORT': self.DB_MASTER_PORT,
                'ATOMIC_REQUESTS': True,
                'CONN_MAX_AGE': 60,
                'CONN_HEALTH_CHECKS': True
            }
        }


class Settings(DatabaseSettings, BaseSettings):
    DEBUG: bool = False
    ENVIRONMENT: str
    HOST: str
    PORT: int

    SECRET_KEY: str
    ALLOWED_HOSTS: list = []

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / "env/.env"

@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
