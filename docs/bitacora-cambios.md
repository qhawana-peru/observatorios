# Bitácora de cambios

Toda corrección, cambio de método o decisión editorial que afecte lo publicado, con fecha y qué cambió. Lo más reciente arriba.

## 2026-10-14

- **Repositorio creado.** Primera versión de las herramientas (lectura y validación de archivos del MEF, sitio, automatizaciones), la metodología del Observatorio El Niño y las guías del equipo.
- **Carga inicial de datos del 14 de octubre.** Las 115 filas de `el-nino/datos/ejecucion_pp0068.csv` con fecha 2026-10-14 se tomaron de la exportación pública del MEF leída en el navegador, no de archivos guardados; por eso esa fecha no tiene carpeta en `el-nino/fuentes/mef/`. Pasaron los seis controles. El primer corte con archivos originales será el del lunes 26 de octubre.
- **Dato del 13 de octubre (46,9 %).** Viene de una lectura en pantalla del MEF sin archivo guardado. Ese día el PIM total era S/ 4,763.4 M; el 14 de octubre, S/ 4,751.7 M. El cambio regional más visible es Tumbes (de S/ 73.3 M a S/ 58.2 M según las dos lecturas); queda por verificar si fue una modificación presupuestaria o un error de la lectura del 13.
- **Bitácora de hechos.** Las entradas marcadas como `prensa` en `el-nino/datos/hechos.csv` están pendientes de reemplazo por su fuente primaria.
