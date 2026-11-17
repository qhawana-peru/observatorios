import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import construir_sitio as cs  # noqa: E402


class TestAvisos(unittest.TestCase):
    def setUp(self):
        self.a = cs.construir_avisos(date(2026, 11, 17))

    def test_niveles_coinciden_con_la_tabla_del_senamhi(self):
        # El nivel máximo en el mapa de cada aviso debe ser el que el SENAMHI publica en su tabla.
        import csv
        filas = list(csv.DictReader(open(os.path.join(cs.EN, "datos", "avisos_senamhi_lluvia.csv"), encoding="utf-8")))
        nivel = {"AMARILLO": 2, "NARANJA": 3, "ROJO": 4}
        mx = {}
        for r in filas:
            lv = 4 if float(r["pct_area_rojo"]) > 0 else 3 if float(r["pct_area_naranja_o_mas"]) > 0 else 2
            mx[r["aviso"]] = max(mx.get(r["aviso"], 0), lv)
        for r in filas:
            self.assertEqual(mx[r["aviso"]], nivel[r["nivel_aviso"]], r["aviso"])

    def test_dias_futuros_no_cuentan(self):
        tumbes = self.a["matriz"]["TUMBES"]
        pasados = sum(1 for f in self.a["dias"] if f <= "2026-11-17")
        self.assertEqual(self.a["resumen"]["TUMBES"]["dias2"], sum(c >= "2" for c in tumbes[:pasados]))

    def test_territorio_no_cuenta_dos_veces(self):
        t = cs.dias_territorio(self.a, ["LIMA", "CALLAO"])
        self.assertLessEqual(t["naranja"], self.a["resumen"]["LIMA"]["dias3"] + self.a["resumen"]["CALLAO"]["dias3"])
        uno = cs.dias_territorio(self.a, ["LIMA"])
        self.assertEqual(uno["naranja"], self.a["resumen"]["LIMA"]["dias3"])


if __name__ == "__main__":
    unittest.main()
