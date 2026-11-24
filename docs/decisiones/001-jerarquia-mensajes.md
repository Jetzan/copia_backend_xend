# 001 · Jerarquía de la clase Mensaje

## Contexto

La base de datos distingue `tipo` (texto, archivo, sticker, sistema) y `formato` (plano, markdown). Todas las filas de la tabla `mensaje` tienen las columnas `contenido_cifrado` y `formato`, pero `contenido_cifrado` es opcional según el tipo (por ejemplo, un sticker no lo lleva).

El profesor exige implementar herencia y polimorfismo.

## Alternativas

**A. Subclases por combinación de tipo y formato, con fábrica.**

Crear clases específicas para las combinaciones de tipo y formato, por ejemplo `MensajeTextoPlano` y `MensajeTextoMarkdown`, utilizando una fábrica para instanciarlas.

Ventajas:
- Cada combinación podría tener comportamientos especializados.
- El formato podría resolverse mediante clases concretas.

Desventajas:
- Aumenta considerablemente el número de clases.
- Genera combinaciones innecesarias entre tipos y formatos.
- Complica el mantenimiento y la incorporación de nuevos formatos.

**B. Subclases por tipo, con contenido y formato en la clase base.**

Crear una clase base `Mensaje` con los atributos comunes, incluyendo `contenido` y `formato`, y subclases según el tipo: `MensajeTexto`, `MensajeArchivo`, `MensajeSticker` y `MensajeSistema`.

Ventajas:
- Mantiene una jerarquía sencilla.
- Evita duplicar atributos comunes.
- Es consistente con la estructura de la base de datos.
- Permite agregar nuevos tipos sin crear combinaciones de clases por formato.

Desventajas:
- La clase base contiene atributos que algunos tipos pueden utilizar de manera limitada o no utilizar.
- Las subclases deben validar qué atributos y comportamientos son permitidos según su tipo.

## Decisión

**B. Subclases por tipo, con contenido y formato en la clase base.**

Se implementará una clase base `Mensaje` que concentrará los atributos comunes, incluyendo `contenido` (texto legible, `str | None`) y `formato`. De ella heredarán las clases `MensajeTexto`, `MensajeArchivo`, `MensajeSticker` y `MensajeSistema`.

## Justificación

Se eligió esta alternativa porque corresponde mejor a la estructura de la base de datos, en la cual todas las filas de mensajes cuentan con las columnas `contenido_cifrado` y `formato`, aunque el contenido puede ser nulo dependiendo del tipo de mensaje.

La restricción `ck_mensaje_contenido` exige contenido en los tipos `texto` y `sistema`, exige `sticker_id` en los sticker y permite contenido opcional en los de tipo `archivo`; por eso el contenido no puede ser exclusivo de `MensajeTexto`.

La distinción entre `tipo` y `formato` se mantendrá: el tipo determinará la clase concreta y sus comportamientos específicos, mientras que el formato será un atributo que indique cómo debe interpretarse el contenido textual cuando corresponda.

El polimorfismo se aplicará mediante métodos comunes como `validar()` y `serializar()`, que podrán ser implementados o sobrescritos por las subclases según las necesidades de cada tipo de mensaje. De esta forma, cada clase podrá manejar sus propias reglas sin perder una interfaz común.

Esta alternativa evita crear una clase por cada combinación de tipo y formato, reduce la complejidad de la jerarquía y facilita el mantenimiento y la futura incorporación de funcionalidades.

## Consecuencias

- `Mensaje` contendrá los atributos comunes, incluyendo `contenido` de tipo `str | None` y `formato`. El repositorio se encargará de convertir desde y hacia la columna `contenido_cifrado`.
- Las subclases representarán los diferentes tipos de mensaje y sus reglas específicas.
- El formato se conservará al leer y escribir los datos en la base de datos.
- La validación determinará qué atributos son obligatorios, opcionales o aplicables según el tipo de mensaje.
- El procesamiento de texto plano y Markdown se realizará cuando corresponda, sin necesidad de crear nuevas subclases por formato.
- Flutter será responsable de la presentación visual de los mensajes; el backend se enfocará en validación, procesamiento, serialización y lógica de negocio.
- El repositorio necesitará una fábrica que elija la subclase según el valor de `tipo` al convertir filas en objetos.
- La conversión entre bytes y texto se realizará en el repositorio. Cuando se implemente el cifrado real, el repositorio también será responsable de integrar los procesos de cifrado y descifrado, manteniendo el dominio independiente de estos mecanismos.