"""Controles de la tabla de emergencias (el-nino/datos/emergencias.csv).

Uso:
    python herramientas/validar_emergencias.py

Revisa que cada fila incluida:
  1. tenga su reporte original archivado (PDF en el-nino/fuentes/indeci/ con huella en el manifiesto),
  2. enlace al portal de INDECI,
  3. haya ocurrido dentro del periodo y en una región del piloto,
  4. traiga cifras numéricas o vacías (vacío = no reportado; nunca se escribe 0 si el reporte no lo dice),
  5. no repita un mismo reporte en dos filas.
Y que cada fila excluida diga por qué.
"""
from __future__ import annotations

import csv
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, "el-nino", "datos", "emergencias.csv")
CONFIG = os.path.join(RAIZ, "el-nino", "config", "emergencias.json")
NUMERICOS = ["personas_damnificadas", "personas_afectadas", "personas_heridas", "viviendas_inhabitables",
             "viviendas_afectadas", "iiee_afectadas", "eess_afectados", "vias_afectadas_km"]


def archivados(raiz: str = RAIZ) -> set:
    vistos = set()
    for m in glob.glob(os.path.join(raiz, "el-nino", "fuentes", "indeci", "*", "manifiesto.json")):
        carpeta = os.path.relpath(os.path.dirname(m), raiz)
        for a in json.load(open(m, encoding="utf-8")).get("archivos", []):
            if a.get("archivo") and a.get("sha256"):
                vistos.add(f"{carpeta}/{a['archivo']}".replace(os.sep, "/"))
    return vistos


def revisar(filas: list, cfg: dict, pdfs: set) -> list:
    problemas, reportes = [], {}
    for f in filas:
        i = f.get("id") or "(sin id)"
        if f.get("incluido") not in ("si", "no"):
            problemas.append(f"{i}: 'incluido' debe ser si o no.")
            continue
        if f["incluido"] == "no":
            if not f.get("nota", "").startswith("Excluido"):
                problemas.append(f"{i}: una fila excluida debe explicar el motivo en 'nota' (empieza con 'Excluido').")
            continue
        if f.get("archivo") not in pdfs:
            problemas.append(f"{i}: el reporte no está archivado ({f.get('archivo') or 'sin archivo'}). Agrega su PDF a el-nino/config/indeci_reportes.json.")
        if not f.get("fuente_url", "").startswith("https://portal.indeci.gob.pe/"):
            problemas.append(f"{i}: la fuente debe ser un enlace del portal de INDECI.")
        if f.get("fecha_ocurrencia", "") < cfg["desde"]:
            problemas.append(f"{i}: ocurrió antes del {cfg['desde']}; debe ir como excluido.")
        if f.get("region") not in cfg["regiones"]:
            problemas.append(f"{i}: {f.get('region')} no está en las regiones del piloto.")
        for c in NUMERICOS:
            v = f.get(c, "")
            if v:
                try:
                    if float(v) < 0:
                        raise ValueError
                except ValueError:
                    problemas.append(f"{i}: '{c}' debe ser un número o quedar vacío (no reportado).")
        clave = f.get("reporte")
        if clave in reportes:
            problemas.append(f"{i}: el {clave} ya está en la fila {reportes[clave]}.")
        reportes[clave] = i
    return problemas


def main() -> int:
    filas = list(csv.DictReader(open(CSV, encoding="utf-8", newline="")))
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    problemas = revisar(filas, cfg, archivados())
    incl = [f for f in filas if f["incluido"] == "si"]
    print(f"Emergencias: {len(incl)} incluidas, {len(filas) - len(incl)} excluidas.")
    for p in problemas:
        print("✗", p)
    if not problemas:
        print("✓ Cada emergencia incluida tiene su reporte original archivado y cifras válidas.")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
