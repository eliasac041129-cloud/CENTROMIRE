#!/usr/bin/env python3
"""Genera los PDFs del EXPEDIENTE_MAESTRO: individuales + manual consolidado con portada e indice."""
import os, glob
import markdown
from weasyprint import HTML
from _pdf_common import prep

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "EXPEDIENTE_MAESTRO")
OUT = os.path.join(ROOT, "PDFS", "EXPEDIENTE_MAESTRO")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: Letter; margin: 1.9cm 1.8cm 2cm; @bottom-right { content: "Pag. " counter(page); font-size:9px; color:#999; } @bottom-left { content: "CENTRO MIRE - Expediente Maestro"; font-size:8px; color:#c3a7bd; } }
@page cover { margin: 0; @bottom-right { content:""; } @bottom-left { content:""; } }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'DejaVu Sans',Arial,sans-serif; font-size:11px; color:#1a1a1a; line-height:1.5; }
h1 { font-size:19px; color:#7a2e6d; border-bottom:3px solid #b5548f; padding-bottom:6px; margin:0 0 12px; }
h2 { font-size:14px; color:#7a2e6d; margin-top:16px; border-bottom:1px solid #e3c3d8; padding-bottom:3px; }
h3 { font-size:12px; color:#9b3d84; margin-top:12px; }
p { margin:6px 0; }
table { border-collapse:collapse; width:100%; margin:9px 0; font-size:9.4px; }
th,td { border:1px solid #d8b8cd; padding:4px 6px; text-align:left; vertical-align:top; }
th { background:#f3e2ee; color:#5f2455; font-weight:bold; }
tr:nth-child(even) td { background:#faf4f8; }
blockquote { border-left:4px solid #b5548f; background:#fbf3f8; margin:10px 0; padding:8px 12px; color:#4a2340; }
ul,ol { margin:6px 0 6px 18px; } li { margin:3px 0; }
hr { border:none; border-top:1px solid #ddd; margin:14px 0; }
strong { color:#3a1533; }
.doc { page-break-before: always; }
.cover { page: cover; height:27.94cm; page-break-after:always; background:linear-gradient(135deg,#7a2e6d,#b5548f 55%,#e4a5cd); color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:3cm; }
.cover .mire { font-size:66px; font-weight:bold; letter-spacing:3px; }
.cover .sub { font-size:19px; opacity:.95; margin-bottom:28px; }
.cover .title { font-size:27px; font-weight:bold; line-height:1.3; border-top:2px solid rgba(255,255,255,.6); border-bottom:2px solid rgba(255,255,255,.6); padding:15px 0; }
.cover .meta { font-size:13px; opacity:.95; margin-top:24px; line-height:1.7; }
.toc { page-break-after: always; }
.toc ol { font-size:11.5px; line-height:1.9; }
"""

titles = {
 "00_INDICE_Y_GUIA_DE_USO":"Índice y Guía de Uso",
 "01_AVISO_PRIVACIDAD_INTEGRAL":"Aviso de Privacidad Integral",
 "02_AVISO_PRIVACIDAD_SIMPLIFICADO":"Aviso de Privacidad Simplificado (cartel)",
 "03_AVISO_PRIVACIDAD_REDES":"Aviso de Privacidad Corto (redes)",
 "04_FICHA_CLINICA_ESTETICA":"Ficha Clínica-Estética del Cliente",
 "05_CUESTIONARIO_SALUD":"Cuestionario de Salud",
 "06_CONSENTIMIENTO_INFORMADO_GENERAL":"Consentimiento Informado General",
 "07_CONSENTIMIENTOS_POR_PROCEDIMIENTO":"Consentimientos por Procedimiento",
 "08_CONSENTIMIENTO_USO_IMAGEN":"Consentimiento de Uso de Imagen",
 "09_INDICACIONES_CUIDADOS_POSTERIORES":"Indicaciones y Cuidados Posteriores",
 "10_POLITICA_PRECIOS_CANCELACIONES":"Política de Precios y Cancelaciones",
 "11_REFERENCIA_MEDICA_POSTQUIRURGICA":"Referencia Médica Postquirúrgica",
 "12_CONVENIO_COLABORACION_MEDICO":"Convenio de Colaboración con el Médico",
 "13_PROTOCOLO_DERIVACION_URGENCIAS":"Protocolo de Derivación y Urgencias",
 "14_BITACORA_SERVICIOS":"Bitácora de Servicios",
 "15_INVENTARIO_EQUIPOS_Y_PRODUCTOS":"Inventario de Equipos y Productos",
 "16_PROTOCOLOS_HIGIENE_LIMPIEZA":"Protocolos de Higiene y Limpieza",
 "17_POLITICA_SERVICIOS_Y_AVISO_PUBLICO":"Política de Servicios y Aviso al Público",
 "18_CHECKLIST_TOTAL_BLINDAJE_Y_TRAMITES":"Checklist Total de Blindaje y Trámites",
}

md = markdown.Markdown(extensions=["tables","fenced_code","sane_lists","nl2br"])
files = sorted(glob.glob(os.path.join(SRC, "*.md")))

# 1) PDFs individuales
for f in files:
    base = os.path.splitext(os.path.basename(f))[0]
    with open(f, encoding="utf-8") as fh:
        md.reset(); body = md.convert(prep(fh.read()))
    html = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, base_url=ROOT).write_pdf(os.path.join(OUT, base + ".pdf"))
    print("OK ind:", base)

# 2) Manual consolidado
cover = """
<div class="cover">
  <div class="mire">MIRË</div>
  <div class="sub">Centro de Belleza Integral y Diseño</div>
  <div class="title">EXPEDIENTE MAESTRO<br>Kit completo de blindaje<br>(Clínica de Cosmiatría)</div>
  <div class="meta">Angélica Mirely Jiménez Regalado<br>Aviso de Funcionamiento COFEPRIS No. 2509135018X00286 · Giro SCIAN 812110<br>Av. del Conscripto 13, Miguel Hidalgo, CDMX (dentro de Clínica Bloom)</div>
</div>
"""
toc_items = "".join(f"<li>{titles.get(os.path.splitext(os.path.basename(f))[0], os.path.basename(f))}</li>" for f in files)
toc = f'<div class="toc"><h1>Contenido del Expediente</h1><ol>{toc_items}</ol></div>'
parts = [cover, toc]
for f in files:
    with open(f, encoding="utf-8") as fh:
        md.reset(); parts.append(f'<div class="doc">{md.convert(prep(fh.read()))}</div>')
html = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
manual = os.path.join(ROOT, "PDFS", "EXPEDIENTE_MAESTRO_CENTRO_MIRE.pdf")
HTML(string=html, base_url=ROOT).write_pdf(manual)
print("OK manual:", os.path.relpath(manual, ROOT))
