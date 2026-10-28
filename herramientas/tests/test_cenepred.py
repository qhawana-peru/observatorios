import csv
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import validar_cenepred as v  # noqa: E402


class TestCenepred(unittest.TestCase):
    def test_datos_del_repositorio_cuadran(self):
        self.assertEqual(v.validar(), [])

    def test_detecta_cifra_mal_transcrita(self):
        d = tempfile.mkdtemp()
        try:
            ruta = os.path.join(d, "x.csv")
            with open(v.RUTA, encoding="utf-8", newline="") as f:
                filas = list(csv.DictReader(f))
            for r in filas:
                if r["estudio"] == "A" and r["departamento"] == "LIMA" and r["nivel"] == "muy alto" and r["peligro"] == "inundacion":
                    r["poblacion"] = str(int(r["poblacion"]) + 1)
            with open(ruta, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(filas[0]))
                w.writeheader()
                w.writerows(filas)
            errores = v.validar(ruta)
            self.assertTrue(any("poblacion" in e for e in errores))
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
