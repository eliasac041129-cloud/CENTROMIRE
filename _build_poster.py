#!/usr/bin/env python3
"""Genera un cartel imprimible (aviso al publico) con diseno, tamano carta vertical."""
import os
from weasyprint import HTML

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "PDFS")
os.makedirs(OUT, exist_ok=True)

HTML_DOC = """
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<style>
@page { size: Letter portrait; margin: 0; }
* { box-sizing: border-box; margin:0; padding:0; }
body { font-family:'DejaVu Sans',Arial,sans-serif; }
.frame { height:27.94cm; padding:1.1cm; }
.card { height:25.74cm; border:3px solid #b5548f; border-radius:22px; padding:1.4cm 1.3cm; display:flex; flex-direction:column; background:linear-gradient(180deg,#ffffff 0%,#fdf6fb 100%); }
.brand { text-align:center; }
.brand .mire { font-size:58px; font-weight:bold; color:#7a2e6d; letter-spacing:3px; }
.brand .sub { font-size:15px; color:#b5548f; letter-spacing:1px; margin-top:2px; }
.divider { height:3px; background:linear-gradient(90deg,transparent,#b5548f,transparent); margin:16px 0 20px; }
.headline { text-align:center; font-size:23px; color:#5f2455; font-weight:bold; line-height:1.3; margin-bottom:14px; }
.lead { text-align:center; font-size:14px; color:#4a2340; line-height:1.55; margin-bottom:18px; }
.points { list-style:none; margin:0 0 auto; }
.points li { font-size:13.5px; color:#2a2a2a; line-height:1.45; padding:9px 12px 9px 40px; margin:8px 0; background:#f7e8f2; border-radius:12px; position:relative; }
.points li::before { content:"\\2714"; position:absolute; left:14px; top:9px; color:#9b3d84; font-weight:bold; }
.points li.no { background:#fbe6e6; }
.points li.no::before { content:"\\2716"; color:#c0392b; }
.footer { margin-top:16px; text-align:center; }
.footer .note { font-size:11.5px; color:#7a2e6d; font-style:italic; margin-bottom:10px; }
.footer .legal { font-size:10px; color:#8a6f84; border-top:1px solid #e3c3d8; padding-top:8px; }
.contact { font-size:12px; color:#5f2455; margin-top:6px; }
</style></head>
<body>
<div class="frame"><div class="card">
  <div class="brand">
    <div class="mire">MIRË</div>
    <div class="sub">CENTRO DE BELLEZA INTEGRAL Y DISEÑO</div>
  </div>
  <div class="divider"></div>
  <div class="headline">Somos un centro de estética y belleza</div>
  <div class="lead">Ofrecemos tratamientos <strong>estéticos no invasivos</strong> de cuidado facial y corporal, con atención profesional y personalizada.</div>
  <ul class="points">
    <li>Servicios de estética facial y corporal: HydraFacial, radiofrecuencia, ultrasonido estético, maderoterapia y presoterapia.</li>
    <li>Atención por <strong>cosmiatra certificada</strong>, con productos y equipos con registro sanitario.</li>
    <li class="no">No realizamos procedimientos médicos, quirúrgicos ni inyectables.</li>
    <li>Los cuidados estéticos posteriores a una cirugía se realizan <strong>únicamente por indicación y bajo supervisión de tu médico</strong>.</li>
    <li>Los resultados estéticos varían en cada persona y no se garantizan.</li>
  </ul>
  <div class="footer">
    <div class="note">Tu bienestar y tu seguridad son primero. 🤍</div>
    <div class="contact">📍 Av. del Conscripto 13, Miguel Hidalgo, CDMX (dentro de Clínica Bloom) &nbsp;·&nbsp; 📲 @centro.mire</div>
    <div class="legal">Aviso de Funcionamiento COFEPRIS No. 2509135018X00286 &nbsp;·&nbsp; Giro: Salón/clínica de belleza (SCIAN 812110)</div>
  </div>
</div></div>
</body></html>
"""

out = os.path.join(OUT, "CARTEL_AVISO_AL_PUBLICO.pdf")
HTML(string=HTML_DOC, base_url=ROOT).write_pdf(out)
print("OK:", os.path.relpath(out, ROOT))
