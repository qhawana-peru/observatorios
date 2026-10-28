# Bitácora de cambios

Toda corrección, cambio de método o decisión editorial que afecte lo publicado, con fecha y qué cambió. Lo más reciente arriba.

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

