import pytest

from app.core.exceptions import (
    ArchivoDemasiadoGrandeError,
    ConflictoError,
    ConversacionNoAutorizadaError,
    PermisoDenegadoError,
    XendError,
)


def test_mensaje_por_defecto():
    assert XendError().message == "Error interno del servidor."


def test_mensaje_personalizado():
    assert ConflictoError("Ya existe").message == "Ya existe"


def test_conversacion_no_autorizada_es_un_permiso_denegado():
    exc = ConversacionNoAutorizadaError()
    assert isinstance(exc, PermisoDenegadoError)
    assert exc.status_code == 403
    assert exc.code == "conversacion_no_autorizada"


def test_archivo_demasiado_grande():
    exc = ArchivoDemasiadoGrandeError(4 * 1024**3, 3 * 1024**3)
    assert exc.status_code == 413
    assert "4.00 GB" in exc.message and "3.00 GB" in exc.message


@pytest.mark.parametrize("clase", [ConflictoError, ConversacionNoAutorizadaError])
def test_todas_heredan_de_xend_error(clase):
    assert issubclass(clase, XendError)
