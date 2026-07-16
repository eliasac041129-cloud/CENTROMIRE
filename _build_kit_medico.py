#!/usr/bin/env python3
"""Genera el 'Kit del Medico': PDF con el convenio de colaboracion y el formato
de indicacion postquirurgica, para entregar a cada medico que refiere pacientes."""
import os
import markdown
from weasyprint import HTML
from _pdf_common import prep

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "PDFS")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: Letter; margin: 1.8cm 1.8cm 2cm; @bottom-right { content: "Pag. " counter(page) " / " counter(pages); font-size:9px; color:#999; } @bottom-left { content: "CENTRO MIRE - Kit del Medico"; font-size:8px; color:#c3a7bd; } }
@page cover { @bottom-right { content:""; } @bottom-left { content:""; } }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'DejaVu Sans',Arial,sans-serif; font-size:11px; color:#1a1a1a; line-height:1.5; }
h1 { font-size:18px; color:#7a2e6d; border-bottom:3px solid #b5548f; padding-bottom:6px; margin:0 0 12px; }
h2 { font-size:14px; color:#7a2e6d; margin-top:16px; border-bottom:1px solid #e3c3d8; padding-bottom:3px; }
h3 { font-size:12px; color:#9b3d84; margin-top:12px; }
p { margin:6px 0; }
table { border-collapse:collapse; width:100%; margin:10px 0; font-size:10px; }
th,td { border:1px solid #d8b8cd; padding:5px 6px; text-align:left; vertical-align:top; }
th { background:#f3e2ee; color:#5f2455; font-weight:bold; }
blockquote { border-left:4px solid #b5548f; background:#fbf3f8; margin:10px 0; padding:8px 12px; color:#4a2340; }
ul,ol { margin:6px 0 6px 18px; } li { margin:3px 0; }
hr { border:none; border-top:1px solid #ddd; margin:14px 0; }
strong { color:#3a1533; }
.doc { page-break-before: always; }
.cover { page: cover; height:26cm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; border:3px solid #b5548f; border-radius:20px; background:linear-gradient(180deg,#ffffff,#fdf6fb); padding:2cm; }
.cover .mire { font-size:56px; font-weight:bold; color:#7a2e6d; letter-spacing:3px; }
.cover .sub { font-size:15px; color:#b5548f; letter-spacing:1px; margin-bottom:26px; }
.cover .title { font-size:26px; font-weight:bold; color:#5f2455; border-top:2px solid #b5548f; border-bottom:2px solid #b5548f; padding:14px 0; margin-bottom:22px; }
.cover .idx { font-size:14px; color:#4a2340; line-height:2; text-align:left; }
.cover .idx b { color:#7a2e6d; }
.cover .fields { margin-top:30px; font-size:13px; color:#333; text-align:left; width:100%; }
.cover .fields div { margin:10px 0; border-bottom:1px solid #cbb; padding-bottom:4px; }
.cover .note { margin-top:26px; font-size:10.5px; color:#8a6f84; font-style:italic; }
"""

cover = """
<div class="cover">
  <div class="mire">MIRË</div>
  <div class="sub">CENTRO DE BELLEZA INTEGRAL Y DISEÑO</div>
  <div class="title">KIT DEL MÉDICO<br>Colaboración y referencia de pacientes</div>
  <div class="idx">
    Este paquete incluye:<br>
    <b>1.</b> Convenio de colaboración y prestación de servicios estéticos complementarios<br>
    <b>2.</b> Formato de indicación médica para cuidado estético (por paciente)
  </div>
  <div class="fields">
    <div>Médico / especialidad: ______________________________________________</div>
    <div>Cédula profesional: ____________________ &nbsp;&nbsp; Fecha: ____________________</div>
    <div>Consultorio / clínica: __________________________________________</div>
  </div>
  <div class="note">Firma un convenio con cada médico e imprime el formato de indicación por cada paciente referido. Consérvalos en la carpeta de verificación.</div>
</div>
"""

files = [
    "BLINDAJE_COFEPRIS/07_CONVENIO_COLABORACION_MEDICO.md",
    "BLINDAJE_COFEPRIS/08_INDICACION_MEDICA_POSTQUIRURGICA.md",
]

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
parts = [cover]
for rel in files:
    f = os.path.join(ROOT, rel)
    if not os.path.exists(f):
        print("MISSING:", rel); continue
    with open(f, encoding="utf-8") as fh:
        md.reset()
        parts.append(f'<div class="doc">{md.convert(prep(fh.read()))}</div>')

html = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
out = os.path.join(OUT, "KIT_DEL_MEDICO.pdf")
HTML(string=html, base_url=ROOT).write_pdf(out)
print("OK:", os.path.relpath(out, ROOT))
