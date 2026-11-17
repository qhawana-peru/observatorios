"""Genera los datos del Observatorio del sistema de salud desde una descarga completa de RENIPRESS (SUSALUD).

Uso:
    python3 salud/renipress.py RUTA_AL_EXPORT.xls --corte 2026-11-16

La descarga original NO se guarda en el repositorio: trae el nombre del director médico,
teléfonos y RUC de cada establecimiento. Este script deja solo lo necesario, sin datos personales:

  salud/datos/renipress_resumen_AAAAMMDD.json            conteos por institución (página y fichas)
  salud/datos/renipress_institucion_departamento_AAAAMMDD.csv
  salud/geo/puntos.json      un registro por establecimiento: lat, lon, red, capacidad, aproximado,
                             departamento (UBIGEO), nombre, categoría, distrito
  salud/geo/departamentos.json   resumen por departamento y red

Reglas:
  - Red: 0 MINSA y gobiernos regionales; 1 EsSalud; 2 Sanidades FFAA; 3 Sanidad PNP; 4 privados;
    5 municipales, INPE y otros.
  - Capacidad: 2 hospital general (II-1, II-2, III-1, III-2); 1 con internamiento; 0 sin internamiento.
  - Nombre: el que publica RENIPRESS, sin números de documento ni teléfonos.
  - Sin coordenadas: se ubica en el promedio de los demás establecimientos de su distrito (o de su
    provincia), con un desplazamiento fijo derivado del código único, y se marca como aproximado.

Requiere xlrd (pip install xlrd).
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import os
import re

import xlrd

AQUI = os.path.dirname(os.path.abspath(__file__))
RED = {"GOBIERNO REGIONAL": 0, "MINSA": 0, "ESSALUD": 1,
       "SANIDAD DEL EJERCITO DEL PERU": 2, "SANIDAD DE LA MARINA DE GUERRA DEL PERU": 2,
       "SANIDAD DE LA FUERZA AEREA DEL PERU": 2, "SANIDAD DE LA POLICIA NACIONAL DEL PERU": 3,
       "PRIVADO": 4}
GENERALES = ("II-1", "II-2", "III-1", "III-2")


def limpiar_nombre(texto):
    """Nombre tal como lo publica RENIPRESS, sin números de documento (RUC, DNI) ni teléfonos."""
    t = re.sub(r"\d{8,}|\b9\d{2} \d{3} \d{3}\b", "", str(texto))
    t = " ".join(t.split()).strip(" -–,.;:")
    return (t or "Establecimiento sin nombre registrado")[:60]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--corte", required=True, help="AAAA-MM-DD de la descarga")
    a = ap.parse_args()
    tag = a.corte.replace("-", "")
    hoja = xlrd.open_workbook(a.export).sheet_by_index(0)
    cab = hoja.row_values(0)
    ix = {h: i for i, h in enumerate(cab)}
    filas = [hoja.row_values(r) for r in range(1, hoja.nrows)]
    g = lambda r, k: r[ix[k]]

    def red(r): return RED.get(g(r, "Institución"), 5)

    def cap(r):
        c = str(g(r, "Categoria")).strip()
        if c in GENERALES:
            return 2
        return 1 if "CON INTERNAMIENTO" in g(r, "Tipo") else 0

    def camas(r): return num(g(r, "CAMAS")) or 0.0

    # Resumen por institución
    inst = {}
    for nombre in sorted({g(r, "Institución") for r in filas}):
        rr = [r for r in filas if g(r, "Institución") == nombre]
        inst[nombre] = dict(n=len(rr),
                            intern=sum("CON INTERNAMIENTO" in g(r, "Tipo") for r in rr),
                            hosp=sum(str(g(r, "Categoria")).startswith(("II", "III")) for r in rr),
                            camas=int(sum(camas(r) for r in rr)),
                            lima=sum(g(r, "Departamento") == "LIMA" for r in rr),
                            deps=len({g(r, "Departamento") for r in rr}))
    fecha = "/".join(reversed(a.corte.split("-")))
    resumen = dict(inst=inst, total=dict(n=len(filas), deps=len({g(r, "Departamento") for r in filas})), corte=fecha)
    with open(os.path.join(AQUI, "datos", f"renipress_resumen_{tag}.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    cnt = collections.Counter((g(r, "Departamento"), g(r, "Institución")) for r in filas)
    with open(os.path.join(AQUI, "datos", f"renipress_institucion_departamento_{tag}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["departamento", "institucion", "establecimientos"])
        for (d, i), n in sorted(cnt.items()):
            w.writerow([d, i, n])

    # Puntos
    cen = collections.defaultdict(list)
    for r in filas:
        la, lo = num(g(r, "NORTE")), num(g(r, "ESTE"))
        if la and lo:
            cen[g(r, "UBIGEO")].append((la, lo))
    prov = collections.defaultdict(list)
    for u, v in cen.items():
        prov[u[:4]] += v

    def media(v): return sum(x for x, _ in v) / len(v), sum(y for _, y in v) / len(v)

    def desvio(codigo, escala=0.025):
        h = hashlib.md5(codigo.encode()).digest()
        ang, d = h[0] / 255 * 2 * math.pi, math.sqrt(h[1] / 255) * escala
        return d * math.sin(ang), d * math.cos(ang)

    puntos = []
    dep = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0, 0, 0]))
    for r in filas:
        la, lo = num(g(r, "NORTE")), num(g(r, "ESTE"))
        aprox = 0
        if not (la and lo):
            u = g(r, "UBIGEO")
            la, lo = media(cen.get(u) or prov[u[:4]])
            dy, dx = desvio(str(g(r, "Código Único")))
            la, lo, aprox = la + dy, lo + dx, 1
        k, c, d = red(r), cap(r), g(r, "UBIGEO")[:2]
        nombre = limpiar_nombre(g(r, "Nombre del establecimiento"))
        puntos.append([round(la, 4), round(lo, 4), k, c, aprox, d, nombre, str(g(r, "Categoria")), str(g(r, "Distrito")).strip().title()])
        x = dep[d][k]
        x[0] += 1; x[1] += c >= 1; x[2] += c == 2; x[3] += camas(r); x[4] += aprox
    nombres = {g(r, "UBIGEO")[:2]: g(r, "Departamento").strip() for r in filas}
    salida = {d: {"nombre": nombres[d], "g": {k: [int(v) for v in dep[d][k]] for k in range(6)}} for d in dep}
    with open(os.path.join(AQUI, "geo", "puntos.json"), "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(p, ensure_ascii=False) for p in puntos) + "\n]\n")
    with open(os.path.join(AQUI, "geo", "departamentos.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False)
    print(f"{len(filas)} establecimientos; {sum(p[4] for p in puntos)} con ubicación aproximada; corte {fecha}.")
    print("Actualiza RESUMEN en salud/build.py si cambia la fecha del corte.")


if __name__ == "__main__":
    main()
