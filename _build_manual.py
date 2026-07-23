#!/usr/bin/env python3
"""Genera un PDF unico consolidado (manual) con portada, indice y todos los documentos."""
import os, glob
import markdown
from weasyprint import HTML
from _pdf_common import prep

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "PDFS")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: Letter; margin: 2cm 1.8cm; @bottom-right { content: "Pag. " counter(page); font-size: 9px; color:#999; } @bottom-left { content: "CENTRO MIRE - Manual de Blindaje COFEPRIS"; font-size: 8px; color:#bbb; } }
@page cover { margin: 0; @bottom-right { content: ""; } @bottom-left { content: ""; } }
* { box-sizing: border-box; }
body { font-family:'DejaVu Sans',Arial,sans-serif; font-size:11px; color:#1a1a1a; line-height:1.5; }
h1 { font-size:20px; color:#7a2e6d; border-bottom:3px solid #b5548f; padding-bottom:6px; margin:0 0 12px; }
h2 { font-size:14.5px; color:#7a2e6d; margin-top:18px; border-bottom:1px solid #e3c3d8; padding-bottom:3px; }
h3 { font-size:12.5px; color:#9b3d84; margin-top:13px; }
p { margin:6px 0; }
table { border-collapse:collapse; width:100%; margin:10px 0; font-size:9.6px; }
th,td { border:1px solid #d8b8cd; padding:5px 6px; text-align:left; vertical-align:top; }
th { background:#f3e2ee; color:#5f2455; font-weight:bold; }
tr:nth-child(even) td { background:#faf4f8; }
code { background:#f2f2f2; padding:1px 4px; border-radius:3px; font-family:'DejaVu Sans Mono',monospace; font-size:9.5px; }
pre { background:#f6f6f6; border:1px solid #e0e0e0; border-radius:5px; padding:10px; font-size:9.5px; white-space:pre-wrap; }
blockquote { border-left:4px solid #b5548f; background:#fbf3f8; margin:10px 0; padding:8px 12px; color:#4a2340; }
ul,ol { margin:6px 0 6px 18px; padding:0; } li { margin:3px 0; }
hr { border:none; border-top:1px solid #ddd; margin:16px 0; }
strong { color:#3a1533; }
a { color:#9b3d84; text-decoration:none; }
.doc { page-break-before: always; }
/* Portada */
.cover { page: cover; height:100vh; background:linear-gradient(135deg,#7a2e6d 0%,#b5548f 55%,#e4a5cd 100%); color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:3cm; }
.cover .mire { font-size:64px; font-weight:bold; letter-spacing:2px; margin-bottom:6px; }
.cover .sub { font-size:20px; opacity:.95; margin-bottom:30px; }
.cover .title { font-size:30px; font-weight:bold; line-height:1.25; margin-bottom:16px; border-top:2px solid rgba(255,255,255,.6); border-bottom:2px solid rgba(255,255,255,.6); padding:16px 0; }
.cover .meta { font-size:13px; opacity:.95; margin-top:26px; line-height:1.7; }
.cover .warn { position:absolute; bottom:1.6cm; left:0; right:0; font-size:10px; opacity:.9; padding:0 3cm; }
/* Indice */
.toc { page-break-after: always; }
.toc ol { font-size:12px; line-height:2; }
.toc li { margin:2px 0; }
"""

# Portada + Indice
cover = """
<div class="cover">
  <div class="mire">MIRË</div>
  <div class="sub">Centro de Belleza Integral y Diseño</div>
  <div class="title">MANUAL DE BLINDAJE<br>JURÍDICO Y SANITARIO<br>COFEPRIS</div>
  <div class="meta">
    Angélica Mirely Jiménez Regalado<br>
    Aviso de Funcionamiento COFEPRIS No. 2509135018X00286 · Giro SCIAN 812110<br>
    Av. del Conscripto 13, Miguel Hidalgo, CDMX (dentro de Clínica Bloom)
  </div>
  <div class="warn">Documento de cumplimiento y buenas prácticas. No sustituye la asesoría de un abogado sanitario colegiado. Verifica los criterios vigentes en el portal de COFEPRIS/DIGIPRiS antes de cada trámite.</div>
</div>
"""

titles = {
 "BLINDAJE_JURIDICO_CENTRO_MIRE": "Diagnóstico y plan de blindaje (documento principal)",
 "00_GUIA_VERIFICACION_COFEPRIS": "Guía maestra de verificación COFEPRIS",
 "01_CHECKLIST_CARPETA_VERIFICACION": "Checklist de la carpeta de verificación",
 "02_AVISO_PRIVACIDAD_INTEGRAL": "Aviso de Privacidad Integral",
 "03_AVISO_PRIVACIDAD_SIMPLIFICADO": "Aviso de Privacidad Simplificado",
 "04_CONSENTIMIENTO_INFORMADO_ESTETICO": "Consentimiento Informado Estético",
 "05_CONSENTIMIENTO_USO_IMAGEN": "Consentimiento de Uso de Imagen",
 "06_CUESTIONARIO_SALUD_CLIENTE": "Cuestionario de Salud del Cliente",
 "07_CONVENIO_COLABORACION_MEDICO": "Convenio de Colaboración con el Médico",
 "08_INDICACION_MEDICA_POSTQUIRURGICA": "Indicación Médica Postquirúrgica",
 "09_INVENTARIO_EQUIPOS_Y_PRODUCTOS": "Inventario de Equipos y Productos",
 "10_BITACORA_SERVICIOS": "Bitácora de Servicios",
 "11_PROTOCOLOS_HIGIENE_Y_LIMPIEZA": "Protocolos de Higiene y Limpieza",
 "12_POLITICA_Y_AVISO_AL_PUBLICO": "Política de Servicios y Aviso al Público",
 "13_GUIA_REDES_SOCIALES": "Guía de Redes Sociales",
 "14_DICTAMEN_LEGAL_Y_PLAN_DE_ACCION": "Dictamen Legal y Plan de Acción",
 "15_CHECKLIST_LISTO_PARA_COFEPRIS": "Checklist Definitivo Listo para COFEPRIS",
}

files = [os.path.join(ROOT, "BLINDAJE_JURIDICO_CENTRO_MIRE.md")]
files += sorted(glob.glob(os.path.join(ROOT, "BLINDAJE_COFEPRIS", "*.md")))

toc_items = "".join(f"<li>{titles.get(os.path.splitext(os.path.basename(f))[0], os.path.basename(f))}</li>" for f in files if os.path.exists(f))
toc = f'<div class="toc"><h1>Contenido del manual</h1><ol>{toc_items}</ol></div>'

md = markdown.Markdown(extensions=["tables","fenced_code","sane_lists","nl2br"])
parts = [cover, toc]
for f in files:
    if not os.path.exists(f):
        continue
    with open(f, encoding="utf-8") as fh:
        md.reset()
        parts.append(f'<div class="doc">{md.convert(prep(fh.read()))}</div>')

html = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
out = os.path.join(OUT, "MANUAL_COMPLETO_CENTRO_MIRE.pdf")
HTML(string=html, base_url=ROOT).write_pdf(out)
print("OK:", os.path.relpath(out, ROOT))
