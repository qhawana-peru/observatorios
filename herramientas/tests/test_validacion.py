"""Pruebas del lector y de los seis controles. Correr con:
    python -m unittest discover herramientas/tests
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import mef  # noqa: E402
import procesar  # noqa: E402
import validar  # noqa: E402

MUESTRA = json.load(open(os.path.join(AQUI, "muestras", "mef_2026-10-14.json"), encoding="utf-8"))
DETALLE = {k: v["detalle"] for k, v in validar.cargar_config()["rutas"].items()}


def armar_corte(base, fecha="2026-10-14", cambiar=None):
    """Crea una carpeta de corte con los 7 archivos de la muestra real del 14-10."""
    carpeta = os.path.join(base, fecha)
    os.makedirs(carpeta)
    for cod, d in MUESTRA.items():
        if cod.startswith("_"):
            continue
        d = json.loads(json.dumps(d))
        if cambiar:
            cambiar(cod, d)
        if d is None or d.get("omitir"):
            continue
        html = mef.html_de_prueba(d["incluye"], d["fecha"], d["col"], d["rows"])
        nombre = f"{fecha.replace('-', '')}_PP0068_{cod}_{DETALLE[cod]}_p1de1.xls"
        with open(os.path.join(carpeta, nombre), "wb") as f:
            f.write(html.encode("cp1252"))
    return carpeta


class Lector(unittest.TestCase):
    def test_archivo_real_windows_1252(self):
        a = mef.leer_archivo(os.path.join(AQUI, "muestras", "D1_real_cp1252.xls"))
        self.assertEqual(a.fecha_consulta, "2026-10-14")
        self.assertEqual(a.anio, 2026)
        self.assertEqual(a.incluye, "Actividades y Proyectos")
        self.assertEqual(a.columna, "Nivel de Gobierno")
        self.assertEqual([f.codigo for f in a.filas], ["E", "M", "R"])
        self.assertEqual(a.filas[2].pim, 819_746_830)
        self.assertEqual(a.filas[2].devengado, 575_318_404)
        self.assertEqual(a.filas[2].avance, 70.2)

    def test_rechaza_xlsx(self):
        with self.assertRaises(ValueError):
            mef.leer(b"PK\x03\x04resto")


class Controles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fallas(self, carpeta):
        res, _ = validar.validar(carpeta)
        return [r.nombre for r in res if not r.ok], res

    def test_corte_real_pasa_los_seis_controles(self):
        fallas, res = self.fallas(armar_corte(self.tmp))
        self.assertEqual(fallas, [], validar.informe(res, {"fecha": "x"}))

    def test_falta_un_archivo(self):
        def quitar(cod, d):
            if cod == "D5":
                d["omitir"] = True
        fallas, _ = self.fallas(armar_corte(self.tmp, cambiar=quitar))
        self.assertTrue(any("Encabezado" in f for f in fallas))
        self.assertTrue(any("partes suman" in f for f in fallas))

    def test_opcion_incluye_equivocada(self):
        def mal(cod, d):
            if cod == "D3":
                d["incluye"] = "Actividades y Proyectos"
        fallas, _ = self.fallas(armar_corte(self.tmp, cambiar=mal))
        self.assertTrue(any("Encabezado" in f for f in fallas))

    def test_cifra_alterada(self):
        def alterar(cod, d):
            if cod == "D2":
                d["rows"][21][6] = "38,783,270"   # devengado de Tumbes cambiado a mano
        fallas, _ = self.fallas(armar_corte(self.tmp, cambiar=alterar))
        self.assertTrue(any("partes suman" in f for f in fallas))
        self.assertTrue(any("Avance" in f for f in fallas))

    def test_sin_filtro_0068(self):
        def todo(cod, d):
            if cod == "D1":
                d["rows"][0][2] = "289,000,000,000"
        fallas, _ = self.fallas(armar_corte(self.tmp, cambiar=todo))
        self.assertTrue(any("Total de control" in f for f in fallas))

    def test_archivos_de_otro_dia(self):
        def otro(cod, d):
            if cod == "D6":
                d["fecha"] = "Fecha de la Consulta: 13-octubre-2026"
        fallas, _ = self.fallas(armar_corte(self.tmp, cambiar=otro))
        self.assertTrue(any("Encabezado" in f for f in fallas))

    def test_aviso_de_cambio_brusco(self):
        armar_corte(self.tmp, "2026-10-14")
        def recorte(cod, d):
            d["fecha"] = "Fecha de la Consulta: 21-octubre-2026"
        carpeta = armar_corte(self.tmp, "2026-10-21", cambiar=recorte)
        # sin cambios: ningún aviso de cambio brusco
        res, _ = validar.validar(carpeta)
        self.assertTrue(res[5].ok)
        self.assertTrue(any("Ningún" in a for a in res[5].avisos))

    def test_procesar_escribe_csv(self):
        carpeta = armar_corte(self.tmp)
        archivos, _ = validar.leer_corte(carpeta)
        filas = procesar.filas_de(archivos, "2026-10-14", validar.cargar_config())
        salida = os.path.join(self.tmp, "datos.csv")
        procesar.escribir(filas, "2026-10-14", salida)
        procesar.escribir(filas, "2026-10-14", salida)   # repetir no duplica
        with open(salida, encoding="utf-8") as f:
            n = sum(1 for _ in f) - 1
        self.assertEqual(n, len(filas))
        self.assertEqual(n, 3 + 26 + 18 + 25 + 24 + 14 + 5)


if __name__ == "__main__":
    unittest.main()


class FormularioDeHecho(unittest.TestCase):
    CUERPO = """### Fecha del hecho

2026-10-15

### Tipo de hecho

peligro: pronóstico o comunicado del ENFEN

### Qué pasó, en lenguaje simple

N° 18: se mantiene la alerta.

### Qué cambia frente a lo anterior (opcional)

_No response_

### Enlace a la fuente primaria

https://enfen.imarpe.gob.pe/comunicados/

### Cita textual del documento

Estado del sistema: alerta.

### Solo para comunicados ENFEN — magnitud del Niño Costero

4 extraordinario

### Solo para comunicados ENFEN — magnitud del Niño global

no aplica
"""

    def test_lee_el_formulario(self):
        import hecho_desde_issue as h
        f = h.fila(h.leer_formulario(self.CUERPO), "42")
        self.assertEqual((f["id"], f["franja"], f["fecha"], f["costero"], f["global"], f["cambio"]),
                         ("H42", "peligro", "2026-10-15", "4", "", ""))
        self.assertEqual(f["etiqueta_fecha"], "15 oct 2026")

    def test_rechaza_fuente_sin_https(self):
        import hecho_desde_issue as h
        with self.assertRaises(ValueError):
            h.fila(h.leer_formulario(self.CUERPO.replace("https://enfen", "enfen")), "1")
