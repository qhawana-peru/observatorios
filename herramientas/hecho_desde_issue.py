"""Convierte un formulario "Registrar un hecho" en una fila de el-nino/datos/hechos.csv.

Lo usa la automatización cuando alguien del equipo pone la etiqueta
`listo-para-registrar` a un formulario ya verificado. Lee el texto del
formulario desde la variable de entorno CUERPO y el número desde NUMERO.
"""
from __future__ import annotations

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construir_sitio import EN, etiqueta  # noqa: E402

RUTA = os.path.join(EN, "datos", "hechos.csv")
CAMPOS = {
    "Fecha del hecho": "fecha",
    "Tipo de hecho": "franja",
    "Qué pasó, en lenguaje simple": "texto",
    "Qué cambia frente a lo anterior (opcional)": "cambio",
    "Enlace a la fuente primaria": "fuente_url",
    "Cita textual del documento": "cita",
    "Solo para comunicados ENFEN — magnitud del Niño Costero": "costero",
    "Solo para comunicados ENFEN — magnitud del Niño global": "global",
}


def leer_formulario(cuerpo: str) -> dict:
    datos = {}
    for bloque in re.split(r"^### ", cuerpo, flags=re.M)[1:]:
        titulo, _, valor = bloque.partition("\n")
        valor = valor.strip()
        if valor == "_No response_":
            valor = ""
        clave = CAMPOS.get(titulo.strip())
        if clave:
            datos[clave] = " ".join(valor.split())
    return datos


def fila(datos: dict, numero: str) -> dict:
    fecha = datos.get("fecha", "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
        raise ValueError(f"La fecha «{fecha}» no tiene el formato AAAA-MM-DD.")
    url = datos.get("fuente_url", "")
    if not url.startswith("https://"):
        raise ValueError("El enlace a la fuente primaria debe empezar con https://")
    franja = datos.get("franja", "otro").split(":")[0].strip()
    if franja not in ("peligro", "respuesta", "control", "otro"):
        raise ValueError(f"Tipo de hecho desconocido: {franja}")

    def magnitud(v):
        return v.split(" ")[0] if v and v[0].isdigit() else ""

    return {"id": f"H{numero}", "franja": franja, "fecha": fecha, "etiqueta_fecha": etiqueta(fecha),
            "texto": datos.get("texto", ""), "cambio": datos.get("cambio", ""), "fuente_url": url,
            "fuente_tipo": "primaria", "costero": magnitud(datos.get("costero", "")),
            "global": magnitud(datos.get("global", "")), "futuro": "", "pct": ""}


def main():
    cuerpo, numero = os.environ.get("CUERPO", ""), os.environ.get("NUMERO", "0")
    nueva = fila(leer_formulario(cuerpo), numero)
    with open(RUTA, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        columnas = lector.fieldnames
        filas = [r for r in lector if r["id"] != nueva["id"]]
    filas.append(nueva)
    filas.sort(key=lambda r: r["fecha"])
    with open(RUTA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)
    print(f"Hecho {nueva['id']} del {nueva['fecha']} agregado.")


if __name__ == "__main__":
    main()
