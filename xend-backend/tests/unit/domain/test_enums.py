import pytest

from app.domain.enums import (
    EstadoCuenta,
    EstadoSubida,
    FormatoMensaje,
    Plataforma,
    RolParticipante,
    TipoConversacion,
    TipoEstado,
    TipoMensaje,
    Visibilidad,
)


@pytest.mark.parametrize(
    ("enum", "valores"),
    [
        (EstadoCuenta, {"activa", "suspendida", "eliminada"}),
        (Plataforma, {"android", "web", "windows", "linux"}),
        (Visibilidad, {"todos", "contactos", "nadie"}),
        (EstadoSubida, {"pendiente", "subiendo", "completo", "fallido", "eliminado"}),
        (TipoConversacion, {"individual", "grupo"}),
        (RolParticipante, {"miembro", "admin", "propietario"}),
        (TipoMensaje, {"texto", "archivo", "sticker", "sistema"}),
        (FormatoMensaje, {"plano", "markdown"}),
        (TipoEstado, {"texto", "imagen", "video"}),
    ],
)
def test_valores_coinciden_con_la_bd(enum, valores):
    assert {miembro.value for miembro in enum} == valores


def test_se_construye_desde_el_texto_de_la_bd():
    assert TipoMensaje("sticker") is TipoMensaje.STICKER


def test_valor_invalido_falla():
    with pytest.raises(ValueError):
        TipoMensaje("audio")
