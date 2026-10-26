#!/usr/bin/env python3
"""Vídeo gráfico da passagem da Normani por São Paulo (feed do Instagram, 1080x1350, 30 fps).

Motion graphics na identidade do projeto: degradê verde e amarelo, Instrument Serif + Inter, fotos como peças,
contadores e um mapa com o trajeto da noite do show. Cada quadro é uma página HTML posicionada no tempo t
(render(t) no JS) e fotografada pelo Chromium; as cenas trocam no tempo da trilha (122 BPM). Gera:
  Normani-SP-Highlights.mp4            com trilha
  Normani-SP-Highlights-sem-trilha.mp4 sem áudio, para usar um som do próprio Instagram

Uso: python3 build_video.py [--preview 12.5 30 ...]   (--preview só salva PNGs desses segundos)
"""
import glob, json, os, pathlib, subprocess, sys

B = pathlib.Path(__file__).resolve().parent
N = B.parent
M = B / "media"
OUT = pathlib.Path(os.environ.get("VIDEO_CACHE", "/tmp/normani-video-cache"))
FPS, W, H = 30, 1080, 1350
BEAT = 60 / 122
MUSIC, MUSIC_START = M / "trilha-voxel-revolution.mp3", 9.86   # o drop da trilha cai no fim da abertura
GRN, YEL, INK, PAPER = "#13B04B", "#F2EC1A", "#0B0B0C", "#F4EEDC"

# números absolutos, todos verificados nas páginas (dados-varredura/); são piso
D = dict(
    tw_views=1_041_976, tw_likes=84_598, tw_rts=6_063, tw2_views=168_668,
    story1=12_228, story2=12_369,
    press_articles=49, press_outlets=35,
    tweets=15_000, views=6_213_660, likes=480_243, posts=199,
    thanks_ig_likes=127_547, thanks_x_views=147_485,
)
if (N / "dados-varredura/video_numeros.json").exists():
    D.update(json.loads((N / "dados-varredura/video_numeros.json").read_text()))

OUTLETS = ["Vogue Brasil", "Harper’s Bazaar", "Hugo Gloss", "Steal the Look", "CNN Brasil", "Gshow", "Billboard Brasil",
           "ELLE Brasil", "Glamour", "Veja São Paulo", "Terra", "Capricho", "GQ Brasil", "POPline", "Estrelando", "TodaTeen",
           "Tracklist", "Choquei", "Revista Raça", "Mundo Negro", "OFuxico", "Caderno Pop", "A Gazeta", "iG Gente"]

# mapa (OpenStreetMap, z15, recolorido) e posições dos lugares em pixels do mapa
PIN = dict(pacaembu=(620, 600), ibirapuera=(848, 1622), notie=(1267, 554))


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


def card(name, d, style, pos="50% 30%", fx="scale"):
    return a(f'<div class="ph" style="background-image:url({img(name)});background-position:{pos}"></div>', d, fx,
             cls="card", style=style)


def bar(d, style):
    return f'<div class="bar" data-d="{d:.3f}" style="{style}"></div>'


STAR = '<svg viewBox="0 0 100 100"><path d="M50 0 L56 44 L100 50 L56 56 L50 100 L44 56 L0 50 L44 44 Z"/></svg>'


def star(style, spin=40, d=0.0):
    return f'<div class="star" data-spin="{spin}" data-d="{d}" style="{style}">{STAR}</div>'


SCENES = []


def scene(beats, html, cls="grad"):
    SCENES.append((beats, html, cls))


def build():
    # 0 · abertura
    scene(8, star("left:760px;top:120px;width:200px", 30, 0.3) + star("left:110px;top:1030px;width:120px", -50, 0.6) +
          a('brasil.ir apresenta', 0.1, cls="kick c", style="top:400px") +
          rv('Normani', 0.5, "hero", "top:450px") +
          rv('em <i>São Paulo</i>', 1.1, "sub c", "top:730px") +
          bar(1.6, "left:390px;top:860px;width:300px") +
          a('15 — 18 de outubro de 2026', 1.8, cls="date c", style="top:885px"), "grad intro")

    # 1 · chegada
    scene(6, card("aero1.jpg", 0.0, "left:500px;top:80px;width:440px;height:560px;--r:4deg", "50% 25%") +
          card("aero2.jpg", 0.35, "left:250px;top:400px;width:380px;height:440px;--r:-5deg", "50% 30%") +
          a('15.10', 0.1, "left", cls="outline", style="left:70px;top:150px") +
          rv('Chegou', 0.3, "ttl", "left:70px;top:880px") + rv('em São Paulo.', 0.5, "ttl it", "left:70px;top:1005px") +
          a('Fãs, flores e autógrafos no aeroporto de Guarulhos.', 0.9, cls="body", style="left:70px;top:1170px"))

    # 2 · o tweet
    tw = ('<div class="tw"><div class="who"><img src="' + (N / "img/avatar.jpg").as_uri() + '"><div><b>Normani</b><span>@Normani · 16 out</span></div></div>'
          '<p><mark>Brasil, I’m not devastated. I’m MOTIVATED.</mark> Nem acredito que estou aqui depois de tanto tempo. '
          'Cheguei aqui ouvindo Duquesa, Marina Sena, Budah e Pabllo Vittar. Quem mais preciso ouvir?</p></div>')
    scene(8, a('16.10 · o tweet', 0.05, cls="kick", style="left:80px;top:90px") +
          a(tw, 0.15, "scale", style="left:90px;right:90px;top:170px;--r:-1deg") +
          a(f'{cnt(D["tw_views"], 0.6)}<small>visualizações</small>', 0.5, cls="kpi", style="left:80px;top:700px") +
          a(f'{cnt(D["tw_likes"], 1.0)}<small>curtidas</small>', 0.9, cls="kpi", style="left:80px;top:880px") +
          a(f'{cnt(D["tw_rts"], 1.3)}<small>reposts</small>', 1.2, cls="kpi", style="left:600px;top:880px") +
          a(f'E no dia seguinte, mais {cnt(D["tw2_views"], 2.3)} visualizações:<br>“Eu esperei tanto por esse momento, Brasil.”', 2.2,
            cls="body sm", style="left:80px;top:1110px"))

    # 3 · a página de notícias do X
    def story(t, n, d, top):
        return a(f'<small>Em alta · Entretenimento</small><h4>{t}</h4><b>{cnt(n, d + 0.2)} posts</b>', d, "left",
                 cls="story", style=f"top:{top}px")
    scene(8, a('No X', 0.05, cls="kick", style="left:80px;top:90px") +
          rv('O X criou uma página', 0.1, "ttl2", "left:80px;top:140px") +
          rv('de notícias sobre a passagem', 0.25, "ttl2", "left:80px;top:225px") +
          rv('dela <i>pelo Brasil.</i>', 0.4, "ttl2", "left:80px;top:310px") +
          story("Normani Arrives in São Paulo for First Solo Brazil Show", D["story1"], 0.9, 460) +
          story("Normani Rocks São Paulo Concert and Fashion Week Runway", D["story2"], 1.4, 720) +
          a(f'{cnt(D["story1"] + D["story2"], 2.4)}<small>posts nas duas páginas</small>', 2.2, cls="kpi", style="left:80px;top:1010px"))

    # 4 · ensaio
    scene(4, card("st_ensaio.jpg", 0.0, "left:560px;top:80px;width:420px;height:720px;--r:3deg", "50% 40%") +
          a('17.10', 0.05, "left", cls="outline", style="left:70px;top:180px") +
          rv('Ensaio', 0.2, "ttl", "left:70px;top:880px") + rv('no Pacaembu.', 0.35, "ttl it", "left:70px;top:1005px") +
          a('Tudo pronto pro primeiro show solo dela no Brasil.', 0.6, cls="body", style="left:70px;top:1170px"))

    # 5 · a noite em quatro paradas (mapa)
    px, py = PIN["pacaembu"]; ix, iy = PIN["ibirapuera"]; nx, ny = PIN["notie"]
    segs = [(f"M{px} {py} Q {px - 170} {(py + iy) / 2} {ix} {iy}", b(6), b(2)),
            (f"M{ix} {iy} Q {ix + 230} {(py + iy) / 2} {px + 12} {py + 14}", b(11), b(2)),
            (f"M{px} {py} Q {(px + nx) / 2} {py - 160} {nx} {ny}", b(15), b(2))]
    svg = "".join(f'<path class="draw" data-d="{d:.3f}" data-dur="{du:.3f}" d="{p}"/>' for p, d, du in segs)
    pins = "".join(
        f'<div class="pin" data-d="{d:.3f}" style="left:{x}px;top:{y}px"><i></i><span>{t}</span></div>'
        for (x, y), t, d in [(PIN["pacaembu"], "Pacaembu", b(1.5)), (PIN["ibirapuera"], "Parque Ibirapuera", b(7.5)),
                             (PIN["notie"], "Terraço Notiê", b(16.5))])
    cam = [(0, px, py + 80, 1.15), (b(5.5), px, py + 80, 1.25), (b(7), (px + ix) / 2, (py + iy) / 2, 0.62), (b(8.2), ix, iy + 60, 1.2),
           (b(10.6), ix, iy + 60, 1.25), (b(12), (px + ix) / 2, (py + iy) / 2, 0.62), (b(13.2), px, py + 80, 1.2),
           (b(14.6), px, py + 80, 1.25), (b(16), (px + nx) / 2, py, 0.9), (b(17.2), nx, ny + 80, 1.2),
           (b(18.6), nx, ny + 80, 1.25), (b(20), (px + nx) / 2 + 40, (py + iy) / 2 + 60, 0.58)]
    stops = [(b(2), b(6), "18h45", "Show no Meli Music", "Pacaembu · primeiro show solo no Brasil, estádio esgotado", "foto_a.jpg"),
             (b(8), b(11), "21h", "Desfile da Dendezeiro", "SPFW · Parque Ibirapuera · ela abriu o desfile", "st_desfile.jpg"),
             (b(13), b(15), "22h", "Meet & greet com os fãs", "De volta ao Meli Music, no Pacaembu", "mg_foto1.jpg"),
             (b(17), b(20), "1h30", "After party", "Terraço Notiê · Centro", "st_after.jpg")]
    cards = "".join(
        f'<div class="stop m" data-a="{s:.3f}" data-b="{e:.3f}"><div class="ph" style="background-image:url({img(f)})"></div>'
        f'<div class="st"><b>{h}</b><h4>{t}</h4><p>{sub}</p></div></div>' for s, e, h, t, sub, f in stops)
    scene(20, f'<div class="map" data-cam=\'{json.dumps([[round(t, 3), x, y, s] for t, x, y, s in cam])}\'>'
              f'<img src="{img("mapa.png")}"><svg viewBox="0 0 1792 2048">{svg}</svg>{pins}</div>'
              '<div class="mapfade"></div>' +
          a('17.10 · uma noite, quatro paradas', 0.05, cls="kick", style="left:80px;top:80px") + cards +
          '<div class="osm">© OpenStreetMap</div>', "mapsc")

    # 6 · TikTok
    scene(4, card("tiktok.jpg", 0.1, "left:540px;top:110px;width:440px;height:600px;--r:3deg", "50% 0%") +
          a('No TikTok', 0.05, cls="kick", style="left:80px;top:130px") +
          rv('Em alta', 0.15, "ttl", "left:70px;top:860px") + rv('pela coreografia.', 0.3, "ttl it", "left:70px;top:985px") +
          a('“normani choreography” virou busca em alta<br>depois do show no Meli Music.', 0.6, cls="body", style="left:70px;top:1140px"))

    # 7 · imprensa
    hl = OUTLETS[:4]
    wall = "".join(a(o, 0.1 + i * 0.07, "up", cls="ol" + (" hl" if o in hl else ""), dur=0.3) for i, o in enumerate(OUTLETS))
    scene(8, a('Na imprensa', 0.05, cls="kick", style="left:80px;top:90px") +
          f'<div class="wall">{wall}</div>' +
          card("press_DennUPWRrAC.jpg", b(3), "left:60px;top:800px;width:230px;height:290px;--r:-4deg") +
          card("press_DenQqN0CxRC.jpg", b(3.3), "left:300px;top:820px;width:230px;height:290px;--r:3deg") +
          card("press_DendbMdKO4g.jpg", b(3.6), "left:540px;top:800px;width:230px;height:290px;--r:-2deg") +
          card("press_Dend_POhqCW.jpg", b(3.9), "left:780px;top:820px;width:230px;height:290px;--r:4deg") +
          a(f'{cnt(D["press_articles"], b(5) + 0.1)} matérias · {cnt(D["press_outlets"], b(5) + 0.2)} veículos', b(5), cls="big1"))

    # 8 · designs da brasil.ir
    ds = [("guia-01.jpg", "Guia de São Paulo"), ("guia-02.jpg", "Guia de São Paulo"), ("guia-09.jpg", "Guia de São Paulo"),
          ("crachas.jpg", "Crachás"), ("cordao.jpg", "Cordão"), ("convite.png", "Convite do after"),
          ("afterdeck-1.jpg", "Proposta do after"), ("guia-04.jpg", "Guia de São Paulo")]
    slides = "".join(f'<img class="m contain" data-a="{b(i):.3f}" data-b="{b(i + 1):.3f}" src="{img(f)}">' for i, (f, _) in enumerate(ds))
    labels = "".join(f'<div class="m lbl" data-a="{b(i):.3f}" data-b="{b(i + 1):.3f}">{t}</div>' for i, (_, t) in enumerate(ds))
    scene(8, a('Feito por brasil.ir', 0.05, cls="kick", style="left:80px;top:90px") +
          rv('Cada detalhe', 0.1, "ttl2", "left:80px;top:140px") + rv('<i>pensado pra ela.</i>', 0.25, "ttl2", "left:80px;top:225px") +
          f'<div class="stage">{slides}</div>{labels}')

    # 9 · fotos e vídeos
    fotos = ["foto_a.jpg", "foto_b.jpg", "foto_c.jpg", "foto_d.jpg", "foto_e.jpg", "foto_f.jpg", "foto_g.jpg", "mg_foto1.jpg", "st_crowd.jpg"]
    cells = "".join(f'<div class="g">' + "".join(
        f'<img class="m cover" data-a="{b(k):.3f}" data-b="{b(k + 1):.3f}" src="{img(fotos[(i + k * 4) % 9])}">' for k in range(4)) + "</div>"
        for i in range(9))
    scene(4, f'<div class="grid">{cells}</div><div class="veil"></div>' +
          a(f'{cnt(1500, 0.1, "+")}<small>fotos</small>', 0.05, "scale", cls="mega", style="top:330px") +
          a('6h+<small>de vídeo gravado</small>', b(2), "scale", cls="mega", style="top:720px"), "full")

    # 10 · números
    scene(8, a('A passagem em números', 0.05, cls="kick", style="left:80px;top:90px") +
          a(f'{cnt(D["tweets"], 0.3, "+")}<small>tweets sobre a passagem dela pelo Brasil</small>', 0.2, cls="num", style="top:200px") +
          a(f'{cnt(D["views"], b(2.5) + 0.1)}<small>visualizações no X, Instagram e TikTok</small>', b(2.5), cls="num", style="top:560px") +
          a(f'{cnt(D["likes"], b(5) + 0.1)}<small>curtidas</small>', b(5), cls="num", style="top:920px"))

    # 11 · o agradecimento dela
    scene(8, a('25.10 · Normani', 0.05, cls="kick", style="left:80px;top:90px") +
          card("thanks_ig.jpg", 0.1, "left:600px;top:150px;width:400px;height:500px;--r:3deg", "50% 20%") +
          card("st_show.jpg", 0.35, "left:470px;top:420px;width:330px;height:420px;--r:-4deg", "50% 30%") +
          a('“BRASIL, thank you for making this monumental return to SÃO PAULO so memorable. YOU HAVE MY HEART.”', 0.7,
            cls="quote", style="left:80px;right:80px;top:880px") +
          a(f'{cnt(D["thanks_ig_likes"], 1.6)}<small>curtidas no Instagram</small>', 1.5, cls="kpi s", style="left:80px;top:1130px") +
          a(f'{cnt(D["thanks_x_views"], 1.9)}<small>visualizações no X</small>', 1.8, cls="kpi s", style="left:580px;top:1130px") +
          rv('Ela <i>amou.</i>', 0.3, "ttl", "left:70px;top:300px"))

    # 12 · fim
    scene(8, star("left:800px;top:200px;width:160px", 30) + star("left:130px;top:1000px;width:110px", -40) +
          rv('Obrigado,', 0.2, "hero2", "top:380px") + rv('<i>Brasil.</i>', 0.45, "hero2", "top:560px") +
          a(f'<img src="{(N.parent / "logo/brasil-ir-branco.png").as_uri()}">', 1.1, cls="logo") +
          a('Trilha: “Voxel Revolution”, Kevin MacLeod (incompetech.com) · CC BY 4.0', 1.4, cls="credit"), "grad intro")


CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url({(N / 'fontes/InstrumentSerif-italic.woff2').as_uri()})}}
@font-face{{font-family:'IS';font-style:normal;src:url({(N / 'fontes/InstrumentSerif-normal.woff2').as_uri()})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#06140e;font-family:Inter,sans-serif;color:#fff}}
.sc{{position:absolute;inset:0;display:none;overflow:hidden}}
.bgw{{position:absolute;inset:-80px;background:url({(N.parent / 'wallpapers/ipad-brasil.png').as_uri()}) center/cover}}
.sc.grad::after{{content:"";position:absolute;inset:0;background:rgba(6,24,18,.22);pointer-events:none}}
.a{{position:absolute;opacity:0;z-index:2}}
.rvw{{position:absolute;overflow:hidden;padding:0 10px 14px 0;z-index:2}}
.rv{{transform:translateY(110%)}}
.kick{{font-size:24px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{YEL};white-space:nowrap}}
.kick.c,.sub.c,.date.c{{left:0;right:0;text-align:center}}
.hero{{left:0;right:0;text-align:center;font-family:'IS';font-style:italic;font-size:260px;line-height:1;letter-spacing:-.02em}}
.sub{{font-family:'IS';font-size:100px;line-height:1}} .sub i{{color:{YEL}}}
.date{{font-size:24px;font-weight:600;letter-spacing:.12em;opacity:.92}}
.bar{{position:absolute;height:6px;background:{YEL};transform-origin:left;transform:scaleX(0);border-radius:3px;z-index:2}}
.star{{position:absolute;opacity:0;z-index:1}} .star svg{{width:100%;fill:{YEL}}}
.outline{{font-family:'IS';font-size:200px;line-height:1;color:transparent;-webkit-text-stroke:2px {YEL}}}
.ttl{{font-family:'IS';font-size:124px;line-height:1;letter-spacing:-.02em;white-space:nowrap}}
.ttl.it,.ttl i{{font-style:italic;color:{YEL}}}
.ttl2{{font-family:'IS';font-size:84px;line-height:1;letter-spacing:-.01em;white-space:nowrap}} .ttl2 i{{color:{YEL}}}
.body{{font-size:32px;line-height:1.35;font-weight:500}} .body.sm{{font-size:27px}}
.card{{border-radius:22px;overflow:hidden;background:#fff;padding:12px;box-shadow:0 30px 60px rgba(0,0,0,.4);z-index:1}}
.card .ph{{width:100%;height:100%;border-radius:12px;background-size:cover}}
.tw{{background:#fff;color:{INK};border-radius:30px;padding:34px 38px;box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.who{{display:flex;align-items:center;gap:16px}}
.who img{{width:72px;height:72px;border-radius:50%;object-fit:cover}}
.who b{{display:block;font-size:28px}} .who span{{font-size:22px;color:#536471}}
.tw p{{font-size:31px;line-height:1.4;margin-top:20px}}
.tw mark{{background:{YEL};padding:0 6px;border-radius:6px}}
.kpi .cnt{{display:block;white-space:nowrap;font-family:'IS';font-size:150px;line-height:1;color:{YEL}}}
.kpi small{{display:block;font-size:26px;font-weight:500;margin-top:4px}}
.kpi.s .cnt{{font-size:96px}}
.story{{left:80px;right:80px;background:rgba(6,14,10,.82);border:1px solid rgba(255,255,255,.14);border-radius:26px;padding:28px 34px}}
.story small{{font-size:20px;color:#9aa;font-weight:600}}
.story h4{{font-size:38px;font-weight:700;line-height:1.2;margin:8px 0 10px}}
.story b{{font-size:26px;color:{YEL}}}
.mapsc{{background:#06140e}}
.map{{position:absolute;left:0;top:0;width:1792px;height:2048px;transform-origin:0 0}}
.map img{{position:absolute;inset:0;width:100%;height:100%;filter:brightness(.9) saturate(1.1)}}
.map svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.draw{{fill:none;stroke:{YEL};stroke-width:9;stroke-linecap:round;filter:drop-shadow(0 0 10px rgba(242,236,26,.7))}}
.pin{{position:absolute;opacity:0}}
.pin i{{position:absolute;left:-22px;top:-22px;width:44px;height:44px;border-radius:50%;background:{YEL};box-shadow:0 0 0 10px rgba(242,236,26,.25),0 0 40px rgba(242,236,26,.8)}}
.pin span{{position:absolute;left:36px;top:-24px;white-space:nowrap;font-size:34px;font-weight:800;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
.mapfade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,20,14,.85) 0%,rgba(6,20,14,0) 18%,rgba(6,20,14,0) 55%,rgba(6,20,14,.92) 78%)}}
.stop{{position:absolute;left:60px;right:60px;top:985px;height:300px;display:none;background:{PAPER};color:{INK};border-radius:26px;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.45);z-index:3}}
.stop .ph{{position:absolute;left:0;top:0;bottom:0;width:250px;background-size:cover;background-position:50% 25%}}
.stop .st{{position:absolute;left:290px;right:30px;top:30px}}
.stop b{{display:block;font-family:'IS';font-size:92px;line-height:.9;color:{GRN}}}
.stop h4{{font-size:38px;font-weight:800;margin-top:14px;line-height:1.1}}
.stop p{{font-size:23px;margin-top:8px;color:#333;line-height:1.3}}
.stop.m{{inset:auto;left:60px;right:60px;top:985px;width:auto;height:300px}}
.osm{{position:absolute;right:16px;bottom:8px;font-size:13px;opacity:.6}}
.wall{{position:absolute;left:70px;right:70px;top:160px;display:flex;flex-wrap:wrap;gap:6px 22px;z-index:2}}
.wall .a{{position:relative;font-family:'IS';font-size:54px;line-height:1.1;white-space:nowrap;opacity:0}}
.wall .hl{{color:{YEL};font-style:italic}}
.big1{{left:0;right:0;top:1170px;text-align:center;font-size:40px;font-weight:700}}
.big1 .cnt{{font-family:'IS';font-weight:400;font-size:110px;color:{YEL};vertical-align:-12px}}
.stage{{position:absolute;left:70px;right:70px;top:360px;height:820px;border-radius:30px;overflow:hidden;background:rgba(6,24,18,.45);box-shadow:0 26px 50px rgba(0,0,0,.35);z-index:1}}
.m{{position:absolute;inset:0;width:100%;height:100%;display:none}}
.cover{{object-fit:cover}} .contain{{object-fit:contain;padding:30px}}
.lbl{{top:1215px;height:auto;text-align:center;font-size:30px;font-weight:700;color:{YEL};letter-spacing:.1em;text-transform:uppercase;z-index:2}}
.grid{{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:8px;background:{YEL}}}
.g{{position:relative;overflow:hidden}}
.veil{{position:absolute;inset:0;background:rgba(6,24,18,.62)}}
.mega{{left:0;right:0;text-align:center}}
.mega,.mega .cnt{{font-family:'IS';font-size:230px;line-height:1;color:{YEL}}}
.mega small{{display:block;font-family:Inter;font-size:36px;font-weight:700;color:#fff;letter-spacing:.06em;text-transform:uppercase}}
.num{{left:80px;right:80px}}
.num .cnt{{display:block;font-family:'IS';font-size:190px;line-height:.95;color:{YEL};white-space:nowrap}}
.num small{{display:block;font-size:30px;font-weight:500;margin-top:6px}}
.quote{{font-family:'IS';font-style:italic;font-size:54px;line-height:1.12}}
.hero2{{left:0;right:0;text-align:center;font-family:'IS';font-size:200px;line-height:1}} .hero2 i{{color:{YEL}}}
.logo{{left:0;right:0;top:890px;text-align:center}} .logo img{{height:120px}}
.credit{{left:0;right:0;bottom:46px;text-align:center;font-size:17px;opacity:.75}}
.flash{{position:absolute;inset:0;background:{YEL};pointer-events:none;opacity:0;z-index:9}}
"""

JS = r"""
const E = p => 1 - Math.pow(1 - p, 3);
const EIO = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const C = v => Math.max(0, Math.min(1, v));
const fmt = (v, s) => Math.round(v).toLocaleString('pt-BR') + s;
const SC = [...document.querySelectorAll('.sc')];
for (const p of document.querySelectorAll('.draw')) { const L = p.getTotalLength(); p.dataset.len = L; p.style.strokeDasharray = L; }
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
        : `scale(${0.8 + 0.2 * p})`) + ` rotate(${rot})` + (fx === 'scale' ? ` translateY(${Math.sin(t * 1.3 + +el.dataset.d * 7) * 6}px)` : '');
    }
    for (const el of s.querySelectorAll('.rv')) el.style.transform = `translateY(${(1 - E(C((r - +el.dataset.d) / .5))) * 110}%)`;
    for (const el of s.querySelectorAll('.bar')) el.style.transform = `scaleX(${E(C((r - +el.dataset.d) / .5))})`;
    for (const el of s.querySelectorAll('.star')) {
      const p = E(C((r - +el.dataset.d) / .6));
      el.style.opacity = p; el.style.transform = `rotate(${r * +el.dataset.spin}deg) scale(${p})`;
    }
    for (const m of s.querySelectorAll('.m')) {
      const ma = +m.dataset.a, mb = +m.dataset.b, vis = r >= ma && r < mb;
      m.style.display = vis ? 'block' : 'none';
      if (!vis) continue;
      const p = E(C((r - ma) / .3));
      if (m.classList.contains('stop')) { m.style.transform = `translateY(${(1 - p) * 80}px)`; m.style.opacity = p; }
      else if (!m.classList.contains('lbl')) m.style.transform = `scale(${1.06 - 0.05 * ((r - ma) / (mb - ma)) + (1 - p) * .06})`;
    }
    for (const c of s.querySelectorAll('.cnt')) c.textContent = fmt(+c.dataset.to * E(C((r - +c.dataset.d) / 1.0)), c.dataset.suf);
    for (const p of s.querySelectorAll('.draw')) p.style.strokeDashoffset = +p.dataset.len * (1 - EIO(C((r - +p.dataset.d) / +p.dataset.dur)));
    for (const p of s.querySelectorAll('.pin')) {
      const q = E(C((r - +p.dataset.d) / .4));
      p.style.opacity = q; p.style.transform = `scale(${0.5 + 0.5 * q})`;
    }
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
    for beats, body, cls in SCENES:
        d = b(beats)
        bg = '<div class="bgw"></div>' if "grad" in cls else ""
        html += f'<section class="sc {cls}" data-a="{t:.4f}" data-b="{t + d:.4f}">{bg}{body}</section>'
        t += d
    inter = (N / "fontes/inter.css").read_text()
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Normani SP highlights</title>'
            f'<style>{inter}{CSS}</style></head><body>{html}<div class="flash"></div><script>{JS}</script></body></html>'), t


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    html, dur = page()
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
                                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
        for i in range(nfr):
            pg.evaluate("t => render(t)", i / FPS)
            enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % 300 == 0: print(f"{i}/{nfr}", flush=True)
        enc.stdin.close(); enc.wait(); br.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-ss", str(MUSIC_START), "-t", f"{dur:.3f}", "-i", str(MUSIC),
                    "-filter_complex", f"[1:a]afade=t=out:st={dur - 2.5:.2f}:d=2.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", str(B / "Normani-SP-Highlights.mp4")], check=True)
    print(f"ok: {dur:.1f}s")


if __name__ == "__main__":
    main()
