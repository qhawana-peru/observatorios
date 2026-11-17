"""Resume los agregados de mortalidad del SINADEF para la vista «De qué morimos».

Entrada: salud/datos/mortalidad_sinadef_agregados.json, producido por salud/sinadef_agregar.js
(se ejecuta en un navegador sobre el archivo abierto fallecidos_sinadef.csv del MINSA, sin
descargar los registros individuales: solo cuenta).
Salida: salud/datos/mortalidad_sinadef_resumen.json y mortalidad_sinadef_subgrupos.csv.

Reglas (las mismas del script de agregación):
- Causa básica aproximada: la última causa con código CIE-10 válido en la secuencia A→D.
- Si el campo MUERTE VIOLENTA dice accidente de tránsito, homicidio, suicidio, otro accidente o
  accidente de trabajo, la muerte va al grupo III (lesiones).
- Grupos: I transmisibles, maternas, perinatales y nutricionales; II no transmisibles;
  III lesiones; X mal definidas, poco informativas o sin código.
"""
import csv, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
GRUPOS = {
    "I": {"n": "Transmisibles, maternas, perinatales y nutricionales", "c": "#3FA488"},
    "II": {"n": "No transmisibles", "c": "#5F86DA"},
    "III": {"n": "Lesiones", "c": "#D9668F"},
    "X": {"n": "Mal definidas, poco informativas o sin código", "c": "#8A94A6"},
}
ORDEN_SEGURO = ["SIS", "ESSALUD", "PRIVADOS", "SANIDAD FFAA", "SANIDAD PNP", "OTROS", "USUARIO", "EXONERADO", "IGNORADO"]
ORDEN_EDAD = ["<1", "1-4", "5-14", "15-29", "30-59", "60-79", "80+", "sin dato"]
UMBRAL = 5  # celdas menores se ocultan en cortes finos


def main(corte="15/09/2026", consulta="17/11/2026", parcial=2024, ultimo=2023, hasta="05/05/2024"):
    raw = json.load(open(os.path.join(DATOS, "mortalidad_sinadef_agregados.json"), encoding="utf-8"))
    GK = raw["grupos"]
    anios = sorted(int(a) for a in raw["G"])
    parcial, ultimo = int(parcial), int(ultimo)

    def vacio():
        return {"I": 0, "II": 0, "III": 0, "X": 0, "total": 0}

    por_anio = {a: vacio() for a in anios}
    sub = {}
    for a in anios:
        lista = []
        for clave, n in zip(raw["A"]["S"], raw["A"]["M"][str(a)]):
            g, s_ = clave.split("|")
            por_anio[a][g] += n
            por_anio[a]["total"] += n
            if n:
                lista.append({"g": g, "s": s_, "n": n})
        lista.sort(key=lambda x: (x["g"] == "X", -x["n"]))
        sub[a] = lista
        assert por_anio[a]["total"] == raw["G"][str(a)]["total"], a

    def cruce(clave, renombre=None, omitir=()):
        out = {}
        for a in anios:
            tabla = {}
            for c, v in zip(raw[clave]["C"], raw[clave]["M"][str(a)]):
                c = (renombre or {}).get(c, c)
                if c in omitir:
                    continue
                fila = tabla.setdefault(c, vacio())
                for g, n in zip(GK, v):
                    fila[g] += n
                    fila["total"] += n
            for c in list(tabla):
                if tabla[c]["total"] == 0:
                    del tabla[c]
                    continue
                for g in GK:  # celdas pequeñas: no se publican en cortes finos
                    if 0 < tabla[c][g] < UMBRAL:
                        tabla[c][g] = 0
            out[a] = tabla
        return out

    sindato = {"SIN DATO": "DEPARTAMENTO SIN DATO", "SIN REGISTRO": "DEPARTAMENTO SIN DATO", "EXTRANJERO O SIN DATO": "EXTRANJERO O PAÍS SIN DATO"}
    dep = cruce("B", sindato)
    seguro = cruce("C", {"SIN REGISTRO": "IGNORADO", "SOAT": "OTROS"})
    edad = cruce("D")
    calidad = {a: raw["G"][str(a)] for a in anios}
    # Alertas de cobertura: un departamento cuyo registro cae a menos de la mitad del año anterior
    # (o salta a más del doble) no cambió de mortalidad: cambió lo que llega al archivo abierto.
    alertas = []
    completos = [a for a in anios if a != parcial]
    for a0, a1 in zip(completos, completos[1:]):
        for d in sorted(set(dep[a0]) | set(dep[a1])):
            n0 = dep[a0].get(d, {}).get("total", 0)
            n1 = dep[a1].get(d, {}).get("total", 0)
            if max(n0, n1) >= 500 and (n1 < n0 * 0.5 or n1 > n0 * 2) and not (a1 in (2020, 2021) and n1 > n0):
                alertas.append({"dep": d, "de": a0, "a": a1, "n0": n0, "n1": n1})
    res = {"corte": corte, "consulta": consulta, "parcial": parcial, "ultimo": ultimo, "anios": anios, "filas": raw["filas"],
           "grupos": GRUPOS, "porAnio": por_anio, "sub": sub, "seguro": seguro, "edad": edad, "dep": dep,
           "calidad": calidad, "alertas": alertas, "hasta": hasta, "ordenSeguro": ORDEN_SEGURO, "ordenEdad": ORDEN_EDAD,
           "notaEF": "Las causas E y F no entran en la regla: el diccionario no dice si son parte de la cadena o «otros estados» (parte II del certificado)."}
    json.dump(res, open(os.path.join(DATOS, "mortalidad_sinadef_resumen.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(DATOS, "mortalidad_sinadef_subgrupos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["anio", "grupo", "subgrupo", "defunciones_registradas", "porcentaje", "nota"])
        for a in anios:
            for x in sub[a]:
                w.writerow([a, x["g"], x["s"], x["n"], round(x["n"] / por_anio[a]["total"] * 100, 2), "año incompleto en el archivo abierto" if a == parcial else ""])
    print("Alertas de cobertura:", alertas)
    return res


if __name__ == "__main__":
    r = main(*sys.argv[1:])
    for a in r["anios"]:
        t = r["porAnio"][a]
        print(a, t["total"], {g: round(t[g] / t["total"] * 100, 1) for g in ("I", "II", "III", "X")})
