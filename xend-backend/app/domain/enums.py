"""Tipos enumerados del dominio. Sus valores coinciden con los ENUM de PostgreSQL."""

from enum import StrEnum


class EstadoCuenta(StrEnum):
    ACTIVA = "activa"
    SUSPENDIDA = "suspendida"
    ELIMINADA = "eliminada"


class Plataforma(StrEnum):
    ANDROID = "android"
    WEB = "web"
    WINDOWS = "windows"
    LINUX = "linux"


class Visibilidad(StrEnum):
    TODOS = "todos"
    CONTACTOS = "contactos"
    NADIE = "nadie"


class EstadoSubida(StrEnum):
    PENDIENTE = "pendiente"
    SUBIENDO = "subiendo"
    COMPLETO = "completo"
    FALLIDO = "fallido"
    ELIMINADO = "eliminado"


class TipoConversacion(StrEnum):
    INDIVIDUAL = "individual"
    GRUPO = "grupo"


class RolParticipante(StrEnum):
    MIEMBRO = "miembro"
    ADMIN = "admin"
    PROPIETARIO = "propietario"


class TipoMensaje(StrEnum):
    TEXTO = "texto"
    ARCHIVO = "archivo"
    STICKER = "sticker"
    SISTEMA = "sistema"


class FormatoMensaje(StrEnum):
    PLANO = "plano"
    MARKDOWN = "markdown"


class TipoEstado(StrEnum):
    TEXTO = "texto"
    IMAGEN = "imagen"
    VIDEO = "video"
