"""Excepciones propias de Xend. Cada una sabe su código HTTP y su código de error."""


class XendError(Exception):
    """Base de todos los errores controlados de la aplicación."""

    status_code: int = 500
    code: str = "error_interno"
    default_message: str = "Error interno del servidor."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class SolicitudInvalidaError(XendError):
    status_code = 400
    code = "solicitud_invalida"
    default_message = "La solicitud no es válida."


class NoAutenticadoError(XendError):
    status_code = 401
    code = "no_autenticado"
    default_message = "Credenciales inválidas o ausentes."


class PermisoDenegadoError(XendError):
    status_code = 403
    code = "permiso_denegado"
    default_message = "No tienes permiso para realizar esta acción."


class ConversacionNoAutorizadaError(PermisoDenegadoError):
    code = "conversacion_no_autorizada"
    default_message = "No eres participante de esta conversación."


class RecursoNoEncontradoError(XendError):
    status_code = 404
    code = "no_encontrado"
    default_message = "El recurso solicitado no existe."


class ConflictoError(XendError):
    status_code = 409
    code = "conflicto"
    default_message = "El recurso ya existe."

    def __init__(self, message: str | None = None, *, constraint: str | None = None) -> None:
        super().__init__(message)
        self.constraint = constraint  # permite al repositorio decidir un reintento


class ArchivoDemasiadoGrandeError(XendError):
    status_code = 413
    code = "archivo_demasiado_grande"

    def __init__(self, tamano_bytes: int, maximo_bytes: int) -> None:
        self.tamano_bytes = tamano_bytes
        self.maximo_bytes = maximo_bytes
        super().__init__(
            f"El archivo pesa {tamano_bytes / 1024**3:.2f} GB y el máximo "
            f"permitido es {maximo_bytes / 1024**3:.2f} GB."
        )


class ErrorDeValidacionError(XendError):
    status_code = 422
    code = "validacion_fallida"
    default_message = "Los datos enviados no son válidos."


class ErrorDeBaseDeDatosError(XendError):
    status_code = 500
    code = "error_base_datos"
    default_message = "Error al acceder a los datos."


class ServicioNoDisponibleError(XendError):
    status_code = 503
    code = "servicio_no_disponible"
    default_message = "El servicio de datos no está disponible. Intenta de nuevo."
