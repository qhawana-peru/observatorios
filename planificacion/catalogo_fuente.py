"""Fuente única del catálogo del Museo de la planificación (Qhawana).

Genera los CSV abiertos en catalogo/. Cada dato tiene enlace oficial y fecha de consulta.
Licencia de los datos: CC BY 4.0. Fecha de consulta de esta versión: 16/11/2026.
"""
import csv, os

CONSULTA = "2026-11-16"
OUT = os.path.join(os.path.dirname(__file__), "catalogo")

# id, sala, sector, tipo, corto, nombre, actores, norma, ini, fin, catalogado, resumen
PLANES = [
    ("an", "principal", "", "Políticas de Estado", "Acuerdo Nacional", "Acuerdo Nacional: 35 Políticas de Estado",
     "Foro del Acuerdo Nacional (partidos, organizaciones sociales y Gobierno)", "Suscrito el 22/07/2002", 2002, "", "si",
     "35 políticas de Estado agrupadas en cuatro ejes temáticos. Orientan el accionar del Estado en el largo plazo."),
    ("vision", "principal", "", "Visión de país", "Visión al 2050", "Visión del Perú al 2050",
     "Foro del Acuerdo Nacional (consenso) · CEPLAN (formulación)", "Acta de la sesión 126 del Foro del Acuerdo Nacional", 2019, 2050, "si",
     "Cinco ejes estratégicos. Es la base del PEDN al 2050."),
    ("pedn", "principal", "", "Plan de desarrollo nacional", "PEDN al 2050", "Plan Estratégico de Desarrollo Nacional al 2050",
     "CEPLAN (formula) · PCM y Consejo de Ministros (aprueban)", "DS 095-2022-PCM · actualizado por DS 103-2023-PCM", 2022, 2050, "si",
     "Cuatro objetivos nacionales. Todas las entidades del Sinaplan deben articular sus planes a sus objetivos y acciones estratégicas."),
    ("pgg", "principal", "", "Política General de Gobierno", "PGG 2026-2031", "Política General de Gobierno 2026-2031",
     "Presidencia de la República · Consejo de Ministros · PCM", "DS 127-2026-PCM", 2026, 2031, "si",
     "Cinco ejes y 30 lineamientos. La norma no fija metas, indicadores ni plazos; encarga a los ministerios las medidas para cumplirla y a las entidades del Sinaplan incorporarlas en sus planes."),
    # Sala nacional — sector Salud (primer sector completo)
    ("pnms", "sectorial", "MINSA", "Política nacional multisectorial", "PNMS al 2030", "Política Nacional Multisectorial de Salud al 2030 \"Perú, País Saludable\"",
     "Ministerio de Salud (rector) y sectores corresponsables", "DS 026-2020-SA", 2020, 2030, "si",
     "Política multisectorial bajo rectoría del MINSA. Tres objetivos prioritarios orientados a reducir los años de vida perdidos por causas evitables."),
    ("pem-pnms", "sectorial", "MINSA", "Plan estratégico multisectorial", "PEM de la PNMS", "Plan Estratégico Multisectorial de la Política Nacional Multisectorial de Salud al 2030",
     "Ministerio de Salud y sectores corresponsables", "DS 016-2021-SA", 2021, 2030, "si",
     "Plan para implementar la PNMS al 2030."),
    ("pesem-salud", "sectorial", "MINSA", "PESEM", "PESEM Salud", "Plan Estratégico Sectorial Multianual del Sector Salud",
     "Ministerio de Salud · Comisión Sectorial de Planeamiento Estratégico", "RM 1174-2023/MINSA (2024-2030)", 2024, 2030, "si",
     "Plan del sector Salud articulado al PEDN al 2050. Reemplaza al PESEM 2016-2021, que se había ampliado al 2025."),
    # Sala institucional
    ("pei-minsa", "sectorial", "MINSA", "PEI", "PEI MINSA", "Plan Estratégico Institucional del Ministerio de Salud",
     "Ministerio de Salud (pliego 011)", "PEI 2025-2030 · norma de aprobación por confirmar", 2025, 2030, "si",
     "Plan institucional del pliego MINSA, alineado con el PESEM del sector y la PNMS."),
]
REGIONES = ["Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica",
            "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima (región)", "Loreto", "Madre de Dios", "Moquegua",
            "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali", "Lima Metropolitana"]
EP = "https://busquedas.elperuano.pe/dispositivo/NL/"
EXONERA = "https://www.gob.pe/institucion/ceplan/normas-legales/8301534-043-2026-ceplan-pcd"
# region: (nombre del plan, norma, inicio, fin, enlace, [(fecha, descripcion, norma, url, vigente)], [(tipo, texto)], [reportes extra])
REG = {
    "Amazonas": ("PDRC del departamento de Amazonas 2026-2040", "Ordenanza regional publicada en El Peruano (número por confirmar)", 2026, 2040, EP + "2528461-1",
                 [("2022-10-29", "PDRC de la Región Amazonas hasta 2025", "OR 009-2022-GRA/CR", "https://cdn.www.gob.pe/uploads/document/file/4432375/Acuerdo%20de%20Consejo%20032-2023%20CR.pdf", "no"),
                  ("2026", "PDRC 2026-2040, con informe técnico de CEPLAN de abril de 2026", "", EP + "2528461-1", "si")], [], []),
    "Áncash": ("PDRC de Áncash 2024-2034", "Ordenanza regional publicada el 21/11/2024 (número por confirmar)", 2024, 2034, EP + "2346253-1", [("2024-11-21", "Publicación en El Peruano", "", EP + "2346253-1", "si")], [], []),
    "Apurímac": ("PDRC Apurímac al 2033", "OR 014-2022-GR-APURÍMAC/CR", 2022, 2033, "https://cdn.www.gob.pe/uploads/document/file/7252657/6086531-plan-de-desarrollo-regional-concertado-pdrc-apurimac-al-2033.pdf", [], [], []),
    "Arequipa": ("PDRC 2026-2035 del departamento de Arequipa", "OR 549-AREQUIPA", 2026, 2035, EP + "2499935-1", [], [], []),
    "Ayacucho": ("PDRC de Ayacucho 2016-2027 (ampliado)", "Norma de ampliación por confirmar", 2016, 2027, "https://cdn.www.gob.pe/uploads/document/file/8078795/6777471-i-audiencia-publica-2025.pdf", [],
                 [("observacion", "Plan formulado para 2016-2021 y ampliado hasta 2027. Lo cita el propio gobierno regional en su audiencia pública de 2025; falta ubicar la ordenanza de ampliación.")], []),
    "Cajamarca": ("PDRC Cajamarca al 2033", "OR D4-2023-GR.CAJ/CR (02/06/2023)", 2023, 2033, EP + "2203132-1", [("2023-08-10", "Publicación en El Peruano", "OR D4-2023-GR.CAJ/CR", EP + "2203132-1", "si")],
                  [("discrepancia", "El informe de evaluación de octubre de 2025 se titula \"PDRC al 2030\", aunque el plan aprobado es al 2033; también usa dos enunciados distintos para los objetivos 11 y 12.")],
                  [("2023–2024", "Informe de evaluación del PDRC, periodos 2023-2024 (octubre 2025)", "ubicado", "2025-10", "https://www.regioncajamarca.gob.pe/media/portal/KJDIG/documento/85882/EVALUACI%C3%93N_PDRC_VB_1.pdf?r=1768840168", "Índice de gestión del PDRC 2024: 55,65 %.")]),
    "Callao": ("PDRC 2025-2034 de la Provincia Constitucional del Callao", "OR 007-2024 (Gobierno Regional del Callao)", 2025, 2034, "https://www.gob.pe/institucion/regioncallao/colecciones/10147-ordenanzas-del-consejo-regional",
               [("2022-10-25", "Ampliación del PDRC 2011-2021 hasta 2025", "OR 009-2022", "https://www.gob.pe/institucion/regioncallao/colecciones/10147-ordenanzas-del-consejo-regional", "no"),
                ("2023-05-19", "Ampliación hasta 2027", "OR 002-2023", "https://hndac.gob.pe/wp-content/uploads/PLAN-DE-DESARROLLO-REGIONAL-CONCERTADO-ACTUALIZADO.pdf", "no"),
                ("2024-09-16", "PDRC 2025-2034", "OR 007-2024", EP + "2531967-1", "si")],
               [("discrepancia", "Dos fuentes oficiales dan fechas distintas para la OR 007-2024: el portal gob.pe del Gobierno Regional la lista con fecha 20/06/2024; una ordenanza regional de 2026 y la audiencia pública de 2025 la citan con fecha 16/09/2024. No hay explicación documentada.")], []),
    "Cusco": ("PDRC del Cusco al 2033", "OR 239-2023-CR/GR CUSCO", 2023, 2033, "https://sinia.minam.gob.pe/normas/plan-desarrollo-regional-concertado-cusco-2033", [("2023-12-01", "Publicación", "OR 239-2023-CR/GR CUSCO", "https://sinia.minam.gob.pe/normas/plan-desarrollo-regional-concertado-cusco-2033", "si")], [], []),
    "Huancavelica": ("PDRC Huancavelica al 2034", "OR 558-GOB.REG-HVCA/CR (19/02/2026)", 2026, 2034, EP + "2493850-1", [], [], []),
    "Huánuco": ("PDRC Huánuco al 2033", "OR 086-2022-GRH-CR", 2022, 2033, EP + "2194295-1", [("2022-11-17", "Publicación en El Peruano", "OR 086-2022-GRH-CR", EP + "2194295-1", "si")], [], []),
    "Ica": ("PDRC de Ica 2016-2027 (ampliado)", "Ordenanza regional de ampliación de 2023 (número por confirmar)", 2016, 2027, "https://juventud.gob.pe/normativa-joven-pdf/1/166.pdf",
            [("2022", "Ampliación del PDRC 2016-2021 hasta 2025", "OR 003-2022-GORE-ICA", "https://juventud.gob.pe/normativa-joven-pdf/1/166.pdf", "no"),
             ("2023", "Ampliación hasta 2027", "", "https://juventud.gob.pe/normativa-joven-pdf/1/166.pdf", "si")], [], []),
    "Junín": ("PDRC Junín al 2040", "Norma de aprobación por confirmar", "", 2040, "https://www.regionjunin.gob.pe/descargar.php/archivo/GRJ-144520bc36a5e4c2680040d8df6ac7b22f31ea.pdf/", [],
              [("observacion", "El Gobierno Regional cita el PDRC Junín al 2040 en sus documentos; falta ubicar la ordenanza que lo aprueba.")], []),
    "La Libertad": ("PDRC La Libertad 2023-2033", "OR 000007-2023-GRLL/CR (03/08/2023)", 2023, 2033, "https://juventud.gob.pe/normativa-joven-pdf/1/105.pdf", [("2023-09-21", "Publicación en El Peruano", "OR 000007-2023-GRLL/CR", "https://juventud.gob.pe/normativa-joven-pdf/1/105.pdf", "si")], [], []),
    "Lambayeque": ("PDRC 2026-2040 del departamento de Lambayeque", "OR 000003-2026-GR.LAMB/CR (12/03/2026)", 2026, 2040, EP + "2502009-1", [], [], []),
    "Lima (región)": ("PDRC 2025-2040 de la Región Lima", "Ordenanza regional (número por confirmar)", 2025, 2040, "https://www.gob.pe/institucion/regionlima/normas-legales/tipos/40-ordenanza-regional", [], [], []),
    "Loreto": ("PDRC Loreto al 2021, ampliado al 2027", "OR 014-2015-GRL-CR; ampliación al 2027 por confirmar", 2015, 2027, "https://cdn.www.gob.pe/uploads/document/file/4631031/ACR%20N048.pdf",
               [("2015-10-29", "PDRC Loreto al 2021", "OR 014-2015-GRL-CR", "https://aplicaciones02.regionloreto.gob.pe/sites/default/files/normativa_regional/ordenanza_regional_no_014-2015.pdf", "no"),
                ("2023", "Ampliación del horizonte al 2027 (acuerdo del Consejo Regional)", "", "https://cdn.www.gob.pe/uploads/document/file/4631031/ACR%20N048.pdf", "si")], [], []),
    "Madre de Dios": ("Plan de Desarrollo Concertado 2007-2021 de Madre de Dios", "OR 019-2007-GRMDD/CR", 2007, 2021, "https://cdn.www.gob.pe/uploads/document/file/2286531/APROBADO%20MEDIANTE%20ORDENANZA%20REGIONAL%20N%C2%B0%20018-2007-CR/GRMDD.pdf", [],
                      [("observacion", "Es el último PDRC que ubicamos. No encontramos una ampliación ni un plan nuevo al 16/11/2026; puede existir y cualquiera puede aportar el enlace.")], []),
    "Moquegua": ("PDRC Moquegua al 2032", "Norma de aprobación por confirmar", "", 2032, "https://www.gob.pe/institucion/regionmoquegua/informes-publicaciones/tipos/27", [], [], []),
    "Pasco": ("PDRC de Pasco 2025-2034", "Norma de aprobación por confirmar", 2025, 2034, "https://intranet.mesadeconcertacion.org.pe/storage/documentos/2025-12-22/recomendaciones-dialogo-regional-pdcr-al-2034.pdf", [],
              [("observacion", "La aprobación la reportan la Mesa de Concertación y un documento del Congreso; falta ubicar la ordenanza regional.")], []),
    "Piura": ("PDRC de Piura 2025-2034", "OR 527-2025/GRP-CR (25/08/2025)", 2025, 2034, EP + "2431989-1",
              [("2017-02-27", "PDRC Piura hacia el 2021", "OR 381-2017/GRP-CR", "https://sni.org.pe/ordenanza-que-aprueba-el-plan-de-desarrollo-regional-concertado-piura-hacia-el-2021/", "no"),
               ("2023-09-27", "Ampliación del horizonte al 2027 (derogada en 2025)", "OR 488-2023/GRP-CR", "https://juventud.gob.pe/normativa-joven-pdf/1/107.pdf", "no"),
               ("2025-08-29", "PDRC 2025-2034, publicado en El Peruano", "OR 527-2025/GRP-CR", EP + "2431989-1", "si")],
              [("observacion", "El plan 2025-2034 derogó la ampliación al 2027. La versión 5 del museo mostraba a Piura con el plan antiguo ampliado; quedó corregido el 16/11/2026."),
               ("observacion", "El documento completo está en la plataforma gob.pe, pero no pudimos abrirlo con nuestras herramientas: sus objetivos e indicadores están por catalogar.")],
              [("2023", "Informe de evaluación del PDRC 2016-2027, año 2023 (31/10/2024)", "ubicado", "2024-10", "https://www.gob.pe/institucion/regionpiura/informes-publicaciones/6141428-informe-de-evaluacion-pdrc-2016-2027-ano-2023", "Corresponde al plan anterior.")]),
    "Puno": ("PDRC Puno al 2034", "OR 000014-2025-GRP/GR PUNO", 2025, 2034, "https://www.regionpuno.gob.pe/wp-content/uploads/2025/08/0000939382_ORDENANZA-REGIONAL_000014_GR-PUNOFA.pdf",
             [("2025-09-03", "Publicación en El Peruano", "OR 000014-2025-GRP/GR PUNO", EP + "2433656-1", "si")],
             [("observacion", "No pudimos abrir el documento completo del plan: la página del PDRC en el portal del Gobierno Regional no respondía al 16/11/2026. Sus objetivos e indicadores están por catalogar.")], []),
    "San Martín": ("PDRC San Martín al 2040", "Norma de aprobación por confirmar", "", 2040, "https://www.eeas.europa.eu/delegations/per%C3%BA/san-mart%C3%ADn-proyecta-su-futuro-sostenible-con-apoyo-de-la-uni%C3%B3n-europea_es",
                   [("2018-11-19", "PDRC San Martín al 2030", "OR 030-2018-GRSM/CR", "https://cdn.www.gob.pe/uploads/document/file/6166933/5440483-resolucion-n-055-2024-grsm-gtbm-t.pdf", "no"),
                    ("2026", "PDRC al 2040, citado en una ordenanza regional de junio de 2026", "", EP + "2535749-1", "si")],
                   [("observacion", "Documentos oficiales recientes citan dos planes: el PDRC al 2030 (OR 030-2018-GRSM/CR) y el PDRC al 2040. Falta ubicar la ordenanza que aprueba el plan al 2040.")],
                   [("2022–2023", "Informe de evaluación del PDRC al 2030, periodos 2022-2023 (oct 2024)", "ubicado", "2024-10", "https://cdn.www.gob.pe/uploads/document/file/7305243/6241603-anexo-rer-307.pdf", "")]),
    "Tacna": ("PDRC Tacna al 2034", "OR 001-2024-CR/GOB.REG.TACNA", 2024, 2034, "https://juventud.gob.pe/normativa-joven-pdf/1/287.pdf", [("2024-02-23", "Publicación en El Peruano", "OR 001-2024-CR/GOB.REG.TACNA", "https://juventud.gob.pe/normativa-joven-pdf/1/287.pdf", "si")], [], []),
    "Tumbes": ("PDRC Tumbes al 2034", "OR 005-2025/GOB.REG.TUMBES-CR", 2025, 2034, EP + "2495039-1", [], [], []),
    "Ucayali": ("PDRC del departamento de Ucayali 2023-2033", "OR 001-2023-GRU-CR", 2023, 2033, "https://sinia.minam.gob.pe/normas/aprobacion-plan-desarrollo-regional-concertado-departamento-ucayali-2023", [], [], []),
    "Lima Metropolitana": ("Plan Regional de Desarrollo Concertado de Lima 2012-2025", "Municipalidad Metropolitana de Lima (norma por confirmar)", 2012, 2025, "https://sinia.minam.gob.pe/documentos/plan-regional-desarrollo-concertado-lima-2012-2025", [],
                           [("observacion", "Es el último plan regional concertado de Lima Metropolitana que ubicamos. El PLANMET 2040 (Ordenanza 2499-2022) es un plan de desarrollo urbano, no un plan de desarrollo concertado. Puede existir uno vigente: cualquiera puede aportar el enlace.")], []),
}
REP_REG, VER_REG, NOTA_REG, FUENTE_REG = [], [], [], []
for i, r in enumerate(REGIONES):
    pid = f"pdrc-{i:02d}"
    nom, norma, ini, fin, url, vers, notas, reps = REG[r]
    PLANES.append((pid, "territorial", r, "PDRC", r, nom,
                   "Municipalidad Metropolitana de Lima" if r == "Lima Metropolitana" else f"Gobierno Regional de {r}",
                   norma, ini, fin, "si", f"Plan de desarrollo concertado vigente o último ubicado para {r}, según fuentes oficiales consultadas el 16/11/2026."))
    VER_REG.extend((pid,) + v for v in vers)
    NOTA_REG.extend((pid,) + n for n in notas)
    FUENTE_REG.append((pid, nom, url))
    REP_REG.extend((pid,) + x for x in reps)
    REP_REG.append((pid, "2025", "Evaluación del PDRC correspondiente a 2025: CEPLAN exoneró por única vez (RPCD 043-2026/CEPLAN/PCD)", "noexigido", "", EXONERA, ""))

# Nivel dentro de su eje. Principal: 0. Sectorial: 1 políticas y PEM, 2 PESEM, 3 PEI/POI.
# Territorial: 1 PDRC, 2 PDLC provincial, 3 PDLC distrital, 4 PEI/POI subnacional.
NIVEL = {"an": 0, "vision": 0, "pedn": 0, "pgg": 0, "pnms": 1, "pem-pnms": 1, "pesem-salud": 2, "pei-minsa": 3}

# Los 19 sectores del Poder Ejecutivo (18 ministerios y la PCM). Orden pensado para el diagrama de arcos.
SECTORES = [
    ("PCM", "PCM", "Presidencia del Consejo de Ministros"), ("RREE", "RR. EE.", "Relaciones Exteriores"),
    ("MEF", "MEF", "Economía y Finanzas"), ("MINDEF", "Mindef", "Defensa"), ("MININTER", "Mininter", "Interior"),
    ("MINJUSDH", "Minjusdh", "Justicia y Derechos Humanos"), ("MINEDU", "Minedu", "Educación"), ("MINCUL", "Cultura", "Cultura"),
    ("MIDIS", "Midis", "Desarrollo e Inclusión Social"), ("MINSA", "Minsa", "Salud"), ("MIMP", "MIMP", "Mujer y Poblaciones Vulnerables"),
    ("MTPE", "MTPE", "Trabajo y Promoción del Empleo"), ("MVCS", "Vivienda", "Vivienda, Construcción y Saneamiento"),
    ("MTC", "MTC", "Transportes y Comunicaciones"), ("MINAM", "Minam", "Ambiente"), ("MIDAGRI", "Midagri", "Desarrollo Agrario y Riego"),
    ("PRODUCE", "Produce", "Producción"), ("MINEM", "Minem", "Energía y Minas"), ("MINCETUR", "Mincetur", "Comercio Exterior y Turismo"),
]
PNMS_TXT = "https://observateperu.ins.gob.pe/sites/default/files/2024-10/Pol%C3%ADtica%20Nacional%20Multisectorial%20de%20Salud%20al%202030%20.pdf"
# plan_id, sector, rol, evidencia. Rol según la tabla de sectores involucrados de la PNMS.
MULTISECTORIAL = [("pnms", "MINSA", "Rector", PNMS_TXT)] + [("pnms", c, rol, PNMS_TXT) for c, rol in [
    ("MINEDU", "Hábitos y estilos de vida en el curso de vida"), ("MVCS", "Agua segura y alcantarillado"),
    ("MIMP", "Reducción de la violencia familiar"), ("MIDIS", "Asistencia alimentaria y acceso a servicios del Estado"),
    ("MINAM", "Vigilancia y control de la contaminación ambiental"), ("MTC", "Seguridad vial y prevención de accidentes"),
    ("MIDAGRI", "Inocuidad y seguridad alimentaria"), ("MINJUSDH", "Salud en penales y centros juveniles"),
    ("MTPE", "Seguridad y salud en el trabajo"), ("MININTER", "Salud en sus establecimientos y seguridad ciudadana"),
    ("MINDEF", "Salud en sus establecimientos y gestión del riesgo de desastres"), ("MINCUL", "Pertinencia cultural en las políticas")]]

# plan_id, fecha, descripcion, norma, url, vigente
VERSIONES = [
    ("an", "2002-07-22", "Suscripción del Acuerdo Nacional", "", "", "si"),
    ("vision", "2019-04-29", "Aprobación por consenso en la sesión 126 del Foro del Acuerdo Nacional", "Acta 126", "https://acuerdonacional.pe/wp-content/uploads/2023/03/Acta-126-Vision-del-Peru-al-2050.pdf", "si"),
    ("pedn", "2022-07-28", "Aprobación", "DS 095-2022-PCM", "https://busquedas.elperuano.pe/dispositivo/NL/2090829-7", "no"),
    ("pedn", "2023-09-14", "Actualización", "DS 103-2023-PCM", "https://busquedas.elperuano.pe/dispositivo/NL/2215042-3/", "si"),
    ("pedn", "2026-07-14", "Modificación de 26 fichas técnicas de indicadores", "RPCD 046-2026/CEPLAN/PCD", "https://busquedas.elperuano.pe/dispositivo/NL/2534766-1", ""),
    ("pgg", "2025-12-20", "PGG anterior 2025-2026 (hasta julio de 2026)", "DS 141-2025-PCM", "https://www.gob.pe/institucion/pcm/noticias/1317002-ejecutivo-aprueba-la-politica-general-de-gobierno-2025-2026", "no"),
    ("pgg", "2026-09-05", "Publicación de la PGG 2026-2031 (aprobada en Consejo de Ministros el 04/09/2026)", "DS 127-2026-PCM", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3", "si"),
    ("pnms", "2020", "Aprobación", "DS 026-2020-SA", "https://observateperu.ins.gob.pe/sites/default/files/2024-10/Pol%C3%ADtica%20Nacional%20Multisectorial%20de%20Salud%20al%202030%20.pdf", "si"),
    ("pem-pnms", "2021-06-27", "Aprobación (separata especial de El Peruano)", "DS 016-2021-SA", "https://vlex.com.pe/vid/869835364", "si"),
    ("pesem-salud", "2016-06-02", "PESEM 2016-2021", "RM 367-2016/MINSA", "https://www.minsa.gob.pe/transparencia/index.asp?op=1001", "no"),
    ("pesem-salud", "2022", "Ampliación del horizonte del PESEM 2016-2021 al año 2025", "RM 364-2022-MINSA", "https://www.gob.pe/institucion/minsa/normas-legales/3002475-364-2022-minsa", "no"),
    ("pesem-salud", "2024-01-03", "PESEM 2024-2030 (fecha de publicación en el portal del MINSA)", "RM 1174-2023/MINSA", "https://www.minsa.gob.pe/transparencia/index.asp?op=1001", "si"),
    ("pei-minsa", "2024", "PEI 2019-2027 ampliado", "RM 172-2024-MINSA", "https://cdn.www.gob.pe/uploads/document/file/6594276/5734282-resolucion-ministerial-n-172-2024-minsa.pdf", "no"),
    ("pei-minsa", "2025", "PEI 2025-2030", "Por confirmar", "https://cdn.www.gob.pe/uploads/document/file/7566687/6425886-plan-estrategico-institucional-2025-2030-del-ministerio-de-salud.pdf", "si"),
]

# plan_id, plan_superior, base (declarada|norma), evidencia
ARTICULACION = [
    ("vision", "an", "declarada", "https://acuerdonacional.pe/wp-content/uploads/2023/03/Acta-126-Vision-del-Peru-al-2050.pdf"),
    ("pedn", "an", "declarada", "https://busquedas.elperuano.pe/dispositivo/NL/2090829-7"),
    ("pedn", "vision", "declarada", "https://busquedas.elperuano.pe/dispositivo/NL/2090829-7"),
    ("pgg", "an", "declarada", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3"),
    ("pgg", "pedn", "declarada", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3"),
    ("pnms", "pedn", "norma", ""),
    ("pem-pnms", "pnms", "declarada", "https://vlex.com.pe/vid/869835364"),
    ("pesem-salud", "pedn", "declarada", "https://juventud.gob.pe/normativa-joven-pdf/3/105.pdf"),
    ("pesem-salud", "pnms", "norma", ""),
    ("pei-minsa", "pesem-salud", "declarada", "https://cdn.www.gob.pe/uploads/document/file/7566687/6425886-plan-estrategico-institucional-2025-2030-del-ministerio-de-salud.pdf"),
    ("pei-minsa", "pnms", "declarada", "https://cdn.www.gob.pe/uploads/document/file/7566687/6425886-plan-estrategico-institucional-2025-2030-del-ministerio-de-salud.pdf"),
] + [(f"pdrc-{i:02d}", "pedn", "norma", "") for i in range(26)]

# plan_id, periodo, tipo, estado, publicado, url, nota
REPORTES = [
    ("an", "2024", "Reporte de seguimiento de las Políticas de Estado 2024 (CEPLAN)", "noubicado", "", "https://cdn.www.gob.pe/uploads/document/file/8083048/6779901-sesion_326_consejo_directivo_11042025.pdf", "Se presentó al Consejo Directivo de CEPLAN el 11/04/2025; no encontramos el reporte publicado. El enlace es el acta de esa sesión."),
    ("an", "2015–2024", "Reporte de seguimiento de las Políticas de Estado 2025 (CEPLAN)", "ubicado", "2025-10", "https://cdn.www.gob.pe/uploads/document/file/9474737/7757132-ceplan-reporte-de-seguimiento-de-las-politicas-de-estado-2025.pdf", ""),
    ("vision", "—", "Una visión no tiene reporte propio; se sigue a través del PEDN", "noaplica", "", "", ""),
    ("pedn", "2024", "Reporte de seguimiento del PEDN correspondiente al año 2024 (CEPLAN)", "noubicado", "", "https://cdn.www.gob.pe/uploads/document/file/8207551/6860546-3-rd-cumplimiento-pnmgp-ejercicio-2024-vf.pdf", "Un documento oficial dice que CEPLAN lo elaboró; no encontramos el reporte publicado. El enlace es el documento que lo menciona."),
    ("pgg", "2026", "Primer reporte de seguimiento de la PGG 2026-2031", "porrevisar", "", "", "Falta tabular cuándo exige la norma el primer reporte."),
    ("pnms", "2022", "Reporte de seguimiento de la PNMS, año 2022", "ubicado", "", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2023/IPMS_2023-reporte_seguimiento.pdf", ""),
    ("pnms", "2023", "Reporte de seguimiento de la PNMS, año 2023", "ubicado", "2024-07-03", "https://www.minsa.gob.pe/transparencia/index.asp?op=1401", ""),
    ("pnms", "2023", "Informe de evaluación de la PNMS al 2030", "ubicado", "2024-06-15", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2024/Informe%20de%20evaluacion%20de%20PNMS%202023.pdf", ""),
    ("pnms", "2024", "Reporte de seguimiento de la PNMS, año 2024", "ubicado", "2025-06-16", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2025/Reporte-seguimiento-Politica-Nacional-Multisectorial-Salud-2024.pdf", ""),
    ("pnms", "2024", "Reporte de cumplimiento de la PNMS, año 2024", "ubicado", "2025-06-16", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2025/Reporte-cumplimiento-Politica-Nacional-Multisectorial-Salud-2024.pdf", ""),
    ("pnms", "2025", "Reporte de seguimiento de la PNMS, año 2025", "ubicado", "2026-06-15", "https://www.minsa.gob.pe/transparencia/index.asp?op=1401", ""),
    ("pem-pnms", "2023–2025", "Matriz de compromisos multisectoriales de la PNMS", "ubicado", "2024", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2024/MATRIZ-DE-COMPROMISOS-MULTISECTORIALES-PNMS-2023.pdf", ""),
    ("pesem-salud", "2021", "Informe de evaluación de implementación del PESEM 2016-2021, año 2021", "ubicado", "", "https://www.minsa.gob.pe/Recursos/OTRANS/05PlanEstrategico/Archivos/2023/IEI2016-2021-PESEM.pdf", ""),
    ("pesem-salud", "2023", "Informe de evaluación de resultados del PESEM 2016-2025 ampliado, año 2023", "ubicado", "", "https://www.minsa.gob.pe/Recursos/OTRANS/05PlanEstrategico/Archivos/2024/Informe-evaluacion-PESEM-Sector-Salud-2023.pdf", ""),
    ("pesem-salud", "2024–2025", "Reportes de seguimiento del PESEM 2024-2030", "porrevisar", "", "", "Revisar el portal de transparencia del MINSA antes de marcarlo como no ubicado."),
    ("pei-minsa", "2023", "Informe de evaluación institucional MINSA 2023", "ubicado", "", "https://www.minsa.gob.pe/Recursos/OTRANS/14Informes/pei/Informe%20de%20evaluacion%20institucional%20MINSA%202023.pdf", ""),
]

# plan_id, dimension, valor (si|no|sin_verificar), evidencia
DIMS = ["Indicadores y metas", "Plan de implementación", "Seguimiento publicado", "Evaluación publicada", "Articulación declarada"]
DIMENSIONES = [
    ("an", "Indicadores y metas", "si", "https://cdn.www.gob.pe/uploads/document/file/9474737/7757132-ceplan-reporte-de-seguimiento-de-las-politicas-de-estado-2025.pdf"),
    ("an", "Seguimiento publicado", "si", "https://cdn.www.gob.pe/uploads/document/file/9474737/7757132-ceplan-reporte-de-seguimiento-de-las-politicas-de-estado-2025.pdf"),
    ("pedn", "Indicadores y metas", "si", "https://busquedas.elperuano.pe/dispositivo/NL/2534766-1"),
    ("pedn", "Seguimiento publicado", "sin_verificar", ""),
    ("pedn", "Articulación declarada", "si", "https://busquedas.elperuano.pe/dispositivo/NL/2090829-7"),
    ("pgg", "Indicadores y metas", "no", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3"),
    ("pgg", "Articulación declarada", "si", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3"),
    ("pnms", "Indicadores y metas", "si", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2023/IPMS_2023-reporte_seguimiento.pdf"),
    ("pnms", "Plan de implementación", "si", "https://vlex.com.pe/vid/869835364"),
    ("pnms", "Seguimiento publicado", "si", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2025/Reporte-seguimiento-Politica-Nacional-Multisectorial-Salud-2024.pdf"),
    ("pnms", "Evaluación publicada", "si", "https://www.minsa.gob.pe/Recursos/OTRANS/09GestionIns/indicadores/2024/Informe%20de%20evaluacion%20de%20PNMS%202023.pdf"),
    ("pesem-salud", "Evaluación publicada", "si", "https://www.minsa.gob.pe/Recursos/OTRANS/05PlanEstrategico/Archivos/2024/Informe-evaluacion-PESEM-Sector-Salud-2023.pdf"),
    ("pesem-salud", "Seguimiento publicado", "sin_verificar", ""),
    ("pesem-salud", "Articulación declarada", "si", "https://juventud.gob.pe/normativa-joven-pdf/3/105.pdf"),
    ("pei-minsa", "Evaluación publicada", "si", "https://www.minsa.gob.pe/Recursos/OTRANS/14Informes/pei/Informe%20de%20evaluacion%20institucional%20MINSA%202023.pdf"),
    ("pei-minsa", "Articulación declarada", "si", "https://cdn.www.gob.pe/uploads/document/file/7566687/6425886-plan-estrategico-institucional-2025-2030-del-ministerio-de-salud.pdf"),
]

# plan_id, tipo (discrepancia|pista|observacion), texto
NOTAS = [
    ("vision", "discrepancia", "Dos fuentes oficiales dan fechas distintas. El acta de la sesión 126 del Foro del Acuerdo Nacional registra el lunes 29 de abril de 2019; el folleto 'Visión del país al 2050' del Acuerdo Nacional dice que se aprobó el 27 de febrero de 2019. No hay explicación documentada; el acta es el registro de la sesión."),
    ("pgg", "pista", "Pista corregida. La prensa informó metas con plazo a diciembre de 2026, julio de 2027 y 2031. El texto del DS 127-2026-PCM no fija metas, indicadores ni plazos; esos plazos se mencionaron en la exposición del presidente del Consejo de Ministros ante la Cámara de Diputados."),
    ("pesem-salud", "observacion", "Superposición de horizontes: el PESEM 2016-2021 ampliado al 2025 (RM 364-2022-MINSA) y el PESEM 2024-2030 (RM 1174-2023/MINSA) cubren ambos 2024 y 2025. El informe de evaluación del año 2023 corresponde al plan ampliado. No hay explicación documentada de cuál rige en esos dos años."),
    ("pei-minsa", "observacion", "Superposición de horizontes: el PEI 2019-2027 ampliado (RM 172-2024-MINSA) y el PEI 2025-2030 cubren ambos 2025 a 2027. Falta confirmar la norma que aprueba el PEI 2025-2030."),
]

FUENTES = [
    ("an", "Acuerdo Nacional: Políticas de Estado, Visión del Perú al 2050", "https://acuerdonacional.pe/wp-content/uploads/2024/01/Politicas_de_Estado_2023.pdf"),
    ("vision", "Acta 126: Visión del Perú al 2050 (Acuerdo Nacional)", "https://acuerdonacional.pe/wp-content/uploads/2023/03/Acta-126-Vision-del-Peru-al-2050.pdf"),
    ("vision", "Folleto Visión del país al 2050 (Acuerdo Nacional)", "https://acuerdonacional.pe/wp-content/uploads/2022/11/3-Folleto-Vision-del-pais-al-2050.pdf"),
    ("pedn", "DS 095-2022-PCM (El Peruano)", "https://busquedas.elperuano.pe/dispositivo/NL/2090829-7"),
    ("pedn", "DS 103-2023-PCM (El Peruano)", "https://busquedas.elperuano.pe/dispositivo/NL/2215042-3/"),
    ("pedn", "RPCD 046-2026/CEPLAN/PCD (El Peruano)", "https://busquedas.elperuano.pe/dispositivo/NL/2534766-1"),
    ("pgg", "DS 127-2026-PCM (El Peruano)", "https://busquedas.elperuano.pe/dispositivo/NL/2551404-3"),
    ("pnms", "Política Nacional Multisectorial de Salud al 2030 (texto)", "https://observateperu.ins.gob.pe/sites/default/files/2024-10/Pol%C3%ADtica%20Nacional%20Multisectorial%20de%20Salud%20al%202030%20.pdf"),
    ("pnms", "MINSA: transparencia, políticas nacionales", "https://www.minsa.gob.pe/transparencia/index.asp?op=1401"),
    ("pem-pnms", "DS 016-2021-SA", "https://vlex.com.pe/vid/869835364"),
    ("pesem-salud", "MINSA: transparencia, PESEM", "https://www.minsa.gob.pe/transparencia/index.asp?op=1001"),
    ("pesem-salud", "RM 364-2022-MINSA (gob.pe)", "https://www.gob.pe/institucion/minsa/normas-legales/3002475-364-2022-minsa"),
    ("pei-minsa", "PEI 2025-2030 del Ministerio de Salud (gob.pe)", "https://cdn.www.gob.pe/uploads/document/file/7566687/6425886-plan-estrategico-institucional-2025-2030-del-ministerio-de-salud.pdf"),
    ("pei-minsa", "RM 172-2024-MINSA (gob.pe)", "https://cdn.www.gob.pe/uploads/document/file/6594276/5734282-resolucion-ministerial-n-172-2024-minsa.pdf"),
]


# ---------------------------------------------------------------------------
# Políticas nacionales: lista oficial del Informe anual de políticas nacionales 2023
# (CEPLAN, agosto 2024): 40 políticas aprobadas en el marco del DS 029-2018-PCM, a junio de 2024.
REP_PN, FUENTES_PN, ART_PN = [], [], []
NOMBRE_SECTOR = {}
INFORME_PN = "https://www.mef.gob.pe/contenidos/transparencia/doc_gestion/Informe_anual_politicas_nacionales_2023.pdf"
POLITICAS = [  # n, nombre, decreto, rector, tipo, necesidad
    (1, "Política Nacional contra las Drogas al 2030", "DS 192-2020-PCM", "PCM", "Multisectorial", "salud"),
    (2, "Política Nacional de Gestión del Riesgo de Desastres al 2050", "DS 038-2021-PCM", "PCM", "Multisectorial", "ambiente"),
    (3, "Política Nacional de Modernización de la Gestión Pública al 2030", "DS 103-2022-PCM", "PCM", "Multisectorial", "estado"),
    (4, "Política Nacional Multisectorial de Transformación Digital al 2030", "DS 085-2023-PCM", "PCM", "Multisectorial", "movilidad"),
    (5, "Política Nacional de Cultura al 2030", "DS 009-2020-MC", "MINCUL", "Sectorial", "cultura"),
    (6, "Política Nacional de Lenguas Originarias, Tradición Oral e Interculturalidad al 2040", "DS 012-2021-MC", "MINCUL", "Multisectorial", "cultura"),
    (7, "Política Nacional de la Lectura, el Libro y Bibliotecas al 2030", "DS 007-2022-MC", "MINCUL", "Sectorial", "cultura"),
    (8, "Política Nacional del Pueblo Afroperuano al 2030", "DS 005-2022-MC", "MINCUL", "Multisectorial", "cultura"),
    (9, "Política Nacional del Ambiente al 2030", "DS 023-2021-MINAM", "MINAM", "Multisectorial", "ambiente"),
    (10, "Política Nacional Penitenciaria al 2030", "DS 011-2020-JUS", "MINJUSDH", "Multisectorial", "seguridad"),
    (11, "Política Nacional del Adolescente en Riesgo y en Conflicto con la Ley Penal al 2030", "DS 009-2023-JUS", "MINJUSDH", "Multisectorial", "seguridad"),
    (12, "Política Nacional de Lucha contra el Crimen Organizado 2019-2030", "DS 017-2019-IN", "MININTER", "Multisectorial", "seguridad"),
    (13, "Política Nacional Multisectorial de Lucha contra el Terrorismo 2019-2023", "DS 023-2019-IN", "MININTER", "Multisectorial", "seguridad"),
    (14, "Política Nacional frente a la Trata de Personas y sus formas de explotación al 2030", "DS 009-2021-IN", "MININTER", "Multisectorial", "seguridad"),
    (15, "Política Nacional Multisectorial de Seguridad Ciudadana al 2030", "DS 006-2022-IN", "MININTER", "Multisectorial", "seguridad"),
    (16, "Política Nacional de Cooperación Técnica Internacional al 2030", "DS 008-2023-RE", "RREE", "Sectorial", "estado"),
    (17, "Política Nacional de Competitividad y Productividad", "DS 345-2018-EF", "MEF", "Multisectorial", "produccion"),
    (18, "Política Nacional de Inclusión Financiera", "DS 255-2019-EF", "MEF", "Multisectorial", "empleo"),
    (19, "Política Nacional de Actividad Física, Recreación, Deporte y Educación Física", "DS 014-2022-MINEDU", "MINEDU", "Sectorial", "educacion"),
    (20, "Política Nacional de Atención Educativa para la Población de Ámbitos Rurales", "DS 013-2018-MINEDU", "MINEDU", "Sectorial", "educacion"),
    (21, "Política Nacional de Educación Superior y Técnico Productiva", "DS 012-2020-MINEDU", "MINEDU", "Sectorial", "educacion"),
    (22, "Política Nacional de Juventud", "DS 013-2019-MINEDU", "MINEDU", "Multisectorial", "educacion"),
    (23, "Política Nacional Multisectorial de Salud al 2030", "DS 026-2020-SA", "MINSA", "Multisectorial", "salud"),
    (24, "Política Nacional de Empleo Decente", "DS 013-2021-TR", "MTPE", "Multisectorial", "empleo"),
    (25, "Política Nacional de Seguridad y Salud en el Trabajo al 2030", "DS 018-2021-TR", "MTPE", "Multisectorial", "empleo"),
    (26, "Política Nacional Agraria 2021-2030", "DS 017-2021-MIDAGRI", "MIDAGRI", "Sectorial", "alimentacion"),
    (27, "Política Nacional Multisectorial para la Pequeña Minería y Minería Artesanal al 2030", "DS 016-2022-EM", "MINEM", "Multisectorial", "produccion"),
    (28, "Política Nacional Marítima", "DS 012-2019-DE", "MINDEF", "Multisectorial", "produccion"),
    (29, "Política Nacional de Seguridad y Defensa Nacional", "DS 005-2021-DE", "MINDEF", "Multisectorial", "seguridad"),
    (30, "Política Nacional de Transporte Urbano", "DS 012-2019-MTC", "MTC", "Sectorial", "movilidad"),
    (31, "Política Nacional Multisectorial de Seguridad Vial 2023-2030", "DS 009-2023-MTC", "MTC", "Multisectorial", "movilidad"),
    (32, "Política Nacional de Vivienda y Urbanismo al 2030", "DS 012-2021-VIVIENDA", "MVCS", "Sectorial", "vivienda"),
    (33, "Política Nacional de Desarrollo Industrial", "DS 016-2022-PRODUCE", "PRODUCE", "Sectorial", "produccion"),
    (34, "Política Nacional de Acuicultura al 2030", "DS 001-2023-PRODUCE", "PRODUCE", "Sectorial", "alimentacion"),
    (35, "Política Nacional para la Calidad", "DS 006-2024-PRODUCE", "PRODUCE", "Sectorial", "produccion"),
    (36, "Política Nacional de Igualdad de Género", "DS 008-2019-MIMP", "MIMP", "Multisectorial", "proteccion"),
    (37, "Política Nacional Multisectorial de Discapacidad para el Desarrollo al 2030", "DS 007-2021-MIMP", "MIMP", "Multisectorial", "proteccion"),
    (38, "Política Nacional Multisectorial para las niñas, niños y adolescentes al 2030", "DS 008-2021-MIMP", "MIMP", "Multisectorial", "proteccion"),
    (39, "Política Nacional Multisectorial para las personas adultas mayores al 2030", "DS 006-2021-MIMP", "MIMP", "Multisectorial", "proteccion"),
    (40, "Política Nacional de Desarrollo e Inclusión Social al 2030", "DS 008-2022-MIDIS", "MIDIS", "Multisectorial", "proteccion"),
]
# Agrupación editorial de Qhawana: cada política se asigna a la necesidad a la que más sirve.
NECESIDADES = [
    ("salud", "Salud", "Prevenir y atender enfermedades"),
    ("educacion", "Educación", "Aprender en cada etapa de la vida"),
    ("vivienda", "Vivienda y agua", "Vivienda, agua y una ciudad habitable"),
    ("seguridad", "Seguridad y justicia", "Vivir seguro y acceder a justicia"),
    ("empleo", "Trabajo e ingresos", "Trabajo digno, seguro y con ingresos"),
    ("alimentacion", "Alimentación", "Alimentos suficientes y sanos"),
    ("proteccion", "Protección e inclusión", "Protección para quien más lo necesita"),
    ("movilidad", "Movilidad y conexión", "Moverse con seguridad y estar conectado"),
    ("ambiente", "Ambiente y desastres", "Ambiente sano y menos riesgo de desastres"),
    ("cultura", "Cultura e identidad", "Lengua, identidad y cultura"),
    ("estado", "Un Estado que funcione", "Trámites, servicios y gestión pública"),
    ("produccion", "Producción", "Producir, competir y crecer"),
]
NOTAS_NEC = [
    ("vivienda", "observacion", "La lista oficial de CEPLAN (junio de 2024) no incluye una política nacional de agua y saneamiento aprobada en el marco del DS 029-2018-PCM. Falta verificar qué instrumento rige ese servicio."),
]


def escribir(nombre, encabezado, filas):
    with open(os.path.join(OUT, nombre), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(encabezado)
        w.writerows(filas)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ART = {"MININTER": "del ", "MINAM": "del ", "PRODUCE": "de la ", "MIMP": "de la "}
    NOMBRE_SECTOR.update({c: ("Presidencia del Consejo de Ministros" if c == "PCM" else "Ministerio " + ART.get(c, "de ") + n) for c, a, n in SECTORES})
    filas = [(p[0], p[1], p[2] if p[1] == "sectorial" else "", p[2] if p[1] == "territorial" else "", NIVEL.get(p[0], 1)) + p[3:] for p in PLANES]
    import re
    nec_pol = []
    for n, nom, ds, rec, tipo, nec in POLITICAS:
        pid = "pnms" if n == 23 else f"pn-{n:02d}"
        nec_pol.append((pid, nec))
        if n == 23:
            continue
        anio = int(ds.split("-")[1])
        m = re.search(r"(\d{4})\s*-\s*(\d{4})", nom) or None
        fin = int(m.group(2)) if m else (int(re.search(r"al (\d{4})", nom).group(1)) if re.search(r"al (\d{4})", nom) else "")
        ini = int(m.group(1)) if m else anio
        corto = re.sub(r"^Política Nacional (Multisectorial )?(de |del |de la |para (la |las |los )?|contra (las |el )?|frente a (la )?)?", "", nom)
        corto = corto[0].upper() + corto[1:]
        filas.append((pid, "sectorial", rec, "", 1, f"Política nacional {tipo.lower()}", corto, nom, NOMBRE_SECTOR[rec] + " (rector)", ds, ini, fin, "si",
                      f"Política nacional {tipo.lower()} aprobada por {ds}. Figura en la lista oficial de CEPLAN a junio de 2024."))
        REP_PN.append((pid, "2023", "Informe anual de políticas nacionales 2023 (CEPLAN, agosto 2024)", "ubicado", "2024-08", INFORME_PN, "Reporte consolidado de CEPLAN; falta enlazar el reporte de cumplimiento de la propia política."))
        FUENTES_PN.append((pid, "Informe anual de políticas nacionales 2023 (CEPLAN)", INFORME_PN, CONSULTA))
        ART_PN.append((pid, "pedn", "norma", ""))
    escribir("planes.csv", ["id", "eje", "sector", "region", "nivel", "tipo", "corto", "nombre", "actores", "norma", "horizonte_inicio", "horizonte_fin", "catalogado", "resumen"], filas)
    escribir("reportes.csv", ["plan_id", "periodo", "tipo", "estado", "publicado", "url", "nota"], REPORTES + REP_PN + REP_REG + [("pnms", "2023", "Informe anual de políticas nacionales 2023 (CEPLAN, agosto 2024)", "ubicado", "2024-08", INFORME_PN, "Reporte consolidado de CEPLAN.")])
    escribir("articulacion.csv", ["plan_id", "plan_superior", "base", "evidencia_url"], ARTICULACION + ART_PN)
    escribir("fuentes.csv", ["plan_id", "titulo", "url", "fecha_consulta"], [f + (CONSULTA,) for f in FUENTES + FUENTE_REG] + FUENTES_PN)
    escribir("necesidades.csv", ["codigo", "nombre", "descripcion"], NECESIDADES)
    escribir("necesidad_plan.csv", ["plan_id", "necesidad"], nec_pol + [("pem-pnms", "salud"), ("pesem-salud", "salud"), ("pei-minsa", "salud")])
    escribir("notas_necesidad.csv", ["necesidad", "tipo", "texto"], NOTAS_NEC)
    escribir("sectores.csv", ["codigo", "abreviatura", "nombre"], SECTORES)
    escribir("multisectorial.csv", ["plan_id", "sector", "rol", "evidencia_url"], MULTISECTORIAL)
    escribir("versiones.csv", ["plan_id", "fecha", "descripcion", "norma", "url", "vigente"], VERSIONES + VER_REG)
    escribir("dimensiones.csv", ["plan_id", "dimension", "valor", "evidencia_url"], DIMENSIONES)
    escribir("notas.csv", ["plan_id", "tipo", "texto"], NOTAS + NOTA_REG)
    print("CSV escritos en", OUT)
