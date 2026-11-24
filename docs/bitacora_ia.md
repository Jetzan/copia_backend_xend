# Bitácora de uso de IA

| Fecha | Integrante | Herramienta | Propósito | Resultado (aceptado / modificado / descartado y por qué) | Verificación | Commit |
|---|---|---|---|---|---|---|
| 2026-11-14 | Jetzan Esquivel | Claude (chat) | Estructura de carpetas del backend FastAPI, pyproject.toml y comandos de entorno | Aceptado con ajustes propios (renombré logging.py a logging_config.py, agregué crypto.py y analysis.py) | Ejecuté pytest, ruff, bandit y pip-audit sin errores | (843fcfb) |
| 2026-11-14 | Jetzan Esquivel | Claude (chat) | Configuración de Git/GitHub, .gitignore y plantillas de PR y CI | Aceptado; corregí el .gitignore para carpetas data/ anidadas | git status limpio, push exitoso | 73d5465 |
| 2026-11-16 | Jetzan Esquivel | Claude (chat) | config.py (pydantic-settings), jerarquía de excepciones, traducción de errores de PostgreSQL, handlers HTTP y CORS | Aceptado; verifiqué los nombres de restricciones contra la BD real y agregué la de mensajes duplicados | 28 tests, ruff y bandit sin errores; restricciones comprobadas en psql | e5e9066, 76ae0ff |
| 2026-11-20 | Jetzan Esquivel | Claude (chat) | Enums del dominio (StrEnum) equivalentes a los tipos ENUM de PostgreSQL | Aceptado; comparé los valores contra pg_enum en mi BD local | 11 tests nuevos, ruff y bandit sin errores; consulta a pg_enum coincide | 1bee749 |
| 2026-11-21 | Jetzan Esquivel | Claude (chat) | Estructura del registro de decisión 001 y revisión de huecos en la justificación | La decisión (B) y su justificación son mías; la IA señaló que el contenido no es exclusivo de MensajeTexto y que faltaban la restricción ck_mensaje_contenido y la sección de alternativas, y acepté esos ajustes | Contrasté con el esquema SQL y los datos de prueba de Hugo | 2f23225 |
