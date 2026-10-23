# Guía de emergencias · Observatorio El Niño

Cómo se registra una emergencia del INDECI en el observatorio. Reglas de fondo: documento técnico, sección "Reglas de la franja de impacto". No hace falta saber programar.

## 1. Encontrar los reportes

- Portal: <https://portal.indeci.gob.pe/emergencias/>. Cada evento tiene reportes numerados (preliminar, complementario, informe de emergencia) que se actualizan con el tiempo.
- Búsqueda por región en formato de lista: `https://portal.indeci.gob.pe/emergencias/feed/?s=piura` (cambia `piura` por la región; agrega `&paged=2` para la página siguiente). **No devuelve todos los reportes**: en la prueba del 23 de octubre faltaba el N.º 14589 de Piura. Revisa también la portada del portal y los boletines del COER de cada región.
- La prensa sirve para saber dónde buscar, nunca como fuente.

## 2. Decidir si entra

| Pregunta | Si la respuesta es no |
| --- | --- |
| ¿La **fecha de ocurrencia** (sección 1, "Hechos") es del 1 de setiembre de 2026 o posterior? | Va como excluido. Ojo: un reporte de octubre puede ser de un evento de febrero. |
| ¿El peligro es lluvia o un efecto de la lluvia (inundación, huaico, deslizamiento, derrumbe, desborde, erosión, quebrada)? | No entra. |
| ¿La región está en el piloto (Tumbes, Piura, Lambayeque, La Libertad)? | Anótalo como tarea para cuando se amplíe. |

## 3. Archivar el PDF

1. En la página del reporte, copia el enlace del PDF (termina en `.pdf` y lleva el número del reporte).
2. Abre una propuesta que agregue una línea a `el-nino/config/indeci_reportes.json` con el número, la región y el enlace.
3. La automatización **Descargar reportes de INDECI** baja el PDF y lo guarda con su huella en `el-nino/fuentes/indeci/AAAA-MM-DD/`. Si el PDF no existe, lo dice en el manifiesto y no se guarda nada.

## 4. Copiar las cifras

En `el-nino/datos/emergencias.csv`, una fila por evento, con la **última versión archivada**:

- Cifras del cuadro **3.1 Reporte de daños** del PDF, tal cual. Si un daño está descrito pero no contado, deja la celda vacía.
- Kilómetros: si el reporte da metros, conviértelos (200 m = 0.2).
- `nota`: diferencias entre versiones, errores del documento, distritos sin cifras.
- `sinpad`: el código, o "sin registro" si el reporte lo dice.
- Si una versión nueva cambia las cifras, actualiza la fila y explica en `nota` qué cambió.

## 5. Revisión

El validador revisa que cada fila incluida tenga su PDF archivado, enlace del INDECI, fecha dentro del periodo, región del piloto y cifras numéricas o vacías. Un miembro del comité que no preparó la fila compara las cifras con el PDF antes de aprobar.
