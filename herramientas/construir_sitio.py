"""Genera el sitio público de Qhawana: portada, Observatorio El Niño, Monitor de incendios, Museo de la planificación
y Observatorio del sistema de salud.

Uso:
    python herramientas/construir_sitio.py            # escribe _site/
    python herramientas/construir_sitio.py --salida carpeta

Lee:
  el-nino/datos/ejecucion_pp0068.csv   cortes validados del MEF
  el-nino/datos/hechos.csv             bitácora de pronósticos, decisiones y alertas
  el-nino/datos/emergencias.csv        emergencias del COEN-INDECI (piloto costa norte)
  el-nino/config/emergencias.json      alcance de esa tabla y declaratoria vigente
  el-nino/config/contexto.json         pronóstico por región y planes aprobados
  el-nino/datos/exposicion_cenepred.csv  población expuesta según los escenarios del CENEPRED
  el-nino/datos/riesgo_distritos_cenepred.csv  nivel de riesgo de cada distrito según el CENEPRED
  el-nino/datos/riesgo_lima_cenepred.csv       riesgo por manzana de Lima y Callao, sumado por distrito
  el-nino/config/riesgo.json           estudios del CENEPRED de la pestaña Riesgo
  el-nino/config/brechas.json          territorios de la sección de brechas (Lima y regiones críticas)
  el-nino/config/sitio.json            estado de publicación y dirección del repositorio
y escribe _site/el-nino/index.html con sus datos abiertos. Luego llama a sitio_incendios.py,
que escribe _site/incendios/ y la portada (_site/index.html).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from datetime import date, timedelta
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(RAIZ, "el-nino")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "setiembre", "octubre", "noviembre", "diciembre"]
CORTOS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "set", "oct", "nov", "dic"]
ACENTOS = {"Apurimac": "Apurímac", "Ancash": "Áncash", "Huanuco": "Huánuco", "Junin": "Junín",
           "San Martin": "San Martín"}


def titulo(n: str) -> str:
    n = n.title()
    for a, b in ((" De ", " de "), (" Del ", " del "), (" La ", " la ")):
        n = n.replace(a, b)
    return ACENTOS.get(n, n)


def etiqueta(fecha: str, largo=False) -> str:
    a, m, d = fecha.split("-")
    if largo:
        return f"{int(d)} de {MESES[int(m) - 1]} de {a}"
    return f"{int(d)} {CORTOS[int(m) - 1]} {a}"


def leer_csv(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def construir_datos() -> dict:
    filas = leer_csv(os.path.join(EN, "datos", "ejecucion_pp0068.csv"))
    por_fecha = defaultdict(list)
    for r in filas:
        for k in ("pim", "devengado"):
            r[k] = int(r[k])
        por_fecha[r["fecha_corte"]].append(r)
    fechas = sorted(por_fecha)
    corte = fechas[-1]
    ult = por_fecha[corte]

    def tabla(cod):
        return {r["codigo"]: r for r in ult if r["archivo"] == cod}

    d1, d2, d3, d4, d5 = (tabla(c) for c in ("D1", "D2", "D3", "D4", "D5"))
    niveles = {}
    pares = {"E": ("D6", "D7"), "M": ("D4", "D5"), "R": ("D2", "D3")}
    for n, (ca, cp) in pares.items():
        a = [r for r in ult if r["archivo"] == ca]
        p = [r for r in ult if r["archivo"] == cp]
        niveles[n] = {
            "t": [d1[n]["pim"], d1[n]["devengado"]],
            "a": [sum(r["pim"] for r in a), sum(r["devengado"] for r in a)],
            "p": [sum(r["pim"] for r in p), sum(r["devengado"] for r in p)],
        }
    muni = {}
    for cod, r in d4.items():
        p = d5.get(cod, {"pim": 0, "devengado": 0})
        muni[r["nombre"]] = [r["pim"] + p["pim"], r["devengado"] + p["devengado"], r["pim"], r["devengado"]]

    regiones = []
    for cod, a in sorted(d2.items()):
        p = d3.get(cod, {"pim": 0, "devengado": 0})
        nombre = a["nombre"]
        if cod == "465":
            region, rotulo, dep = "Lima Metropolitana", "Municipalidad Metropolitana de Lima", "LIMA"
        elif "CALLAO" in nombre:
            region, rotulo, dep = "Callao", "Gobierno Regional del Callao", "PROVINCIA CONSTITUCIONAL DEL CALLAO"
        else:
            dep = nombre.replace("GOBIERNO REGIONAL DEL DEPARTAMENTO DE ", "")
            region = titulo(dep)
            rotulo = "Gobierno Regional de " + region
        m = muni.get(dep, [0, 0, 0, 0])
        regiones.append({"c": cod, "r": region, "l": rotulo,
                         "t": [a["pim"] + p["pim"], a["devengado"] + p["devengado"]],
                         "a": [a["pim"], a["devengado"]], "p": [p["pim"], p["devengado"]], "m": m})

    serie = []
    for f in fechas:
        rs = por_fecha[f]
        tot = [r for r in rs if r["archivo"] == "D1"]
        act = [r for r in rs if r["tipo"] == "actividades"]
        pro = [r for r in rs if r["tipo"] == "proyectos"]
        P, D = sum(r["pim"] for r in tot), sum(r["devengado"] for r in tot)
        serie.append({"fecha": f, "etiqueta": etiqueta(f), "pim": P, "devengado": D,
                      "pct": round(D / P * 100, 1) if P else 0,
                      "pim_act": sum(r["pim"] for r in act), "dev_act": sum(r["devengado"] for r in act),
                      "pim_proy": sum(r["pim"] for r in pro), "dev_proy": sum(r["devengado"] for r in pro)})

    hechos = leer_csv(os.path.join(EN, "datos", "hechos.csv"))
    with open(os.path.join(EN, "config", "contexto.json"), encoding="utf-8") as f:
        contexto = json.load(f)
    with open(os.path.join(EN, "config", "sitio.json"), encoding="utf-8") as f:
        sitio = json.load(f)
    emergencias = construir_emergencias()
    avisos = construir_avisos()
    brechas = construir_brechas(ult, emergencias, avisos)
    return {"avisos": avisos, "riesgo": construir_riesgo(), "brechas": brechas, "corte": corte, "corte_corto": etiqueta(corte), "corte_largo": etiqueta(corte, True),
            "aprobado": sitio.get("estado") == "publicado", "niveles": niveles, "regiones": regiones,
            "serie": serie, "hechos": hechos, "emergencias": emergencias, "contexto": contexto, "_repo": sitio.get("repositorio", "#")}


def construir_riesgo() -> dict:
    """Zonas de riesgo por distrito (CENEPRED). Se envía compacto: una lista por distrito."""
    with open(os.path.join(EN, "config", "riesgo.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    n = lambda v: int(v) if v not in (None, "") else None
    dist = []
    for r in leer_csv(os.path.join(EN, "datos", "riesgo_distritos_cenepred.csv")):
        dist.append([r["ubigeo"], r["dep"], r["prov"], r["dist"], n(r["pob"]), n(r["a_inu"]), n(r["a_mm"]),
                     n(r["b_inu"]), n(r["b_pinu"]), n(r["b_mm"]), n(r["b_pmm"]), n(r["pc_inu"]) or 0, n(r["pc_mm"]) or 0])
    lima = [[r["ubigeo"], r["prov"], r["dist"]] + [int(r[k]) for k in
            ("pob_ma", "pob_a", "pob_m", "manz_ma", "ninos_0_5_ma", "mayores_65_ma", "eess_ma", "iiee_ma")]
            for r in leer_csv(os.path.join(EN, "datos", "riesgo_lima_cenepred.csv"))]
    return {"estudios": cfg["estudios"], "consultado": cfg["consultado"], "consultado_largo": etiqueta(cfg["consultado"], True),
            "dist": dist, "lima": lima}


def construir_emergencias() -> dict:
    with open(os.path.join(EN, "config", "emergencias.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    filas = leer_csv(os.path.join(EN, "datos", "emergencias.csv"))
    campos = ["personas_damnificadas", "personas_afectadas", "viviendas_inhabitables", "viviendas_afectadas",
              "iiee_afectadas", "eess_afectados", "vias_afectadas_km"]
    eventos = []
    for r in filas:
        if r["incluido"] != "si":
            continue
        e = {k: r[k] for k in ("id", "region", "provincia", "distritos", "fecha_ocurrencia", "evento", "reporte",
                               "reporte_version", "fecha_reporte", "otros_danos", "evaluacion", "nota", "fuente_url", "archivo", "sinpad")}
        e["etiqueta"] = etiqueta(r["fecha_ocurrencia"])
        for c in campos:
            e[c] = float(r[c]) if r[c] else None
        eventos.append(e)
    eventos.sort(key=lambda e: e["fecha_ocurrencia"], reverse=True)
    excluidos = [r for r in filas if r["incluido"] == "no"]
    return {"desde": cfg["desde"], "desde_largo": etiqueta(cfg["desde"], True), "revisado": cfg["revisado_hasta"],
            "revisado_largo": etiqueta(cfg["revisado_hasta"], True), "regiones": cfg["regiones"], "decreto": cfg["decreto"],
            "eventos": eventos, "excluidos": len(excluidos)}


UMBRAL_AREA = 5.0  # % del departamento bajo el nivel para contar el día (método en docs/el-nino-avisos.md)


def construir_avisos(hoy: date | None = None) -> dict:
    """Avisos del SENAMHI desde el 1 set 2026.

    Lluvia: por departamento y día, el nivel más alto que cubre al menos UMBRAL_AREA % de su superficie, entre todos
    los avisos de ese día. Ríos: lista de avisos hidrológicos con su estación, cuenca y departamento."""
    hoy = hoy or date.today()
    filas = leer_csv(os.path.join(EN, "datos", "avisos_senamhi_lluvia.csv"))
    rios = leer_csv(os.path.join(EN, "datos", "avisos_senamhi_rios.csv"))
    nivel = {}
    avisos = {}
    for r in filas:
        avisos[r["aviso"]] = (r["nivel_aviso"], r["inicio"], r["fin"])
        lv = 4 if float(r["pct_area_rojo"]) >= UMBRAL_AREA else 3 if float(r["pct_area_naranja_o_mas"]) >= UMBRAL_AREA \
            else 2 if float(r["pct_area_amarillo_o_mas"]) >= UMBRAL_AREA else 0
        k = (r["departamento"], r["fecha"])
        if lv > nivel.get(k, 0):
            nivel[k] = lv
    desde = "2026-09-01"
    fechas = sorted({f for _, f in nivel})
    ultimo = max(fechas)
    dias = []
    d = date.fromisoformat(desde)
    while d <= date.fromisoformat(ultimo):
        dias.append(d.isoformat())
        d += timedelta(days=1)
    deps = sorted({dep for dep, _ in nivel})
    matriz = {dep: "".join(str(nivel.get((dep, f), 0)) for f in dias) for dep in deps}
    resumen = {}
    for dep, cad in matriz.items():
        pasado = cad[: sum(1 for f in dias if f <= hoy.isoformat())]
        resumen[dep] = {"dias2": sum(c >= "2" for c in pasado), "dias3": sum(c >= "3" for c in pasado), "dias4": sum(c == "4" for c in pasado)}
    hoy_s = hoy.isoformat()
    return {
        "desde": desde, "hoy": hoy_s, "dias": dias, "matriz": matriz, "resumen": resumen, "umbral": UMBRAL_AREA,
        "lluvia": {"total": len(avisos), "rojos": sum(v[0] == "ROJO" for v in avisos.values()),
                   "naranjas": sum(v[0] == "NARANJA" for v in avisos.values()),
                   "vigentes": sorted([{"n": k, "nivel": v[0], "inicio": v[1], "fin": v[2]} for k, v in avisos.items() if v[2] >= hoy_s],
                                      key=lambda x: x["inicio"])},
        "rios": {"total": len(rios), "rojos": sum(r["nivel"] == "ROJO" for r in rios),
                 "vigentes": sum(r["fin"] >= hoy_s for r in rios),
                 "lista": [{k: r[k] for k in ("aviso", "rio", "estacion", "tipo", "inicio", "fin", "nivel", "departamento", "cuenca")}
                           for r in sorted(rios, key=lambda r: (r["inicio"], r["aviso"]), reverse=True)]},
    }


def dias_territorio(avisos: dict, deps: list) -> dict:
    """Días (hasta hoy) en que al menos uno de los departamentos tuvo aviso de lluvia naranja o rojo; sin contar dos veces."""
    n = sum(1 for f in avisos["dias"] if f <= avisos["hoy"])
    nivel = [max((int(avisos["matriz"].get(d, "0" * len(avisos["dias"]))[i]) for d in deps), default=0) for i in range(n)]
    return {"naranja": sum(v >= 3 for v in nivel), "rojo": sum(v == 4 for v in nivel), "desde": avisos["desde"]}


def construir_brechas(ult, emergencias, avisos=None) -> dict:
    """Junta, por territorio, la exposición del CENEPRED con el PP 0068 del último corte y las emergencias del piloto.

    No calcula ningún índice: pone las cifras lado a lado (método en docs/el-nino-brechas.md)."""
    with open(os.path.join(EN, "config", "brechas.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    with open(os.path.join(EN, "config", "contexto.json"), encoding="utf-8") as f:
        ctx = json.load(f)
    expo = leer_csv(os.path.join(EN, "datos", "exposicion_cenepred.csv"))
    estudios = {}
    for r in expo:
        estudios.setdefault(r["estudio"], {"titulo": r["titulo"], "fecha": r["fecha_estudio"], "insumos": r["insumos"],
                                           "unidad": r["unidad"], "url": r["fuente_url"], "tablas": {}})
        estudios[r["estudio"]]["tablas"][f'{r["peligro"]}|{r["nivel"]}'] = f'{r["tabla"]}, p. {r["pagina"]}'

    def expo_de(estudio, deps):
        out = {}
        for r in expo:
            if r["estudio"] != estudio or r["departamento"] not in deps:
                continue
            k = f'{r["peligro"]}|{r["nivel"]}'
            o = out.setdefault(k, {"unidades": 0, "poblacion": 0, "viviendas": 0, "eess": 0, "iiee": 0, "deps": []})
            for c in ("unidades", "poblacion", "viviendas", "eess", "iiee"):
                o[c] += int(r[c]) if r[c] else 0
            o["deps"].append(r["departamento"])
        for o in out.values():
            o["faltan"] = [d for d in deps if d not in o["deps"]]
        return out

    pliegos = {(r["archivo"], r["codigo"]): r for r in ult if r["archivo"] in ("D2", "D3")}
    muni = {(r["archivo"], r["nombre"]): r for r in ult if r["archivo"] in ("D4", "D5")}
    em_por_region = defaultdict(int)
    for e in emergencias["eventos"]:
        em_por_region[e["region"]] += 1
    territorios = []
    for t in cfg["territorios"]:
        def suma(filas):
            return [sum(r["pim"] for r in filas), sum(r["devengado"] for r in filas)]
        gr_a = [pliegos[k] for k in (("D2", c) for c in t["pliegos"]) if k in pliegos]
        gr_p = [pliegos[k] for k in (("D3", c) for c in t["pliegos"]) if k in pliegos]
        mu_a = [muni[k] for k in (("D4", n) for n in t["municipal"]) if k in muni]
        mu_p = [muni[k] for k in (("D5", n) for n in t["municipal"]) if k in muni]
        nombres = sorted({titulo(r["nombre"]) for r in gr_a + gr_p})
        en_piloto = [r for r in t["emergencias"] if r in emergencias["regiones"]]
        territorios.append({
            "id": t["id"], "nombre": t["nombre"], "detalle": t.get("detalle", ""), "nota": t.get("nota", ""),
            "cenepred": t["cenepred"], "pliegos": nombres,
            "expo": {e: expo_de(e, t["cenepred"]) for e in (cfg["escenario_principal"], cfg["escenario_secundario"])},
            "gr": {"a": suma(gr_a), "p": suma(gr_p)}, "mu": {"a": suma(mu_a), "p": suma(mu_p)},
            "plan": {p: p in ctx["plan_aprobado"] for p in t["plan"]},
            "pronostico": ctx["pronostico"].get(t["pronostico"]),
            "emergencias": None if not en_piloto else sum(em_por_region[r] for r in en_piloto),
            "avisos_lluvia": None if not avisos else dias_territorio(avisos, t["cenepred"]),
        })
    return {"revision": cfg["revision"], "principal": cfg["escenario_principal"], "secundario": cfg["escenario_secundario"],
            "estudios": estudios, "territorios": territorios, "fuente_pronostico": ctx["_fuentes"]["pronostico"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(RAIZ, "_site"))
    args = ap.parse_args()
    datos = construir_datos()
    with open(os.path.join(RAIZ, "sitio", "plantilla.html"), encoding="utf-8") as f:
        html = f.read()
    repo = datos.pop("_repo")
    html = html.replace("__DATOS__", json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__REPO__", repo)
    corte = html.index("</style>") + len("</style>")
    cabeza, cuerpo = html[:corte], html[corte:]
    cabeza = cabeza.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    pagina = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
              '<meta name="description" content="Qué hizo el Estado con el aviso de El Niño 2026-2027: '
              'presupuesto de prevención por región, con datos públicos del MEF.">\n'
              '<style>:root{color-scheme:light}[hidden]{display:none!important}</style>\n'
              + cabeza + "\n</head>\n<body>\n" + cuerpo + "\n</body>\n</html>\n")
    # El Niño vive ahora en /el-nino/; la raíz es la portada con el menú de observatorios.
    carpeta = os.path.join(args.salida, "el-nino")
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina)
    # Datos abiertos en /el-nino/datos/ y, por compatibilidad con enlaces ya compartidos, también en /datos/.
    for destino in (os.path.join(carpeta, "datos"), os.path.join(args.salida, "datos")):
        os.makedirs(destino, exist_ok=True)
        for nombre in ("ejecucion_pp0068.csv", "hechos.csv", "emergencias.csv", "exposicion_cenepred.csv"):
            shutil.copy(os.path.join(EN, "datos", nombre), destino)
    print(f"El Niño generado en {carpeta} (corte {datos['corte']}, {len(datos['regiones'])} pliegos).")
    # Museo de la planificación: /planificacion/ con sus datos abiertos en /planificacion/datos/.
    import importlib.util
    spec = importlib.util.spec_from_file_location("planificacion_build", os.path.join(RAIZ, "planificacion", "build.py"))
    museo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(museo)
    museo.main(os.path.join(args.salida, "planificacion"), repo)
    # Observatorio del sistema de salud: /salud/ con los datos del mapa en /salud/geo/ y abiertos en /salud/datos/.
    spec = importlib.util.spec_from_file_location("salud_build", os.path.join(RAIZ, "salud", "build.py"))
    salud = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(salud)
    salud.main(os.path.join(args.salida, "salud"), repo)
    import sitio_incendios
    d = sitio_incendios.construir(args.salida)
    print(f"Incendios generado (corte {d['corte']}, {len(d['pistas'])} pistas vigentes). Portada en {args.salida}/index.html.")


if __name__ == "__main__":
    main()
