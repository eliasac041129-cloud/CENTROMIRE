#!/usr/bin/env python3
"""Genera el EXPEDIENTE MAESTRO de Centro Mire en PDF.

Un PDF continuo por tomo, en blanco y negro, formato juridico, listo para
imprimir sin edicion previa. Requiere: weasyprint, markdown.

Uso:  python3 _build_expediente.py
Salida: EXPEDIENTE_MAESTRO/PDF/*.pdf
"""

import re
import shutil
from pathlib import Path

import markdown
from weasyprint import HTML

BASE = Path(__file__).resolve().parent
OUT = BASE / "PDF"

ESTABLECIMIENTO = "CENTRO MIRË DE BELLEZA INTEGRAL Y DISEÑO"

# ---------------------------------------------------------------- metadatos

TOMOS = [
    {
        "dir": None,
        "file": "00_INDICE_MAESTRO.md",
        "pdf": "00_INDICE_MAESTRO.pdf",
        "impresion": "Imprimir a doble cara.",
        "hoja_por_doc": False,
        "label": "Índice maestro",
        "titulo": "ÍNDICE MAESTRO DEL EXPEDIENTE",
        "destinatario": "Titular del establecimiento",
        "reservado": True,
        "uso": "Documento de control. Se conserva con la titular. No circula.",
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_1_CLIENTE",
        "pdf": "TOMO_1_CLIENTE.pdf",
        "portada": False,
        "impresion": "Imprimir A DOBLE CARA. Juego base: paginas 1 a 7 (4 hojas). Anexo A: paginas 8 y 9, solo si el cliente viene de un procedimiento medico. Anexo B: pagina 10, solo si autoriza el uso de su imagen.",
        "hoja_por_doc": False,
        "hoja_nueva": ["07_anexo_a_cuidado_postmedico.md", "08_anexo_b_uso_imagen.md"],
        "label": "Tomo 1 · Cliente",
        "titulo": "TOMO 1\nEXPEDIENTE DEL CLIENTE",
        "destinatario": "Cliente",
        "reservado": False,
        "uso": (
            "Se imprimen y firman completos los documentos 1 a 5 por cada cliente nuevo. "
            "El Anexo A solo se imprime cuando el cliente viene de un procedimiento médico y "
            "el Anexo B solo si autoriza el uso de su imagen. Se entrega copia del "
            "consentimiento y de las indicaciones al cliente; el expediente firmado se "
            "archiva por folio, bajo llave."
        ),
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_2_TITULAR",
        "pdf": "TOMO_2_TITULAR_CONFIDENCIAL.pdf",
        "impresion": "Imprimir a doble cara.",
        "hoja_por_doc": False,
        "label": "Tomo 2 · Titular (confidencial)",
        "titulo": "TOMO 2\nDICTAMEN, ESTRATEGIA Y PLAN DE ACCIÓN",
        "destinatario": "Titular del establecimiento y sus asesores",
        "reservado": True,
        "uso": (
            "DOCUMENTO CONFIDENCIAL. No se entrega a clientes, personal ni terceros y NO "
            "forma parte de la carpeta que se muestra a la autoridad. Contiene el análisis "
            "de riesgo y las acciones por ejecutar. Se conserva bajo llave."
        ),
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_3_MEDICO",
        "pdf": "TOMO_3_MEDICO.pdf",
        "impresion": "Imprimir a doble cara. Cada instrumento inicia hoja: el convenio se firma por duplicado, la indicacion medica se reproduce por paciente y la carta se entrega suelta.",
        "hoja_por_doc": True,
        "label": "Tomo 3 · Médico",
        "titulo": "TOMO 3\nCOLABORACIÓN CON MÉDICOS",
        "destinatario": "Médico que refiere pacientes",
        "reservado": False,
        "uso": (
            "Se imprime un juego por cada médico. El convenio se firma por duplicado, un "
            "ejemplar para cada parte. El formato de indicación médica se reproduce y se "
            "usa uno por paciente; se anexa al expediente del cliente. La carta de alcance "
            "y límites se entrega antes de recibir la primera referencia."
        ),
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_4_PERSONAL",
        "pdf": "TOMO_4_PERSONAL.pdf",
        "impresion": "Imprimir a doble cara. Los protocolos de urgencias y de visita de autoridad y la carta de compromiso inician hoja, porque se fijan a la vista o se archivan por separado.",
        "hoja_por_doc": False,
        "hoja_nueva": ["04_protocolo_urgencias.md", "05_protocolo_visita_autoridad.md", "07_carta_compromiso.md"],
        "label": "Tomo 4 · Personal",
        "titulo": "TOMO 4\nMANUAL DE OPERACIÓN DEL PERSONAL",
        "destinatario": "Personal y colaboradores",
        "reservado": False,
        "uso": (
            "Se imprime un juego por cada persona que trabaje o colabore en el "
            "establecimiento, antes de que atienda a su primer cliente. Se lee completo y "
            "se firma la carta de compromiso final. El protocolo de urgencias y el de "
            "visita de autoridad se fijan también en el área de servicio."
        ),
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_5_VERIFICACION",
        "pdf": "TOMO_5_CARPETA_VERIFICACION.pdf",
        "impresion": "Imprimir a doble cara. El inventario y las bitacoras inician hoja porque se reproducen y se reemplazan cada mes.",
        "hoja_por_doc": False,
        "hoja_nueva": ["04_inventario.md", "05_bitacoras.md"],
        "label": "Tomo 5 · Carpeta de verificación",
        "titulo": "TOMO 5\nCARPETA DE VERIFICACIÓN SANITARIA",
        "destinatario": "Autoridad, en visita de verificación",
        "reservado": False,
        "uso": (
            "Se imprime un ejemplar, se integra en carpeta física con sus anexos y se "
            "mantiene accesible en el establecimiento. Se entrega al verificador al inicio "
            "de la visita. Las bitácoras se reproducen por mes."
        ),
        "base_font": "10pt",
    },
    {
        "dir": "TOMO_6_AVISOS_PUBLICO",
        "pdf": "TOMO_6_AVISOS_AL_PUBLICO.pdf",
        "portada": False,
        "impresion": "Imprimir a UNA CARA: cada aviso es una hoja independiente para fijar a la vista.",
        "hoja_por_doc": True,
        "label": "Tomo 6 · Avisos al público",
        "titulo": "TOMO 6\nAVISOS PARA EXHIBIR AL PÚBLICO",
        "destinatario": "Público y clientes",
        "reservado": False,
        "uso": (
            "Se imprime un ejemplar de cada aviso y se fija a la vista del público, en "
            "marco o funda plástica. El aviso de privacidad simplificado y el de alcance de "
            "servicios van en recepción, a la entrada."
        ),
        "base_font": "11.5pt",
    },
]

# ---------------------------------------------------------------- estilos

CSS_TMPL = """
@page {{
  size: Letter;
  margin: 1.35cm 1.5cm 1.25cm 1.6cm;
  @top-left {{
    content: "{establecimiento}";
    font-family: "Liberation Serif", serif; font-size: 7pt;
    color: #000; padding-bottom: 1pt;
  }}
  @top-right {{
    content: "{label}";
    font-family: "Liberation Serif", serif; font-size: 7pt; color: #000;
  }}
  @bottom-left {{
    content: "{pie}";
    font-family: "Liberation Serif", serif; font-size: 6.5pt; color: #000;
  }}
  @bottom-right {{
    content: "Pag. " counter(page) " de " counter(pages);
    font-family: "Liberation Serif", serif; font-size: 7pt; color: #000;
  }}
}}

* {{ color: #000 !important; box-sizing: border-box; }}

html {{ font-family: "Liberation Serif", "DejaVu Serif", serif; }}
body {{
  font-family: "Liberation Serif", "DejaVu Serif", serif;
  font-size: {base_font};
  line-height: 1.22;
  text-align: justify;
  hyphens: none;
  orphans: 2; widows: 2;
}}

/* ---- encabezado del tomo (sin hoja de portada, para no gastar papel) ---- */
.portada {{ text-align: left; margin-bottom: 9pt; }}
.portada .marca {{
  font-size: 8.5pt; letter-spacing: .05em; text-transform: uppercase;
  border-bottom: 1.4pt solid #000; padding-bottom: 2pt; margin-bottom: 6pt;
}}
.portada h1 {{
  font-size: 13pt; line-height: 1.18; margin: 0 0 4pt 0; text-transform: uppercase;
  border: 0; padding: 0; white-space: pre-line; text-align: left;
}}
.portada .datos {{ font-size: 8pt; line-height: 1.3; margin: 0 0 5pt 0; }}
.portada .datos b {{ text-transform: uppercase; letter-spacing: .04em; }}
.portada .uso {{
  border: .7pt solid #000; padding: 4pt 6pt; font-size: 8pt; line-height: 1.28;
  margin-bottom: 5pt;
}}
.portada .uso b {{ text-transform: uppercase; letter-spacing: .05em; }}
.portada .sello {{
  border: 1.3pt solid #000; padding: 3pt 6pt; font-size: 8.5pt; font-weight: bold;
  text-transform: uppercase; text-align: center; margin-bottom: 5pt;
}}
.portada .indice {{ font-size: 8pt; line-height: 1.3; margin-bottom: 5pt; }}
.portada .legal {{ font-size: 7pt; line-height: 1.25; }}

/* ---- documentos ---- */
.doc.nueva {{ page-break-before: always; }}
.doc.sigue {{ border-top: 1.2pt solid #000; padding-top: 7pt; margin-top: 10pt; }}

h1 {{
  font-size: 11.5pt; text-transform: uppercase; text-align: center; margin: 0 0 6pt 0;
  padding-bottom: 3pt; border-bottom: 1.2pt solid #000; line-height: 1.2;
  page-break-after: avoid;
}}
h2 {{
  font-size: 9.5pt; text-transform: uppercase; margin: 8pt 0 3pt 0;
  border-bottom: .5pt solid #000; padding-bottom: 1pt; page-break-after: avoid;
}}
h3 {{ font-size: 9.5pt; margin: 6pt 0 2pt 0; page-break-after: avoid; }}
p {{ margin: 0 0 3.5pt 0; }}
ol, ul {{ margin: 0 0 3.5pt 0; padding-left: 14pt; }}
li {{ margin-bottom: 1.5pt; }}
strong {{ font-weight: bold; }}
hr {{ border: 0; border-top: .7pt solid #000; margin: 7pt 0; }}

blockquote {{
  margin: 5pt 0; padding: 4pt 7pt; border: .7pt solid #000; font-size: 9.5pt;
  text-align: justify;
}}
blockquote p:last-child {{ margin-bottom: 0; }}

table {{
  width: 100%; border-collapse: collapse; margin: 4pt 0 5pt 0; font-size: 8.5pt;
}}
th, td {{
  border: .5pt solid #000; padding: 2pt 3pt; text-align: left;
  vertical-align: top; line-height: 1.2;
}}
th {{ font-weight: bold; text-transform: uppercase; font-size: 7.5pt; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}

table.firmas {{ margin-top: 11pt; break-inside: avoid; font-size: 9.5pt; }}
table.firmas td {{
  border: 0; width: 50%; padding: 2pt 12pt 0 0; text-align: left; line-height: 1.4;
}}

.box {{
  display: inline-block; width: 8.5pt; height: 8.5pt; border: .8pt solid #000;
  margin: 0 2pt -.5pt 0; vertical-align: baseline;
}}

/* linea de llenado a mano */
.ul {{
  display: inline-block; border-bottom: .7pt solid #000; height: .9em;
  margin: 0 1.5pt -.18em 1.5pt;
}}

/* listas de casillas: una por renglon, sin vinetas */
ul.chk {{ list-style: none; padding-left: 0; margin: 3pt 0 4pt 0; }}
ul.chk li {{ margin-bottom: 2.5pt; text-align: left; }}

/* dato por completar */
.ph {{ font-style: italic; }}

em {{ font-style: italic; }}
"""

CSS_CARTEL = """
body.cartel {{ font-size: 11.5pt; line-height: 1.32; }}
body.cartel h1 {{ font-size: 15pt; }}
body.cartel h2 {{ font-size: 12pt; }}
body.cartel h3 {{ font-size: 11.5pt; }}
body.cartel p {{ margin-bottom: 5pt; }}
body.cartel li {{ margin-bottom: 3pt; }}
body.cartel .portada h1 {{ font-size: 13pt; }}
"""

# ---------------------------------------------------------------- utilidades

MD_EXT = ["tables", "attr_list", "sane_lists", "md_in_html"]


def _linea(m: re.Match) -> str:
    """Convierte una corrida de guiones bajos en una linea de llenado."""
    ancho = max(1.2, len(m.group(0)) * 0.42)
    return f'<span class="ul" style="width:{ancho:.1f}em"></span>'


BOX = '<span class="box"></span>'


def _inline(t: str) -> str:
    """Negritas y cursivas dentro de bloques HTML generados a mano."""
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", t)
    return t


def _listas_de_casillas(text: str) -> str:
    """Renglones que empiezan con casilla -> lista vertical, uno por linea.

    Evita que varias casillas se corran en un mismo parrafo, lo que hace
    imposible marcarlas a mano.
    """
    out, bloque = [], []

    def cerrar():
        if bloque:
            items = "".join(
                f"<li>{BOX} {_inline(t)}</li>" for t in bloque
            )
            out.append("")
            out.append(f'<ul class="chk">{items}</ul>')
            out.append("")
            bloque.clear()

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("\u2610") and not s.startswith("|"):
            bloque.append(s[1:].strip())
        else:
            cerrar()
            out.append(line)
    cerrar()
    return "\n".join(out)


def prep(text: str) -> str:
    """Ajustes de origen antes de convertir a HTML."""
    text = _listas_de_casillas(text)
    # casillas de verificacion como recuadro dibujado (imprime bien en B/N)
    for ch in ("\u2610", "\u2611", "\u2612"):
        text = text.replace(ch, BOX)
    # marcadores de dato por completar: se imprimen entre corchetes
    text = re.sub(
        r"\u27e8([^\u27e9]+)\u27e9", r'<span class="ph">[\1]</span>', text
    )
    # las corridas de guiones bajos se vuelven lineas dibujadas; asi no las
    # interpreta markdown como enfasis ni se rompen al final de renglon
    text = re.sub(r"_{2,}", _linea, text)
    return text


def md_to_html(path: Path) -> str:
    raw = prep(path.read_text(encoding="utf-8"))
    return markdown.markdown(raw, extensions=MD_EXT)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def indice_html(files) -> str:
    """Indice en linea corrida: informa lo mismo ocupando una fraccion del espacio."""
    if len(files) < 2:
        return ""
    partes = [f"{i}. {esc(first_heading(f))}" for i, f in enumerate(files, 1)]
    return (
        "<div class='indice'><b>CONTENIDO: </b>" + " · ".join(partes) + "</div>"
    )


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return re.sub(r"\*+", "", line[2:]).strip()
    return path.stem


LEGAL = (
    "Documento de cumplimiento y buenas prácticas para uso interno del establecimiento. "
    "No constituye representación legal ni sustituye la asesoría de un abogado sanitario "
    "con cédula. La normativa debe verificarse vigente antes de cada trámite."
)


def portada(tomo, files) -> str:
    titulo = esc(tomo["titulo"])
    sello = (
        "<div class='sello'>Documento confidencial - uso reservado de la titular</div>"
        if tomo["reservado"]
        else ""
    )
    return f"""
<div class="portada">
  <div class="marca">{esc(ESTABLECIMIENTO)} &nbsp;·&nbsp; Expediente maestro de
    cumplimiento v2.0 &nbsp;·&nbsp; {esc(tomo['label'])}</div>
  <h1>{titulo}</h1>
  <div class="datos">
    <b>Destinatario:</b> {esc(tomo['destinatario'])}.
    <b>Establecimiento:</b> estética y belleza, Aviso de Funcionamiento COFEPRIS
    No. 2509135018X00286 (SCIAN 812110), Av. del Conscripto 13, Col. Manuel Ávila
    Camacho, C.P. 11610, Alcaldía Miguel Hidalgo, CDMX. Contacto:
    mirecbi19@gmail.com · 56 1681 8058.
    <b>Perímetro de operación:</b> servicios estéticos NO INVASIVOS sobre piel intacta;
    no se realizan actos médicos, procedimientos invasivos ni inyectables.
    <b>Emisión:</b> ____/____/20____.
  </div>
  <div class="uso"><b>Uso e impresión: </b>{esc(tomo['uso'])} {esc(tomo['impresion'])}</div>
  {sello}
  {indice_html(files)}
  <div class="legal">{esc(LEGAL)}</div>
</div>
"""


def build_pdf(tomo):
    if tomo["dir"] is None:
        files = [BASE / tomo["file"]]
    else:
        files = sorted(p for p in (BASE / tomo["dir"]).glob("*.md"))

    # Solo se fuerza hoja nueva donde el documento debe poder circular o
    # firmarse por separado. El resto corre a continuacion, para no gastar hojas.
    forzadas = tomo.get("hoja_nueva", [])
    partes = []
    for i, p in enumerate(files):
        nueva = i > 0 and (tomo.get("hoja_por_doc") or p.name in forzadas)
        cls = "doc nueva" if nueva else ("doc sigue" if i > 0 else "doc")
        partes.append(f"<div class='{cls}'>{md_to_html(p)}</div>")
    cuerpo = "".join(partes)

    pie = "Documento confidencial" if tomo["reservado"] else tomo["label"]
    css = CSS_TMPL.format(
        establecimiento=ESTABLECIMIENTO,
        label=tomo["label"],
        pie=pie,
        base_font=tomo["base_font"],
    )
    body_class = "cartel" if tomo["dir"] == "TOMO_6_AVISOS_PUBLICO" else ""
    encabezado = portada(tomo, files) if tomo.get("portada", True) else ""
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>{esc(tomo['label'])}</title><style>{css}{CSS_CARTEL.format()}</style></head>
<body class="{body_class}">{encabezado}{cuerpo}</body></html>"""

    dest = OUT / tomo["pdf"]
    HTML(string=html, base_url=str(BASE)).write_pdf(str(dest))
    return dest, len(files)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for tomo in TOMOS:
        dest, n = build_pdf(tomo)
        size = dest.stat().st_size / 1024
        print(f"{dest.name:42s} {n:2d} doc(s)  {size:7.1f} KB")


if __name__ == "__main__":
    main()
