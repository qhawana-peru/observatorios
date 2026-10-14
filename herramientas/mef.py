"""Lectura de los archivos que exporta la Consulta Amigable del MEF.

El botón "Exportar" del MEF entrega un archivo .xls que en realidad es una
página HTML (codificación Windows-1252) con tres tablas:
  - id="hd": fecha de la consulta, año e "Incluye"
  - class="MapTable": nombres de columnas
  - class="Data": una fila por elemento del desglose

Solo usa la biblioteca estándar de Python, para que cualquiera pueda correrlo.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

CAMPOS = ["pia", "pim", "certificacion", "compromiso_anual",
          "atencion_mensual", "devengado", "girado"]

MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
         "julio": 7, "agosto": 8, "setiembre": 9, "septiembre": 9, "octubre": 10,
         "noviembre": 11, "diciembre": 12}


@dataclass
class Fila:
    codigo: str
    nombre: str
    pia: int
    pim: int
    certificacion: int
    compromiso_anual: int
    atencion_mensual: int
    devengado: int
    girado: int
    avance: float


@dataclass
class ArchivoMEF:
    fecha_consulta: str | None = None   # AAAA-MM-DD
    anio: int | None = None
    incluye: str | None = None
    columna: str | None = None
    filas: list[Fila] = field(default_factory=list)


class _Lector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tablas: list[dict] = []
        self._pila: list[dict] = []
        self._fila: list[str] | None = None
        self._celda: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            t = {"id": a.get("id", ""), "clase": a.get("class", ""), "filas": [], "texto": []}
            self.tablas.append(t)
            self._pila.append(t)
        elif tag == "tr" and self._pila:
            self._fila = []
        elif tag in ("td", "th") and self._fila is not None:
            self._celda = []
        elif tag == "br" and self._pila:
            self._pila[-1]["texto"].append("\n")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._celda is not None and self._fila is not None:
            self._fila.append(" ".join("".join(self._celda).split()))
            self._celda = None
        elif tag == "tr" and self._fila is not None and self._pila:
            self._pila[-1]["filas"].append(self._fila)
            self._fila = None
        elif tag == "table" and self._pila:
            self._pila.pop()

    def handle_data(self, data):
        if self._celda is not None:
            self._celda.append(data.replace("\xa0", " "))
        if self._pila:
            self._pila[-1]["texto"].append(data.replace("\xa0", " "))


def _decodificar(contenido: bytes) -> str:
    try:
        return contenido.decode("utf-8")
    except UnicodeDecodeError:
        return contenido.decode("cp1252")


def _entero(txt: str) -> int:
    txt = txt.strip().replace(",", "")
    if txt in ("", "-"):
        return 0
    return int(round(float(txt)))


def leer(contenido: bytes | str) -> ArchivoMEF:
    """Lee un archivo exportado por la Consulta Amigable."""
    if isinstance(contenido, bytes):
        if contenido[:4] == b"PK\x03\x04":
            raise ValueError("El archivo fue abierto y guardado en Excel (.xlsx). "
                             "Descárgalo de nuevo y súbelo sin abrirlo.")
        contenido = _decodificar(contenido)
    lector = _Lector()
    lector.feed(contenido)
    res = ArchivoMEF()

    hd = next((t for t in lector.tablas if t["id"] == "hd"), None)
    if hd:
        texto = " ".join("".join(hd["texto"]).split())
        m = re.search(r"Fecha de la Consulta:\s*(\d{1,2})-([a-záéíóú]+)-(\d{4})", texto, re.I)
        if m and m.group(2).lower() in MESES:
            res.fecha_consulta = f"{m.group(3)}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
        m = re.search(r"Año de Ejecución:\s*(\d{4})", texto)
        if m:
            res.anio = int(m.group(1))
        m = re.search(r"Incluye:\s*(.+?)\s*$", texto)
        if m:
            res.incluye = m.group(1).strip()

    mapa = next((t for t in lector.tablas if "MapTable" in t["clase"]), None)
    if mapa and mapa["filas"] and mapa["filas"][0]:
        res.columna = mapa["filas"][0][0].strip()

    datos = next((t for t in lector.tablas if "Data" in t["clase"].split()), None)
    if datos is None:
        raise ValueError("No se encontró la tabla de datos. ¿Es un archivo exportado de la Consulta Amigable?")
    for celdas in datos["filas"]:
        celdas = [c for c in celdas]
        if len(celdas) < 9:
            continue
        etiqueta = celdas[0].strip()
        if ":" in etiqueta:
            codigo, nombre = [x.strip() for x in etiqueta.split(":", 1)]
        else:
            codigo, nombre = "", etiqueta
        nums = celdas[-8:]
        valores = [_entero(x) for x in nums[:7]]
        avance = float(nums[7].strip() or 0)
        res.filas.append(Fila(codigo, nombre, *valores, avance))
    return res


def leer_archivo(ruta: str) -> ArchivoMEF:
    with open(ruta, "rb") as f:
        return leer(f.read())


def html_de_prueba(incluye: str, fecha: str, columna: str, filas: list[list[str]]) -> str:
    """Arma un archivo con la misma estructura que la exportación del MEF (para pruebas)."""
    cab = (f'<body><table id="hd"><tr><td colspan="9"><div class=\'title\'>Consulta Amigable</div>'
           f"<div class='fecha'>{fecha}</div><br /><b>Año de Ejecución: <span class='value'>2026</span>"
           f"<br />Incluye: <span class='value'>{incluye}</span></b></td></tr></table>"
           f'<table id="ctl00_CPH1_Mt0" class="MapTable"><tr><td rowspan="2">{columna}</td>'
           "<td>PIA</td><td>PIM</td><td>Certificación</td><td>Compromiso Anual</td><td colspan=\"3\"> Ejecución </td>"
           "<td>Avance %&nbsp; </td></tr><tr><td>Atención de Compromiso Mensual&nbsp; </td><td>Devengado&nbsp; </td>"
           "<td>Girado&nbsp; </td></tr></table><table class=\"Data\" cellspacing=\"0\" cellpadding=\"1\">")
    cuerpo = "".join(
        f'<tr id="tr{i}"><td align="left"> {f[0]} </td>' + "".join(f"<td> {v} </td>" for v in f[1:8])
        + f"<td>&nbsp; {f[8]} </td></tr>" for i, f in enumerate(filas))
    return cab + cuerpo + "</table></body>"
