#!/usr/bin/env python3
"""Normani × Brasil 2026: página única com os influenciadores convidados (PDF 1280x720).

Fotos em img/pessoas/<slug>.jpg. Seguidores do Instagram conferidos por busca em out/2026.
"""
import glob, sys
import build_geral as g

# (nome, @instagram ou None, seguidores ou None)
CONVIDADOS = [
    ("Dan Mendes", "danmendesoficial", "1M"),
    ("Josy Ramos", "josyramos", "422K"),
    ("Ana Flávia", "anaflaviadeverdade", "358K"),
    ("Jude Paulla", "judepaulla", "380K"),
    ("Jess", None, None),
    ("Julia Rodrigues", None, None),
    ("Juliano Floss", "julianofloss", "6M"),
]


def card(nome, ig, seg):
    av = g.avatar(nome, "", 132)
    if ig:
        av = f'<a href="https://www.instagram.com/{ig}/">{av}</a>'
        handle = f'<a class="h" href="https://www.instagram.com/{ig}/">@{ig}</a>'
    else:
        handle = '<span class="h">@ a confirmar</span>'
    n = f'<b class="n">{seg}</b><small>seguidores</small>' if seg else '<b class="n">—</b><small>seguidores</small>'
    return f'<div class="cv">{av}{handle}{n}</div>'


HTML = (
    g.blob(1150, 60, 280) + g.blob(80, 740, 300, "g", .8) + g.blob(700, 780, 240) +
    '<h1 class="t" style="top:50px">Influenciadores convidados</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Instagram</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:900px;font-size:18px;line-height:1.45">'
    'Criadores de conteúdo brasileiros convidados para a passagem da Normani por São Paulo. '
    'Clique na foto para abrir o perfil.</p>'
    '<div class="cvs">' + "".join(card(*c) for c in CONVIDADOS) + '</div>'
    + g.ft("Influenciadores convidados", 1)
)

CSS = g.CSS + """
.cvs{position:absolute;left:60px;right:60px;top:265px;display:grid;grid-template-columns:repeat(7,1fr);gap:12px;z-index:3}
.cv{background:#fff;border:1.4px solid #0B0B0C;border-radius:22px;padding:20px 8px 18px;display:flex;flex-direction:column;align-items:center;text-align:center;height:330px}
.cv a{color:inherit;text-decoration:none}
.cv .pp b{font-size:16px;margin-top:14px}
.cv .h{font-size:11.5px;color:#0E8A3A;font-weight:600;margin-top:4px;word-break:break-all}
.cv .n{font-size:38px;font-weight:400;letter-spacing:-.03em;margin-top:auto;line-height:1}
.cv small{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;margin-top:4px}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Influenciadores convidados</title>'
            f'<style>{g.FONTES}{CSS}</style></head><body><section class="sl">{HTML}</section></body></html>')
    out = g.B / "Normani-Influenciadores-Convidados.html"
    out.write_text(html)
    pdf = g.B / "Normani-Influenciadores-Convidados.pdf"
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True)
        if "--png" in sys.argv:
            pg.query_selector("section.sl").screenshot(path=str(g.B / "preview-convidados.png"))
        b.close()
    print(pdf.name)
