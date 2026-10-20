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

# (x, y, rotação) de cada parada; a trilha passa pelos pinos
STOPS = [
    dict(n="01", day="Thu, Oct 15", t="Touchdown", img="aeroporto", pos="50% 30%",
         txt="Fans waiting at the airport. Hugs, selfies and autographs for everyone on the way out.",
         stat=("25K+ views", "on fan clips in the first hours · Hugo Gloss, POPline, Terra")),
    dict(n="02", day="Fri, Oct 16", t="The tweet", img=None,
         txt="“Brasil, I’m not devastated. I’m MOTIVATED.” A Brazilian meme, flipped with love.",
         stat=("Trending in Brazil", "the same night")),
    dict(n="03", day="Sat, Oct 17", t="Runway", img="spfw", pos="50% 35%",
         txt="She opened the Dendezeiro show at São Paulo Fashion Week N61, to screams and applause.",
         stat=("Vogue · Bazaar · ELLE · FFW · CNN", "covered the look")),
    dict(n="04", day="Sat, Oct 17", t="Meli Music", img="show", pos="50% 40%",
         txt="Her first solo show in Brazil, for a sold-out Pacaembu. “Little Secrets” live for the first time.",
         stat=("1st international act", "in the festival’s history")),
    dict(n="05", day="Sat night", t="The after", img="after", pos="50% 30%",
         txt="Hosted by Sharp. She danced “Bonde das Maravilhas”, and the clip went everywhere.",
         stat=("25K views · 3K likes", "on one fan clip alone · Terra, Steal the Look")),
]
TW = [("1M+", "views"), ("84.6K", "likes"), ("6K", "reposts"), ("1.7K", "replies"), ("1.4K", "quotes")]


def stop(s, side, top):
    pic = (f'<div class="ph" style="background-image:url({I[s["img"]]});background-position:{s["pos"]}"></div>'
           if s["img"] else
           f'<div class="tw"><div class="who"><img src="{AV}"><b>Normani</b></div>'
           f'<div class="nums">{"".join(f"<div><b>{a}</b><small>{b}</small></div>" for a, b in TW)}</div></div>')
    st = (f'<p class="st"><b>{s["stat"][0]}</b> {s["stat"][1]}</p>' if s["stat"] else "")
    return (f'<div class="stop {side}" style="top:{top}px">'
            f'<div class="pin">{s["n"]}</div>'
            f'<div class="card">{pic}<div class="tx"><small>{s["day"]}</small><h3>{s["t"]}</h3><p>{s["txt"]}</p>{st}</div></div></div>')


TOPS = [236, 408, 580, 752, 924]
SIDES = ["l", "r", "l", "r", "l"]
# trilha tracejada em S passando pelos pinos (x=540 no centro)
PATH = ("M540 206 C 540 232, 520 242, 520 262 S 560 404, 560 434 S 520 576, 520 606 "
        "S 560 748, 560 778 S 520 920, 520 950 S 540 1060, 540 1100")

HTML = f"""
<section class="p">
  <div class="bg"></div>
  <svg class="trail" viewBox="0 0 1080 1350"><path d="{PATH}"/></svg>
  <div class="hd">
    <span class="kick">Field notes · São Paulo, October 2026</span>
    <h1>Normani’s <i>São Paulo</i> trail</h1>
    <p>Four days, one city, and a lot of love along the way.</p>
  </div>
  {"".join(stop(s, sd, t) for s, sd, t in zip(STOPS, SIDES, TOPS))}
  <div class="end"><span class="x">✕</span><div class="kp">
    <div><b>1M+</b><small>views on her tweet</small></div><div><b>Trending</b><small>topic in Brazil</small></div>
    <div><b>Sold out</b><small>Meli Music, Pacaembu</small></div><div><b>20+</b><small>outlets told the story</small></div></div></div>
  <div class="ft"><p>Obrigado, Brasil.</p><img src="{LOGO}"></div>
</section>"""

CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url(data:font/woff2;base64,{SI})}}
@font-face{{font-family:'IS';font-style:normal;src:url(data:font/woff2;base64,{SN})}}
*{{margin:0;padding:0;box-sizing:border-box}}
@page{{size:1080px 1350px;margin:0}}
body{{font-family:Inter,sans-serif}}
.p{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{DEEP} url({BG}) center/cover;color:#fff}}
.bg{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,24,18,.35) 0%,rgba(6,24,18,.08) 30%,rgba(6,24,18,.1) 70%,rgba(6,24,18,.6) 100%)}}
.trail{{position:absolute;inset:0;width:1080px;height:1350px}}
.trail path{{fill:none;stroke:{YEL};stroke-width:3;stroke-dasharray:2 12;stroke-linecap:round;opacity:.85}}
.hd{{position:absolute;left:64px;right:64px;top:56px;text-align:center}}
.kick{{font-size:14px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:{YEL}}}
.hd h1{{font-family:'IS';font-weight:400;font-size:76px;line-height:1;margin-top:12px;letter-spacing:-.01em}}
.hd h1 i{{color:{YEL}}}
.hd p{{font-size:18px;opacity:.95;margin-top:10px}}
.stop{{position:absolute;width:1080px;height:170px}}
.pin{{position:absolute;top:56px;width:52px;height:52px;border-radius:50%;background:{YEL};color:{INK};
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;box-shadow:0 0 0 6px rgba(242,236,26,.18)}}
.stop.l .pin{{left:494px}} .stop.r .pin{{left:534px}}
.card{{position:absolute;top:0;width:420px;height:170px;background:{PAPER};color:{INK};border-radius:18px;display:flex;overflow:hidden;
  box-shadow:0 14px 30px rgba(0,0,0,.35)}}
.stop.l .card{{left:52px;transform:rotate(-1deg)}} .stop.r .card{{left:608px;transform:rotate(1deg)}}
.ph{{width:120px;flex:none;background-size:cover}}
.tx{{padding:14px 18px;display:flex;flex-direction:column}}
.tx small{{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:{GRN}}}
.tx h3{{font-family:'IS';font-weight:400;font-size:32px;line-height:1;margin:3px 0 5px}}
.tx p{{font-size:13px;line-height:1.38}}
.tx .st{{margin-top:auto;font-size:12px;opacity:.75}}
.tx .st b{{opacity:1;font-weight:700}}
.tw{{width:170px;flex:none;background:#fff;padding:12px 14px;border-right:1px solid #e6e1d2;display:flex;flex-direction:column;justify-content:space-between}}
.who{{display:flex;align-items:center;gap:7px;font-size:12px}}
.who img{{width:28px;height:28px;border-radius:50%;object-fit:cover}}
.who span{{color:#666}}
.nums{{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;margin-top:6px}}
.nums div:first-child{{grid-column:span 2}}
.nums b{{display:block;font-size:18px;font-weight:800;letter-spacing:-.02em;line-height:1}}
.nums div:first-child b{{font-size:28px;color:{GRN}}}
.nums small{{font-size:10px;color:#666;display:block;margin-top:1px}}
.end{{position:absolute;left:64px;right:64px;top:1088px;text-align:center}}
.kp{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px;background:rgba(6,24,18,.55);border-radius:20px;padding:16px 10px;backdrop-filter:blur(6px)}}
.kp b{{display:block;font-family:'IS';font-weight:400;font-size:44px;line-height:1;color:{YEL}}}
.kp small{{display:block;font-size:12.5px;margin-top:4px;opacity:.9}}
.end .x{{display:block;font-size:30px;color:{YEL};font-weight:800;line-height:1}}
.end p{{font-size:12.5px;opacity:.8;margin-top:6px;line-height:1.45}}
.end b{{color:{YEL};opacity:1}}
.ft{{position:absolute;left:0;right:0;bottom:24px;display:flex;flex-direction:column;align-items:center;gap:8px}}
.ft p{{font-family:'IS';font-style:italic;font-size:22px;opacity:.85}}
.ft img{{height:46px}}
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
