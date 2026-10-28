# Brechas: exposición frente a respuesta (Observatorio El Niño)

27 de octubre de 2026 · Estado: **sin revisión del comité editorial** (la página lo dice en un recuadro).

## Qué responde

¿Cuánta gente está expuesta a El Niño en cada territorio, y qué respuesta del Estado se puede medir ahí con datos públicos? Pone las dos cosas lado a lado. No calcula un índice, ni ordena territorios, ni dice dónde ayudar: muestra las cifras para que organizaciones, medios y autoridades decidan.

## Territorios (fase actual)

Lima y Callao, más cinco regiones de la costa: Piura, Tumbes, Lambayeque, La Libertad e Ica. Se eligieron así:

- **Lima y Callao:** la mayor población en riesgo alto por inundación del país según el CENEPRED. Al sumar Callao, también tiene más de medio millón de personas en riesgo muy alto.
- **Piura:** la mayor población en riesgo muy alto por inundación.
- **Tumbes, Lambayeque y La Libertad:** son el piloto de emergencias y tienen ríos con caudales sobre lo normal desde noviembre (ENFEN N.º 18).
- **Ica:** concentra cerca del 44 % del presupuesto regional del PP 0068 y tiene más de 440 mil personas en riesgo muy alto por inundación.

Para agregar un territorio basta una entrada en `el-nino/config/brechas.json`. No hace falta tocar código.

## Fuentes y reglas

| Dato | Fuente | Archivo |
|---|---|---|
| Personas, viviendas, establecimientos de salud y colegios expuestos | CENEPRED, estudios de escenarios de riesgo | `el-nino/datos/exposicion_cenepred.csv` |
| Presupuesto y gasto | MEF, PP 0068: pliego regional (D2/D3) y municipalidades del departamento (D4/D5) | `el-nino/datos/ejecucion_pp0068.csv` |
| Plan de gestión del riesgo | Lista publicada el 27 jun 2026 | `el-nino/config/contexto.json` |
| Pronóstico | Comunicado ENFEN N.º 18-2026 | `el-nino/config/contexto.json` |
| Emergencias | COEN-INDECI, solo para el piloto | `el-nino/datos/emergencias.csv` |

### Dos escenarios oficiales del CENEPRED que no coinciden

| | Estudio A (principal) | Estudio B (secundario) |
|---|---|---|
| Título | Escenarios de riesgo por inundaciones y movimientos en masa ante lluvias intensas asociadas al FEN | Escenario de riesgo por lluvias para el verano 2027 |
| Fecha | Mayo 2026 | Agosto 2026 |
| Insumo | Lluvias máximas de los Niños de 1983, 1998, 2017 y 2023 (SENAMHI); ENFEN N.º 09 | Pronóstico estacional SENAMHI IT N.º 07-2026; ENFEN N.º 13 |
| Unidad | Distrito | Centro poblado |
| Riesgo muy alto por inundación (país) | 3 926 892 personas | 905 850 personas |

Las diferencias tienen explicación documentada. A es un escenario de "lo peor ya visto" a nivel de distrito: cuenta a toda la población del distrito. B parte de un pronóstico y cuenta solo los centros poblados expuestos. Por regla del observatorio se muestran ambos y no se elige uno. A es el principal porque se hizo para planificar ante El Niño y porque su transcripción es completa y está verificada.

**Versiones que faltan.** El CENEPRED informó que actualizó el estudio A el 30 de junio de 2026 y, según la agencia Andina (7 oct), actualizó el de verano 2027 en octubre. La prensa atribuye a esas versiones cifras mucho mayores (por ejemplo, 2,28 millones de personas en Lima en riesgo muy alto por inundación). Mientras no tengamos los PDF, esas cifras **no se publican**. Conseguirlos es la primera tarea pendiente (manual 06).

### Cómo se transcribió y verificó (cuatro ojos parcial)

1. Las tablas del PDF se leyeron con asistencia de IA. El texto extraído mezcla columnas: por ejemplo, "PIURA 2 0 1 164 486" son 20 distritos y 1 164 486 personas.
2. Cada fila se separó con dos criterios: la población debe ser mayor que el número de viviendas, y la suma de los distritos debe dar el total impreso.
3. **Control automático:** `herramientas/validar_cenepred.py` comprueba que, en el estudio A, las filas de las cuatro tablas (inundación y huaicos, riesgo muy alto y alto) sumen exactamente el total nacional impreso en las cinco columnas: distritos, población, viviendas, salud y colegios. Las 20 sumas cuadran. Corre en cada propuesta.
4. **Estudio B:** su extracción tuvo filas ilegibles (Callao, Huancavelica y Moquegua). Solo se transcribieron los seis departamentos necesarios, cuyas cifras de población y viviendas son consistentes con los totales. Callao queda "sin dato legible".
5. **Falta:** que una persona coteje cada fila con el PDF (estudio A: tablas 7 a 10, págs. 26 a 30; estudio B: tablas 3 y 4, págs. 13 y 18) y cambie `revision_humana` a `hecha` en el CSV.

## Límites que la página declara

- El CENEPRED no separa Lima Metropolitana de Lima provincias. El MEF sí, así que la ficha suma la Municipalidad Metropolitana, el Gobierno Regional de Lima y el del Callao.
- Inundación y huaicos no se suman, porque un mismo distrito puede estar en los dos.
- El PP 0068 cubre todos los peligros, no solo El Niño.
- No es una evaluación de necesidades. Esa la hacen el INDECI y los gobiernos locales (EDAN). La sección orienta hacia la lista de distritos del CENEPRED y hacia la plataforma de defensa civil local.

## Decisiones pendientes del comité

- Aprobar que se publique sin revisión, o retirarla hasta que se haga el cotejo humano.
- Decidir si se agrega un indicador relativo, como el presupuesto por persona expuesta. Hoy no se calcula a propósito: mezcla un programa multipeligro con un escenario de un solo peligro y puede leerse como un ranking.
- Decidir si se reemplaza A por su versión de junio cuando la tengamos.
