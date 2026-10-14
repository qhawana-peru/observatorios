# Guía de administración: poner en marcha las cuentas de Qhawana

Para quien administra Qhawana. No hace falta saber programar ni haber usado GitHub antes. Toma entre una y dos horas, y conviene hacerlo con la segunda persona administradora al lado.

GitHub cambia a veces el nombre exacto de los menús. Si algo no aparece donde dice esta guía, busca la palabra en el buscador de la configuración.

## Qué es GitHub, en una línea

Un lugar donde se guardan archivos con su historia completa: quién cambió qué, cuándo y quién lo aprobó. Lo usan universidades, gobiernos y medios para publicar datos abiertos. Es gratuito para proyectos públicos.

Tres palabras que vas a ver:

- **Repositorio:** la carpeta del proyecto, con todo su historial.
- **Propuesta de cambio** (en GitHub: *pull request*): un cambio que alguien sugiere y que otra persona revisa antes de que entre.
- **Organización:** la cuenta institucional de Qhawana. Las personas entran con su cuenta propia y la organización les da permisos.

## Paso 1. Correo de Qhawana

1. Crea una cuenta de correo para Qhawana (por ejemplo, en Gmail). Es el correo de contacto de la convocatoria y el de recuperación de las cuentas.
2. Activa la verificación en dos pasos.
3. Guarda la contraseña y los códigos de respaldo en un gestor de contraseñas al que tenga acceso la segunda persona administradora.

## Paso 2. Tu cuenta personal en GitHub

1. Entra a github.com y crea tu cuenta con tu correo personal. Esta cuenta es tuya, no de Qhawana.
2. En tu perfil, ve a **Settings › Password and authentication** y activa **Two-factor authentication** con una app de códigos (Google Authenticator, Microsoft Authenticator o similar). Guarda los códigos de recuperación.

La segunda persona administradora hace lo mismo con su propia cuenta.

## Paso 3. Crear la organización Qhawana

1. Con tu cuenta abierta, ve a **github.com/organizations/plan** y elige el plan **Free**.
2. Nombre de la organización: `qhawana-peru` (ya creada).
3. Correo de contacto: el correo de Qhawana del paso 1.
4. Cuando pregunte a quién pertenece, elige que es de una persona (tu cuenta). Más adelante se transfiere al receptor del observatorio.
5. Invita a la segunda persona administradora con el rol **Owner**.

## Paso 4. Seguridad de la organización

En la organización, **Settings**:

1. **Authentication security:** marca **Require two-factor authentication** para todos los miembros.
2. **Member privileges › Base permissions:** elige **Read**. Así nadie puede cambiar nada sin pasar por una propuesta.

## Paso 5. Crear el repositorio y subir el contenido

1. En la organización, botón **New repository**.
2. Nombre: `observatorios`. Visibilidad: **Public**. No marques ninguna opción de agregar archivos.
3. Para subir el contenido hay dos caminos:
   - **Recomendado:** conecta GitHub a Claude (en claude.ai, la configuración de conectores), dale acceso a la organización Qhawana y pídeme que suba el repositorio. Lo dejo listo y te aviso.
   - **Por tu cuenta:** instala la aplicación **GitHub Desktop**, inicia sesión, clona el repositorio vacío, copia dentro el contenido de la carpeta `observatorios` que te entregué (incluida la carpeta oculta `.github`) y pulsa **Commit** y luego **Push**.

## Paso 6. Equipos

En la organización, **Teams › New team**. Crea cuatro equipos (los nombres deben ser exactos, porque las reglas de aprobación los usan):

| Equipo | Quiénes | Permiso sobre el repositorio |
| --- | --- | --- |
| `comite-editorial` | Las 3 personas del comité | **Write** |
| `datos` | Gestor(a) de datos | **Maintain** |
| `analistas` | Finanzas públicas, peligro y riesgo, comunicación | **Write** |
| `coordinacion` | Coordinador(a) general | **Triage** |

Para dar el permiso: entra al repositorio, **Settings › Collaborators and teams › Add teams**.

Mientras opera el núcleo transitorio, pon a sus integrantes en `comite-editorial` y `datos`, y anótalo en `docs/bitacora-cambios.md`.

## Paso 6b. Permitir que las automatizaciones abran propuestas

Sin esto, la descarga de los lunes baja los archivos pero no puede abrir la propuesta para el comité.

1. En la organización, **Settings › Actions › General › Workflow permissions**: elige **Read and write permissions** y marca **Allow GitHub Actions to create and approve pull requests**. Guarda.
2. Repite lo mismo en el repositorio: **Settings › Actions › General**, misma sección.

## Paso 7. Publicar el sitio

En el repositorio, **Settings › Pages › Build and deployment › Source:** elige **GitHub Actions**. La primera publicación sale sola en cuanto se apruebe el primer cambio; también puedes lanzarla desde **Actions › Publicar sitio › Run workflow**.

La dirección será `https://qhawana-peru.github.io/observatorios/`. Un dominio propio se puede agregar después en esa misma pantalla.

## Paso 8. La regla de cuatro ojos

Esto hace que nada se publique sin que otra persona del comité lo apruebe, incluido tú.

En el repositorio, **Settings › Rules › Rulesets › New ruleset › New branch ruleset**:

1. Nombre: `Cuatro ojos`. **Enforcement status:** Active.
2. **Bypass list:** déjala vacía. Ni los administradores pueden saltarse la regla.
3. **Target branches:** *Include default branch*.
4. Marca:
   - **Restrict deletions** y **Block force pushes**.
   - **Require a pull request before merging**, con **Required approvals: 1**, **Dismiss stale pull request approvals when new commits are pushed** y **Require review from Code Owners**.
   - **Require status checks to pass**, y agrega el control llamado `validar`. Aparece en la lista después de la primera propuesta; si no lo ves, vuelve a este paso cuando exista una.
5. Guarda.

GitHub no deja que alguien apruebe su propia propuesta, así que el autor siempre necesita a otra persona.

## Paso 9. La cuenta del bot

Las automatizaciones (descarga de los lunes, registro de hechos) abren propuestas. Para que esas propuestas pasen por la validación, necesitan un permiso propio.

1. Crea una segunda cuenta de GitHub llamada `qhawana-bot` con el correo de Qhawana. GitHub permite una cuenta de máquina así por persona.
2. Invítala a la organización y al equipo `analistas`.
3. Con la sesión de `qhawana-bot` abierta: **Settings › Developer settings › Personal access tokens › Fine-grained tokens › Generate new token**.
   - **Resource owner:** qhawana-peru. **Repository access:** solo `observatorios`.
   - **Permissions:** Contents, Pull requests e Issues en **Read and write**.
   - **Expiration:** un año. Anota la fecha en un calendario compartido.
4. Copia el código que aparece (solo se muestra una vez).
5. En el repositorio, **Settings › Secrets and variables › Actions › New repository secret**. Nombre: `QHAWANA_BOT_TOKEN`. Pega el código.

Si la organización pide aprobar el token, apruébalo en **Settings › Personal access tokens › Pending requests**.

## Paso 10. Etiquetas

En el repositorio, **Issues › Labels › New label**. Crea: `hecho`, `listo-para-registrar`, `correccion`, `tarea`, `el-nino`, `descarga-manual`.

## Paso 11. Probar que todo funciona

1. **Actions › Descargar corte del MEF › Run workflow.** En unos minutos debe aparecer una propuesta nueva con siete archivos y un comentario de validación. Si en cambio aparece un aviso de "descarga manual pendiente", los servidores de GitHub no llegan al MEF: avísame y lo resolvemos; mientras tanto, la descarga se hace a mano con los enlaces de la guía.
2. Pide a otra persona del comité que la apruebe y la una (**Merge**). Revisa que el sitio se actualice.

## Altas y bajas

- **Alta:** firma del acuerdo de colaborador, invitación a la organización, alta en el equipo de su rol, verificación en dos pasos activa.
- **Baja:** retirarla de la organización la misma semana en que deja su rol. Su trabajo queda en el historial, con su nombre.

## Transferencia

Cuando Qhawana entregue el observatorio hay dos caminos: transferir el repositorio a la organización de GitHub del receptor (**Settings › General › Transfer ownership**, al final de la página), o agregar a sus responsables como Owners de la organización Qhawana y retirarse después. En ambos casos todo el historial viaja con el repositorio.
