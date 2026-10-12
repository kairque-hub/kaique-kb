#!/usr/bin/env python3
"""Normani × Brasil 2026: crachás AAA no formato do gabarito (arredondado, com furo).

Gera:
  Normani-Crachas-AAA.pdf            página de apresentação com as 6 opções (1280x720)
  Normani-Crachas-AAA-Impressao.pdf  uma opção por página, com sangria, sem guias
  Normani-Crachas-AAA-Guias.pdf      igual, com as linhas de sangria, corte e furo para conferência

Proporções tiradas do gabarito da gráfica: corte em formato de pílula (semicírculos em cima e embaixo),
sangria em volta e furo centralizado no topo. Na sangria entra só o fundo.
"""
import base64, glob, sys
import build_geral as g

# geometria (unidades = px do gabarito / 2)
CW, CH = 495, 773            # linha de corte
BW, BH = 632, 901            # linha de sangria
OX, OY = (BW - CW) / 2, 62   # posição do corte dentro da sangria
HOLE_Y, HOLE_R = 50, 12.5    # furo, em coordenadas do corte

YEL, GRN, LAV, INK, PINK = "#F2EC1A", "#13B04B", "#D5D7E3", "#0B0B0C", "#F49AB0"
NAVY, CREAM = "#1D2B6B", "#EEE8DA"


def f64(p):
    return base64.b64encode((g.B / p).read_bytes()).decode()


def png(p):
    return "data:image/png;base64," + f64(p)


HALF = png("img/cracha/halftone.png")
BUST = png("img/cracha/bust.png")
RBW = g.uri("img/cracha/rosto_bw.jpg")
STAND = g.uri("img/stand.jpg")

FONTS = f"""
@font-face{{font-family:'Mr Dafoe';src:url(data:font/woff2;base64,{f64('fontes/MrDafoe.woff2')})}}
@font-face{{font-family:'Instrument Serif';font-style:normal;src:url(data:font/woff2;base64,{f64('fontes/InstrumentSerif-normal.woff2')})}}
@font-face{{font-family:'Instrument Serif';font-style:italic;src:url(data:font/woff2;base64,{f64('fontes/InstrumentSerif-italic.woff2')})}}
"""


def star(x, y, s, cor="#fff"):
    return (f'<svg class="k-st" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px" viewBox="0 0 20 20">'
            f'<path d="M10 0 L11.2 8.8 L20 10 L11.2 11.2 L10 20 L8.8 11.2 L0 10 L8.8 8.8Z" fill="{cor}"/></svg>')


def logo(size, cor="#fff", glow=True):
    """'Normani' refeito: script com brilho e estrelinhas, como na referência"""
    s = size
    stars = (star(s * .12, -s * .18, s * .34) + star(s * 1.2, s * .02, s * .22) +
             star(s * 1.75, s * .08, s * .18) + star(s * 2.55, -s * .06, s * .26))
    sh = "text-shadow:0 0 .08em #fff,0 0 .28em rgba(255,200,220,.9);" if glow else ""
    return (f'<span class="k-lg" style="font-size:{s}px;color:{cor};{sh}">Normani'
            f'{stars if glow else ""}</span>')


def at(x, y, html, w=None, center=False, extra=""):
    st = f"left:{x}px;top:{y}px;" + (f"width:{w}px;" if w else "") + ("text-align:center;" if center else "") + extra
    return f'<div class="k-a" style="{st}">{html}</div>'


def mid(y, html, extra=""):
    return f'<div class="k-a" style="left:0;right:0;top:{y}px;text-align:center;{extra}">{html}</div>'


# ------------------------------------------------------------------ designs
# cada design: (nome, descrição, fundo css da sangria, html em coordenadas do corte)
D = []

# 01 Halftone (design escolhido; a versão por função troca o rodapé)
def halftone(role=None, verde=False, verso=False):
    """verso=True: fundo verde, detalhes em amarelo"""
    ac = YEL if verso else GRN
    glow = "242,236,26" if verso else "19,176,75"
    contorno = ""
    if verde:
        k = 16
        contorno = (f'<svg class="k-a" style="left:0;top:0;z-index:5" width="{CW}" height="{CH}">'
                    f'<rect x="{k}" y="{k}" width="{CW - 2 * k}" height="{CH - 2 * k}" rx="{CW / 2 - k}" '
                    f'fill="none" stroke="{GRN}" stroke-width="3"/>'
                    f'<circle cx="{CW / 2}" cy="{HOLE_Y}" r="{HOLE_R + 7}" fill="none" stroke="{GRN}" stroke-width="3"/></svg>')
    rcor = "color:#fff" if verso else ""
    rodape = contorno + (mid(662, f'<span class="k-role" style="{rcor}"><b style="color:{ac}">●</b> {role.upper()}</span>') if role else "")
    return (
    f'<div class="k-a" style="left:-40px;top:60px;width:575px;height:470px;'
    f'background:radial-gradient(closest-side,rgba({glow},.3),rgba({glow},0))"></div>'
    f'<img class="k-a" src="{BUST}" style="left:17px;top:96px;width:461px;'
    '-webkit-mask-image:linear-gradient(180deg,#000 72%,transparent 92%);mask-image:linear-gradient(180deg,#000 72%,transparent 92%)">'
    '<div class="k-a k-panel" style="left:62px;top:470px;width:371px;height:150px;overflow:hidden">'
    f'<i style="position:absolute;left:0;top:0;bottom:0;width:7px;background:{ac}"></i>'
    '<p class="k-nm" style="font-size:34px">NORMANI</p><p class="k-ev">Brazil 2026</p>'
    f'<div style="position:absolute;left:24px;bottom:14px">{logo(30, INK, False)}</div>'
    '<b class="k-aaa" style="position:absolute;right:22px;top:18px;font-size:58px">AAA</b>'
    f'<span class="k-tag" style="position:absolute;right:24px;bottom:20px;font-size:10px;color:{GRN}">ALL ACCESS</span></div>'
    + rodape)


D.append(("Halftone", "Yellow, cut-out photo, green details", f"background:{YEL}", halftone()))

# 02 Editorial
swirl = (f'<svg class="k-a" style="left:0;top:0" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">'
         f'<path d="M-10 250 C 80 205, 140 300, 205 245 S 300 170, 270 210 S 330 300, 420 238 S 520 200, 520 240" '
         f'fill="none" stroke="{NAVY}" stroke-width="1.6"/>'
         f'<path d="M-10 640 C 90 600, 120 700, 230 650 S 380 590, 520 660" fill="none" stroke="{NAVY}" stroke-width="1.4"/>'
         f'<ellipse cx="247" cy="445" rx="168" ry="176" fill="none" stroke="{NAVY}" stroke-width="1.2"/></svg>')
D.append(("Editorial", "Cream & navy, serif", f"background:{CREAM}",
    swirl +
    mid(92, f'<span class="k-serif" style="font-size:96px;color:{NAVY}">NORMANI</span>') +
    mid(190, f'<span class="k-serif" style="font-size:30px;font-style:italic;color:{NAVY}">Brazil 2026</span>') +
    f'<div class="k-a k-glow" style="left:107px;top:305px;width:280px;height:280px"></div>'
    f'<div class="k-a k-round" style="left:132px;top:330px;width:230px;height:230px;background-image:url({RBW})"></div>' +
    mid(586, f'<span class="k-serif" style="font-size:78px;color:{NAVY};letter-spacing:.04em">AAA</span>') +
    mid(680, logo(36, NAVY, False))))

# 03 Pink glow
D.append(("Pink glow", "Pink, cut-out photo", f"background:{PINK}",
    '<div class="k-a" style="left:-60px;top:40px;width:615px;height:540px;'
    'background:radial-gradient(closest-side,rgba(255,255,255,.95),rgba(255,255,255,.35) 55%,rgba(255,255,255,0))"></div>'
    f'<img class="k-a" src="{BUST}" style="left:-8px;top:88px;width:511px">'
    f'<div class="k-a" style="left:0;right:0;top:420px;height:353px;background:linear-gradient(180deg,rgba(244,154,176,0),{PINK} 45%)"></div>'
    + mid(448, logo(92)) +
    mid(585, '<p class="k-nm" style="font-size:34px;color:#fff">NORMANI</p><p class="k-ev" style="color:#fff">Brazil 2026</p>') +
    mid(668, '<span class="k-pill" style="border-color:#fff;color:#fff">AAA · ALL ACCESS</span>')))

# 04 Noir
D.append(("Noir", "Black, giant AAA", f"background:{INK}",
    f'<img class="k-a" src="{BUST}" style="left:22px;top:84px;width:451px;filter:grayscale(1) contrast(1.15)">'
    f'<div class="k-a" style="left:0;right:0;top:330px;height:220px;background:linear-gradient(180deg,rgba(11,11,12,0),{INK} 75%)"></div>'
    + mid(418, f'<b class="k-aaa" style="font-size:176px;color:{YEL};letter-spacing:-.04em">AAA</b>') +
    mid(590, logo(52, "#FBD3DD")) +
    mid(668, '<span class="k-nm" style="font-size:22px;color:#fff">NORMANI</span>'
             '<span class="k-ev" style="color:#FBD3DD;margin-left:10px;font-size:15px">Brazil 2026</span>')))

# 05 Brasil (identidade do deck)
D.append(("Brasil", "Deck colors, oval photo", f"background:linear-gradient(172deg,{LAV} 0%,{LAV} 22%,{YEL} 58%,#9ADB3E 82%,{GRN} 100%)",
    f'<div class="k-a" style="left:112px;top:92px;width:270px;height:340px;border-radius:50%;border:2px solid {INK};'
    f'background:url({STAND}) 50% 6%/150% auto"></div>'
    + mid(372, logo(58)) +
    mid(452, f'<span style="font-size:62px;letter-spacing:-.045em;color:{INK}">NORMANI</span>') +
    mid(530, f'<span class="k-pill">Brazil 2026</span>') +
    f'<div class="k-a" style="left:187px;top:578px;width:120px;height:120px;border-radius:50%;background:{INK};'
    f'display:flex;align-items:center;justify-content:center"><b class="k-aaa" style="color:{YEL};font-size:40px">AAA</b></div>'))

# 06 Verso
stars = "".join(star(x, y, s, "rgba(255,255,255,.85)") for x, y, s in
                [(70, 170, 14), (400, 150, 18), (60, 520, 12), (420, 560, 15), (110, 330, 9), (390, 380, 10), (230, 120, 11)])
D.append(("Back side", "Pink, script logo", f"background:linear-gradient(180deg,{PINK},#EC7598)",
    stars +
    mid(140, '<span class="k-tag" style="color:#fff">ALL ACCESS</span>') +
    mid(250, logo(124), "transform:rotate(-7deg)") +
    mid(420, '<b class="k-aaa k-out" style="font-size:120px">AAA</b>') +
    mid(580, '<p class="k-nm" style="font-size:28px;color:#fff">NORMANI</p><p class="k-ev" style="color:#fff">Brazil 2026</p>') +
    mid(672, '<span class="k-tag" style="color:#fff">SÃO PAULO</span>')))


# ------------------------------------------------------------------ render
def badge(bg, inner, guides=False):
    """crachá completo: sangria (fundo) + corte (arte recortada no formato) + furo"""
    gd = ""
    if guides:
        gd = (f'<svg class="k-a" style="left:0;top:0;z-index:20" width="{BW}" height="{BH}">'
              f'<rect x="1" y="1" width="{BW - 2}" height="{BH - 2}" rx="{BW / 2 - 1}" fill="none" stroke="#E5322D" stroke-width="2"/>'
              f'<rect x="{OX}" y="{OY}" width="{CW}" height="{CH}" rx="{CW / 2}" fill="none" stroke="#000" stroke-width="2"/>'
              f'<circle cx="{OX + CW / 2}" cy="{OY + HOLE_Y}" r="{HOLE_R}" fill="none" stroke="#000" stroke-width="2"/></svg>')
    return (f'<div class="k-b" style="{bg}">'
            f'<div class="k-c" style="left:{OX}px;top:{OY}px">{inner}</div>{gd}</div>')


def shown(bg, inner):
    """como fica depois do corte, com o furo vazado (para a página de apresentação)"""
    return (f'<div class="k-cut" style="{bg}">{inner}'
            f'<i class="k-hole" style="left:{CW / 2 - HOLE_R}px;top:{HOLE_Y - HOLE_R}px"></i></div>')


BADGE_CSS = f"""
.k-a{{position:absolute}}
.k-b{{position:relative;width:{BW}px;height:{BH}px;border-radius:{BW / 2}px;overflow:hidden}}
.k-c,.k-cut{{position:absolute;width:{CW}px;height:{CH}px;border-radius:{CW / 2}px;overflow:hidden;font-family:Inter,sans-serif;color:{INK}}}
.k-cut{{position:relative}}
.k-hole{{position:absolute;width:{2 * HOLE_R}px;height:{2 * HOLE_R}px;border-radius:50%;background:{LAV};box-shadow:inset 0 2px 3px rgba(0,0,0,.35);z-index:10}}
.k-lg{{position:relative;display:inline-block;font-family:'Mr Dafoe';line-height:1;white-space:nowrap}}
.k-st{{position:absolute;filter:drop-shadow(0 0 3px #fff)}}
.k-serif{{font-family:'Instrument Serif';line-height:1}}
.k-nm{{font-weight:800;letter-spacing:.05em;line-height:1}}
.k-ev{{font-size:16px;font-weight:500;margin-top:5px}}
.k-aaa{{font-weight:800;line-height:1;letter-spacing:-.02em}}
.k-out{{color:transparent;-webkit-text-stroke:2.5px #fff}}
.k-tag{{font-size:12px;font-weight:700;letter-spacing:.22em}}
.k-pill{{display:inline-block;border:1.6px solid {INK};border-radius:999px;padding:5px 18px;font-size:14px;font-weight:600;letter-spacing:.06em}}
.k-role{{display:inline-block;color:{INK};font-size:16px;font-weight:700;letter-spacing:.22em}}
.k-panel{{background:#fff;border-radius:22px;padding:22px 24px}}
.k-round{{border-radius:50%;background-size:cover;background-position:center;filter:grayscale(1)}}
.k-glow{{border-radius:50%;background:radial-gradient(closest-side,{NAVY} 55%,rgba(29,43,107,.45) 75%,rgba(29,43,107,0))}}
"""

S = .372  # escala na página de apresentação
xs = [52 + i * (CW * S + 14) for i in range(6)]
cards = ""
for (nome, desc, bg, inner), x in zip(D, xs):
    i = D.index((nome, desc, bg, inner)) + 1
    cards += (f'<div class="k-ring" style="left:{x + CW * S / 2 - 9}px"></div>'
              f'<div class="k-show" style="left:{x}px;top:212px;width:{CW * S}px;height:{CH * S}px">'
              f'<div style="transform:scale({S});transform-origin:0 0">{shown(bg, inner)}</div></div>'
              f'<div class="k-cap" style="left:{x}px;width:{CW * S}px"><small>{i:02d}</small><b>{nome}</b><span>{desc}</span></div>')

PAGE = (
    g.blob(1180, 30, 230) + g.blob(60, 760, 260, "g", .7) +
    f'<div class="hd">{g.pill("Credentials")}<span>NORMANI · Brazil 2026 · AAA</span></div>'
    '<h1 class="t" style="top:88px;font-size:50px">AAA badges</h1>'
    '<p class="big" style="position:absolute;left:400px;top:100px;width:820px;font-size:15px;line-height:1.5">'
    'Six design options in the printer’s badge shape: rounded top and bottom, punch hole at the top. '
    'Print files with bleed are delivered separately.</p>'
    + cards +
    '<div class="ft" style="right:auto;width:400px"><span>AAA badges</span></div>'
)

PAGE_CSS = f"""
.k-show{{position:absolute;z-index:3;filter:drop-shadow(0 14px 18px rgba(0,0,0,.22))}}
.k-ring{{position:absolute;top:186px;width:18px;height:40px;z-index:4;border:3px solid #a9a9ae;border-radius:9px;border-bottom-color:#d9d9dd}}
.k-cap{{position:absolute;top:516px;z-index:3;text-align:center}}
.k-cap small{{display:block;font-size:11px;font-weight:700;color:#0E8A3A}}
.k-cap b{{display:block;font-size:18px;font-weight:400;letter-spacing:-.02em;margin-top:2px}}
.k-cap span{{display:block;font-size:12px;color:#444;margin-top:2px}}
"""


def render(path_html, path_pdf, html, w, h, png=None):
    from playwright.sync_api import sync_playwright
    path_html.write_text(html)
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(path_html.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(900)
        pg.pdf(path=str(path_pdf), width=f"{w}px", height=f"{h}px", print_background=True)
        if png:
            for i, el in enumerate(pg.query_selector_all(".shot"), 1):
                el.screenshot(path=str(png).format(i))
        b.close()


def doc(title, body, extra_css="", w=1280, h=720):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{g.FONTES}{FONTS}{g.CSS}{BADGE_CSS}{extra_css}'
            f'@page{{size:{w}px {h}px;margin:0}}.pg{{width:{w}px;height:{h}px;position:relative;overflow:hidden;break-after:page;background:#fff}}</style>'
            f'</head><body>{body}</body></html>')


# ------------------------------------------------------------------ verso verde (opção)
stars_v = "".join(star(x, y, sz, "rgba(242,236,26,.9)") for x, y, sz in
                  [(80, 190, 14), (395, 165, 18), (70, 560, 12), (410, 590, 15), (120, 360, 9), (380, 400, 10)])
VERSO = (stars_v +
         f'<svg class="k-a" style="left:0;top:0" width="{CW}" height="{CH}"><rect x="16" y="16" width="{CW - 32}" height="{CH - 32}" '
         f'rx="{CW / 2 - 16}" fill="none" stroke="{YEL}" stroke-width="3"/></svg>' +
         mid(170, f'<span class="k-tag" style="color:{YEL}">ALL ACCESS</span>') +
         mid(270, logo(116, YEL, False), "transform:rotate(-7deg)") +
         mid(430, f'<b class="k-aaa" style="font-size:150px;color:{YEL};letter-spacing:-.04em">AAA</b>') +
         mid(610, '<p class="k-nm" style="font-size:28px;color:#fff">NORMANI</p><p class="k-ev" style="color:#fff">Brazil 2026</p>'))
VERSO_BG = f"background:{GRN}"

# ------------------------------------------------------------------ versões finais
VERSOES = [("AAA", None), ("Creative team", "Creative team"), ("Management", "Management"),
           ("Tour manager", "Tour manager"), ("Staff", "Staff")]
BG = f"background:{YEL}"
SV = .36
vx = [(1280 - 6 * CW * SV - 5 * 18) / 2 + i * (CW * SV + 18) for i in range(6)]
FINAL = (
    g.blob(1180, 30, 230) + g.blob(60, 760, 260, "g", .7) +
    f'<div class="hd">{g.pill("Credentials")}<span>NORMANI · Brazil 2026</span></div>'
    '<h1 class="t" style="top:88px;font-size:50px">Badges</h1>'
    '<p class="big" style="position:absolute;left:330px;top:100px;width:880px;font-size:15px;line-height:1.5">'
    'Five versions, Normani’s AAA badge plus one for each team, with the role at the bottom. '
    'Yellow on the front, green on the back, with her photo on both sides.</p>'
    + "".join(
        f'<div class="k-ring" style="left:{x + CW * SV / 2 - 9}px"></div>'
        f'<div class="k-show" style="left:{x}px;top:212px;width:{CW * SV}px;height:{CH * SV}px">'
        f'<div style="transform:scale({SV});transform-origin:0 0">{shown(BG, halftone(r))}</div></div>'
        f'<div class="k-cap" style="left:{x}px;width:{CW * SV}px;top:505px"><small>{i:02d}</small><b>{n}</b></div>'
        for i, ((n, r), x) in enumerate(zip(VERSOES, vx), 1))
    + f'<div class="k-ring" style="left:{vx[5] + CW * SV / 2 - 9}px"></div>'
    f'<div class="k-show" style="left:{vx[5]}px;top:212px;width:{CW * SV}px;height:{CH * SV}px">'
    f'<div style="transform:scale({SV});transform-origin:0 0">{shown(VERSO_BG, halftone("Tour manager", verso=True))}</div></div>'
    f'<div class="k-cap" style="left:{vx[5]}px;width:{CW * SV}px;top:505px"><small>Back</small><b>Green, same role</b></div>'
    + '<div class="ft" style="right:auto;width:400px"><span>Badges</span></div>'
)

SC = .52
cmp_items = [("Current", BG, halftone("Tour manager")),
             ("Green contour + hole ring", BG, halftone("Tour manager", True)),
             ("Green back side", VERSO_BG, VERSO)]
cx = [(1280 - 3 * CW * SC - 2 * 60) / 2 + i * (CW * SC + 60) for i in range(3)]
COMPARA = (
    g.blob(1180, 30, 230) + g.blob(60, 760, 260, "g", .7) +
    f'<div class="hd">{g.pill("Credentials")}<span>Green details</span></div>'
    + "".join(
        f'<div class="k-ring" style="left:{x + CW * SC / 2 - 9}px;top:96px"></div>'
        f'<div class="k-show" style="left:{x}px;top:122px;width:{CW * SC}px;height:{CH * SC}px">'
        f'<div style="transform:scale({SC});transform-origin:0 0">{shown(bg, inn)}</div></div>'
        f'<div class="k-cap" style="left:{x}px;width:{CW * SC}px;top:540px"><small>{i:02d}</small><b>{n}</b></div>'
        for i, ((n, bg, inn), x) in enumerate(zip(cmp_items, cx), 1))
    + '<div class="ft" style="right:auto;width:400px"><span>Green details</span></div>'
)

if __name__ == "__main__":
    B = g.B
    prev = "--png" in sys.argv
    render(B / "Normani-Crachas-AAA.html", B / "Normani-Crachas-AAA.pdf",
           doc("AAA badges", f'<section class="sl shot">{PAGE}</section>', PAGE_CSS),
           1280, 720, B / "preview-crachas.png" if prev else None)
    render(B / "Normani-Cracha-AAA-Final.html", B / "Normani-Cracha-AAA-Final.pdf",
           doc("Badges", f'<section class="sl shot">{FINAL}</section>', PAGE_CSS),
           1280, 720, B / "preview-cracha-final.png" if prev else None)
    render(B / "Normani-Crachas-Verde-Opcoes.html", B / "Normani-Crachas-Verde-Opcoes.pdf",
           doc("Green details", f'<section class="sl shot">{COMPARA}</section>', PAGE_CSS),
           1280, 720, B / "preview-cracha-verde.png" if prev else None)
    for nome, guides in (("Impressao", False), ("Guias", True)):
        body = "".join(f'<div class="pg shot">{badge(BG, halftone(r), guides)}</div>'
                       f'<div class="pg shot">{badge(VERSO_BG, halftone(r, verso=True), guides)}</div>' for _, r in VERSOES)
        render(B / f"Normani-Crachas-AAA-{nome}.html", B / f"Normani-Crachas-AAA-{nome}.pdf",
               doc(f"AAA badges - {nome}", body, w=BW, h=BH), BW, BH,
               B / f"preview-cracha-{nome.lower()}-{{}}.png" if prev else None)
    print("ok: apresentação + impressão + guias")
