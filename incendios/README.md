# Monitor de incendios forestales

Página pública: `/incendios/` del sitio de Qhawana. Método completo: [`docs/incendios-metodologia.md`](../docs/incendios-metodologia.md).

## Cómo actualizar un corte

1. Consulta el servicio de SERFOR desde un navegador (ver metodología) y actualiza los CSV de `datos/` con la nueva fecha de corte.
2. Cambia `fecha_corte` en `config/sitio.json`.
3. Agrega una fila por región a `datos/seguimiento_proyeccion.csv` con los focos Suomi NPP al nuevo corte y el rango proyectado en ese momento.
4. Revisa `datos/pistas.csv`: cambia el estado de las pistas verificadas y agrega las nuevas con `registrada` y `vence` (30 días).
5. Abre una propuesta de cambio. Otra persona del comité la revisa antes de unirla.

## Cómo se verifica una pista

Con el formulario **Verificar una pista** del repositorio. Quien la revisa actualiza `pistas.csv` y, si corresponde, pasa la cifra oficial a los datos del observatorio con su fuente.
