"""Descarga las siete exportaciones del MEF para el corte de hoy.

Uso:
    python herramientas/descargar.py              # fecha de hoy en Lima
    python herramientas/descargar.py 2026-10-26   # fecha de la carpeta

Guarda los archivos tal como llegan, sin modificarlos, en
el-nino/fuentes/mef/AAAA-MM-DD/, con los nombres de la guía, y un
manifiesto con el enlace, el tamaño y la huella SHA-256 de cada uno.
Si el MEF no responde, termina con error y la descarga se hace a mano
siguiendo la guía (los mismos enlaces están en el-nino/config/rutas.json).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validar  # noqa: E402

LIMA = dt.timezone(dt.timedelta(hours=-5))


def url_de(cfg: dict, codigo: str) -> str:
    return cfg["base"] + cfg["rutas"][codigo]["tramo"] + cfg["cola"].format(anio=cfg["anio"])


def bajar(url: str, intentos: int = 3) -> bytes:
    ultimo = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Qhawana-observatorio/1.0 (datos abiertos)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def main():
    cfg = validar.cargar_config()
    fecha = sys.argv[1] if len(sys.argv) > 1 else dt.datetime.now(LIMA).date().isoformat()
    carpeta = os.path.join(validar.RAIZ, "el-nino", "fuentes", "mef", fecha)
    os.makedirs(carpeta, exist_ok=True)
    manifiesto = {"fecha": fecha, "descargado": dt.datetime.now(LIMA).isoformat(timespec="seconds"),
                  "fuente": "MEF, Consulta Amigable (exportación pública)", "archivos": []}
    for codigo, ruta in cfg["rutas"].items():
        url = url_de(cfg, codigo)
        contenido = bajar(url)
        nombre = f"{fecha.replace('-', '')}_PP0068_{codigo}_{ruta['detalle']}_p1de1.xls"
        with open(os.path.join(carpeta, nombre), "wb") as f:
            f.write(contenido)
        manifiesto["archivos"].append({"codigo": codigo, "archivo": nombre, "url": url,
                                       "bytes": len(contenido), "sha256": hashlib.sha256(contenido).hexdigest()})
        print(f"{codigo}: {len(contenido):,} bytes")
        time.sleep(2)   # sin apuro: no sobrecargar el servidor del MEF
    with open(os.path.join(carpeta, "manifiesto.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=2)
    print(f"Listo: {carpeta}")


if __name__ == "__main__":
    main()
