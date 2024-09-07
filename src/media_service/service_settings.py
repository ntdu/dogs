
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


class DogsConnectorSettings(BaseSettings):
    DOGS_API_URL: str
    DOGS_API_KEY: str

class MinIOSettings(BaseSettings):
    MINIO_DOMAIN: str = ''
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_API: str
    MINIO_PATH: str
    MINIO_BUCKET_NAME: str
    AWS_S3_ENDPOINT_URL: str
    MINIO_PUBLIC_DOMAIN: str

    def get_minio_server_url(self) -> str:
        if self.MINIO_DOMAIN:
            return self.MINIO_DOMAIN
        return f'{self.MINIO_HOST}:{self.MINIO_PORT}'

class Settings(MinIOSettings, DogsConnectorSettings, DatabaseSettings, BaseSettings):
    DEBUG: bool = False
    ENVIRONMENT: str
    HOST: str
    PORT: int

    SECRET_KEY: str
    ALLOWED_HOSTS: list = []
    INTERNAL_IPS: list = ["127.0.0.1"]

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / "env/.env"

@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
