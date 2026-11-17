"""Controles del Observatorio del sistema de salud: los datos son coherentes, no traen datos personales y la página se genera."""
import importlib.util
import json
import os
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SA = os.path.join(RAIZ, "salud")


def cargar(*partes):
    with open(os.path.join(SA, *partes), encoding="utf-8") as f:
        return json.load(f)


class TestSalud(unittest.TestCase):
    def test_puntos_cuadran_con_el_resumen(self):
        puntos = cargar("geo", "puntos.json")
        resumen = cargar("datos", "renipress_resumen_20261116.json")
        self.assertEqual(len(puntos), resumen["total"]["n"])
        privados = sum(1 for p in puntos if p[2] == 4)
        self.assertEqual(privados, resumen["inst"]["PRIVADO"]["n"])

    def test_puntos_dentro_del_peru_y_con_campos_validos(self):
        for p in cargar("geo", "puntos.json"):
            self.assertEqual(len(p), 9)
            self.assertTrue(-18.6 < p[0] < 0.3 and -81.5 < p[1] < -68.4, p)
            self.assertIn(p[2], range(6))
            self.assertIn(p[3], (0, 1, 2))
            self.assertIn(p[4], (0, 1))

    def test_departamentos_cuadran(self):
        deps = cargar("geo", "departamentos.json")
        puntos = cargar("geo", "puntos.json")
        self.assertEqual(len(deps), 25)
        self.assertEqual(sum(v[0] for d in deps.values() for v in d["g"].values()), len(puntos))
        contornos = cargar("geo", "departamentos_contornos.json")
        self.assertEqual({f["properties"]["FIRST_IDDP"] for f in contornos["features"]}, set(deps))

    def test_sin_datos_personales(self):
        import re
        puntos = cargar("geo", "puntos.json")
        ruc = re.compile(r"\b(10|15|17|20)\d{9}\b")      # RUC de 11 dígitos
        telefono = re.compile(r"\b9\d{2} ?\d{3} ?\d{3}\b")  # celular peruano
        for p in puntos:
            for campo in p[6:]:
                self.assertIsNone(ruc.search(campo), p)
                self.assertIsNone(telefono.search(campo), p)
        # cada registro tiene solo coordenadas, códigos, nombre del establecimiento, categoría y distrito
        self.assertTrue(all(isinstance(p[6], str) and len(p[6]) <= 60 for p in cargar("geo", "puntos.json")))

    def test_pagina_se_genera(self):
        spec = importlib.util.spec_from_file_location("salud_build", os.path.join(SA, "build.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        with tempfile.TemporaryDirectory() as tmp:
            m.main(tmp)
            html = open(os.path.join(tmp, "index.html"), encoding="utf-8").read()
            self.assertNotIn("__RENI__", html)
            self.assertIn("sin revisión del comité", html)
            for f in ("puntos.json", "departamentos.json", "departamentos_contornos.json"):
                self.assertTrue(os.path.exists(os.path.join(tmp, "geo", f)))


if __name__ == "__main__":
    unittest.main()


class TestMortalidad(unittest.TestCase):
    def test_grupos_cuadran_con_el_total_y_la_calidad(self):
        r = cargar("datos", "mortalidad_sinadef_resumen.json")
        crudo = cargar("datos", "mortalidad_sinadef_agregados.json")
        self.assertEqual(sum(v["total"] for v in crudo["G"].values()), crudo["filas"])
        for a in r["anios"]:
            t = r["porAnio"][str(a)]
            self.assertEqual(t["I"] + t["II"] + t["III"] + t["X"], t["total"])
            self.assertEqual(t["total"], r["calidad"][str(a)]["total"])
            self.assertEqual(sum(x["n"] for x in r["sub"][str(a)]), t["total"])

    def test_celdas_pequenas_suprimidas(self):
        r = cargar("datos", "mortalidad_sinadef_resumen.json")
        for corte in ("dep", "seguro", "edad"):
            for tabla in r[corte].values():
                for fila in tabla.values():
                    for g in ("I", "II", "III", "X"):
                        self.assertFalse(0 < fila[g] < 5, (corte, fila))

    def test_el_anio_parcial_y_el_corte_estan_declarados(self):
        r = cargar("datos", "mortalidad_sinadef_resumen.json")
        self.assertIn(r["parcial"], r["anios"])
        self.assertNotEqual(r["ultimo"], r["parcial"])
        self.assertRegex(r["hasta"], r"^\d\d/\d\d/\d{4}$")
