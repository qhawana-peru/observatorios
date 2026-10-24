# Manual 03 · Pistas por verificar

**Qué es:** las cifras que aparecen en la prensa o en redes y que el observatorio muestra aparte, marcadas como "sin verificar", para que alguien las contraste con una fuente oficial. Nunca entran en los cálculos.
**Cada cuánto:** cuando llega una verificación, y una revisión el día 1 de cada mes.
**Tiempo:** unos 10 minutos por pista.
**Quién:** cualquiera puede verificar; el comité decide.
**Dónde están:** `incendios/datos/pistas.csv`.

## Ciclo de una pista

1. **Registro:** alguien del equipo agrega una fila con la cifra, el medio, la fecha, el enlace, la pregunta concreta y dónde verificarla. Fecha de registro = hoy; vence a los 30 días.
2. **Verificación:** cualquier persona usa el formulario **Verificar una pista** (botón "Ayúdanos a verificar" del sitio). Debe dar la fuente oficial con enlace y fecha.
3. **Decisión del comité:** cambia el campo `estado`:
   - `verificada`: la fuente oficial dice lo mismo.
   - `corregida`: la fuente oficial da otra cifra. Se anota cuál.
   - `descartada`: no hay fuente oficial o la cifra no se sostiene.
4. **Paso a los datos:** si la fuente oficial es de las que usa el observatorio, la cifra oficial pasa a los datos con su fuente y fecha de corte. La pista se queda en `pistas.csv` como registro.
5. **Vencimiento:** a los 30 días sin verificar deja de mostrarse sola. No se borra.

## Cómo revisar una verificación

1. Abre el issue con la etiqueta `pista`.
2. Abre el enlace oficial que dio la persona. Revisa que la cifra, el lugar y la fecha coincidan con la pregunta de la pista.
3. Si está bien: edita `pistas.csv` (lápiz › cambia el `estado` › rama nueva › propuesta). En la propuesta, enlaza el issue.
4. Agradece en el issue y ciérralo cuando se una la propuesta. Quien verifica es la persona que más queremos que vuelva.

## Reglas

- La prensa es pista, nunca fuente de cifras publicables.
- Si dos fuentes oficiales difieren, se muestran ambas y se explica por qué. No se elige la que conviene.
- Nada de nombres de víctimas, heridos ni datos personales, aunque la nota los traiga.
- No se publican números de cuentas, Yape o Plin de colectas sin verificar.

## Revisión mensual (día 1)

- ¿Cuántas pistas vencieron sin verificar? Si son la mayoría, el mecanismo no está funcionando: difúndelo o cambia cómo se pregunta.
- ¿Hay alguna que convenga renovar? Se registra de nuevo con fecha nueva y se anota en la bitácora.
