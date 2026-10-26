#!/usr/bin/env python3
"""Vídeo de highlights da passagem da Normani por São Paulo (feed do Instagram, 1080x1350, 30 fps).

Cada quadro é uma página HTML posicionada no tempo t (função render(t) no JS) e fotografada pelo Chromium.
Os cortes caem no tempo da trilha (122 BPM). Gera:
  Normani-SP-Highlights.mp4            com trilha
  Normani-SP-Highlights-sem-trilha.mp4 sem áudio, para usar um som do próprio Instagram

Uso: python3 build_video.py [--preview 12.5 30 ...]   (--preview só salva PNGs desses segundos)
"""
import base64, glob, json, os, pathlib, shutil, subprocess, sys

B = pathlib.Path(__file__).resolve().parent
N = B.parent
M = B / "media"
CACHE = pathlib.Path(os.environ.get("VIDEO_CACHE", "/tmp/normani-video-cache"))
FPS, W, H = 30, 1080, 1350
BEAT = 60 / 122
MUSIC, MUSIC_START = M / "trilha-voxel-revolution.mp3", 9.86   # o drop da trilha cai no fim da abertura
F = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
GRN, YEL, INK, PAPER = "#13B04B", "#F2EC1A", "#0B0B0C", "#F4EEDC"

# números (dados-varredura/ e media/*.json; tudo verificado nas páginas, valores são piso)
D = dict(
    tw_views=1_041_976, tw_likes=84_598, tw_rts=6_063,
    tw2_views=168_668,
    story1=12_228, story2=12_369,
    hugo_show=748_095, hugo_after=538_484, hugo_aero=372_064, hugo_total=1_930_496,
    stl_total=216_526, vogue=109_827, dendezeiro_x=79_489,
    press_articles=49, press_outlets=35,
    tweets=15_000, views=6_200_000, likes=480_000,
    thanks_ig_likes=127_547, thanks_x_views=147_485,
)
if (N / "dados-varredura/video_numeros.json").exists():
    D.update(json.loads((N / "dados-varredura/video_numeros.json").read_text()))

OUTLETS = ["Vogue Brasil", "Harper’s Bazaar", "Hugo Gloss", "Steal the Look", "CNN Brasil", "Gshow", "Billboard Brasil",
           "ELLE Brasil", "Glamour", "Veja SP", "Terra", "Capricho", "GQ Brasil", "POPline", "Estrelando", "TodaTeen",
           "Tracklist", "Choquei", "Revista Raça", "Mundo Negro", "OFuxico", "Caderno Pop"]

CLIPS = {}   # nome -> nº de quadros extraídos


def prep_clips():
    for mp4 in sorted(M.glob("*.mp4")):
        d = CACHE / mp4.stem
        if not d.exists() or not any(d.iterdir()):
            d.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"fps={FPS},scale={W}:-2",
                            "-q:v", "3", str(d / "%04d.jpg")], check=True)
        CLIPS[mp4.stem] = len(list(d.glob("*.jpg")))


def img(name):
    return (M / name).as_uri()


# ---------- peças de HTML (tempos relativos ao início da cena, em segundos) ----------
def clip(name, a, b, cls="cover", style=""):
    return (f'<img class="m clip {cls}" data-a="{a:.3f}" data-b="{b:.3f}" data-dir="{(CACHE / name).as_uri()}" '
            f'data-n="{CLIPS[name]}" style="{style}">')


def pic(name, a, b, cls="cover", style=""):
    return f'<img class="m {cls}" data-a="{a:.3f}" data-b="{b:.3f}" src="{img(name)}" style="{style}">'


def cnt(v, fmt, d, cls=""):
    return f'<span class="cnt {cls}" data-to="{v}" data-fmt="{fmt}" data-d="{d}">0</span>'


def a(html, d, fx="up", cls="", style="", dur=0.4):
    return f'<div class="a {cls}" data-d="{d}" data-fx="{fx}" data-dur="{dur}" style="{style}">{html}</div>'


b = lambda n: n * BEAT        # batidas -> segundos

SCENES = []   # (duração em batidas, html, classe)


def scene(beats, html, cls=""):
    SCENES.append((beats, html, cls))


AV = F(N / "img/avatar.jpg")
VF = ('<svg class="vf" viewBox="0 0 24 24"><path fill="#1D9BF0" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91C2.63 9.33 1.75 10.57 1.75 12s.88 2.67 2.19 3.34c-.46 1.39-.2 2.9.81 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.46 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34z"/>'
      '<path fill="#fff" d="M10.1 16.3l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>')


def build_scenes():
    # 0 · abertura (o drop entra no corte seguinte)
    scene(8, a('brasil.ir apresenta', 0.1, cls="kick c") +
          a('Normani', 0.6, "scale", cls="hero", dur=0.6) +
          a('em <i>São Paulo</i>', 1.3, cls="sub c") +
          a('15 — 18 de outubro de 2026', 2.0, cls="date c"), "intro")

    # 1 · chegada
    scene(6, pic("aero1.jpg", 0, b(2)) + clip("aero", b(2), b(4)) + pic("aero2.jpg", b(4), b(6)) +
          '<div class="shade"></div>' +
          a('15.10 · Guarulhos', 0.05, cls="kick lo") + a('Chegou.', 0.2, cls="ttl lo") +
          a(f'{cnt(D["hugo_aero"], "mil", 0.6)}<small>views no vídeo do Hugo Gloss</small>', 0.5, cls="chip lo2"), "full")

    # 2 · o tweet
    tw = (f'<div class="tw"><div class="who"><img src="data:image/jpeg;base64,{AV}"><div><b>Normani {VF}</b><span>@Normani</span></div></div>'
          '<p><mark>Brasil, I’m not devastated. I’m MOTIVATED.</mark> Nem acredito que estou aqui depois de tanto tempo. '
          'Cheguei aqui ouvindo Duquesa, Marina Sena, Budah e Pabllo Vittar. Quem mais preciso ouvir?</p></div>')
    scene(8, a('16.10 · o tweet', 0.05, cls="kick top") + a(tw, 0.15, "scale", style="position:absolute;left:90px;right:90px;top:250px") +
          '<div class="kpis" style="top:760px">' +
          a(f'{cnt(D["tw_views"], "mi", 0.5)}<small>visualizações</small>', 0.4, cls="kpi") +
          a(f'{cnt(D["tw_likes"], "mil", 0.7)}<small>curtidas</small>', 0.6, cls="kpi") +
          a(f'{cnt(D["tw_rts"], "mil", 0.9)}<small>reposts</small>', 0.8, cls="kpi") + '</div>' +
          a(f'<p>“Eu esperei tanto por esse momento, Brasil.” <b>{cnt(D["tw2_views"], "mil", 2.4)} views</b> no segundo tweet</p>',
            2.2, cls="note", style="top:1010px"), "grad")

    # 3 · a página de notícias do X
    def story(t, n, d, top):
        return a(f'<small>Em alta · Entretenimento</small><h4>{t}</h4><b>{cnt(n, "mil", d + 0.2)} posts</b>', d, "left",
                 cls="story", style=f"top:{top}px")
    scene(8, a('No X', 0.05, cls="kick top") +
          a('O X criou uma página de notícias<br>sobre a passagem dela pelo Brasil', 0.15, cls="ttl2") +
          story("Normani Arrives in São Paulo for First Solo Brazil Show", D["story1"], 0.8, 430) +
          story("Normani Rocks São Paulo Concert and Fashion Week Runway", D["story2"], 1.4, 690) +
          a(f'{cnt(D["story1"] + D["story2"], "mil", 2.4)}<small>posts nas duas páginas</small>', 2.2, cls="chip c2"), "grad x")

    # 4 · ensaio
    scene(4, clip("ensaio", 0, b(4)) + '<div class="shade"></div>' +
          a('17.10 · Pacaembu', 0.05, cls="kick lo") + a('Ensaio.', 0.15, cls="ttl lo"), "full")

    # 5 · show
    cuts = ["show_a", "show_b", "show_c", "show_d", "show_crowd", "show_e"]
    scene(12, "".join(clip(c, b(2 * i), b(2 * i + 2)) for i, c in enumerate(cuts)) + '<div class="shade"></div>' +
          a('17.10 · Meli Music', 0.05, cls="kick lo", style="bottom:560px") + a('1º show solo<br>no Brasil', 0.2, cls="ttl lo", style="bottom:250px") +
          a('Pacaembu esgotado', b(4), cls="pill lo3") +
          a(f'{cnt(D["hugo_show"], "mil", b(8) + 0.2)}<small>views em “Motivation” no Hugo Gloss</small>', b(8), cls="chip lo2"), "full")

    # 6 · desfile Dendezeiro
    scene(8, clip("desfile_a", 0, b(4)) + clip("desfile_b", b(4), b(8)) + '<div class="shade"></div>' +
          a('17.10 · SPFW N61', 0.05, cls="kick lo", style="bottom:560px") + a('Do palco direto<br>pra passarela', 0.2, cls="ttl lo", style="bottom:250px") +
          a('abriu o desfile da Dendezeiro', 0.7, cls="pill lo3") +
          a(f'{cnt(D["dendezeiro_x"], "mil", b(4) + 0.2)}<small>views no vídeo da Dendezeiro no X</small>', b(4), cls="chip lo2"), "full")

    # 7 · meet & greet
    scene(6, a('Meet & greet', 0.05, cls="kick top") + a('Com os fãs.', 0.1, cls="ttl2") +
          a(clip("mg", 0, b(6)), 0.2, "scale", cls="card", style="left:70px;top:330px;width:520px;height:900px;--r:-2deg") +
          a(pic("mg_foto1.jpg", 0, b(6)), 0.6, "scale", cls="card", style="left:560px;top:310px;width:450px;height:340px;--r:3deg") +
          a(pic("mg_foto2.jpg", 0, b(6)), 1.0, "scale", cls="card", style="left:600px;top:640px;width:420px;height:300px;--r:-2deg") +
          a(pic("mg_call.jpg", 0, b(6), style="object-position:50% 20%"), 1.4, "scale", cls="card",
            style="left:620px;top:950px;width:380px;height:300px;--r:2deg"), "grad")

    # 8 · after party
    scene(6, clip("after", 0, b(6)) + '<div class="shade"></div>' +
          a('After party · Sharp', 0.05, cls="kick lo") + a('E depois, é onde?', 0.2, cls="ttl lo") +
          a(f'{cnt(D["hugo_after"], "mil", 0.9)}<small>views no “Bonde das Maravilhas” no Hugo Gloss</small>', 0.8, cls="chip lo2"), "full")

    # 9 · TikTok
    scene(4, a('No TikTok', 0.05, cls="kick top") + a('Em alta pela<br>coreografia', 0.1, cls="ttl2") +
          a(pic("tiktok.jpg", 0, b(4), "contain"), 0.3, "scale", cls="card shot", style="left:270px;top:430px;width:540px;height:800px;--r:-2deg"),
          "grad")

    # 10 · imprensa
    press = [("press_DenQqN0CxRC.jpg", "Hugo Gloss", f'{cnt(D["hugo_total"], "mi", 0.0)} views em 4 posts'),
             ("press_DendbMdKO4g.jpg", "Steal the Look", f'{cnt(D["stl_total"], "mil", 0.0)} views'),
             ("press_DennUPWRrAC.jpg", "Vogue Brasil", f'{cnt(D["vogue"], "mil", 0.0)} views'),
             ("press_Dend_POhqCW.jpg", "Harper’s Bazaar", "“Normani está entre nós!”")]
    tiles = ""
    for i, (f, o, s) in enumerate(press):
        d = 0.3 + i * b(1)
        tiles += a(f'<div class="ph" style="background-image:url({img(f)})"></div><div class="pt"><b>{o}</b><small>{s.replace("data-d=\"0.0\"", f"data-d=\"{d + 0.2:.2f}\"")}</small></div>',
                   d, "scale", cls="press", style=f"left:{70 + (i % 2) * 480}px;top:{250 + (i // 2) * 400}px")
    tick = "".join(f"<span>{o}</span><i>✶</i>" for o in OUTLETS * 2)
    scene(10, a('Na imprensa', 0.05, cls="kick top") + tiles +
          a(f'<b>{cnt(D["press_articles"], "int", b(5) + 0.2)}</b> matérias em <b>{cnt(D["press_outlets"], "int", b(5) + 0.3)}</b> veículos', b(5), cls="big1") +
          f'<div class="tick"><div class="tk" data-speed="160">{tick}</div></div>', "grad")

    # 11 · designs da brasil.ir
    ds = [("guia-01.jpg", "Guia de São Paulo"), ("guia-02.jpg", "Guia de São Paulo"), ("guia-09.jpg", "Guia de São Paulo"),
          ("crachas.jpg", "Crachás"), ("cordao.jpg", "Cordão"), ("convite.png", "Convite do after"),
          ("afterdeck-1.jpg", "Proposta do after"), ("guia-04.jpg", "Guia de São Paulo")]
    slides = "".join(pic(f, b(i), b(i + 1), "contain") for i, (f, _) in enumerate(ds))
    labels = "".join(f'<div class="m lbl" data-a="{b(i):.3f}" data-b="{b(i + 1):.3f}">{t}</div>' for i, (_, t) in enumerate(ds))
    scene(8, a('Feito por brasil.ir', 0.05, cls="kick top") + a('Cada detalhe<br>pensado pra ela', 0.1, cls="ttl2") +
          f'<div class="stage">{slides}</div>{labels}', "grad")

    # 12 · fotos e vídeos
    fotos = ["foto_a.jpg", "foto_b.jpg", "foto_c.jpg", "foto_d.jpg", "foto_e.jpg", "foto_f.jpg", "foto_g.jpg", "mg_foto1.jpg", "aero1.jpg"]
    cells = ""
    for i in range(9):
        cells += '<div class="g">' + "".join(pic(fotos[(i + k * 4) % 9], b(k), b(k + 1)) for k in range(4)) + "</div>"
    scene(4, f'<div class="grid">{cells}</div><div class="shade2"></div>' +
          a('1.500+ fotos', 0.05, "scale", cls="mega", style="top:470px") +
          a('6h+ de vídeo', b(2), "scale", cls="mega", style="top:690px"), "full")

    # 13 · números
    scene(8, a('A passagem em números', 0.05, cls="kick top") +
          a(f'{cnt(D["tweets"], "mil+", 0.3)}<small>tweets sobre a passagem dela</small>', 0.2, cls="num", style="top:300px") +
          a(f'{cnt(D["views"], "mi+", b(2.5) + 0.1)}<small>visualizações no X, Instagram e TikTok</small>', b(2.5), cls="num", style="top:620px") +
          a(f'{cnt(D["likes"], "mil+", b(5) + 0.1)}<small>curtidas</small>', b(5), cls="num", style="top:940px"), "grad")

    # 14 · o agradecimento dela (a trilha respira aqui)
    scene(8, a('25.10 · Normani', 0.05, cls="kick top") +
          a(pic("thanks_ig.jpg", 0, b(8)), 0.1, "scale", cls="card", style="left:80px;top:250px;width:440px;height:560px;--r:-2deg") +
          a(clip("thanks_v", 0, b(8)), 0.4, "scale", cls="card", style="left:560px;top:290px;width:440px;height:560px;--r:2deg") +
          a('“BRASIL, thank you for making this monumental return to SÃO PAULO so memorable. YOU HAVE MY HEART.”', 0.9, cls="quote") +
          '<div class="kpis" style="top:1130px">' +
          a(f'{cnt(D["thanks_ig_likes"], "mil", 1.8)}<small>curtidas no Instagram</small>', 1.6, cls="kpi") +
          a(f'{cnt(D["thanks_x_views"], "mil", 2.2)}<small>views no X</small>', 2.0, cls="kpi") + '</div>', "grad")

    # 15 · fim
    scene(8, a('Obrigado,<br><i>Brasil.</i>', 0.2, "scale", cls="hero2", dur=0.7) +
          a(f'<img src="{(N.parent / "logo/brasil-ir-branco.png").as_uri()}">', 1.0, cls="logo") +
          a('Trilha: “Voxel Revolution”, Kevin MacLeod (incompetech.com) · CC BY 4.0', 1.4, cls="credit"), "intro")


CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url({(N / 'fontes/InstrumentSerif-italic.woff2').as_uri()})}}
@font-face{{font-family:'IS';font-style:normal;src:url({(N / 'fontes/InstrumentSerif-normal.woff2').as_uri()})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:Inter,sans-serif;color:#fff}}
.sc{{position:absolute;inset:0;display:none;overflow:hidden}}
.sc.grad,.sc.intro{{background:url({(N.parent / 'wallpapers/ipad-brasil.png').as_uri()}) center/cover}}
.sc.grad::before{{content:"";position:absolute;inset:0;background:rgba(6,24,18,.28)}}
.sc.intro::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,rgba(0,0,0,0),rgba(6,24,18,.45))}}
.m{{position:absolute;inset:0;width:100%;height:100%;display:none}}
.cover{{object-fit:cover}} .contain{{object-fit:contain}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.25) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,0) 45%,rgba(6,24,18,.88) 100%)}}
.shade2{{position:absolute;inset:0;background:rgba(6,24,18,.55)}}
.a{{position:absolute;opacity:0}}
.kick{{font-size:24px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{YEL}}}
.kick.c{{left:0;right:0;top:420px;text-align:center}}
.kick.top{{left:80px;top:90px}}
.kick.lo{{left:80px;bottom:420px}}
.hero{{left:0;right:0;top:470px;text-align:center;font-family:'IS';font-style:italic;font-size:250px;line-height:1;letter-spacing:-.02em}}
.sub{{font-family:'IS';font-size:96px;line-height:1}} .sub i{{color:{YEL}}}
.sub.c{{left:0;right:0;top:740px;text-align:center}}
.date{{font-size:24px;font-weight:600;letter-spacing:.12em;opacity:.9}} .date.c{{left:0;right:0;top:880px;text-align:center}}
.ttl{{font-family:'IS';font-size:150px;line-height:.92;letter-spacing:-.02em}}
.ttl.lo{{left:76px;right:60px;bottom:250px}}
.ttl2{{left:80px;right:80px;top:135px;font-family:'IS';font-size:84px;line-height:.98;letter-spacing:-.01em}}
.x .ttl2{{font-size:72px}}
.chip{{display:flex;align-items:baseline;gap:16px;font-size:24px}}
.chip .cnt{{font-family:'IS';font-size:84px;line-height:1;color:{YEL}}}
.chip small{{font-size:24px;font-weight:500;max-width:520px;line-height:1.25}}
.chip.lo2{{left:80px;right:60px;bottom:90px}}
.chip.c2{{left:80px;right:80px;top:1060px}}
.pill{{font-size:26px;font-weight:700;background:{YEL};color:{INK};padding:10px 22px;border-radius:40px}}
.pill.lo3{{left:80px;bottom:190px}}
.tw{{background:#fff;color:{INK};border-radius:30px;padding:34px 38px;box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.who{{display:flex;align-items:center;gap:16px}}
.who img{{width:72px;height:72px;border-radius:50%;object-fit:cover}}
.who b{{display:flex;align-items:center;gap:6px;font-size:28px}} .who span{{font-size:22px;color:#536471}}
.vf{{width:26px;height:26px}}
.tw p{{font-size:31px;line-height:1.4;margin-top:20px}}
.tw mark{{background:{YEL};padding:0 6px;border-radius:6px}}
.kpis{{position:absolute;left:80px;right:80px;display:flex;gap:40px}}
.kpi{{position:relative;flex:1}}
.kpi .cnt{{display:block;white-space:nowrap;font-family:'IS';font-size:96px;line-height:1;color:{YEL}}}
.kpi small{{display:block;font-size:24px;font-weight:500;margin-top:6px}}
.note{{left:80px;right:80px}} .note p{{font-size:28px;line-height:1.4;opacity:.95}} .note b{{color:{YEL}}}
.story{{left:80px;right:80px;background:rgba(6,14,10,.82);border:1px solid rgba(255,255,255,.14);border-radius:26px;padding:28px 34px}}
.story small{{font-size:20px;color:#9aa;font-weight:600}}
.story h4{{font-size:38px;font-weight:700;line-height:1.2;margin:8px 0 10px}}
.story b{{font-size:24px;color:{YEL}}}
.card{{border-radius:30px;overflow:hidden;box-shadow:0 26px 50px rgba(0,0,0,.4);background:#111}}
.card.shot{{background:#fff}}
.press{{width:460px;height:380px;border-radius:26px;overflow:hidden;background:{PAPER};color:{INK};box-shadow:0 20px 40px rgba(0,0,0,.35)}}
.press .ph{{height:270px;background-size:cover;background-position:50% 30%}}
.press .pt{{padding:16px 22px}} .press b{{display:block;font-size:30px;font-weight:800}}
.press small{{display:block;font-size:22px;color:#333;margin-top:2px}} .press small .cnt{{font-weight:800;color:{GRN}}}
.big1{{left:70px;right:70px;top:1075px;font-size:36px;font-weight:600;text-align:center}}
.big1 b{{font-family:'IS';font-weight:400;font-size:96px;color:{YEL};vertical-align:-8px}}
.tick{{position:absolute;left:0;right:0;bottom:30px;height:60px;overflow:hidden;background:{YEL};color:{INK}}}
.tk{{position:absolute;white-space:nowrap;top:13px;font-size:28px;font-weight:800;text-transform:uppercase;letter-spacing:.04em}}
.tk span{{margin:0 22px}} .tk i{{font-style:normal;color:{GRN}}}
.stage{{position:absolute;left:70px;right:70px;top:390px;height:820px;border-radius:30px;overflow:hidden;background:rgba(6,24,18,.5);box-shadow:0 26px 50px rgba(0,0,0,.35)}}
.stage .m{{padding:28px}}
.lbl{{position:absolute;left:0;right:0;top:1240px;height:auto;width:auto;text-align:center;font-size:30px;font-weight:700;color:{YEL};letter-spacing:.08em;text-transform:uppercase}}
.grid{{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:6px}}
.g{{position:relative;overflow:hidden}}
.mega{{left:0;right:0;text-align:center;font-family:'IS';font-size:170px;line-height:1;color:{YEL};text-shadow:0 8px 30px rgba(0,0,0,.5)}}
.num{{left:80px;right:80px}}
.num .cnt{{display:block;font-family:'IS';font-size:220px;line-height:.9;color:{YEL}}}
.num small{{display:block;font-size:30px;font-weight:500;margin-top:8px}}
.quote{{left:80px;right:80px;top:880px;font-family:'IS';font-style:italic;font-size:54px;line-height:1.12}}
.hero2{{left:0;right:0;top:400px;text-align:center;font-family:'IS';font-size:190px;line-height:.92}} .hero2 i{{color:{YEL}}}
.logo{{left:0;right:0;top:860px;text-align:center}} .logo img{{height:120px}}
.credit{{left:0;right:0;bottom:46px;text-align:center;font-size:17px;opacity:.75}}
.flash{{position:absolute;inset:0;background:#fff;pointer-events:none;opacity:0;z-index:9}}
"""

JS = r"""
const E = p => 1 - Math.pow(1 - p, 3);
const C = v => Math.max(0, Math.min(1, v));
function fmt(v, f) {
  const br = (x, d) => x.toFixed(d).replace('.', ',').replace(/,0+$/, '');
  if (f.startsWith('mil')) return (v >= 1e5 ? Math.round(v / 1e3) : br(v / 1e3, 1)) + ' mil' + (f.endsWith('+') ? '+' : '');
  if (f.startsWith('mi')) return br(v / 1e6, v >= 1e7 ? 0 : (f === 'mi+' ? 1 : 2)) + ' mi' + (f.endsWith('+') ? '+' : '');
  return Math.round(v).toLocaleString('pt-BR');
}
const SC = [...document.querySelectorAll('.sc')];
function render(t) {
  const waits = [];
  let flash = 0;
  for (const s of SC) {
    const a = +s.dataset.a, b = +s.dataset.b;
    const on = t >= a && t < b;
    s.style.display = on ? 'block' : 'none';
    if (!on) continue;
    const r = t - a;
    flash = Math.max(flash, C(1 - r / 0.12) * (a > 0 ? 0.55 : 0));
    for (const el of s.querySelectorAll('.a')) {
      const p = E(C((r - +el.dataset.d) / +el.dataset.dur));
      el.style.opacity = p;
      const rot = el.style.getPropertyValue('--r') || '0deg';
      const fx = el.dataset.fx;
      el.style.transform = (fx === 'up' ? `translateY(${(1 - p) * 60}px)` : fx === 'left' ? `translateX(${(1 - p) * -120}px)`
        : `scale(${0.82 + 0.18 * p})`) + ` rotate(${rot})`;
    }
    for (const m of s.querySelectorAll('.m')) {
      const ma = +m.dataset.a, mb = +m.dataset.b;
      const vis = r >= ma && r < mb;
      m.style.display = vis ? 'block' : 'none';
      if (!vis) continue;
      const k = (r - ma) / (mb - ma), punch = C(1 - (r - ma) / 0.18) * 0.05;
      if (!m.classList.contains('lbl')) m.style.transform = `scale(${1.07 - 0.06 * k + punch})`;
      if (m.classList.contains('clip')) {
        const i = Math.min(+m.dataset.n, Math.floor((r - ma) * 30) + 1);
        const src = m.dataset.dir + '/' + String(i).padStart(4, '0') + '.jpg';
        if (m.getAttribute('src') !== src) { m.setAttribute('src', src); waits.push(m.decode().catch(() => 0)); }
      }
    }
    for (const c of s.querySelectorAll('.cnt')) {
      const p = E(C((r - +c.dataset.d) / 0.9));
      c.textContent = fmt(+c.dataset.to * p, c.dataset.fmt);
    }
    for (const k of s.querySelectorAll('.tk')) k.style.transform = `translateX(${-r * +k.dataset.speed}px)`;
  }
  document.querySelector('.flash').style.opacity = flash;
  return Promise.all(waits);
}
"""


def page():
    build_scenes()
    html, t = "", 0.0
    for beats, body, cls in SCENES:
        d = b(beats)
        html += f'<section class="sc {cls}" data-a="{t:.4f}" data-b="{t + d:.4f}">{body}</section>'
        t += d
    inter = (N / "fontes/inter.css").read_text()
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Normani SP highlights</title>'
            f'<style>{inter}{CSS}</style></head><body>{html}<div class="flash"></div><script>{JS}</script></body></html>'), t


def main():
    from playwright.sync_api import sync_playwright
    prep_clips()
    html, dur = page()
    out = CACHE / "video.html"
    out.write_text(html)
    prev = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]] if "--preview" in sys.argv else None
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux*/chrome'))[-1]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"])
        pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        if prev:
            for s in prev:
                pg.evaluate("t => render(t)", s); pg.wait_for_timeout(50)
                pg.screenshot(path=str(CACHE / f"prev_{s:05.2f}.png"))
            br.close(); print("preview:", CACHE); return
        nfr = int(round(dur * FPS))
        silent = B / "Normani-SP-Highlights-sem-trilha.mp4"
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
        for i in range(nfr):
            pg.evaluate("t => render(t)", i / FPS)
            enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % 150 == 0: print(f"{i}/{nfr}", flush=True)
        enc.stdin.close(); enc.wait(); br.close()
    fade = dur - 2.5
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-ss", str(MUSIC_START), "-t", f"{dur:.3f}", "-i", str(MUSIC),
                    "-filter_complex", f"[1:a]afade=t=in:st=0:d=0.05,afade=t=out:st={fade:.2f}:d=2.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", str(B / "Normani-SP-Highlights.mp4")], check=True)
    print(f"ok: {dur:.1f}s")


if __name__ == "__main__":
    main()
