"""Handlers que convierten excepciones en respuestas JSON uniformes."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import XendError

logger = logging.getLogger(__name__)


def _respuesta(status: int, code: str, message: str, details: list | None = None) -> JSONResponse:
    cuerpo: dict = {"code": code, "message": message}
    if details:
        cuerpo["details"] = details
    return JSONResponse(status_code=status, content={"error": cuerpo})


async def manejar_xend_error(request: Request, exc: XendError) -> JSONResponse:
    return _respuesta(exc.status_code, exc.code, exc.message)


async def manejar_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Solo campo y mensaje: nunca el valor recibido, que podría ser una contraseña.
    detalles = [
        {"campo": ".".join(str(p) for p in e["loc"]), "mensaje": e["msg"]} for e in exc.errors()
    ]
    return _respuesta(422, "validacion_fallida", "Los datos enviados no son válidos.", detalles)


async def manejar_error_inesperado(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return _respuesta(500, "error_interno", "Error interno del servidor.")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(XendError, manejar_xend_error)
    app.add_exception_handler(RequestValidationError, manejar_validacion)
    app.add_exception_handler(Exception, manejar_error_inesperado)
