"""Valida el-nino/datos/exposicion_cenepred.csv, la transcripción de los estudios de escenarios de riesgo del CENEPRED.

Control de lectura: en las tablas marcadas como completas (estudio A), la suma de las filas por departamento debe dar
exactamente el total nacional impreso en el PDF, columna por columna. Si una cifra se transcribió mal, no cuadra.
En el estudio B solo se transcribieron algunos departamentos, así que solo se revisa que haya total y fuente.

Uso: python herramientas/validar_cenepred.py   (sale con código 1 si algo falla)
"""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(RAIZ, "el-nino", "datos", "exposicion_cenepred.csv")
COMPLETOS = {"A"}  # estudios cuyas tablas se transcribieron completas
COLUMNAS = ("unidades", "poblacion", "viviendas", "eess", "iiee")


def validar(ruta: str = RUTA) -> list[str]:
    errores = []
    with open(ruta, encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f))
    grupos = defaultdict(list)
    for r in filas:
        if not r["fuente_url"].startswith("https://"):
            errores.append(f"{r['estudio']} {r['departamento']}: falta el enlace a la fuente")
        if not r["tabla"] or not r["pagina"]:
            errores.append(f"{r['estudio']} {r['departamento']}: falta tabla o página")
        grupos[(r["estudio"], r["peligro"], r["nivel"])].append(r)
    for (est, pel, niv), g in sorted(grupos.items()):
        tot = [r for r in g if r["departamento"] == "TOTAL NACIONAL"]
        if len(tot) != 1:
            errores.append(f"{est} {pel} {niv}: debe haber exactamente un TOTAL NACIONAL")
            continue
        deps = [r for r in g if r["departamento"] != "TOTAL NACIONAL"]
        if len({r["departamento"] for r in deps}) != len(deps):
            errores.append(f"{est} {pel} {niv}: departamento repetido")
        if est not in COMPLETOS:
            continue
        for c in COLUMNAS:
            s = sum(int(r[c]) for r in deps if r[c])
            t = int(tot[0][c])
            if s != t:
                errores.append(f"{est} {pel} {niv}: la columna {c} suma {s:,} y el total impreso es {t:,}")
    return errores


if __name__ == "__main__":
    e = validar()
    for x in e:
        print("ERROR:", x)
    print("Exposición CENEPRED: " + ("todo cuadra con los totales impresos." if not e else f"{len(e)} problema(s)."))
    sys.exit(1 if e else 0)
