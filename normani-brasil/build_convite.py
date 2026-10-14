#!/usr/bin/env python3
"""Convite do after NORMANI TAKES SÃO PAULO: story (1080x1920) e feed (1080x1350), em PNG e PDF."""
import base64, glob, sys
import build_geral as g

YEL, GRN, INK = "#F2EC1A", "#13B04B", "#0B0B0C"
F = lambda p: base64.b64encode((g.B / p).read_bytes()).decode()
FONTS = (f"@font-face{{font-family:'IS';font-style:italic;src:url(data:font/woff2;base64,{F('fontes/InstrumentSerif-italic.woff2')})}}"
         f"@font-face{{font-family:'IS';font-style:normal;src:url(data:font/woff2;base64,{F('fontes/InstrumentSerif-normal.woff2')})}}")
ROOM = g.uri("img/after/convite-bg.jpg")


def convite(w, h):
    big = h > 1500
    return f"""
<section class="iv" style="width:{w}px;height:{h}px">
  <div class="bgp" style="background-image:url({ROOM})"></div>
  <div class="shade"></div>
  <div class="glow"></div>
  <div class="in">
    <p class="you">You’re invited</p>
    <h1><span>Normani</span><b>Takes</b><b>São Paulo</b></h1>
    <p class="sub"><i>the official after party</i></p>
    <div class="rule"></div>
    <div class="row">
      <div><small>When</small><p>Oct 17, after the show<br>1 AM – 5 AM</p></div>
      <div><small>Where</small><p>Terraço Notiê<br>Rua Formosa, 157 · Centro</p></div>
    </div>
    <div class="tags"><span>Open bar</span><span>Invite only</span><span>DJs 94tago &amp; Aisha Mbikila</span></div>
    <p class="fine">Name on the list required · Bring your ID · Entry via Shopping Light parking</p>
  </div>
</section>"""


CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000;font-family:Inter,sans-serif}}
.iv{{position:relative;overflow:hidden;background:{INK};color:#fff;break-after:page}}
.bgp{{position:absolute;inset:0;background-size:cover;background-position:50% 50%}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,12,0) 0%,rgba(11,11,12,.25) 40%,rgba(11,11,12,.82) 75%,rgba(11,11,12,.92) 100%)}}
.glow{{position:absolute;left:-20%;right:-20%;bottom:-25%;height:60%;background:none}}
.in{{position:absolute;left:84px;right:84px;bottom:110px}}
.you{{font-size:22px;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:{YEL}}}
h1{{margin-top:22px;line-height:.86}}
h1 span{{display:block;font-family:'IS';font-style:italic;font-weight:400;font-size:190px;letter-spacing:-.02em}}
h1 b{{display:block;font-size:118px;font-weight:800;letter-spacing:-.045em;text-transform:uppercase}}
h1 b:last-child{{color:{YEL}}}
.sub{{font-family:'IS';font-size:44px;margin-top:22px;opacity:.9}}
.rule{{height:2px;background:rgba(255,255,255,.35);margin:42px 0 30px}}
.row{{display:grid;grid-template-columns:1fr 1.3fr;gap:30px}}
.row small{{display:block;font-size:17px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{GRN}}}
.row p{{font-size:34px;font-weight:600;line-height:1.25;margin-top:8px;letter-spacing:-.01em}}
.tags{{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}}
.tags span{{border:2px solid #fff;border-radius:999px;padding:9px 22px;font-size:20px;font-weight:600}}
.tags span:first-child{{background:{YEL};border-color:{YEL};color:{INK}}}
.fine{{font-size:16px;opacity:.6;margin-top:30px;letter-spacing:.02em}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        for nome, (w, h) in {"Story": (1080, 1920), "Feed": (1080, 1350)}.items():
            html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Normani Takes São Paulo</title>'
                    f'<style>{g.FONTES}{FONTS}{CSS}@page{{size:{w}px {h}px;margin:0}}</style></head><body>{convite(w, h)}</body></html>')
            out = g.B / f"Convite-After-{nome}.html"; out.write_text(html)
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
            pg.screenshot(path=str(g.B / f"Convite-After-{nome}.png"))
            pg.pdf(path=str(g.B / f"Convite-After-{nome}.pdf"), width=f"{w}px", height=f"{h}px", print_background=True)
        b.close()
    print("ok")
