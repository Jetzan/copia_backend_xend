"""Traduce errores de PostgreSQL (psycopg) a excepciones de Xend."""

import psycopg
from psycopg import errors as pg

from app.core.exceptions import (
    ConflictoError,
    ErrorDeBaseDeDatosError,
    ErrorDeValidacionError,
    ServicioNoDisponibleError,
    SolicitudInvalidaError,
    XendError,
)

_MENSAJES_UNICOS = {
    "ux_usuario_username_lower": "El nombre de usuario ya está en uso.",
    "ux_credencial_correo_lower": "El correo ya está registrado.",
    "usuario_xnd_id_key": "El identificador XND ya existe.",
    "usuario_credencial_telefono_hash_key": "El teléfono ya está registrado.",
    "conversacion_clave_individual_key": "Ya existe un chat entre estos usuarios.",
    "mensaje_conversacion_id_id_cliente_key": "El mensaje ya fue enviado.",
}


def traducir_error_bd(exc: psycopg.Error) -> XendError:
    """Convierte un error de psycopg en un XendError sin exponer el texto de la BD."""
    constraint = getattr(exc.diag, "constraint_name", None)

    if isinstance(exc, pg.UniqueViolation):  # 23505
        mensaje = _MENSAJES_UNICOS.get(constraint, "El recurso ya existe.")
        return ConflictoError(mensaje, constraint=constraint)
    if isinstance(exc, pg.CheckViolation):  # 23514
        return ErrorDeValidacionError("Los datos no cumplen las reglas del sistema.")
    if isinstance(exc, pg.ForeignKeyViolation):  # 23503
        return ErrorDeValidacionError("Se hace referencia a un recurso que no existe.")
    if isinstance(exc, pg.NotNullViolation):  # 23502
        return ErrorDeValidacionError("Falta un campo obligatorio.")
    if isinstance(exc, pg.InvalidTextRepresentation):  # 22P02
        return SolicitudInvalidaError("Un valor tiene un formato incorrecto.")
    if isinstance(exc, psycopg.OperationalError):  # conexión caída, nodo no disponible
        return ServicioNoDisponibleError()
    return ErrorDeBaseDeDatosError()
