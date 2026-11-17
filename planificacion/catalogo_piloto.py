"""Piloto de la vitrina con indicadores y de los hilos (anemia infantil, pobreza monetaria y empleo adecuado).

Regiones piloto: Cajamarca, Piura y Puno. Escribe en catalogo/: objetivos.csv, indicadores.csv, hilo.csv,
hilos.csv, hilo_pendientes.csv, hallazgos.csv y las fichas de KPI. Solo fuentes oficiales.
Consulta: 16/11/2026 (anemia y Cajamarca) y 17/11/2026 (pobreza y empleo).
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

# Fuentes de los hilos de pobreza y empleo (consulta: 17/11/2026)
INEI_PERFIL = "https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1106/cap03.pdf"
INEI_POB2020 = "https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/pobreza2020/Pobreza2020.pdf"
INEI_NUEVA_MET = "https://proyectos.inei.gob.pe/iinei/srienaho/Descarga/DocumentosMetodologicos/2004-55/Informe-Tecnico-Pobreza.pdf"
INEI_NOTA_2024 = "https://cdna.www.gob.pe/en/institucion/inei/noticias/1164173-pobreza-monetaria-afecto-al-27-6-de-la-poblacion-del-pais-en-el-ano-2024"
PNDIS_2030 = "https://cdn.www.gob.pe/uploads/document/file/4090334/PNDIS%20al%202030.pdf.pdf"
CONGRESO_IND = "https://www3.congreso.gob.pe/Docs/DGP/GestionInformacionEstadistica/files/carp-geo-2026/ago-26-indicadores-estadisticos-senado.pdf"
BICENTENARIO = "https://cdn.www.gob.pe/uploads/document/file/6787686/5879883-el-plan-bicentenario-el-peru-hacia-el-2021.pdf"
PEDN_METAS = "https://peru2050.ceplan.gob.pe/metas/"
INEI_EMPLEO_0412 = "https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1105/libro.pdf"

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
    I("OER.06", "IND.01.OER.06", "PEA ocupada adecuadamente empleada", "", 2021, 37.8, "2023=34.34;2024=34.99", "2023=31.35;2024=31.98", "%", "", "empleo"),
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

# Hilos. Cada fila: hilo, serie, etiqueta, plan_id, tipo (meta | medido | meta-otra), ámbito, población, criterio, puntos, fuente, url, nota
HILO = [
    ("anemia", "pedn", "PEDN al 2050", "pedn", "meta", "Perú", "6 a 35 meses", "Fijada antes del cambio de criterio de 2024", "2021=38.8;2026=30;2030=22;2040=21;2050=20",
     "PEDN al 2050, indicadores (CEPLAN), AE 1.2.3", PEDN_IND, "Copia del documento oficial; falta enlazar la de CEPLAN. La RPCD 046-2026/CEPLAN/PCD modificó 26 fichas: por verificar si esta fue una."),
    ("anemia", "pndis", "Política de Desarrollo e Inclusión Social", "pn-40", "meta", "Perú", "6 a 35 meses", "Fijada antes del cambio de criterio de 2024", "2021=38.8;2024=36.8;2030=32.3",
     "Reporte de cumplimiento 2024 de la PNDIS (MIDIS), indicador IOP.01.02", PNDIS_REP, "Valor 2024 reportado: 43,7 %."),
    ("anemia", "pmanemia", "Plan Multisectorial contra la Anemia 2024-2030", "", "meta", "Perú", "menores de 36 meses", "", "2030=37.2",
     "Observatorio Nacional de Prospectiva (CEPLAN), ficha T13", PMA, "Norma de aprobación del plan por confirmar."),
    ("anemia", "pnmnna", "Política de Niñas, Niños y Adolescentes", "pn-38", "meta", "Perú", "6 a 35 meses", "", "2024=38.9",
     "Reporte de cumplimiento 2024 de la PNMNNA (MIMP), indicador IOP.01.03", PNMNNA_REP, "Solo ubicamos la meta 2024; valor 2024 reportado: 43,7 %."),
    ("anemia", "endes-363", "ENDES · criterio anterior", "", "medido", "Perú", "6 a 35 meses", "RM 363-2022-MINSA", "2019=40.1;2020=40;2021=38.8;2022=42.4;2023=43.1;2024=43.7",
     "INEI, Indicadores de resultados de los programas presupuestales, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("anemia", "endes-251", "ENDES · criterio OMS 2024", "", "medido", "Perú", "6 a 35 meses", "RM 251-2024-MINSA", "2019=31.4;2020=30.4;2021=28.4;2022=33.5;2023=34.6;2024=35.3",
     "INEI, Indicadores de resultados de los programas presupuestales, ENDES 2024, cuadro 06.1A", ENDES_PPR, "El INEI usa este criterio en su nota de prensa de la ENDES 2024."),
    ("anemia", "caj-363", "ENDES · criterio anterior", CAJ, "medido", "Cajamarca", "6 a 35 meses", "RM 363-2022-MINSA", "2019=28.7;2020=33.8;2021=32.9;2022=38.2;2023=34.9;2024=38.4", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("anemia", "caj-251", "ENDES · criterio OMS 2024", CAJ, "medido", "Cajamarca", "6 a 35 meses", "RM 251-2024-MINSA", "2019=31.7;2020=36.8;2021=32.3;2022=35.7;2023=32.5;2024=40.6", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),
    ("anemia", "caj-pdrc", "Meta del PDRC (6 a 59 meses)", CAJ, "meta-otra", "Cajamarca", "6 a 59 meses", "Fuente no indicada", "2021=20;2023=18.3;2024=17.4",
     "Informe de evaluación del PDRC Cajamarca, periodos 2023-2024 (oct 2025)", EVAL_CAJ, "Valores reportados por el propio informe: 25,8 % (2023) y 27,6 % (2024). Otro grupo de edad: no se compara con las líneas de ENDES."),
    ("anemia", "piu-363", "ENDES · criterio anterior", "pdrc-19", "medido", "Piura", "6 a 35 meses", "RM 363-2022-MINSA", "2019=43.8;2020=43.2;2021=36.7;2022=38;2023=39.7;2024=42.4", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("anemia", "piu-251", "ENDES · criterio OMS 2024", "pdrc-19", "medido", "Piura", "6 a 35 meses", "RM 251-2024-MINSA", "2019=32.9;2020=34.1;2021=28.5;2022=28.9;2023=33.2;2024=35.4", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),
    ("anemia", "pun-363", "ENDES · criterio anterior", "pdrc-20", "medido", "Puno", "6 a 35 meses", "RM 363-2022-MINSA", "2019=69.9;2020=69.4;2021=70.4;2022=67.2;2023=70.4;2024=76", "INEI, ENDES 2024, cuadro 06A", ENDES_PPR, ""),
    ("anemia", "pun-251", "ENDES · criterio OMS 2024", "pdrc-20", "medido", "Puno", "6 a 35 meses", "RM 251-2024-MINSA", "2019=42.8;2020=38.8;2021=34;2022=39.2;2023=46.4;2024=53.1", "INEI, ENDES 2024, cuadro 06.1A", ENDES_PPR, ""),

    # ---- Hilo de pobreza monetaria (2004-2025). Una sola serie vigente del INEI, armada con sus ediciones oficiales:
    # 2004-2012 (Perfil de la pobreza 2004-2012), 2013-2020 (Evolución de la pobreza 2009-2020), 2021 (citado por la PNDIS al 2030)
    # y 2022-2025 (citado por el Congreso). Donde las ediciones se superponen (2009-2012), las cifras coinciden.
    ("pobreza", "pob-vigente", "INEI · metodología vigente", "", "medido", "Perú", "toda la población", "Vigente (canasta ENAHO 2010)",
     "2004=58.7;2005=55.6;2006=49.1;2007=42.4;2008=37.3;2009=33.5;2010=30.8;2011=27.8;2012=25.8;2013=23.9;2014=22.7;2015=21.8;2016=20.7;2017=21.7;2018=20.5;2019=20.2;2020=30.1;2021=25.9;2022=27.5;2023=29;2024=27.6;2025=25.7",
     "INEI, Perfil de la pobreza 2004-2012 (gráfico 3.1); Evolución de la pobreza monetaria 2009-2020 (cuadro 3.1); PNDIS al 2030 (2021, cita a la ENAHO); Congreso, indicadores estadísticos, ago 2026 (2022-2025, cita al INEI)", INEI_POB2020,
     "2020: encuesta por teléfono durante el confinamiento, con cuestionario reducido (INEI). Falta enlazar como fuente directa el informe técnico del INEI 2016-2025."),
    ("pobreza", "pob-anterior", "INEI · metodología anterior", "", "medido", "Perú", "toda la población", "Anterior (canasta ENAHO 1997, Censo 1993)",
     "2004=48.6;2009=34.8;2010=31.3",
     "INEI, Evolución de la pobreza 2004-2010. Nueva metodología (gráfico 4)", INEI_NUEVA_MET,
     "Solo los años que el INEI publica para comparar ambas metodologías."),
    ("pobreza", "bic-pobreza", "Plan Bicentenario (serie anterior)", "", "meta-otra", "Perú", "toda la población", "Línea de base con la metodología anterior",
     "2009=34.8;2021=10",
     "Plan Bicentenario: el Perú hacia el 2021 (DS 054-2011-PCM), objetivo nacional A, objetivo específico 4, p. 52", BICENTENARIO,
     "Meta: menos de 10 % al 2021. La tabla no indica el año de la línea de base; el texto y el gráfico 1.7 la ubican en 2009."),
    ("pobreza", "pedn-pobreza", "PEDN al 2050", "pedn", "meta", "Perú", "toda la población", "",
     "2050=3",
     "CEPLAN, Perú 2050: metas del PEDN", PEDN_METAS,
     "Solo ubicamos la meta al 2050; la línea de base y las metas intermedias están por catalogar."),
    ("pobreza", "ext-vigente", "INEI · metodología vigente", "", "medido", "Perú", "toda la población", "Vigente (canasta ENAHO 2010)",
     "2004=16.4;2005=15.8;2006=13.8;2007=11.2;2008=10.9;2009=9.5;2010=7.6;2011=6.3;2012=6;2013=4.7;2014=4.3;2015=4.1;2016=3.8;2017=3.8;2018=2.8;2019=2.9;2020=5.1;2021=;2022=5;2023=5.7;2024=5.5;2025=4.7",
     "INEI, Perfil de la pobreza 2004-2012 (gráfico 3.4); Evolución de la pobreza monetaria 2009-2020 (gráfico 3.5); Congreso, ago 2026 (2022-2025, cita al INEI)", INEI_POB2020,
     "2021 sin dato: la PNDIS cita 2,1 %, cifra por cotejar con el informe técnico del INEI."),
    ("pobreza", "bic-extrema", "Plan Bicentenario (serie anterior)", "", "meta-otra", "Perú", "toda la población", "Línea de base con la metodología anterior",
     "2008=12.6;2021=5",
     "Plan Bicentenario (DS 054-2011-PCM), objetivo específico 4, p. 52", BICENTENARIO,
     "La tabla no indica el año: el gráfico 1.7 del plan ubica 12,6 % en 2008, y el texto da 11,5 % para 2009."),
    # ---- Hilo de empleo adecuado
    ("empleo", "emp-inei", "INEI · empleo adecuado", "", "medido", "Perú", "población ocupada", "INEI (ENAHO)",
     "2004=22.2;2005=21.3;2006=27.4;2007=32.7;2008=36.9;2009=40;2010=42.3;2011=44.8;2012=48.1",
     "INEI, Evolución de los indicadores de empleo e ingreso por departamento 2004-2012 (resumen ejecutivo, p. 20)", INEI_EMPLEO_0412,
     "Serie 2013-2025 por enlazar. El INEI rotula la base como población ocupada en el gráfico y como PEA en el texto."),
    ("empleo", "bic-adecuado", "Plan Bicentenario (MTPE-ENAHO)", "", "meta-otra", "Perú", "PEA total", "MTPE-ENAHO: PEA empleada adecuadamente ÷ PEA total",
     "2009=51.6;2021=75",
     "Plan Bicentenario (DS 054-2011-PCM), eje 4, objetivo específico 5, indicador 16, p. 177", BICENTENARIO,
     "Otra medición que la del INEI para el mismo año: no se compara con la línea del INEI."),
    ("empleo", "caj-emp-meta", "Meta del PDRC", CAJ, "meta-otra", "Cajamarca", "PEA ocupada", "Fuente no indicada",
     "2021=37.8;2023=34.34;2024=34.99",
     "Informe de evaluación del PDRC Cajamarca, periodos 2023-2024 (oct 2025), IND.01.OER.06", EVAL_CAJ, ""),
    ("empleo", "caj-emp-rep", "Reportado por el gobierno regional", CAJ, "medido", "Cajamarca", "PEA ocupada", "Reportado por la entidad",
     "2023=31.35;2024=31.98",
     "Informe de evaluación del PDRC Cajamarca, periodos 2023-2024 (oct 2025), IND.01.OER.06", EVAL_CAJ, "Valor que reporta el propio gobierno regional."),
]

# Hallazgos: id, ámbito (hilo:<id> o plan_id), tipo, título, observamos, por qué puede pasar, pregunta abierta, fuentes "título|url;;título|url"
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

    ("h-bic-serie", "hilo:pobreza", "medicion", "La meta de pobreza del Plan Bicentenario se fijó con una serie que el INEI reemplazó",
     "El Plan Bicentenario (DS 054-2011-PCM) fijó para 2021 una pobreza menor al 10 % y una pobreza extrema de 5 %, con líneas de base de 34,8 % y 12,6 % (fuente INEI). Esas cifras son de la metodología anterior del INEI. Con la metodología vigente, el INEI recalculó la pobreza de 2009 en 33,5 % y la de 2004 pasó de 48,6 % a 58,7 %. Con la serie vigente, la pobreza fue 20,2 % en 2019 y 25,9 % en 2021. En el propio plan, la base de la pobreza extrema (12,6 %) corresponde a 2008 según su gráfico, mientras el texto da 11,5 % para 2009.",
     "El INEI actualizó su metodología: la canasta pasó a basarse en la ENAHO 2010 en lugar de la de 1997, y las proyecciones de población, en el Censo 2007 en lugar del de 1993. El plan se formuló con las cifras oficiales de entonces. No ubicamos una versión aprobada del plan que reexpresara sus metas con la nueva serie. Por eso el museo no calcula la distancia entre la meta y el resultado: no miden con la misma serie (regla 4 del método).",
     "¿Con qué serie se evaluó la meta de pobreza del Plan Bicentenario? Cuando cambia la forma de medir, ¿quién debe reexpresar las metas vigentes, y cómo se hará con las del PEDN al 2050?",
     "Plan Bicentenario, p. 52|" + BICENTENARIO + ";;INEI, Evolución de la pobreza 2004-2010. Nueva metodología|" + INEI_NUEVA_MET + ";;INEI, Evolución de la pobreza monetaria 2009-2020|" + INEI_POB2020 + ";;PNDIS al 2030 (pobreza 2021)|" + PNDIS_2030),
    ("h-bic-empleo", "hilo:empleo", "medicion", "Dos cifras de empleo adecuado para el mismo año",
     "El Plan Bicentenario midió el empleo adecuado de 2009 en 51,6 % (fuente MTPE-ENAHO, PEA empleada adecuadamente entre PEA total) y fijó una meta de 75 % para 2021. Para el mismo año, el INEI publica una tasa de empleo adecuado de 40,0 %. El plan también fijó una meta de trabajo asalariado de 60 % para 2021, desde una base de 42,7 %.",
     "Las dos cifras salen de la ENAHO, pero pueden usar distinta definición de empleo adecuado (umbral de ingresos u horas), distinto ámbito o distinta base. El plan no publica la ficha técnica del indicador. Por eso el museo no compara la meta con la serie del INEI.",
     "¿Qué definición de empleo adecuado usó el Plan Bicentenario y con qué serie se evaluó? ¿Usan la misma la Política Nacional de Empleo Decente y los planes regionales?",
     "Plan Bicentenario, p. 177|" + BICENTENARIO + ";;INEI, Evolución de los indicadores de empleo e ingreso por departamento 2004-2012|" + INEI_EMPLEO_0412),
    ("h-caj-empleo", "hilo:empleo", "meta-base", "Cajamarca fijó metas de empleo adecuado por debajo de su línea de base",
     "El PDRC Cajamarca al 2033 sigue la PEA ocupada adecuadamente empleada. Su línea de base es 37,8 % (2021) y sus metas son 34,34 % (2023) y 34,99 % (2024), es decir, menores que el punto de partida. El gobierno regional reporta 31,35 % y 31,98 %. El informe de evaluación no indica la fuente del dato.",
     "Una meta menor que la línea de base puede reflejar que se esperaba una caída tras 2021, o un cambio de fuente entre la línea de base y las metas. El informe no lo explica.",
     "¿Qué supuesto llevó a fijar metas menores que la línea de base? ¿De qué fuente sale el dato, y es comparable con el que publica el INEI para Cajamarca?",
     "Informe de evaluación del PDRC Cajamarca 2023-2024|" + EVAL_CAJ),
]


# Hilos: id, nombre, pregunta, texto de presentación, estado
HILOS = [
    ("anemia", "Anemia infantil", "¿Hablan el mismo idioma los planes sobre anemia infantil?",
     "Seguimos un mismo problema por todos los niveles de planificación: el PEDN, las políticas nacionales, un plan multisectorial y los planes regionales piloto (Cajamarca, Piura y Puno).", "piloto"),
    ("pobreza", "Pobreza monetaria", "¿Qué metas de pobreza se puso el Estado y con qué serie se miden?",
     "La serie oficial del INEI desde 2004, las metas del Plan Bicentenario (al 2021, ya vencido) y del PEDN al 2050. Las metas de las políticas nacionales y de los planes regionales están por catalogar.", "piloto"),
    ("empleo", "Empleo adecuado", "¿Qué metas de empleo se puso el Estado y miden lo mismo que el INEI?",
     "El empleo adecuado según el INEI, la meta del Plan Bicentenario y la del plan regional de Cajamarca. La informalidad y la Política Nacional de Empleo Decente están por catalogar.", "piloto"),
]

# Lo que falta en cada hilo, a la vista: hilo, pieza, qué falta, estado
PENDIENTES = [
    ("pobreza", "INEI, informe técnico 2016-2025", "Enlazarlo como fuente directa de 2021-2025 (hoy: la PNDIS para 2021 y el Congreso para 2022-2025, ambos citando al INEI)", "Por cotejar"),
    ("pobreza", "Pobreza extrema 2021", "La PNDIS cita 2,1 %; cotejar con el informe técnico del INEI antes de graficarla", "Por cotejar"),
    ("pobreza", "PEDN al 2050", "Línea de base y metas intermedias de pobreza monetaria (solo ubicamos la meta de 3 % al 2050)", "Por catalogar"),
    ("pobreza", "Política de Desarrollo e Inclusión Social al 2030", "Indicadores y metas de pobreza (fichas en la sección 6.2 y el anexo 7 del documento)", "Por catalogar"),
    ("pobreza", "Acuerdo Nacional, Política de Estado 10", "Indicador de pobreza en su reporte de seguimiento", "Por catalogar"),
    ("pobreza", "PDRC Cajamarca", "No tiene indicador de pobreza entre los 19 de su informe de evaluación 2023-2024", "Revisado"),
    ("pobreza", "PDRC Piura y Puno", "Indicador de pobreza, si lo tienen", "Por catalogar"),
    ("pobreza", "Plan Bicentenario", "Informe de evaluación final de CEPLAN, si existe", "Por ubicar"),
    ("pobreza", "Grupos de departamentos", "Grupos estadísticamente semejantes del INEI, con sus intervalos, en lugar de cifras sueltas por departamento", "Por catalogar"),
    ("pobreza", "Pobreza urbana y rural, vulnerabilidad", "Series 2004-2025 del INEI", "Por enlazar"),
    ("empleo", "INEI, empleo adecuado 2013-2025", "Serie nacional y de Cajamarca (Evolución de los indicadores de empleo e ingreso por departamento)", "Por enlazar"),
    ("empleo", "Informalidad", "El INEI publica más de una medición (encuesta de empleo nacional y cuenta satélite de la economía informal); se explican juntas, con una persona de estadística", "Por catalogar"),
    ("empleo", "Política Nacional de Empleo Decente (DS 013-2021-TR)", "Indicadores, metas y reporte de cumplimiento", "Por catalogar"),
    ("empleo", "PEDN al 2050", "Metas de desempleo (menos de 5 %) y empleo formal (duplicarlo) al 2050: líneas de base por catalogar", "Por catalogar"),
    ("empleo", "Plan Bicentenario, trabajo asalariado", "Meta de 60 % al 2021 (base 42,7 %): falta la serie oficial para mostrarla", "Por enlazar"),
    ("empleo", "Planilla electrónica (MTPE)", "Contraste del empleo formal registrado con la ENAHO", "Por catalogar"),
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
    escribir("hilo.csv", ["hilo", "serie", "etiqueta", "plan_id", "tipo", "ambito", "poblacion", "criterio", "puntos", "fuente", "url", "nota"], HILO)
    escribir("hilos.csv", ["id", "nombre", "pregunta", "texto", "estado"], HILOS)
    escribir("hilo_pendientes.csv", ["hilo", "pieza", "falta", "estado"], PENDIENTES)
    escribir("hallazgos.csv", ["id", "ambito", "tipo", "titulo", "observamos", "por_que", "pregunta", "fuentes"], HALLAZGOS)
    print("piloto:", len(OBJETIVOS), "objetivos,", len(INDICADORES), "indicadores,", len(HILO), "series en", len(HILOS), "hilos,", len(HALLAZGOS), "hallazgos,", len(PENDIENTES), "pendientes")
