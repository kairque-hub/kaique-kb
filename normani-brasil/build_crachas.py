#!/usr/bin/env python3
"""Normani × Brasil 2026: página única com três propostas de crachá AAA (PDF 1280x720)."""
import base64, glob, sys
import build_geral as g

DAFOE = base64.b64encode((g.B / "fontes/MrDafoe.woff2").read_bytes()).decode()
FOTO = g.uri("img/cracha_normani.jpg")
ROSTO = g.uri("img/cracha_rosto.jpg")


def estrela(x, y, s):
    return (f'<svg class="x-st" style="left:{x}%;top:{y}%;width:{s}px;height:{s}px" viewBox="0 0 20 20">'
            '<path d="M10 0 L11.3 8.7 L20 10 L11.3 11.3 L10 20 L8.7 11.3 L0 10 L8.7 8.7Z" fill="#fff"/></svg>')


def logo(size, cor="#fff"):
    """logo 'Normani' refeita: script com brilho e estrelinhas"""
    stars = estrela(6, 2, size * .32) + estrela(30, 18, size * .22) + estrela(52, 22, size * .18) + estrela(88, 8, size * .26)
    return (f'<div class="x-lg" style="font-size:{size}px;color:{cor}">'
            f'<span>Normani</span>{stars}</div>')


def alca(cor, texto="", tcor="#0B0B0C"):
    t = f'<span style="color:{tcor}">{texto}</span>' if texto else '<i class="x-rv"></i><i class="x-rv" style="top:62px"></i>'
    return f'<div class="x-strap" style="background:{cor}">{t}</div><div class="x-clip"><b></b><i></i></div>'


# 01: foto com degradê rosa (ref. crachá vermelho)
c1 = (alca("#F49AB0") +
      f'<div class="x-card x-c1"><div class="x-ph" style="background-image:url({FOTO})"></div>'
      '<div class="x-fade"></div>'
      f'<div class="x-lgw">{logo(46)}</div>'
      '<div class="x-bt"><p class="x-nm">NORMANI</p><p class="x-ev">Brazil 2026</p></div>'
      '<b class="x-aaa">AAA</b></div>')

# 02: escuro com a foto e AAA grande (ref. crachá azul)
c2 = (alca("#0B0B0C") +
      f'<div class="x-card x-c2"><div class="x-ph" style="background-image:url({FOTO})"></div>'
      '<div class="x-dk"></div>'
      f'<div class="x-lgw" style="top:18px">{logo(44, "#FBD3DD")}</div>'
      '<b class="x-aaa">AAA</b>'
      '<div class="x-bt"><p class="x-nm">NORMANI</p><p class="x-ev">Brazil 2026</p></div></div>')

# 03: ID com campos (ref. crachá neon)
barras = "".join(f'<i style="width:{w}px"></i>' for w in [2, 1, 3, 1, 1, 2, 4, 1, 2, 1, 3, 1, 2, 2, 1, 4, 1, 1, 3, 2, 1, 2, 1, 3, 1, 2, 4, 1, 2, 1, 1, 3])
c3 = (alca("#F2EC1A", "NORMANI ✶ BRAZIL 2026 ✶ AAA") +
      '<div class="x-card x-c3"><span class="x-cr" style="left:12px">+</span><span class="x-cr" style="right:12px">+</span>'
      f'<div class="x-idp"><i style="background-image:url({ROSTO})"></i></div>'
      '<div class="x-fl"><small>Name</small><b>NORMANI</b></div>'
      '<div class="x-fl"><small>Event</small><b>Brazil 2026</b></div>'
      '<div class="x-fl"><small>Access</small><b class="x-big">AAA</b></div>'
      f'<div class="x-bot"><div class="x-bc">{barras}</div>{logo(30, "#F2EC1A")}</div></div>')

HTML = (
    g.blob(150, 60, 260) + g.blob(80, 760, 300, "g", .8) +
    f'<div class="hd">{g.pill("Credentials")}<span>All access</span></div>'
    '<h1 class="t2" style="left:60px;top:105px;font-size:56px;line-height:1.02">AAA<br>badges</h1>'
    '<p class="x-big" style="position:absolute;left:60px;top:245px;width:280px;font-size:16px;line-height:1.5">'
    'Three options for Normani’s all-access credential in Brazil, with her photo and logo.</p>'
    '<div class="x-opts"><p><small>01</small>Photo + pink fade</p><p><small>02</small>Dark, big AAA</p><p><small>03</small>ID card</p></div>'
    f'<div class="x-bdg" style="left:390px">{c1}</div>'
    f'<div class="x-bdg" style="left:680px">{c2}</div>'
    f'<div class="x-bdg" style="left:970px">{c3}</div>'
    + '<div class="ft" style="right:auto;width:280px"><span>AAA badges</span></div>'
)

CSS = g.CSS + f"""
@font-face{{font-family:'Mr Dafoe';src:url(data:font/woff2;base64,{DAFOE})}}
.x-opts{{position:absolute;left:60px;top:360px;width:280px;z-index:3}}
.x-opts p{{display:flex;gap:16px;font-size:14.5px;border-top:1.4px solid #0B0B0C;padding:9px 0}}
.x-opts small{{font-size:11.5px;font-weight:700;color:#0E8A3A}}
.x-bdg{{position:absolute;top:0;width:250px;height:690px;z-index:3}}
.x-lb{{position:absolute;left:0;right:0;bottom:-4px;text-align:center;font-size:11px;font-weight:600}}
.x-strap{{position:absolute;left:105px;top:-10px;width:40px;height:205px;border-radius:0 0 4px 4px;box-shadow:inset -6px 0 8px rgba(0,0,0,.18);display:flex;justify-content:center}}
.x-strap span{{writing-mode:vertical-rl;transform:rotate(180deg);font-size:10px;font-weight:800;letter-spacing:.12em;padding-top:14px;white-space:nowrap}}
.x-strap .x-rv{{position:absolute;top:40px;left:16px;width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff,#9a9a9a)}}
.x-clip{{position:absolute;left:110px;top:188px;width:30px;height:70px}}
.x-clip b{{position:absolute;left:3px;top:0;width:24px;height:22px;border:4px solid #b9b9bd;border-radius:50% 50% 40% 40%;}}
.x-clip i{{position:absolute;left:10px;top:18px;width:10px;height:46px;border-radius:5px;background:linear-gradient(90deg,#8d8d92,#f2f2f4 45%,#a3a3a8)}}
.x-card{{position:absolute;left:0;top:250px;width:250px;height:400px;border-radius:16px;overflow:hidden;box-shadow:0 18px 30px rgba(0,0,0,.28)}}
.x-card:before{{content:"";position:absolute;left:107px;top:10px;width:36px;height:9px;border-radius:5px;background:rgba(0,0,0,.55);z-index:9}}
.x-card .x-ph{{position:absolute;inset:0;background-size:cover;background-position:50% 12%}}
.x-lg{{position:relative;font-family:'Mr Dafoe';line-height:1;text-shadow:0 0 6px rgba(255,255,255,.9),0 0 16px rgba(255,190,210,.8);white-space:nowrap}}
.x-lg .x-st{{position:absolute;filter:drop-shadow(0 0 3px #fff)}}
.x-lgw{{position:absolute;left:0;right:0;top:206px;display:flex;justify-content:center;z-index:3}}
.x-c1 .x-fade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(244,154,176,0) 38%,rgba(244,154,176,.85) 58%,#F49AB0 72%)}}
.x-bt{{position:absolute;left:20px;bottom:18px;z-index:3}}
.x-nm{{font-size:25px;font-weight:700;letter-spacing:.06em;line-height:1}}
.x-ev{{font-size:13px;font-weight:500;margin-top:4px}}
.x-c1 .x-bt{{color:#fff}}
.x-c1 .x-aaa{{position:absolute;right:16px;bottom:16px;font-size:30px;font-weight:800;color:#fff;letter-spacing:.02em}}
.x-c2{{background:#0B0B0C}}
.x-c2 .x-ph{{filter:grayscale(1) contrast(1.1);opacity:.75}}
.x-c2 .x-dk{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,12,.55) 0%,rgba(11,11,12,0) 30%,rgba(11,11,12,.2) 55%,#0B0B0C 85%)}}
.x-c2 .x-aaa{{position:absolute;left:18px;bottom:62px;font-size:84px;font-weight:800;line-height:1;color:#F2EC1A;letter-spacing:-.03em;z-index:3}}
.x-c2 .x-bt{{color:#fff;bottom:18px;display:flex;align-items:baseline;gap:10px}}
.x-c2 .x-nm{{font-size:18px}}.x-c2 .x-ev{{margin:0;color:#FBD3DD}}
.x-c3{{background:#0B0B0C;color:#F2EC1A;padding:26px 20px 0}}
.x-c3 .x-cr{{position:absolute;top:8px;color:#888;font-size:14px}}
.x-idp{{height:150px;background:#F2EC1A;position:relative;overflow:hidden}}
.x-idp i{{position:absolute;inset:0;background-size:cover;background-position:50% 72%;filter:grayscale(1) contrast(1.3) brightness(1.55);mix-blend-mode:multiply}}
.x-bot{{display:flex;align-items:center;justify-content:space-between;margin-top:12px}}
.x-lgs{{position:absolute;left:0;right:0;top:150px;display:flex;justify-content:center}}
.x-fl{{border-bottom:1px solid #5a5a1e;padding:5px 0 4px}}
.x-fl:first-of-type{{margin-top:12px}}
.x-fl small{{display:block;font-size:9.5px;color:#ccc}}
.x-fl b{{font-size:17px;font-weight:700;letter-spacing:.03em}}
.x-fl b.x-big{{font-size:24px}}
.x-bc{{display:flex;gap:2px;height:34px}}
.x-bc i{{background:#F2EC1A;height:100%}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AAA badges</title>'
            f'<style>{g.FONTES}{CSS}</style></head><body><section class="sl">{HTML}</section></body></html>')
    out = g.B / "Normani-Crachas-AAA.html"
    out.write_text(html)
    pdf = g.B / "Normani-Crachas-AAA.pdf"
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True)
        if "--png" in sys.argv:
            pg.query_selector("section.sl").screenshot(path=str(g.B / "preview-crachas.png"))
        b.close()
    print(pdf.name)
