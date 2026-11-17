# Museo de la planificación — Metodología de indicadores

Versión 1 · 17 de noviembre de 2026 · corte de datos 16/11/2026 · licencia CC BY 4.0. Las fichas se mantienen en `planificacion/catalogo/kpis.csv`; este documento las reproduce. **Versión preliminar, sin revisión del comité.**

## Para qué sirven

Responden a la pregunta del museo: qué se propuso el Estado, cómo se conectan sus planes y si alguien les hace seguimiento. **Miden el sistema de planificación, no califican a las entidades.**

## Reglas de uso

1. **Sistema, no entidad.** Se publican cifras y distribuciones. El dato de cada entidad vive en su ficha, nunca en una tabla ordenada.
2. **Sin índice compuesto.** Cada indicador se muestra por separado.
3. **Misma regla para todos.** La fórmula no cambia según el sector o el gobierno.
4. **Comparar solo lo comparable.** Dos metas se comparan si tienen la misma población, fuente y criterio de medición. Si no, el hallazgo es que miden distinto.
5. **Ubicado no es existe.** Lo no ubicado se rotula con su fecha y cualquiera puede aportar el enlace.
6. **Derecho a réplica.** Toda entidad puede corregir o aportar un documento mediante el formulario de corrección del repositorio.
7. **Lo que dice la entidad se rotula como suyo** y no se recalcula.

## Estados

- **Activo:** se calcula con todo el catálogo en cada corte.
- **Piloto:** se calcula solo donde ya hay datos (hoy, Cajamarca y el hilo de anemia).
- **En revisión:** definido; le falta un insumo o una validación externa.
- **Etapa 2:** requiere cruzar planes con presupuesto (MEF).

## Fichas

### Sistema
**S1 · Planes regionales vigentes ubicados** · Activo
- Pregunta: ¿Cada territorio tiene un plan de desarrollo concertado vigente?
- Cálculo: PDRC con horizonte vigente y fuente oficial enlazada ÷ 26 (25 gobiernos regionales y Lima Metropolitana)
- Fuente: Catálogo del museo (ordenanzas en El Peruano y portales regionales). Frecuencia: Mensual. Desagregación: Región.
- Advertencias: Ubicado no es lo mismo que existe: un plan no ubicado puede existir. La norma de 11 planes está por confirmar.
- Dónde se ve: Territorio; Tabla y método

**S2 · Planes con horizonte vencido y sin reemplazo ubicado** · Activo
- Pregunta: ¿Dónde se planifica con un plan que ya terminó?
- Cálculo: Número de planes del catálogo cuyo horizonte terminó antes del año en curso y sin plan sucesor ubicado
- Fuente: Catálogo del museo. Frecuencia: Mensual. Desagregación: Tipo de plan, región.
- Advertencias: Se informa como número, no como lista ordenada. Antes de publicar un caso se hace una búsqueda a fondo o una solicitud de acceso a la información.
- Dónde se ve: Plano; Territorio; Tabla y método

**S3 · Planes regionales con horizonte ampliado** · Activo
- Pregunta: ¿Se planifica de nuevo o se estira el plan anterior?
- Cálculo: PDRC vigentes formulados hasta 2016 y ampliados por ordenanza ÷ PDRC vigentes
- Fuente: Catálogo del museo (versiones de cada plan). Frecuencia: Mensual. Desagregación: Región.
- Advertencias: Ampliar está permitido por CEPLAN; el indicador describe, no sanciona.
- Dónde se ve: Territorio; Tabla y método

**S4 · Desfase de adecuación al plan superior** · En revisión
- Pregunta: ¿Cuánto tarda un plan en ajustarse al PEDN actualizado?
- Cálculo: Años entre la actualización del PEDN (DS 103-2023-PCM) y la aprobación o actualización del plan inferior
- Fuente: Catálogo del museo. Frecuencia: Anual. Desagregación: Tipo de plan, región.
- Advertencias: Requiere la fecha exacta de aprobación de cada plan y saber si declara alinearse al PEDN de 2023.

**S5 · Cobertura del inventario por tipo de plan exigido** · En revisión
- Pregunta: ¿Existen todos los planes que la norma exige?
- Cálculo: Planes vigentes ubicados ÷ entidades obligadas a tenerlos, por tipo (PESEM, PEI, PDLC…)
- Fuente: Catálogo del museo y padrón de entidades obligadas. Frecuencia: Trimestral. Desagregación: Tipo de plan, sector, región.
- Advertencias: Requiere el padrón de entidades obligadas (19 sectores, pliegos, 196 provincias, distritos).


### Diseño
**D1 · Indicadores con línea de base y año** · Piloto
- Pregunta: ¿Se sabe desde dónde se parte?
- Cálculo: Indicadores del plan con valor y año de línea de base ÷ indicadores del plan
- Fuente: Documento del plan o su informe de evaluación. Frecuencia: Al aprobar o actualizar el plan. Desagregación: Plan.
- Advertencias: En el piloto se usa el informe de evaluación de Cajamarca, no el documento completo del plan.
- Dónde se ve: Ficha del plan

**D2 · Indicadores con fuente de datos declarada** · Piloto
- Pregunta: ¿Se sabe de dónde sale el dato?
- Cálculo: Indicadores con fuente declarada en el documento evaluado ÷ indicadores del plan
- Fuente: Documento del plan o su informe de evaluación. Frecuencia: Al aprobar o actualizar el plan. Desagregación: Plan.
- Advertencias: Mide lo que dice el documento revisado; el plan completo puede declarar fuentes que el informe omite.
- Dónde se ve: Ficha del plan

**D3 · Indicadores con dato disponible para su territorio** · En revisión
- Pregunta: ¿Habrá con qué medir cada año?
- Cálculo: Indicadores cuya fuente publica dato con representatividad para el nivel del plan ÷ indicadores del plan
- Fuente: Fichas técnicas de las encuestas del INEI y registros administrativos. Frecuencia: Anual. Desagregación: Plan.
- Advertencias: Requiere una tabla de representatividad por encuesta, nivel y año, validada por una persona de estadística.

**D4 · Ritmo exigido frente a ritmo observado** · Piloto
- Pregunta: ¿La meta pide un cambio parecido al que se ha visto?
- Cálculo: (Meta − línea de base) ÷ años del plan, frente a la variación anual promedio de la serie oficial en los últimos cinco años
- Fuente: Plan e INEI. Frecuencia: Anual. Desagregación: Indicador, plan.
- Advertencias: Solo con serie oficial comparable (mismo indicador, misma fuente, mismo criterio). Una meta ambiciosa no es una mala meta: se presenta como pregunta.
- Dónde se ve: Hilos


### Articulación
**A1 · Objetivos con vínculo declarado al nivel superior** · Piloto
- Pregunta: ¿El plan dice a qué objetivo nacional contribuye?
- Cálculo: Objetivos del plan con vínculo declarado al PEDN (o al plan superior) ÷ objetivos del plan
- Fuente: Matriz de articulación del plan o su informe de evaluación. Frecuencia: Al aprobar o actualizar el plan. Desagregación: Plan.
- Advertencias: Solo cuenta el vínculo declarado por la entidad, con evidencia.
- Dónde se ve: Ficha del plan

**A2 · Cobertura inversa del PEDN** · En revisión
- Pregunta: ¿Los objetivos nacionales bajan a los territorios?
- Cálculo: Para cada objetivo del PEDN, número de PDRC que declaran contribuir a él
- Fuente: Matrices de articulación de los 26 PDRC. Frecuencia: Anual. Desagregación: Objetivo del PEDN.
- Advertencias: Solo tiene sentido con la mayoría de los PDRC catalogados; con tres regiones confundiría.

**A3 · Indicadores en lenguaje común** · En revisión
- Pregunta: ¿Los niveles miden lo mismo de la misma forma?
- Cálculo: Indicadores del plan con la misma definición y fuente que un indicador del nivel nacional ÷ indicadores del plan
- Fuente: Planes y fichas técnicas. Frecuencia: Anual. Desagregación: Plan.
- Advertencias: Requiere comparar fichas técnicas, no solo nombres de indicadores.

**A4 · Metas distintas para un mismo indicador** · Piloto
- Pregunta: ¿Cuántos instrumentos se comprometen con lo mismo y cuánto difieren?
- Cálculo: Número de instrumentos con meta para el mismo indicador y año; distancia entre la meta más exigente y la menos exigente
- Fuente: Planes, políticas y sus reportes. Frecuencia: Anual. Desagregación: Hilo.
- Advertencias: Se calcula por hilo. Solo entre metas de la misma población; si difiere, se anota.
- Dónde se ve: Hilos

**A5 · Brecha entre meta regional y nacional** · En revisión
- Pregunta: ¿Las metas regionales suman a la nacional?
- Cálculo: Meta regional menos meta nacional al mismo año, para indicadores comparables
- Fuente: PDRC y PEDN. Frecuencia: Anual. Desagregación: Región, indicador.
- Advertencias: Rara vez comparable: distinto grupo de edad, fuente o año. Se activa solo con A3 resuelto.

**A6 · Multisectorialidad efectiva** · En revisión
- Pregunta: ¿Los sectores involucrados en una política tienen compromisos propios?
- Cálculo: Sectores involucrados con indicadores o servicios asignados ÷ sectores declarados en la política
- Fuente: Textos de las políticas nacionales multisectoriales. Frecuencia: Anual. Desagregación: Política.
- Advertencias: Requiere catalogar las 28 políticas multisectoriales; hoy solo está la de Salud.


### Seguimiento
**G1 · Planes con al menos un reporte ubicado** · Activo
- Pregunta: ¿Hay alguna prueba pública de que se sigue el plan?
- Cálculo: Planes con al menos un reporte de seguimiento o evaluación ubicado ÷ planes catalogados, por tipo
- Fuente: Catálogo del museo. Frecuencia: Mensual. Desagregación: Tipo de plan.
- Advertencias: No mide si se publicaron todos los exigidos (eso es G2). Para las 40 políticas cuenta el informe anual consolidado de CEPLAN, no un reporte propio de cada una. En los PDRC la mayoría de reportes está por revisar.
- Dónde se ve: Tabla y método

**G2 · Reportes publicados frente a exigidos** · En revisión
- Pregunta: ¿Se publica lo que la norma pide, y a tiempo?
- Cálculo: Reportes ubicados ÷ reportes exigidos por la norma; días de retraso respecto al plazo
- Fuente: Catálogo del museo y directiva de CEPLAN. Frecuencia: Trimestral. Desagregación: Tipo de plan, entidad.
- Advertencias: Requiere tabular la frecuencia y el plazo exigidos a cada tipo de plan, incluidas las exoneraciones (RPCD 043-2026).

**G3 · Completitud del último reporte** · Piloto
- Pregunta: ¿El reporte trae datos?
- Cálculo: Indicadores con valor en el último periodo evaluado ÷ indicadores del plan
- Fuente: Informe de evaluación del plan. Frecuencia: Anual. Desagregación: Plan.
- Advertencias: Un indicador sin dato puede deberse a que la fuente nacional aún no publica.
- Dónde se ve: Ficha del plan

**G4 · Metas del último año alcanzadas, según el propio reporte** · Piloto
- Pregunta: ¿Qué dice la entidad de su propio avance?
- Cálculo: Indicadores con avance de 100 % en el último periodo, según el informe ÷ indicadores con dato
- Fuente: Informe de evaluación del plan. Frecuencia: Anual. Desagregación: Plan.
- Advertencias: Es el resultado que declara la entidad; Qhawana no lo recalcula ni lo compara entre regiones.
- Dónde se ve: Ficha del plan


### Ciudadano
**C1 · Compromisos por necesidad y territorio** · En revisión
- Pregunta: ¿Quién se comprometió a qué sobre mi necesidad, en mi región?
- Cálculo: Número de metas vigentes por necesidad ciudadana y región, con su responsable
- Fuente: Objetivos e indicadores catalogados. Frecuencia: Mensual. Desagregación: Necesidad, región.
- Advertencias: Requiere los objetivos e indicadores catalogados de los planes de cada región.

**C2 · Metas que vencen en la gestión** · En revisión
- Pregunta: ¿Qué debe lograrse durante este periodo de gobierno?
- Cálculo: Metas con año dentro del periodo de la autoridad (2027-2030 regional; 2026-2031 nacional)
- Fuente: Objetivos e indicadores catalogados. Frecuencia: Anual. Desagregación: Región, nivel de gobierno.
- Advertencias: Requiere metas multianuales catalogadas; el informe de Cajamarca solo trae metas 2023-2024.


### Presupuesto
**P1 · Presupuesto vinculado a objetivos del plan** · Etapa 2
- Pregunta: ¿Cuánto del presupuesto financia lo que el plan prioriza?
- Cálculo: PIM vinculado a objetivos del plan (programas presupuestales y articulación del PEI) ÷ PIM total
- Fuente: MEF, Consulta Amigable y datos abiertos. Frecuencia: Trimestral. Desagregación: Entidad, objetivo.
- Advertencias: Etapa 2. Reutiliza las herramientas de El Niño.

**P2 · Gasto sin vínculo con un plan** · Etapa 2
- Pregunta: ¿Qué se gasta fuera de lo planificado?
- Cálculo: Gasto devengado en actividades y proyectos sin vínculo declarado con un objetivo ÷ devengado total
- Fuente: MEF. Frecuencia: Trimestral. Desagregación: Entidad.
- Advertencias: Etapa 2. El vínculo depende de cómo cada entidad registra su POI.

**P3 · Coherencia entre prioridades y asignación** · Etapa 2
- Pregunta: ¿Los objetivos priorizados reciben más recursos?
- Cálculo: PIM por objetivo priorizado frente a no priorizado, por entidad
- Fuente: MEF y plan. Frecuencia: Anual. Desagregación: Entidad.
- Advertencias: Etapa 2.


### Observatorio
**O1 · Piezas con fuente oficial enlazada** · Activo
- Pregunta: ¿Cada pieza del museo se puede verificar?
- Cálculo: Piezas con al menos una fuente oficial enlazada ÷ piezas del catálogo
- Fuente: Catálogo del museo. Frecuencia: En cada corte. Desagregación: Eje.
- Advertencias: Rinde cuentas de Qhawana, no del Estado.
- Dónde se ve: Tabla y método

**O2 · Antigüedad de la verificación** · Activo
- Pregunta: ¿Qué tan al día está el catálogo?
- Cálculo: Días desde la última consulta de las fuentes de cada pieza
- Fuente: Catálogo del museo. Frecuencia: En cada corte. Desagregación: Pieza.
- Advertencias: Hoy todas las piezas tienen la misma fecha de consulta.
- Dónde se ve: Tabla y método

**O3 · Correcciones y tiempo de respuesta** · En revisión
- Pregunta: ¿Qué tan rápido corrige Qhawana?
- Cálculo: Aportes y réplicas recibidos; mediana de días hasta resolverlos
- Fuente: Formulario de aportes. Frecuencia: Mensual. Desagregación: Tipo de aporte.
- Advertencias: Requiere el canal de aportes y réplica, que aún no existe.


## Indicadores descartados

- **Índice compuesto de calidad o de gestión:** Mezcla dimensiones distintas, no dice qué corregir e invita a ordenar entidades.
- **Ranking de regiones o sectores:** Contradice la regla 6 del museo y castiga a quien publica más.
- **Proporción de objetivos de resultado frente a objetivos de gestión:** La clasificación es interpretativa y no replicable sin una regla externa.
- **Concordancia del dato reportado con la fuente oficial:** Es una función de control o auditoría, no de un observatorio ciudadano; y la mayoría de indicadores no es comparable.
