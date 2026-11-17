# Bitácora de cambios

Toda corrección, cambio de método o decisión editorial que afecte lo publicado, con fecha y qué cambió. Lo más reciente arriba.

## 2026-11-17: portada reorganizada (sin revisión del comité ni de cuatro ojos)
- **Orden de los observatorios**, por decisión de Pepe: Museo de la planificación, Observatorio del sistema de salud y Observatorio El Niño.
- **Monitor de incendios forestales fuera del menú.** Queda en pausa al cierre de la temporada; su página y sus datos siguen en `/incendios/`, con un enlace discreto bajo las tarjetas, para no romper los enlaces ya compartidos. Sus pistas vencen el 22 nov.
- **Textos corregidos:** el principio «Cuatro ojos» decía que nada se publica sin una segunda revisión, lo que hoy no se cumple; pasa a «Revisión a la vista» (cada página dice si pasó por el comité y cada cambio queda en la bitácora). «Verifica una pista» (incendios) se reemplaza por «Aporta un documento» (enlaces a planes o reportes no ubicados del museo).

## 2026-11-17: se publica el Observatorio del sistema de salud como versión preliminar (sin revisión del comité ni de cuatro ojos)
- **Nuevo observatorio en `/salud/`**, por decisión de Pepe. Pregunta: ¿quién financia, quién atiende y quién termina pagando? Cinco vistas: diseño formal (rectoría del MINSA y supervisión de SUSALUD sobre todo el sistema; la SBS solo sobre las empresas de seguros), circulación del dinero (incluidos gasto de bolsillo y reembolsos), filtración del bolsillo, mapa de prestadores y tabla.
- **Mapa de prestadores** con la descarga completa de RENIPRESS (SUSALUD) al 16/11/2026: 27 051 establecimientos. 7 003 (26 %, casi todos privados) no traen coordenadas y se ubican en el promedio de su distrito, marcados como aproximados. La descarga original no se sube porque trae datos personales (director, teléfono, RUC); se publica solo lo derivado (`salud/renipress.py`).
- **Lectura del corte:** el 63 % de los establecimientos es privado, pero el 64 % de los 368 hospitales generales (II-1 a III-2) es público. 10 233 de los 17 039 privados son consultorios y 273 de los 404 privados de categoría II o III son especializados (II-E).
- **Cifras de prensa solo como pistas** en las fichas (por ejemplo, las atenciones del FISSAL a julio de 2026 y la espera de citas en EsSalud). El gasto de bolsillo por seguro es de 2019 (DIGEMID) y se rotula como participación en el total, no gasto por persona.
- **Licencia distinta en un archivo:** `salud/geo/departamentos_contornos.json` deriva de juaneladio/peru-geojson (límites del INEI) y mantiene su licencia MPL-2.0.
- **Controles nuevos:** `herramientas/tests/test_salud.py` (puntos cuadran con el resumen y por departamento, coordenadas dentro del Perú, sin datos personales y generación de la página).

## 2026-11-17: se publica el Museo de la planificación como versión preliminar (sin revisión del comité ni de cuatro ojos)
- **Nuevo observatorio en `/planificacion/`**, por decisión de Pepe. Inventario de planes del Estado: 4 planes de país, 40 políticas nacionales (lista de CEPLAN a junio de 2024), el sector Salud completo y los 26 planes regionales (PDRC), cada uno con su fuente oficial y su bitácora de seguimiento. Corte del catálogo: 16/11/2026.
- **Piloto de indicadores y primer hilo:** objetivos e indicadores del PDRC Cajamarca (desde su informe de evaluación 2023-2024) y el hilo de la anemia infantil (PEDN, políticas nacionales, plan multisectorial, ENDES con los dos criterios de medición). Piura y Puno quedan "por catalogar": no se pudieron abrir sus documentos completos.
- **27 indicadores del museo con ficha** (6 activos, 7 en piloto, 11 en revisión, 3 de etapa 2) y 4 descartados con su razón. Método en `docs/planificacion-metodologia.md`.
- **Aviso visible en la página:** versión preliminar, sin revisión del comité; las cifras del piloto están en cotejo manual con sus documentos.
- **Controles nuevos:** `herramientas/tests/test_planificacion.py` (identificadores únicos, referencias, 26 pliegos, fuente en cada pieza, hallazgos completos, estados de KPI y generación de la página).

## 2026-11-17: cortes del MEF del 16 y 17 nov, nueva declaratoria y diseño compartido con el museo (sin revisión de cuatro ojos)
- **MEF: entran los cortes del 16 nov** (descarga del lunes, no publicada) **y del 17 nov** (lanzado a mano). Ambos pasan los seis controles. Al 17 nov: PIM S/ 5,106.6 M, devengado S/ 2,554.9 M (50,0 %). Nacional 41,0 %, municipal 54,9 %, regional 73,1 %. Avisos de cambio de PIM: proyectos del Gobierno Regional de Tumbes de S/ 4.4 M a 5.5 M (16 nov) y a 8.7 M (17 nov), +99 % en dos cortes; actividades municipales de Lambayeque +21 % (16 nov).
- **Nueva declaratoria:** DS N.º 149-2026-PCM (3 nov), 60 días, 1,380 distritos de 191 provincias en 24 departamentos y el Callao. Se registra con la nota de El Peruano; falta enlazar la norma y su anexo, y confirmar si prorroga el DS N.º 124-2026-PCM (vencido el 30 oct) o es una declaratoria nueva. Entre el 31 oct y el 2 nov no hubo declaratoria vigente ubicada.
- **ENFEN N.º 20 (13 nov):** el PDF oficial está publicado en el portal de la Dirección de Hidrografía y Navegación, pero su lectura automática está bloqueada. Su contenido no se publica hasta leerlo en el documento. Las fichas regionales siguen mostrando el pronóstico por región del N.º 17.
- **Emergencias (INDECI):** sin actualizar desde el 23 oct. El portal del INDECI no fue accesible en esta actualización; la sección lo dice con su fecha de revisión.
- **Diseño:** la página de El Niño adopta la paleta y la tipografía del museo de la planificación (noche azul institucional, oro, turquesa, verde andino y magenta; Big Shoulders Display, IBM Plex Sans e IBM Plex Mono), con modo oscuro. No cambian cifras ni método.

## 2026-11-13: cortes atrasados del MEF, incendios y aviso sobre Suomi NPP (sin revisión de cuatro ojos)
- **MEF: entran dos cortes**, el del 9 nov (descarga automática que no llegó a publicarse) y el del 13 nov (lanzado a mano). Ambos pasan los controles; las dos descargas volvieron a fallar solo al abrir la propuesta (paso 6b pendiente).
- **El avance baja de 50,1 % a 49,6 % aunque el devengado sube S/ 95,8 M**, porque el PIM del PP 0068 creció S/ 245 M entre el 2 y el 13 nov. Casi todo en el nivel nacional (+S/ 161,5 M): sector Defensa +S/ 111,2 M y Salud +S/ 35,1 M, en actividades. **Por verificar** qué norma lo explica.
- **ENFEN N.º 20:** previsto para el 13 nov; al cierre el PDF no estaba en el sitio del ENFEN. La prensa ya informa su contenido, pero por regla no se registra hasta tener el documento.
- **Incendios, SERFOR al 13 nov:** 42 alertas y 51 focos de 3 días; totales cuadran.
- **Suomi NPP sin datos desde el 1 nov 2026** en todo el país (consulta por satélite: último foco de NPP el 1 nov; NOAA-20, NOAA-21 y GOES siguen al 13 nov). Como la proyección usa solo NPP, se congelan en el 3 nov `seguimiento_proyeccion.csv`, `serfor_curvas_npp.csv` y `serfor_historial_npp.csv`, y la página lo dice. Sin esto, la página habría mostrado focos −100 % y una proyección falsa. Si NPP no vuelve, la proyección del próximo año necesita otra serie (NOAA-20 desde 2020).
- **Semanas sin corte (4 al 12 nov):** no se pueden reconstruir. Las alertas recientes de SERFOR son una ventana móvil y el MEF solo entrega el acumulado del día. Lo acumulado (focos del año, devengado) sí queda al día con este corte.

## 2026-11-03: corte de incendios (sin revisión de cuatro ojos)
- SERFOR al 3 nov (21:11). Los totales por departamento cuadran con los nacionales (38 alertas, 562 focos) y la serie diaria de Suomi NPP suma lo que reporta SERFOR. Publicado sin segunda persona, por decisión de Pepe.

## 2026-11-02: corte del MEF, ENFEN N.º 19 y corte de incendios (sin revisión de cuatro ojos)
- **Publicado sin revisión de una segunda persona**, por decisión de Pepe, mientras no haya comité. Claude preparó y revisó; la propuesta la une Claude.
- **MEF al 2 nov** (descarga automática lanzada a mano a las 00:00). Pasa los seis controles; avance total del PP 0068: 50,1 %. La automatización otra vez no pudo abrir la propuesta: falta el permiso de Actions (guía de administración, paso 6b).
- **ENFEN N.º 19 (30 oct):** el tramo extraordinario del Niño Costero se alarga hasta febrero de 2027 (el N.º 18 decía enero). El pronóstico por región ya no menciona Ica ni Arequipa, así que se retiraron sus frases. Próximo comunicado: 13 nov.
- **DS 124-2026-PCM:** vencía el 30 oct. No encontramos una prórroga publicada al 2 nov; la página lo muestra como vencido y pide revisar El Peruano. **Por verificar.**
- **Incendios, SERFOR al 2 nov (00:00):** consulta hecha por Claude en el navegador integrado; los totales por departamento cuadran con los nacionales (205 alertas y 465 focos de 3 días). Focos en fuerte baja en Cusco y Cajamarca; las alertas activas se mueven a Huánuco, Apurímac, Puno, Huancavelica, Junín y Lima.

## 2026-10-27 (noche): corte de incendios con todas las regiones
- Primer corte con el panorama nacional (SERFOR al 27 oct, 23:12). La consulta la corrió Claude en el navegador integrado de la computadora de Pepe; los totales por departamento cuadran con los nacionales (1 813 alertas y 1 489 focos de 3 días).
- Cusco: las 61 alertas recientes figuran como extinguidas (el 26 oct había 41 confirmadas). Cajamarca: 28 alertas sin verificar.

## 2026-10-27: brechas, ENFEN N.º 18, IGP y retiro de Contraste
- **Contraste retirado del sitio y del README** por decisión de Pepe. Su página de presentación usaba cifras de prensa como valores. Se retoma cuando El Niño tenga equipo.
- **Nueva sección "Brechas" en El Niño**, para Lima y Callao, Piura, Tumbes, Lambayeque, La Libertad e Ica: población expuesta según el CENEPRED frente a la respuesta medible (PP 0068, plan de gestión del riesgo, emergencias). **Publicada sin revisión del comité**, con un recuadro que lo dice. Método en `docs/el-nino-brechas.md`.
- **Exposición del CENEPRED transcrita** en `el-nino/datos/exposicion_cenepred.csv`, con dos escenarios oficiales que no coinciden y se muestran ambos: el estudio de El Niño (mayo 2026, por distrito) y el de lluvias del verano 2027 (agosto 2026, por centro poblado). Nuevo control `herramientas/validar_cenepred.py`: las 20 sumas del estudio de mayo cuadran con sus totales impresos.
- **No se publican** las cifras de las actualizaciones del CENEPRED de junio y octubre, que solo conocemos por la prensa. Queda pendiente conseguir los PDF.
- **ENFEN N.º 18 (16 oct) registrado.** Reemplaza la fila "próximo comunicado", que tenía fecha del 15. Pronóstico por región actualizado: caudales del Rímac y el Chillón sobre lo normal desde diciembre. Se agrega la fila del N.º 19 (30 oct).
- **IGP, informe técnico 2026-08 (14 set):** el ICEN de julio llegó a 3,38 °C. No se publica su categoría, porque el informe la rotula "cálida fuerte" aunque el valor pasa de 3,0. Está por aclarar con el IGP.
- Manual nuevo: `docs/manuales/06-fuentes-peligro-y-riesgo.md`.
- **Incendios: panorama de todas las regiones.** La consulta a SERFOR (`serfor_consulta.js`) ahora trae alertas por estado, focos de 3 días y focos anuales de todos los departamentos, con pocas consultas agrupadas. La página muestra una tabla en orden alfabético (sin ranking, como pide el método) con el PP 0068 al lado. Aparece desde el primer corte que se haga con el script nuevo; los cortes anteriores no traen esos datos. La proyección sigue solo para Cusco y Cajamarca.

## 2026-10-24: corte de incendios al 23 oct y manuales
- Datos de SERFOR al 23 oct. Desde el 20 oct, los focos Suomi NPP en Cusco cayeron más de 90 % (de unos 73 a entre 2 y 4 por día) y Cajamarca no tiene alertas activas. La lectura publicada advierte que parte de la caída puede deberse a la nubosidad y que persisten focos en otras regiones.
- SERFOR completa sus registros con retraso: los focos Suomi NPP de Cusco al 19 oct figuran hoy como 5294 (publicamos 5260). El seguimiento conserva la cifra publicada en cada corte.
- Corte de incendios semiautomático (consulta en el navegador más automatización) y manuales de operación en `docs/manuales/`.
- Se subió directo a main por error, el 24 oct, sin revisión de otra persona; la regla de cuatro ojos aún no estaba activa. La automatización se agrega aparte, en la propuesta `ajustes-24oct`.
  
## 2026-10-23

- **Monitor de incendios forestales migrado al repositorio** (`incendios/`). Datos de SERFOR con corte al 19 de octubre de 2026 para Cusco y Cajamarca, proyección de temporada con el satélite Suomi NPP y método en `docs/incendios-metodologia.md`.
- **Nueva regla editorial: pistas por verificar.** La prensa sigue sin ser fuente de cifras publicables. Desde hoy puede mostrarse solo como *pista por verificar*: en una sección aparte, con la etiqueta en cada tarjeta, fuera de resúmenes y cálculos, y con vencimiento de 30 días. Se suma el formulario **Verificar una pista**. Primeras 10 pistas registradas, vencen el 22 de noviembre de 2026.
- **Portada nueva.** La raíz del sitio pasa a ser un menú con los tres observatorios. El Niño se mueve a `/el-nino/`; sus datos siguen también en `/datos/` para no romper enlaces.
- **Nueva sección: emergencias registradas durante El Niño (piloto costa norte).** Reportes del COEN-INDECI de Tumbes, Piura, Lambayeque y La Libertad sobre lluvias y sus efectos ocurridos desde el 1 de setiembre. Diez emergencias incluidas (seis en Tumbes, cuatro en Piura), ninguna encontrada en Lambayeque ni La Libertad. Cada fila tiene el PDF original archivado con su huella. Reglas en el documento técnico y procedimiento en la guía de emergencias.
- **Ocho reportes excluidos por fecha de ocurrencia.** Siete reportes de Piura publicados entre el 1 y el 22 de octubre corresponden a lluvias de enero y febrero de 2026, y uno de La Libertad a un deslizamiento del 27 de agosto. Quedan en la tabla con el motivo.
- **Discrepancia por aclarar con INDECI.** El reporte N.º 14810 (Lagunas, Piura) cita el DS N.º 140-2026-PCM, que es de déficit hídrico y no incluye a Piura. Lagunas figura en el DS N.º 124-2026-PCM.
- **Pendiente.** La declaratoria del DS N.º 124-2026-PCM vence el 30 de octubre; registrar si se prorroga.

## 2026-10-22

- **Cortes del 19 y del 22 de octubre.** La descarga automática del lunes 19 y la lanzada a mano el jueves 22 llegaron al MEF y guardaron los siete archivos, pero no pudieron abrir la propuesta porque falta el permiso de la guía de administración (paso 6b). Se juntaron en una sola propuesta. Ambos pasan los seis controles. Avisos de cambio de PIM (>10 %) al 22: proyectos de los gobiernos regionales de Ica (+14 %), Junín (+30 %) y Moquegua (−28 %), y actividades municipales en Apurímac, Lambayeque (+16 % cada una) y Madre de Dios (+20 %). Al 19: proyectos municipales de Amazonas (+39 %).
- **Tumbes.** El PIM regional de Tumbes se mantiene en S/ 58.2 M en los cortes del 14, 19 y 22 con archivos originales. La cifra de S/ 73.3 M del 13 de octubre, que no tiene archivo, sigue sin verificar.

## 2026-10-14

- **Primer corte aprobado como piloto.** El corte del 14 de octubre (propuesta #1) lo aprobó y unió una sola persona del equipo fundador, antes de que existieran el comité editorial y la regla de cuatro ojos. Esa persona no preparó los datos: los bajó la descarga automática y los revisó el validador. El sitio se publicó ese día como versión preliminar. Desde la instalación del comité, ningún cambio entra sin la aprobación de un miembro que no lo preparó.
- **Repositorio creado.** Primera versión de las herramientas (lectura y validación de archivos del MEF, sitio, automatizaciones), la metodología del Observatorio El Niño y las guías del equipo.
- **Primer corte con archivos originales (14 de octubre, 17:05).** La descarga automática desde GitHub llegó al MEF y guardó los siete archivos con su huella digital en `el-nino/fuentes/mef/2026-10-14/`. Pasaron los seis controles y coinciden cifra por cifra con la carga inicial, que se había tomado de la exportación leída en el navegador.
- **Dato del 13 de octubre (46,9 %).** Viene de una lectura en pantalla del MEF sin archivo guardado. Ese día el PIM total era S/ 4,763.4 M; el 14 de octubre, S/ 4,751.7 M. El cambio regional más visible es Tumbes (de S/ 73.3 M a S/ 58.2 M según las dos lecturas); queda por verificar si fue una modificación presupuestaria o un error de la lectura del 13.
- **Bitácora de hechos.** Las entradas marcadas como `prensa` en `el-nino/datos/hechos.csv` están pendientes de reemplazo por su fuente primaria.

