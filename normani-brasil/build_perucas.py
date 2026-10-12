#!/usr/bin/env python3
"""Normani × Brasil 2026: página única com o orçamento das perucas do Normani front row (PDF 1280x720)."""
import glob, sys
import build_geral as g

QTD = 50
USD = 4.99  # R$ por US$ (cotação de 12/10/2026)
# (opção, fotos, preço cheio, preço a partir de 20 un., observação)
OPCOES = [
    ("A", ["img/peruca_a.jpg"], "R$38", 33, "R$33 each from 20 units"),
    ("B", ["img/peruca_b1.jpg", "img/peruca_b2.jpg"], None, 30, "R$30 each from 20 units"),
]


def brl(v):
    return "R$" + f"{v:,}".replace(",", ".")


def usd(v):
    return f"US${v / USD:,.2f}"


def card(op, fotos, cheio, preco, obs):
    imgs = "".join(f'<i style="background-image:url({g.uri(f)})"></i>' for f in fotos)
    cheio_html = f'<s>{cheio}</s> ' if cheio else ""
    return (f'<div class="op"><div class="ph2">{imgs}</div>'
            f'<div class="tx"><span class="pill">Option {op}</span>'
            f'<p class="pu">{cheio_html}<b>R${preco}</b><small> / wig</small></p>'
            f'<p class="us">≈ {usd(preco)} / wig</p>'
            f'<p class="ob">{obs}</p>'
            f'<div class="tot"><span>{QTD} wigs × R${preco}</span><div><b>{brl(QTD * preco)}</b>'
            f'<small>≈ {usd(QTD * preco)}</small></div></div></div></div>')


HTML = (
    g.blob(330, 40, 230) + g.blob(80, 760, 280, "g", .8) + g.blob(1250, 760, 240) +
    f'<div class="hd">{g.pill("Idea")}<span>The Normani front row</span></div>'
    '<h1 class="t2" style="left:60px;top:105px;font-size:54px;line-height:1.02">Wigs for<br>the front row</h1>'
    '<p class="big" style="position:absolute;left:60px;top:240px;width:390px;font-size:16px;line-height:1.5">'
    'The idea: hand out black wigs with bangs, her signature look, to the fans at the front before the show. '
    'A crowd of fans dressed as Normani, like Karol G did at Coachella 2022.</p>'
    f'<div class="oval" style="left:60px;top:420px;width:150px;height:150px;border:4px solid #F2EC1A;'
    f'background-image:url({g.IMG["normani_close"]});background-position:50% 30%;background-size:cover"></div>'
    '<p style="position:absolute;left:230px;top:448px;width:220px;font-size:14px;line-height:1.45;z-index:3">'
    f'<b>{QTD} wigs</b><br>synthetic, black, with bangs, to hand out at the front.</p>'
    '<div class="ops">' + "".join(card(*o) for o in OPCOES) + '</div>'
    + f'<p class="src" style="left:490px;bottom:52px">Exchange rate: US$1 = R${USD:.2f} (Oct 12, 2026). Dollar values are approximate.</p>'
    + g.ft("Front row wigs", 1)
)

CSS = g.CSS + """
.ops{position:absolute;left:490px;right:60px;top:48px;display:grid;grid-template-columns:1fr 1fr;gap:18px;z-index:3}
.op{background:#fff;border:1.4px solid #0B0B0C;border-radius:22px;overflow:hidden;height:590px;display:flex;flex-direction:column}
.ph2{height:330px;display:flex;border-bottom:1.4px solid #0B0B0C}
.ph2 i{flex:1;background-size:cover;background-position:center}
.ph2 i+i{border-left:1.4px solid #0B0B0C}
.tx{padding:16px 20px 18px;display:flex;flex-direction:column;flex:1}
.tx .pill{align-self:flex-start}
.pu{font-size:34px;letter-spacing:-.03em;margin-top:12px;line-height:1}
.pu b{font-weight:400}
.pu s{color:#888;font-size:22px}
.pu small{font-size:14px;letter-spacing:0;color:#444}
.us{font-size:15px;color:#444;margin-top:6px}
.tot>div{text-align:right;line-height:1}
.tot small{display:block;font-size:14px;color:#333;margin-top:4px}
.ob{font-size:13px;color:#0E8A3A;font-weight:600;margin-top:6px}
.tot{margin-top:auto;background:#F2EC1A;border:1.4px solid #0B0B0C;border-radius:16px;padding:10px 16px;display:flex;justify-content:space-between;align-items:center}
.tot span{font-size:12.5px;font-weight:600}
.tot b{font-size:32px;font-weight:400;letter-spacing:-.03em}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Front row wigs</title>'
            f'<style>{g.FONTES}{CSS}</style></head><body><section class="sl">{HTML}</section></body></html>')
    out = g.B / "Normani-Perucas-Front-Row.html"
    out.write_text(html)
    pdf = g.B / "Normani-Perucas-Front-Row.pdf"
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True)
        if "--png" in sys.argv:
            pg.query_selector("section.sl").screenshot(path=str(g.B / "preview-perucas.png"))
        b.close()
    print(pdf.name)
