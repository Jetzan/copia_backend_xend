import pytest
from pydantic import ValidationError

from app.core.config import MAX_FILE_SIZE_BYTES, Settings

BASE = {
    "postgres_user": "usuario_prueba",
    "postgres_password": "secreto123",
    "mongo_uri": "mongodb://localhost:27017",
}


def build(**extra) -> Settings:
    return Settings(_env_file=None, **BASE, **extra)


def test_limite_por_defecto_es_3gb():
    assert build().max_file_size_bytes == 3_221_225_472


def test_rechaza_limite_mayor_a_3gb():
    with pytest.raises(ValidationError):
        build(max_file_size_bytes=MAX_FILE_SIZE_BYTES + 1)


def test_cors_vacio_por_defecto():
    assert build().cors_origins == []


def test_faltan_credenciales(monkeypatch):
    for nombre in ("XEND_POSTGRES_USER", "XEND_POSTGRES_PASSWORD", "XEND_MONGO_URI"):
        monkeypatch.delenv(nombre, raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_password_no_aparece_en_repr():
    settings = build()
    assert "secreto123" not in repr(settings)
    assert "secreto123" not in str(settings)


def test_conninfo_usa_esquema_xend():
    info = build().postgres_conninfo()
    assert "search_path=xend" in info
    assert "dbname=xend" in info
