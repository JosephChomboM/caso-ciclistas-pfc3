from functools import lru_cache

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: str = "development"
    database_url: str = "sqlite:///./ciclolima.db"
    jwt_secret: SecretStr
    jwt_ttl_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]

    @model_validator(mode="after")
    def secure_settings(self):
        if len(self.jwt_secret.get_secret_value()) < 32:
            raise ValueError("JWT_SECRET requiere al menos 32 caracteres aleatorios")
        if not 1 <= self.jwt_ttl_minutes <= 120:
            raise ValueError("JWT_TTL_MINUTES debe estar entre 1 y 120")
        if "*" in self.cors_origins:
            raise ValueError("CORS requiere orígenes explícitos")
        if self.environment == "production":
            if not self.database_url.startswith("postgresql+psycopg://"):
                raise ValueError("Producción requiere PostgreSQL con psycopg")
            if not self.cors_origins or any(
                not origin.startswith("https://") for origin in self.cors_origins
            ):
                raise ValueError("Producción requiere orígenes HTTPS")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
