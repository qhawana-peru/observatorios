# Bitácora de cambios

Toda corrección, cambio de método o decisión editorial que afecte lo publicado, con fecha y qué cambió. Lo más reciente arriba.

## 2026-11-18: salud, se quita la etiqueta «75 % hemodiálisis» (sin revisión del comité ni de cuatro ojos)
- En «Cómo circula el dinero», la etiqueta de la línea EsSalud → clínicas privadas caía junto a la línea del FISSAL y parecía suya. Se quita la etiqueta; la línea y su explicación al pasar el cursor se mantienen. Observación de Pepe.

## 2026-11-18: pestaña "Riesgo" con zonas de riesgo por distrito (sin revisión de cuatro ojos)
- **Qué hay:**
  - Nivel de riesgo por inundación y por movimientos en masa de los 1893 distritos del país, según dos estudios del CENEPRED: el escenario El Niño actualizado con el IT N.º 69-2026 del SENAMHI y el de verano 2027 de octubre (IT N.º 13-2026).
  - Tramos críticos de la ANA por distrito.
  - El estudio de Lima Metropolitana y Callao manzana por manzana (Censos 2025), sumado por distrito.
- **Navegación:** departamento, provincia y búsqueda por distrito. La vista inicial muestra los 100 distritos en riesgo muy alto por inundación en los dos estudios.
- **Pestañas:** Riesgo pasa a ser el paso 2. Respuesta pasa a 3 e Impacto a 4.
- **Control:** los CSV cuadran exactamente con los totales impresos en las hojas de resumen de los Excel del CENEPRED (prueba nueva `test_zonas_riesgo.py`).
- **Diferencias declaradas:**
  - En el estudio de Lima, el PDF imprime 609 550 personas en riesgo muy alto y el Excel suma 609 586. Se publica el Excel.
  - La cifra de 2,28 millones de personas de Lima en riesgo muy alto que citaba la prensa ya tiene fuente oficial: es el escenario El Niño actualizado, que cuenta la población completa de 18 distritos del departamento.
- **Pendiente:** la pestaña Brechas sigue con la versión de mayo del escenario El Niño. Actualizarla cambia cifras publicadas y requiere decisión.

## 2026-11-18: título de la línea de tiempo (sin revisión de cuatro ojos)
- "Aviso, decisiones y gasto en el mismo calendario" pasa a "Pronóstico, decisiones y gasto en una misma línea de tiempo". La franja superior del gráfico muestra el pronóstico del ENFEN, no los avisos del SENAMHI, que tienen su propia pestaña. El título anterior mezclaba los dos.

## 2026-11-18: El Niño en pestañas (sin revisión de cuatro ojos)
- **Qué cambia:** la página de El Niño deja de ser una sola columna larga. Se organiza en siete pestañas. **Resumen** reúne lo esencial y la ficha por región. Siguen tres pestañas numeradas con la secuencia del observatorio: **1 Aviso** (avisos del SENAMHI), **2 Respuesta** (presupuesto de los 26 gobiernos) y **3 Impacto** (emergencias del INDECI). Después vienen **Brechas**, **Calendario** y **Método**.
- **No cambian cifras ni textos:** solo se mueven las secciones existentes.
- **Enlaces:** cada pestaña tiene su dirección (`#avisos`, `#brechas`, `#metodo`…) y la dirección antigua `#region` abre Resumen. Al final de cada pestaña hay botones para ir a la anterior y a la siguiente. Con JavaScript desactivado, la página se ve como antes, en una sola columna.
- **Accesibilidad:** las pestañas usan los roles `tablist`, `tab` y `tabpanel` y se recorren con las flechas del teclado.

## 2026-11-18: MEF 18 nov, ENFEN N.º 20 y emergencias del INDECI al 18 nov (sin revisión de cuatro ojos)
- **MEF 18 nov:** pasa los seis controles. PIM S/ 5,120.6 M; devengado S/ 2,580.9 M (50,4 %). Nacional 41,4 %, municipal 55,2 %, regional 73,4 %. Aviso: actividades municipales de Cusco +30 % de PIM.
- **ENFEN N.º 20 (13 nov):** se registra leyendo la página oficial del ENFEN. Niño Costero extraordinario hasta febrero de 2027, debilitándose hasta julio; Niño global muy fuerte hasta febrero. Los ríos Tumbes y Piura, muy superiores a lo normal; Chillón, Rímac y Lurín, superiores desde enero (el N.º 19 decía diciembre), y se suman Pisco e Ica. Las fichas regionales pasan del pronóstico del N.º 17 al del N.º 20, y la etiqueta lee la fuente de `contexto.json` en vez de un texto fijo.
- **Declaratoria:** los reportes del INDECI dicen que el DS N.º 149-2026-PCM rige del 4 nov 2026 al 2 ene 2027. Falta enlazar la norma.
- **Emergencias:** se archivan 50 reportes nuevos del COEN (Tumbes, Piura, Lambayeque y La Libertad) con su PDF y su huella. La tabla pasa de 10 a 49 emergencias incluidas: Tumbes 26, Piura 19, Lambayeque 2 y La Libertad 2. Se actualizan siete filas existentes con versiones posteriores de sus reportes.
- **Regla nueva contra duplicados:** el INDECI publica reportes departamentales que agrupan emergencias. Se cuenta cada emergencia una vez según su código del SINPAD; los reportes de Zarumilla (N.º 15878) y Máncora (N.º 15632) quedan excluidos porque sus códigos y cifras están dentro de los departamentales N.º 15734 y N.º 15591. El reporte departamental de Piura N.º 15631 trae cifras solo en texto y puede repetir el de Yamango: se muestra sin sumar.
- **Discrepancia de Lagunas:** el reporte N.º 2 (N.º 15568) ya no cita el DS N.º 140-2026-PCM.
- **Pendiente:** la búsqueda del portal del INDECI no devuelve todos los reportes; esta revisión cubre los que devuelve por región.

## 2026-11-17: avisos del SENAMHI de lluvias y ríos (sin revisión de cuatro ojos)
- Nueva sección en El Niño: 37 avisos de lluvia (10 rojos) y 87 avisos de ríos (8 rojos) desde el 1 set 2026, con calendario por departamento y lista de avisos de ríos recientes. Sugerencia externa de monitorear lluvias; se descartó Meteored (privado, pronóstico de modelo) y se usaron los avisos oficiales.
- Cada aviso de lluvia se cruza con los límites del INEI que publica el SENAMHI: un día cuenta si al menos el 5 % del departamento está bajo ese nivel. El nivel máximo de cada mapa coincide con el de la tabla del SENAMHI en los 37 avisos.
- Las fichas de Brechas suman "días con aviso de lluvia naranja o rojo".
- Herramientas nuevas: `senamhi_avisos.js` (consulta en navegador) y `procesar_avisos_senamhi.py`. Método en `docs/el-nino-avisos.md`; manual 06, parte D.

## 2026-11-17: salud, el FISSAL muestra su población (sin revisión del comité ni de cuatro ojos)
- En el diseño formal, al seleccionar el FISSAL no se encendía ninguna población: la línea de afiliación solo unía a «Residentes sin otro seguro» con el SIS. Se agrega la línea con el FISSAL y la ficha aclara que no tiene población propia: cubre a los afiliados al SIS cuando tienen una enfermedad de alto costo. Observación de Pepe.

## 2026-11-17 · Museo: hilos de pobreza monetaria y empleo adecuado

- Qué: la vista «Hilos» pasa a tener tres hilos con selector (anemia infantil, pobreza monetaria y empleo adecuado), por decisión de Pepe (pobreza y empleo como hilos del museo, no como observatorio aparte; periodo 2004-2025; pobreza monetaria como medida principal; Plan Bicentenario como caso de cierre). El hilo de anemia no cambia.
- Pobreza: serie vigente del INEI 2004-2025 (ediciones 2004-2012 y 2009-2020; 2021 citado por la PNDIS al 2030 y 2022-2025 por el Congreso, ambos citando al INEI, por cotejar con el informe técnico 2016-2025), serie anterior del INEI (2004, 2009 y 2010), metas del Plan Bicentenario y meta del PEDN al 2050. Pobreza extrema 2021 sin dato hasta cotejarla.
- Empleo: empleo adecuado del INEI 2004-2012, meta del Plan Bicentenario (otra medición) y meta y valor reportado del PDRC Cajamarca.
- Tres hallazgos nuevos: la meta de pobreza del Plan Bicentenario se fijó con una serie que el INEI reemplazó; dos cifras de empleo adecuado para 2009; Cajamarca fijó metas de empleo adecuado por debajo de su línea de base.
- Regla: no se calcula la distancia entre una meta y una serie distinta a la suya. Lo que falta, en `hilo_pendientes.csv`.
- Revisión: sin revisión de cuatro ojos (suspendida); preparado, revisado y unido por Claude. Pruebas: 55 pasan.

## 2026-11-17 · Salud: corrección de la vista 5 y nuevo nombre «Mortalidad»

- Qué: los gráficos de mortalidad aparecían debajo de las otras pestañas después de visitarla (la regla `display:grid` anulaba el atributo `hidden`). Se agrega `#mort[hidden]{display:none}` y una prueba. La pestaña pasa a llamarse «Mortalidad», a pedido de Pepe.
- Revisión: sin revisión de cuatro ojos (suspendida); preparado, revisado y unido por Claude.

## 2026-11-17 · Salud: vista 5 «De qué morimos» (SINADEF)

- Qué: nueva vista en /salud/ con la mortalidad proporcional por tres grandes grupos de causas (transmisibles/maternas/perinatales/nutricionales; no transmisibles; lesiones) más un bloque de causas mal definidas o sin código; por año (2017–2024), subgrupo, seguro, edad y departamento; calidad del registro y alertas de cobertura.
- Fuente: archivo abierto del SINADEF (MINSA, ODC-By), actualizado el 15/09/2026 pero con registros solo hasta el 05/05/2024. 1 110 168 registros agregados en el navegador con `salud/sinadef_agregar.js` (sin guardar registros individuales); resumen con `salud/sinadef_resumen.py`.
- Regla propia: causa básica aproximada (última causa con código válido A→D; lesiones por el campo «muerte violenta»). No son tasas. Celdas menores de 5 suprimidas en cortes por departamento, seguro y edad.
- Revisión: sin revisión de cuatro ojos (suspendida); preparado, revisado y unido por Claude. Pruebas: 52 pasan.

## 2026-11-17: portada, texto de presentación (sin revisión de cuatro ojos)
- Por decisión de Pepe ("decir lo que somos, no lo que no somos"), el pie de la portada queda: "Qhawana (quechua: «lugar desde donde se mira») es una iniciativa ciudadana independiente." Se retira "sin afiliación partidaria". No cambian cifras ni métodos.

## 2026-11-17: salud, población sin seguro y gasto de bolsillo en el diseño formal (sin revisión de cuatro ojos)
- **"No afiliados" pasa a "Sin seguro (con derecho al SIS)"**, por observación de Pepe. Desde el DU 017-2019 todo residente sin otro seguro tiene derecho al SIS, así que la norma ya no prevé esa población. La ficha muestra las dos cifras oficiales del INEI, que no coinciden: 5,2 % sin seguro en el Censo 2025 y 8,9 % en la ENAHO de enero a marzo de 2025 (censo frente a encuesta trimestral; seguro autodeclarado en ambas).
- **"Ninguna" pasa a "Pago directo (sin IAFAS)"** y el régimen "Gasto directo" a **"Sin aseguramiento"**: el pago directo no es un régimen.
- **Nueva franja transversal en la fila de población:** el gasto de bolsillo lo pagan afiliados de todos los regímenes y quienes no tienen seguro; no es una población ni parte del diseño. Remite a las vistas "Cómo circula el dinero" y "Dónde se filtra el bolsillo". No cambia ninguna cifra existente.

## 2026-11-17: ilustraciones nuevas en la portada (sin revisión del comité ni de cuatro ojos)
- Por pedido de Pepe, las tarjetas del museo y de salud dejan de parecer organigramas. Museo: fachada de museo de noche, con frontón dorado, un plan iluminado en la entrada y estandartes turquesa y verde (sus alas sectorial y territorial). Salud: un electrocardiograma que termina en una moneda (S/) que cae a un bolsillo, por la pregunta de quién termina pagando. Animaciones suaves que se apagan si el usuario pidió reducir el movimiento. No cambian datos ni textos.

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

