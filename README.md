# Qhawana · Observatorios

**Qhawana** (quechua: "lugar desde donde se mira") es una iniciativa ciudadana que construye observatorios con datos públicos para mirar qué pasa en el Perú y qué hace el Estado al respecto. Cada cifra enlaza a su fuente oficial, el método es público y un comité editorial con reglas conocidas decide qué se publica.

Este repositorio contiene todo lo necesario para operar los observatorios: los archivos originales descargados de fuentes oficiales, los datos procesados, el código que los valida y publica, la metodología y la bitácora de cambios. Está hecho para que otro equipo pueda continuarlo sin el equipo fundador.

## Observatorios

| Observatorio | Pregunta | Estado |
| --- | --- | --- |
| **El Niño** (`el-nino/`) | ¿Qué hizo el Estado con el aviso que tuvo antes del Fenómeno El Niño 2026-2027? | En operación (fase 1) |
| Incendios forestales | ¿Dónde y cuánto se quema, y qué tan lejos está el fin de la temporada? | Por migrar a este repositorio |
| Contraste (criminalidad) | ¿Por qué las fuentes oficiales no coinciden, y qué compra el presupuesto de seguridad? | En diseño |

## Cómo se publica una cifra

1. **Carga.** Los archivos del MEF se descargan cada lunes (automáticamente o a mano) y entran como una *propuesta de cambio*. Los hechos (comunicados, decretos, alertas) se registran con el formulario **Registrar un hecho**, con fuente primaria obligatoria.
2. **Validación automática.** Cada propuesta pasa por los seis controles de la [guía de descarga](docs/el-nino-guia-descarga-mef.md). El resultado aparece como comentario en la propuesta.
3. **Aprobación.** Un miembro del comité editorial que no preparó el dato revisa y aprueba. Sin esa aprobación, nada entra.
4. **Publicación.** Al aprobarse, el sitio y los datos abiertos se regeneran desde los archivos originales.

## Estructura

```
el-nino/
  fuentes/mef/AAAA-MM-DD/   archivos originales del MEF, tal como se descargaron (no se editan)
  datos/                    datos abiertos: ejecucion_pp0068.csv y hechos.csv
  config/                   enlaces de descarga, contexto por región, estado del sitio
herramientas/               programas en Python (solo biblioteca estándar) y sus pruebas
sitio/                      plantilla de la página pública
docs/                       metodología, guías para el equipo y documentos de gobernanza
.github/                    formularios, plantillas y automatizaciones
```

## Para el equipo

- ¿Primera vez? Empieza por la [guía para el equipo](docs/guia-equipo.md). No necesitas saber programar.
- ¿Eres del comité editorial? Empieza por la [cartilla de 5 minutos](docs/cartilla-comite.md) y luego la [guía del comité](docs/guia-comite.md).
- ¿Administras las cuentas? Lee la [guía de administración](docs/guia-administracion.md).

## Correr las herramientas en tu computadora

Requiere Python 3.10 o superior, sin instalar nada más.

```bash
python -m unittest discover -s herramientas/tests          # pruebas
python herramientas/validar.py el-nino/fuentes/mef/2026-10-26   # validar un corte
python herramientas/construir_sitio.py                        # generar el sitio en _site/
```

## Licencias

- **Textos y datos:** [Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](LICENSE-DATOS.md). Puedes usarlos y adaptarlos citando a Qhawana y a la fuente oficial.
- **Código:** [MIT](LICENSE).
- Los archivos originales en `el-nino/fuentes/` son información pública del Estado peruano; se conservan sin cambios como respaldo de cada cifra.

## Correcciones

Si encuentras un error, usa el formulario **Reportar un error**. Toda corrección se revisa en 48 horas y se publica con fecha y qué cambió en la [bitácora de cambios](docs/bitacora-cambios.md).
