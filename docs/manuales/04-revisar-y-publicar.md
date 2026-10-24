# Manual 04 · Revisar, aprobar y publicar

**Qué es:** ser los "cuatro ojos". Nada entra al sitio sin que otra persona lo revise. GitHub no deja aprobar tu propia propuesta.
**Tiempo:** 10 a 20 minutos por propuesta.
**Quién:** comité editorial (y datos para cambios técnicos).

## Qué revisar

1. **Checks en verde.** Abajo de la propuesta, la validación (`validar`) y, si aplica, la automatización deben estar en verde. Si alguno está en rojo, no apruebes.
2. **Files changed.** Lee qué cambió. Preguntas guía:
   - ¿Cada cifra nueva tiene fuente oficial y fecha de corte?
   - ¿Hay alguna cifra de prensa fuera de las pistas?
   - ¿Hay datos personales o nombres de víctimas?
   - ¿La lectura del corte dice algo que las cifras no sostienen?
   - ¿Se cambiaron cifras de cortes pasados? No se debe: solo se anota la revisión en la bitácora.
3. **Vista previa.** Si cambia la página, mira cómo queda después de unir y avisa si algo se ve mal.

## Aprobar y unir

1. **Files changed › Review changes › Approve**, con un comentario breve de qué revisaste.
2. Si pides cambios: **Request changes** y explica qué falta. Quien propuso corrige en la misma rama.
3. Con la aprobación y los checks en verde: **Merge pull request › Confirm merge**.
4. En unos 2 minutos corre **Publicar sitio**. Abre `https://qhawana-peru.github.io/observatorios/` y revisa la fecha de corte. Si no cambia, recarga sin caché (**Ctrl + Shift + R**, o **Cmd + Shift + R** en Mac).

## Qué puede salir mal

| Problema | Qué hacer |
|---|---|
| "This branch has conflicts" | Dos propuestas tocaron el mismo archivo. Pulsa **Resolve conflicts**: GitHub muestra las dos versiones entre `<<<<<<<` y `>>>>>>>`. Deja el texto correcto, borra las marcas y pulsa **Mark as resolved › Commit merge**. Si son archivos de datos (CSV), mejor pide a datos que lo resuelva. |
| El botón Merge está gris | Falta una aprobación o un check en verde. Lee el mensaje encima del botón. |
| El sitio no se actualizó | **Actions › Publicar sitio**: si falló, abre el error y avisa a datos. Puedes relanzarlo con **Re-run jobs**. |
| Se publicó algo con un error | No lo borres del historial. Abre una propuesta que lo corrija y anota en `docs/bitacora-cambios.md` qué estaba mal, desde cuándo y qué se corrigió. Corregir a la vista es parte de la credibilidad. |

## La bitácora

Todo cambio de método, corrección de error o decisión del comité se anota en `docs/bitacora-cambios.md`, con fecha, qué cambió y por qué. Los cortes rutinarios no hace falta anotarlos, salvo que haya algo raro (revisiones grandes de la fuente, una región sin datos, etc.).
