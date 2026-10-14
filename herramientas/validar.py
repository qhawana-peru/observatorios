"""Corre los seis controles de la Guía de descarga sobre un corte del MEF.

Uso:
    python herramientas/validar.py el-nino/fuentes/mef/2026-10-26
    python herramientas/validar.py el-nino/fuentes/mef/2026-10-26 --informe informe.md

Un corte es una carpeta con fecha (AAAA-MM-DD) que contiene los siete archivos
D1 a D7, nombrados como dice la guía: AAAAMMDD_PP0068_D2_GR-actividades_p1de1.xls

Sale con código 1 si algún control falla, para que la revisión automática
marque el cambio como no aprobable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mef  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RAIZ, "el-nino", "config", "rutas.json")
PATRON = re.compile(r"^(\d{8})_PP0068_(D\d)_.*?_p(\d+)de(\d+)\.xls$", re.I)
UMBRAL_CAMBIO = 0.10


@dataclass
class Resultado:
    nombre: str
    ok: bool = True
    errores: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def error(self, msg):
        self.ok = False
        self.errores.append(msg)


def cargar_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def leer_corte(carpeta: str) -> tuple[dict[str, mef.ArchivoMEF], list[str]]:
    """Lee los archivos de una carpeta. Une las páginas de un mismo código."""
    archivos: dict[str, mef.ArchivoMEF] = {}
    problemas: list[str] = []
    paginas: dict[str, dict[int, int]] = {}
    for nombre in sorted(os.listdir(carpeta)):
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta) or nombre.startswith("."):
            continue
        if nombre.lower().endswith((".md", ".json", ".txt")):
            continue
        m = PATRON.match(nombre)
        if not m:
            problemas.append(f"`{nombre}` no sigue la convención de nombres de la guía "
                             "(AAAAMMDD_PP0068_D#_detalle_p#de#.xls).")
            continue
        _, codigo, pag, total = m.groups()
        codigo = codigo.upper()
        try:
            leido = mef.leer_archivo(ruta)
        except ValueError as e:
            problemas.append(f"`{nombre}`: {e}")
            continue
        paginas.setdefault(codigo, {})[int(pag)] = int(total)
        if codigo in archivos:
            archivos[codigo].filas.extend(leido.filas)
        else:
            archivos[codigo] = leido
    for codigo, pags in paginas.items():
        total = max(pags.values())
        faltan = [p for p in range(1, total + 1) if p not in pags]
        if faltan:
            problemas.append(f"{codigo}: faltan las páginas {', '.join(map(str, faltan))} de {total}.")
    return archivos, problemas


def corte_anterior(carpeta: str) -> str | None:
    base = os.path.dirname(os.path.abspath(carpeta))
    actual = os.path.basename(os.path.abspath(carpeta))
    previas = sorted(d for d in os.listdir(base)
                     if re.match(r"^\d{4}-\d{2}-\d{2}$", d) and d < actual)
    return os.path.join(base, previas[-1]) if previas else None


def pim_previo_en_datos(fecha: str) -> tuple[str | None, dict]:
    """Si no hay carpeta anterior, compara con el último corte publicado en los datos abiertos."""
    import csv
    ruta = os.path.join(RAIZ, "el-nino", "datos", "ejecucion_pp0068.csv")
    if not os.path.exists(ruta):
        return None, {}
    with open(ruta, encoding="utf-8", newline="") as fh:
        filas = [r for r in csv.DictReader(fh) if r["fecha_corte"] < fecha]
    if not filas:
        return None, {}
    ultima = max(r["fecha_corte"] for r in filas)
    return ultima, {(r["archivo"], r["codigo"]): int(r["pim"]) for r in filas if r["fecha_corte"] == ultima}


def validar(carpeta: str) -> tuple[list[Resultado], dict]:
    cfg = cargar_config()
    fecha = os.path.basename(os.path.abspath(carpeta))
    archivos, problemas = leer_corte(carpeta)
    res: list[Resultado] = []

    # 1. Encabezado correcto
    r = Resultado("Encabezado correcto (fecha, año y opción Incluye)")
    for p in problemas:
        r.error(p)
    for codigo, ruta in cfg["rutas"].items():
        a = archivos.get(codigo)
        if a is None:
            r.error(f"Falta el archivo {codigo} ({ruta['descripcion'].lower()}).")
            continue
        if a.anio != cfg["anio"]:
            r.error(f"{codigo}: el año es {a.anio}, debería ser {cfg['anio']}.")
        if a.incluye != ruta["incluye"]:
            r.error(f"{codigo}: dice «Incluye: {a.incluye}», debería decir «{ruta['incluye']}». "
                    "Repite la ruta desde el paso 3 de la guía.")
        if a.columna and a.columna != ruta["columna"]:
            r.error(f"{codigo}: la primera columna es «{a.columna}», debería ser «{ruta['columna']}». "
                    "Revisa el último botón que pulsaste.")
        if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha) and a.fecha_consulta and a.fecha_consulta != fecha:
            r.error(f"{codigo}: es del {a.fecha_consulta}, pero la carpeta es del {fecha}. "
                    "Todos los archivos de un corte deben bajarse el mismo día.")
    res.append(r)

    # 2. Total de control
    r = Resultado("Total de control del día (D1)")
    d1 = archivos.get("D1")
    niveles = {}
    if d1:
        niveles = {f.codigo: f for f in d1.filas}
        faltan = [n for n in ("E", "M", "R") if n not in niveles]
        if faltan:
            r.error(f"D1 no trae los niveles {', '.join(faltan)}.")
        total_pim = sum(f.pim for f in d1.filas)
        if total_pim > 50_000_000_000:
            r.error(f"El total de D1 es S/ {total_pim:,.0f}: parece todo el presupuesto público. "
                    "Falta el filtro de la Categoría Presupuestal 0068 (paso 4 de la guía).")
    else:
        r.error("Sin D1 no hay total de control.")
    res.append(r)

    # 3. Las partes suman el todo
    r = Resultado("Las partes suman el todo (actividades + proyectos = total del nivel)")
    for a_cod, p_cod, nivel in cfg["pares"]:
        a, p = archivos.get(a_cod), archivos.get(p_cod)
        if not (a and p and nivel in niveles):
            r.error(f"No se puede comprobar {a_cod} + {p_cod}: falta algún archivo.")
            continue
        tol = len(a.filas) + len(p.filas) + 2   # el MEF redondea cada fila a soles
        for campo in ("pim", "devengado"):
            suma = sum(getattr(f, campo) for f in a.filas) + sum(getattr(f, campo) for f in p.filas)
            ref = getattr(niveles[nivel], campo)
            if abs(suma - ref) > tol:
                r.error(f"{a_cod} + {p_cod}: {campo.upper() if campo == 'pim' else 'devengado'} suma "
                        f"S/ {suma:,.0f}, pero D1 dice S/ {ref:,.0f} para el nivel {nivel} "
                        f"(diferencia S/ {suma - ref:,.0f}). Descarga de nuevo los dos archivos.")
    res.append(r)

    # 4. Todas las páginas descargadas
    r = Resultado("Todas las páginas descargadas")
    for codigo, a in archivos.items():
        if not a.filas:
            r.error(f"{codigo} no tiene filas.")
        if len(a.filas) % cfg["tamano_pagina"] == 0 and a.filas:
            r.error(f"{codigo} tiene exactamente {len(a.filas)} filas: probablemente hay otra página.")
        codigos = [f.codigo for f in a.filas]
        rep = sorted({c for c in codigos if codigos.count(c) > 1})
        if rep:
            r.error(f"{codigo} repite filas ({', '.join(rep[:5])}): ¿se subió una página dos veces?")
    res.append(r)

    # 5. Avance recalculado
    r = Resultado("Avance recalculado (devengado ÷ PIM = columna Avance %)")
    for codigo, a in archivos.items():
        malas = [f for f in a.filas if f.pim > 0 and abs(round(f.devengado / f.pim * 100, 1) - f.avance) > 0.15]
        if malas:
            f = malas[0]
            r.error(f"{codigo}: {len(malas)} fila(s) con avance que no cuadra; por ejemplo {f.codigo} "
                    f"({f.devengado:,} ÷ {f.pim:,} ≠ {f.avance} %). Puede que el archivo se haya alterado.")
    res.append(r)

    # 6. Cambios bruscos (solo aviso)
    r = Resultado("Cambios bruscos de presupuesto frente al corte anterior (solo aviso)")
    previa = corte_anterior(carpeta)
    resumen_cambios = []
    antes_pim: dict[tuple[str, str], int] = {}
    fecha_previa = None
    if previa:
        prev, _ = leer_corte(previa)
        fecha_previa = os.path.basename(previa)
        antes_pim = {(c, f.codigo): f.pim for c, a in prev.items() for f in a.filas}
    else:
        fecha_previa, antes_pim = pim_previo_en_datos(fecha)
    if antes_pim:
        for codigo, a in archivos.items():
            for f in a.filas:
                b = antes_pim.get((codigo, f.codigo))
                if b and abs(f.pim - b) / b > UMBRAL_CAMBIO:
                    cambio = (f.pim - b) / b
                    r.avisos.append(f"{codigo} · {f.codigo} {f.nombre.title()}: PIM de S/ {b:,} a "
                                    f"S/ {f.pim:,} ({cambio:+.0%}). Anotar en la propuesta; lo revisa el analista.")
                    resumen_cambios.append({"archivo": codigo, "codigo": f.codigo, "antes": b, "ahora": f.pim})
        if not r.avisos:
            r.avisos.append(f"Ningún PIM cambió más de {UMBRAL_CAMBIO:.0%} frente al corte del {fecha_previa}.")
    else:
        r.avisos.append("Es el primer corte: no hay con qué comparar.")
    res.append(r)

    meta = {"fecha": fecha, "archivos": sorted(archivos), "corte_anterior": fecha_previa,
            "niveles": {k: {"pim": v.pim, "devengado": v.devengado} for k, v in niveles.items()},
            "cambios": resumen_cambios}
    return res, meta


def informe(res: list[Resultado], meta: dict) -> str:
    ok = all(r.ok for r in res)
    lineas = [f"## Validación del corte del {meta['fecha']}", ""]
    lineas.append("**Resultado: todo cuadra. Puede pasar a revisión del comité.**" if ok else
                  "**Resultado: hay problemas. No se puede aprobar hasta corregirlos.**")
    lineas.append("")
    for i, r in enumerate(res, 1):
        marca = "✅" if r.ok else "❌"
        lineas.append(f"{i}. {marca} {r.nombre}")
        for e in r.errores:
            lineas.append(f"   - {e}")
        for a in r.avisos:
            lineas.append(f"   - ⚠️ {a}" if "Ningún" not in a and "primer corte" not in a else f"   - {a}")
    if meta.get("niveles"):
        lineas += ["", "**Totales del PP 0068 (D1)**", "", "| Nivel | PIM | Devengado | Avance |", "| --- | ---: | ---: | ---: |"]
        nombres = {"E": "Nacional", "M": "Municipal", "R": "Regional"}
        tp = td = 0
        for k in ("E", "M", "R"):
            v = meta["niveles"].get(k)
            if v:
                tp += v["pim"]; td += v["devengado"]
                lineas.append(f"| {nombres[k]} | S/ {v['pim']:,} | S/ {v['devengado']:,} | {v['devengado']/v['pim']*100:.1f} % |")
        if tp:
            lineas.append(f"| **Total** | **S/ {tp:,}** | **S/ {td:,}** | **{td/tp*100:.1f} %** |")
    return "\n".join(lineas) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta")
    ap.add_argument("--informe", help="Guardar el informe en este archivo")
    args = ap.parse_args()
    res, meta = validar(args.carpeta)
    texto = informe(res, meta)
    print(texto)
    if args.informe:
        with open(args.informe, "w", encoding="utf-8") as f:
            f.write(texto)
    sys.exit(0 if all(r.ok for r in res) else 1)


if __name__ == "__main__":
    main()
