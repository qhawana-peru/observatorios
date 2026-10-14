# Guía de descarga: Consulta Amigable del MEF

13 de octubre de 2026 (revisado el 14 de octubre) · Pepe Díaz

Cada lunes, el equipo de finanzas públicas descarga del MEF la ejecución del Programa Presupuestal 0068 en siete archivos, los revisa con seis controles y los entrega antes de las 12:00. Con esos archivos se actualiza la serie de ejecución y el tablero del observatorio.

## Antes de empezar

- **Fuente:** [Consulta Amigable del MEF, consulta de ejecución del gasto](https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx). Es pública, no requiere usuario y se actualiza a diario.
- **Quiénes:** los dos analistas de finanzas públicas, en semanas alternas. Quien no descarga revisa (control de calidad cruzado). Las cifras que salen de estos archivos pasan después por la aprobación del comité editorial.
- **Cuándo:** lunes por la mañana, con datos al cierre del domingo. Si el lunes es feriado, se descarga el primer día hábil.
- **Qué se mide:** devengado sobre PIM del PP 0068. Los archivos traen también PIA, certificación, compromiso anual, atención de compromiso mensual y girado; se conservan todas las columnas.
- **Navegador:** cualquiera en computadora. Desde el celular la consulta es difícil de usar y la exportación puede fallar.

## Las descargas de cada semana

En la fase 1 son siete rutas, un archivo por ruta. En cada nivel de gobierno se separan actividades (gasto corriente) y proyectos de inversión, como pide la métrica del documento técnico. Tiempo estimado: unos 45 minutos, por medir en la prueba del lunes 26 de octubre. Todas empiezan igual: año 2026, **Categoría Presupuestal 0068**. Lo que cambia es el desglose y la opción **Incluye**.

| Código | Para qué sirve | Ruta después de Categoría Presupuestal 0068 | Incluye |
| --- | --- | --- | --- |
| D1 | Total de control del día | Nivel de Gobierno | Actividades/Proyectos |
| D2 | Gasto corriente de cada pliego del nivel regional | Nivel de Gobierno R → Sector (99: Gobiernos Regionales) → Pliego | Sólo Actividades |
| D3 | Inversión de cada pliego del nivel regional | Nivel de Gobierno R → Sector (99: Gobiernos Regionales) → Pliego | Sólo Proyectos |
| D4 | Gasto corriente de municipalidades, sumado por departamento | Nivel de Gobierno M → Gob.Loc./Mancom. → Departamento | Sólo Actividades |
| D5 | Inversión de municipalidades, sumada por departamento | Nivel de Gobierno M → Gob.Loc./Mancom. → Departamento | Sólo Proyectos |
| D6 | Gasto corriente del nivel nacional, por sector | Nivel de Gobierno E → Sector | Sólo Actividades |
| D7 | Inversión del nivel nacional, por sector | Nivel de Gobierno E → Sector | Sólo Proyectos |

Rutas verificadas en pantalla el 14 de octubre de 2026. Tres detalles que confunden:

- **Nivel regional y nacional pasan por Sector.** El botón Pliego solo aparece después de elegir un sector. En el regional hay un único sector (99), así que D2 y D3 traen los 26 pliegos en una sola tabla. En el nacional, Pliego mostraría solo los de un sector a la vez, por eso D6 y D7 se descargan al nivel de sector (14 sectores en actividades y 5 en proyectos al 14 de octubre).
- **Hay dos botones Departamento.** Para D4 y D5 se usa el de la columna "¿Quién gasta?", que ordena por la municipalidad que ejecuta. El de "¿Dónde se gasta?" ordena por el lugar de la meta y da otra cifra.
- **Cambiar la opción Incluye recarga la consulta desde el TOTAL.** Por eso cada par actividades/proyectos se recorre dos veces.

### Nombre de cada archivo

`AAAAMMDD_PP0068_<código>_<detalle>_p<página>de<total>.xls`

Ejemplos: `20261019_PP0068_D2_GR-actividades_p1de1.xls` · `20261019_PP0068_D7_GN-proyectos_p1de2.xls`. La fecha es la de la descarga, no la del lunes de la semana.

**Detalle fino (plan de respaldo o fase 2).** Desde D4 o D5 se puede bajar hasta cada municipalidad y cada proyecto: marcar el departamento → **Municipalidad** (no hace falta pasar por Provincia) → marcar la municipalidad → **Producto/Proyecto**. En Sólo Proyectos, cada fila es un proyecto con su código único de inversión (CUI), el mismo que usan Invierte.pe e INFOBRAS. Probado el 14 de octubre en Tumbes: 13 municipalidades con actividades del PP 0068 y 6 con proyectos.

## Descarga con enlaces directos

Cada ruta de la tabla tiene un enlace fijo y público que entrega el mismo archivo que el botón Exportar, sin recorrer la consulta. Verificado el 14 de octubre de 2026. Cada lunes a las 8:00 el repositorio de Qhawana descarga los siete archivos solo y abre la propuesta del corte. Si el MEF no responde, aparece un aviso de "descarga manual pendiente" y quien tenga el turno abre estos enlaces desde su computadora: el navegador baja cada archivo, se renombra según la convención y se sube sin abrirlo. Toma unos cinco minutos.

- D1: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=&y=2026&cpage=1&psize=400`
- D2: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=R&2=99&3=&ap=Actividad&y=2026&cpage=1&psize=400`
- D3: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=R&2=99&3=&ap=Proyecto&y=2026&cpage=1&psize=400`
- D4: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=M&37=M&5=&ap=Actividad&y=2026&cpage=1&psize=400`
- D5: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=M&37=M&5=&ap=Proyecto&y=2026&cpage=1&psize=400`
- D6: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=E&2=&ap=Actividad&y=2026&cpage=1&psize=400`
- D7: `https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?_tgt=xls&_uhc=yes&0=&30=0068&1=E&2=&ap=Proyecto&y=2026&cpage=1&psize=400`

El archivo .xls que entrega el MEF es en realidad una página web guardada (codificación Windows-1252). Por eso no hay que abrirlo ni guardarlo en Excel: el validador lo lee tal cual. El paso a paso que sigue queda como respaldo si algún día los enlaces dejan de funcionar.

## Paso a paso

La consulta funciona siempre igual: se marca una fila haciendo clic sobre ella y luego se pulsa el botón del siguiente desglose. Cada nivel elegido queda arriba, como una ruta.

1. Abre la [Consulta Amigable](https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx) y entra a la consulta de **ejecución del gasto**.
2. Elige el año **2026**.
3. En **Incluye**, marca la opción de la tabla (Actividades y Proyectos, Solo Actividades o Solo Proyectos). Hazlo antes de desglosar: cambiarla después reinicia la consulta.
4. Con la fila TOTAL marcada, pulsa **Categoría Presupuestal**. Marca la fila **0068: Reducción de vulnerabilidad y atención de emergencias por desastres**.
5. Pulsa el siguiente botón de la ruta (por ejemplo, **Nivel de Gobierno**), marca la fila que corresponde (R, M o E) y sigue hasta el último desglose de la tabla.
6. Revisa la línea superior de resultados: debe decir "Resultados 1 - N de N, Página 1 de 1". Si dice "Página 1 de 2" o más, exporta cada página por separado.
7. Exporta con el botón de exportar a Excel. El archivo baja con extensión .xls; no lo abras ni lo vuelvas a guardar antes de entregarlo, porque Excel puede cambiar los números.
8. Renómbralo con la convención de la sección anterior.
9. Para la siguiente ruta, vuelve a la Categoría Presupuestal 0068 haciendo clic en ella dentro de la ruta superior, sin empezar de cero.

**Si un botón tiene otro nombre en pantalla** o no aparece donde dice la guía (por ejemplo, Municipalidad después de Departamento), anota el nombre real, baja por el camino disponible (Provincia y luego Municipalidad, una exportación por provincia) y avisa para corregir la guía.

## Control de calidad antes de entregar

Quien revisa marca cada control. Un archivo que falla uno no se entrega: se vuelve a descargar.

- [ ] **Encabezado correcto:** fecha de la consulta de hoy, año 2026 y la opción Incluye que pide la tabla.
- [ ] **Total de control del día:** D1 muestra el PIM y el devengado de la Categoría Presupuestal 0068. Referencia del 13 de octubre de 2026: PIM S/ 4,763,441,758 y devengado S/ 2,233,049,564. Como D2 a D7 traen solo actividades o solo proyectos, su total se compara con D1 en el control siguiente.
- [ ] **Las partes suman el todo:** dentro de cada archivo, la suma de las filas es igual a su fila superior. Además, D2 + D3 da el total del nivel regional de D1 (13 de octubre: PIM S/ 834,265,707); D4 + D5, el del nivel local; y D6 + D7, el del nivel nacional. Si un par no cuadra, se descargan de nuevo los dos archivos.
- [ ] **Todas las páginas descargadas:** el número de filas coincide con el "Resultados 1 - N de N" del encabezado.
- [ ] **Avance recalculado:** devengado entre PIM, en tres filas al azar, coincide con la columna Avance %.
- [ ] **Cambios bruscos anotados:** si el PIM de un pliego cambió más de 10 % frente a la semana anterior, se anota en el registro. No se corrige ni se explica; lo revisa el analista.

## Entrega y errores frecuentes

Los siete archivos se suben juntos al repositorio de Qhawana, en la carpeta `el-nino/fuentes/mef/AAAA-MM-DD` con la fecha de la descarga, como una propuesta de cambio (la Guía para el equipo explica cómo, sin saber programar). La propuesta es el registro: guarda quién descargó, cuándo y quién aprobó. La validación automática corre los seis controles y deja el resultado como comentario; nadie copia cifras a mano.

| Error | Cómo se nota | Qué hacer |
| --- | --- | --- |
| Solo se exportó la primera página | El encabezado dice "Página 1 de 2" o hay menos filas que N | Exportar cada página y nombrarlas p1de2, p2de2 |
| Opción Incluye equivocada | El encabezado no dice lo que pide la tabla | Repetir la ruta desde el paso 3 |
| Falta el filtro del PP 0068 | El total del archivo ronda los S/ 289 mil millones (todo el presupuesto) | Volver al paso 4 |
| Archivo abierto y guardado en Excel | Extensión .xlsx o números con otro formato | Descargar de nuevo y entregar sin abrir |
| Archivos de días distintos | El total del PP 0068 no coincide entre archivos | Descargar todo en una misma sesión |
| La consulta no responde | La página no carga o se corta | Reintentar en una hora; si persiste, anotarlo y descargar el martes |
