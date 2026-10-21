#!/usr/bin/env python3
"""Recap da passagem da Normani por São Paulo: uma página 1080x1350 (post vertical do Instagram),
como um mapa de caça ao tesouro. Logo brasil.ir clara, centralizada embaixo."""
import base64, glob, pathlib, sys

B = pathlib.Path(__file__).parent
F = lambda p: base64.b64encode(p.read_bytes()).decode()
U = lambda p, m="image/jpeg": f"data:{m};base64," + F(p)
INTER = (B / "fontes/inter.css").read_text()
SI, SN = F(B / "fontes/InstrumentSerif-italic.woff2"), F(B / "fontes/InstrumentSerif-normal.woff2")
LOGO = U(B.parent / "logo/brasil-ir-branco.png", "image/png")
AV = U(B / "img/avatar.jpg")
BG = U(B / "img/recap/bg.jpg")
I = {k: U(B / f"img/recap/{k}.jpg") for k in ("aeroporto", "spfw", "show", "after")}
GRN, YEL, INK, DEEP, PAPER = "#13B04B", "#F2EC1A", "#0B0B0C", "#0D2A1E", "#F4EEDC"

# números da varredura (dados-varredura/, coletados 20-21/10/2026). Tudo piso: só o que deu para verificar.
X_V, IG_V, TT_V = 3_749_403, 2_441_980, 22_277
LIKES = 217_528 + 260_376 + 2_339
KPI = [("6.2M+", "views on X, Instagram<br>and TikTok"), ("480K+", "likes across<br>199 posts"),
       ("49", "press stories<br>in 35 outlets"), ("2", "Trending stories by X<br>· 24.6K posts")]

STOPS = [
    dict(n="01", day="Thu, Oct 15", t="Touchdown", img="aeroporto", pos="50% 30%",
         txt="Fans at Guarulhos, hugs and autographs.",
         m=[("370K", "views · Hugo Gloss video"), ("12.2K", "posts · X story on her arrival")]),
    dict(n="02", day="Fri, Oct 16", t="The tweet", img=None,
         txt="“Brasil, I’m not devastated. I’m MOTIVATED.”",
         m=[("146", "tweets about the trip"), ("3.7M", "views on X in four days")]),
    dict(n="03", day="Sat, Oct 17", t="Meli Music", img="show", pos="50% 40%",
         txt="First solo show in Brazil, sold-out Pacaembu.",
         m=[("1M+", "IG views · 22 show posts"), ("734K", "views · “Motivation” clip")]),
    dict(n="04", day="Sat, Oct 17", t="Runway", img="spfw", pos="50% 35%",
         txt="From the stage to open Dendezeiro at SPFW.",
         m=[("409K", "IG views · 13 runway posts"), ("76K", "views · Dendezeiro on X")]),
    dict(n="05", day="Sat night", t="The after", img="after", pos="50% 30%",
         txt="Hosted by Sharp. “Bonde das Maravilhas” went viral.",
         m=[("637K", "IG views · 4 after posts"), ("43K", "IG likes · 4 after posts")]),
]
TW = [("1M+", "views"), ("84.6K", "likes"), ("6K", "reposts")]
BARS = [("X", X_V, "3.75M"), ("Instagram", IG_V, "2.44M"), ("TikTok", TT_V, "22K")]


def stop(s, side, top):
    pic = (f'<div class="ph" style="background-image:url({I[s["img"]]});background-position:{s["pos"]}"></div>'
           if s["img"] else
           f'<div class="tw"><div class="who"><img src="{AV}"><b>Normani</b></div>'
           f'<div class="nums">{"".join(f"<div><b>{a}</b><small>{b}</small></div>" for a, b in TW)}</div></div>')
    m = "".join(f'<div><b>{a}</b><small>{b}</small></div>' for a, b in s["m"])
    return (f'<div class="stop {side}" style="top:{top}px">'
            f'<div class="pin">{s["n"]}</div>'
            f'<div class="card">{pic}<div class="tx"><small>{s["day"]}</small><h3>{s["t"]}</h3><p>{s["txt"]}</p>'
            f'<div class="m">{m}</div></div></div></div>')


TOPS = [370, 520, 670, 820, 970]
SIDES = ["l", "r", "l", "r", "l"]
# trilha tracejada em S passando pelos pinos
PATH = ("M540 344 C 540 370, 520 380, 520 400 S 560 520, 560 550 S 520 670, 520 700 "
        "S 560 820, 560 850 S 520 970, 520 1000 S 540 1100, 540 1124")
MAXB = max(v for _, v, _ in BARS)

HTML = f"""
<section class="p">
  <div class="bg"></div>
  <svg class="trail" viewBox="0 0 1080 1350"><path d="{PATH}"/></svg>
  <div class="hd">
    <span class="kick">Field notes · São Paulo, October 15–18, 2026</span>
    <h1>Normani’s <i>São Paulo</i> trail</h1>
    <p>Four days, one city, and a lot of love along the way.</p>
  </div>
  <div class="kp">{"".join(f'<div><b>{a}</b><small>{b}</small></div>' for a, b in KPI)}</div>
  {"".join(stop(s, sd, t) for s, sd, t in zip(STOPS, SIDES, TOPS))}
  <div class="ch"><span class="lb">Where Brazil watched · views by platform</span>
    {"".join(f'<div class="br"><span>{n}</span><i style="width:{max(v / MAXB * 640, 4):.0f}px"></i><b>{t}</b></div>' for n, v, t in BARS)}
  </div>
  <div class="ft"><p>Obrigado, Brasil.</p><img src="{LOGO}"></div>
</section>"""

CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url(data:font/woff2;base64,{SI})}}
@font-face{{font-family:'IS';font-style:normal;src:url(data:font/woff2;base64,{SN})}}
*{{margin:0;padding:0;box-sizing:border-box}}
@page{{size:1080px 1350px;margin:0}}
body{{font-family:Inter,sans-serif}}
.p{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{DEEP} url({BG}) center/cover;color:#fff}}
.bg{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,24,18,.4) 0%,rgba(6,24,18,.08) 30%,rgba(6,24,18,.1) 65%,rgba(6,24,18,.65) 100%)}}
.trail{{position:absolute;inset:0;width:1080px;height:1350px}}
.trail path{{fill:none;stroke:{YEL};stroke-width:3;stroke-dasharray:2 12;stroke-linecap:round;opacity:.85}}
.hd{{position:absolute;left:64px;right:64px;top:44px;text-align:center}}
.kick{{font-size:13px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{YEL}}}
.hd h1{{font-family:'IS';font-weight:400;font-size:70px;line-height:1;margin-top:10px;letter-spacing:-.01em}}
.hd h1 i{{color:{YEL}}}
.hd p{{font-size:17px;opacity:.95;margin-top:8px}}
.kp{{position:absolute;left:40px;right:40px;top:206px;display:grid;grid-template-columns:repeat(4,1fr);gap:2px;
  background:rgba(6,24,18,.55);border-radius:20px;overflow:hidden;backdrop-filter:blur(6px)}}
.kp div{{padding:16px 10px 14px;text-align:center;background:rgba(255,255,255,.03)}}
.kp b{{display:block;font-family:'IS';font-weight:400;font-size:50px;line-height:1;color:{YEL}}}
.kp small{{display:block;font-size:12.5px;line-height:1.35;margin-top:6px;opacity:.92}}
.stop{{position:absolute;width:1080px;height:136px}}
.pin{{position:absolute;top:42px;width:52px;height:52px;border-radius:50%;background:{YEL};color:{INK};
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;box-shadow:0 0 0 6px rgba(242,236,26,.18)}}
.stop.l .pin{{left:494px}} .stop.r .pin{{left:534px}}
.card{{position:absolute;top:0;width:440px;height:136px;background:{PAPER};color:{INK};border-radius:16px;display:flex;overflow:hidden;
  box-shadow:0 12px 26px rgba(0,0,0,.35)}}
.stop.l .card{{left:40px;transform:rotate(-1deg)}} .stop.r .card{{left:600px;transform:rotate(1deg)}}
.ph{{width:104px;flex:none;background-size:cover}}
.tx{{padding:11px 16px;display:flex;flex-direction:column;flex:1}}
.tx small{{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:{GRN}}}
.tx h3{{font-family:'IS';font-weight:400;font-size:27px;line-height:1;margin:2px 0 3px}}
.tx p{{font-size:12px;line-height:1.35}}
.m{{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:10px;border-top:1px solid rgba(11,11,12,.14);padding-top:6px}}
.m b{{display:block;font-size:19px;font-weight:800;letter-spacing:-.02em;line-height:1;color:{GRN}}}
.m small{{display:block;font-size:9.5px;font-weight:500;letter-spacing:0;text-transform:none;color:#555;margin-top:2px;line-height:1.25}}
.tw{{width:150px;flex:none;background:#fff;padding:10px 12px;border-right:1px solid #e6e1d2;display:flex;flex-direction:column;justify-content:space-between}}
.who{{display:flex;align-items:center;gap:7px;font-size:12px}}
.who img{{width:26px;height:26px;border-radius:50%;object-fit:cover}}
.nums{{display:grid;grid-template-columns:1fr 1fr;gap:3px 8px}}
.nums div:first-child{{grid-column:span 2}}
.nums b{{display:block;font-size:16px;font-weight:800;letter-spacing:-.02em;line-height:1}}
.nums div:first-child b{{font-size:26px;color:{GRN}}}
.nums small{{font-size:9.5px;color:#666;display:block}}
.ch{{position:absolute;left:40px;right:40px;top:1128px;background:rgba(6,24,18,.55);border-radius:20px;padding:14px 26px 12px;backdrop-filter:blur(6px)}}
.lb{{display:block;font-size:11.5px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{YEL};margin-bottom:8px}}
.br{{display:flex;align-items:center;gap:14px;height:22px;margin-bottom:5px}}
.br span{{width:110px;font-size:14px;font-weight:600}}
.br i{{height:14px;border-radius:0 4px 4px 0;background:{YEL}}}
.br b{{font-size:15px;font-weight:800}}
.ft{{position:absolute;left:0;right:0;bottom:22px;display:flex;flex-direction:column;align-items:center;gap:6px}}
.ft p{{font-family:'IS';font-style:italic;font-size:20px;opacity:.85}}
.ft img{{height:40px}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Normani’s São Paulo trail</title><style>{INTER}{CSS}</style></head><body>{HTML}</body></html>'
    out = B / "Recap-Normani-SP.html"
    out.write_text(html)
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.screenshot(path=str(B / "Recap-Normani-SP.png"))
        pg.pdf(path=str(B / "Recap-Normani-SP.pdf"), width="1080px", height="1350px", print_background=True)
        b.close()
    print("ok")
