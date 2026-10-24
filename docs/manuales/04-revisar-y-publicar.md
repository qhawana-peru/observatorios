# Manual 04 · Revisar, aprobar y publicar

**Qué es:** ser los "cuatro ojos". Nada entra al sitio sin que otra persona lo revise. GitHub no deja aprobar tu propia propuesta.
**Tiempo:** 10 a 20 minutos por propuesta.
**Quién:** comité editorial (y datos para cambios técnicos).

## Cómo moverse en GitHub (para no perderse)

**La regla de oro:** antes de editar o subir cualquier cosa, mira el botón de rama. Si dice **main**, cámbialo a tu rama. Todo lo que se hace en **main** se publica sin revisión.

### Volver a la portada del repositorio
Desde cualquier página: arriba a la izquierda dice `qhawana-peru / observatorios`. Haz clic en **observatorios**.

### Crear una rama nueva (antes de empezar un cambio)
1. En la portada, haz clic en el botón de rama (dice **main** con una flechita), arriba de la lista de carpetas.
2. Escribe el nombre de la rama nueva en el cuadro, sin espacios (por ejemplo `ajustes-24oct` o `corte-incendios-2026-10-30`).
3. Haz clic en **Create branch: … from main**. El botón ya muestra el nombre de tu rama.

### Cambiar a una rama que ya existe
En la portada, botón de rama › elige la rama de la lista. Si no aparece, escribe parte de su nombre en el cuadro.

### Abrir y editar un archivo
1. Con el botón en tu rama, haz clic en las carpetas hasta llegar al archivo. También puedes usar el buscador **Go to file** (arriba de la lista de la izquierda) y escribir parte del nombre.
2. Con el archivo abierto, haz clic en el **lápiz** ✏️ arriba a la derecha del texto ("Edit this file").
3. Revisa que junto al nombre del archivo diga `in <tu rama>`. Si dice `in main`, cancela y vuelve a cambiar de rama.
4. Para ir al final del texto: haz clic dentro y pulsa **Ctrl + End** (en Mac, **Cmd + flecha abajo**).

### Crear un archivo nuevo o subir archivos
Con el botón en tu rama, entra a la carpeta donde va el archivo y pulsa **Add file** (arriba a la derecha de la lista):
- **Create new file:** escribes el nombre. Si pones `carpeta/archivo.md`, cada `/` crea una carpeta.
- **Upload files:** arrastras archivos o carpetas. Ojo: Windows esconde las carpetas que empiezan con punto (como `.github`); esas se crean con *Create new file*.

### Guardar (commit)
Al pulsar **Commit changes...** aparece una ventana con dos opciones:
- **Commit directly to the `<rama>` branch:** correcto si la rama es la tuya. **Nunca si dice main.**
- **Create a new branch for this commit and start a pull request:** úsala si te olvidaste de crear la rama antes. Pon un nombre y pulsa **Propose changes**.

### Abrir la propuesta (pull request)
1. Pestaña **Pull requests** (arriba). Si acabas de guardar en tu rama, aparece una franja amarilla con el botón **Compare & pull request**: púlsalo.
2. Si no aparece: **New pull request** › en **compare** elige tu rama (en **base** debe quedar `main`).
3. Escribe un título claro y en la descripción qué cambiaste y por qué. Pulsa **Create pull request**.
4. A la derecha, en **Reviewers**, elige a la persona que revisará.

### Saber si algo funcionó
- Abajo de la propuesta, los **checks**: círculo amarillo = corriendo; ✔ verde = bien; ✖ rojo = falló (haz clic en **Details** para ver por qué).
- Pestaña **Actions:** lista de todas las automatizaciones, con su resultado.

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
