# Guía para el equipo

Para analistas, comunicación y cualquier persona que colabore con Qhawana. No necesitas saber programar: todo se hace desde el navegador.

## Antes de empezar

1. Firma el acuerdo de colaborador (`docs/acuerdo-colaborador.md`).
2. Crea tu cuenta en github.com con tu correo personal.
3. Activa la verificación en dos pasos: **Settings › Password and authentication › Two-factor authentication**. Sin esto la organización no te deja entrar.
4. Acepta la invitación a la organización Qhawana que te llegará por correo.

Tu primera tarea la haces acompañado de alguien del equipo.

## Lo que vas a hacer más seguido

### Revisar la descarga del lunes (finanzas públicas)

Cada lunes a las 8:00 se descargan solos los siete archivos del MEF y aparece una propuesta llamada **Corte MEF del AAAA-MM-DD** en la pestaña **Pull requests**.

1. Ábrela y lee el comentario de validación.
2. Si dice "todo cuadra", revisa los avisos de cambios bruscos: si algún presupuesto cambió más de 10 %, anota en un comentario si sabes por qué (una transferencia, un decreto). No lo corrijas: solo lo anotas.
3. El comité la aprueba.

### Subir un corte a mano (si aparece "Descarga manual pendiente")

1. Abre los siete enlaces de la sección **Descarga con enlaces directos** de `docs/el-nino-guia-descarga-mef.md`. Cada uno baja un archivo `.xls`.
2. No los abras. Renómbralos así: `AAAAMMDD_PP0068_D1_niveles_p1de1.xls`, `..._D2_GR-actividades_...`, y así hasta D7 (la tabla de la guía tiene el detalle de cada uno).
3. Pon los siete en una carpeta llamada con la fecha, por ejemplo `2026-10-26`.
4. En el repositorio, entra a `el-nino/fuentes/mef/` y pulsa **Add file › Upload files**.
5. Arrastra la carpeta completa a la página (funciona en Chrome y Edge).
6. Abajo, elige **Create a new branch for this commit and start a pull request** y pulsa **Propose changes**, y luego **Create pull request**.
7. En unos minutos aparece el comentario de validación. Si algo falla, el comentario dice qué y cómo corregirlo: vuelve a bajar ese archivo y súbelo a la misma propuesta (**Add file › Upload files** desde la rama de la propuesta).

### Registrar un hecho (decretos, comunicados, alertas)

1. Pestaña **Issues › New issue › Registrar un hecho**.
2. Llena el formulario. El enlace debe ir a la fuente primaria: el PDF del ENFEN, la norma en El Peruano, el informe de la Contraloría. Una nota de prensa sirve para encontrar el documento, pero no se registra como fuente.
3. Copia en "Cita textual" el fragmento exacto que respalda lo que escribiste.
4. Pide a otra persona del equipo que lo revise. Si está bien, esa persona le pone la etiqueta `listo-para-registrar`.
5. Se abre sola una propuesta que agrega el hecho a la bitácora. El comité la aprueba.

### Tomar una tarea

En **Issues**, filtra por la etiqueta `tarea`. Para tomar una, pulsa **Assign yourself**. Si no puedes terminarla a tiempo, escríbelo en la tarea y quítate la asignación: no pasa nada, lo importante es que nadie la crea en curso.

## Reglas que no cambian

- Toda cifra con fuente primaria y fecha de corte.
- Nada de datos personales: ni de damnificados, ni de funcionarios, ni del equipo.
- Hechos, no adjetivos. No se atribuyen intenciones a nadie.
- Si tienes un conflicto de interés en un territorio (eres candidato, funcionario o contratista de ese gobierno), no trabajas sobre ese territorio.
- No hablas en nombre de Qhawana sin que el comité lo acuerde.
- Si eres servidor público, no usas información, tiempo ni recursos de tu cargo.

## Si algo no funciona

Escribe en la tarea o en la propuesta donde te trabaste, con una captura de pantalla. Alguien de `datos` responde.
