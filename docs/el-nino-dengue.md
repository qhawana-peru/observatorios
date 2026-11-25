# Dengue en el Observatorio El Niño (piloto)

Desde el 25 nov 2026. Responde a una pregunta frecuente: ¿el aumento del dengue tiene que ver con El Niño?

## Qué se publica
- Casos de dengue (confirmados y probables) acumulados hasta la misma semana epidemiológica de cada año, de 2021 a 2026, por departamento. Archivo: `el-nino/datos/dengue_cdc.csv`.
- Cifras nacionales de la semana (casos y defunciones) y alertas epidemiológicas del CDC-MINSA: `el-nino/config/dengue.json`.
- En la página, pestaña 4 Impacto: las cuatro regiones del piloto (Tumbes, Piura, Lambayeque y La Libertad) y el total del país, para 2023, 2024, 2025 y 2026.

## Fuente
[Sala situacional de enfermedades metaxénicas del CDC-MINSA](https://app7.dge.gob.pe/maps2/shiny_metaxenicas_web/), pestaña **Tablas**, tabla "Casos totales por año y departamentos". Se actualiza cada semana. La primera carga es de la semana 45 (corte 14 nov 2026, publicada el 20 nov). Se comprobó que la suma de los departamentos es igual al total del país.

## Cómo se actualiza
1. Abrir la sala (desde un navegador en el Perú) y la pestaña Tablas.
2. Copiar la tabla por departamentos y las cifras nacionales de la semana a los dos archivos.
3. Cambiar `se`, `corte`, `actualizado_fuente` y `consultado` en `dengue.json`.

## Reglas de lectura
- **Periodos iguales.** Se compara hasta la misma semana de cada año, no años completos.
- **Coincidencia no es causa.** El CDC-MINSA atribuyó en parte las epidemias de 2023 y 2024 a El Niño costero y al ciclón Yaku ([AE-CDC N.º 001-2026](https://epipublic.dge.gob.pe/uploads/alertas/alertas_20261_09_145341.pdf)). Calor y lluvias favorecen al vector, pero también pesan el serotipo, la inmunidad previa, el almacenamiento de agua y el control vectorial. El observatorio no atribuye casos a El Niño.
- **Base baja.** 2025 tuvo muy pocos casos; el aumento frente a 2025 se lee junto con 2023 y 2024.

## Pendientes
- Archivar el PDF oficial de la alerta epidemiológica N.º 008-2026 (oct 2026, por El Niño 2026-2027). Hoy solo se conoce por la Agencia Andina.
- Serie semanal (canal endémico) por región, para ver si la subida está fuera de lo habitual para la época.
- Leptospirosis, que también sube con las lluvias.
- Que una persona de epidemiología revise el método.
