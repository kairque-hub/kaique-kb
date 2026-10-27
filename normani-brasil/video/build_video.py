#!/usr/bin/env python3
"""Vídeo gráfico "Normani takes São Paulo" (feed do Instagram, 1080x1350, 30 fps), todo em inglês.

Só motion graphics na identidade do projeto, sem fotos nem vídeos: degradê verde e amarelo, Instrument Serif + Inter,
contadores, ícones e um mapa vetorial com o trajeto da noite do show. Cada quadro é uma página HTML posicionada no
tempo t (render(t) no JS) e fotografada pelo Chromium; as cenas trocam no tempo da trilha (122 BPM). Gera:
  Normani-SP-Highlights.mp4            com trilha
  Normani-SP-Highlights-sem-trilha.mp4 sem áudio, para usar um som do próprio Instagram

Uso: python3 build_video.py [--preview 12.5 30 ...]   (--preview só salva PNGs desses segundos)
"""
import glob, json, math, os, pathlib, subprocess, sys
import datetime as dt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import trilha  # noqa: E402

B = pathlib.Path(__file__).resolve().parent
N = B.parent
M = B / "media"
OUT = pathlib.Path(os.environ.get("VIDEO_CACHE", "/tmp/normani-video-cache"))
FPS, W, H = 30, 1080, 1350
BEAT = 60 / 122
START = {}                                   # início de cada cena com nome, em segundos
APEX = {}                                    # instante do ápice do gráfico (para o "ding")
# faixas da Mixkit (Stock Music Free License): arquivo, BPM original, início (s) escolhido para o drop cair no fim da abertura
TRACKS = {
    "hazy": (M / "mixkit-132-hazy-after-hours.mp3", 121, 11.92),
}
GRN, YEL, INK, PAPER, DEEP = "#13B04B", "#F2EC1A", "#0B0B0C", "#F4EEDC", "#06140e"

# números absolutos, todos verificados nas páginas (dados-varredura/); são piso
D = dict(
    tw_views=1_041_976, tw_likes=84_598, tw_rts=6_063, tw2_views=168_668,
    story1=12_228, story2=12_369, story3=942, story4=1_525,
    press_articles=49, press_outlets=35,
    tweets=15_000, views=6_213_660, likes=480_243,
    thanks_ig_likes=127_547, thanks_x_views=147_485,
)
if (N / "dados-varredura/video_numeros.json").exists():
    D.update(json.loads((N / "dados-varredura/video_numeros.json").read_text()))

OUTLETS = ["Vogue Brasil", "Harper’s Bazaar", "Hugo Gloss", "Steal the Look", "CNN Brasil", "Gshow", "Billboard Brasil",
           "ELLE Brasil", "Glamour", "Veja São Paulo", "Metrópoles", "Terra", "Capricho", "GQ Brasil", "POPline", "Estrelando",
           "TodaTeen", "Tracklist", "Choquei", "Revista Raça", "Mundo Negro", "OFuxico", "Bahia Notícias", "A Gazeta"]


# mapa vetorial: coordenadas em pixels da grade OpenStreetMap z15 a partir do tile (12134, 18588)
def P(lat, lon):
    n = 2 ** 15
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return round((x - 12134) * 256), round((y - 18588) * 256)


PIN = dict(pacaembu=P(-23.5473, -46.6653), ibirapuera=P(-23.5875, -46.6555), notie=P(-23.5455, -46.6375))
ROADS = [  # (nome, pontos lat/lon)
    ("Av. Paulista", [(-23.5555, -46.6620), (-23.5710, -46.6440)]),
    ("Av. 23 de Maio", [(-23.5480, -46.6370), (-23.5530, -46.6400), (-23.5700, -46.6440), (-23.5840, -46.6500)]),
    ("Av. Rebouças", [(-23.5560, -46.6630), (-23.5760, -46.6870)]),
    ("R. da Consolação", [(-23.5440, -46.6440), (-23.5560, -46.6610)]),
    ("Av. Brigadeiro", [(-23.5560, -46.6400), (-23.5830, -46.6610)]),
    ("Av. Pacaembu", [(-23.5300, -46.6620), (-23.5420, -46.6640), (-23.5473, -46.6653)]),
    ("Elevado", [(-23.5390, -46.6700), (-23.5420, -46.6550), (-23.5450, -46.6420)]),
    ("Av. Ibirapuera", [(-23.5900, -46.6650), (-23.6050, -46.6650)]),
]
PARK = [P(*c) for c in [(-23.5815, -46.6560), (-23.5850, -46.6500), (-23.5900, -46.6520), (-23.5930, -46.6590),
                        (-23.5900, -46.6650), (-23.5850, -46.6630)]]


def img(name):
    return (M / name).as_uri()


def b(n):          # batidas -> segundos
    return n * BEAT


# ---------- peças de HTML (tempos relativos ao início da cena, em segundos) ----------
def a(html, d, fx="up", cls="", style="", dur=0.45):
    return f'<div class="a {cls}" data-d="{d:.3f}" data-fx="{fx}" data-dur="{dur}" style="{style}">{html}</div>'


def rv(text, d, cls="", style=""):
    """linha que sobe de dentro de uma máscara"""
    return f'<div class="rvw {cls}" style="{style}"><div class="rv" data-d="{d:.3f}">{text}</div></div>'


def cnt(v, d, suf=""):
    return f'<span class="cnt" data-to="{v}" data-d="{d:.3f}" data-suf="{suf}">0</span>'


def bar(d, style):
    return f'<div class="bar" data-d="{d:.3f}" style="{style}"></div>'


def draw(path, d, dur, cls="ln", vb="0 0 1080 1350", style="left:0;top:0;width:1080px;height:1350px"):
    return (f'<svg class="dsvg" viewBox="{vb}" style="{style}"><path class="draw {cls}" data-d="{d:.3f}" data-dur="{dur:.3f}" d="{path}"/></svg>')


STAR = '<svg viewBox="0 0 100 100"><path d="M50 0 L56 44 L100 50 L56 56 L50 100 L44 56 L0 50 L44 44 Z"/></svg>'


def star(style, spin=40, d=0.0):
    return f'<div class="star" data-spin="{spin}" data-d="{d}" style="{style}">{STAR}</div>'


ICON = {  # traços simples, 48x48
    "mic": '<path d="M24 6a7 7 0 0 1 7 7v10a7 7 0 0 1-14 0V13a7 7 0 0 1 7-7zM12 22a12 12 0 0 0 24 0M24 34v8M17 42h14"/>',
    "runway": '<path d="M18 42 22 6h4l4 36M12 42h24M24 12v26"/>',
    "heart": '<path d="M24 41S7 31 7 18a8.5 8.5 0 0 1 17-2 8.5 8.5 0 0 1 17 2c0 13-17 23-17 23z"/>',
    "glass": '<path d="M14 6h20l-2 14a8 8 0 0 1-16 0zM24 28v12M16 42h16"/>',
    "plane": '<path d="M4 26 44 8l-8 32-10-10-6 10v-14L36 14 14 28z"/>',
    "cam": '<path d="M6 14h9l3-5h12l3 5h9v26H6zM24 34a7 7 0 1 0 0-14 7 7 0 0 0 0 14z"/>',
    "film": '<path d="M8 8h32v32H8zM8 16h32M8 32h32M16 8v8M32 8v8M16 32v8M32 32v8"/>',
}


def icon(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 48 48">{ICON[k]}</svg>'


BRT = dt.timezone(dt.timedelta(hours=-3))
T0 = dt.datetime(2026, 10, 14, tzinfo=BRT)
NB = 13 * 4                                   # 14 a 26 de outubro, blocos de 6 h
PEAKS = []


def conv_series():
    """curtidas por bloco de 6 h (horário de Brasília) nos posts da varredura no X e no Instagram"""
    V = N / "dados-varredura"
    ev, seen = [], set()
    def add(when, likes, key=None):
        if key and key in seen: return
        if key: seen.add(key)
        ev.append((when, likes or 0))
    for f in ("x_rows.json", "x_tweets_novos.json"):
        for r in json.loads((V / f).read_text()):
            add(dt.datetime.strptime(r["date"], "%a %b %d %H:%M:%S %z %Y"), r.get("likes"), "x" + r["id"])
    for r in json.loads((V / "varredura_2026-10-26.json").read_text())["new_tweets"]:
        add(dt.datetime.fromisoformat(r["date_utc"].replace("Z", "+00:00")), r.get("likes"), "x" + str(r["id"]))
    add(dt.datetime(2026, 10, 25, 22, 6, tzinfo=dt.timezone.utc), 15_135, "x2114478770203791728")
    for p in json.loads((V / "instagram.json").read_text())["posts"]:
        add(dt.datetime.fromisoformat(p["date"].replace("Z", "+00:00")), p.get("likes"), "ig" + p["shortcode"])
    add(dt.datetime(2026, 10, 25, 21, 44, tzinfo=dt.timezone.utc), D["thanks_ig_likes"], "igDe7s9Cpkhtz")
    vals = [0.0] * NB
    for when, likes in ev:
        i = int((when.astimezone(BRT) - T0).total_seconds() // (6 * 3600))
        if 0 <= i < NB: vals[i] += likes
    vals = [v ** 0.75 for v in vals]
    vals = [0.2 * a + 0.6 * c + 0.2 * e for a, c, e in zip([vals[0]] + vals[:-1], vals, vals[1:] + [vals[-1]])]
    blk = lambda day, hour: (day - 14) * 4 + hour // 6
    PEAKS[:] = [(blk(15, 12), "Arrival"), (blk(16, 18), "The tweet"), (blk(17, 18), "Show + Dendezeiro"),
                (blk(18, 12), "After party"), (blk(25, 18), "Her thank-you")]
    labels = [((d - 14) * 4, f"OCT {d}") for d in range(14, 27, 2)]
    return vals, labels


SCENES = []
HTML = []


def scene(beats, html, cls="grad", key=None):
    SCENES.append((beats, html, cls, key))


def build():
    # 0 · abertura
    scene(8, star("left:780px;top:150px;width:190px", 30, 0.3) + star("left:110px;top:1040px;width:120px", -50, 0.6) +
          rv('Normani', 0.3, "hero", "top:380px") +
          rv('takes <i>São Paulo</i>', 0.9, "sub c", "top:660px") +
          bar(1.5, "left:390px;top:810px;width:300px") +
          a('October 15 — 18, 2026', 1.7, cls="date c", style="top:840px"), "grad intro")

    # 1 · chegada
    arc = "M130 520 Q 540 120 900 470"
    scene(6, a('Oct 15', 0.05, cls="kick", style="left:80px;top:90px") +
          draw(arc, 0.2, 1.4, "dash") +
          f'<div class="mover" data-path="{arc}" data-d="0.2" data-dur="1.4">{icon("plane", "ic big")}</div>' +
          a('<i></i><span>GRU</span>', 1.5, "scale", cls="dot", style="left:900px;top:470px") +
          rv('Landed in', 0.4, "ttl", "left:70px;top:720px") + rv('São Paulo.', 0.6, "ttl it", "left:70px;top:850px") +
          a('Fans, flowers and autographs at Guarulhos airport.', 1.0, cls="body", style="left:70px;top:1050px"))

    # 2 · o tweet
    tw = ('<div class="tw"><div class="who"><img class="av" src="' + (N / "img/avatar.jpg").as_uri() + '"><div><b>Normani</b><span>@Normani · Oct 16</span></div></div>'
          '<p class="hl"><mark>Brasil, I’m not devastated. I’m MOTIVATED.</mark></p>'
          '<p>I can’t believe I’m here after so long. I landed listening to Duquesa, Marina Sena, Budah and Pabllo Vittar. '
          'Who else should I be listening to?</p></div>')
    scene(8, a('Oct 16 · the tweet', 0.05, cls="kick", style="left:80px;top:90px") +
          a(tw, 0.15, "scale", style="left:90px;right:90px;top:160px;--r:-1deg") +
          a(f'{cnt(D["tw_views"], 0.6)}<small>views</small>', 0.5, cls="kpi", style="left:80px;top:690px") +
          a(f'{cnt(D["tw_likes"], 1.0)}<small>likes</small>', 0.9, cls="kpi", style="left:80px;top:870px") +
          a(f'{cnt(D["tw_rts"], 1.3)}<small>reposts</small>', 1.2, cls="kpi", style="left:600px;top:870px") +
          a(f'The next day, {cnt(D["tw2_views"], 2.3)} more views:<br>“I waited so long for this moment, Brasil.”', 2.2,
            cls="body sm", style="left:80px;top:1110px"))

    # 3 · as páginas de notícias do X
    stories = [("Normani Arrives in São Paulo for First Solo Brazil Show", D["story1"]),
               ("Normani Rocks São Paulo Concert and Fashion Week Runway", D["story2"]),
               ("Brazilian Fans Share Heartfelt Meet-and-Greets with Normani", D["story3"]),
               ("Normani Thanks Fans for Memorable São Paulo Return", D["story4"])]
    st = "".join(a(f'<small>Trending now · Entertainment</small><h4>{t}</h4><b>{cnt(n, 0.8 + i * 0.35 + 0.2)} posts</b>',
                   0.8 + i * 0.35, "left", cls="story", style=f"top:{390 + i * 165}px") for i, (t, n) in enumerate(stories))
    scene(8, a('On X', 0.05, cls="kick", style="left:80px;top:90px") +
          rv('X created news pages', 0.1, "ttl2", "left:80px;top:140px") +
          rv('about her time <i>in Brazil.</i>', 0.25, "ttl2", "left:80px;top:225px") + st +
          a(f'{cnt(sum(n for _, n in stories), 2.5)}<small>posts across the four pages</small>', 2.3, cls="kpi s2", style="left:80px;top:1070px"), key="x")

    # 4 · ensaio (palco desenhado)
    stage = ("M140 700 L940 700 M200 700 L260 560 L820 560 L880 700 M260 560 L260 330 M820 560 L820 330 "
             "M240 330 L840 330 M340 330 L300 560 M440 330 L420 560 M540 330 L540 560 M640 330 L660 560 M740 330 L780 560")
    scene(4, a('Oct 17', 0.05, cls="kick", style="left:80px;top:90px") + draw(stage, 0.1, 1.2) +
          rv('Rehearsal', 0.3, "ttl", "left:70px;top:800px") + rv('at Pacaembu.', 0.45, "ttl it", "left:70px;top:930px") +
          a('Getting ready for her first solo show in Brazil.', 0.7, cls="body", style="left:70px;top:1130px"))

    # 5 · a noite em quatro paradas (mapa vetorial)
    px, py = PIN["pacaembu"]; ix, iy = PIN["ibirapuera"]; nx, ny = PIN["notie"]
    roads = ""
    for name, pts in ROADS:
        xy = [P(*q) for q in pts]
        roads += f'<path class="road" d="M{" L".join(f"{x} {y}" for x, y in xy)}"/>'
        mx, my = xy[len(xy) // 2 - (1 if len(xy) % 2 == 0 else 0)]
        ang = math.degrees(math.atan2(xy[-1][1] - xy[0][1], xy[-1][0] - xy[0][0]))
        ang = ang - 180 if ang > 90 else ang + 180 if ang < -90 else ang
        roads += f'<text class="rl" transform="translate({mx} {my}) rotate({ang:.1f})" dy="-14">{name}</text>'
    park = "M" + " L".join(f"{x} {y}" for x, y in PARK) + " Z"
    segs = [(f"M{px} {py} Q {px - 170} {(py + iy) / 2} {ix} {iy}", b(6), b(2)),
            (f"M{ix} {iy} Q {ix + 230} {(py + iy) / 2} {px + 12} {py + 14}", b(11), b(2)),
            (f"M{px} {py} Q {(px + nx) / 2} {py - 160} {nx} {ny}", b(15), b(2))]
    route = "".join(f'<path class="draw route" data-d="{d:.3f}" data-dur="{du:.3f}" d="{p}"/>' for p, d, du in segs)
    svg = (f'<svg viewBox="0 0 1792 2048"><path class="park" d="{park}"/><text class="pl" x="{PARK[0][0] - 60}" y="{PARK[3][1] + 50}">Ibirapuera Park</text>'
           f'{roads}<text class="pl" x="{P(-23.5440, -46.6330)[0]}" y="{P(-23.5440, -46.6330)[1]}">DOWNTOWN</text>{route}</svg>')
    pins = "".join(
        f'<div class="pin" data-d="{d:.3f}" style="left:{x}px;top:{y}px"><i></i><span>{t}</span></div>'
        for (x, y), t, d in [(PIN["pacaembu"], "Pacaembu", b(1.5)), (PIN["ibirapuera"], "Dendezeiro · SPFW", b(7.5)),
                             (PIN["notie"], "Terraço Notiê", b(16.5))])
    cam = [(0, px, py + 80, 1.15), (b(5.5), px, py + 80, 1.25), (b(7), (px + ix) / 2, (py + iy) / 2, 0.62), (b(8.2), ix, iy + 60, 1.2),
           (b(10.6), ix, iy + 60, 1.25), (b(12), (px + ix) / 2, (py + iy) / 2, 0.62), (b(13.2), px, py + 80, 1.2),
           (b(14.6), px, py + 80, 1.25), (b(16), (px + nx) / 2, py, 0.9), (b(17.2), nx, ny + 80, 1.2),
           (b(18.6), nx, ny + 80, 1.25), (b(20), (px + nx) / 2 + 40, (py + iy) / 2 + 60, 0.58)]
    stops = [(b(2), b(6), "6:45pm", "Show at Meli Music", "Pacaembu · her first solo show in Brazil, sold out", "mic"),
             (b(8), b(11), "9pm", "Dendezeiro runway at SPFW", "She opened the Dendezeiro show · São Paulo Fashion Week", "runway"),
             (b(13), b(15), "10pm", "Meet & greet with fans", "Back at Meli Music, Pacaembu", "heart"),
             (b(17), b(20), "1:30am", "After party", "Terraço Notiê · Downtown", "glass")]
    cards = "".join(
        f'<div class="stop m" data-a="{s:.3f}" data-b="{e:.3f}"><div class="si">{icon(ic)}<small>0{i + 1}/04</small></div>'
        f'<div class="st"><b>{h}</b><h4>{t}</h4><p>{sub}</p></div></div>' for i, (s, e, h, t, sub, ic) in enumerate(stops))
    scene(20, f'<div class="map" data-cam=\'{json.dumps([[round(t, 3), x, y, s] for t, x, y, s in cam])}\'>{svg}{pins}</div>'
              '<div class="mapfade"></div>' +
          a('Oct 17 · one night, four stops', 0.05, cls="kick", style="left:80px;top:80px") + cards, "mapsc", key="map")

    # 6 · TikTok (gráfico de busca)
    chart = "M0 230 L90 228 L180 226 L270 224 L360 222 L450 218 L540 205 L600 150 L660 60 L720 20"
    scene(4, a('On TikTok', 0.05, cls="kick", style="left:80px;top:90px") +
          a('<div class="sb">⌕&nbsp; normani choreography</div><small>Search popularity · last 7 days</small>'
            f'<b>{cnt(40_200, 0.5)}</b>', 0.1, "scale", cls="panel", style="left:80px;right:80px;top:170px;height:600px") +
          draw(chart, 0.4, 1.0, "chart", "0 0 720 240", "left:150px;top:470px;width:780px;height:260px") +
          rv('Trending', 0.3, "ttl", "left:70px;top:830px") + rv('for her choreography.', 0.45, "ttl it", "left:70px;top:960px") +
          a('After the Meli Music show, fans kept searching for her moves.', 0.7, cls="body", style="left:70px;top:1150px"))

    # 7 · imprensa
    hl = OUTLETS[:4]
    wall = "".join(a(o, 0.1 + i * 0.07, "up", cls="ol" + (" hl" if o in hl else ""), dur=0.3) for i, o in enumerate(OUTLETS))
    scene(8, a('In the press', 0.05, cls="kick", style="left:80px;top:90px") + f'<div class="wall">{wall}</div>' +
          a(f'{cnt(D["press_articles"], b(4) + 0.1)}<small>stories</small>', b(4), cls="kpi", style="left:80px;top:900px") +
          a(f'{cnt(D["press_outlets"], b(4.5) + 0.1)}<small>outlets</small>', b(4.5), cls="kpi", style="left:560px;top:900px"))

    # 8 · as peças da brasil.ir, desenhadas
    guide = ('<div class="mk-guide"><small>Team Normani</small><h5>São<br>Paulo</h5><p><i>a field guide</i> to eating, shopping<br>and going out in the city</p></div>')
    badges = "".join(f'<div class="mk-badge" style="background:{bg};color:{fg}"><i></i><b>AAA</b><small>NORMANI · BRAZIL 2026</small></div>'
                     for bg, fg in [(YEL, INK), (GRN, "#fff"), (INK, YEL)])
    lanyard = '<div class="mk-lan">' + ('<span class="scr">Normani</span><b>✶</b><span>BRAZIL 2026</span><b>✶</b><span>AAA</span><b>✶</b>' * 3) + '</div>'
    invite = ('<div class="mk-inv"><small>YOU’RE INVITED</small><h5><i>Normani</i><br>TAKES<br><em>SÃO PAULO</em></h5>'
              '<p>Oct 17, after the show · 1AM–5AM<br>Location revealed on the day</p></div>')
    items = [(guide, "São Paulo guide"), (f'<div class="mk-row">{badges}</div>', "AAA badges"), (lanyard, "Lanyard"), (invite, "After party invite")]
    slides = "".join(f'<div class="m mk" data-a="{b(2 * i):.3f}" data-b="{b(2 * i + 2):.3f}">{h}</div>' for i, (h, _) in enumerate(items))
    labels = "".join(f'<div class="m lbl" data-a="{b(2 * i):.3f}" data-b="{b(2 * i + 2):.3f}">{t}</div>' for i, (_, t) in enumerate(items))
    scene(8, a('Made by brasil.ir', 0.05, cls="kick", style="left:80px;top:90px") +
          rv('Every detail,', 0.1, "ttl2", "left:80px;top:140px") + rv('<i>designed for her.</i>', 0.25, "ttl2", "left:80px;top:225px") +
          f'<div class="stage">{slides}</div>{labels}')

    # 9 · fotos e vídeos
    frames = "".join(f'<div class="fr" data-d="{(i % 7) * 0.09 + (i // 7) * 0.05:.2f}"></div>' for i in range(35))
    scene(4, f'<div class="frames">{frames}</div><div class="veil"></div>' +
          a(icon("cam", "ic mid"), 0.0, "scale", style="left:490px;top:250px") +
          a(f'{cnt(1500, 0.1, "+")}<small>photos</small>', 0.05, "scale", cls="mega", style="top:330px") +
          a(icon("film", "ic mid"), b(2) - 0.1, "scale", style="left:490px;top:700px") +
          a('6h+<small>of video</small>', b(2), "scale", cls="mega", style="top:780px"), "full")

    # 9b · como a conversa cresceu (curtidas a cada 6 h nos posts da varredura)
    vals, labels = conv_series()
    PW, PH, top, bot = 920, 560, 70, 470
    mx = max(vals)
    pts = [(i / (len(vals) - 1) * PW, bot - (v / mx) * (bot - top)) for i, v in enumerate(vals)]
    path = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(
        f" C{p0[0] + (p1[0] - pm[0]) / 6:.1f} {p0[1] + (p1[1] - pm[1]) / 6:.1f} {p1[0] - (p2[0] - p0[0]) / 6:.1f} {p1[1] - (p2[1] - p0[1]) / 6:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        for pm, p0, p1, p2 in zip([pts[0]] + pts[:-2], pts[:-1], pts[1:], pts[2:] + [pts[-1]]))
    area = path + f" L{PW} {bot} L0 {bot} Z"
    WD, WT = 0.6, b(7)                       # a linha é revelada da esquerda para a direita
    ia = max(range(len(vals)), key=lambda i: vals[i])
    APEX["rel"] = WD + WT * pts[ia][0] / PW
    days = "".join(f'<text class="cx" x="{i / (len(vals) - 1) * PW:.0f}" y="{bot + 44}">{lab}</text>' for i, lab in labels)
    notes = ""
    for i, txt in PEAKS:
        x, y = pts[i]
        d = WD + WT * x / PW
        big = i == ia
        notes += (f'<g class="pk" data-d="{d:.3f}"><line x1="{x:.0f}" y1="{y - 14:.0f}" x2="{x:.0f}" y2="{(y - 70 if not big else 40):.0f}"/>'
                  f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{16 if big else 10}"/>'
                  f'<text x="{x:.0f}" y="{(y - 82 if not big else 26):.0f}" class="{"pkb" if big else ""}">{txt}</text></g>')
    chart = (f'<svg class="conv" viewBox="0 0 {PW} {PH}" style="left:80px;top:360px;width:{PW}px;height:{PH}px">'
             f'<defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YEL}" stop-opacity=".55"/>'
             f'<stop offset="1" stop-color="{GRN}" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="cw"><rect class="wipe" data-d="{WD:.3f}" data-dur="{WT:.3f}" x="-20" y="-200" width="0" height="900"/></clipPath></defs>'
             f'<line class="base" x1="0" y1="{bot}" x2="{PW}" y2="{bot}"/>{days}'
             f'<g clip-path="url(#cw)"><path d="{area}" fill="url(#cg)"/><path class="cl" d="{path}"/></g>{notes}</svg>')
    scene(14, a('The conversation', 0.05, cls="kick", style="left:80px;top:90px") +
          rv('How Brazil talked', 0.1, "ttl2", "left:80px;top:140px") + rv('<i>about her.</i>', 0.25, "ttl2", "left:80px;top:225px") +
          chart + a('<i></i>', APEX["rel"], "scale", cls="burst", style=f"left:{80 + pts[ia][0]:.0f}px;top:{360 + pts[ia][1]:.0f}px", dur=0.6) +
          a('Engagement on posts about Normani, every 6 hours · Oct 14–26', 0.4, cls="cap", style="left:80px;top:1010px") +
          a(f'<b>Peak:</b> Oct 17, the night of the show and the Dendezeiro runway', APEX["rel"] + 0.1, cls="body sm",
            style="left:80px;top:1090px;right:80px"), key="conv")

    # 10 · números
    scene(8, a('Her visit in numbers', 0.05, cls="kick", style="left:80px;top:90px") +
          a(f'{cnt(D["tweets"], 0.3, "+")}<small>tweets about her time in Brazil</small>', 0.2, cls="num", style="top:200px") +
          a(f'{cnt(D["views"], b(2.5) + 0.1)}<small>views on X, Instagram and TikTok</small>', b(2.5), cls="num", style="top:560px") +
          a(f'{cnt(D["likes"], b(5) + 0.1)}<small>likes</small>', b(5), cls="num", style="top:920px"), key="numbers")

    # 11 · o agradecimento dela
    scene(8, a('Oct 25 · Normani', 0.05, cls="kick", style="left:80px;top:90px") +
          a(icon("heart", "ic heart"), 0.1, "scale", style="left:700px;top:150px") +
          rv('She <i>loved it.</i>', 0.3, "ttl", "left:70px;top:230px") +
          a('“BRASIL, thank you for making this monumental return to SÃO PAULO so memorable. YOU HAVE MY HEART.”', 0.7,
            cls="quote", style="left:80px;right:80px;top:520px") +
          a(f'{cnt(D["thanks_ig_likes"], 1.6)}<small>likes on Instagram</small>', 1.5, cls="kpi s2", style="left:80px;top:1020px") +
          a(f'{cnt(D["thanks_x_views"], 1.9)}<small>views on X</small>', 1.8, cls="kpi s2", style="left:580px;top:1020px"), key="thanks")

    # 12 · fim
    scene(8, star("left:800px;top:200px;width:160px", 30) + star("left:130px;top:1000px;width:110px", -40) +
          rv('Thank you,', 0.2, "hero2", "top:380px") + rv('<i>Brasil.</i>', 0.45, "hero2", "top:560px") +
          a(f'<img src="{(N.parent / "logo/brasil-ir-branco.png").as_uri()}">', 1.1, cls="logo"), "grad intro", key="outro")


CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url({(N / 'fontes/InstrumentSerif-italic.woff2').as_uri()})}}
@font-face{{font-family:'IS';font-style:normal;src:url({(N / 'fontes/InstrumentSerif-normal.woff2').as_uri()})}}
@font-face{{font-family:'Mr Dafoe';src:url({(N / 'fontes/MrDafoe.woff2').as_uri()})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{DEEP};font-family:Inter,sans-serif;color:#fff}}
.sc{{position:absolute;inset:0;display:none;overflow:hidden}}
.bgw{{position:absolute;inset:-80px;background:url({(N.parent / 'wallpapers/ipad-brasil.png').as_uri()}) center/cover}}
.sc.grad::after{{content:"";position:absolute;inset:0;background:rgba(6,24,18,.22);pointer-events:none}}
.a{{position:absolute;opacity:0;z-index:2}}
.rvw{{position:absolute;overflow:hidden;padding:0 10px 14px 0;z-index:2}}
.rv{{transform:translateY(110%)}}
.kick{{font-size:24px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{YEL};white-space:nowrap}}
.sub.c,.date.c{{left:0;right:0;text-align:center}}
.hero{{left:0;right:0;text-align:center;font-family:'IS';font-style:italic;font-size:280px;line-height:1;letter-spacing:-.02em}}
.sub{{font-family:'IS';font-size:110px;line-height:1}} .sub i{{color:{YEL}}}
.date{{font-size:26px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;opacity:.95}}
.bar{{position:absolute;height:6px;background:{YEL};transform-origin:left;transform:scaleX(0);border-radius:3px;z-index:2}}
.star{{position:absolute;opacity:0;z-index:1}} .star svg{{width:100%;fill:{YEL}}}
.ttl{{font-family:'IS';font-size:124px;line-height:1;letter-spacing:-.02em;white-space:nowrap}}
.ttl.it,.ttl i{{font-style:italic;color:{YEL}}}
.ttl2{{font-family:'IS';font-size:84px;line-height:1;letter-spacing:-.01em;white-space:nowrap}} .ttl2 i{{color:{YEL}}}
.body{{font-size:32px;line-height:1.35;font-weight:500}} .body.sm{{font-size:27px}}
.dsvg{{position:absolute;overflow:visible;z-index:1}}
.draw{{fill:none;stroke-linecap:round;stroke-linejoin:round}}
.ln{{stroke:{YEL};stroke-width:5}}
.dash{{stroke:{YEL};stroke-width:5;opacity:.9}}
.chart{{stroke:{YEL};stroke-width:8}}
.mover{{position:absolute;left:0;top:0;z-index:3;opacity:0}}
.ic{{fill:none;stroke:{YEL};stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}}
.ic.big{{width:96px;height:96px;margin:-48px 0 0 -48px;display:block}}
.ic.mid{{width:100px;height:100px}}
.ic.heart{{width:240px;height:240px;fill:{YEL};stroke:none}}
.dot i{{position:absolute;left:-20px;top:-20px;width:40px;height:40px;border-radius:50%;background:{YEL};box-shadow:0 0 0 10px rgba(242,236,26,.25)}}
.dot span{{position:absolute;left:-60px;top:36px;width:120px;text-align:center;font-size:40px;font-weight:800}}
.tw{{background:#fff;color:{INK};border-radius:30px;padding:34px 38px;box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.who{{display:flex;align-items:center;gap:16px}}
.av{{width:72px;height:72px;border-radius:50%;object-fit:cover}}
.who b{{display:block;font-size:28px}} .who span{{font-size:22px;color:#536471}}
.tw p{{font-size:29px;line-height:1.4;margin-top:16px}} .tw p.hl{{font-size:36px;font-weight:700;margin-top:22px}}
.tw mark{{background:{YEL};padding:0 6px;border-radius:6px}}
.kpi .cnt{{display:block;white-space:nowrap;font-family:'IS';font-size:150px;line-height:1;color:{YEL}}}
.kpi small{{display:block;font-size:26px;font-weight:500;margin-top:4px}}
.kpi.s2 .cnt{{font-size:120px}}
.story{{left:80px;right:80px;background:rgba(6,14,10,.82);border:1px solid rgba(255,255,255,.14);border-radius:24px;padding:20px 30px}}
.story small{{font-size:18px;color:#9aa;font-weight:600}}
.story h4{{font-size:27px;font-weight:700;line-height:1.2;margin:4px 0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.story b{{font-size:24px;color:{YEL}}}
.mapsc{{background:{DEEP}}}
.map{{position:absolute;left:0;top:0;width:1792px;height:2048px;transform-origin:0 0;
  background:radial-gradient(circle,rgba(242,236,26,.16) 2px,transparent 2.5px) 0 0/48px 48px,linear-gradient(160deg,#0b2a1b,#06140e)}}
.map svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.road{{fill:none;stroke:rgba(233,245,160,.35);stroke-width:7;stroke-linecap:round;stroke-linejoin:round}}
.rl{{font:600 24px Inter;fill:rgba(233,245,160,.6);text-anchor:middle;letter-spacing:.06em}}
.park{{fill:rgba(19,176,75,.38);stroke:rgba(19,176,75,.9);stroke-width:3}}
.pl{{font:700 28px Inter;fill:rgba(233,245,160,.75);letter-spacing:.12em}}
.route{{stroke:{YEL};stroke-width:10;filter:drop-shadow(0 0 12px rgba(242,236,26,.7))}}
.pin{{position:absolute;opacity:0}}
.pin i{{position:absolute;left:-22px;top:-22px;width:44px;height:44px;border-radius:50%;background:{YEL};box-shadow:0 0 0 10px rgba(242,236,26,.25),0 0 40px rgba(242,236,26,.8)}}
.pin span{{position:absolute;left:36px;top:-24px;white-space:nowrap;font-size:34px;font-weight:800;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
.mapfade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,20,14,.9) 0%,rgba(6,20,14,0) 18%,rgba(6,20,14,0) 55%,rgba(6,20,14,.94) 78%)}}
.stop{{background:{PAPER};color:{INK};border-radius:26px;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.45);z-index:3}}
.stop.m{{inset:auto;left:60px;right:60px;top:985px;width:auto;height:300px}}
.stop .si{{position:absolute;left:0;top:0;bottom:0;width:220px;background:{GRN};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.stop .si .ic{{width:110px;height:110px;stroke:#fff}}
.stop .si small{{font-size:22px;font-weight:800;color:{YEL};letter-spacing:.12em}}
.stop .st{{position:absolute;left:260px;right:30px;top:32px}}
.stop b{{display:block;font-family:'IS';font-size:96px;line-height:.9;color:{GRN}}}
.stop h4{{font-size:38px;font-weight:800;margin-top:14px;line-height:1.1}}
.stop p{{font-size:24px;margin-top:8px;color:#333;line-height:1.3}}
.panel{{background:rgba(6,14,10,.82);border:1px solid rgba(255,255,255,.14);border-radius:30px;padding:40px 46px}}
.panel .sb{{font-size:34px;font-weight:700;background:#fff;color:{INK};border-radius:40px;padding:16px 28px}}
.panel small{{display:block;font-size:24px;color:#9aa;margin-top:30px;font-weight:600}}
.panel b .cnt{{font-family:'IS';font-weight:400;font-size:110px;color:{YEL};line-height:1.1}}
.wall{{position:absolute;left:70px;right:70px;top:160px;display:flex;flex-wrap:wrap;gap:6px 22px;z-index:2}}
.wall .a{{position:relative;font-family:'IS';font-size:58px;line-height:1.1;white-space:nowrap;opacity:0}}
.wall .hl{{color:{YEL};font-style:italic}}
.stage{{position:absolute;left:70px;right:70px;top:360px;height:820px;border-radius:30px;overflow:hidden;background:rgba(6,24,18,.45);box-shadow:0 26px 50px rgba(0,0,0,.35);z-index:1}}
.m{{position:absolute;inset:0;width:100%;height:100%;display:none}}
.mk{{display:flex;align-items:center;justify-content:center}}
.lbl{{top:1215px;height:auto;text-align:center;font-size:30px;font-weight:700;color:{YEL};letter-spacing:.1em;text-transform:uppercase;z-index:2}}
.mk-guide{{width:500px;height:640px;border-radius:16px;padding:44px;background:linear-gradient(160deg,{GRN},#0d5a35 55%,#e3b512);box-shadow:0 30px 60px rgba(0,0,0,.4);transform:rotate(-3deg)}}
.mk-guide small{{font-size:16px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:{YEL}}}
.mk-guide h5{{font-family:'IS';font-weight:400;font-size:150px;line-height:.9;margin-top:150px}}
.mk-guide p{{font-size:20px;margin-top:20px}} .mk-guide i{{font-family:'IS';color:{YEL};font-size:26px}}
.mk-row{{display:flex;gap:30px}}
.mk-badge{{width:240px;height:400px;border-radius:120px;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 26px 50px rgba(0,0,0,.4)}}
.mk-badge:nth-child(2){{transform:translateY(-30px) rotate(3deg)}} .mk-badge:nth-child(1){{transform:rotate(-4deg)}}
.mk-badge i{{position:absolute;top:28px;width:46px;height:14px;border-radius:7px;background:rgba(0,0,0,.25)}}
.mk-badge b{{font-size:84px;font-weight:900;letter-spacing:-.02em}}
.mk-badge small{{font-size:13px;font-weight:800;letter-spacing:.1em;margin-top:10px}}
.mk-lan{{width:1400px;height:110px;background:{INK};border-top:12px solid {GRN};border-bottom:12px solid {GRN};display:flex;align-items:center;gap:30px;
  padding-left:40px;white-space:nowrap;color:{YEL};transform:rotate(-8deg);box-shadow:0 26px 50px rgba(0,0,0,.4)}}
.mk-lan span{{font-size:34px;font-weight:700;letter-spacing:.18em}} .mk-lan .scr{{font-family:'Mr Dafoe';font-size:60px;letter-spacing:0;display:inline}}
.mk-lan b{{color:{GRN};font-size:30px}}
.mk-inv{{width:480px;height:600px;border-radius:16px;padding:44px;background:linear-gradient(170deg,#0d5a35,{DEEP});box-shadow:0 30px 60px rgba(0,0,0,.4);transform:rotate(3deg)}}
.mk-inv small{{font-size:16px;font-weight:800;letter-spacing:.2em;color:{YEL}}}
.mk-inv h5{{font-weight:900;font-size:70px;line-height:.95;margin-top:120px}} .mk-inv h5 i{{font-family:'IS';font-weight:400;font-size:96px}}
.mk-inv em{{font-style:normal;color:{YEL}}} .mk-inv p{{font-size:20px;margin-top:30px;line-height:1.4}}
.frames{{position:absolute;inset:-20px;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,1fr);gap:18px;padding:30px}}
.fr{{border:3px solid rgba(242,236,26,.0);border-radius:14px;background:rgba(242,236,26,.0)}}
.veil{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,rgba(6,24,18,.85),rgba(6,24,18,.35))}}
.sc.full{{background:url({(N.parent / 'wallpapers/ipad-brasil.png').as_uri()}) center/cover}}
.mega{{left:0;right:0;text-align:center}}
.mega,.mega .cnt{{font-family:'IS';font-size:220px;line-height:1;color:{YEL}}}
.mega small{{display:block;font-family:Inter;font-size:36px;font-weight:700;color:#fff;letter-spacing:.08em;text-transform:uppercase}}
.num{{left:80px;right:80px}}
.num .cnt{{display:block;font-family:'IS';font-size:190px;line-height:.95;color:{YEL};white-space:nowrap}}
.num small{{display:block;font-size:30px;font-weight:500;margin-top:6px}}
.quote{{font-family:'IS';font-style:italic;font-size:66px;line-height:1.1}}
.hero2{{left:0;right:0;text-align:center;font-family:'IS';font-size:200px;line-height:1}} .hero2 i{{color:{YEL}}}
.logo{{left:0;right:0;top:890px;text-align:center}} .logo img{{height:120px}}
.credit{{left:0;right:0;bottom:46px;text-align:center;font-size:17px;opacity:.75}}
.conv{{position:absolute;overflow:visible;z-index:2}}
.conv .cl{{fill:none;stroke:{YEL};stroke-width:6;stroke-linejoin:round;filter:drop-shadow(0 0 10px rgba(242,236,26,.6))}}
.conv .base{{stroke:rgba(255,255,255,.35);stroke-width:2}}
.conv .cx{{font:700 20px Inter;fill:rgba(255,255,255,.75);text-anchor:middle;letter-spacing:.08em}}
.conv .pk{{opacity:0}} .conv .pk line{{stroke:rgba(255,255,255,.6);stroke-width:2;stroke-dasharray:4 5}}
.conv .pk circle{{fill:{YEL};stroke:{DEEP};stroke-width:4}}
.conv .pk text{{font:800 24px Inter;fill:#fff;text-anchor:middle}} .conv .pk text.pkb{{font-size:30px;fill:{YEL}}}
.burst i{{position:absolute;left:-90px;top:-90px;width:180px;height:180px;border-radius:50%;border:5px solid {YEL};box-shadow:0 0 50px rgba(242,236,26,.8)}}
.cap{{font-size:22px;font-weight:600;opacity:.8}}
.body b{{color:{YEL}}}
.flash{{position:absolute;inset:0;background:{YEL};pointer-events:none;opacity:0;z-index:9}}
"""

JS = r"""
const E = p => 1 - Math.pow(1 - p, 3);
const EIO = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const C = v => Math.max(0, Math.min(1, v));
const fmt = (v, s) => Math.round(v).toLocaleString('en-US') + s;
const SC = [...document.querySelectorAll('.sc')];
for (const p of document.querySelectorAll('.draw')) { const L = p.getTotalLength(); p.dataset.len = L; p.style.strokeDasharray = L; }
const MP = [...document.querySelectorAll('.mover')].map(m => {
  const s = document.createElementNS('http://www.w3.org/2000/svg', 'path'); s.setAttribute('d', m.dataset.path);
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); g.appendChild(s); document.body.appendChild(g);
  g.style.position = 'absolute'; g.style.width = 0; g.style.height = 0; return [m, s];
});
function render(t) {
  let flash = 0;
  for (const s of SC) {
    const a = +s.dataset.a, b = +s.dataset.b, on = t >= a && t < b;
    s.style.display = on ? 'block' : 'none';
    if (!on) continue;
    const r = t - a;
    flash = Math.max(flash, C(1 - r / 0.1) * (a > 0 ? 0.35 : 0));
    const bg = s.querySelector('.bgw');
    if (bg) bg.style.transform = `translate(${Math.sin(t * .35) * 40}px,${Math.cos(t * .3) * 30}px) scale(${1.05 + .03 * Math.sin(t * .5)})`;
    for (const el of s.querySelectorAll('.a')) {
      const p = E(C((r - +el.dataset.d) / +el.dataset.dur));
      const rot = el.style.getPropertyValue('--r') || '0deg', fx = el.dataset.fx;
      el.style.opacity = p;
      el.style.transform = (fx === 'up' ? `translateY(${(1 - p) * 60}px)` : fx === 'left' ? `translateX(${(1 - p) * -140}px)`
        : `scale(${0.8 + 0.2 * p})`) + ` rotate(${rot})`;
    }
    for (const el of s.querySelectorAll('.rv')) el.style.transform = `translateY(${(1 - E(C((r - +el.dataset.d) / .5))) * 110}%)`;
    for (const el of s.querySelectorAll('.bar')) el.style.transform = `scaleX(${E(C((r - +el.dataset.d) / .5))})`;
    for (const el of s.querySelectorAll('.star')) {
      const p = E(C((r - +el.dataset.d) / .6));
      el.style.opacity = p; el.style.transform = `rotate(${r * +el.dataset.spin}deg) scale(${p})`;
    }
    for (const m of s.querySelectorAll('.m')) {
      const ma = +m.dataset.a, mb = +m.dataset.b, vis = r >= ma && r < mb;
      m.style.display = vis ? (m.classList.contains('mk') ? 'flex' : 'block') : 'none';
      if (!vis) continue;
      const p = E(C((r - ma) / .3));
      if (m.classList.contains('stop')) { m.style.transform = `translateY(${(1 - p) * 80}px)`; m.style.opacity = p; }
      else if (m.classList.contains('mk')) { m.style.transform = `scale(${0.85 + 0.15 * p + 0.03 * ((r - ma) / (mb - ma))})`; m.style.opacity = p; }
    }
    for (const c of s.querySelectorAll('.cnt')) c.textContent = fmt(+c.dataset.to * E(C((r - +c.dataset.d) / 1.0)), c.dataset.suf);
    for (const p of s.querySelectorAll('.draw')) p.style.strokeDashoffset = +p.dataset.len * (1 - EIO(C((r - +p.dataset.d) / +p.dataset.dur)));
    for (const p of s.querySelectorAll('.pin')) {
      const q = E(C((r - +p.dataset.d) / .4));
      p.style.opacity = q; p.style.transform = `scale(${0.5 + 0.5 * q})`;
    }
    for (const f of s.querySelectorAll('.fr')) {
      const q = C((r - +f.dataset.d) / .25), on2 = q > 0 ? 1 : 0;
      f.style.borderColor = `rgba(242,236,26,${0.85 * q})`; f.style.background = `rgba(242,236,26,${0.12 * q})`;
    }
    for (const [m, path] of MP) {
      if (!s.contains(m)) continue;
      const k = EIO(C((r - +m.dataset.d) / +m.dataset.dur)), L = path.getTotalLength();
      const p0 = path.getPointAtLength(k * L), p1 = path.getPointAtLength(Math.min(L, k * L + 1));
      const ang = Math.atan2(p1.y - p0.y, p1.x - p0.x) * 180 / Math.PI;
      m.style.opacity = r > +m.dataset.d ? 1 : 0;
      m.style.transform = `translate(${p0.x}px,${p0.y}px) rotate(${ang + 25}deg)`;
    }
    for (const w of s.querySelectorAll('.wipe')) w.setAttribute('width', 960 * C((r - +w.dataset.d) / +w.dataset.dur));
    for (const g of s.querySelectorAll('.pk')) g.style.opacity = E(C((r - +g.dataset.d) / .3));
    for (const bu of s.querySelectorAll('.burst')) { const q = C((r - +bu.dataset.d) / 0.8); bu.style.opacity = q > 0 && q < 1 ? 1 - q : 0; bu.style.transform = `scale(${0.3 + 1.4 * q})`; }
    const map = s.querySelector('.map');
    if (map) {
      const K = JSON.parse(map.dataset.cam);
      let i = 0; while (i < K.length - 2 && r > K[i + 1][0]) i++;
      const [t0, x0, y0, s0] = K[i], [t1, x1, y1, s1] = K[i + 1], k = EIO(C((r - t0) / (t1 - t0)));
      const x = x0 + (x1 - x0) * k, y = y0 + (y1 - y0) * k, z = s0 + (s1 - s0) * k;
      map.style.transform = `translate(${540 - x * z}px,${560 - y * z}px) scale(${z})`;
    }
  }
  document.querySelector('.flash').style.opacity = flash;
}
"""


def page():
    build()
    html, t = "", 0.0
    for beats, body, cls, key in SCENES:
        d = b(beats)
        if key: START[key] = t
        bg = '<div class="bgw"></div>' if "grad" in cls else ""
        html += f'<section class="sc {cls}" data-a="{t:.4f}" data-b="{t + d:.4f}">{bg}{body}</section>'
        t += d
    inter = (N / "fontes/inter.css").read_text()
    HTML[:] = [html]
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Normani takes São Paulo</title>'
            f'<style>{inter}{CSS}</style></head><body>{html}<div class="flash"></div><script>{JS}</script></body></html>'), t


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    html, dur = page()
    if "--audio" in sys.argv:          # só refaz a trilha, reaproveitando o vídeo sem áudio
        mux(dur); print("ok: audio"); return
    f = OUT / "video.html"
    f.write_text(html)
    prev = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]] if "--preview" in sys.argv else None
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux*/chrome'))[-1]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"])
        pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        if prev:
            for s in prev:
                pg.evaluate("t => render(t)", s)
                pg.screenshot(path=str(OUT / f"prev_{s:05.2f}.png"))
            br.close(); print("preview:", OUT); return
        nfr = int(round(dur * FPS))
        silent = B / "Normani-SP-Highlights-sem-trilha.mp4"
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
        for i in range(nfr):
            pg.evaluate("t => render(t)", i / FPS)
            enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % 300 == 0: print(f"{i}/{nfr}", flush=True)
        enc.stdin.close(); enc.wait(); br.close()
    mux(dur)


def counter_ticks(html):
    """instantes dos "tiques" dos contadores: um tique a cada 1/14 do caminho do número (rápido no começo, desacelerando)"""
    import re
    ticks = []
    for sec in re.finditer(r'<section class="sc[^"]*" data-a="([\d.]+)" data-b="([\d.]+)">(.*?)</section>', html, re.S):
        a0 = float(sec.group(1))
        for d in re.findall(r'class="cnt" data-to="\d+" data-d="([\d.]+)"', sec.group(3)):
            for k in range(1, 15):
                p = k / 14
                ticks.append(a0 + float(d) + (1 - (1 - p) ** (1 / 3)) * 1.0)     # inverso de E(p) = 1-(1-p)^3
    ticks.sort()
    out = []
    for t in ticks:
        if not out or t - out[-1] > 0.05: out.append(t)
    return out


def mux(dur):
    """trilha editada sobre o vídeo sem áudio, uma versão por faixa"""
    silent = B / "Normani-SP-Highlights-sem-trilha.mp4"
    ticks = counter_ticks(page()[0] if not SCENES else HTML[0])
    for name, (src, bpm, start) in TRACKS.items():
        wav = OUT / f"trilha-{name}.wav"
        trilha.make(wav, dur, src, bpm, start, drop=b(8), breakdown=START["thanks"], outro=START["outro"],
                    dings=[START["conv"] + APEX["rel"]], hits=[START["x"], START["map"], START["numbers"]], ticks=ticks)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(wav),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        "-movflags", "+faststart", str(B / "Normani-SP-Highlights.mp4")], check=True)
    print(f"ok: {dur:.1f}s")


if __name__ == "__main__":
    main()
