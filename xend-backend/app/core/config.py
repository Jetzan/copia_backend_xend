"""Configuración central de Xend, leída de variables de entorno o del archivo .env."""

from functools import lru_cache
from typing import Literal

from psycopg.conninfo import make_conninfo
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Regla de negocio: debe coincidir con el CHECK de la tabla archivo (3 GB).
MAX_FILE_SIZE_BYTES = 3 * 1024**3


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="XEND_",
        extra="ignore",
    )

    environment: Literal["development", "testing", "production"] = "development"
    cors_origins: list[str] = Field(default_factory=list)
    max_file_size_bytes: int = Field(default=MAX_FILE_SIZE_BYTES, gt=0, le=MAX_FILE_SIZE_BYTES)

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "xend"
    postgres_schema: str = "xend"
    postgres_user: str
    postgres_password: SecretStr

    mongo_uri: SecretStr
    mongo_db: str = "xend_analytics"

    def postgres_conninfo(self) -> str:
        """Cadena de conexión para psycopg, con el search_path del esquema de Xend."""
        return make_conninfo(
            host=self.postgres_host,
            port=self.postgres_port,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            options=f"-c search_path={self.postgres_schema}",
        )


@lru_cache
def get_settings() -> Settings:
    """Una sola instancia de Settings para toda la aplicación."""
    return Settings()
