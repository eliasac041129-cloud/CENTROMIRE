#!/usr/bin/env python3
"""Utilidades compartidas para generar PDFs: reemplazo de simbolos por HTML/SVG
que SI se imprimen (la fuente base no tiene casillas, palomas, taches ni emojis)."""
import re

# --- Elementos dibujados (no dependen de glifos de la fuente) ---
BOX = ('<span style="display:inline-block;width:12px;height:12px;border:1.5px solid #7a2e6d;'
       'border-radius:2px;vertical-align:-2px;margin-right:2px;"></span>')
CHECK = ('<svg width="12" height="12" viewBox="0 0 16 16" style="vertical-align:-2px;margin-right:1px;">'
         '<path d="M2 8.5 L6 12.5 L14 3.5" fill="none" stroke="#2e7d32" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CHECKBOX = ('<svg width="13" height="13" viewBox="0 0 16 16" style="vertical-align:-2px;margin-right:2px;">'
            '<rect x="1" y="1" width="14" height="14" rx="2.5" fill="none" stroke="#7a2e6d" stroke-width="1.4"/>'
            '<path d="M3.5 8.5 L6.5 11.5 L12.5 4" fill="none" stroke="#2e7d32" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CROSS = ('<svg width="12" height="12" viewBox="0 0 16 16" style="vertical-align:-2px;margin-right:1px;">'
         '<path d="M3.5 3.5 L12.5 12.5 M12.5 3.5 L3.5 12.5" stroke="#c0392b" stroke-width="2.6" '
         'stroke-linecap="round"/></svg>')

def _dot(color):
    return (f'<span style="display:inline-block;width:11px;height:11px;border-radius:50%;'
            f'background:{color};vertical-align:-1px;"></span>')

RED, ORANGE, YELLOW, GREEN = _dot("#e53935"), _dot("#fb8c00"), _dot("#fbc02d"), _dot("#43a047")

# Mapeo de simbolos -> HTML (se aplica ANTES de eliminar emojis restantes)
REPLACEMENTS = {
    "\U0001F534": RED,      # circulo rojo
    "\U0001F7E0": ORANGE,   # circulo naranja
    "\U0001F7E1": YELLOW,   # circulo amarillo
    "\U0001F7E2": GREEN,    # circulo verde
    "\u2705": CHECK,        # check verde
    "\u2714": CHECK, "\u2713": CHECK,
    "\u2611": CHECKBOX,     # casilla marcada
    "\u2610": BOX,          # casilla vacia
    "\u274C": CROSS, "\u26D4": CROSS, "\u2716": CROSS, "\u2717": CROSS,
}

# Rangos de emoji a ELIMINAR (decorativos). NO incluye flechas 2190-21FF,
# bullet 2022, guiones, ni acentos/Ñ/Ë.
_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF"   # pictogramas y suplementarios
    "\U00002600-\U000027BF"    # simbolos misc + dingbats
    "\U0001F1E6-\U0001F1FF"    # indicadores regionales
    "\U00002B00-\U00002BFF"    # estrellas y flechas extra
    "\U0001F3FB-\U0001F3FF"    # tonos de piel
    "\uFE0F\u200D\u20E3]+",
    flags=re.UNICODE,
)

def prep(text: str) -> str:
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    text = _EMOJI_RE.sub("", text)
    # limpia dobles espacios que deja el emoji removido
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text
