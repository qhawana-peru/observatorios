"""Convierte la consulta de avisos del SENAMHI (herramientas/senamhi_avisos.js) en los CSV del Observatorio El Niño.

Uso: python herramientas/procesar_avisos_senamhi.py avisos_lluvia_AAAA-MM-DD.txt avisos_rios_AAAA-MM-DD.txt
Escribe el-nino/datos/avisos_senamhi_lluvia.csv y el-nino/datos/avisos_senamhi_rios.csv (los reemplaza completos).
Método: docs/el-nino-avisos.md.
"""
import csv
import os
import re
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "el-nino", "datos")
URLM = ("https://idesep.senamhi.gob.pe/geoserver/g_aviso/ows?service=WFS&version=1.0.0&request=GetFeature"
        "&typeName=g_aviso:view_aviso&outputFormat=application/json&viewparams=qry:{n}_{m}_{a}")
# Estaciones hidrológicas: ubicación del mapa de estaciones del SENAMHI cruzada con los límites del INEI (IDESEP),
# verificada el 17 nov 2026 contra la capa aviso_hidro_pub. Una estación nueva se agrega aquí (manual 06, parte D).
EST = {"BORJA": ("LORETO", "DATEM DEL MARAÑON", "Intercuenca 49877"), "BELLAVISTA": ("LORETO", "MAYNAS", "Cuenca Napo"),
       "EL TIGRE": ("TUMBES", "TUMBES", "Cuenca Tumbes"), "CABO INGA": ("TUMBES", "TUMBES", "Cuenca Tumbes"),
       "ALAMOR": ("PIURA", "SULLANA", "Cuenca Chira"), "CAÑAD": ("CAJAMARCA", "SANTA CRUZ", "Cuenca Chancay-Lambayeque"),
       "SANTA MARÍA DE NANAY": ("LORETO", "MAYNAS", "Cuenca Nanay"), "TAMSHIYACU": ("LORETO", "MAYNAS", "Intercuenca 49797"),
       "ENAPU PERÚ": ("LORETO", "MAYNAS", "Cuenca Itaya"), "PTE. AGUAYTÍA": ("UCAYALI", "PADRE ABAD", "Cuenca Aguaytía"),
       "SAN REGIS": ("LORETO", "LORETO", "Intercuenca Bajo Marañón"), "LAGUNAS": ("LORETO", "ALTO AMAZONAS", "Intercuenca Bajo Huallga"),
       "PUERTO ALEGRIA": ("LORETO", "MARISCAL RAMON CASTILLA", "Intercuenca 4977"), "NAUTA": ("LORETO", "LORETO", "Intercuenca Bajo Marañón"),
       "HUALLAPE": ("CAJAMARCA", "JAEN", "Cuenca Chinchipe")}


def lluvia(ruta):
    texto = open(ruta, encoding="utf-8").read()
    avisos_txt, zonas_txt = texto.split("#ZONAS")
    meta = {l.split("|")[0]: l.split("|") for l in avisos_txt.replace("#AVISOS", "").strip().splitlines()}
    out = []
    for l in zonas_txt.strip().splitlines():
        n, m, f, dep, p2, p3, p4 = l.strip().split("|")
        _, tit, emi, ini, fin, niv = meta[n]
        out.append(dict(aviso=n, titulo=tit, nivel_aviso=niv, emision=emi, inicio=ini, fin=fin, mapa=m, fecha=f,
                        departamento=dep, pct_area_amarillo_o_mas=p2, pct_area_naranja_o_mas=p3, pct_area_rojo=p4,
                        fuente_url=URLM.format(n=n, m=m, a=ini[:4])))
    return out


def rios(ruta):
    out = []
    for l in open(ruta, encoding="utf-8").read().strip().splitlines():
        num, tit, ini, fin, horas, niv = l.split("|")
        m = re.search(r"R[ÍI]O\s+(.+?)\s+-\s+ESTACI[ÓO]N\s+(.+)$", tit)
        rio, est = (m.group(1).strip(), m.group(2).strip()) if m else ("", "")
        tipo = "incremento" if tit.startswith("INCREMENTO") else "descenso" if "DESCENSO" in tit else "situación actual"
        dep, prov, cuenca = EST.get(est, ("", "", ""))
        out.append(dict(aviso=num, titulo=tit, rio=rio.title(), estacion=est.title(), tipo=tipo, inicio=ini, fin=fin, horas=horas,
                        nivel=niv, departamento=dep, provincia=prov, cuenca=cuenca,
                        ubicacion="estación del mapa del SENAMHI cruzada con límites del INEI (IDESEP)" if dep
                        else "sin ubicar: la estación no figura en el mapa de estaciones del SENAMHI",
                        fuente_url="https://www.senamhi.gob.pe/?p=avisos-hidrologicos"))
    return out


def escribir(nombre, filas):
    with open(os.path.join(DATOS, nombre), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    ll, rr = lluvia(sys.argv[1]), rios(sys.argv[2])
    escribir("avisos_senamhi_lluvia.csv", ll)
    escribir("avisos_senamhi_rios.csv", rr)
    print(f"Lluvia: {len({r['aviso'] for r in ll})} avisos, {len(ll)} filas. Ríos: {len(rr)} avisos, {Counter(r['nivel'] for r in rr)}.")
    sin = sorted({r["estacion"] for r in rr if not r["departamento"]})
    if sin:
        print("Estaciones sin ubicar:", ", ".join(sin))
