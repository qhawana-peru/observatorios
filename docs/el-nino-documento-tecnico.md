# Observatorio El Niño — Documento técnico

13 de octubre de 2026 (revisado el 14 de octubre) · Qhawana

El observatorio responde una pregunta: **qué hizo el Estado, en cada nivel de gobierno, con el aviso que tuvo antes del Fenómeno El Niño 2026-2027.** Cruza el pronóstico oficial con las decisiones, el presupuesto y las obras, territorio por territorio, desde datos públicos verificables.

## Propósito y alcance

En octubre de 2025 el ENFEN esperaba condiciones neutras. Activó la vigilancia en enero de 2026, la alerta en febrero y en agosto ya pronosticaba un Niño Costero extraordinario, con el pico esperado entre noviembre de 2026 y febrero de 2027. El aviso efectivo fue de unos 9 a 10 meses antes del pico. Ese periodo es el objeto de estudio: cuánto aviso hubo y cuánto se convirtió en prevención.

- **Periodo:** octubre 2025 a junio 2027, con 2017 y 2023 como eventos de referencia.
- **Fase 1 (noviembre 2026 a junio 2027):** los 25 gobiernos regionales y la Municipalidad Metropolitana de Lima (los 26 pliegos que el MEF clasifica en el nivel regional), más las entidades nacionales; las municipalidades solo sumadas por departamento. Piloto en Tumbes y Piura.
- **Fase 2 (desde 2027, si hay equipo):** nivel distrital, empezando por los 796 distritos declarados en emergencia; monitoreo territorial y salud.
- **Fuera del alcance:** pronosticar el clima (eso lo hace el ENFEN), atender emergencias y recibir denuncias contra personas.

## Principios

1. **Toda cifra con fuente primaria enlazada.** La prensa sirve solo como pista para buscar la fuente primaria; no se publica como valor.
2. **Mismas reglas para todos los territorios y todos los gobiernos.** Ningún indicador se crea ni se omite según quién gobierne.
3. **Una sola cadena de medición del gasto** (PIM, certificado, comprometido, devengado, avance físico). Cada cifra dice en qué eslabón está.
4. **Hechos públicos, no personas.** No se publican datos de damnificados ni se atribuyen intenciones a funcionarios.
5. **Correcciones públicas.** Todo error se corrige en la misma página, con fecha y qué cambió.
6. **Decisiones editoriales colegiadas.** Nada se publica por decisión de una sola persona.
7. **La IA asiste, las personas verifican.** Las herramientas de IA leen documentos, extraen datos y redactan borradores; ninguna salida se publica sin revisión humana.
8. **Los servidores públicos que participen no usan información, tiempo ni recursos de su cargo**, y no ejercen vocería.
9. **Construido para ser transferido.** Todo se diseña para poder donarse a la academia o a la sociedad civil.

### Construido para ser transferido

El destino previsto es una universidad u organización de la sociedad civil. Para que la transferencia no requiera el permiso de nadie, se cumplen estas condiciones:

- **Licencias abiertas desde el primer día:** textos y datos con CC BY 4.0; código con licencia MIT. Quien colabora acepta esas licencias al sumarse, así nadie queda como dueño exclusivo de una parte.
- **Cuentas institucionales, no personales:** repositorio, dominio, carpeta compartida y herramientas a nombre del observatorio, con al menos dos administradores.
- **Sin datos personales en lo que se publica o transfiere:** los voluntarios se registran aparte, con lo mínimo, y ese registro no se publica ni forma parte de la transferencia.
- **Identidad propia:** el observatorio lleva solo la identidad de Qhawana.
- **Documentado para que otro lo opere:** metodología, guías de descarga, diccionario de datos y bitácora de decisiones al día, para que un equipo nuevo continúe sin el equipo fundador.
- **Herramientas reemplazables:** ninguna etapa depende de una sola herramienta o proveedor; si una herramienta de IA deja de estar disponible, el flujo sigue con otra o a mano.

### Cuándo y cómo se transfiere

**Regla:** el momento de la transferencia está por definir. Mientras tanto se cumplen las condiciones de arriba, para que pueda hacerse sin pedir permiso a nadie.

1. **Receptor elegido con anticipación.** El comité editorial mantiene una lista corta de posibles receptores (universidades u organizaciones de la sociedad civil) y la revisa cada seis meses.
2. **Criterios del receptor:** independencia partidaria, capacidad en finanzas públicas o gestión del riesgo, compromiso de mantener las licencias abiertas y de operar al menos dos años.
3. **Entrega completa:** cuentas, dominio, repositorio, datos, documentación y bitácora, en un plazo máximo de 60 días desde el acuerdo con el receptor.
4. **Sin privilegios para nadie:** ni Qhawana ni quienes la impulsaron conservan veto, uso de la marca del observatorio, acceso preferente a datos ni cargos reservados. Pueden seguir colaborando a título personal, con las reglas del receptor.
5. **Anuncio público conjunto** de la transferencia, con el balance de lo hecho hasta entonces.

## Arquitectura

El observatorio tiene tres franjas que se leen en paralelo (peligro, respuesta del Estado y ejecución) sobre una capa territorial, más una capa de impacto que se activa en la temporada de lluvias.

*(Diagrama de arquitectura: 4 familias de fuentes, 1 revisión, 3 productos. Pendiente de redibujar en este repositorio.)*

La revisión humana es el único paso por el que pasa todo. Los tres productos salen del mismo registro verificado, así que una cifra corregida se corrige en todos a la vez.

## Fuentes, indicadores y reglas de medición

Cada indicador tiene una fuente primaria, una frecuencia de actualización y un responsable de rol.

| Franja | Indicador | Fuente primaria | Frecuencia |
| --- | --- | --- | --- |
| Peligro | Estado de alerta, magnitud y probabilidades por región Niño | [Comunicados ENFEN](https://enfen.imarpe.gob.pe/comunicados/) | Quincenal |
| Peligro | Anomalía observada (ICEN mensual) frente a lo pronosticado | Informes técnicos ENFEN | Mensual |
| Peligro | Avisos de lluvia y caudales por cuenca | SENAMHI | Diaria a semanal |
| Riesgo | Escenarios de riesgo: población, viviendas, salud, educación expuestas | CENEPRED (SIGRID), Visor INDECI | Por escenario |
| Respuesta | Decretos de emergencia, planes multisectoriales, transferencias | Diario Oficial El Peruano | Al publicarse |
| Respuesta | Plan de gestión del riesgo aprobado y grupo de trabajo activo, por gobierno regional (local, en la fase 2) | Normas regionales y municipales, portales de transparencia | Mensual |
| Ejecución | PIM, certificado, devengado del PP 0068 por pliego y nivel | MEF, Consulta Amigable | Semanal |
| Ejecución | Avance físico de obras de prevención | Invierte.pe, INFOBRAS | Mensual |
| Control | Informes de control concurrente | Contraloría General | Al publicarse |
| Impacto | Emergencias, damnificados, daños | INDECI (SINPAD, COEN) | Diaria en temporada |
| Impacto | Dengue y otras enfermedades sensibles al clima | CDC-MINSA | Semanal |

### Reglas de medición

**Métrica única de ejecución:** devengado sobre PIM del Programa Presupuestal 0068, por pliego y nivel de gobierno, con fecha de corte. En todos los niveles (regional, local y nacional) se reporta en dos partes, como las distingue la Consulta Amigable del MEF: **actividades** (gasto corriente: limpieza y descolmatación, bienes de ayuda humanitaria) y **proyectos de inversión** (defensas ribereñas, drenaje). Junto al porcentaje va el monto devengado en soles, porque el PIM cambia durante el año. Razón: al 13 de octubre, cerca del 82 % del PIM del programa está fuera del nivel regional, y sin esta separación no se puede saber si el aviso se convirtió en obras.

**Plan de respaldo (decidido el 14 de octubre).** Con los enlaces directos, las siete descargas toman minutos y la separación en todos los niveles deja de ser un riesgo de carga de trabajo. El respaldo queda para otro caso: si el MEF deja de responder por más de una semana, el seguimiento fino se concentra en regiones piloto, al detalle de cada municipalidad y proyecto, y se mantienen las descargas del nivel regional (D1 a D3) para las fichas de diciembre.

Límite declarado: el PP 0068 cubre todos los peligros (sismos, heladas, lluvias), no solo El Niño, y hay recursos para El Niño que llegan por otras vías. Es la mejor aproximación pública disponible, no una medida exacta del gasto en El Niño.

- **El gasto se reporta siempre con su eslabón.** "46,9 % de ejecución" no se publica solo; se publica "46,9 % devengado sobre el PIM del PP 0068 al 13 de octubre". Así se evita mezclar certificación con devengado.
- **Las cifras de ejecución que declaran autoridades o terceros con otra base se registran como hechos (quién dijo qué y cuándo), no como valores de la serie de ejecución.** En la página aparecen como eventos de la franja de respuesta, con su fuente.
- **Cada dato lleva fecha de corte** además de la fecha de publicación.
- **Las discrepancias no se resuelven especulando.** Hay dos casos. Si la prensa o un tercero da una cifra distinta a la de la fuente primaria, se publica la primaria con la nota "discrepancia por verificar". Si dos fuentes oficiales dan cifras distintas para lo mismo, se publican ambas y se explica la diferencia solo con lo que esté documentado (definición, cobertura, fecha de corte); si no hay explicación documentada, se dice así.
- **Las comparaciones entre territorios usan tasas,** no montos absolutos: devengado sobre PIM, población expuesta sobre población total.

## Flujo de trabajo, automatización y verificación

El observatorio publica en dos ritmos: un corte quincenal atado a cada comunicado del ENFEN y un corte semanal de ejecución presupuestal. Ninguna cifra pasa a la página pública sin dos revisiones humanas.

### Ciclo de cada corte

1. **Captura.** Una tarea programada revisa las fuentes en sus fechas conocidas (el próximo comunicado ENFEN es el 15 de octubre). Una herramienta de IA lee el documento y extrae los campos definidos en un registro estructurado.
2. **Extracción.** La herramienta llena el registro: fecha, estado, magnitudes, probabilidades, territorios mencionados, y una frase en lenguaje simple. Cada campo guarda la cita de la página de origen.
3. **Primera revisión.** El analista de la franja compara el registro con el documento original y corrige.
4. **Segunda revisión.** El comité editorial aprueba o devuelve.
5. **Publicación.** Se actualiza la página pública y se anota en la bitácora de cambios.
6. **Difusión.** Comunicación prepara la pieza corta para redes a partir de lo ya aprobado, sin agregar cifras.

### Lo que hace la IA y lo que no

| Hace | No hace |
| --- | --- |
| Lee comunicados, decretos e informes y extrae datos con su cita | Decidir qué se publica |
| Redacta resúmenes en lenguaje simple como borrador | Calificar a autoridades o atribuir intenciones |
| Calcula tasas y detecta discrepancias entre fuentes | Firmar o hablar en nombre del observatorio |
| Mantiene la página y el registro de datos | Guardar datos personales de voluntarios en el registro del observatorio |

### Limitaciones técnicas conocidas

- **Consulta Amigable del MEF:** cada consulta tiene un enlace de exportación fijo y público (verificado el 14 de octubre). La descarga semanal es automática, los lunes a las 8:00; si el MEF no responde, una persona la hace a mano con los mismos enlaces, siguiendo la Guía de descarga. Los archivos se guardan sin modificar, con su huella digital.
- **Algunas fuentes publican en PDF escaneado o como imagen.** Requieren lectura asistida y una revisión más cuidadosa.
- **Los portales de transparencia municipales** son irregulares. El seguimiento de planes municipales depende de monitores territoriales, previstos para la fase 2.

## Operación: acceso y flujo de datos

El observatorio no vive en la cuenta de ninguna persona. Todo se opera con herramientas estándar a nombre de Qhawana, para que pueda transferirse tal cual.

### Dónde vive cada cosa

- **Repositorio en GitHub (organización Qhawana):** archivos originales descargados, datos procesados en CSV con fecha de corte, código, metodología y bitácora de cambios. Todo cambio queda registrado con autor, fecha y aprobación.
- **Sitio público:** se genera desde el repositorio y se actualiza solo cuando el comité aprueba un corte.
- **Tablero de tareas:** cada tarea con responsable y plazo, en el mismo repositorio.
- **Cuentas raíz:** dos administradores, verificación en dos pasos obligatoria y compromiso escrito de transferir las cuentas al receptor del observatorio.

### Acceso por rol

| Rol | Ve | Carga | Aprueba |
| --- | --- | --- | --- |
| Público | Sitio y datos abiertos | — | — |
| Analista | Todo el material interno | Archivos originales y registros de hechos | No |
| Comité editorial | Todo | Comentarios | Sí; nada se publica sin su aprobación |
| Gestor(a) de datos | Todo | Todo | Solo cambios técnicos, nunca cifras |
| Coordinación | Todo | Tareas | No |

Incorporación: acuerdo de colaborador (licencia abierta de lo que aporta y declaración de conflictos de interés), verificación en dos pasos y una primera tarea acompañada. Al dejar un rol, el acceso se retira esa misma semana.

### Flujo de cada dato

1. **Carga.** El analista sube desde el navegador los archivos del MEF con el nombre que fija la guía. Los hechos que no son cifras del MEF (decretos, informes de control, comunicados) se registran en un formulario con fecha, tipo, enlace a la fuente primaria y cita textual; sin fuente primaria no se puede enviar.
2. **Validación automática.** Un programa lee los archivos, corre los seis controles de la Guía de descarga y responde con un resumen: si pasó, y qué cifras cambiaron frente al corte anterior.
3. **Aprobación.** Un miembro del comité que no preparó el dato revisa el resumen y aprueba. Sin esa aprobación el cambio no se publica; la herramienta lo impide.
4. **Publicación.** Al aprobarse, el sitio y los datos abiertos se actualizan con su fecha de corte y una línea en la bitácora.

La IA puede leer documentos y proponer registros con su cita; nunca aprueba ni publica. Nadie del equipo necesita saber programar: cargar es arrastrar archivos o llenar un formulario, y aprobar es un botón.

## Roles del equipo

La fase 1 necesita 10 personas en siete roles, seleccionadas por convocatoria abierta. Mientras tanto opera un núcleo transitorio (ver Gobernanza).

| Rol | Qué hace | Perfil buscado | Personas | Horas por semana |
| --- | --- | --- | --- | --- |
| Coordinador(a) general | Conduce la agenda, los plazos y el ciclo de cortes. No aprueba publicaciones por sí solo(a). | Gestión de proyectos, experiencia en sector público | 1 | 4 a 6 |
| Miembro del comité editorial | Aprueba cada publicación, resuelve discrepancias, ordena correcciones y responde apelaciones. | Criterio técnico y reputación de independencia; al menos uno de los tres, externo a Qhawana | 3 | 2 a 3 |
| Analista de finanzas públicas | Hace las descargas semanales del MEF según la guía, procesa el PP 0068 y aplica la cadena de medición del gasto. | Economía, contabilidad o gestión pública; manejo de SIAF y Consulta Amigable | 2 | 3 a 4 |
| Analista de peligro y riesgo | Revisa los resúmenes de ENFEN, SENAMHI y CENEPRED y vincula el pronóstico con el territorio expuesto. | Geografía, ingeniería civil o hidráulica, meteorología, gestión del riesgo | 1 | 3 a 4 |
| Gestor(a) de datos y herramientas digitales | Mantiene el registro, las tareas programadas y la página; opera las herramientas de IA y revisa sus resultados técnicos. | Datos, programación básica o análisis | 1 | 3 a 5 |
| Editor(a) de comunicación y lenguaje claro | Convierte lo aprobado en piezas cortas y mantiene el glosario. | Periodismo, comunicación o divulgación | 1 | 2 a 3 |
| Asesor(a) legal y de ética de datos | Revisa privacidad, riesgo de difamación, conflictos de interés y licencias, por consulta puntual. | Derecho, de preferencia administrativo o protección de datos | 1 | 1 |
| **Total** |  |  | **10** |  |

En la fase 2 se agregan monitores territoriales (uno por región priorizada), un(a) responsable de alianzas y un(a) analista de salud para la vigilancia de dengue y de establecimientos expuestos.

### Reglas de rol

- **Cuatro ojos.** Lo que prepara un analista lo aprueba un miembro del comité editorial que no lo preparó. El control de calidad entre analistas que pide la Guía de descarga es un paso previo y no reemplaza esta aprobación.
- **Conflicto de interés declarado.** Quien sea candidato, funcionario o contratista de un gobierno observado se abstiene en ese territorio.
- **Rotación.** El comité editorial rota un integrante cada seis meses.
- **Salida ordenada.** Quien deja un rol entrega sus registros y accesos en la semana de su salida.

## Gobernanza, riesgos y reglas de publicación

**Independencia.** El observatorio es parte de Qhawana, una iniciativa ciudadana. Su independencia se sostiene en el método y no en declaraciones: fuentes oficiales enlazadas, las mismas reglas para todos los gobiernos, un comité editorial con al menos un integrante externo y metodología abierta.

**Núcleo transitorio.** Hasta el 22 de noviembre opera un núcleo de dos o tres personas, declarado como transitorio. Prepara la metodología y los datos, publica la convocatoria, conduce la selección y entrega sus funciones al equipo seleccionado. No publica cifras ni hallazgos hacia afuera.

### Reglas de publicación

- Todo hallazgo sobre un gobierno se publica con la misma ficha que se usa para los gobiernos comparables.
- Antes de publicar un hallazgo negativo sobre una entidad, se revisa su portal y su respuesta pública más reciente.
- No se reutilizan documentos de otras iniciativas sin la atribución que su licencia exija.

### Riesgos y respuesta

| Riesgo | Señal temprana | Respuesta |
| --- | --- | --- |
| Se lee como herramienta de oposición | Solo se publican hallazgos negativos de un mismo color político | Fichas iguales para todos; publicar también lo que funciona |
| Cifra equivocada publicada | Reclamo de una entidad o un periodista | Corrección pública en 48 horas; revisar el paso del ciclo que falló |
| Error de extracción de la IA | Discrepancia entre registro y documento | Cuatro ojos obligatorio; cita textual de origen en cada campo |
| Reclamo por difamación | Mención de personas o adjetivos sobre funcionarios | Solo hechos institucionales; revisión de ética y legal |
| Abandono de voluntarios | Cortes que se atrasan | Roles pequeños y acotados; suplente por rol |
| Cambio de autoridades el 1 de enero de 2027 | Transferencias de gestión sin el tema de El Niño | Ficha por gobierno regional para las comisiones de transferencia, publicada en diciembre |
| Fuente que deja de publicar | Portal caído o sin actualizar | Registrar la falta como dato; usar fuente alternativa marcada |

## Hoja de ruta y convocatoria

Las fichas de transferencia (8 al 22 de diciembre) son el único hito atado a una fecha externa: el cambio de autoridades del 1 de enero de 2027. El calendario se corrió una semana el 14 de octubre; ese hito ya no tiene margen para otro retraso.

### Hoja de ruta

1. **13 al 26 de octubre.** Preparación a cargo del núcleo transitorio: cuentas de Qhawana y repositorio en marcha, metodología cerrada, corte del comunicado ENFEN del jueves 15 y primera descarga automática del MEF el lunes 26.
2. **26 de octubre al 8 de noviembre.** Convocatoria abierta, con difusión en universidades, colegios profesionales y redes de gestión pública.
3. **9 al 15 de noviembre.** Filtro y entrevistas.
4. **16 al 22 de noviembre.** Incorporación del equipo. El comité editorial se instala y aprueba la metodología y el primer conjunto de datos.
5. **23 de noviembre al 7 de diciembre.** Piloto en Tumbes y Piura, a nivel de gobierno regional.
6. **8 al 22 de diciembre.** Fichas de los 25 gobiernos regionales y de la Municipalidad Metropolitana de Lima para las comisiones de transferencia de gestión.
7. **Enero a marzo de 2027.** Seguimiento durante el pico, con los mismos dos ritmos de corte.
8. **Abril a junio de 2027.** Balance público: aviso disponible frente a acción tomada, y pronóstico frente a lo ocurrido.

### Texto de la convocatoria

> **Convocatoria: Observatorio El Niño**
>
> Desde febrero de 2026 el ENFEN mantiene la alerta por El Niño Costero, y desde agosto pronostica que será extraordinario. Hubo cerca de diez meses de aviso antes del pico esperado. Queremos saber, con datos públicos, qué hizo cada gobierno con ese aviso.
>
> Buscamos un equipo pequeño y riguroso de 10 personas: coordinación, finanzas públicas (manejo de SIAF o Consulta Amigable), riesgo de desastres, datos, comunicación, derecho y un comité editorial. Es voluntariado, sin pago: entre 1 y 6 horas por semana, a distancia, de noviembre de 2026 a junio de 2027.
>
> Trabajamos con inteligencia artificial y herramientas digitales para leer documentos oficiales y extraer datos. Las personas verificamos y decidimos qué se publica.
>
> Todo lo que produzcamos será abierto y está pensado para donarse a la academia o a la sociedad civil.
>
> Reglas: toda cifra con fuente, las mismas reglas para todos los gobiernos, nada se publica por decisión de una sola persona, y quien tenga conflicto de interés en un territorio se abstiene en él.
>
> Para postular, escribe a [CORREO DE CONTACTO] indicando qué rol te interesa y tu experiencia relevante. Cierre: domingo 8 de noviembre.

### Selección

Del 9 al 15 de noviembre, el núcleo transitorio y una persona externa revisan las postulaciones con los perfiles de la tabla de roles y entrevistan a quienes pasen el filtro. Se prioriza experiencia verificable. Los roles asignados se comunican dentro del equipo, cada uno con su suplente.
