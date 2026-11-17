"""Genera index.html del Museo de la planificación desde los CSV de catalogo/ y el mapa de geo/mapa.json.

Uso: python3 catalogo_fuente.py && python3 catalogo_piloto.py && python3 build.py [--salida carpeta] [--repo URL]
La página queda legible sin JavaScript: contadores, leyenda y tabla se escriben en el HTML.
"""
import csv, json, os, html, re, datetime
from collections import defaultdict
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(BASE, "catalogo")
MAPA = os.path.join(BASE, "geo", "mapa.json")
CORTE = date(2026, 11, 16)
CORTE_TXT = CORTE.strftime("%d/%m/%Y")
CEPAL_PERU = "https://observatorioplanificacion.cepal.org/es/paises/?country=per"

ESTADOS = {
    "ubicado": ["Ubicado", "e-ubicado", "El reporte existe y está enlazado."],
    "noubicado": ["No ubicado al " + CORTE_TXT, "e-noubicado", "No lo encontramos a la fecha de corte. Puede existir: cualquiera puede aportar el enlace."],
    "noexigido": ["No exigido aún", "e-noexigido", "El plan es reciente y todavía no le toca reportar."],
    "fuera": ["Fuera de plazo", "e-fuera", "Venció el plazo que fija la norma y no hay reporte ubicado."],
    "noaplica": ["No aplica", "e-noaplica", "Visión o acuerdo de largo plazo, sin reporte propio."],
    "porrevisar": ["Por revisar", "e-porrevisar", "Todavía no lo buscamos."],
}
DIMS = ["Indicadores y metas", "Plan de implementación", "Seguimiento publicado", "Evaluación publicada", "Articulación declarada"]
NIVELES = {
    "sectorial": ["", "Políticas nacionales y planes multisectoriales", "Plan sectorial (PESEM)", "Planes institucionales de los ministerios (PEI y POI)"],
    "territorial": ["", "Planes regionales (PDRC)", "Planes provinciales (PDLC)", "Planes distritales (PDLC)", "Planes institucionales subnacionales (PEI y POI)"],
}
DEP = {  # nombre en catálogo -> nombre en el mapa
    "Amazonas": "AMAZONAS", "Áncash": "ANCASH", "Apurímac": "APURIMAC", "Arequipa": "AREQUIPA", "Ayacucho": "AYACUCHO",
    "Cajamarca": "CAJAMARCA", "Callao": "CALLAO", "Cusco": "CUSCO", "Huancavelica": "HUANCAVELICA", "Huánuco": "HUANUCO",
    "Ica": "ICA", "Junín": "JUNIN", "La Libertad": "LA LIBERTAD", "Lambayeque": "LAMBAYEQUE", "Lima (región)": "LIMA",
    "Loreto": "LORETO", "Madre de Dios": "MADRE DE DIOS", "Moquegua": "MOQUEGUA", "Pasco": "PASCO", "Piura": "PIURA",
    "Puno": "PUNO", "San Martín": "SAN MARTIN", "Tacna": "TACNA", "Tumbes": "TUMBES", "Ucayali": "UCAYALI", "Lima Metropolitana": "_MML",
}


def leer(n):
    with open(os.path.join(CAT, n), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def temporalidad(p):
    ini, fin = p["horizonte_inicio"], p["horizonte_fin"]
    if not ini and fin:
        return f"Hasta {fin} · inicio por verificar"
    if not ini:
        return "Por catalogar"
    if not fin:
        return "Largo plazo · sin horizonte fijo" if p["id"] == "an" else "Horizonte por verificar"
    a = int(fin) - int(ini)
    return ("Corto plazo" if a <= 3 else "Mediano plazo" if a <= 6 else "Largo plazo") + f" · {a} años"


def vigencia(p):
    if p["catalogado"] != "si":
        return "Por catalogar"
    if p["horizonte_fin"] and int(p["horizonte_fin"]) < CORTE.year:
        return "Horizonte vencido"
    return "Vigente"


def generacion(p):
    """Solo para planes territoriales: nuevo (formulado desde 2022), ampliado (plan antiguo con horizonte extendido) o vencido."""
    if p["eje"] != "territorial":
        return ""
    if vigencia(p) == "Horizonte vencido":
        return "vencido"
    ini = int(p["horizonte_inicio"]) if p["horizonte_inicio"] else 9999
    return "ampliado" if ini <= 2016 else "nuevo"


def main(salida=None, repo="https://github.com/qhawana-peru/observatorios"):
    """Escribe <salida>/index.html (por defecto, junto a este archivo) y copia los CSV a <salida>/datos/."""
    planes = leer("planes.csv")
    rel = {k: defaultdict(list) for k in ["versiones", "articulacion", "reportes", "dimensiones", "notas", "fuentes", "multisectorial"]}
    for k in rel:
        for r in leer(k + ".csv"):
            rel[k][r["plan_id"]].append(r)
    nec_de = {r["plan_id"]: r["necesidad"] for r in leer("necesidad_plan.csv")}
    sectores = [{"cod": r["codigo"], "abr": r["abreviatura"], "nombre": r["nombre"]} for r in leer("sectores.csv")]
    notas_nec = defaultdict(list)
    for r in leer("notas_necesidad.csv"):
        notas_nec[r["necesidad"]].append({"tipo": r["tipo"], "texto": r["texto"]})

    puntos = lambda s: [{"a": int(k), "v": (float(v) if v != "" else None)} for k, v in (x.split("=") for x in s.split(";") if x)]
    inds = defaultdict(list)
    for r in leer("indicadores.csv"):
        inds[(r["plan_id"], r["objetivo"])].append({"cod": r["codigo"], "nombre": r["indicador"], "pob": r["poblacion"], "lb": {"a": int(r["lb_anio"]), "v": float(r["lb_valor"])},
                                                    "metas": puntos(r["metas"]), "obt": puntos(r["obtenidos"]), "unidad": r["unidad"], "fuente": r["fuente_dato"], "hilo": r["hilo"],
                                                    "avance": float(r["avance_reportado"]) if r["avance_reportado"] else None})
    objetivos = defaultdict(list)
    for r in leer("objetivos.csv"):
        objetivos[r["plan_id"]].append({"cod": r["codigo"], "enun": r["enunciado"], "on": r["objetivo_nacional"], "url": r["evidencia_url"], "ind": inds[(r["plan_id"], r["codigo"])]})
    hilo = [dict(r, puntos=puntos(r["puntos"])) for r in leer("hilo.csv")]
    hilos = leer("hilos.csv")
    pendientes = leer("hilo_pendientes.csv")
    hallazgos = [dict(r, fuentes=[dict(zip(("t", "u"), f.split("|", 1))) for f in r["fuentes"].split(";;") if f]) for r in leer("hallazgos.csv")]

    piezas = []
    for p in planes:
        pid = p["id"]
        bit = rel["reportes"][pid]
        estado = "ubicado" if any(b["estado"] == "ubicado" for b in bit) and bit[-1]["estado"] != "noubicado" else (bit[-1]["estado"] if bit else "porrevisar")
        corto = re.sub(r"^La Lectura", "Lectura", p["corto"])
        piezas.append({
            "id": pid, "eje": p["eje"], "sector": p["sector"], "region": p["region"], "nivel": int(p["nivel"]),
            "necesidad": nec_de.get(pid, ""), "tipo": p["tipo"], "corto": corto, "nombre": p["nombre"],
            "actores": p["actores"], "norma": p["norma"], "resumen": p["resumen"], "catalogado": p["catalogado"] == "si",
            "horizonte": (f'{p["horizonte_inicio"]}–{p["horizonte_fin"]}' if p["horizonte_fin"] else f'desde {p["horizonte_inicio"]} · fin por verificar') if p["horizonte_inicio"] else (f'hasta {p["horizonte_fin"]} · inicio por verificar' if p["horizonte_fin"] else "Por catalogar"),
            "generacion": generacion(p), "norma_pendiente": "por confirmar" in p["norma"].lower(),
            "temporalidad": temporalidad(p), "vigencia": vigencia(p),
            "articula": [{"sup": a["plan_superior"], "base": a["base"], "url": a["evidencia_url"]} for a in rel["articulacion"][pid]],
            "versiones": rel["versiones"][pid], "bitacora": bit,
            "dims": {d["dimension"]: {"valor": d["valor"], "url": d["evidencia_url"]} for d in rel["dimensiones"][pid]},
            "notas": rel["notas"][pid], "fuentes": rel["fuentes"][pid], "estado": estado,
            "multi": [{"sector": m["sector"], "rol": m["rol"], "url": m["evidencia_url"]} for m in rel["multisectorial"][pid]],
            "dep": DEP.get(p["region"], ""), "objetivos": objetivos[pid],
        })
    necesidades = [{"cod": r["codigo"], "nombre": r["nombre"], "desc": r["descripcion"], "notas": notas_nec[r["codigo"]]} for r in leer("necesidades.csv")]

    # Contadores (también visibles sin JavaScript)
    cat = [p for p in piezas if p["catalogado"]]
    pn = [p for p in piezas if p["id"].startswith("pn-") or p["id"] == "pnms"]
    reportes = [b for p in piezas for b in p["bitacora"]]
    sect_con = len({p["sector"] for p in piezas if p["eje"] == "sectorial" and p["nivel"] >= 2})
    reg_cat = sum(1 for p in piezas if p["eje"] == "territorial" and p["catalogado"])
    cont = [
        (len([p for p in cat if p["eje"] == "principal"]), "planes de país"),
        (len(pn), "políticas nacionales (lista de CEPLAN a jun 2024)"),
        (f"{sect_con} de {len(sectores)}", "sectores con PESEM y PEI catalogados"),
        (f"{reg_cat} de 26", "planes regionales ubicados"),
        (sum(1 for b in reportes if b["estado"] == "ubicado"), "reportes de seguimiento ubicados"),
        (sum(1 for p in cat if p["vigencia"] == "Horizonte vencido"), "con horizonte vencido"),
    ]
    cont_html = "".join(f'<div class="cont"><b>{v}</b><span>{html.escape(t)}</span></div>' for v, t in cont)
    cont_html += f'<div class="cont corte"><b>Corte {CORTE_TXT}</b><span>fuentes oficiales consultadas ese día</span></div>'

    pill = lambda e: f'<span class="estado {ESTADOS[e][1]}" title="{html.escape(ESTADOS[e][2])}">{html.escape(ESTADOS[e][0])}</span>'
    leyenda = "<span>Seguimiento:</span>" + "".join(pill(k) for k in ESTADOS)

    por_id = {p["id"]: p for p in piezas}
    nombre_nec = {n["cod"]: n["nombre"] for n in necesidades}
    eje_txt = {"principal": "Atrio · planes de país", "sectorial": "Ala sectorial", "territorial": "Ala territorial"}
    filas = []
    for p in piezas:
        art = ", ".join(por_id[a["sup"]]["corto"] + (" (según la norma)" if a["base"] == "norma" else "") for a in p["articula"]) or "—"
        donde = eje_txt[p["eje"]] + (" · " + nombre_nec[p["necesidad"]] if p["necesidad"] else "") + (" · " + p["region"] if p["region"] else "")
        filas.append(
            f'<tr><td>{html.escape(donde)}</td><td>{html.escape(p["nombre"])}</td><td>{html.escape(p["actores"])}</td>'
            f'<td><span class="norma">{html.escape(p["norma"])}</span></td><td>{html.escape(p["vigencia"])}<br><span class="vacio">{html.escape(p["temporalidad"])}</span></td>'
            f'<td>{html.escape(art)}</td><td>{pill(p["estado"])}</td></tr>')
    tabla = ('<table><caption>Catálogo completo · corte ' + CORTE_TXT + '</caption><thead><tr><th>Dónde está</th><th>Pieza</th><th>Actores</th>'
             '<th>Norma</th><th>Vigencia</th><th>Se articula con</th><th>Seguimiento</th></tr></thead><tbody>' + "".join(filas) + "</tbody></table>")

    # ---------- KPI ----------
    fichas = leer("kpis.csv"); descart = leer("kpis_descartados.csv")
    pdrc = [p for p in piezas if p["eje"] == "territorial"]
    vig = [p for p in pdrc if p["generacion"] in ("nuevo", "ampliado")]
    grupos = [("Planes de país", [p for p in piezas if p["eje"] == "principal"]),
              ("Políticas nacionales", [p for p in piezas if p["id"].startswith("pn-") or p["id"] == "pnms"]),
              ("Planes del sector Salud (PEM, PESEM, PEI)", [p for p in piezas if p["id"] in ("pem-pnms", "pesem-salud", "pei-minsa")]),
              ("Planes regionales (PDRC)", pdrc)]
    con_rep = lambda ps: sum(1 for p in ps if any(b["estado"] == "ubicado" for b in p["bitacora"]))
    fechas = [f["fecha_consulta"] for p in piezas for f in p["fuentes"] if f.get("fecha_consulta")]
    dias = max((datetime.date(2026, 11, 16) - datetime.date.fromisoformat(f)).days for f in fechas) if fechas else None
    valor = {
        "S1": (f"{len(vig)} de {len(pdrc)}", "planes regionales con horizonte vigente y fuente oficial enlazada"),
        "S2": (str(sum(1 for p in piezas if p["vigencia"] == "Horizonte vencido")), "planes del catálogo con horizonte vencido y sin reemplazo ubicado"),
        "S3": (f"{sum(1 for p in vig if p['generacion'] == 'ampliado')} de {len(vig)}", "planes regionales vigentes que son planes antiguos ampliados"),
        "G1": (f"{sum(con_rep(ps) for _, ps in grupos)} de {sum(len(ps) for _, ps in grupos)}", "planes con al menos un reporte de seguimiento o evaluación ubicado",
               [(n, con_rep(ps), len(ps)) for n, ps in grupos]),
        "O1": (f"{sum(1 for p in piezas if p['fuentes'])} de {len(piezas)}", "piezas con al menos una fuente oficial enlazada"),
        "O2": (f"{dias} días" if dias is not None else "—", f"antigüedad máxima de la verificación al corte {CORTE_TXT}"),
    }
    # Piloto por plan
    for p in piezas:
        ind = [i for o in p["objetivos"] for i in o["ind"]]
        if not ind:
            p["kpi"] = {}
            continue
        con = [i for i in ind if i["obt"] and i["obt"][-1]["v"] is not None]
        p["kpi"] = {"D1": [sum(1 for i in ind if i["lb"]["v"] is not None and i["lb"]["a"]), len(ind)],
                    "D2": [sum(1 for i in ind if i["fuente"]), len(ind)],
                    "A1": [sum(1 for o in p["objetivos"] if o["on"]), len(p["objetivos"])],
                    "G3": [len(con), len(ind)],
                    "G4": [sum(1 for i in con if (i["avance"] or 0) >= 100), len(con)]}
    # Hilos. Anemia: A4 y D4 como en la v7. Pobreza y empleo: solo lo que la regla 4 permite (sin restar series distintas).
    anemia = [s for s in hilo if s["hilo"] == "anemia"]
    metas_nac = [s for s in anemia if s["ambito"] == "Perú" and s["tipo"] == "meta"]
    m2030 = [pt["v"] for s in metas_nac for pt in s["puntos"] if pt["a"] == 2030]
    ritmo = []
    for s in metas_nac:
        pts = s["puntos"]
        if len(pts) > 1 and any(pt["a"] == 2030 for pt in pts):
            lb, m = pts[0], next(pt for pt in pts if pt["a"] == 2030)
            ritmo.append({"serie": s["etiqueta"], "exigido": round((lb["v"] - m["v"]) / (m["a"] - lb["a"]), 2)})
    obs = {}
    for s in anemia:
        if s["ambito"] == "Perú" and s["tipo"] == "medido":
            p0, p1 = s["puntos"][-6], s["puntos"][-1]
            obs[s["criterio"]] = round((p1["v"] - p0["v"]) / (p1["a"] - p0["a"]), 2)
    serie = lambda sid: next(s for s in hilo if s["serie"] == sid)
    valor_en = lambda sid, a: next((pt["v"] for pt in serie(sid)["puntos"] if pt["a"] == a), None)
    ult = lambda sid: [pt for pt in serie(sid)["puntos"] if pt["v"] is not None][-1]
    kpi_hilo = {"A4": {"n": len(metas_nac), "min2030": min(m2030), "max2030": max(m2030), "rango": round(max(m2030) - min(m2030), 1)},
                "D4": {"ritmo": ritmo, "observado": obs},
                "pobreza": {"meta_bic": valor_en("bic-pobreza", 2021), "lb_bic": valor_en("bic-pobreza", 2009),
                            "anterior_2009": valor_en("pob-anterior", 2009), "vigente_2009": valor_en("pob-vigente", 2009),
                            "v2019": valor_en("pob-vigente", 2019), "v2021": valor_en("pob-vigente", 2021), "ultimo": ult("pob-vigente"),
                            "meta_pedn_2050": valor_en("pedn-pobreza", 2050)},
                "empleo": {"bic_2009": valor_en("bic-adecuado", 2009), "inei_2009": valor_en("emp-inei", 2009), "meta_bic": valor_en("bic-adecuado", 2021)}}

    est_txt = {"activo": "Activo", "piloto": "Piloto", "revision": "En revisión", "etapa2": "Etapa 2"}
    tarjetas = "".join(f'<div class="kpi-c"><code>{k}</code><b>{html.escape(v[0])}</b><span>{html.escape(v[1])}</span></div>' for k, v in valor.items())
    g1 = "".join(f"<li>{html.escape(n)}: {a} de {t}</li>" for n, a, t in valor["G1"][2])
    def ficha_html(f):
        return (f'<details class="kpi-f" id="kpi-{f["codigo"]}"><summary><code>{f["codigo"]}</code> <b>{html.escape(f["nombre"])}</b> '
                f'<span class="est {f["estado"]}">{est_txt[f["estado"]]}</span></summary><dl>'
                f'<dt>Pregunta</dt><dd>{html.escape(f["pregunta"])}</dd><dt>Cálculo</dt><dd>{html.escape(f["formula"])}</dd>'
                f'<dt>Fuente</dt><dd>{html.escape(f["fuente"])}</dd><dt>Frecuencia</dt><dd>{html.escape(f["frecuencia"])}</dd>'
                f'<dt>Desagregación</dt><dd>{html.escape(f["desagregacion"])}</dd><dt>Advertencias de uso</dt><dd>{html.escape(f["advertencias"])}</dd>'
                + (f'<dt>Dónde se ve</dt><dd>{html.escape(f["donde"])}</dd>' if f["donde"] else "") + "</dl></details>")
    niveles_k = []
    for f in fichas:
        if f["nivel"] not in niveles_k: niveles_k.append(f["nivel"])
    metodo = ('<section class="metodo"><h2>Indicadores del museo · corte ' + CORTE_TXT + '</h2>'
              '<p>Miden el sistema de planificación, no califican entidades: se muestran como cifras y distribuciones, nunca como listas ordenadas. '
              'Cada indicador tiene su ficha. Los marcados como piloto se calculan solo donde ya hay datos (Cajamarca y los hilos).</p>'
              f'<div class="kpi-grid">{tarjetas}</div><p class="det-m">G1 por tipo de plan:</p><ul class="det-m">{g1}</ul>'
              '<h3>Fichas</h3>' + "".join(f'<h4>{html.escape(n)}</h4>' + "".join(ficha_html(f) for f in fichas if f["nivel"] == n) for n in niveles_k)
              + '<h3>Indicadores descartados</h3><ul>' + "".join(f'<li><b>{html.escape(d["nombre"])}.</b> {html.escape(d["razon"])}</li>' for d in descart) + '</ul></section>')
    tabla = metodo + tabla

    datos = {"corte": CORTE_TXT, "estados": ESTADOS, "piezas": piezas, "dimensiones": DIMS, "sectores": sectores,
             "necesidades": necesidades, "niveles": NIVELES, "mapa": json.load(open(MAPA)), "cepal": CEPAL_PERU, "hilo": hilo, "hilos": hilos, "pendientes": pendientes, "hallazgos": hallazgos, "kpiHilo": kpi_hilo, "kpiSis": {k: list(v[:2]) for k, v in valor.items()},
             "on": {"ON1": "Capacidades de las personas", "ON2": "Gestión sostenible del territorio", "ON3": "Competitividad y productividad", "ON4": "Sociedad justa y Estado efectivo"}}
    pl = open(os.path.join(BASE, "plantilla.html"), encoding="utf-8").read()
    out = (pl.replace("__CORTE__", CORTE_TXT).replace("__CONTADORES__", cont_html).replace("__LEYENDA__", leyenda)
             .replace("__TABLA__", tabla).replace("__REPO__", repo).replace("__DATOS__", json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")))
    salida = salida or BASE
    os.makedirs(os.path.join(salida, "datos"), exist_ok=True)
    open(os.path.join(salida, "index.html"), "w", encoding="utf-8").write(out)
    import shutil
    for n in sorted(os.listdir(CAT)):
        if n.endswith(".csv"):
            shutil.copy(os.path.join(CAT, n), os.path.join(salida, "datos", n))
    print("index.html:", len(piezas), "piezas;", cont)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida")
    ap.add_argument("--repo", default="https://github.com/qhawana-peru/observatorios")
    a = ap.parse_args()
    main(a.salida, a.repo)
