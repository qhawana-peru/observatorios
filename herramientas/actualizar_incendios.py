"""Actualiza los datos del monitor de incendios a partir de una consulta a SERFOR.

Uso:
    python herramientas/actualizar_incendios.py incendios/cortes/serfor_AAAA-MM-DD.json [--nota "texto"]

El archivo JSON lo genera herramientas/serfor_consulta.js desde un navegador.
El script reescribe los CSV de incendios/datos/, agrega la fila del corte en
seguimiento_proyeccion.csv (sin tocar las de cortes anteriores) y cambia la
fecha de corte en incendios/config/sitio.json. Al final imprime un resumen
para escribir la lectura del corte.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sitio_incendios import cuantil  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "incendios", "datos")
CONFIG = os.path.join(RAIZ, "incendios", "config", "sitio.json")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
MES_CORTO = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
ESTADOS = {1: ("alertado", "Sin verificar (alertado)"), 2: ("confirmado", "Confirmadas"),
           3: ("controlado", "Controladas"), 4: ("extinguido", "Extinguidas")}
CAPA0 = "0: Alerta de Incendio Forestal"
CAPA2 = "2: Focos de Calor"
# SERFOR escribe los nombres en mayúsculas y sin tildes.
TILDES = {"LA CONVENCION": "La Convención", "CELENDIN": "Celendín", "CONTUMAZA": "Contumazá",
          "JAEN": "Jaén", "QUISPICANCHI": "Quispicanchi", "ESPINAR": "Espinar"}


def leer(nombre: str) -> list[dict]:
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escribir(nombre: str, filas: list[dict], campos: list[str]) -> None:
    with open(os.path.join(DATOS, nombre), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def d(texto: str) -> date:
    return date.fromisoformat(texto)


def dia_mes(x: date) -> str:
    return f"{x.day} de {MESES[x.month - 1]}"


def periodo(desde: str | None, hasta: str | None, corte: date, vacio: str) -> str:
    if not desde:
        return f"{vacio} al {dia_mes(corte)}"
    a, b = d(desde), d(hasta)
    if a == b:
        return dia_mes(a)
    if a.month == b.month:
        return f"{a.day} al {b.day} de {MESES[b.month - 1]}"
    return f"{dia_mes(a)} al {dia_mes(b)}"


def periodo_corto(desde: str, hasta: str) -> str:
    a, b = d(desde), d(hasta)
    if a.month == b.month:
        return f"{a.day} al {b.day} {MES_CORTO[b.month - 1]} {b.year}"
    return f"{a.day} {MES_CORTO[a.month - 1]} al {b.day} {MES_CORTO[b.month - 1]} {b.year}"


def nombre_provincia(x: str) -> str:
    return TILDES.get(x, x.title())


def rango_publicado(historial: list[dict], region: str) -> tuple[int, int]:
    previas = [float(r["adicional_pct"]) for r in historial
               if r["region"] == region and r["adicional_pct"] not in ("", None)]
    return round(cuantil(previas, .25)), round(cuantil(previas, .75))


CAMPOS_DEP = ["fecha_corte", "departamento", "alertas", "alertas_activas", "alertas_desde", "alertas_hasta",
              "focos_3d", "focos_anio_menos2", "focos_anio_menos1", "focos_anio", "periodo_anual"]


def sin_tildes(x: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", x.upper()) if unicodedata.category(c) != "Mn")


def nombre_departamento(x: str) -> str:
    n = x.title().replace(" De ", " de ").replace(" Del ", " del ")
    return {"Apurimac": "Apurímac", "Ancash": "Áncash", "Huanuco": "Huánuco", "Junin": "Junín",
            "San Martin": "San Martín"}.get(n, n)


def panorama(D: dict, corte: date) -> list[dict]:
    """Una fila por departamento: alertas recientes (activas = alertadas o confirmadas), focos de 3 días y
    focos del 1 de enero a la fecha del corte en tres años. Departamentos sin nada no aparecen."""
    anio = corte.year
    filas = {}

    def f(dep):
        return filas.setdefault(dep, {"fecha_corte": corte.isoformat(), "departamento": nombre_departamento(dep),
                                      "alertas": 0, "alertas_activas": 0, "alertas_desde": "", "alertas_hasta": "",
                                      "focos_3d": 0, "focos_anio_menos2": 0, "focos_anio_menos1": 0, "focos_anio": 0,
                                      "periodo_anual": f"1 ene al {corte.day} {MES_CORTO[corte.month - 1]}"})
    for a in D["alertas_estado"]:
        if not a["dep"]:
            continue
        r = f(a["dep"])
        r["alertas"] += a["n"]
        if a["estado"] in (1, 2):
            r["alertas_activas"] += a["n"]
        if a["desde"] and (not r["alertas_desde"] or a["desde"] < r["alertas_desde"]):
            r["alertas_desde"] = a["desde"]
        if a["hasta"] and a["hasta"] > r["alertas_hasta"]:
            r["alertas_hasta"] = a["hasta"]
    for dep, n in D["focos_3d"].items():
        if dep:
            f(dep)["focos_3d"] = n
    for y, campo in ((anio - 2, "focos_anio_menos2"), (anio - 1, "focos_anio_menos1"), (anio, "focos_anio")):
        for dep, n in D["focos_anual"].get(str(y), D["focos_anual"].get(y, {})).items():
            if dep:
                f(dep)[campo] = n
    # Orden alfabético a propósito: el método no compara regiones entre sí (docs/incendios-metodologia.md).
    return sorted(filas.values(), key=lambda r: sin_tildes(r["departamento"]))


def actualizar(consulta: dict, nota: str | None = None) -> dict:
    corte = d(consulta["corte"])
    anio = corte.year
    regiones = consulta["regiones"]

    # 1. Alertas recientes y focos de 3 días
    alertas = []

    def fila(reg, ind, desc, valor, per, capa):
        alertas.append({"fecha_corte": corte.isoformat(), "region": reg, "indicador": ind,
                        "descripcion": desc, "valor": valor, "periodo": per, "capa_serfor": capa})

    for reg, R in regiones.items():
        est = {e["clave"]: e for e in R["alertas_estado"]}
        desdes = [e["desde"] for e in est.values() if e["desde"]]
        hastas = [e["hasta"] for e in est.values() if e["hasta"]]
        per = periodo(min(desdes) if desdes else None, max(hastas) if hastas else None,
                      corte, "sin alertas en el sistema")
        fila(reg, "alertas", "Alertas recientes en el sistema", sum(e["n"] for e in est.values()), per, CAPA0)
        for codigo, (ind, desc) in ESTADOS.items():
            fila(reg, ind, desc, est.get(codigo, {"n": 0})["n"], per, CAPA0)
        f3 = R["focos_3d"]
        fila(reg, "focos_3d", "Focos de calor", f3["n"],
             periodo(f3["desde"], f3["hasta"], corte, "sin focos"), CAPA2)
    P = consulta["peru"]
    fila("Perú", "alertas", "Alertas recientes en todo el país", P["alertas"]["n"],
         periodo(P["alertas"]["desde"], P["alertas"]["hasta"], corte, "sin alertas en el sistema"), CAPA0)
    fila("Perú", "focos_3d", "Focos de calor en todo el país", P["focos_3d"]["n"],
         periodo(P["focos_3d"]["desde"], P["focos_3d"]["hasta"], corte, "sin focos"), CAPA2)
    escribir("serfor_alertas_recientes.csv", alertas, list(alertas[0]))

    # 2. Alertas por provincia (el periodo es el de las alertas de toda la región)
    prov = []
    for reg, R in regiones.items():
        est = R["alertas_estado"]
        if not est:
            continue
        per = periodo_corto(min(e["desde"] for e in est), max(e["hasta"] for e in est))
        for p in sorted(R["alertas_provincia"], key=lambda p: (-p["n"], p["clave"])):
            prov.append({"fecha_corte": corte.isoformat(), "region": reg,
                         "provincia": nombre_provincia(p["clave"]), "alertas": p["n"], "periodo": per})
    escribir("serfor_alertas_provincia.csv", prov, ["fecha_corte", "region", "provincia", "alertas", "periodo"])

    # 3. Focos anuales, todos los satélites, mismo periodo cada año
    per_anual = f"1 ene al {corte.day} {MES_CORTO[corte.month - 1]}"
    focos = [{"fecha_corte": corte.isoformat(), "region": reg, "anio": y, "periodo": per_anual,
              "satelites": "todos", "focos": n}
             for reg, R in regiones.items() for y, n in sorted(R["focos_anual"].items())]
    escribir("serfor_focos_anual.csv", focos, list(focos[0]))

    # 3b. Panorama nacional por departamento (cortes desde el 28 oct 2026; los anteriores no lo traen)
    if "departamentos" in consulta:
        escribir("serfor_departamentos.csv", panorama(consulta["departamentos"], corte), CAMPOS_DEP)

    # 4. Seguimiento: se fija el rango publicado en el corte anterior y se agrega el nuevo corte
    historial_previo = leer("serfor_historial_npp.csv")
    seguimiento = leer("seguimiento_proyeccion.csv")
    if any(r["corte"] == corte.isoformat() for r in seguimiento):
        raise SystemExit(f"El corte {corte} ya está en seguimiento_proyeccion.csv. "
                         "Si hay que repetirlo, quita esas filas a mano y vuelve a correr.")
    for reg, R in regiones.items():
        filas = sorted((r for r in seguimiento if r["region"] == reg), key=lambda r: r["corte"])
        if filas and not filas[-1]["rango_bajo_pct"]:
            filas[-1]["rango_bajo_pct"], filas[-1]["rango_alto_pct"] = rango_publicado(historial_previo, reg)
        seguimiento.append({"region": reg, "corte": corte.isoformat(),
                            "focos_npp": R["npp"][str(anio)]["hasta_corte"],
                            "rango_bajo_pct": "", "rango_alto_pct": ""})
    orden = list(regiones)
    seguimiento.sort(key=lambda r: (orden.index(r["region"]) if r["region"] in orden else 99, r["corte"]))
    escribir("seguimiento_proyeccion.csv", seguimiento, ["region", "corte", "focos_npp", "rango_bajo_pct", "rango_alto_pct"])

    # 5. Historial Suomi NPP a la fecha del corte
    historial = []
    for reg, R in regiones.items():
        for y, v in sorted(R["npp"].items()):
            h, t = v["hasta_corte"], v["total_anio"]
            historial.append({"region": reg, "anio": y, "fecha_referencia": corte.strftime("%m-%d"),
                              "hasta_corte": h, "total_anio": t if t is not None else "",
                              "adicional_pct": round((t - h) / h * 100, 1) if t is not None and h else "",
                              "satelite": "Suomi NPP"})
    escribir("serfor_historial_npp.csv", historial, list(historial[0]))

    # 6. Curva 2026 por semana: la semana k termina el día 7k del año; la última llega al corte
    curvas = leer("serfor_curvas_npp.csv")
    semana_corte = math.ceil(corte.timetuple().tm_yday / 7)
    for reg, R in regiones.items():
        total = R["npp"][str(anio)]["hasta_corte"]
        diario = {d(k): n for k, n in R["npp_diario"].items()}
        propias = [r for r in curvas if r["region"] == reg and r["anio"] == str(anio)]
        ultima = max((int(r["semana"]) for r in propias), default=1)
        valores = {}
        for k in range(ultima, semana_corte + 1):
            fin = min(date(anio, 1, 1) + timedelta(days=7 * k - 1), corte)
            valores[k] = total - sum(n for dia, n in diario.items() if dia > fin)
        curvas = [r for r in curvas if not (r["region"] == reg and r["anio"] == str(anio) and int(r["semana"]) >= ultima)]
        curvas += [{"region": reg, "anio": str(anio), "semana": str(k), "acumulado": v, "satelite": "Suomi NPP"}
                   for k, v in valores.items()]
    curvas.sort(key=lambda r: (orden.index(r["region"]), int(r["anio"]), int(r["semana"])))
    escribir("serfor_curvas_npp.csv", curvas, ["region", "anio", "semana", "acumulado", "satelite"])

    # 7. Configuración del sitio
    with open(CONFIG, encoding="utf-8") as f:
        sitio = json.load(f)
    sitio["fecha_corte"] = corte.isoformat()
    sitio["nota_corte"] = nota or ""
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(sitio, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return resumen(consulta, historial)


def resumen(consulta: dict, historial: list[dict]) -> dict:
    corte = d(consulta["corte"])
    out = {"corte": corte.isoformat(), "regiones": {}}
    for reg, R in consulta["regiones"].items():
        diario = {d(k): n for k, n in R["npp_diario"].items()}
        ult = sum(n for dia, n in diario.items() if corte - timedelta(days=7) < dia <= corte)
        prev = sum(n for dia, n in diario.items() if corte - timedelta(days=14) < dia <= corte - timedelta(days=7))
        p25, p75 = rango_publicado(historial, reg)
        out["regiones"][reg] = {
            "alertas": sum(e["n"] for e in R["alertas_estado"]),
            "focos_npp_ultimos_7_dias": ult, "focos_npp_7_dias_previos": prev,
            "cambio_pct": round((ult / prev - 1) * 100) if prev else None,
            "rango_restante_pct": [p25, p75]}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("consulta", help="JSON generado por serfor_consulta.js")
    ap.add_argument("--nota", help="Lectura breve del corte para mostrar en la página")
    args = ap.parse_args()
    with open(args.consulta, encoding="utf-8") as f:
        consulta = json.load(f)
    r = actualizar(consulta, args.nota)
    print(f"Corte {r['corte']} aplicado.")
    for reg, v in r["regiones"].items():
        cambio = "sin datos previos" if v["cambio_pct"] is None else f"{v['cambio_pct']:+d} %"
        print(f"- {reg}: {v['alertas']} alertas; focos Suomi NPP últimos 7 días: {v['focos_npp_ultimos_7_dias']} "
              f"(7 días previos: {v['focos_npp_7_dias_previos']}, {cambio}); "
              f"faltaría +{v['rango_restante_pct'][0]} a +{v['rango_restante_pct'][1]} %.")
    if not args.nota:
        print("Falta la lectura del corte: escríbela en incendios/config/sitio.json (campo nota_corte).")


if __name__ == "__main__":
    main()
