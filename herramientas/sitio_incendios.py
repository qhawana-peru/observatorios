"""Genera la página del Monitor de incendios forestales y la portada de Qhawana.

Lo llama construir_sitio.py. También se puede correr solo:
    python herramientas/sitio_incendios.py --salida _site

Lee incendios/datos/*.csv e incendios/config/sitio.json y escribe:
  <salida>/incendios/index.html      la página del monitor
  <salida>/incendios/datos/          los datos abiertos, tal cual
  <salida>/index.html                la portada con el menú de observatorios

Las pistas (cifras de prensa sin verificar) se muestran solo mientras no venzan.
Ninguna pista entra en resúmenes ni en cálculos.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(RAIZ, "incendios")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "setiembre", "octubre", "noviembre", "diciembre"]
REGIONES = ("Cusco", "Cajamarca")


def leer_csv(nombre):
    with open(os.path.join(INC, "datos", nombre), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fecha_larga(iso: str) -> str:
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"


def cuantil(valores, p):
    """Cuantil con interpolación lineal (el mismo criterio que una hoja de cálculo)."""
    v = sorted(valores)
    if not v:
        return None
    k = (len(v) - 1) * p
    i = int(k)
    if i + 1 >= len(v):
        return v[-1]
    return v[i] + (v[i + 1] - v[i]) * (k - i)


def pistas_vigentes(pistas, hoy: date):
    """Una pista se muestra si sigue sin verificar y no venció."""
    return [p for p in pistas
            if p["estado"] == "sin verificar" and date.fromisoformat(p["vence"]) >= hoy]


def proyeccion(historial, seguimiento, region):
    filas = [r for r in historial if r["region"] == region]
    previas = [float(r["adicional_pct"]) for r in filas if r["adicional_pct"] not in ("", None)]
    actual = next(int(r["hasta_corte"]) for r in filas if r["anio"] == "2026")
    lugar = 1 + sum(1 for r in filas if r["anio"] != "2026" and int(r["hasta_corte"]) > actual)
    seg = sorted((r for r in seguimiento if r["region"] == region), key=lambda r: r["corte"])
    semana = None
    if len(seg) >= 2:
        a, b = seg[-2], seg[-1]
        semana = {"desde": a["corte"], "hasta": b["corte"],
                  "pct": round((int(b["focos_npp"]) / int(a["focos_npp"]) - 1) * 100, 1),
                  "bajo": a["rango_bajo_pct"], "alto": a["rango_alto_pct"]}
    return {"focos_2026": actual, "lugar": lugar, "anios": len(filas),
            "p25": round(cuantil(previas, .25)), "mediana": round(cuantil(previas, .5)),
            "p75": round(cuantil(previas, .75)), "min": round(min(previas)), "max": round(max(previas)),
            "semana": semana}


def construir_datos(hoy: date | None = None) -> dict:
    hoy = hoy or date.today()
    with open(os.path.join(INC, "config", "sitio.json"), encoding="utf-8") as f:
        sitio = json.load(f)
    alertas = leer_csv("serfor_alertas_recientes.csv")
    focos = leer_csv("serfor_focos_anual.csv")
    prov = leer_csv("serfor_alertas_provincia.csv")
    hect = leer_csv("serfor_hectareas_anual.csv")
    curvas = leer_csv("serfor_curvas_npp.csv")
    hist = leer_csv("serfor_historial_npp.csv")
    seg = leer_csv("seguimiento_proyeccion.csv")
    pistas = leer_csv("pistas.csv")

    regiones = {}
    for reg in REGIONES:
        regiones[reg] = {
            "alertas": {r["indicador"]: {"v": int(r["valor"]), "periodo": r["periodo"]}
                        for r in alertas if r["region"] == reg},
            "focos": [[r["anio"], int(r["focos"])] for r in focos if r["region"] == reg],
            "provincias": [[r["provincia"], int(r["alertas"]), r["periodo"]] for r in prov if r["region"] == reg],
            "hectareas": [[r["anio"], round(float(r["hectareas"]))] for r in hect if r["region"] == reg],
            "curvas": {},
            "proyeccion": proyeccion(hist, seg, reg),
        }
        for r in curvas:
            if r["region"] == reg:
                regiones[reg]["curvas"].setdefault(r["anio"], []).append(int(r["acumulado"]))
    peru = {r["indicador"]: {"v": int(r["valor"]), "periodo": r["periodo"]}
            for r in alertas if r["region"] == "Perú"}
    vigentes = pistas_vigentes(pistas, hoy)
    return {"corte": sitio["fecha_corte"], "corte_largo": fecha_larga(sitio["fecha_corte"]),
            "aprobado": sitio.get("estado") == "publicado", "nota": sitio.get("nota_corte", ""), "regiones": regiones, "peru": peru,
            "pistas": vigentes, "pistas_total": len(pistas), "_repo": sitio.get("repositorio", "#")}


def envolver(plantilla: str, descripcion: str) -> str:
    """Convierte una plantilla (estilo + cuerpo) en un documento HTML completo."""
    corte = plantilla.index("</style>") + len("</style>")
    cabeza, cuerpo = plantilla[:corte], plantilla[corte:]
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<meta name="description" content="{descripcion}">\n'
            '<style>:root{color-scheme:light}[hidden]{display:none!important}</style>\n'
            + cabeza + "\n</head>\n<body>\n" + cuerpo + "\n</body>\n</html>\n")


def construir(salida: str, hoy: date | None = None) -> dict:
    datos = construir_datos(hoy)
    repo = datos.pop("_repo")
    with open(os.path.join(RAIZ, "sitio", "incendios.html"), encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__DATOS__", json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__REPO__", repo)
    destino = os.path.join(salida, "incendios")
    os.makedirs(os.path.join(destino, "datos"), exist_ok=True)
    with open(os.path.join(destino, "index.html"), "w", encoding="utf-8") as f:
        f.write(envolver(html, "Dónde y cuánto se quema en Cusco y Cajamarca, con datos públicos de SERFOR, "
                               "y qué cifras de prensa faltan verificar."))
    for nombre in os.listdir(os.path.join(INC, "datos")):
        if nombre.endswith(".csv"):
            shutil.copy(os.path.join(INC, "datos", nombre), os.path.join(destino, "datos"))
    with open(os.path.join(RAIZ, "sitio", "portada.html"), encoding="utf-8") as f:
        portada = f.read().replace("__REPO__", repo).replace("__CORTE_INCENDIOS__", datos["corte_largo"])
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(envolver(portada, "Qhawana: observatorios ciudadanos con datos públicos sobre incendios "
                                  "forestales, El Niño y seguridad en el Perú."))
    return datos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(RAIZ, "_site"))
    args = ap.parse_args()
    d = construir(args.salida)
    print(f"Incendios: corte {d['corte']}, {len(d['pistas'])} de {d['pistas_total']} pistas vigentes. Portada escrita.")


if __name__ == "__main__":
    main()
