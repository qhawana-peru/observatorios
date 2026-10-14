"""Convierte un corte validado del MEF en filas del archivo de datos abiertos.

Uso:
    python herramientas/procesar.py el-nino/fuentes/mef/2026-10-26

Escribe (o reemplaza, si ya existía) las filas de esa fecha en
el-nino/datos/ejecucion_pp0068.csv. No corre si la validación falla.
"""
from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validar  # noqa: E402

RAIZ = validar.RAIZ
SALIDA = os.path.join(RAIZ, "el-nino", "datos", "ejecucion_pp0068.csv")
COLUMNAS = ["fecha_corte", "archivo", "nivel", "tipo", "codigo", "nombre", "pia", "pim",
            "certificacion", "compromiso_anual", "atencion_mensual", "devengado", "girado", "avance_mef"]


def filas_de(archivos: dict, fecha: str, cfg: dict) -> list[dict]:
    out = []
    for codigo, ruta in cfg["rutas"].items():
        a = archivos.get(codigo)
        if not a:
            continue
        for f in a.filas:
            out.append({
                "fecha_corte": fecha, "archivo": codigo,
                "nivel": f.codigo if codigo == "D1" else ruta["nivel"],
                "tipo": ruta["tipo"], "codigo": f.codigo, "nombre": f.nombre,
                "pia": f.pia, "pim": f.pim, "certificacion": f.certificacion,
                "compromiso_anual": f.compromiso_anual, "atencion_mensual": f.atencion_mensual,
                "devengado": f.devengado, "girado": f.girado, "avance_mef": f.avance,
            })
    return out


def escribir(nuevas: list[dict], fecha: str, salida: str = SALIDA):
    existentes = []
    if os.path.exists(salida):
        with open(salida, encoding="utf-8", newline="") as fh:
            existentes = [r for r in csv.DictReader(fh) if r["fecha_corte"] != fecha]
    todas = existentes + nuevas
    todas.sort(key=lambda r: (r["fecha_corte"], r["archivo"], r["codigo"]))
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(todas)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    carpeta = sys.argv[1]
    res, meta = validar.validar(carpeta)
    if not all(r.ok for r in res):
        print(validar.informe(res, meta))
        print("No se procesa: corrige primero lo que marca la validación.")
        sys.exit(1)
    archivos, _ = validar.leer_corte(carpeta)
    filas = filas_de(archivos, meta["fecha"], validar.cargar_config())
    escribir(filas, meta["fecha"])
    print(f"{len(filas)} filas del corte {meta['fecha']} escritas en {os.path.relpath(SALIDA, RAIZ)}.")


if __name__ == "__main__":
    main()
