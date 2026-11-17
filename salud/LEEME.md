# Observatorio del sistema de salud

Mapa de los actores del sistema de salud del Perú. Pregunta: **¿quién financia, quién atiende y quién termina pagando?**

Estado: **versión preliminar, sin revisión del comité.** Corte de establecimientos: RENIPRESS (SUSALUD) al 16/11/2026.

## Vistas

1. **Diseño formal.** Naturaleza y régimen de cada IAFAS; rectoría del MINSA y supervisión de SUSALUD sobre todo el sistema (la SBS, solo sobre las empresas de seguros); conducción del financiamiento, IAFAS, red preferente y población. Contorno del subsistema integrado (FFAA, PNP, EsSalud).
2. **Cómo circula el dinero.** Fuentes, fondos y prestadores: red preferente, compras e intercambio vigentes, convenios sin vigencia verificada, gasto de bolsillo de los hogares y reembolsos. El grosor de las flechas no es proporcional al monto: faltan las Cuentas Nacionales de Salud.
3. **Dónde se filtra el bolsillo.** Gasto de bolsillo de 2019 según el seguro de quien paga (DIGEMID con ENAHO). Es participación en el total, no gasto por persona.
4. **Dónde están los prestadores.** Los 27 051 establecimientos de RENIPRESS por red y capacidad, con lupa de Lima y Callao y una vista de «una red por mapa».
5. **Tabla.** La misma información sin interacción.

Cada actor y cada flecha tienen una ficha con sus cifras y su fuente, rotulada por tipo (oficial, estudio, documento de empresa, consultora). Las cifras de prensa aparecen aparte, como **pistas por verificar**, y nunca en titulares ni cálculos.

## Cómo se genera

```
python3 salud/renipress.py RUTA_AL_EXPORT.xls --corte AAAA-MM-DD   # solo cuando hay un corte nuevo de RENIPRESS
python3 salud/build.py --salida _site/salud
```

El sitio completo lo genera `herramientas/construir_sitio.py`, que llama a `build.py`. Los controles están en `herramientas/tests/test_salud.py`.

**La descarga original de RENIPRESS no se guarda en el repositorio**: trae el nombre del director médico, teléfonos y RUC de cada establecimiento. `renipress.py` deja solo lo necesario.

## Datos

- `datos/renipress_resumen_20261116.json`: conteos por institución (establecimientos, con internamiento, categoría II o III, camas, departamentos).
- `datos/renipress_institucion_departamento_20261116.csv`: establecimientos por departamento e institución.
- `geo/puntos.json`: un registro por establecimiento, en este orden: latitud, longitud, red (0 MINSA y gobiernos regionales, 1 EsSalud, 2 Sanidades FFAA, 3 Sanidad PNP, 4 privados, 5 municipales, INPE y otros), capacidad (2 hospital general, 1 con internamiento, 0 sin internamiento), ubicación aproximada (1 o 0), código de departamento, nombre, categoría y distrito.
- `geo/departamentos.json`: resumen por departamento y red.
- `geo/departamentos_contornos.json`: contornos departamentales.

**Definiciones.** Hospital general: categorías II-1, II-2, III-1 y III-2 (los II-E y III-E son establecimientos especializados). Ubicación aproximada: 7 003 establecimientos (26 %, casi todos privados) no traen coordenadas; se ubican en el promedio de los demás establecimientos de su distrito, con un desplazamiento fijo, y se dibujan como anillos. El campo de camas viene vacío para los establecimientos privados.

## Licencias

Textos y datos de Qhawana: CC BY 4.0. Código: MIT. **Excepción:** `geo/departamentos_contornos.json` deriva de `peru_departamental_simple.geojson` del repositorio [juaneladio/peru-geojson](https://github.com/juaneladio/peru-geojson) (límites del INEI, 2007), simplificado (solo código y nombre, coordenadas a tres decimales). Ese archivo mantiene su licencia original, **Mozilla Public License 2.0**.

## Reglas

1. Solo documentos públicos y oficiales; la prensa, como pista por verificar.
2. Cuando dos fuentes oficiales difieren, se muestran ambas.
3. Lo que alguien del equipo sabe por experiencia propia entra como pista hasta que un documento público lo respalde.
4. Sin datos personales: ni de pacientes, ni de directores, ni de funcionarios.
5. Contar establecimientos no es medir capacidad ni cobertura: no se calcula cobertura por habitante sin población con fecha (INEI).
