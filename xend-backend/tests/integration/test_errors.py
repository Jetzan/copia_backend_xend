from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.errors import register_exception_handlers
from app.core.exceptions import ArchivoDemasiadoGrandeError, ConversacionNoAutorizadaError


def crear_cliente() -> TestClient:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/prohibido")
    def prohibido() -> None:
        raise ConversacionNoAutorizadaError()

    @app.get("/grande")
    def grande() -> None:
        raise ArchivoDemasiadoGrandeError(4 * 1024**3, 3 * 1024**3)

    @app.get("/falla")
    def falla() -> None:
        raise RuntimeError("secreto interno")

    @app.get("/numero/{n}")
    def numero(n: int) -> dict[str, int]:
        return {"n": n}

    # raise_server_exceptions=False: queremos ver la respuesta 500, no la excepción.
    return TestClient(app, raise_server_exceptions=False)


def test_conversacion_no_autorizada_devuelve_403():
    r = crear_cliente().get("/prohibido")
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "conversacion_no_autorizada"


def test_archivo_grande_devuelve_413():
    assert crear_cliente().get("/grande").status_code == 413


def test_error_inesperado_no_filtra_detalles():
    r = crear_cliente().get("/falla")
    assert r.status_code == 500
    assert "secreto interno" not in r.text


def test_validacion_usa_formato_uniforme_sin_el_valor_recibido():
    r = crear_cliente().get("/numero/abc")
    assert r.status_code == 422
    cuerpo = r.json()["error"]
    assert cuerpo["code"] == "validacion_fallida"
    assert "abc" not in r.text
