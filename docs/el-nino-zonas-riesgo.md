# Zonas de riesgo por distrito (Observatorio El Niño, pestaña "Riesgo")

18 de noviembre de 2026 · Estado: publicado **sin revisión de cuatro ojos** (decisión de Pepe), anotado en la bitácora.

## Qué responde

¿Qué distritos del país tienen mayor riesgo ante las lluvias de El Niño y cuánta gente vive ahí? La pestaña junta tres estudios oficiales del CENEPRED. Para Lima Metropolitana y el Callao baja hasta el nivel de manzana, sumado por distrito. No calcula un índice propio ni elige entre estudios.

## Fuentes

Todas vienen del SIGRID del CENEPRED y se consultaron el 18 de noviembre de 2026. Se usó el Excel de cada ficha, no el PDF.

| Clave | Estudio | Ficha | Excel | Unidad |
|---|---|---|---|---|
| A | Escenario El Niño, actualizado con el informe técnico N.º 69-2026/SENAMHI-DMA-SPC (lluvias de los Niños 1983, 1998, 2017 y 2023) | [22169](https://sigrid.cenepred.gob.pe/sigridv3/documento/22169) | `escenario_climatico_llu/13_excel.zip` | Distrito; población del distrito completo |
| B | Verano 2027, actualización de octubre (informe técnico N.º 13-2026/SENAMHI-DMA-SVC) | [23278](https://sigrid.cenepred.gob.pe/sigridv3/documento/23278) | `escenario_trimestral/103_tabla.zip` | Distrito; población en las zonas de mayor susceptibilidad |
| L | Lima Metropolitana y Callao, El Niño 2026-2027 | [23279](https://sigrid.cenepred.gob.pe/sigridv3/documento/23279) | `escenario_climatico_llu/17_excel.zip` | Manzana censal (Censos 2025) |

Los puntos críticos son los tramos de la ANA que vienen en el Excel de B (`Puntos_criticos_IT132026.xlsx`).

## Archivos

- `el-nino/datos/riesgo_distritos_cenepred.csv`: 1893 distritos.
  - Columnas: `ubigeo, dep, prov, dist, pob` (población del estudio A), `a_inu, a_mm` (nivel de riesgo en A, por inundación y por movimientos en masa), `b_inu, b_pinu, b_mm, b_pmm` (nivel en B y población en las zonas de mayor susceptibilidad), `pc_inu, pc_mm` (tramos críticos de la ANA).
  - Escala de niveles: 1 bajo, 2 medio, 3 alto, 4 muy alto.
- `el-nino/datos/riesgo_lima_cenepred.csv`: 50 distritos de Lima Metropolitana y Callao.
  - Por nivel de riesgo: manzanas y población (`ma` muy alto, `a` alto, `m` medio, `b` bajo).
  - Solo para riesgo muy alto: niños de 0 a 5 años, mayores de 65, establecimientos de salud y colegios.
- `el-nino/config/riesgo.json`: títulos, enlaces y fecha de consulta.

## Cómo se obtuvo

1. El SIGRID no responde a servidores fuera del Perú. Los Excel se abrieron en el navegador integrado con JSZip y SheetJS y se convirtieron allí a CSV.
   - A: hojas `Riesgo por inundación` y `Riesgo por MMasa`.
   - B: hojas `BD_ERInund` y `BD_ERMMasa`.
   - L: hoja `BD_ERISLima`, sumada por `UBIGEO` y `n_riesgo`.
2. Los tramos de la ANA con un ubigeo que no está en la lista de distritos quedan fuera. Por ejemplo `00000`, o distritos creados después del censo como 022009 o 120300.
3. **Control:** `herramientas/tests/test_zonas_riesgo.py` comprueba que los CSV cuadren con los totales que el CENEPRED imprime en las hojas de resumen de sus Excel. Todos cuadran exactamente:
   - A, inundación: 209 distritos y 7 951 322 personas en riesgo muy alto; 557 y 11 963 523 en alto.
   - A, movimientos en masa: 185 distritos y 1 383 000 personas en riesgo muy alto.
   - B, inundación: 153 distritos y 5 323 000 personas en zonas de mayor susceptibilidad; 289 y 3 683 797 en alto.
   - B, movimientos en masa: 787 distritos y 3 912 232 personas.

## Diferencias que se muestran y no se corrigen

- **Lima: PDF frente a Excel del estudio L.**

  | Riesgo | PDF, tabla 13 | Excel |
  |---|---|---|
  | Muy alto | 609 550 | 609 586 |
  | Alto | 520 734 | 520 849 |
  | Medio | 460 899 | 461 079 |

  Bajo (30 personas), establecimientos de salud (26) y colegios (187) en riesgo muy alto coinciden. Las cifras por distrito, como las 115 756 personas de San Juan de Lurigancho, coinciden con la tabla 14. Se publica el Excel y la página declara la diferencia.
- **Lima: tres cifras distintas, de tres estudios.**
  - L: 609 586 personas viven en manzanas de riesgo muy alto.
  - A: 1 822 466 personas viven en los 6 distritos de Lima Metropolitana y Callao que el estudio clasifica en riesgo muy alto. Con Lima provincias, son 2 278 267 en 18 distritos del departamento de Lima: es la cifra de "2,28 millones" que citaba la prensa.
  - B: 455 773 personas, casi todas del Callao.

  No se suman ni se comparan como si midieran lo mismo.
- **A frente a B:** 100 distritos están en riesgo muy alto por inundación en los dos estudios. Esa es la vista inicial ("Mayor riesgo del país").
- **Pestaña Brechas:** todavía usa la versión de mayo de A, transcrita del PDF (`exposicion_cenepred.csv`). Actualizarla a esta versión es una decisión pendiente, porque cambia cifras ya publicadas.

## Límites

- Riesgo no es daño ni necesidad. La evaluación de daños y necesidades (EDAN) la hacen el INDECI y los gobiernos locales.
- Los nombres de distrito vienen sin tildes, tal como los trae el INEI en los Excel.
- La población de A y la de L vienen de censos distintos: L usa los Censos 2025.

## Actualizar

Cuando el CENEPRED publique una versión nueva, se hacen tres cosas:

1. Cambiar el enlace en `riesgo.json`.
2. Repetir el paso 1 con el Excel nuevo.
3. Poner en la prueba los totales impresos de la nueva hoja de resumen.
