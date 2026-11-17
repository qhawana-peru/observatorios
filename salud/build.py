"""Genera la página del Observatorio del sistema de salud.

Uso:
    python3 salud/build.py --salida _site/salud

Escribe <salida>/index.html desde plantilla.html (inyecta el resumen de RENIPRESS y el de mortalidad del SINADEF),
copia los datos del mapa a <salida>/geo/ y los datos abiertos a <salida>/datos/.
Los datos se regeneran con renipress.py (RENIPRESS) y con sinadef_agregar.js + sinadef_resumen.py (SINADEF).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
RESUMEN = "renipress_resumen_20261116.json"


def main(salida=None, repo="https://github.com/qhawana-peru/observatorios"):
    salida = salida or os.path.join(AQUI, "_salida")
    os.makedirs(salida, exist_ok=True)
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(AQUI, "datos", RESUMEN), encoding="utf-8") as f:
        resumen = json.load(f)
    html = html.replace("__RENI__", json.dumps(resumen, ensure_ascii=False, separators=(",", ":")))
    with open(os.path.join(AQUI, "datos", "mortalidad_sinadef_resumen.json"), encoding="utf-8") as f:
        mort = json.load(f)
    html = html.replace("__MORT__", json.dumps(mort, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__REPO__", repo)
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    for carpeta in ("geo", "datos"):
        destino = os.path.join(salida, carpeta)
        os.makedirs(destino, exist_ok=True)
        for nombre in sorted(os.listdir(os.path.join(AQUI, carpeta))):
            shutil.copy(os.path.join(AQUI, carpeta, nombre), destino)
    print(f"Sistema de salud generado en {salida} (RENIPRESS {resumen['corte']}, {resumen['total']['n']} establecimientos).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida")
    main(ap.parse_args().salida)
