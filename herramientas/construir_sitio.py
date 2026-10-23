"""Genera el sitio público del Observatorio El Niño a partir de los datos del repositorio.

Uso:
    python herramientas/construir_sitio.py            # escribe _site/
    python herramientas/construir_sitio.py --salida carpeta

Lee:
  el-nino/datos/ejecucion_pp0068.csv   cortes validados del MEF
  el-nino/datos/hechos.csv             bitácora de pronósticos, decisiones y alertas
  el-nino/datos/emergencias.csv        emergencias del COEN-INDECI (piloto costa norte)
  el-nino/config/emergencias.json      alcance de esa tabla y declaratoria vigente
  el-nino/config/contexto.json         pronóstico por región y planes aprobados
  el-nino/config/sitio.json            estado de publicación y dirección del repositorio
y escribe una página estática (index.html) más los datos abiertos en _site/datos/.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
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
    return {"corte": corte, "corte_corto": etiqueta(corte), "corte_largo": etiqueta(corte, True),
            "aprobado": sitio.get("estado") == "publicado", "niveles": niveles, "regiones": regiones,
            "serie": serie, "hechos": hechos, "emergencias": emergencias, "contexto": contexto, "_repo": sitio.get("repositorio", "#")}


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
    os.makedirs(args.salida, exist_ok=True)
    with open(os.path.join(args.salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina)
    destino = os.path.join(args.salida, "datos")
    os.makedirs(destino, exist_ok=True)
    for nombre in ("ejecucion_pp0068.csv", "hechos.csv", "emergencias.csv"):
        shutil.copy(os.path.join(EN, "datos", nombre), destino)
    print(f"Sitio generado en {args.salida} (corte {datos['corte']}, {len(datos['regiones'])} pliegos).")


if __name__ == "__main__":
    main()
