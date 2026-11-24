from fastapi.testclient import TestClient

from app import main
from app.core.config import Settings

ORIGEN = "http://localhost:8080"


def crear_cliente(monkeypatch) -> TestClient:
    settings = Settings(
        _env_file=None,
        postgres_user="u",
        postgres_password="p",
        mongo_uri="mongodb://localhost:27017",
        cors_origins=[ORIGEN],
    )
    monkeypatch.setattr(main, "get_settings", lambda: settings)
    return TestClient(main.create_app())


def test_cors_permite_origen_configurado(monkeypatch):
    r = crear_cliente(monkeypatch).get("/api/v1/health", headers={"Origin": ORIGEN})
    assert r.headers["access-control-allow-origin"] == ORIGEN


def test_cors_rechaza_origen_ajeno(monkeypatch):
    r = crear_cliente(monkeypatch).get(
        "/api/v1/health", headers={"Origin": "http://sitio-malicioso.example"}
    )
    assert "access-control-allow-origin" not in r.headers
