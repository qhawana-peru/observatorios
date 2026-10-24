"""Pruebas del script que aplica una consulta de SERFOR a los datos del monitor."""
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import actualizar_incendios as ai  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(AQUI))
EJEMPLO = os.path.join(AQUI, "datos", "serfor_ejemplo.json")


def leer(carpeta, nombre):
    with open(os.path.join(carpeta, nombre), encoding="utf-8") as f:
        return list(csv.DictReader(f))


class ActualizarIncendios(unittest.TestCase):
    def setUp(self):
        """Copia los datos del repositorio y deja el seguimiento como estaba antes del corte de ejemplo."""
        with open(EJEMPLO, encoding="utf-8") as f:
            self.consulta = json.load(f)
        self.tmp = tempfile.mkdtemp()
        self.datos = os.path.join(self.tmp, "datos")
        shutil.copytree(os.path.join(RAIZ, "incendios", "datos"), self.datos)
        seg = [r for r in leer(self.datos, "seguimiento_proyeccion.csv") if r["corte"] < self.consulta["corte"]]
        for reg in self.consulta["regiones"]:
            filas = [r for r in seg if r["region"] == reg]
            filas[-1]["rango_bajo_pct"] = filas[-1]["rango_alto_pct"] = ""
        with open(os.path.join(self.datos, "seguimiento_proyeccion.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(seg[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(seg)
        self.seg_antes = seg
        self.config = os.path.join(self.tmp, "sitio.json")
        shutil.copy(os.path.join(RAIZ, "incendios", "config", "sitio.json"), self.config)
        self._orig = (ai.DATOS, ai.CONFIG)
        ai.DATOS, ai.CONFIG = self.datos, self.config

    def tearDown(self):
        ai.DATOS, ai.CONFIG = self._orig
        shutil.rmtree(self.tmp)

    def test_aplica_corte(self):
        consulta, corte = self.consulta, self.consulta["corte"]
        ai.actualizar(consulta, "nota de prueba")
        alertas = leer(self.datos, "serfor_alertas_recientes.csv")
        for reg in consulta["regiones"]:
            v = {r["indicador"]: int(r["valor"]) for r in alertas if r["region"] == reg}
            self.assertEqual(v["alertas"], v["alertado"] + v["confirmado"] + v["controlado"] + v["extinguido"])
        seg = leer(self.datos, "seguimiento_proyeccion.csv")
        for reg, R in consulta["regiones"].items():
            filas = [r for r in seg if r["region"] == reg]
            self.assertEqual(filas[-1]["corte"], corte)
            self.assertEqual(int(filas[-1]["focos_npp"]), R["npp"][corte[:4]]["hasta_corte"])
            self.assertTrue(filas[-2]["rango_bajo_pct"] and filas[-2]["rango_alto_pct"],
                            "el rango publicado queda registrado")
            antes = [r for r in self.seg_antes if r["region"] == reg]
            self.assertEqual([r["focos_npp"] for r in filas[:-1]], [r["focos_npp"] for r in antes],
                             "no se reescriben cortes pasados")
        for r in leer(self.datos, "serfor_historial_npp.csv"):
            if r["total_anio"]:
                h, t = int(r["hasta_corte"]), int(r["total_anio"])
                self.assertEqual(float(r["adicional_pct"]), round((t - h) / h * 100, 1))
        curvas = leer(self.datos, "serfor_curvas_npp.csv")
        for reg, R in consulta["regiones"].items():
            c = [int(r["acumulado"]) for r in curvas if r["region"] == reg and r["anio"] == corte[:4]]
            self.assertEqual(c, sorted(c))
            self.assertEqual(c[-1], R["npp"][corte[:4]]["hasta_corte"])
        with open(self.config, encoding="utf-8") as f:
            sitio = json.load(f)
        self.assertEqual(sitio["fecha_corte"], corte)
        self.assertEqual(sitio["nota_corte"], "nota de prueba")

    def test_no_repite_un_corte(self):
        ai.actualizar(self.consulta)
        with self.assertRaises(SystemExit):
            ai.actualizar(self.consulta)

    def test_periodos(self):
        self.assertEqual(ai.periodo("2026-10-09", "2026-10-23", date(2026, 10, 23), "x"), "9 al 23 de octubre")
        self.assertEqual(ai.periodo("2026-09-28", "2026-10-02", date(2026, 10, 2), "x"),
                         "28 de septiembre al 2 de octubre")
        self.assertEqual(ai.periodo(None, None, date(2026, 10, 23), "sin focos"), "sin focos al 23 de octubre")
        self.assertEqual(ai.nombre_provincia("LA CONVENCION"), "La Convención")


if __name__ == "__main__":
    unittest.main()
