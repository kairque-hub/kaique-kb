#!/usr/bin/env python3
"""Monta o HTML de impressão e gera o PDF do relatório."""
import base64, glob, pathlib, subprocess, sys
from playwright.sync_api import sync_playwright

B = pathlib.Path(__file__).parent
html = (B/"pdf.template.html").read_text()
html = html.replace("{{FONTES}}", (B/"fontes/embed.css").read_text())
html = html.replace("{{VEICULOS}}", (B/"dados_veiculos.js").read_text())
html = html.replace("{{PUBLICO}}", "data:image/jpeg;base64," +
                    base64.b64encode((B/"img/publico.jpg").read_bytes()).decode())
saida_html = B/"pdf.build.html"
saida_html.write_text(html)

exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
pdf = B/"Vanessa-da-Mata-Rock-in-Rio-2026-Relatorio.pdf"
erros = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page()
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto(saida_html.as_uri())
    pg.wait_for_timeout(1500)
    pg.emulate_media(media="print")
    pg.pdf(path=str(pdf), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
if erros:
    print("ERROS JS:", erros); sys.exit(1)
print(f"{pdf.name}: {pdf.stat().st_size/1024/1024:.2f} MB")
