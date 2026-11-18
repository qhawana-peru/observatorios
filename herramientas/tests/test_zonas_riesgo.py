import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import construir_sitio as cs  # noqa: E402

RUTA = os.path.join(cs.EN, "datos", "riesgo_distritos_cenepred.csv")


class TestZonasRiesgo(unittest.TestCase):
    """Los CSV derivados de los Excel del CENEPRED deben cuadrar con los totales que el propio CENEPRED imprime
    en las hojas de resumen de esos Excel (consultados el 18 nov 2026)."""

    def setUp(self):
        self.f = list(csv.DictReader(open(RUTA, encoding="utf-8")))

    def cuenta(self, col, nivel="4"):
        return sum(r[col] == nivel for r in self.f)

    def suma(self, campo, col, nivel="4"):
        return sum(int(r[campo] or 0) for r in self.f if r[col] == nivel)

    def test_escenario_el_nino_actualizado(self):
        # Hoja Resumen_Inund y Tabla Resumen (movimientos en masa), "Total general"
        self.assertEqual((self.cuenta("a_inu"), self.suma("pob", "a_inu")), (209, 7951322))
        self.assertEqual((self.cuenta("a_inu", "3"), self.suma("pob", "a_inu", "3")), (557, 11963523))
        self.assertEqual((self.cuenta("a_mm"), self.suma("pob", "a_mm")), (185, 1383000))

    def test_verano_2027_octubre(self):
        # Hojas Resumen_ERInund y Resumen_ERMMasa: población en zonas de mayor susceptibilidad
        self.assertEqual((self.cuenta("b_inu"), self.suma("b_pinu", "b_inu")), (153, 5323000))
        self.assertEqual((self.cuenta("b_inu", "3"), self.suma("b_pinu", "b_inu", "3")), (289, 3683797))
        self.assertEqual((self.cuenta("b_mm"), self.suma("b_pmm", "b_mm")), (787, 3912232))

    def test_ubigeos_unicos_y_validos(self):
        u = [r["ubigeo"] for r in self.f]
        self.assertEqual(len(u), len(set(u)))
        self.assertTrue(all(len(x) == 6 and x.isdigit() and r["dist"] for x, r in zip(u, self.f)))

    def test_lima(self):
        r = cs.construir_riesgo()
        self.assertEqual(len(r["lima"]), 50)
        self.assertEqual(sum(d[3] for d in r["lima"]), 609586)


if __name__ == "__main__":
    unittest.main()
