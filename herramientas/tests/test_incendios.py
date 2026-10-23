"""Pruebas del Monitor de incendios: datos completos y reglas de las pistas."""
import csv
import os
import sys
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import sitio_incendios as si  # noqa: E402

DATOS = os.path.join(si.INC, "datos")


def leer(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class Datos(unittest.TestCase):
    def test_cada_region_tiene_alertas_y_focos(self):
        filas = leer("serfor_alertas_recientes.csv")
        for reg in si.REGIONES:
            ind = {r["indicador"] for r in filas if r["region"] == reg}
            self.assertTrue({"alertas", "alertado", "confirmado", "controlado", "extinguido", "focos_3d"} <= ind, reg)

    def test_estados_suman_el_total_de_alertas(self):
        filas = leer("serfor_alertas_recientes.csv")
        for reg in si.REGIONES:
            v = {r["indicador"]: int(r["valor"]) for r in filas if r["region"] == reg}
            self.assertEqual(v["alertado"] + v["confirmado"] + v["controlado"] + v["extinguido"], v["alertas"], reg)

    def test_curvas_no_decrecen(self):
        series = {}
        for r in leer("serfor_curvas_npp.csv"):
            series.setdefault((r["region"], r["anio"]), []).append(int(r["acumulado"]))
        for clave, s in series.items():
            self.assertEqual(s, sorted(s), clave)
        self.assertNotIn(("Cusco", "2022"), series, "2022 se excluye por la interrupción de Suomi NPP")

    def test_cuantil_lineal(self):
        self.assertEqual(si.cuantil([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(si.cuantil([10, 20, 30], 0.25), 15)


class Pistas(unittest.TestCase):
    CAMPOS = ["id", "region", "tema", "dato", "fuente_original", "medio", "fecha_nota", "url",
              "pregunta", "donde_verificar", "estado", "registrada", "vence"]
    ESTADOS = {"sin verificar", "verificada", "corregida", "descartada"}

    def test_campos_y_estados(self):
        filas = leer("pistas.csv")
        self.assertEqual(list(filas[0].keys()), self.CAMPOS)
        ids = [p["id"] for p in filas]
        self.assertEqual(len(ids), len(set(ids)), "ids repetidos")
        for p in filas:
            self.assertIn(p["estado"], self.ESTADOS, p["id"])
            for u in p["url"].split():
                self.assertTrue(u.startswith("https://"), p["id"])

    def test_vencen_a_los_30_dias(self):
        for p in leer("pistas.csv"):
            dias = (date.fromisoformat(p["vence"]) - date.fromisoformat(p["registrada"])).days
            self.assertLessEqual(dias, 30, p["id"])

    def test_vencidas_no_se_muestran(self):
        filas = leer("pistas.csv")
        self.assertEqual(si.pistas_vigentes(filas, date(2099, 1, 1)), [])
        vig = si.pistas_vigentes(filas, date.fromisoformat(filas[0]["registrada"]))
        self.assertTrue(all(p["estado"] == "sin verificar" for p in vig))

    def test_pistas_fuera_de_los_calculos(self):
        datos = si.construir_datos(date(2026, 10, 23))
        texto = str({k: v for k, v in datos.items() if k not in ("pistas",)})
        for p in leer("pistas.csv"):
            self.assertNotIn(p["dato"], texto, p["id"])


if __name__ == "__main__":
    unittest.main()
