import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actualizar_incendios as a  # noqa: E402

# Datos de ejemplo con la forma que entrega serfor_consulta.js (no son cifras reales).
EJEMPLO = {
    "alertas_estado": [
        {"dep": "CUSCO", "estado": 2, "n": 41, "desde": "2026-10-25", "hasta": "2026-10-25"},
        {"dep": "CUSCO", "estado": 4, "n": 12, "desde": "2026-10-17", "hasta": "2026-10-25"},
        {"dep": "APURIMAC", "estado": 1, "n": 3, "desde": "2026-10-20", "hasta": "2026-10-26"},
        {"dep": "AMAZONAS", "estado": 4, "n": 5, "desde": "2026-10-10", "hasta": "2026-10-12"},
    ],
    "focos_3d": {"CUSCO": 20, "JUNIN": 7},
    "focos_anual": {"2024": {"CUSCO": 100}, "2025": {"CUSCO": 50, "JUNIN": 9}, "2026": {"CUSCO": 80, "JUNIN": 30}},
}


class TestPanorama(unittest.TestCase):
    def setUp(self):
        self.filas = a.panorama(EJEMPLO, date(2026, 10, 26))
        self.por = {r["departamento"]: r for r in self.filas}

    def test_orden_alfabetico_sin_ranking(self):
        self.assertEqual([r["departamento"] for r in self.filas], ["Amazonas", "Apurímac", "Cusco", "Junín"])

    def test_activas_son_alertadas_y_confirmadas(self):
        self.assertEqual(self.por["Cusco"]["alertas"], 53)
        self.assertEqual(self.por["Cusco"]["alertas_activas"], 41)
        self.assertEqual(self.por["Amazonas"]["alertas_activas"], 0)
        self.assertEqual(self.por["Apurímac"]["alertas_activas"], 3)

    def test_focos_y_periodo(self):
        c = self.por["Cusco"]
        self.assertEqual((c["focos_3d"], c["focos_anio_menos2"], c["focos_anio_menos1"], c["focos_anio"]), (20, 100, 50, 80))
        self.assertEqual(self.por["Junín"]["focos_anio"], 30)
        self.assertEqual(c["periodo_anual"], "1 ene al 26 oct")
        self.assertEqual((c["alertas_desde"], c["alertas_hasta"]), ("2026-10-17", "2026-10-25"))


if __name__ == "__main__":
    unittest.main()
