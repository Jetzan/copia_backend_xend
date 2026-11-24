from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import PropertyMock, patch

import psycopg
import pytest
from psycopg import errors as pg

from app.core.exceptions import (
    ConflictoError,
    ErrorDeBaseDeDatosError,
    ErrorDeValidacionError,
    ServicioNoDisponibleError,
    SolicitudInvalidaError,
)
from app.database.errors import traducir_error_bd


@contextmanager
def error_bd(clase, constraint=None):
    """Crea un error de psycopg simulando el nombre de la restricción."""
    diag = SimpleNamespace(constraint_name=constraint)
    with patch.object(clase, "diag", new_callable=PropertyMock, return_value=diag):
        yield clase("fallo de prueba con detalle interno")


def test_username_duplicado_es_conflicto():
    with error_bd(pg.UniqueViolation, "ux_usuario_username_lower") as exc:
        resultado = traducir_error_bd(exc)
    assert isinstance(resultado, ConflictoError)
    assert resultado.status_code == 409
    assert resultado.constraint == "ux_usuario_username_lower"
    assert "nombre de usuario" in resultado.message


@pytest.mark.parametrize(
    ("clase", "esperada", "status"),
    [
        (pg.CheckViolation, ErrorDeValidacionError, 422),
        (pg.ForeignKeyViolation, ErrorDeValidacionError, 422),
        (pg.NotNullViolation, ErrorDeValidacionError, 422),
        (pg.InvalidTextRepresentation, SolicitudInvalidaError, 400),
        (psycopg.OperationalError, ServicioNoDisponibleError, 503),
        (psycopg.ProgrammingError, ErrorDeBaseDeDatosError, 500),
    ],
)
def test_traduccion_por_tipo(clase, esperada, status):
    with error_bd(clase) as exc:
        resultado = traducir_error_bd(exc)
    assert isinstance(resultado, esperada)
    assert resultado.status_code == status


def test_no_expone_el_texto_de_la_bd():
    with error_bd(pg.CheckViolation) as exc:
        resultado = traducir_error_bd(exc)
    assert "detalle interno" not in resultado.message


def test_mensaje_duplicado_es_conflicto():
    with error_bd(pg.UniqueViolation, "mensaje_conversacion_id_id_cliente_key") as exc:
        resultado = traducir_error_bd(exc)
    assert resultado.status_code == 409
    assert resultado.constraint == "mensaje_conversacion_id_id_cliente_key"
