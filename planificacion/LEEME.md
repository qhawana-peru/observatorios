# Museo de la planificación

Inventario navegable de los planes del Estado peruano, desde el Acuerdo Nacional hasta los planes regionales, contrastado con sus propios reportes de seguimiento. Pregunta: **¿qué se propuso el Estado para mejorar la calidad de vida de las personas, quién lo planificó, cómo se conectan los planes de sectores y territorios, y cuáles tienen seguimiento?**

Estado: **versión preliminar, sin revisión del comité.** Corte del catálogo: 16/11/2026. Lanzamiento previsto: 2 de enero de 2027.

## Cómo se genera

```
python3 planificacion/catalogo_fuente.py   # planes, versiones, reportes, notas, fuentes, sectores, necesidades
python3 planificacion/catalogo_piloto.py   # objetivos, indicadores, hilo de anemia, hallazgos y fichas de KPI
python3 planificacion/build.py --salida _site/planificacion
```

El sitio completo lo genera `herramientas/construir_sitio.py`, que llama a `build.py`. Los CSV de `catalogo/` son los datos abiertos (CC BY 4.0) y se copian a `/planificacion/datos/` del sitio. Los controles están en `herramientas/tests/test_planificacion.py`.

## Tablas del catálogo

- `planes.csv`: cada pieza (plan, política o instrumento), con eje, nivel, actores, norma y horizonte.
- `versiones.csv`, `reportes.csv`, `notas.csv`, `fuentes.csv`, `articulacion.csv`, `dimensiones.csv`.
- `sectores.csv` (19), `multisectorial.csv` (sectores involucrados que declara cada política), `necesidades.csv` (12, agrupación editorial de Qhawana), `necesidad_plan.csv`, `notas_necesidad.csv`.
- Piloto: `objetivos.csv`, `indicadores.csv` (Cajamarca), `hallazgos.csv`.
- Hilos: `hilos.csv` (anemia infantil, pobreza monetaria y empleo adecuado), `hilo.csv` (cada serie medida o meta, con su hilo, fuente y nota) y `hilo_pendientes.csv` (lo que falta catalogar en cada hilo, a la vista).
- Indicadores del museo: `kpis.csv` y `kpis_descartados.csv`. Método en [docs/planificacion-metodologia.md](../docs/planificacion-metodologia.md).

## Reglas

1. Solo documentos públicos y oficiales, con enlace y fecha de consulta.
2. El seguimiento se mide contra lo que la norma exige a cada tipo de plan.
3. La articulación que se muestra es la declarada por la entidad; la que solo exige la norma va punteada.
4. Un hallazgo compara dos documentos oficiales con una regla publicada y termina en una pregunta abierta.
5. Mismas reglas para todos; sin puntajes, rankings ni índices compuestos.
6. "No ubicado" no es "no existe": se rotula con su fecha y cualquiera puede aportar el enlace.

## Mapa

`geo/mapa.json` son los contornos departamentales proyectados para la página, derivados de un GeoJSON público de departamentos del Perú.
