"""Pruebas del script que aplica una consulta de SERFOR a los datos del monitor."""
import csv
import json
import os
import shutil
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import actualizar_incendios as ai  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(AQUI))
EJEMPLO = os.path.join(AQUI, "datos", "serfor_ejemplo.json")


def leer(carpeta, nombre):
    with open(os.path.join(carpeta, nombre), encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    """Copia los datos del repositorio y deja el seguimiento como estaba antes del corte de ejemplo."""
    consulta = json.load(open(EJEMPLO, encoding="utf-8"))
    datos = tmp_path / "datos"
    shutil.copytree(os.path.join(RAIZ, "incendios", "datos"), datos)
    seg = [r for r in leer(datos, "seguimiento_proyeccion.csv") if r["corte"] < consulta["corte"]]
    for reg in consulta["regiones"]:
        filas = [r for r in seg if r["region"] == reg]
        filas[-1]["rango_bajo_pct"] = filas[-1]["rango_alto_pct"] = ""
    with open(datos / "seguimiento_proyeccion.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(seg[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(seg)
    config = tmp_path / "sitio.json"
    shutil.copy(os.path.join(RAIZ, "incendios", "config", "sitio.json"), config)
    monkeypatch.setattr(ai, "DATOS", str(datos))
    monkeypatch.setattr(ai, "CONFIG", str(config))
    return consulta, str(datos), str(config), seg


def test_aplica_corte(entorno):
    consulta, datos, config, seg_antes = entorno
    ai.actualizar(consulta, "nota de prueba")
    corte = consulta["corte"]
    alertas = leer(datos, "serfor_alertas_recientes.csv")
    for reg in consulta["regiones"]:
        v = {r["indicador"]: int(r["valor"]) for r in alertas if r["region"] == reg}
        assert v["alertas"] == v["alertado"] + v["confirmado"] + v["controlado"] + v["extinguido"]
    seg = leer(datos, "seguimiento_proyeccion.csv")
    for reg, R in consulta["regiones"].items():
        filas = [r for r in seg if r["region"] == reg]
        assert filas[-1]["corte"] == corte
        assert int(filas[-1]["focos_npp"]) == R["npp"][corte[:4]]["hasta_corte"]
        assert filas[-2]["rango_bajo_pct"] and filas[-2]["rango_alto_pct"], "el rango publicado queda registrado"
        antes = [r for r in seg_antes if r["region"] == reg]
        assert [r["focos_npp"] for r in filas[:-1]] == [r["focos_npp"] for r in antes], "no se reescriben cortes pasados"
    for r in leer(datos, "serfor_historial_npp.csv"):
        if r["total_anio"]:
            h, t = int(r["hasta_corte"]), int(r["total_anio"])
            assert float(r["adicional_pct"]) == round((t - h) / h * 100, 1)
    curvas = leer(datos, "serfor_curvas_npp.csv")
    for reg, R in consulta["regiones"].items():
        c = [int(r["acumulado"]) for r in curvas if r["region"] == reg and r["anio"] == corte[:4]]
        assert c == sorted(c) and c[-1] == R["npp"][corte[:4]]["hasta_corte"]
    sitio = json.load(open(config, encoding="utf-8"))
    assert sitio["fecha_corte"] == corte and sitio["nota_corte"] == "nota de prueba"


def test_no_repite_un_corte(entorno):
    consulta = entorno[0]
    ai.actualizar(consulta)
    with pytest.raises(SystemExit):
        ai.actualizar(consulta)


def test_periodos():
    from datetime import date
    assert ai.periodo("2026-10-09", "2026-10-23", date(2026, 10, 23), "x") == "9 al 23 de octubre"
    assert ai.periodo("2026-09-28", "2026-10-02", date(2026, 10, 2), "x") == "28 de septiembre al 2 de octubre"
    assert ai.periodo(None, None, date(2026, 10, 23), "sin focos") == "sin focos al 23 de octubre"
    assert ai.nombre_provincia("LA CONVENCION") == "La Convención"
