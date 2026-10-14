# Guía del comité editorial

El comité decide qué se publica. Nada entra al sitio sin la aprobación de un miembro que no preparó el cambio; la herramienta lo impide.

## Revisar y aprobar una propuesta

1. Pestaña **Pull requests**. Las que esperan tu revisión aparecen con tu equipo como revisor.
2. Lee el comentario de validación automática (si es un corte del MEF) y la lista de verificación de la propuesta.
3. Pestaña **Files changed**: ahí ves exactamente qué entra. En un hecho nuevo, abre el enlace de la fuente y compara el texto con la cita.
4. Si está bien: **Review changes › Approve › Submit review**, y luego **Merge pull request**. El sitio se actualiza solo en unos minutos.
5. Si no: **Review changes › Request changes**, explicando qué falta. Quien la preparó la corrige en la misma propuesta.

## Qué revisar según el tipo

| Propuesta | Qué mirar |
| --- | --- |
| Corte del MEF | La validación dice "todo cuadra". Los avisos de cambios bruscos tienen una explicación anotada o se dejan como "por revisar". |
| Hecho en la bitácora | La fuente es primaria. El texto dice lo que dice la cita, sin adjetivos. La fecha es la del documento. |
| Corrección | Hay una fuente que la respalda. Queda anotada en `docs/bitacora-cambios.md` con fecha y qué cambió. |
| Cambio de método o de textos | Lo aprueban al menos dos miembros del comité, y se anota en la bitácora de cambios. |

## Reglas

- No apruebas lo que preparaste (GitHub tampoco te deja).
- Si tienes un conflicto de interés con el territorio o la entidad de la propuesta, no la revisas.
- Todo hallazgo sobre un gobierno se publica con la misma ficha que para los demás.
- Antes de publicar un hallazgo negativo sobre una entidad, se revisa su portal y su respuesta pública más reciente.
- Las correcciones se publican en 48 horas.

## Pasar el sitio de "versión preliminar" a "publicado"

Cuando el comité apruebe el método y el primer corte, cambia en `el-nino/config/sitio.json` el valor `"estado": "preliminar"` por `"estado": "publicado"`, mediante una propuesta. Desde entonces, el sitio dice que las cifras están aprobadas por el comité.
