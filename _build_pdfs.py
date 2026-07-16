#!/usr/bin/env python3
"""Convierte los .md del paquete de blindaje a PDFs listos para imprimir."""
import os, glob
import markdown
from weasyprint import HTML
from _pdf_common import prep

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "PDFS")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: Letter; margin: 2cm 1.8cm; @bottom-right { content: "Pag. " counter(page) " / " counter(pages); font-size: 9px; color:#888; } }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 11px; color:#1a1a1a; line-height:1.5; }
h1 { font-size: 21px; color:#7a2e6d; border-bottom:3px solid #b5548f; padding-bottom:6px; margin:0 0 12px; }
h2 { font-size: 15px; color:#7a2e6d; margin-top:20px; border-bottom:1px solid #e3c3d8; padding-bottom:3px; }
h3 { font-size: 12.5px; color:#9b3d84; margin-top:14px; }
p { margin:6px 0; }
table { border-collapse:collapse; width:100%; margin:10px 0; font-size:9.7px; }
th, td { border:1px solid #d8b8cd; padding:5px 6px; text-align:left; vertical-align:top; }
th { background:#f3e2ee; color:#5f2455; font-weight:bold; }
tr:nth-child(even) td { background:#faf4f8; }
code { background:#f2f2f2; padding:1px 4px; border-radius:3px; font-family:'DejaVu Sans Mono',monospace; font-size:9.5px; }
pre { background:#f6f6f6; border:1px solid #e0e0e0; border-radius:5px; padding:10px; font-size:9.5px; white-space:pre-wrap; }
blockquote { border-left:4px solid #b5548f; background:#fbf3f8; margin:10px 0; padding:8px 12px; color:#4a2340; }
ul, ol { margin:6px 0 6px 18px; padding:0; }
li { margin:3px 0; }
hr { border:none; border-top:1px solid #ddd; margin:16px 0; }
strong { color:#3a1533; }
a { color:#9b3d84; text-decoration:none; }
.brand { text-align:right; font-size:9px; color:#a878a0; margin-bottom:4px; }
"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "nl2br", "toc"])

files = [os.path.join(ROOT, "BLINDAJE_JURIDICO_CENTRO_MIRE.md")]
files += sorted(glob.glob(os.path.join(ROOT, "BLINDAJE_COFEPRIS", "*.md")))

count = 0
for f in files:
    if not os.path.exists(f):
        continue
    with open(f, encoding="utf-8") as fh:
        text = fh.read()
    md.reset()
    body = md.convert(prep(text))
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="brand">CENTRO MIRË · Blindaje COFEPRIS</div>{body}</body></html>"""
    base = os.path.splitext(os.path.basename(f))[0]
    out_pdf = os.path.join(OUT, base + ".pdf")
    HTML(string=html, base_url=ROOT).write_pdf(out_pdf)
    count += 1
    print("OK:", os.path.relpath(out_pdf, ROOT))

print(f"\nGenerados {count} PDFs en {os.path.relpath(OUT, ROOT)}/")
