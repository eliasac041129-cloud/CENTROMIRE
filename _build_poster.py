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
.points li { font-size:13.5px; color:#2a2a2a; line-height:1.45; padding:10px 12px 10px 42px; margin:8px 0; background:#f7e8f2; border-radius:12px; position:relative; }
.points li .mk { position:absolute; left:12px; top:9px; }
.points li.no { background:#fbe6e6; }
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
    <li><span class="mk">__CHECK__</span>Servicios de estética facial y corporal: HydraFacial, radiofrecuencia, ultrasonido estético, maderoterapia y presoterapia.</li>
    <li><span class="mk">__CHECK__</span>Atención por <strong>cosmiatra certificada</strong>, con productos y equipos con registro sanitario.</li>
    <li class="no"><span class="mk">__CROSS__</span>No realizamos procedimientos médicos, quirúrgicos ni inyectables.</li>
    <li><span class="mk">__CHECK__</span>Los cuidados estéticos posteriores a una cirugía se realizan <strong>únicamente por indicación y bajo supervisión de tu médico</strong>.</li>
    <li><span class="mk">__CHECK__</span>Los resultados estéticos varían en cada persona y no se garantizan.</li>
  </ul>
  <div class="footer">
    <div class="note">Tu bienestar y tu seguridad son primero. 🤍</div>
    <div class="contact">📍 Av. del Conscripto 13, Miguel Hidalgo, CDMX (dentro de Clínica Bloom) &nbsp;·&nbsp; 📲 @centro.mire</div>
    <div class="legal">Aviso de Funcionamiento COFEPRIS No. 2509135018X00286 &nbsp;·&nbsp; Giro: Salón/clínica de belleza (SCIAN 812110)</div>
  </div>
</div></div>
</body></html>
"""

_CHECK = ('<svg width="17" height="17" viewBox="0 0 16 16" style="vertical-align:-3px">'
          '<path d="M2 8.5 L6 12.5 L14 3.5" fill="none" stroke="#2e7d32" stroke-width="2.8" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg>')
_CROSS = ('<svg width="17" height="17" viewBox="0 0 16 16" style="vertical-align:-3px">'
          '<path d="M3.5 3.5 L12.5 12.5 M12.5 3.5 L3.5 12.5" stroke="#c0392b" stroke-width="2.8" '
          'stroke-linecap="round"/></svg>')

doc = HTML_DOC.replace("__CHECK__", _CHECK).replace("__CROSS__", _CROSS).replace("\U0001F90D", "")
out = os.path.join(OUT, "CARTEL_AVISO_AL_PUBLICO.pdf")
HTML(string=doc, base_url=ROOT).write_pdf(out)
print("OK:", os.path.relpath(out, ROOT))
