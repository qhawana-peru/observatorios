# Monitor de incendios forestales: metodología

Versión 1 · 23 de octubre de 2026 · Estado: preliminar, pendiente de aprobación del comité editorial.

## Pregunta

¿Dónde y cuánto se quema en Cusco y Cajamarca, y qué tan lejos está el fin de la temporada?

Cada región se presenta por separado. Sus cifras no se suman ni se comparan entre sí.

## Fuente primaria: SERFOR

- **Visor:** https://sniffs.serfor.gob.pe/monitoreo/incendiosforestales/?view=hotspots
- **Servicio de datos (ArcGIS REST, público):** https://geo.serfor.gob.pe/geoservicios/rest/services/UFMS/Incendios_SAMIv21/MapServer

| Capa | Qué contiene | Cómo se usa |
| --- | --- | --- |
| 0 · Alerta de incendio forestal | Alertas recientes con estado: 1 alertado, 2 confirmado, 3 controlado, 4 extinguido | Conteo por estado y provincia. **Es una ventana móvil**: las alertas atendidas pasan al histórico, así que el conteo no se compara entre cortes. |
| 1 · Alertas históricas | Archivo de alertas | **No se usa.** Registra 47,116 casos en 2026 frente a 11,326 en 2024; posible cambio de método o duplicados. |
| 2 · Focos de calor | Últimos ~3 días | Conteo por región. |
| 3 · Focos de calor histórico | Desde 2012, con el satélite en el campo `SENSAT` | Acumulado anual y proyección. |
| 4 · Ocurrencia de incendios | Incendios forestales con hectáreas (`SUPTOT`) | Hectáreas por año, 2017–2025. 2026 aún no está consolidado. |
| 5 · Cicatrices | Áreas quemadas | No se usa por ahora. |

La consulta se hace con estadísticas agregadas (`outStatistics`, agrupando por departamento, provincia, estado o fecha). No se descargan datos de personas.

**Acceso:** el servicio responde desde un navegador. Falta probar si responde desde los servidores de GitHub; mientras tanto, la consulta se hace a mano y entra como propuesta de cambio.

## Comparabilidad entre años

SERFOR fue sumando satélites: 2012–2019, MODIS y Suomi NPP; desde 2020, NOAA-20; desde 2024, NOAA-21 y GOES. Un año reciente registra más focos aunque no haya más fuego.

- **2026 frente a 2025:** comparación razonable (mezcla de satélites parecida).
- **Series largas:** solo con Suomi NPP (`SENSAT` = `NPP` o `N`), el único presente en toda la serie. Se excluye 2022 por la interrupción de ese satélite a mitad de año.

## Proyección de temporada

No es un pronóstico, es una referencia histórica.

1. Para cada año comparable (2012–2025, sin 2022) se toman los focos Suomi NPP acumulados hasta la fecha de corte y el total del año.
2. Se calcula cuánto se sumó después de esa fecha, como porcentaje de lo acumulado: `(total − hasta_corte) / hasta_corte × 100`.
3. Se publica la mitad central de esos porcentajes (cuartil 25 a cuartil 75, con interpolación lineal), la mediana y los extremos.
4. **Seguimiento:** cada corte guarda lo proyectado en `seguimiento_proyeccion.csv`, para publicar al cierre de la temporada lo proyectado frente a lo ocurrido.

El cálculo está en `herramientas/sitio_incendios.py` (función `proyeccion`).

## Pistas por verificar

La prensa **no** es fuente de cifras publicables. Puede mostrarse solo como **pista por verificar**, con estas reglas:

1. **Zona aparte:** las pistas van en su propia sección, con otro estilo visual. Nunca en titulares, resúmenes ni cálculos.
2. **Etiqueta en cada tarjeta:** "Pista · sin verificar · vence DD/MM/AAAA", para que una captura nunca salga sin ella.
3. **Pregunta y lugar de búsqueda:** cada pista dice qué hay que confirmar y dónde buscar la fuente oficial.
4. **Vencimiento:** 30 días desde su registro. Si nadie la verifica, deja de mostrarse (queda en `pistas.csv` con su estado).
5. **Verificación:** se propone con el formulario **Verificar una pista**, con enlace al documento oficial y cita. Otra persona del comité revisa (cuatro ojos). Si se confirma, la cifra pasa a los datos del observatorio con su fuente primaria y la pista cambia a `verificada`; si la fuente da otra cifra, se publica la oficial y la pista cambia a `corregida`; si no hay fuente, `descartada`.
6. **Sin datos personales:** ni nombres de víctimas ni de heridos.

Estados posibles en `pistas.csv`: `sin verificar`, `verificada`, `corregida`, `descartada`.

## Archivos de datos (`incendios/datos/`)

| Archivo | Contenido |
| --- | --- |
| `serfor_alertas_recientes.csv` | Alertas por estado y focos de 3 días, por región, con periodo y capa |
| `serfor_alertas_provincia.csv` | Alertas recientes por provincia |
| `serfor_focos_anual.csv` | Focos del 1 de enero a la fecha de corte, 2024–2026, todos los satélites |
| `serfor_hectareas_anual.csv` | Incendios y hectáreas por año, 2017–2025 |
| `serfor_curvas_npp.csv` | Focos Suomi NPP acumulados por semana, 2012–2026 (sin 2022) |
| `serfor_historial_npp.csv` | Por año: focos hasta la fecha de corte, total y porcentaje sumado después |
| `seguimiento_proyeccion.csv` | Lo proyectado en cada corte, para el contraste final |
| `pistas.csv` | Cifras de prensa por verificar, con estado y vencimiento |

## Límites conocidos

- Los focos de calor incluyen quemas agrícolas; no todo foco es un incendio forestal.
- Los incendios en pastizales o cultivos pueden no aparecer como alerta forestal (caso de Oxamarca, pista P07).
- Las hectáreas de 2026 no están consolidadas por SERFOR.
- Las cifras de daños (fallecidos, viviendas, afectados) no tienen todavía fuente oficial verificada: están en las pistas.
