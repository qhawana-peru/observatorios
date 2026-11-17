"""Piloto de la vitrina con indicadores y del primer hilo (anemia infantil).

Regiones piloto: Cajamarca, Piura y Puno. Escribe cuatro CSV en catalogo/:
objetivos.csv, indicadores.csv, hilo.csv y hallazgos.csv. Solo fuentes oficiales.
Consulta: 16/11/2026.
"""
import csv, os

OUT = os.path.join(os.path.dirname(__file__), "catalogo")
CAJ = "pdrc-05"  # Cajamarca
EVAL_CAJ = "https://www.regioncajamarca.gob.pe/media/portal/KJDIG/documento/85882/EVALUACI%C3%93N_PDRC_VB_1.pdf?r=1768840168"
PEDN_IND = "https://cdn.climatepolicyradar.org/navigator/PER/2023/national-strategic-development-plan-pedn-to-2050-plan-estrategico-de-desarrollo-nacional-pedn-al-2050_2353d37b8b638109cebd48761ea2a771.pdf"
PNDIS_REP = "https://cdn.www.gob.pe/uploads/document/file/8221743/6868947-formato-de-reporte-de-cumplimiento-ds-029-2018-pcm-12-06-2025-de-dgsei_rev-f.pdf"
PNMNNA_REP = "https://cdn.www.gob.pe/uploads/document/file/8221970/6869059-reporte_cumplimiento_pnmnna_2024.pdf"
PMA = "https://observatorio.ceplan.gob.pe/ficha/t13"
ENDES_PPR = "https://proyectos.inei.gob.pe/endes/2024/ppr2/indicadores_de_resultados_de_los_programas_presupuestales_endes_2024.pdf"
INEI_2024 = "https://www.gob.pe/institucion/inei/noticias/1177022-el-67-4-de-los-ninos-menores-de-seis-meses-recibieron-lactancia-materna"

ON = {"ON1": "ON1 · Capacidades de las personas", "ON2": "ON2 · Gestión sostenible del territorio",
      "ON3": "ON3 · Competitividad y productividad", "ON4": "ON4 · Sociedad justa y Estado efectivo"}

# Objetivos estratégicos regionales del PDRC Cajamarca al 2033 según su Informe de evaluación 2023-2024
# (octubre 2025). Enunciados abreviados por Qhawana; el vínculo con el PEDN es el que declara el informe.
OBJETIVOS = [
    (CAJ, "OER.01", "Mejorar la gestión de las cuencas hidrográficas de manera sostenible e integrada", "ON2"),
    (CAJ, "OER.02", "Reducir la vulnerabilidad de la población y sus medios de vida ante los riesgos de desastres", "ON2"),
    (CAJ, "OER.03", "Mejorar las condiciones de salud de la población, con acceso a servicios oportunos y de calidad", "ON1"),
    (CAJ, "OER.04", "Mejorar la calidad de la educación básica regular, alternativa y especial", "ON1"),
    (CAJ, "OER.05", "Mejorar la seguridad ciudadana en la población", "ON4"),
    (CAJ, "OER.06", "Mejorar las condiciones laborales para un empleo decente", "ON3"),
    (CAJ, "OER.07", "Fortalecer la gobernanza territorial participativa y concertadora", "ON4"),
    (CAJ, "OER.08", "Fomentar la investigación, tecnología, digitalización e innovación", "ON3"),
    (CAJ, "OER.09", "Impulsar el crecimiento económico inclusivo y sostenido", "ON3"),
    (CAJ, "OER.10", "Mejorar la gestión de la calidad ambiental", ""),
    (CAJ, "OER.11", "Agricultura familiar (el informe usa dos enunciados distintos)", "ON3"),
    (CAJ, "OER.12", "Mejorar las condiciones de vida y el ejercicio de derechos de personas en condiciones de vulnerabilidad", ""),
    (CAJ, "OER.13", "Promover infraestructura social, productiva y de innovación", "ON3"),
]

# plan, objetivo, código, indicador, población, LB año, LB valor, metas, obtenidos, unidad, fuente del dato, nota
I = lambda *a: (CAJ,) + a
INDICADORES = [
    I("OER.01", "IND.01.OER.01", "Cuencas con plan de gestión de recursos hídricos aprobado e implementado", "", 2021, 18.75, "2023=25;2024=31.25", "2023=18.75;2024=18.75", "%", "", ""),
    I("OER.02", "IND.01.OER.02", "Población afectada por emergencias de origen natural", "", 2020, 0.08, "2023=0.08;2024=0.07", "2023=0.07;2024=0.07", "%", "", ""),
    I("OER.02", "IND.02.OER.02", "Población urbana en barrios marginales, asentamientos improvisados o viviendas inadecuadas", "", 2021, 56.6, "2023=54.17;2024=53.42", "2023=53.25;2024=50.05", "%", "", ""),
    I("OER.03", "IND.01.OER.03", "Población con algún problema de salud no crónico", "", 2021, 32.2, "2023=30.3;2024=29.4", "2023=33.2;2024=", "%", "", ""),
    I("OER.03", "IND.02.OER.03", "Población con acceso a seguro de salud", "", 2022, 88.3, "2023=89.2;2024=90.1", "2023=91.3;2024=", "%", "", ""),
    I("OER.03", "IND.02.AER.03.04", "Niñas y niños de 6 a 59 meses con anemia (indicador de una acción estratégica)", "6 a 59 meses", 2021, 20.0, "2023=18.3;2024=17.4", "2023=25.8;2024=27.6", "%", "", "anemia"),
    I("OER.04", "IND.01.OER.04", "Estudiantes de 2.º de secundaria con rendimiento satisfactorio en lectura y matemática", "", 2021, 5.0, "2023=5.7;2024=6.07", "2023=;2024=", "%", "", ""),
    I("OER.04", "IND.02.OER.04", "Estudiantes de 2.º y 4.º de primaria con rendimiento satisfactorio en lectura y matemática", "", 2020, 16.7, "2023=21.17;2024=22.14", "2023=;2024=", "%", "", ""),
    I("OER.05", "IND.01.OER.05", "Población de 15 años y más con percepción de inseguridad", "", 2021, 83.5, "2023=86.6;2024=81.2", "2023=83;2024=", "%", "", ""),
    I("OER.06", "IND.01.OER.06", "PEA ocupada adecuadamente empleada", "", 2021, 37.8, "2023=34.34;2024=34.99", "2023=31.35;2024=31.98", "%", "", ""),
    I("OER.06", "IND.02.OER.06", "Tasa de desempleo", "", 2020, 4.7, "2023=3.1;2024=3.1", "2023=4.1;2024=4.1", "%", "", ""),
    I("OER.07", "IND.01.OER.07", "Población adulta que considera buena o muy buena la gestión del Gobierno Regional", "", 2021, 30.3, "2023=34.15;2024=36.08", "2023=22;2024=24.5", "%", "", ""),
    I("OER.08", "IND.01.OER.08", "Inversión privada en investigación, desarrollo e innovación", "", 2022, 0.0, "2023=2.27;2024=4.54", "2023=;2024=", "%", "", ""),
    I("OER.09", "IND.01.OER.09", "Variación anual del PBI real departamental", "", 2021, 11.1, "2023=2.31;2024=2.62", "2023=-0.5;2024=0.92", "%", "", ""),
    I("OER.10", "IND.01.OER.10", "Gasto público ambiental en el gasto total", "", 2018, 0.98, "2023=1.25;2024=1.31", "2023=1.17;2024=0.74", "%", "", ""),
    I("OER.11", "IND.01.OER.11", "Superficie agrícola con cultivos destinados a la venta", "", 2021, 58.1, "2023=60.4;2024=61.6", "2023=;2024=", "%", "", ""),
    I("OER.11", "IND.02.OER.11", "Variación anual del volumen físico de la producción agropecuaria (canasta mínima)", "", 2021, 2.44, "2023=2.33;2024=2.27", "2023=0.11;2024=2.13", "%", "", ""),
    I("OER.12", "IND.01.OER.12", "Personas con discapacidad en edad de trabajar que se incorporan al mercado laboral", "", 2022, 43.0, "2023=43.8;2024=44.7", "2023=20.94;2024=19.05", "%", "", ""),
    I("OER.13", "IND.01.OER.13", "Índice de infraestructura", "", 2022, 4.7, "2023=4.73;2024=4.75", "2023=4.4;2024=5.4", "índice", "", ""),
]

# Hilo de la anemia infantil.
# serie, etiqueta, plan_id, tipo (meta | medido | meta-otra), ámbito, población, criterio, puntos, fuente, url, nota
HILO = [
    ("pedn", "PEDN al 2050", "pedn", "meta", "Perú", "6 a 35 meses", "Fijada antes del cambio de criterio de 2024", "2021=38.8;2026=30;2030=22;2040=21;2050=20",
     "PEDN al 2050, indicadores (CEPLAN), AE 1.2.3", PEDN_IND, "Copia del documento oficial; falta enlazar la de CEPLAN. La RPCD 046-2026/CEPLAN/PCD modificó 26 fichas: por verificar si esta fue una."),
    ("pndis", "Política de Desarrollo e Inclusión Social", "pn-40", "meta", "Perú", "6 a 35 meses", "Fijada antes del cambio de criterio de 2024", "2021=38.8;2024=36.8;2030=32.3",
     "Reporte de cumplimiento 2024 de la PNDIS (MIDIS), indicador IOP.01.02", PNDIS_REP, "Valor 2024 reportado: 43,7 %."),
    ("pmanemia", "Plan Multisectorial contra la Anemia 2024-2030", "", "meta", "Perú", "menores de 36 meses", "", "2030=37.2",
     "Observatorio Nacional de Prospectiva (CEPLAN), ficha T13", PMA, "Norma de aprobación del plan por confirmar."),
    ("pnmnna", "Política de Niñas, Niños y Adolescentes", "pn-38", "meta", "Perú", "6 a 35 meses", "", "2024=38.9",
     "Reporte de cumplimiento 2024 de la PNMNNA (MIMP), indicador IOP.01.03", PNMNNA_REP, "Solo ubicamos la meta 2024; valor 2024 reportado: 43,7 %."),
    ("endes-363", "ENDES · criterio anterior", "", "medido", "Perú", "6 a 35 meses", "RM 363-2022-MINSA", "2019=40.1;2020=40;2021=38.8;2022=42.4;2023=43.1;2024=43.7",
     "INEI, Indicadores de resultados de los programas presupuestales, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("endes-251", "ENDES · criterio OMS 2024", "", "medido", "Perú", "6 a 35 meses", "RM 251-2024-MINSA", "2019=31.4;2020=30.4;2021=28.4;2022=33.5;2023=34.6;2024=35.3",
     "INEI, Indicadores de resultados de los programas presupuestales, ENDES 2024, cuadro 06.1A", ENDES_PPR, "El INEI usa este criterio en su nota de prensa de la ENDES 2024."),
    ("caj-363", "ENDES · criterio anterior", CAJ, "medido", "Cajamarca", "6 a 35 meses", "RM 363-2022-MINSA", "2019=28.7;2020=33.8;2021=32.9;2022=38.2;2023=34.9;2024=38.4", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("caj-251", "ENDES · criterio OMS 2024", CAJ, "medido", "Cajamarca", "6 a 35 meses", "RM 251-2024-MINSA", "2019=31.7;2020=36.8;2021=32.3;2022=35.7;2023=32.5;2024=40.6", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),
    ("caj-pdrc", "Meta del PDRC (6 a 59 meses)", CAJ, "meta-otra", "Cajamarca", "6 a 59 meses", "Fuente no indicada", "2021=20;2023=18.3;2024=17.4",
     "Informe de evaluación del PDRC Cajamarca, periodos 2023-2024 (oct 2025)", EVAL_CAJ, "Valores reportados por el propio informe: 25,8 % (2023) y 27,6 % (2024). Otro grupo de edad: no se compara con las líneas de ENDES."),
    ("piu-363", "ENDES · criterio anterior", "pdrc-19", "medido", "Piura", "6 a 35 meses", "RM 363-2022-MINSA", "2019=43.8;2020=43.2;2021=36.7;2022=38;2023=39.7;2024=42.4", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("piu-251", "ENDES · criterio OMS 2024", "pdrc-19", "medido", "Piura", "6 a 35 meses", "RM 251-2024-MINSA", "2019=32.9;2020=34.1;2021=28.5;2022=28.9;2023=33.2;2024=35.4", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),
    ("pun-363", "ENDES · criterio anterior", "pdrc-20", "medido", "Puno", "6 a 35 meses", "RM 363-2022-MINSA", "2019=69.9;2020=69.4;2021=70.4;2022=67.2;2023=70.4;2024=76", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("pun-251", "ENDES · criterio OMS 2024", "pdrc-20", "medido", "Puno", "6 a 35 meses", "RM 251-2024-MINSA", "2019=42.8;2020=38.8;2021=34;2022=39.2;2023=46.4;2024=53.1", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),
]

# Hallazgos: id, ámbito (hilo:anemia o plan_id), tipo, título, observamos, por qué puede pasar, pregunta abierta, fuentes "título|url;;título|url"
HALLAZGOS = [
    ("h-metas", "hilo:anemia", "metas", "Cuatro metas nacionales para la misma anemia",
     "Para la anemia en niñas y niños pequeños, los instrumentos nacionales fijan metas distintas: el PEDN espera 22 % en 2030; la Política de Desarrollo e Inclusión Social, 32,3 %; el Plan Multisectorial contra la Anemia, 37,2 % (en menores de 36 meses). Para 2024, la Política de Desarrollo e Inclusión Social esperaba 36,8 % y la de Niñas, Niños y Adolescentes, 38,9 %.",
     "Se aprobaron en años distintos, por entidades distintas y con propósitos distintos: el PEDN marca una aspiración de largo plazo y el plan multisectorial, una meta operativa. Ninguna norma obliga a que coincidan.",
     "¿Cuál de estas metas orienta el presupuesto y la evaluación? Cuando se actualicen, ¿podrían converger en una sola trayectoria?",
     "PEDN al 2050, indicadores|" + PEDN_IND + ";;Reporte de cumplimiento 2024 de la PNDIS|" + PNDIS_REP + ";;Reporte de cumplimiento 2024 de la PNMNNA|" + PNMNNA_REP + ";;Ficha T13, CEPLAN|" + PMA),
    ("h-criterio", "hilo:anemia", "medicion", "Cambió la forma de medir y las metas no",
     "Desde la RM 251-2024-MINSA, que adopta la directriz de la OMS de 2024, el INEI publica dos cifras para el mismo año: en 2024, 43,7 % con el criterio anterior y 35,3 % con el nuevo. El cambio no mueve a todas las regiones igual: Puno pasa de 76,0 % a 53,1 % y Cajamarca, de 38,4 % a 40,6 %.",
     "El nuevo criterio cambia los puntos de corte y la corrección por altitud, por eso afecta más a las regiones altoandinas. Las metas vigentes se fijaron con el criterio anterior.",
     "¿Con qué criterio se evaluarán las metas al 2030? ¿Se recalcularán las líneas de base y las metas con el nuevo criterio?",
     "INEI, ENDES 2024, cuadros 06A y 06.1A|" + ENDES_PPR + ";;INEI, nota de prensa ENDES 2024|" + INEI_2024),
    ("h-caj-edad", CAJ, "medicion", "Cajamarca mide la anemia en otro grupo de edad y sin fuente declarada",
     "El PDRC Cajamarca al 2033 sigue la anemia en niñas y niños de 6 a 59 meses, como indicador de una acción estratégica. Su informe de evaluación no indica la fuente. Los planes nacionales y la ENDES usan el grupo de 6 a 35 meses. El valor reportado por el gobierno regional (27,6 % en 2024) se alejó de su meta (17,4 %).",
     "Un plan regional puede elegir indicadores propios; el informe no dice si el dato viene de la ENDES o de registros administrativos. El grupo de 6 a 59 meses incluye a niños mayores, en los que la anemia suele ser menor.",
     "¿Podría el PDRC agregar el indicador de 6 a 35 meses con fuente ENDES, para conversar con el PEDN y con las políticas nacionales? ¿Qué fuente usa hoy?",
     "Informe de evaluación del PDRC Cajamarca 2023-2024|" + EVAL_CAJ),
    ("h-caj-suelto", CAJ, "hilo-suelto", "Dos objetivos regionales sin hilo hacia el plan nacional",
     "En su informe de evaluación, el PDRC Cajamarca vincula 11 de sus 13 objetivos con un objetivo nacional del PEDN. Los de calidad ambiental (OER.10) y de personas en condiciones de vulnerabilidad (OER.12) quedan sin vínculo declarado.",
     "El informe describe la articulación en texto y no en una matriz; es posible que el plan completo sí los vincule. No pudimos abrir el documento completo (47,7 MB) para verificarlo.",
     "¿A qué objetivo nacional contribuyen estos dos objetivos? Si no hay uno que encaje, ¿es una señal para el PEDN?",
     "Informe de evaluación del PDRC Cajamarca 2023-2024|" + EVAL_CAJ),
    ("h-caj-dato", CAJ, "sin-dato", "Siete de 19 indicadores sin dato para 2024",
     "En el informe de evaluación del PDRC Cajamarca, 7 de los 19 indicadores catalogados no tienen valor para 2024, entre ellos todos los de salud y educación de nivel de objetivo. El propio informe recomienda fortalecer los sistemas de datos regionales.",
     "Varios indicadores dependen de encuestas nacionales que publican con rezago o que no tienen representatividad regional cada año.",
     "¿Qué indicadores podrían cambiarse por otros con dato anual disponible, sin perder lo que se quiere medir?",
     "Informe de evaluación del PDRC Cajamarca 2023-2024|" + EVAL_CAJ),
]


# Avance 2024 que reporta el propio informe de evaluación (100 = meta alcanzada); vacío si no hay dato.
AVANCE = {"IND.01.OER.01": 60, "IND.01.OER.02": 100, "IND.02.OER.02": 100, "IND.02.AER.03.04": 0, "IND.01.OER.06": 91.41,
          "IND.02.OER.06": 0, "IND.01.OER.07": 67.9, "IND.01.OER.09": 35.11, "IND.01.OER.10": 56.35, "IND.02.OER.11": 93.83,
          "IND.01.OER.12": 42.62, "IND.01.OER.13": 100}

# Fichas de los KPI. estado: activo (calculado con todo el catálogo), piloto (solo donde hay datos del piloto),
# revision (definido, falta insumo o validación), etapa2 (requiere presupuesto). Los descartados van aparte.
K = lambda *a: a
KPIS = [
    K("S1", "Sistema", "Planes regionales vigentes ubicados", "¿Cada territorio tiene un plan de desarrollo concertado vigente?",
      "PDRC con horizonte vigente y fuente oficial enlazada ÷ 26 (25 gobiernos regionales y Lima Metropolitana)", "Catálogo del museo (ordenanzas en El Peruano y portales regionales)", "Mensual", "Región", "Ubicado no es lo mismo que existe: un plan no ubicado puede existir. La norma de 11 planes está por confirmar.", "activo", "Territorio; Tabla y método"),
    K("S2", "Sistema", "Planes con horizonte vencido y sin reemplazo ubicado", "¿Dónde se planifica con un plan que ya terminó?",
      "Número de planes del catálogo cuyo horizonte terminó antes del año en curso y sin plan sucesor ubicado", "Catálogo del museo", "Mensual", "Tipo de plan, región", "Se informa como número, no como lista ordenada. Antes de publicar un caso se hace una búsqueda a fondo o una solicitud de acceso a la información.", "activo", "Plano; Territorio; Tabla y método"),
    K("S3", "Sistema", "Planes regionales con horizonte ampliado", "¿Se planifica de nuevo o se estira el plan anterior?",
      "PDRC vigentes formulados hasta 2016 y ampliados por ordenanza ÷ PDRC vigentes", "Catálogo del museo (versiones de cada plan)", "Mensual", "Región", "Ampliar está permitido por CEPLAN; el indicador describe, no sanciona.", "activo", "Territorio; Tabla y método"),
    K("S4", "Sistema", "Desfase de adecuación al plan superior", "¿Cuánto tarda un plan en ajustarse al PEDN actualizado?",
      "Años entre la actualización del PEDN (DS 103-2023-PCM) y la aprobación o actualización del plan inferior", "Catálogo del museo", "Anual", "Tipo de plan, región", "Requiere la fecha exacta de aprobación de cada plan y saber si declara alinearse al PEDN de 2023.", "revision", ""),
    K("S5", "Sistema", "Cobertura del inventario por tipo de plan exigido", "¿Existen todos los planes que la norma exige?",
      "Planes vigentes ubicados ÷ entidades obligadas a tenerlos, por tipo (PESEM, PEI, PDLC…)", "Catálogo del museo y padrón de entidades obligadas", "Trimestral", "Tipo de plan, sector, región", "Requiere el padrón de entidades obligadas (19 sectores, pliegos, 196 provincias, distritos).", "revision", ""),
    K("D1", "Diseño", "Indicadores con línea de base y año", "¿Se sabe desde dónde se parte?",
      "Indicadores del plan con valor y año de línea de base ÷ indicadores del plan", "Documento del plan o su informe de evaluación", "Al aprobar o actualizar el plan", "Plan", "En el piloto se usa el informe de evaluación de Cajamarca, no el documento completo del plan.", "piloto", "Ficha del plan"),
    K("D2", "Diseño", "Indicadores con fuente de datos declarada", "¿Se sabe de dónde sale el dato?",
      "Indicadores con fuente declarada en el documento evaluado ÷ indicadores del plan", "Documento del plan o su informe de evaluación", "Al aprobar o actualizar el plan", "Plan", "Mide lo que dice el documento revisado; el plan completo puede declarar fuentes que el informe omite.", "piloto", "Ficha del plan"),
    K("D3", "Diseño", "Indicadores con dato disponible para su territorio", "¿Habrá con qué medir cada año?",
      "Indicadores cuya fuente publica dato con representatividad para el nivel del plan ÷ indicadores del plan", "Fichas técnicas de las encuestas del INEI y registros administrativos", "Anual", "Plan", "Requiere una tabla de representatividad por encuesta, nivel y año, validada por una persona de estadística.", "revision", ""),
    K("D4", "Diseño", "Ritmo exigido frente a ritmo observado", "¿La meta pide un cambio parecido al que se ha visto?",
      "(Meta − línea de base) ÷ años del plan, frente a la variación anual promedio de la serie oficial en los últimos cinco años", "Plan e INEI", "Anual", "Indicador, plan", "Solo con serie oficial comparable (mismo indicador, misma fuente, mismo criterio). Una meta ambiciosa no es una mala meta: se presenta como pregunta.", "piloto", "Hilos"),
    K("A1", "Articulación", "Objetivos con vínculo declarado al nivel superior", "¿El plan dice a qué objetivo nacional contribuye?",
      "Objetivos del plan con vínculo declarado al PEDN (o al plan superior) ÷ objetivos del plan", "Matriz de articulación del plan o su informe de evaluación", "Al aprobar o actualizar el plan", "Plan", "Solo cuenta el vínculo declarado por la entidad, con evidencia.", "piloto", "Ficha del plan"),
    K("A2", "Articulación", "Cobertura inversa del PEDN", "¿Los objetivos nacionales bajan a los territorios?",
      "Para cada objetivo del PEDN, número de PDRC que declaran contribuir a él", "Matrices de articulación de los 26 PDRC", "Anual", "Objetivo del PEDN", "Solo tiene sentido con la mayoría de los PDRC catalogados; con tres regiones confundiría.", "revision", ""),
    K("A3", "Articulación", "Indicadores en lenguaje común", "¿Los niveles miden lo mismo de la misma forma?",
      "Indicadores del plan con la misma definición y fuente que un indicador del nivel nacional ÷ indicadores del plan", "Planes y fichas técnicas", "Anual", "Plan", "Requiere comparar fichas técnicas, no solo nombres de indicadores.", "revision", ""),
    K("A4", "Articulación", "Metas distintas para un mismo indicador", "¿Cuántos instrumentos se comprometen con lo mismo y cuánto difieren?",
      "Número de instrumentos con meta para el mismo indicador y año; distancia entre la meta más exigente y la menos exigente", "Planes, políticas y sus reportes", "Anual", "Hilo", "Se calcula por hilo. Solo entre metas de la misma población; si difiere, se anota.", "piloto", "Hilos"),
    K("A5", "Articulación", "Brecha entre meta regional y nacional", "¿Las metas regionales suman a la nacional?",
      "Meta regional menos meta nacional al mismo año, para indicadores comparables", "PDRC y PEDN", "Anual", "Región, indicador", "Rara vez comparable: distinto grupo de edad, fuente o año. Se activa solo con A3 resuelto.", "revision", ""),
    K("A6", "Articulación", "Multisectorialidad efectiva", "¿Los sectores involucrados en una política tienen compromisos propios?",
      "Sectores involucrados con indicadores o servicios asignados ÷ sectores declarados en la política", "Textos de las políticas nacionales multisectoriales", "Anual", "Política", "Requiere catalogar las 28 políticas multisectoriales; hoy solo está la de Salud.", "revision", ""),
    K("G1", "Seguimiento", "Planes con al menos un reporte ubicado", "¿Hay alguna prueba pública de que se sigue el plan?",
      "Planes con al menos un reporte de seguimiento o evaluación ubicado ÷ planes catalogados, por tipo", "Catálogo del museo", "Mensual", "Tipo de plan", "No mide si se publicaron todos los exigidos (eso es G2). Para las 40 políticas cuenta el informe anual consolidado de CEPLAN, no un reporte propio de cada una. En los PDRC la mayoría de reportes está por revisar.", "activo", "Tabla y método"),
    K("G2", "Seguimiento", "Reportes publicados frente a exigidos", "¿Se publica lo que la norma pide, y a tiempo?",
      "Reportes ubicados ÷ reportes exigidos por la norma; días de retraso respecto al plazo", "Catálogo del museo y directiva de CEPLAN", "Trimestral", "Tipo de plan, entidad", "Requiere tabular la frecuencia y el plazo exigidos a cada tipo de plan, incluidas las exoneraciones (RPCD 043-2026).", "revision", ""),
    K("G3", "Seguimiento", "Completitud del último reporte", "¿El reporte trae datos?",
      "Indicadores con valor en el último periodo evaluado ÷ indicadores del plan", "Informe de evaluación del plan", "Anual", "Plan", "Un indicador sin dato puede deberse a que la fuente nacional aún no publica.", "piloto", "Ficha del plan"),
    K("G4", "Seguimiento", "Metas del último año alcanzadas, según el propio reporte", "¿Qué dice la entidad de su propio avance?",
      "Indicadores con avance de 100 % en el último periodo, según el informe ÷ indicadores con dato", "Informe de evaluación del plan", "Anual", "Plan", "Es el resultado que declara la entidad; Qhawana no lo recalcula ni lo compara entre regiones.", "piloto", "Ficha del plan"),
    K("C1", "Ciudadano", "Compromisos por necesidad y territorio", "¿Quién se comprometió a qué sobre mi necesidad, en mi región?",
      "Número de metas vigentes por necesidad ciudadana y región, con su responsable", "Objetivos e indicadores catalogados", "Mensual", "Necesidad, región", "Requiere los objetivos e indicadores catalogados de los planes de cada región.", "revision", ""),
    K("C2", "Ciudadano", "Metas que vencen en la gestión", "¿Qué debe lograrse durante este periodo de gobierno?",
      "Metas con año dentro del periodo de la autoridad (2027-2030 regional; 2026-2031 nacional)", "Objetivos e indicadores catalogados", "Anual", "Región, nivel de gobierno", "Requiere metas multianuales catalogadas; el informe de Cajamarca solo trae metas 2023-2024.", "revision", ""),
    K("P1", "Presupuesto", "Presupuesto vinculado a objetivos del plan", "¿Cuánto del presupuesto financia lo que el plan prioriza?",
      "PIM vinculado a objetivos del plan (programas presupuestales y articulación del PEI) ÷ PIM total", "MEF, Consulta Amigable y datos abiertos", "Trimestral", "Entidad, objetivo", "Etapa 2. Reutiliza las herramientas de El Niño.", "etapa2", ""),
    K("P2", "Presupuesto", "Gasto sin vínculo con un plan", "¿Qué se gasta fuera de lo planificado?",
      "Gasto devengado en actividades y proyectos sin vínculo declarado con un objetivo ÷ devengado total", "MEF", "Trimestral", "Entidad", "Etapa 2. El vínculo depende de cómo cada entidad registra su POI.", "etapa2", ""),
    K("P3", "Presupuesto", "Coherencia entre prioridades y asignación", "¿Los objetivos priorizados reciben más recursos?",
      "PIM por objetivo priorizado frente a no priorizado, por entidad", "MEF y plan", "Anual", "Entidad", "Etapa 2.", "etapa2", ""),
    K("O1", "Observatorio", "Piezas con fuente oficial enlazada", "¿Cada pieza del museo se puede verificar?",
      "Piezas con al menos una fuente oficial enlazada ÷ piezas del catálogo", "Catálogo del museo", "En cada corte", "Eje", "Rinde cuentas de Qhawana, no del Estado.", "activo", "Tabla y método"),
    K("O2", "Observatorio", "Antigüedad de la verificación", "¿Qué tan al día está el catálogo?",
      "Días desde la última consulta de las fuentes de cada pieza", "Catálogo del museo", "En cada corte", "Pieza", "Hoy todas las piezas tienen la misma fecha de consulta.", "activo", "Tabla y método"),
    K("O3", "Observatorio", "Correcciones y tiempo de respuesta", "¿Qué tan rápido corrige Qhawana?",
      "Aportes y réplicas recibidos; mediana de días hasta resolverlos", "Formulario de aportes", "Mensual", "Tipo de aporte", "Requiere el canal de aportes y réplica, que aún no existe.", "revision", ""),
]
DESCARTADOS = [
    ("Índice compuesto de calidad o de gestión", "Mezcla dimensiones distintas, no dice qué corregir e invita a ordenar entidades."),
    ("Ranking de regiones o sectores", "Contradice la regla 6 del museo y castiga a quien publica más."),
    ("Proporción de objetivos de resultado frente a objetivos de gestión", "La clasificación es interpretativa y no replicable sin una regla externa."),
    ("Concordancia del dato reportado con la fuente oficial", "Es una función de control o auditoría, no de un observatorio ciudadano; y la mayoría de indicadores no es comparable."),
]


def escribir(nombre, encabezado, filas):
    with open(os.path.join(OUT, nombre), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(encabezado)
        w.writerows(filas)


if __name__ == "__main__":
    escribir("objetivos.csv", ["plan_id", "codigo", "enunciado", "objetivo_nacional", "evidencia_url"], [o + (EVAL_CAJ,) for o in OBJETIVOS])
    escribir("indicadores.csv", ["plan_id", "objetivo", "codigo", "indicador", "poblacion", "lb_anio", "lb_valor", "metas", "obtenidos", "unidad", "fuente_dato", "hilo", "avance_reportado"], [i + (AVANCE.get(i[2], ""),) for i in INDICADORES])
    escribir("kpis.csv", ["codigo", "nivel", "nombre", "pregunta", "formula", "fuente", "frecuencia", "desagregacion", "advertencias", "estado", "donde"], KPIS)
    escribir("kpis_descartados.csv", ["nombre", "razon"], DESCARTADOS)
    escribir("hilo.csv", ["serie", "etiqueta", "plan_id", "tipo", "ambito", "poblacion", "criterio", "puntos", "fuente", "url", "nota"], HILO)
    escribir("hallazgos.csv", ["id", "ambito", "tipo", "titulo", "observamos", "por_que", "pregunta", "fuentes"], HALLAZGOS)
    print("piloto:", len(OBJETIVOS), "objetivos,", len(INDICADORES), "indicadores,", len(HILO), "series,", len(HALLAZGOS), "hallazgos")
