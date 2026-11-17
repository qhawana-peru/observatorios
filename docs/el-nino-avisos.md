# Avisos del SENAMHI: lluvias y ríos (Observatorio El Niño)

17 de noviembre de 2026. Sección "Avisos del SENAMHI" de la página de El Niño. Publicada sin revisión de cuatro ojos, por decisión de Pepe.

## Qué responde
Qué advirtió el Estado, dónde y con qué nivel de peligro, antes de cada evento de lluvia o de crecida. Va antes de la sección de emergencias: primero el aviso, después el daño. No pronostica nada por su cuenta y no muestra mapas de empresas privadas (se descartó Meteored por esa razón).

## Fuentes
| Dato | Fuente | Archivo |
|---|---|---|
| Lista de avisos de lluvia (número, fechas, nivel) | SENAMHI, página de avisos meteorológicos | `el-nino/datos/avisos_senamhi_lluvia.csv` |
| Zonas de cada aviso por día y nivel | SENAMHI, servidor de mapas IDESEP, capa `g_aviso:view_aviso` | mismo archivo |
| Límites departamentales | IDESEP, capa `g_carto_fundamento:departamentos` (INEI) | — |
| Avisos de ríos (estación, fechas, nivel) | SENAMHI, página de avisos hidrológicos | `el-nino/datos/avisos_senamhi_rios.csv` |
| Ubicación de estaciones | Mapa de estaciones del SENAMHI, cruzado con IDESEP (departamento, provincia, cuenca) | dentro de `procesar_avisos_senamhi.py` |

Escala del SENAMHI en los mapas: nivel 1 sin aviso, 2 amarillo, 3 naranja, 4 rojo.

## Cómo se asigna un departamento
1. Cada aviso de lluvia trae un mapa por día con polígonos por nivel.
2. Se dibujan esos polígonos y los departamentos en una cuadrícula de 0,02° (unos 2 km) y se calcula qué porcentaje de cada departamento cae bajo cada nivel.
3. Un día cuenta para un departamento si al menos el **5 %** de su superficie está bajo ese nivel. Si dos avisos cubren el mismo día, vale el nivel más alto.
4. En las fichas de Brechas, "Lima y Callao" cuenta un día una sola vez aunque ambos tengan aviso.

**Control:** el nivel máximo que sale del mapa de cada aviso coincide con el nivel que el SENAMHI publica en su tabla en los 37 avisos (prueba automática `test_avisos_senamhi.py`).

**Límites:** el umbral del 5 % es una decisión nuestra; con un umbral menor, más departamentos aparecerían con aviso. La cuadrícula usa grados, no km², lo que distorsiona poco dentro del Perú. Callao es muy pequeño (unas 30 celdas), así que su porcentaje es menos preciso.

## Avisos de ríos
- Se publican todos desde el 1 set, con río, estación, departamento, cuenca y nivel.
- El tipo sale del título: **incremento** (crecida), **descenso** (bajante) o **situación actual**. En la Amazonía, muchos son por bajante: no son riesgo de inundación.
- Dos estaciones no figuran en el mapa de estaciones del SENAMHI y quedan sin ubicar: Lagarto IRD y Yurimaguas DHN.

## Cómo se actualiza
Manual 06, parte D. Tarda unos 10 minutos y se hace desde un navegador en el Perú (el SENAMHI no responde a servidores de fuera); hoy lo hace Claude en el navegador integrado.

## Pendientes
- Decidir con el comité si el umbral del 5 % es el adecuado.
- Caudales observados por estación (monitoreo hidrológico PHISIS): no se incluyeron todavía.
- Avisos de activación de quebradas (huaicos): el SENAMHI los publica aparte; candidatos para una siguiente versión.
