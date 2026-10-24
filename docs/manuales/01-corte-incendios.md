# Manual 01 · Corte de incendios (SERFOR)

**Qué es:** actualizar el monitor de incendios con lo último que publica SERFOR.
**Cada cuánto:** una vez por semana en temporada (julio a noviembre), y también cuando haya una noticia que lo pida.
**Tiempo:** unos 20 minutos.
**Quién:** una persona de datos hace el corte y otra del comité lo revisa.
**Necesitas:** una computadora con Chrome, Edge o Firefox, y tu cuenta de GitHub en la organización.

## Por qué en tu navegador

El servicio de SERFOR no respondió a los servidores en la nube que probamos, pero sí responde a un navegador común. Por eso la consulta la hace una persona y el resto lo hace la automatización. (Falta probar si responde a los servidores de GitHub: si responde, este paso también se puede automatizar.)

## Paso a paso

### A. Consultar a SERFOR (5 min)

1. Abre en el navegador: `https://geo.serfor.gob.pe/geoservicios/rest/services/UFMS/Incendios_SAMIv21/MapServer`. Verás una página de texto técnica: es normal.
2. En otra pestaña, abre el archivo `herramientas/serfor_consulta.js` del repositorio y pulsa el botón **Copy raw file** (dos hojitas, arriba a la derecha del archivo).
3. Vuelve a la pestaña de SERFOR y abre la consola del navegador: **F12** en Windows, o **Cmd + Opción + J** en Mac. Elige la pestaña **Console** (Consola).
4. Pega el código y pulsa **Enter**. Si el navegador dice que no permite pegar, escribe `allow pasting` (o `permitir pegar`), Enter, y vuelve a pegar.
5. Espera de 30 a 60 segundos. Se descarga un archivo `serfor_AAAA-MM-DD.json`. Ese archivo contiene solo conteos, ningún dato de personas.

### B. Subirlo al repositorio (5 min)

6. En GitHub, entra a la carpeta `incendios/cortes/` del repositorio.
7. **Add file › Upload files** y arrastra el JSON.
8. Abajo, elige **Create a new branch for this commit and start a pull request**. Nombre de la rama: `corte-incendios-AAAA-MM-DD` (con la fecha del archivo). Pulsa **Propose changes** y luego **Create pull request**.
9. Espera uno o dos minutos. La automatización **Actualizar incendios** recalcula los datos y agrega un cambio a tu propuesta. En la pestaña **Checks** (o **Actions**) verás un resumen como este:
   `Cusco: 54 alertas; focos Suomi NPP últimos 7 días: 175 (7 días previos: 431, -59 %); faltaría +6 a +10 %.`

### C. Escribir la lectura del corte (10 min)

10. En la propuesta, pestaña **Files changed**, busca `incendios/config/sitio.json`, menú **⋯ › Edit file**.
11. Escribe en `nota_corte` un párrafo de 3 a 5 líneas. Reglas:
    - Solo cifras de SERFOR que estén en el corte. Nada de prensa.
    - Di qué cambió desde el corte anterior y en qué región.
    - Si los focos bajan en época de lluvias, recuerda que las nubes impiden al satélite ver el fuego.
    - No des la temporada por terminada mientras haya focos.
    - Si no hay nada que destacar, deja `""`.
12. **Commit changes** en la misma rama.
13. Pide revisión a otra persona del comité (**Reviewers**, a la derecha). Ella sigue el manual 04.

## Qué puede salir mal

| Problema | Qué hacer |
|---|---|
| La consola muestra un error en rojo que menciona SERFOR | El servicio está caído o lento. Reintenta en una hora. Si cambió la dirección del servicio, avisa: hay que actualizar el script. |
| No se descarga el archivo | Revisa si el navegador bloqueó la descarga (icono en la barra de direcciones) y permítela. |
| La automatización falla con "El corte ya está en seguimiento" | Ya se hizo un corte con esa fecha. Cierra la propuesta, o si quieres repetirlo, pide a datos que quite esa fila a mano. |
| La automatización falla en "Probar" | Algo raro hay en los datos (por ejemplo, SERFOR devolvió un año vacío). No unas la propuesta; avisa a datos. |
| Una región no tiene alertas | Es normal al final de la temporada. La página lo muestra como "Sin alertas". |
| Las cifras de días pasados no coinciden con el corte anterior | SERFOR completa sus registros con días de retraso. No se corrigen los cortes pasados: el seguimiento guarda lo publicado en cada fecha. Si la diferencia es grande, anótala en la bitácora. |

## Antes de la temporada siguiente

- Agrega 2026 a la serie histórica (pasa a tener total anual) y revisa si SERFOR cambió de satélites.
- Para agregar una región, añádela en `REGIONES` del script y en la página: pide ayuda a datos.
