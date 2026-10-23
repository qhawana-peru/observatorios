"""Archiva los PDF de los reportes del COEN-INDECI listados en la configuración.

Uso:
    python herramientas/descargar_indeci.py              # carpeta con la fecha de hoy en Lima
    python herramientas/descargar_indeci.py 2026-10-23

Cada PDF se guarda tal como llega en el-nino/fuentes/indeci/AAAA-MM-DD/,
con un manifiesto (enlace, tamaño, huella SHA-256 y resultado). INDECI
reescribe sus páginas con cada actualización de un evento, pero cada
reporte tiene su propio PDF: archivarlos es la única manera de conservar
la versión que respalda cada cifra. Si un PDF ya está archivado con la
misma huella en una carpeta anterior, no se vuelve a guardar.
"""
from __future__ import annotations

import datetime as dt
import glob
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RAIZ, "el-nino", "config", "indeci_reportes.json")
FUENTES = os.path.join(RAIZ, "el-nino", "fuentes", "indeci")
LIMA = dt.timezone(dt.timedelta(hours=-5))


def url_segura(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(p._replace(path=urllib.parse.quote(urllib.parse.unquote(p.path), safe="/")))


def nombre_archivo(url: str) -> str:
    base = urllib.parse.unquote(url.rsplit("/", 1)[-1])
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9._-]+", "-", base)


def bajar(url: str, intentos: int = 3) -> bytes:
    ultimo = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(url_segura(url), headers={"User-Agent": "Qhawana-observatorio/1.0 (datos abiertos)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            ultimo = e
            if getattr(e, "code", None) == 404:
                break
            time.sleep(5 * (i + 1))
    raise RuntimeError(str(ultimo))


def huellas_archivadas() -> dict:
    vistas = {}
    for m in glob.glob(os.path.join(FUENTES, "*", "manifiesto.json")):
        for a in json.load(open(m, encoding="utf-8")).get("archivos", []):
            if a.get("sha256"):
                vistas[a["sha256"]] = os.path.relpath(os.path.join(os.path.dirname(m), a["archivo"]), RAIZ)
    return vistas


def main() -> int:
    fecha = sys.argv[1] if len(sys.argv) > 1 else dt.datetime.now(LIMA).date().isoformat()
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    vistas = huellas_archivadas()
    carpeta = os.path.join(FUENTES, fecha)
    manifiesto = {"fecha": fecha, "descargado": dt.datetime.now(LIMA).isoformat(timespec="seconds"),
                  "fuente": "INDECI, COEN: reportes de emergencia (PDF publicados en portal.indeci.gob.pe)", "archivos": []}
    nuevos = errores = 0
    for r in cfg["reportes"]:
        fila = {"numero": r["numero"], "region": r.get("region", ""), "url": r["url"]}
        try:
            contenido = bajar(r["url"])
            if not contenido.startswith(b"%PDF"):
                raise RuntimeError("la respuesta no es un PDF")
        except Exception as e:  # noqa: BLE001
            fila["error"] = str(e)
            errores += 1
            print(f"✗ {r['numero']}: {e}")
            manifiesto["archivos"].append(fila)
            continue
        huella = hashlib.sha256(contenido).hexdigest()
        fila.update(bytes=len(contenido), sha256=huella)
        if huella in vistas:
            fila["ya_archivado"] = vistas[huella]
            print(f"= {r['numero']}: sin cambios ({vistas[huella]})")
        else:
            os.makedirs(carpeta, exist_ok=True)
            fila["archivo"] = nombre_archivo(r["url"])
            with open(os.path.join(carpeta, fila["archivo"]), "wb") as f:
                f.write(contenido)
            nuevos += 1
            print(f"✓ {r['numero']}: {fila['archivo']}")
        manifiesto["archivos"].append(fila)
    if nuevos:
        with open(os.path.join(carpeta, "manifiesto.json"), "w", encoding="utf-8") as f:
            json.dump(manifiesto, f, ensure_ascii=False, indent=2)
    print(f"{nuevos} PDF nuevos, {errores} con error.")
    return 1 if errores == len(cfg["reportes"]) else 0


if __name__ == "__main__":
    sys.exit(main())
