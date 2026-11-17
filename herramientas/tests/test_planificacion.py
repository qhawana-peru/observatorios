"""Controles del Museo de la planificación: el catálogo es coherente y la página se genera."""
import csv, importlib.util, os, re, json

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PL = os.path.join(RAIZ, "planificacion")


def leer(n):
    with open(os.path.join(PL, "catalogo", n), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_ids_unicos_y_referencias():
    ids = [p["id"] for p in leer("planes.csv")]
    assert len(ids) == len(set(ids))
    for tabla in ("versiones.csv", "reportes.csv", "notas.csv", "fuentes.csv", "objetivos.csv", "indicadores.csv"):
        for r in leer(tabla):
            assert r["plan_id"] in ids, (tabla, r["plan_id"])


def test_26_pliegos_regionales():
    assert sum(1 for p in leer("planes.csv") if p["eje"] == "territorial") == 26


def test_toda_pieza_tiene_fuente():
    con = {f["plan_id"] for f in leer("fuentes.csv") if f["url"].startswith("http")}
    assert all(p["id"] in con for p in leer("planes.csv"))


def test_hallazgos_completos():
    for h in leer("hallazgos.csv"):
        for c in ("observamos", "por_que", "pregunta", "fuentes"):
            assert h[c].strip(), (h["id"], c)


def test_kpis_estados_validos():
    assert {k["estado"] for k in leer("kpis.csv")} <= {"activo", "piloto", "revision", "etapa2"}


def test_pagina_se_genera(tmp_path):
    spec = importlib.util.spec_from_file_location("b", os.path.join(PL, "build.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.main(str(tmp_path))
    html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "__" not in re.sub(r"<script.*?</script>", "", html, flags=re.S).replace("__proto__", "")
    datos = json.loads(re.search(r'<script id="datos" type="application/json">(.*?)</script>', html, re.S).group(1).replace("<\\/", "</"))
    assert len(datos["piezas"]) == len(leer("planes.csv"))
    assert (tmp_path / "datos" / "kpis.csv").exists()
