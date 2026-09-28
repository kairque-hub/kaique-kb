#!/usr/bin/env python3
"""Normani × Brasil 2026: gera o deck em HTML e fecha em PDF (1280x720, 16:9).

Fotos de perfil do time: img/pessoas/<slug>.jpg (slug = nome em minúsculas, sem acento, com hífen).
"""
import base64, glob, pathlib, sys, unicodedata

B = pathlib.Path(__file__).parent
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def uri(p):
    p = B / p
    return f"data:{MIME[p.suffix.lower()]};base64," + base64.b64encode(p.read_bytes()).decode()


def opt(p):
    return uri(p) if (B / p).exists() else None


def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return "-".join("".join(c if c.isalnum() else " " for c in s).split())


IMG = {k: uri(f"img/{k}.jpg") for k in ("crawl", "hips", "stand", "avatar")}
WORD = '<span class="word">NORMANI</span>'
FONTES = (B / "fontes/inter.css").read_text()

VLOGO = uri("img/vogue_logo.png")
TAG = f'<span>Normani × <img class="vl" src="{VLOGO}"> Brasil · Meli Music 2026</span>'
S = []


def slide(html, bg="", cls=""):
    S.append(f'<section class="sl {cls}" style="{bg}">{html}</section>')


def ft(sec, n):
    return (f'<div class="ft"><span>{sec}</span>'
            f'<span>{TAG}<b class="pn">{n:02d}</b></span></div>')


def blob(x, y, r, cor="y", o=1):
    c = {"y": "242,236,26", "g": "19,176,75"}[cor]
    return (f'<i class="blob" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'background:radial-gradient(circle,rgba({c},{o}) 0%,rgba({c},{o * .55}) 35%,rgba({c},0) 70%)"></i>')


def pill(t, cls=""):
    return f'<span class="pill {cls}">{t}</span>'


def verif():
    return ('<svg class="vf" viewBox="0 0 24 24"><path fill="#1D9BF0" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91C2.63 9.33 1.75 10.57 1.75 12s.88 2.67 2.19 3.34c-.46 1.39-.2 2.9.81 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.46 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34z"/>'
            '<path fill="#fff" d="M10.1 16.3l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>')


def avatar(nome, papel="", tam=58):
    f = opt(f"img/pessoas/{slug(nome)}.jpg") or opt(f"img/pessoas/{slug(nome)}.png")
    ini = "".join(w[0] for w in nome.replace("(", "").split()[:2]).upper()
    dentro = (f'<img src="{f}">' if f else f'<span>{ini}</span>')
    p = f'<small>{papel}</small>' if papel else ""
    return (f'<div class="pp"><div class="av" style="width:{tam}px;height:{tam}px;font-size:{tam * .34:.0f}px">'
            f'{dentro}</div><b>{nome}</b>{p}</div>')


def ph(rot, sub, h=None):
    """placeholder de foto que ainda não chegou"""
    return (f'<div class="ph"><div><b>{rot}</b><small>{sub}</small></div></div>')


# =============================================================== 01 capa
slide(
    blob(1060, 40, 260) + blob(90, 700, 330, "g") + blob(560, 690, 300) +
    f'<img src="{VLOGO}" style="position:absolute;left:60px;top:46px;height:40px;z-index:3">'
    '<p class="tr">Proposta de conteúdo exclusivo<br>para a Vogue Brasil</p>'
    '<div class="rule" style="top:118px"></div>'
    '<h1 class="giga" style="top:150px;font-size:196px">Normani</h1>'
    f'<div style="position:absolute;left:62px;top:405px;display:flex;align-items:center;gap:22px;z-index:3">'
    f'<span style="font-size:96px;font-weight:300;line-height:1">×</span><img src="{VLOGO}" style="height:74px">'
    '<span style="font-size:96px;letter-spacing:-.04em;line-height:1">Brasil</span></div>'
    f'<span class="pill" style="position:absolute;left:62px;top:530px;text-transform:none">Meli Music · 17 de outubro de 2026</span>'
    f'<div class="oval" style="left:915px;top:160px;width:305px;height:400px;background-image:url({IMG["stand"]});background-position:50% 8%;background-size:130%"></div>'
    '<p class="bl">Proposta para a Vogue Brasil · Normani no Meli Music · São Paulo</p>',
    cls="capa")

# =============================================================== 02 índice
idx = [("01", "A história dela com o Brasil"), ("02", "Linha do tempo"), ("03", "Os recibos"),
       ("04", "A proposta para a Vogue"), ("05", "Dia do show"), ("06", "Time local")]
slide(
    '<div class="half">' + blob(640, 360, 300) +
    f'<div class="hd">{pill("Índice")}<span>Normani × Vogue Brasil</span></div>'
    '<p class="big" style="position:absolute;left:60px;top:250px;width:470px">Normani em São Paulo para o primeiro show solo no Brasil. Uma proposta de conteúdo exclusivo para a Vogue Brasil.</p>'
    '<p class="meta" style="position:absolute;left:60px;top:345px">Meli Music 2026, 4ª edição<br>'
    '<b>Sábado, 17 de outubro de 2026</b><br>Mercado Livre Arena Pacaembu · São Paulo</p></div>'
    '<div class="idx" style="padding-top:120px">' + "".join(f'<p><small>{n}</small>{t}</p>' for n, t in idx) +
    '<div class="idxft"><span>Get Ready With Me</span><span>Look exclusivo</span><span>Dendezeiro</span><span>Meli Music</span><span>Time local</span></div></div>',
    cls="p0")

# =============================================================== 03 overview
slide(
    '<p style="position:absolute;left:60px;top:100px;font-size:30px">Visão</p>'
    f'<span class="pill yl" style="position:absolute;left:60px;top:147px">Índice</span>'
    '<h1 style="position:absolute;left:190px;top:18px;font-size:150px;letter-spacing:-.045em;font-weight:400">geral</h1>'
    '<div class="cap">'
    '<div class="c1"><h2>17 out</h2><p>o primeiro show solo dela no Brasil</p>'
    '<div class="row"><small>Meli Music</small><span>4ª edição</span></div></div>'
    '<div class="c2">'
    '<div><h3>4ª</h3><p>vez no Brasil<br>(2014, 2016, 2017)</p></div>'
    '<div><h3>14 anos</h3><p>falando com o Brasil<br>(2012 → 2026)</p></div>'
    '<div><h3>1ª</h3><p>atração internacional<br>da história do festival</p></div>'
    '<div><h3>5 dias</h3><p>em São Paulo<br>(15 → 19/10)</p></div>'
    '<div class="w"><small>Line-up</small><span>Anitta · Luísa Sonza · Gloria Groove · Pedro Sampaio</span></div>'
    '</div></div>'
    '<p class="big" style="position:absolute;left:60px;top:545px;width:520px;font-size:17px;line-height:1.4">'
    'Normani volta ao Brasil pela primeira vez desde 2017, e pela primeira vez sozinha. '
    'A proposta: a Vogue Brasil acompanha a preparação dela para o show e publica o look com exclusividade.</p>'
    '<div class="box dd" style="left:620px;top:535px;width:600px">'
    '<small class="lbl">Dia do show</small>'
    '<div class="tri"><div><h4>Sáb, 17/10</h4><p>Meli Music</p></div>'
    '<div><h4>12h</h4><p>Abertura dos portões</p></div>'
    '<div><h4>A definir</h4><p>Horário do show</p></div></div>'
    '<p style="margin-top:6px;font-size:12px">Mercado Livre Arena Pacaembu · São Paulo · ingressos a partir de R$45 (Sympla)</p></div>'
    '<p class="src" style="bottom:20px">Fontes: Meli Music / Sympla; Exame; Gazeta de São Paulo; The Rio Times (2026).</p>',
    bg="background:#fff")

# =============================================================== 04 história
slide(
    f'<div class="foto" style="left:0;top:0;width:520px;height:720px;background-image:url({IMG["crawl"]});background-position:22% 50%;background-size:auto 100%"></div>'
    '<div class="grad" style="left:520px">' + blob(470, 640, 260, "g") +
    f'<div class="hd" style="left:40px">{pill("Índice")}<span>01 · História</span></div>'
    '<h1 class="t2" style="left:40px;top:140px;font-size:68px">A história dela com<br>o Brasil não é nova.</h1>'
    '<p class="big" style="position:absolute;left:40px;top:340px;width:580px;font-size:19px;line-height:1.5">'
    'Normani fala com os fãs brasileiros desde 2012, antes do primeiro álbum do Fifth Harmony, '
    'e já se apresentou para eles em três turnês. Outubro de 2026 é a primeira vez dela aqui sozinha. '
    'Não é uma apresentação. É uma volta para casa.</p>'
    '<div class="yrs"><div><h3>2014</h3><p>Z Festival</p></div><div><h3>2016</h3><p>7/27 Tour</p></div>'
    '<div><h3>2017</h3><p>PSA Tour</p></div><div class="now"><h3>2026</h3><p>Primeiro show solo</p></div></div>'
    '<div class="ft" style="left:40px;right:60px"><span>A história dela com o Brasil</span>'
    f'<span>{TAG}<b class="pn">04</b></span></div></div>')

# =============================================================== 05 linha do tempo
tl = [
    ("top", "27 dez 2012", "Primeiros tweets", False, "Meses depois do X Factor, já falando com os fãs brasileiros no X."),
    ("bot", "10–12 out 2014", "Rio · Brasília · SP", True, "Primeira vez no Brasil. Z Festival com Austin Mahone: Vivo Rio, Net Live, Espaço das Américas."),
    ("top", "28 jun – 5 jul 2016", "7/27 Tour", True, "Cinco cidades: Porto Alegre, Curitiba, Rio, Brasília e São Paulo."),
    ("bot", "15 dez 2016", "No X", False, "De volta para casa depois da turnê, ainda falando com o Brasil."),
    ("top", "4–7 out 2017", "PSA Tour", True, "Belo Horizonte, Rio e atração principal do Villa Mix São Paulo."),
    ("bot", "17 out 2026", "Meli Music", True, "O primeiro show solo dela no Brasil. O próximo capítulo."),
]
xs = [70, 290, 510, 730, 950, 1200]
tlh = ['<div class="tline"></div>']
for (pos, d, t, live, txt), x in zip(tl, xs):
    tlh.append(f'<i class="dot {"live" if live else ""}" style="left:{x - 10}px"></i>')
    al = "right" if x > 1100 else "left"
    lx = x - 10 if al == "left" else x - 250 + 10
    lv = pill("Ao vivo", "sm") if live else ""
    tlh.append(f'<div class="ev {pos}" style="left:{lx}px;{"top:440px" if pos == "bot" else "bottom:325px"};text-align:{al}">'
               f'<small>{d.upper()}</small><h4>{t} {lv}</h4><p>{txt}</p></div>')
slide(
    blob(1180, 60, 250) + blob(620, 760, 260, "g", .55) +
    '<h1 class="t" style="top:50px">14 anos<br>de Brasil</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Linha do tempo</span>'
    '<div class="leg"><span><i class="dot live s"></i>Ao vivo no Brasil</span><span><i class="dot s"></i>Momento online</span></div>'
    + "".join(tlh) +
    '<p class="src">Fontes: Vagalume, Midiorama (2014); TMDQA!, Tracklist (2016); UAI, Concerts in Brazil (2017); @Normani no X; Meli Music (2026).</p>'
    + ft("Linha do tempo", 5))

# =============================================================== 06 recibos
tw = [("284362815190482944", "27 dez 2012 · 16h19 (BRT)", "Antes da estreia · era X Factor"),
      ("295616015503593472", "27 jan 2013 · 17h35 (BRT)", "Antes da estreia · falando com o Brasil"),
      ("340318633165213696", "31 mai 2013 · 1h07 (BRT)", "Antes da primeira vinda ao Brasil"),
      ("809461122948595712", "15 dez 2016 · 16h12 (BRT)", "Depois da 7/27 Tour no Brasil")]


def tcard(i, d, ctx, hl=False):
    return (f'<a class="tw {"hl" if hl else ""}" href="https://x.com/Normani/status/{i}"><div class="who"><img src="{IMG["avatar"]}">'
            f'<div><b>Normani {verif()}</b><span>@Normani · {d}</span></div></div>'
            f'<small class="lbl">Contexto</small><p class="ctx">{ctx}</p>'
            f'<p class="op">Abrir o post original no X ↗</p><p class="url">x.com/Normani/status/{i}</p></a>')


slide(
    blob(1180, 700, 280, "g", .6) + blob(1320, 640, 220) +
    '<h1 class="t" style="top:50px">Os recibos</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">No X</span>'
    '<p class="big" style="position:absolute;left:60px;top:170px;width:760px;font-size:19px;line-height:1.45">'
    'Antes de “Worth It”, antes de “Motivation”, antes do primeiro álbum do Fifth Harmony: a Normani já falava com o Brasil.</p>'
    '<div class="tgrid">' + tcard(*tw[0], hl=True) + tcard(*tw[1]) + tcard(*tw[2]) + tcard(*tw[3]) +
    '<div class="tw gr" style="grid-column:span 2"><h2>11 shows</h2><p>no Brasil com o Fifth Harmony, em 6 cidades, de 2014 a 2017. '
    'O de 17 de outubro é o primeiro só dela.</p></div></div>'
    + ft("Os recibos", 6))

# =============================================================== 07 vogue brasil
V_ART = "https://www.vogue.com/article/normani-dopamine-interview"
V_REEL = "https://www.instagram.com/reels/C8kf1WghZ25/"
slide(
    blob(90, 720, 280, "g", .8) + blob(560, 760, 240) +
    f'<div class="hd"><img src="{VLOGO}" style="height:26px"><span>Brasil · A proposta</span></div>'
    '<h1 class="t2" style="left:60px;top:100px;font-size:54px;line-height:1.04">Get Ready With Me<br>+ <mark>look exclusivo</mark></h1>'
    '<p class="big" style="position:absolute;left:60px;top:232px;width:580px;font-size:16.5px;line-height:1.5">'
    'Oferecer à Vogue Brasil um Get Ready With Me da Normani: o processo de preparação e o look exclusivo '
    'para o show do Meli Music, em São Paulo. O look será <b>custom Dendezeiro</b>.</p>'
    '<div class="vg" style="top:335px">'
    '<div><small>Redes sociais</small><h4>GRWM em collab</h4><ul>'
    '<li>Vídeo de Get Ready With Me em collab com a Vogue Brasil</li>'
    '<li>Gravado pelo time da artista ou pelo time da revista</li>'
    '<li>Gravação nos dias 15 ou 16 de outubro</li>'
    '<li>Publicação no dia 17, dia do show</li></ul></div>'
    '<div class="yl"><small>Site da Vogue Brasil</small><h4>Look exclusivo</h4><ul>'
    '<li>Fotos exclusivas do look da Normani</li>'
    '<li>Material oferecido com exclusividade para publicação no site</li></ul></div></div>'
    '<small class="lbl" style="position:absolute;left:690px;top:62px;z-index:3">Ela já fez com a Vogue US</small>'
    f'<a href="{V_ART}" class="shot" style="left:690px;top:88px;width:530px;height:279px;background-image:url({uri("img/vogue_artigo.jpg")})"></a>'
    f'<a href="{V_ART}" class="cap2" style="top:374px">Vogue.com · jun 2024 · entrevista sobre o álbum <i>Dopamine</i> ↗<br><span>vogue.com/article/normani-dopamine-interview</span></a>'
    f'<a href="{V_REEL}" class="shot" style="left:690px;top:430px;width:200px;height:200px;background-image:url({uri("img/vogue_reel.jpg")})"></a>'
    f'<a href="{V_REEL}" class="cap2" style="left:910px;top:440px;width:310px">@voguemagazine · Reel<br><b style="font-size:17px;font-weight:500;display:block;margin:6px 0">#VogueWorld Paris: Normani chega de Coach custom</b>25,3 mil curtidas ↗<br><span>instagram.com/reels/C8kf1WghZ25</span></a>'
    + ft("Vogue Brasil", 7))

# =============================================================== 08 dia do show
slide(
    f'<div class="foto" style="left:0;top:0;width:430px;height:720px;background-image:url({IMG["stand"]});background-position:50% 18%;background-size:cover"></div>'
    '<div class="grad" style="left:430px">' + blob(700, 700, 280, "g", .9) +
    f'<div class="hd" style="left:50px">{pill("Dia do show")}<span>Sábado, 17 de outubro</span></div>'
    '<h1 class="t2" style="left:50px;top:95px;font-size:62px">Meli Music.</h1>'
    '<p class="big" style="position:absolute;left:50px;top:180px;width:760px;font-size:17px">Mercado Livre Arena Pacaembu · portões às 12h · horário do show a definir</p>'
    '<div class="g2" style="top:235px">'
    '<div><small>01 · Buzz</small><h4>Influenciadores no show</h4><p>Criadores brasileiros no show e num meet &amp; greet, postando ao longo do dia.</p></div>'
    '<div><small>02 · Vogue Brasil</small><h4>Get Ready With Me</h4><p>Vídeo em collab com a Vogue Brasil, publicado no dia do show.</p></div>'
    '<div><small>03 · Vogue Brasil</small><h4>Exclusividade do look</h4><p>Fotos exclusivas do look para o site da Vogue Brasil.</p></div>'
    '<div><small>04 · After festival</small><h4>Ativação com imprensa local</h4><p>Entrevistas e conteúdo com veículos locais depois do show.</p></div>'
    '<div class="yl"><small>05 · Confirmado</small><h4>Vestindo Dendezeiro</h4><p>Look custom da marca brasileira para o show.</p></div>'
    '<div><small>06 · Na grade</small><h4>Normani Front Row</h4><p>Perucas com franja para os fãs da grade, como a Karol G fez no Coachella 2022.</p></div>'
    '</div>'
    '<div class="ft" style="left:50px;right:60px"><span>Dia do show</span>'
    f'<span>{TAG}<b class="pn">08</b></span></div></div>')

# =============================================================== 09 time local
equipe = [("Steff Lima", "Foto", "@stefflima"), ("Jhuan Martins", "Vídeo", "@jhuanmartins"),
          ("Kaique Brasileiro", "Creative and Communication Manager", "@kaique")]
slide(
    blob(1150, 80, 280) + blob(80, 720, 280, "g", .8) +
    '<h1 class="t" style="top:50px">Time local</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Em São Paulo</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:800px;font-size:19px;line-height:1.45">'
    'O time que produz o conteúdo com a Vogue Brasil em São Paulo: foto, vídeo e coordenação.</p>'
    '<div class="team" style="top:265px">' + "".join(
        f'<div>{avatar(n, "", 120)}<small class="lbl">{r}</small><p>{h}</p></div>' for n, r, h in equipe) + '</div>'
    + ft("Time local", 9))

# =============================================================== 10 obrigado
slide(
    blob(1150, 30, 260) + blob(90, 700, 330, "g") + blob(640, 720, 300) +
    f'<img src="{VLOGO}" style="position:absolute;left:60px;top:46px;height:40px;z-index:3">'
    '<h1 class="giga" style="top:220px;font-size:190px">Obrigado.</h1>'
    '<p style="position:absolute;left:62px;top:460px;font-size:17px">Normani × Vogue Brasil · Meli Music · 17 de outubro de 2026</p>'
    '<div class="rule" style="top:600px;width:440px;right:auto"></div>'
    '<p style="position:absolute;left:62px;top:615px;font-size:17px;font-weight:600">Kaique Brasileiro</p>'
    '<p style="position:absolute;left:62px;top:642px;font-size:13px">Creative and Communication Manager</p>'
    f'<div class="oval" style="left:880px;top:60px;width:340px;height:600px;background-image:url({IMG["hips"]});background-position:50% 30%;background-size:cover"></div>',
    cls="capa")

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
@page{size:1280px 720px;margin:0}
html,body{background:#888}
body{font-family:Inter,sans-serif;color:#0B0B0C;-webkit-font-smoothing:antialiased}
.sl{width:1280px;height:720px;position:relative;overflow:hidden;background:#D5D7E3;page-break-after:always;break-after:page}
.blob{position:absolute;border-radius:50%;pointer-events:none}
.pill{display:inline-block;border:1.4px solid #0B0B0C;border-radius:999px;padding:3px 15px;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;font-weight:500;line-height:1.35;white-space:nowrap;vertical-align:middle}
.pill.sm{font-size:9.5px;padding:1px 9px;border-width:1.2px}
.pill.yl{background:#F2EC1A}
.pill.wl{border-color:#fff;color:#fff}
mark{background:linear-gradient(90deg,#F2EC1A,#C8E23A);padding:0 .12em;border-radius:5px;color:inherit;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.rule{position:absolute;left:60px;right:60px;height:1.4px;background:#0B0B0C}
.ft{position:absolute;left:60px;right:60px;bottom:26px;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:500;z-index:5}
.ft>span:last-child{display:flex;align-items:center;gap:14px}
.pn{border:1.4px solid #0B0B0C;border-radius:999px;padding:1px 12px;font-weight:600;font-size:11px}
.hd{position:absolute;left:60px;top:48px;display:flex;align-items:center;gap:22px;font-size:13px;font-weight:500;z-index:3}
.src{position:absolute;left:60px;bottom:52px;font-size:10px;color:#555;z-index:3}
.t{position:absolute;left:60px;font-size:64px;font-weight:400;letter-spacing:-.035em;line-height:1.02;z-index:3}
.t2{position:absolute;font-size:74px;font-weight:400;letter-spacing:-.04em;line-height:1.0;z-index:3}
.big{font-size:22px;line-height:1.3;z-index:3}
.meta{font-size:14px;line-height:1.7;z-index:3}
.lbl{display:block;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
.foto{position:absolute;background-size:cover;background-position:center}
.foto.rd{border-radius:22px;border:1.4px solid #0B0B0C}
.grad{position:absolute;top:0;right:0;bottom:0;overflow:hidden;background:linear-gradient(180deg,#D5D7E3 0%,#E6E88A 45%,#F2EC1A 70%,#C9E53A 100%)}
.box{position:absolute;border:1.4px solid #0B0B0C;border-radius:22px;padding:16px 24px;z-index:3}
.box.wh{background:#fff}
.blk{position:absolute;background:#0B0B0C;color:#fff;border-radius:26px;padding:26px 30px;z-index:3}
.blk .q{font-size:27px;margin-left:16px;vertical-align:middle;letter-spacing:-.01em}
.blk .tri h4{color:#F2EC1A}
.tri{display:flex;gap:44px;margin-top:10px}
.tri h4{font-size:36px;font-weight:400;letter-spacing:-.03em}
.tri p{font-size:12.5px;margin-top:2px}
.dd .tri h4{font-size:30px;white-space:nowrap}
/* capa */
.capa .tr{position:absolute;right:60px;top:52px;text-align:right;font-size:13.5px;font-weight:500;line-height:1.4}
.giga{position:absolute;left:55px;font-size:230px;font-weight:400;letter-spacing:-.05em;line-height:1;z-index:3}
.giga2{position:absolute;left:62px;font-size:120px;font-weight:400;letter-spacing:-.04em;line-height:1;z-index:3}
.oval{position:absolute;border-radius:50%/50%;border:1.4px solid #0B0B0C;background-size:cover;z-index:3}
.word{font-size:34px;font-weight:600;letter-spacing:.34em;line-height:1}
.vl{height:10px;vertical-align:-1px}
.bl{position:absolute;left:60px;bottom:40px;font-size:13px;font-weight:500;z-index:3}
/* índice */
.half{position:absolute;left:0;top:0;bottom:0;width:640px;overflow:hidden;background:#D5D7E3}
.idx{position:absolute;left:640px;top:0;right:0;bottom:0;background:linear-gradient(170deg,#F2EC1A 0%,#F2EC1A 55%,#9ADB3E 85%,#13B04B 110%);padding:88px 60px 0 60px}
.idx p{font-size:33px;letter-spacing:-.02em;line-height:1.46;display:flex;align-items:baseline;gap:26px}
.idx p small{font-size:12px;font-weight:600;width:16px}
.idxft{position:absolute;left:60px;right:60px;bottom:74px;border-top:1.4px solid #0B0B0C;padding-top:22px;display:flex;justify-content:space-between;font-size:13px;font-weight:500}
/* overview */
.cap{position:absolute;left:40px;top:215px;width:1200px;height:300px;border:1.4px solid #0B0B0C;border-radius:150px;
 background:linear-gradient(90deg,#13B04B 0%,#9AD83F 30%,#F2EC1A 58%,#FBF7C8 85%,#fff 100%);z-index:2}
.c1{position:absolute;left:100px;top:55px}
.c1 h2{font-size:92px;font-weight:400;letter-spacing:-.05em;line-height:1}
.c1 p{font-size:14px;margin-top:10px}
.c1 .row{margin-top:40px;display:flex;align-items:baseline;gap:30px}
.c1 .row small{font-size:13px}.c1 .row span{font-size:30px;letter-spacing:-.03em}
.c2{position:absolute;left:545px;top:58px;width:620px;display:grid;grid-template-columns:repeat(4,1fr);row-gap:26px;border-left:1.4px solid #0B0B0C;padding-left:55px;height:190px}
.c2 h3{font-size:34px;font-weight:400;letter-spacing:-.035em;line-height:1}
.c2 p{font-size:12.5px;line-height:1.5;margin-top:8px}
.c2 .w{grid-column:1/5;display:flex;align-items:baseline;gap:18px}
.c2 .w small{font-size:13px}.c2 .w span{font-size:20px;letter-spacing:-.02em}
/* história */
.yrs{position:absolute;left:40px;top:500px;display:flex;gap:34px;z-index:3}
.yrs h3{font-size:58px;font-weight:400;letter-spacing:-.045em;line-height:1}
.yrs p{font-size:12.5px;font-weight:500;margin-top:6px}
.yrs .now h3{background:#0B0B0C;color:#F2EC1A;border-radius:12px;padding:0 10px}
/* timeline */
.leg{position:absolute;right:60px;top:170px;display:flex;gap:24px;font-size:13px;font-weight:500}
.leg span{display:flex;align-items:center;gap:8px}
.tline{position:absolute;left:60px;right:60px;top:409px;height:1.4px;background:#0B0B0C}
.dot{position:absolute;top:400px;width:20px;height:20px;border-radius:50%;border:1.4px solid #0B0B0C;background:#fff;z-index:2}
.dot.live{background:#13B04B;box-shadow:0 0 0 9px rgba(242,236,26,.75)}
.dot.s{position:static;width:14px;height:14px;display:inline-block;box-shadow:none}
.ev{position:absolute;width:250px;z-index:3}
.ev small{font-size:12px;font-weight:600;letter-spacing:.03em}
.ev h4{font-size:26px;font-weight:400;letter-spacing:-.025em;margin:3px 0 6px;white-space:nowrap}
.ev p{font-size:13px;line-height:1.45}
/* tweets */
.tgrid{position:absolute;left:60px;right:60px;top:250px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;z-index:3}
.tw{background:#fff;border:1.4px solid #0B0B0C;border-radius:22px;padding:17px 18px;height:148px;z-index:3}
.tw.hl{background:linear-gradient(120deg,#fff 30%,#F2EC1A 100%)}
.tw.gr{background:#13B04B}
.tw.gr h2{font-size:52px;font-weight:400;letter-spacing:-.04em;line-height:1}
.tw.gr p{font-size:13.5px;line-height:1.45;margin-top:10px;font-weight:500}
.who{display:flex;gap:11px;align-items:center}
.who img{width:37px;height:37px;border-radius:50%;object-fit:cover}
.who b{font-size:16.5px;display:flex;align-items:center;gap:4px}
.who span{font-size:13.5px;color:#444}
.vf{width:17px;height:17px}
.tw .lbl{font-size:10px;margin-top:9px;color:#333}
.ctx{color:#0E8A3A;font-size:14px;font-weight:500;margin-top:2px}
.op{font-size:12.5px;color:#444;margin-top:5px}
.url{font-size:10.5px;color:#444;margin-top:9px}
/* superfans */
.kpi4{position:absolute;left:60px;right:60px;top:225px;display:grid;grid-template-columns:repeat(4,1fr);z-index:3}
.kpi4 h2{font-size:62px;font-weight:400;letter-spacing:-.05em;line-height:1.1}
.kpi4 p{font-size:13.5px;width:230px;line-height:1.4;margin-top:6px}
.bar{display:flex;align-items:center;gap:12px;margin-top:14px}
.bar span{width:120px;text-align:right;font-size:13px;font-weight:500}
.bar i{height:24px;border:1.4px solid #0B0B0C;border-radius:14px}
.bar b{font-size:16px;font-weight:500}
.why{position:absolute;left:700px;top:392px;width:520px;z-index:3}
.why p{display:flex;align-items:baseline;border-bottom:1.4px solid #0B0B0C;padding:10px 0 6px}
.why b{font-size:34px;font-weight:400;letter-spacing:-.03em;width:125px;flex:none}
.why span{font-size:14px;font-weight:500}
/* bruno */
.cols{display:flex;gap:36px;align-items:flex-end;height:250px;margin:20px 20px 0;border-bottom:1.4px solid #0B0B0C}
.cols div{flex:1;display:flex;flex-direction:column;align-items:center;position:relative}
.cols i{font-style:normal;width:100%;border:1.4px solid #0B0B0C;border-bottom:0;display:block;position:relative}
.cols i b{position:absolute;top:10px;width:100%;text-align:center;font-size:29px;font-weight:400;letter-spacing:-.02em}
.cols i b.up{top:-46px;font-size:40px}
.cols span{position:absolute;bottom:-30px;font-size:13px;font-weight:500;white-space:nowrap}
/* códigos */
.c3{position:absolute;left:600px;width:620px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;z-index:3}
.c3.two{grid-template-columns:repeat(2,1fr)}
.c3>div{border-top:1.4px solid #0B0B0C;padding-top:12px}
.c3 small{font-size:11.5px;font-weight:600;color:#0E8A3A}
.c3 h4{font-size:30px;font-weight:400;letter-spacing:-.03em;margin:4px 0 8px}
.c3 p{font-size:13.5px;line-height:1.5}
/* plano */
.flow{position:absolute;left:60px;right:60px;top:275px;display:flex;align-items:center;gap:8px;font-size:18px;z-index:3}
.fc{flex:1;background:#fff;border:1.4px solid #0B0B0C;border-radius:20px;padding:14px 15px;height:150px}
.fc.yl{background:#F2EC1A}
.fc small{font-size:10.5px;font-weight:700;color:#0E8A3A;letter-spacing:.02em}
.fc h4{font-size:24px;font-weight:400;letter-spacing:-.025em;margin:4px 0 6px}
.fc p{font-size:12.3px;line-height:1.42}
.tbl{position:absolute;left:60px;right:60px;top:465px;font-size:14.5px;z-index:3}
.tbl>div{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 2fr;border-bottom:1.2px solid #777;padding:6px 0}
.tbl>div span:not(:first-child){color:#0E8A3A;letter-spacing:.1em}
.tbl>div span:last-child{letter-spacing:0;color:#0B0B0C;font-size:13.5px}
.tbl .th{border-bottom:1.4px solid #0B0B0C;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase}
.tbl .th span{color:#0B0B0C!important;letter-spacing:.1em!important;font-size:11px!important}
/* dias */
.it{position:absolute;left:60px;width:720px;border-top:1.4px solid #0B0B0C;padding-top:10px;z-index:3}
.it small{font-size:11.5px;font-weight:600;color:#0E8A3A;letter-spacing:.02em}
.it h4{font-size:27px;font-weight:400;letter-spacing:-.025em;margin:2px 0 5px}
.it p{font-size:14.5px;line-height:1.5}
.g2{position:absolute;left:50px;right:60px;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;z-index:3}
.g2>div{background:#fff;border:1.4px solid #0B0B0C;border-radius:18px;padding:13px 18px;height:128px}
.g2>div.yl{background:#13B04B}
.g2>div.yl small{color:#0B0B0C}
.g2 small{font-size:11px;font-weight:700;color:#0E8A3A}
.g2 h4{font-size:23px;font-weight:400;letter-spacing:-.025em;margin:3px 0 5px}
.g2 p{font-size:13px;line-height:1.45}
.ph{width:100%;height:100%;border:1.6px dashed #0B0B0C;border-radius:22px;background:repeating-linear-gradient(135deg,rgba(255,255,255,.55) 0 14px,rgba(255,255,255,.25) 14px 28px);display:flex;align-items:center;justify-content:center;text-align:center;position:relative;z-index:3}
.ph b{display:block;font-size:20px;font-weight:500;letter-spacing:-.01em}
.ph small{display:block;font-size:12px;margin-top:4px;letter-spacing:.08em;text-transform:uppercase}
/* pessoas */
.ppl{position:absolute;left:60px;right:60px;display:grid;grid-template-columns:repeat(7,1fr);row-gap:26px;z-index:3}
.ppl.sm{grid-template-columns:repeat(9,1fr);row-gap:30px}
.pp{display:flex;flex-direction:column;align-items:center;text-align:center}
.pp b{font-size:14.5px;font-weight:600;margin-top:10px;line-height:1.2}
.pp small{font-size:12px;color:#333;margin-top:2px}
.ppl.sm .pp b{font-size:13px}
.av{border-radius:50%;border:1.4px solid #0B0B0C;overflow:hidden;display:flex;align-items:center;justify-content:center;
 background:linear-gradient(145deg,#F6F29A 0%,#F2EC1A 45%,#A7DC3F 100%);font-weight:500;letter-spacing:-.02em}
.av img{width:100%;height:100%;object-fit:cover}
.steps{position:absolute;left:60px;top:460px;width:490px;z-index:3}
.steps p{display:flex;gap:18px;font-size:14.5px;border-top:1.4px solid #0B0B0C;padding:8px 0}
.steps small{font-size:11.5px;font-weight:700;color:#0E8A3A;width:18px}
.team{position:absolute;left:60px;right:60px;top:245px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;z-index:3}
.team>div{background:#fff;border:1.4px solid #0B0B0C;border-radius:22px;padding:26px;text-align:center;height:280px}
.team .pp b{font-size:21px;font-weight:500;margin-top:14px;letter-spacing:-.01em}
.team .lbl{margin-top:12px;font-size:10.5px;color:#0E8A3A;line-height:1.4}
.team p{font-size:14px;margin-top:6px}
a{color:inherit;text-decoration:none}
a.tw{display:block}
.vg{position:absolute;left:60px;width:580px;display:grid;grid-template-columns:1fr 1fr;gap:14px;z-index:3}
.vg>div{background:#fff;border:1.4px solid #0B0B0C;border-radius:20px;padding:14px 18px;height:295px}
.vg>div.yl{background:#F2EC1A}
.vg small{font-size:11px;font-weight:700;color:#0E8A3A;letter-spacing:.04em;text-transform:uppercase}
.vg h4{font-size:24px;font-weight:400;letter-spacing:-.025em;margin:4px 0 10px}
.vg ul{list-style:none}
.vg li{font-size:13px;line-height:1.38;padding:6px 0;border-top:1px solid rgba(0,0,0,.25)}
.shot{position:absolute;display:block;border:1.4px solid #0B0B0C;border-radius:16px;background-size:cover;background-position:center;z-index:3}
.cap2{position:absolute;left:690px;width:530px;font-size:12.5px;line-height:1.45;z-index:3}
.cap2 span{color:#555;font-size:11px}
"""


def html():
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Normani × Brasil 2026</title>'
            f'<style>{FONTES}{CSS}</style></head><body>{"".join(S)}</body></html>')


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = B / "Normani-Brasil-2026.html"
    out.write_text(html())
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    pdf = B / "Normani-Brasil-2026.pdf"
    prev = B / "preview"
    prev.mkdir(exist_ok=True)
    erros = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.on("pageerror", lambda e: erros.append(str(e)))
        pg.goto(out.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True, prefer_css_page_size=True)
        if "--png" in sys.argv:
            for i, el in enumerate(pg.query_selector_all("section.sl"), 1):
                el.screenshot(path=str(prev / f"{i:02d}.png"))
        b.close()
    if erros:
        print("ERROS JS:", erros)
        sys.exit(1)
    print(f"{pdf.name}: {len(S)} páginas, {pdf.stat().st_size / 1024 / 1024:.2f} MB")
