# Manual 05 · Personas, permisos y seguridad

**Qué es:** mantener quién puede hacer qué en el repositorio, y reaccionar si algo se ve mal.
**Quién:** las personas administradoras (Owners) de la organización `qhawana-peru`. Siempre debe haber al menos dos, sin cargo en partidos políticos.
**Puesta en marcha:** la guía de administración explica la configuración inicial (pasos 1 a 11). Este manual es para el día a día.

## Alta de una persona (15 min)

1. Que firme el acuerdo de colaborador.
2. Que cree su cuenta de GitHub y active la verificación en dos pasos (la organización la exige).
3. **Organización › People › Invite member**, con rol **Member**.
4. **Teams**: agrégala al equipo de su rol (`comite-editorial`, `datos`, `analistas` o `coordinacion`).
5. Anota el alta en la bitácora: nombre, rol, fecha. Si tiene un cargo en un partido político, se declara.

## Baja de una persona (5 min)

La misma semana en que deja su rol: **People › ⋯ › Remove from organization**. Su trabajo queda en el historial con su nombre. Anótalo en la bitácora.

## Revisión trimestral (15 min)

- [ ] **People:** ¿todos siguen activos y en el equipo correcto? ¿Hay al menos dos Owners?
- [ ] **Settings › Authentication security:** sigue marcado "Require two-factor authentication".
- [ ] **Settings › Member privileges:** permisos de base en **Read**.
- [ ] **Repositorio › Settings › Rules:** la regla **Cuatro ojos** sigue activa y sin excepciones (bypass vacío).
- [ ] **Token del bot:** fecha de vencimiento (está en el calendario compartido). Si vence en menos de un mes, renuévalo (guía de administración, paso 9).
- [ ] **Correo de Qhawana:** puedes entrar, y los códigos de respaldo están en el gestor de contraseñas compartido.

## Si algo se ve mal

| Señal | Qué hacer |
|---|---|
| Un cambio en `main` que nadie aprobó | Revisa **Settings › Rules** (alguien desactivó la regla). Revierte el cambio con una propuesta y cambia las contraseñas de los Owners. |
| Una persona desconocida en People | Quítala y revisa en **Settings › Audit log** qué hizo. |
| Perdiste tu teléfono o tu acceso | Usa los códigos de recuperación de GitHub. Si no los tienes, la otra persona Owner te quita y te vuelve a invitar cuando recuperes la cuenta. |
| Una cuenta del equipo fue robada | Quítala de la organización de inmediato. Revisa el Audit log y las propuestas de los últimos días. |
| Spam o ataques en issues | **Settings › Moderation options › Interaction limits**: limita los comentarios a colaboradores por 24 horas o una semana. |

## Lo que no se hace nunca

- Compartir una cuenta personal. Cada persona entra con la suya.
- Guardar contraseñas o tokens en el repositorio, en issues o en chats.
- Dar permisos de Owner o de administración a personas con cargos partidarios.
- Saltarse la regla de cuatro ojos "solo esta vez".
