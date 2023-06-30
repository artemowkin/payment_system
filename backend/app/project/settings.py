from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    redis_url: str
    domain: str

    class Config:
        env_file = BASE_DIR.parent.parent / '.env'
        env_prefix = 'app_'


settings = Settings()
