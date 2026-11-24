"""Configuración compartida de pytest."""

import os

# Valores ficticios para que Settings() se pueda construir sin .env (local y CI).
os.environ.setdefault("XEND_POSTGRES_USER", "usuario_de_prueba")
os.environ.setdefault("XEND_POSTGRES_PASSWORD", "clave_de_prueba")
os.environ.setdefault("XEND_MONGO_URI", "mongodb://localhost:27017")
