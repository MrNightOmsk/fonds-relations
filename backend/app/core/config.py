import secrets
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # PostgreSQL
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        password = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # First superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_FULL_NAME: str
    FIRST_SUPERUSER_ORGANIZATION: str

    # Elasticsearch
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    ELASTICSEARCH_SCHEME: str = "http"
    ELASTICSEARCH_USER: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[str] = None
    ELASTICSEARCH_INDEX_PREFIX: str = "fonds_relations"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 