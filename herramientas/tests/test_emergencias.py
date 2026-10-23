"""Pruebas de los controles de la tabla de emergencias."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import validar_emergencias as ve  # noqa: E402

CFG = {"desde": "2026-09-01", "regiones": ["Tumbes", "Piura"]}
PDF = "el-nino/fuentes/indeci/2026-10-23/R1.pdf"


def fila(**k):
    base = {"id": "EM-1", "incluido": "si", "region": "Tumbes", "fecha_ocurrencia": "2026-10-20", "reporte": "N.º 1",
            "fuente_url": "https://portal.indeci.gob.pe/x.pdf", "archivo": PDF, "personas_afectadas": "12", "nota": ""}
    base.update(k)
    return base


class Emergencias(unittest.TestCase):
    def test_fila_correcta(self):
        self.assertEqual(ve.revisar([fila()], CFG, {PDF}), [])

    def test_sin_archivo(self):
        self.assertTrue(any("no está archivado" in p for p in ve.revisar([fila()], CFG, set())))

    def test_antes_del_periodo(self):
        self.assertTrue(any("antes del" in p for p in ve.revisar([fila(fecha_ocurrencia="2026-02-17")], CFG, {PDF})))

    def test_fuera_del_piloto(self):
        self.assertTrue(any("piloto" in p for p in ve.revisar([fila(region="Ica")], CFG, {PDF})))

    def test_cifra_no_numerica(self):
        self.assertTrue(any("número" in p for p in ve.revisar([fila(personas_afectadas="en evaluación")], CFG, {PDF})))

    def test_fuente_de_prensa(self):
        self.assertTrue(any("INDECI" in p for p in ve.revisar([fila(fuente_url="https://rpp.pe/nota")], CFG, {PDF})))

    def test_reporte_repetido(self):
        self.assertTrue(any("ya está" in p for p in ve.revisar([fila(), fila(id="EM-2")], CFG, {PDF})))

    def test_excluida_sin_motivo(self):
        self.assertTrue(any("motivo" in p for p in ve.revisar([fila(incluido="no")], CFG, {PDF})))

    def test_datos_reales(self):
        import csv
        import json
        filas = list(csv.DictReader(open(ve.CSV, encoding="utf-8")))
        self.assertEqual(ve.revisar(filas, json.load(open(ve.CONFIG, encoding="utf-8")), ve.archivados()), [])


if __name__ == "__main__":
    unittest.main()
