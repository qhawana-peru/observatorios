# Manual 06 · ENFEN, IGP y CENEPRED (El Niño)

**Qué es:** mantener al día el pronóstico (ENFEN), los índices del mar (IGP) y la exposición (CENEPRED) que usa el Observatorio El Niño.
**Quién:** análisis de peligro y riesgo. Revisa otra persona del comité (manual 04).
**Necesitas:** navegador y tu cuenta de GitHub. No hace falta programar.

| Fuente | Cada cuánto | Tiempo | Dónde se registra |
|---|---|---|---|
| Comunicado ENFEN | Quincenal (el próximo es el 30 oct 2026) | 10 min | `el-nino/datos/hechos.csv` y `el-nino/config/contexto.json` |
| Informe técnico IGP | Mensual | 10 min | `el-nino/datos/hechos.csv` |
| Escenario de riesgo CENEPRED | Cuando el CENEPRED publique una versión nueva | 1 a 2 horas | `el-nino/datos/exposicion_cenepred.csv` |

**Regla de oro:** el pronunciamiento oficial sobre El Niño es el del ENFEN. El IGP es un insumo técnico y el CENEPRED estima el riesgo. Si dos de ellos difieren, se muestran ambos y se explica la diferencia. No se elige uno.

## A. Comunicado ENFEN (10 min)

1. Abre https://enfen.imarpe.gob.pe/comunicados/ y descarga el comunicado nuevo.
2. Crea una rama, por ejemplo `enfen-19`, siguiendo el manual 04.
3. En `el-nino/datos/hechos.csv`, busca la fila del próximo comunicado (por ejemplo `P19`, con `futuro` = `si`) y complétala:
   - `fecha` y `etiqueta_fecha`, con la fecha real del comunicado.
   - `texto`: qué pronostica, en una o dos líneas y en palabras propias.
   - `cambio`: qué cambió frente al comunicado anterior (caudales, regiones).
   - `fuente_url`: el enlace de descarga del comunicado.
   - `costero` y `global`: magnitud de 0 a 4. Para el costero: 0 neutro, 1 débil, 2 moderado, 3 fuerte, 4 extraordinario. Para el global: 0 neutro, 1 débil, 2 moderado, 3 fuerte, 4 muy fuerte. Si el comunicado da un rango, usa el valor medio, por ejemplo 3.5.
   - `futuro`: vacío.
4. Agrega una fila nueva para el comunicado siguiente, con `futuro` = `si`.
5. En `el-nino/config/contexto.json`, actualiza `_fuentes.pronostico` y las frases de `pronostico` por región, sobre todo lluvias y caudales.
6. Abre la propuesta. La validación corre sola.

**Pendiente al 27 oct:** el comunicado N.º 19 sale el viernes 30. Ese mismo día vence el DS 124-2026-PCM: registra si se prorroga (hecho de la franja de respuesta).

## B. Informe técnico del IGP (10 min)

1. Busca el informe más reciente en https://repositorio.igp.gob.pe, con la búsqueda "Informe Técnico PpR/El Niño-IGP/2026".
2. Copia de la Tabla 1 el último ICEN mensual (valor y categoría) y de la Tabla 2 los valores temporales.
3. Agrega una fila en `hechos.csv` con `franja` = `peligro`, `costero` y `global` vacíos (así no se mezcla con la escala del ENFEN), y un texto que diga que es un insumo técnico.
4. **Ojo:** el IGP publica dos índices, el ICEN clásico y el ICEN relativo (ICENr, con la climatología 1991-2020), que dan valores distintos. Cita siempre el ICEN y menciona el ICENr como lo que es. Si la categoría no corresponde al valor (en el informe 2026-08, el ICEN de julio es 3,38 °C y figura como "cálida fuerte", aunque pasa de 3,0), no publiques la categoría: anótalo en la bitácora y pregunta al IGP.

## C. Escenario del CENEPRED (1 a 2 horas)

Es la tarea más delicada: cada cifra de exposición sale de aquí.

1. **Encontrar el documento.** Revisa la biblioteca del SIGRID (https://sigrid.cenepred.gob.pe/sigridv3/) y las noticias del CENEPRED en gob.pe. Si la prensa menciona una "actualización", busca el PDF oficial: la nota de prensa sola no sirve.
2. **Preferir el Excel.** Algunos estudios publican sus tablas en un archivo `NN_tabla.zip`, en el enlace "Excel" de la ficha del documento. Es mejor que copiar del PDF.
3. **Guardar el original.** Sube el PDF (o el zip) a `el-nino/fuentes/cenepred/AAAA-MM-DD_<nombre-corto>.pdf`, con **Add file › Upload files**.
4. **Transcribir.** En `el-nino/datos/exposicion_cenepred.csv`, agrega filas con una letra de estudio nueva (C, D…), una fila por departamento y por tabla, y la fila `TOTAL NACIONAL` con los totales impresos. Llena `tabla` y `pagina`.
5. **Controlar.** Si transcribiste tablas completas, agrega la letra del estudio a `COMPLETOS` en `herramientas/validar_cenepred.py` (o pide a datos que lo haga). El validador comprueba que las filas sumen el total y avisa si una cifra está mal copiada.
6. **Cotejar.** Otra persona compara cada fila con el PDF y cambia `revision_humana` a `hecha`.
7. **Cambiar el escenario de la página.** En `el-nino/config/brechas.json`, cambia `escenario_principal` o `escenario_secundario` a la letra nueva. Si el recuadro "sin revisión del comité" ya no aplica, cambia `revision.estado` y `revision.texto`.
8. Anota en la bitácora qué versión entró y por qué.

### Qué hacer si las versiones no coinciden

Es lo normal: cada estudio usa otro pronóstico y otra unidad (distrito o centro poblado). No se corrige ni se promedia. Se muestra la versión vigente y se explica la diferencia en `docs/el-nino-brechas.md`.

## Qué puede salir mal

| Problema | Qué hacer |
|---|---|
| La validación dice "la columna población suma X y el total impreso es Y" | Una fila está mal copiada. Revisa contra el PDF las filas donde los dígitos del número de distritos y de la población pueden haberse pegado. |
| El sitio del ENFEN, el IGP o el SIGRID no abre | Reintenta más tarde. No uses la nota de prensa como fuente de cifras. |
| La prensa da una cifra del CENEPRED que no está en ningún PDF | Es una pista: no se publica. Busca el documento o escribe al CENEPRED. |
