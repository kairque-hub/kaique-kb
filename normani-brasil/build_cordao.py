#!/usr/bin/env python3
"""Normani × Brasil 2026: cordão do crachá, 95 x 2,4 cm.

Gera:
  Normani-Cordao-Opcoes.pdf          página de apresentação com as 3 opções (1280x720)
  Normani-Cordao-Impressao.pdf       uma opção por página, em tamanho real com 3 mm de sangria (956 x 30 mm)
  Normani-Cordao-Guias.pdf           igual, com linha de corte (preto) e meio do cordão (pontilhado)

O texto vira 180° na metade do cordão: pendurado no pescoço, os dois lados ficam lendo de cima para baixo.
"""
import glob, sys
import build_geral as g
import build_crachas as k

L, A, SG = 950, 24, 3        # comprimento, altura e sangria em mm
YEL, GRN, INK = k.YEL, k.GRN, k.INK


def unidade(fg, ac):
    """bloco que se repete ao longo do cordão"""
    st = f'<b style="color:{ac}">✶</b>'
    return (f'<span class="c-u"><span class="c-sc" style="color:{fg}">Normani</span>{st}'
            f'<span class="c-ev" style="color:{fg}">BRAZIL 2026</span>{st}'
            f'<b class="c-nm" style="color:{fg}">AAA</b>{st}</span>')


def faixa(bg, fg, ac, borda=None):
    rep = unidade(fg, ac) * 6
    b = (f'<i class="c-bd" style="top:0;background:{borda}"></i><i class="c-bd" style="bottom:0;background:{borda}"></i>'
         if borda else "")
    return (f'<div class="c-strip" style="background:{bg}">{b}'
            f'<div class="c-half">{rep}</div><div class="c-half c-rot">{rep}</div></div>')


OPCOES = [
    ("Black", "Black strap, yellow logo and text, thin green edges.", (INK, YEL, GRN, GRN)),
]

STRIP_CSS = f"""
.c-strip{{position:relative;width:{L + 2 * SG}mm;height:{A + 2 * SG}mm;overflow:hidden;display:flex}}
.c-half{{width:50%;height:100%;display:flex;align-items:center;white-space:nowrap;overflow:hidden;padding-left:12mm}}
.c-half.c-rot{{transform:rotate(180deg)}}
.c-u{{display:inline-flex;align-items:center;gap:5mm;padding-right:5mm;font-family:Inter,sans-serif}}
.c-u .c-nm{{font-size:9.5mm;font-weight:800;letter-spacing:.06em;line-height:1}}
.c-u .c-ev{{font-size:6mm;font-weight:600;letter-spacing:.18em}}
.c-u .c-sc{{font-family:'Mr Dafoe';font-size:12mm;line-height:1;padding-top:1mm}}
.c-u > b:not(.nm){{font-size:6mm}}
.c-bd{{position:absolute;left:0;right:0;height:{SG + 1.6}mm;z-index:2}}
"""


def guias():
    return (f'<svg style="position:absolute;left:0;top:0;width:{L + 2 * SG}mm;height:{A + 2 * SG}mm;z-index:5" '
            f'viewBox="0 0 {L + 2 * SG} {A + 2 * SG}">'
            f'<rect x="{SG}" y="{SG}" width="{L}" height="{A}" fill="none" stroke="#000" stroke-width=".35"/>'
            f'<line x1="{SG + L / 2}" y1="0" x2="{SG + L / 2}" y2="{A + 2 * SG}" stroke="#E5322D" stroke-width=".35" stroke-dasharray="2 1.5"/></svg>')


def doc(title, body, css):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{g.FONTES}{k.FONTS}{g.CSS}{STRIP_CSS}{css}</style></head><body>{body}</body></html>')


# página de apresentação: cordão inteiro em escala + detalhe ampliado
ESC = 1160 / ((L + 2 * SG) * 3.7795)   # mm -> px na tela, cabendo em 1160 px
ZOOM = .9
rows = ""
for i, (nome, desc, (bg, fg, ac, bd)) in enumerate(OPCOES):
    y = 290 + i * 178
    rows += (f'<div class="c-row" style="top:{y}px">'
             f'<div class="c-lab"><small>Final</small><b>{nome}</b><span>{desc}</span></div>'
             f'<div class="c-zoom"><div style="transform:scale({ZOOM});transform-origin:0 0">{faixa(bg, fg, ac, bd)}</div></div>'
             f'<div class="c-full"><div style="transform:scale({ESC:.4f});transform-origin:0 0">{faixa(bg, fg, ac, bd)}</div></div>'
             '</div>')

PAGE = (
    g.blob(1180, 30, 220) + g.blob(60, 760, 260, "g", .7) +
    f'<div class="hd">{g.pill("Lanyard")}<span>95 × 2.4 cm</span></div>'
    '<p class="big" style="position:absolute;left:400px;top:46px;width:820px;font-size:14px;line-height:1.5">'
    'Final design. The pattern repeats along the strap and flips at the middle, so both sides read correctly around the neck. '
    'Close-up on top, full 95 cm strap below.</p>'
    + rows +
    '<div class="ft" style="right:auto;width:400px"><span>Lanyard</span></div>'
)
PAGE_CSS = """
.c-row{position:absolute;left:60px;right:60px;height:160px;z-index:3}
.c-lab{position:absolute;left:0;top:0;width:250px}
.c-lab small{display:block;font-size:11px;font-weight:700;color:#0E8A3A}
.c-lab b{display:block;font-size:24px;font-weight:400;letter-spacing:-.02em}
.c-lab span{display:block;font-size:12.5px;line-height:1.45;color:#333;margin-top:4px}
.c-zoom{position:absolute;left:280px;top:0;width:880px;height:102px;overflow:hidden;border-radius:6px;box-shadow:0 6px 14px rgba(0,0,0,.18)}
.c-full{position:absolute;left:0;top:114px;width:1160px;height:37px;overflow:hidden;border-radius:2px;box-shadow:0 2px 5px rgba(0,0,0,.18)}
"""


def render(name, html, w, h, png=None):
    from playwright.sync_api import sync_playwright
    out = g.B / f"{name}.html"
    out.write_text(html)
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        # tira as repetições que passariam do meio do cordão (sem palavra cortada na dobra)
        pg.evaluate("""() => document.querySelectorAll('.c-half').forEach(h => {
            const lim = h.clientWidth - h.clientWidth * 0.02;
            [...h.querySelectorAll('.c-u')].forEach(u => { if (u.offsetLeft + u.offsetWidth > lim) u.remove(); }); h.style.justifyContent = 'space-evenly'; h.style.paddingLeft = '0';
        })""")
        pg.pdf(path=str(g.B / f"{name}.pdf"), width=w, height=h, print_background=True)
        if png:
            pg.query_selector(".shot").screenshot(path=str(png))
        b.close()


if __name__ == "__main__":
    prev = "--png" in sys.argv
    render("Normani-Cordao-Opcoes", doc("Lanyard", f'<section class="sl shot">{PAGE}</section>', PAGE_CSS),
           "1280px", "720px", g.B / "preview-cordao.png" if prev else None)
    W, H = f"{L + 2 * SG}mm", f"{A + 2 * SG}mm"
    pgcss = f"@page{{size:{W} {H};margin:0}}.pg{{position:relative;width:{W};height:{H};overflow:hidden;break-after:page}}"
    for nome, gd in (("Impressao", False), ("Guias", True)):
        body = "".join(f'<div class="pg">{faixa(bg, fg, ac, bd)}{guias() if gd else ""}</div>'
                       for _, _, (bg, fg, ac, bd) in OPCOES)
        render(f"Normani-Cordao-{nome}", doc(f"Lanyard - {nome}", body, pgcss), W, H)
    print("ok: cordão")
