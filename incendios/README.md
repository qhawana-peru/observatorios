# Monitor de incendios forestales

Página pública: `/incendios/` del sitio de Qhawana. Método completo: [`docs/incendios-metodologia.md`](../docs/incendios-metodologia.md).

## Cómo actualizar un corte

Paso a paso en [`docs/manuales/01-corte-incendios.md`](../docs/manuales/01-corte-incendios.md). En resumen:

1. Desde un navegador, la consola en la página de SERFOR corre `herramientas/serfor_consulta.js` y descarga `serfor_AAAA-MM-DD.json`.
2. Ese archivo se sube a `cortes/` en una rama `corte-incendios-AAAA-MM-DD`.
3. La automatización **Actualizar incendios** corre `herramientas/actualizar_incendios.py`: reescribe los CSV, registra el rango publicado en el corte anterior, agrega el nuevo corte al seguimiento y cambia la fecha en `config/sitio.json`.
4. Una persona escribe la lectura del corte (`nota_corte`) y otra del comité revisa la propuesta.

Los cortes pasados no se reescriben: SERFOR completa sus registros con días de retraso, y el seguimiento guarda lo que se publicó en cada fecha.

## Cómo se verifica una pista

Con el formulario **Verificar una pista** del repositorio. Quien la revisa actualiza `pistas.csv` y, si corresponde, pasa la cifra oficial a los datos del observatorio con su fuente.
