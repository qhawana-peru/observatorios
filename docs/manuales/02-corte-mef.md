# Manual 02 · Corte semanal del MEF (El Niño)

**Qué es:** incorporar cada semana la ejecución del Programa Presupuestal 0068 al observatorio El Niño.
**Cada cuánto:** lunes. Debe quedar revisado antes de las 12:00.
**Tiempo:** 10 minutos si la descarga automática funciona; 15 minutos más si hay que descargar a mano.
**Quién:** las dos personas de finanzas públicas, en semanas alternas. Quien no descarga, revisa.
**Detalle completo:** guía de descarga del MEF (`el-nino/` y el documento 02b).

## Paso a paso (caso normal)

1. Los lunes a las 8:00, la automatización **Descargar corte del MEF** baja los siete archivos (D1 a D7) y abre una propuesta en la carpeta `el-nino/fuentes/mef/AAAA-MM-DD`.
2. Entra a **Pull requests** y abre la propuesta del día.
3. Lee el comentario de la **validación**: corre los seis controles (encabezado, total de control, partes que suman el todo, páginas completas, avance recalculado y cambios bruscos).
   - **Todo en verde:** pasa al paso 4.
   - **Algún control en rojo:** no apruebes. Mira la tabla de problemas abajo.
4. Si la validación marca **cambios bruscos** (PIM de un pliego que cambió más de 10 %), no es un error: anótalo en la propuesta como comentario para el análisis.
5. Pide revisión a la otra persona de finanzas o del comité. Ella aprueba y une (manual 04). El sitio se actualiza solo en unos minutos.

## Si la descarga automática falla

Aparece un aviso (issue) con la etiqueta `descarga-manual`.

1. Abre los siete enlaces directos de la guía de descarga, uno por uno, desde tu computadora. Cada uno baja un archivo .xls.
2. **No los abras en Excel.** Renómbralos: `AAAAMMDD_PP0068_<código>_<detalle>_p1de1.xls` (por ejemplo `20261026_PP0068_D2_GR-actividades_p1de1.xls`).
3. Sube los siete a `el-nino/fuentes/mef/AAAA-MM-DD/` con **Add file › Upload files**, en una rama nueva, y abre la propuesta. La validación corre igual.
4. Cierra el aviso con un comentario que diga que se hizo a mano.

## Qué puede salir mal

| Problema | Qué hacer |
|---|---|
| No apareció ninguna propuesta ni aviso el lunes | Revisa **Actions › Descargar corte del MEF**. Si falló por permisos, falta el paso 6b de la guía de administración. Puedes lanzarla a mano con **Run workflow**. |
| Falta el filtro del PP 0068 (el total ronda S/ 289 mil millones) | Archivo equivocado: descarga de nuevo esa ruta. |
| Las partes no suman el todo | Descarga de nuevo los dos archivos del par (D2/D3, D4/D5 o D6/D7) en la misma sesión. |
| El MEF no responde | Reintenta en una hora. Si sigue, descarga el martes y anótalo en la bitácora. |
| Un archivo se abrió y guardó en Excel | Descárgalo de nuevo; el validador solo acepta el original. |
