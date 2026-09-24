#!/usr/bin/env python3
"""Normani × Brasil 2026: gera o deck em HTML e fecha em PDF (1280x720, 16:9).

Fotos opcionais: se existirem, entram no lugar dos placeholders.
  img/merch.jpg              mockup do merch exclusivo
  img/notie1.jpg, notie2.jpg fotos do Terraço Notiê
  img/pessoas/<slug>.jpg     foto de perfil (slug = nome em minúsculas, sem acento, com hífen)
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


IMG = {k: uri(f"img/{k}.jpg") for k in ("crawl", "hips", "stand", "fans_karolg", "lilyallen", "avatar")}
LOGO = uri("img/logo_black.png")
LOGO_W = uri("img/logo_white.png")
FONTES = (B / "fontes/inter.css").read_text()

TAG = "Normani × Brasil · Meli Music 2026"
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
    '<p style="position:absolute;left:60px;top:52px;font-size:13.5px;font-weight:600;z-index:3">Normani × Brasil 2026</p>'
    '<p class="tr">A Brazil-first plan<br>for her Meli Music week</p>'
    '<div class="rule" style="top:100px"></div>'
    f'<img src="{LOGO}" style="position:absolute;left:52px;top:140px;width:720px;z-index:3">'
    '<h1 class="giga2" style="top:400px">Brasil 2026</h1>'
    f'<span class="pill" style="position:absolute;left:660px;top:470px;text-transform:none">Oct 15–19</span>'
    f'<div class="oval" style="left:915px;top:160px;width:305px;height:400px;background-image:url({IMG["stand"]});background-position:50% 8%;background-size:130%"></div>'
    '<p class="bl">Proposal for Normani · Meli Music · São Paulo · Brazilian fandom</p>',
    cls="capa")

# =============================================================== 02 índice
idx = [("01", "Her story with Brazil isn't new"), ("02", "Brazilian superfans, in numbers"),
       ("03", "Case: Bruno Mars"), ("04", "Cultural codes"), ("05", "Five days in São Paulo"),
       ("06", "Brazil-exclusive merch"), ("07", "The Normani front row"), ("08", "Local team")]
slide(
    '<div class="half">' + blob(640, 360, 300) +
    f'<div class="hd">{pill("Index")}<span>Normani × Brasil</span></div>'
    '<p class="big" style="position:absolute;left:60px;top:250px;width:440px">Her first solo show in Brazil. Five days to make it feel like a homecoming.</p>'
    '<p class="meta" style="position:absolute;left:60px;top:345px">Meli Music 2026, 4th edition<br>'
    '<b>Saturday, October 17, 2026</b><br>Mercado Livre Arena Pacaembu · São Paulo</p></div>'
    '<div class="idx">' + "".join(f'<p><small>{n}</small>{t}</p>' for n, t in idx) +
    '<div class="idxft"><span>Arrival</span><span>Merch</span><span>Reception</span><span>Show day</span><span>After party</span></div></div>',
    cls="p0")

# =============================================================== 03 overview
slide(
    '<p style="position:absolute;left:60px;top:100px;font-size:30px">Executive</p>'
    f'<span class="pill yl" style="position:absolute;left:60px;top:147px">Index</span>'
    '<h1 style="position:absolute;left:215px;top:18px;font-size:150px;letter-spacing:-.045em;font-weight:400">Overview</h1>'
    '<div class="cap">'
    '<div class="c1"><h2>Oct 17</h2><p>her first solo show in Brazil</p>'
    '<div class="row"><small>Meli Music</small><span>4th edition</span></div></div>'
    '<div class="c2">'
    '<div><h3>4th</h3><p>time in Brazil<br>(2014, 2016, 2017)</p></div>'
    '<div><h3>14 yrs</h3><p>talking to Brazil<br>(2012 → 2026)</p></div>'
    '<div><h3>1st</h3><p>international act in<br>Meli Music history</p></div>'
    '<div><h3>5 days</h3><p>in São Paulo<br>(Oct 15 → 19)</p></div>'
    '<div class="w"><small>Line-up</small><span>Anitta · Luísa Sonza · Gloria Groove · Pedro Sampaio</span></div>'
    '</div></div>'
    '<p class="big" style="position:absolute;left:60px;top:545px;width:560px;font-size:18px;line-height:1.4">'
    'Normani is back in Brazil for the first time since 2017, and for the first time on her own. '
    'The plan: turn one festival slot into a five-day Brazilian moment, built with the fans, the local scene and the press.</p>'
    '<div class="box" style="left:680px;top:535px;width:540px">'
    '<small class="lbl">Show day</small>'
    '<div class="tri"><div><h4>Sat, Oct 17</h4><p>Meli Music</p></div>'
    '<div><h4>12 PM</h4><p>Gates open (BRT)</p></div>'
    '<div><h4>TBC</h4><p>Set time</p></div></div>'
    '<p style="margin-top:6px;font-size:13px">Mercado Livre Arena Pacaembu · São Paulo · tickets from R$45 (Sympla)</p></div>'
    '<p class="src" style="bottom:20px">Sources: Meli Music / Sympla; Exame; Gazeta de São Paulo; The Rio Times (2026).</p>',
    bg="background:#fff")

# =============================================================== 04 história
slide(
    f'<div class="foto" style="left:0;top:0;width:520px;height:720px;background-image:url({IMG["crawl"]});background-position:22% 50%;background-size:auto 100%"></div>'
    '<div class="grad" style="left:520px">' + blob(470, 640, 260, "g") +
    f'<div class="hd" style="left:40px">{pill("Index")}<span>01 · History</span></div>'
    '<h1 class="t2" style="left:40px;top:140px">Her story with Brazil<br>isn\'t new.</h1>'
    '<p class="big" style="position:absolute;left:40px;top:340px;width:560px;font-size:19px;line-height:1.5">'
    'Normani has been talking to Brazilian fans since 2012, before Fifth Harmony had an album out, '
    'and has played for them on three tours. October 2026 is her first time here on her own. '
    'It isn\'t an introduction. It\'s a homecoming.</p>'
    '<div class="yrs"><div><h3>2014</h3><p>Z Festival</p></div><div><h3>2016</h3><p>7/27 Tour</p></div>'
    '<div><h3>2017</h3><p>PSA Tour</p></div><div class="now"><h3>2026</h3><p>First solo show</p></div></div>'
    '<div class="ft" style="left:40px;right:60px"><span>Her story with Brazil</span>'
    f'<span>{TAG}<b class="pn">04</b></span></div></div>')

# =============================================================== 05 timeline
tl = [
    ("top", "Dec 27, 2012", "Early tweets", False, "Months after The X Factor, already talking to Brazilian fans on X."),
    ("bot", "Oct 10–12, 2014", "Rio · Brasília · SP", True, "First time in Brazil. Z Festival with Austin Mahone: Vivo Rio, Net Live, Espaço das Américas."),
    ("top", "Jun 28 – Jul 5, 2016", "7/27 Tour", True, "Five cities: Porto Alegre, Curitiba, Rio, Brasília and São Paulo."),
    ("bot", "Dec 15, 2016", "On X", False, "Back home after the tour, still talking to Brazil."),
    ("top", "Oct 4–7, 2017", "PSA Tour", True, "Belo Horizonte, Rio, and headlining Villa Mix São Paulo."),
    ("bot", "Oct 17, 2026", "Meli Music", True, "Her first solo show in Brazil. The next chapter."),
]
xs = [70, 290, 510, 730, 950, 1200]
tlh = ['<div class="tline"></div>']
for (pos, d, t, live, txt), x in zip(tl, xs):
    tlh.append(f'<i class="dot {"live" if live else ""}" style="left:{x - 10}px"></i>')
    al = "right" if x > 1100 else "left"
    lx = x - 10 if al == "left" else x - 250 + 10
    lv = pill("Live", "sm") if live else ""
    top = 300 if pos == "top" else 440
    anc = "bottom:auto" if pos == "bot" else ""
    tlh.append(f'<div class="ev {pos}" style="left:{lx}px;{"top:" + str(top) + "px" if pos == "bot" else "bottom:" + str(720 - 395) + "px"};text-align:{al}">'
               f'<small>{d.upper()}</small><h4>{t} {lv}</h4><p>{txt}</p></div>')
slide(
    blob(1180, 60, 250) + blob(620, 760, 260, "g", .55) +
    '<h1 class="t" style="top:50px">Fourteen years<br>of Brazil</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Timeline</span>'
    '<div class="leg"><span><i class="dot live s"></i>Live in Brazil</span><span><i class="dot s"></i>Online moment</span></div>'
    + "".join(tlh) +
    '<p class="src">Sources: Vagalume, Midiorama (2014); TMDQA!, Tracklist (2016); UAI, Concerts in Brazil (2017); @Normani on X; Meli Music (2026).</p>'
    + ft("Timeline", 5))

# =============================================================== 06 receipts
tw = [("284362815190482944", "Dec 27, 2012 · 4:19 PM BRT", "Pre-debut · X Factor era"),
      ("295616015503593472", "Jan 27, 2013 · 5:35 PM BRT", "Pre-debut · talking to Brazil"),
      ("340318633165213696", "May 31, 2013 · 1:07 AM BRT", "Before her first trip to Brazil"),
      ("809461122948595712", "Dec 15, 2016 · 4:12 PM BRT", "After the 7/27 Tour Brazil leg")]


def tcard(i, d, ctx, hl=False):
    return (f'<div class="tw {"hl" if hl else ""}"><div class="who"><img src="{IMG["avatar"]}">'
            f'<div><b>Normani {verif()}</b><span>@Normani · {d}</span></div></div>'
            f'<small class="lbl">Context</small><p class="ctx">{ctx}</p>'
            f'<p class="op">Open the original post on X ↗</p><p class="url">x.com/Normani/status/{i}</p></div>')


slide(
    blob(1180, 700, 280, "g", .6) + blob(1320, 640, 220) +
    '<h1 class="t" style="top:50px">The receipts</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">On X</span>'
    '<p class="big" style="position:absolute;left:60px;top:170px;width:720px;font-size:19px;line-height:1.45">'
    'Before “Worth It”, before “Motivation”, before the first Fifth Harmony album: Normani was already talking to Brazil.</p>'
    '<div class="tgrid">' + tcard(*tw[0], hl=True) + tcard(*tw[1]) + tcard(*tw[2]) + tcard(*tw[3]) +
    '<div class="tw gr" style="grid-column:span 2"><h2>11 shows</h2><p>in Brazil with Fifth Harmony, across 6 cities, from 2014 to 2017. '
    'Oct 17 is the first one that is hers alone.</p></div></div>'
    + ft("Receipts", 6))

# =============================================================== 07 superfans
slide(
    '<h1 class="t" style="top:50px">Brazilian superfans,<br>in numbers</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Data</span>'
    '<div class="rule" style="top:200px"></div>'
    '<div class="kpi4"><div><h2>150M</h2><p>social media users, 70.4% of the population</p></div>'
    '<div><h2>+14.1%</h2><p>recorded-music growth in 2025, 16th straight year up</p></div>'
    '<div><h2>#8</h2><p>music market in the world, up from #9 (IFPI 2026)</p></div>'
    '<div><h2>~83%</h2><p>of Brazil’s music revenue comes from streaming</p></div></div>'
    '<div class="box wh" style="left:60px;top:390px;width:600px;height:170px">'
    '<small class="lbl">Daily time on social media</small>'
    '<div class="bar"><span>Brazil</span><i style="width:340px;background:#13B04B"></i><b>3h37m</b></div>'
    '<div class="bar"><span>World average</span><i style="width:220px;background:#fff"></i><b>2h21m</b></div>'
    '<p style="font-size:14px;margin-top:14px">Brazilians spend <b>+54%</b> more time on social than the global average.</p></div>'
    '<div class="why"><small class="lbl">Why superfans matter</small>'
    '<p><b>20%</b><span>of listeners are superfans (Luminate / Goldman Sachs)</span></p>'
    '<p><b>+80%</b><span>more spent per month than the average listener</span></p>'
    '<p><b>2×</b><span>spend on physical products: vinyl, CDs</span></p>'
    '<p><b>+17.1%</b><span>Latin America: fastest-growing region in the world</span></p></div>'
    '<p class="src">Sources: DataReportal Digital 2026 Brazil; IFPI Global Music Report 2026; Pro-Música Brasil (Mar 2026); Luminate 2024-25; Goldman Sachs “Music in the Air”.</p>'
    + ft("Superfans", 7),
    bg="background:linear-gradient(135deg,#F2EC1A 0%,#F2EC1A 58%,#13B04B 100%)")

# =============================================================== 08 bruno mars
slide(
    '<h1 class="t" style="top:50px">Case: Bruno Mars</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Rollout made for Brazil</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:520px;font-size:18px;line-height:1.45">'
    'He didn’t just tour Brazil. He built a Brazil-specific rollout, in Portuguese, with local references. Brazil answered.</p>'
    '<div class="box wh" style="left:60px;top:260px;width:520px;height:350px">'
    '<small class="lbl">Instagram followers</small>'
    '<div class="cols"><div><i style="height:190px;background:#fff"><b>~29M</b></i><span>Before The Town ’23</span></div>'
    '<div><i style="height:220px;background:#F2EC1A"><b>33M+</b></i><span>Mar 2024</span></div>'
    '<div><i style="height:28px;background:#13B04B"><b class="up">+4M</b></i><span>Growth</span></div></div></div>'
    '<div class="why" style="left:640px;top:150px;width:580px">'
    '<p><b style="font-size:50px;width:220px">50M+</b><span>views on a Brazilian video, his most-watched content at the time</span></p>'
    '<p><b style="font-size:50px;width:220px">358M</b><span>potential reach from the 2024 tour, in just over a month</span></p>'
    '<p><b style="font-size:50px;width:220px">+243%</b><span>Deezer streams during his Brazil run</span></p></div>'
    '<div class="blk" style="left:640px;top:430px;width:580px">'
    f'{pill("Single made for Brazil", "wl")}<span class="q">“Bonde do Brunão”</span>'
    '<div class="tri"><div><h4>13M+</h4><p>likes</p></div><div><h4>2.3M</h4><p>shares</p></div><div><h4>687K</h4><p>comments</p></div></div></div>'
    '<p class="src">Sources: Instagram @brunomars; Deezer; tour social listening (2023-2024).</p>'
    + ft("Bruno Mars", 8),
    bg="background:linear-gradient(160deg,#F2EC1A 0%,#F2EC1A 60%,#13B04B 115%)")

# =============================================================== 09 códigos culturais
slide(
    blob(90, 90, 250, "g") + blob(1250, 700, 300) +
    f'<span class="pill" style="position:absolute;left:60px;top:45px">Cultural codes</span>'
    '<span style="position:absolute;right:60px;top:45px;font-size:13px">04</span>'
    '<h1 class="t" style="top:90px;font-size:54px;line-height:1.05;width:1150px">The only way to break into the Brazilian market is through <mark>local cultural codes.</mark></h1>'
    '<p class="big" style="position:absolute;left:60px;top:222px;font-size:18px">Most international artists ignore this. The ones who don’t get adopted.</p>'
    '<div class="tw" style="left:60px;top:275px;width:470px;height:auto;position:absolute;padding:20px 22px">'
    f'<div class="who"><img src="{IMG["lilyallen"]}"><div><b>Lily Allen {verif()}</b><span>@lilyallen · May 11, 2026</span></div></div>'
    '<p style="font-size:21px;line-height:1.45;margin:10px 0 8px">Quero dançar com os gays na <mark>Zig</mark>, visitar a <mark>casa da Vita</mark> e conhecer a <mark>Patixa</mark></p>'
    '<p style="font-size:12.5px;color:#555">' + pill("EN", "sm") + ' I want to dance with the gays at Zig, visit Vita’s house and meet Patixa</p></div>'
    '<div class="c3" style="top:275px">'
    '<div><small>01</small><h4>Zig</h4><p>A legendary gay club in São Paulo that became the city’s point of reference.</p></div>'
    '<div><small>02</small><h4>Casa da Vita</h4><p>A nod to <i>Vita’s House</i>, the album by Vita, a trans artist whose tracks took over clubs and the underground.</p></div>'
    '<div><small>03</small><h4>Patixa</h4><p>A national meme: an “influencer” who never made content herself. Every video of her online was made by other people.</p></div></div>'
    '<div class="rule" style="top:500px;right:230px"></div>'
    '<p class="big" style="position:absolute;left:60px;top:515px;width:1000px;font-size:19px;line-height:1.45">'
    'Three references only a Brazilian on the internet would get. It went viral across Brazilian stan Twitter. '
    'This plan speaks the same language: <mark>the fan club, Dendezeiro, funk, and the local R&amp;B and rap scene.</mark></p>'
    + ft("Cultural codes", 9),
    bg="background:#fff")

# =============================================================== 10 cinco dias
dias = [("Day 1 · Thu, Oct 15", "Arrival", "Fan welcome at the airport, Brazil-only merch, fitting with Dendezeiro.", True),
        ("Day 2 · Fri, Oct 16", "Reception", "Rehearsal. At night, a private reception for the local scene at Terraço Notiê.", False),
        ("Day 3 · Sat, Oct 17", "Show day", "Meli Music. Influencers, GRWM, press, a Dendezeiro look, the Normani front row.", False),
        ("Day 4 · Sun, Oct 18", "After party", "A funk-themed party by Agência Dutra for the line-up and the scene.", False),
        ("Day 5 · Mon, Oct 19", "São Paulo", "Local stores and a day with ELLE or Vogue (TBC). Flight home at night.", False)]
slide(
    blob(1100, 60, 300) + blob(1280, 200, 220, "g", .7) +
    '<h1 class="t" style="top:50px">Five days in <mark>São Paulo</mark></h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">The plan</span>'
    '<p class="big" style="position:absolute;left:60px;top:170px;width:760px;font-size:19px;line-height:1.45">'
    'From the moment she lands until the moment she leaves, every day has a Brazilian story to tell, '
    'and every story is built with the people who already love her here.</p>'
    '<div class="flow">' + "→".join(
        f'<div class="fc {"yl" if h else ""}"><small>{d}</small><h4>{t}</h4><p>{x}</p></div>' for d, t, x, h in dias) + '</div>'
    '<div class="tbl"><div class="th"><span></span><span>Fans</span><span>Local scene</span><span>Press &amp; media</span><span>Hosted by</span></div>'
    '<div><span>Airport welcome</span><span>●●●</span><span>●○○</span><span>●●○</span><span>Fan club Normani Brasil</span></div>'
    '<div><span>Notiê reception</span><span>○○○</span><span>●●●</span><span>●●○</span><span>Terraço Notiê</span></div>'
    '<div><span>Show day</span><span>●●●</span><span>●●●</span><span>●●●</span><span>Meli Music</span></div>'
    '<div><span>After party</span><span>●○○</span><span>●●●</span><span>●●○</span><span>Agência Dutra</span></div></div>'
    + ft("The plan", 10))

# =============================================================== 11 dia 1
slide(
    f'<div class="foto" style="right:0;top:0;width:430px;height:720px;background-image:url({IMG["hips"]});background-position:50% 20%;background-size:cover"></div>'
    + blob(700, 740, 260, "g", .6) + blob(130, -20, 200) +
    f'<div class="hd">{pill("Day 1")}<span>Thursday, October 15</span></div>'
    '<h1 class="t2" style="left:60px;top:110px">Arrival.</h1>'
    '<p class="big" style="position:absolute;left:60px;top:230px;width:720px;font-size:19px;line-height:1.45">'
    'Her arrival is big from the moment she steps into the country.</p>'
    '<div class="it" style="top:295px"><small>01 · São Paulo airport</small><h4>Fan welcome</h4>'
    '<p>A welcome arranged ahead of time with fans, led by the local fan club <b>Normani Brasil</b>: signs, banners, '
    'a photo with fans and a drop of the Brazil-exclusive merch.</p></div>'
    '<div class="it" style="top:425px"><small>02 · Same day</small><h4>Pushed to local pop press</h4>'
    '<p>Photos and videos go straight to the big pop outlets, like <b>POPline</b> and <b>Hugo Gloss</b>, so the arrival becomes news within hours.</p></div>'
    '<div class="it" style="top:545px"><small>03 · At the hotel · time TBD</small><h4>Fitting with Dendezeiro</h4>'
    '<p>A Black-owned Brazilian fashion label. The fitting prepares her show-day look.</p></div>'
    + '<div class="ft" style="right:470px"><span>Day 1 · Arrival</span>'
    f'<span>{TAG}<b class="pn">11</b></span></div>')

# =============================================================== 12 merch
merch = opt("img/merch.jpg") or opt("img/merch.png")
mimg = (f'<div class="foto rd" style="left:700px;top:60px;width:520px;height:560px;background-image:url({merch});background-size:contain;background-repeat:no-repeat;background-color:#fff"></div>'
        if merch else '<div style="position:absolute;left:700px;top:60px;width:520px;height:560px">'
        + ph("Merch mockup", "Brazil-exclusive piece") + '</div>')
slide(
    blob(90, 700, 300, "g") + blob(480, 720, 260) + mimg +
    f'<div class="hd">{pill("Merch")}<span>Day 1 → Day 3</span></div>'
    '<h1 class="t2" style="left:60px;top:110px;font-size:62px">A piece of Brazil<br>to take home.</h1>'
    '<p class="big" style="position:absolute;left:60px;top:275px;width:580px;font-size:18px;line-height:1.5">'
    'A limited merch drop made only for this trip. It gives fans something no other country has, '
    'and it leaves a physical mark of her time here: a keepsake of the week.</p>'
    '<div class="c3 two" style="left:60px;top:400px;width:580px">'
    '<div><small>01</small><h4>Connection</h4><p>Made for Brazil, with Brazil. Fans wear it at the airport, the show and online.</p></div>'
    '<div><small>02</small><h4>A keepsake</h4><p>A piece that outlives the weekend and keeps her Brazil trip in people’s feeds.</p></div></div>'
    '<div class="box" style="left:60px;top:560px;width:580px;background:#fff"><small class="lbl">Cost</small>'
    '<p style="font-size:15px;margin-top:4px"><b>Price TBC.</b> We can start with a smaller run to keep it exclusive and the cost low.</p></div>'
    + ft("Merch", 12))

# =============================================================== 13 dia 2
n1, n2 = opt("img/notie1.jpg"), opt("img/notie2.jpg")
fv = lambda f, sub: (f'<div class="foto rd" style="position:relative;width:100%;height:100%;background-image:url({f})"></div>' if f
                     else ph("Terraço Notiê", sub))
slide(
    blob(1250, 30, 220) +
    f'<div class="hd">{pill("Day 2")}<span>Friday, October 16</span></div>'
    '<h1 class="t2" style="left:60px;top:110px;font-size:62px">Rehearsal by day.<br>The scene by night.</h1>'
    '<div class="it" style="top:285px;width:560px"><small>01 · Daytime</small><h4>Rehearsal</h4>'
    '<p>The day is hers and the band’s. No press, no appearances.</p></div>'
    '<div class="it" style="top:395px;width:560px"><small>02 · 7 PM · Terraço Notiê</small><h4>A private reception for the local scene</h4>'
    '<p>Brazil’s R&amp;B, pop, funk and rap artists, together on a rooftop in downtown São Paulo. '
    'The venue covers everything: drinks and content (photo &amp; video).</p></div>'
    '<div class="box" style="left:60px;top:570px;width:560px;background:#fff">'
    '<p style="font-size:14.5px"><b>Nothing is shared without the artist’s approval.</b> Every photo and video goes through her team first.</p></div>'
    '<div style="position:absolute;left:680px;top:110px;width:540px;height:300px">' + fv(n1, "Rooftop") + '</div>'
    '<div style="position:absolute;left:680px;top:425px;width:262px;height:190px">' + fv(n2, "Interior") + '</div>'
    '<div class="box" style="left:958px;top:425px;width:262px;height:190px;background:#F2EC1A">'
    '<small class="lbl">The venue</small><p style="font-size:13px;line-height:1.45;margin-top:6px">Rooftop of the Shopping Light building, downtown SP. '
    'Chef Onildo Rocha. “Best Brazilian Restaurant”, Veja Comer &amp; Beber 2021-23.</p></div>'
    + ft("Day 2 · Reception", 13))

# =============================================================== 14 convidados notiê
artistas = [("Anitta", "Pop · funk"), ("IZA", "Pop · R&B"), ("Pabllo Vittar", "Pop"), ("Gloria Groove", "Pop · rap"),
            ("Liniker", "Soul · R&B"), ("Marina Sena", "Pop"), ("Any Gabrielly", "Pop"), ("Carol Biazin", "Pop"),
            ("Duquesa", "Rap"), ("Budah", "Rap · R&B"), ("Ebony", "Rap"), ("Veigh", "Trap"), ("Teto", "Trap")]
slide(
    blob(100, 720, 300, "g", .8) + blob(560, 760, 260) +
    '<h1 class="t" style="top:50px">Who’s on the list</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Day 2 · Guests</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:900px;font-size:18px;line-height:1.45">'
    'Brazilian R&amp;B, pop, funk and rap artists, invited to meet Normani before the show. '
    'Two of them, Anitta and Gloria Groove, share the Meli Music line-up with her.</p>'
    '<div class="ppl" style="top:250px">' + "".join(avatar(n, p, 92) for n, p in artistas) + '</div>'
    '<div class="box wh" style="left:60px;top:590px;width:1160px;padding:12px 20px;display:flex;gap:40px;font-size:14px">'
    '<span><b>Where</b> Terraço Notiê</span><span><b>When</b> Fri, Oct 16 · 7 PM</span>'
    '<span><b>Hosted by</b> the venue: drinks + photo &amp; video</span><span><b>Cost to the artist</b> none</span></div>'
    + ft("Day 2 · Guests", 14))

# =============================================================== 15 dia 3
slide(
    f'<div class="foto" style="left:0;top:0;width:430px;height:720px;background-image:url({IMG["stand"]});background-position:50% 18%;background-size:cover"></div>'
    '<div class="grad" style="left:430px">' + blob(700, 700, 280, "g", .9) +
    f'<div class="hd" style="left:50px">{pill("Day 3")}<span>Saturday, October 17 · Show day</span></div>'
    '<h1 class="t2" style="left:50px;top:95px;font-size:62px">Meli Music.</h1>'
    '<p class="big" style="position:absolute;left:50px;top:180px;width:760px;font-size:17px">Mercado Livre Arena Pacaembu · gates at 12 PM · set time TBC</p>'
    '<div class="g2" style="top:235px">'
    '<div><small>01 · Buzz</small><h4>Influencers at the show</h4><p>17 Brazilian creators invited to watch the show and join a meet &amp; greet, posting all day.</p></div>'
    '<div><small>02 · Vogue</small><h4>Get Ready With Me</h4><p>Backstage GRWM coverage with Vogue.</p></div>'
    '<div><small>03 · Glamour or ELLE</small><h4>Exclusive look</h4><p>An exclusive look feature with Glamour or ELLE.</p></div>'
    '<div><small>04 · At the festival</small><h4>Local press</h4><p>Interviews with local outlets at the festival.</p></div>'
    '<div class="yl"><small>05 · Confirmed</small><h4>Wearing Dendezeiro</h4><p>Her stage look by the Brazilian label, fitted on Day 1.</p></div>'
    '<div><small>06 · Front row</small><h4>The Normani front row</h4><p>Bang wigs for the crowd. See page 17.</p></div>'
    '</div>'
    '<div class="ft" style="left:50px;right:60px"><span>Day 3 · Show day</span>'
    f'<span>{TAG}<b class="pn">15</b></span></div></div>')

# =============================================================== 16 influenciadores
infl = ["Camila de Lucas", "Dan Mendes", "Ana Flávia", "Foquinha", ("Carol Prado", "Estadão"), "Bianca Andrade",
        "Jude Paulla", "Josy Ramos", "Magá Moura", "Lucas Guedes", "Álvaro", "Priscila Evelyn", "MC Soffia",
        "Julia Rodrigues", "Juliano Floss", "Jess", "Patixa"]
slide(
    blob(1200, 60, 260) + blob(1300, 260, 200, "g", .7) +
    '<h1 class="t" style="top:50px">Buzz from the crowd</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">Day 3 · Influencers</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:900px;font-size:18px;line-height:1.45">'
    'Brazilian creators in pop, beauty, humor, fashion and culture, invited to watch the show and join a meet &amp; greet. '
    'They make the buzz during the show and across her whole time in Brazil.</p>'
    '<div class="ppl sm" style="top:250px">' + "".join(
        avatar(n, "", 82) if isinstance(n, str) else avatar(n[0], n[1], 82) for n in infl) + '</div>'
    '<div class="box wh" style="left:60px;top:590px;width:1160px;padding:12px 20px;display:flex;gap:40px;font-size:14px">'
    '<span><b>When</b> Sat, Oct 17 · show + meet &amp; greet</span><span><b>Where</b> Mercado Livre Arena Pacaembu</span>'
    '<span><b>The ask</b> attend, meet her, post during the show</span></div>'
    + ft("Day 3 · Influencers", 16))

# =============================================================== 17 perucas
slide(
    '<div class="half" style="width:600px">' + blob(540, 100, 260) +
    f'<div class="hd">{pill("Idea")}<span>The Normani front row</span></div>'
    '<h1 class="t2" style="left:60px;top:110px;font-size:58px">A front row<br>of Normanis.</h1>'
    '<p class="big" style="position:absolute;left:60px;top:265px;width:490px;font-size:17.5px;line-height:1.5">'
    'We buy a batch of cheap lace wigs with bangs, her signature look, and hand them out to fans in the front rows before the show. '
    'That guarantees one image: a crowd of fans dressed as Normani.</p>'
    '<div class="steps"><p><small>01</small>Buy cheap bang lace wigs in bulk</p><p><small>02</small>Hand them out at the front, before the show</p>'
    '<p><small>03</small>Shots from the stage, the press pit and the influencers</p><p><small>04</small>Content that feeds the crowd, the press and her own posts</p></div>'
    + '</div>'
    f'<div class="foto" style="left:600px;top:0;width:680px;height:440px;background-image:url({IMG["fans_karolg"]});background-position:50% 40%;background-size:cover"></div>'
    '<div class="blk" style="left:600px;top:440px;width:680px;height:280px;border-radius:0;padding:30px 40px">'
    f'{pill("Reference", "wl")}<h3 style="font-size:34px;font-weight:400;margin:14px 0 10px;letter-spacing:-.02em">Karol G, Coachella 2022</h3>'
    '<p style="font-size:15.5px;line-height:1.5;color:#ddd;width:580px">Fans showed up in blue wigs, her signature color. '
    'The crowd itself became one of the images of her set, and the fans became part of the story.</p>'
    '<p style="font-size:10.5px;color:#888;margin-top:14px">Photo: Gina Ferazzi / Los Angeles Times via Getty Images</p></div>'
    + '<div class="ft" style="right:auto;width:480px"><span>The Normani front row</span>'
    f'<span><b class="pn">17</b></span></div>',
    bg="background:#D5D7E3")

# =============================================================== 18 dia 4
slide(
    blob(1100, 80, 320) + blob(1250, 600, 280, "g") + blob(80, 740, 240, "g", .6) +
    f'<div class="hd">{pill("Day 4")}<span>Sunday, October 18</span></div>'
    '<h1 class="t2" style="left:60px;top:110px">After party.</h1>'
    '<p class="big" style="position:absolute;left:60px;top:230px;width:640px;font-size:19px;line-height:1.5">'
    'A funk music night hosted by <b>Agência Dutra</b>, for the Meli Music line-up, local artists and the invited influencers.</p>'
    '<div class="c3" style="left:60px;top:350px;width:1160px">'
    '<div><small>01 · Who</small><h4>Agência Dutra</h4><p>Specialists in events for Brazil’s Black community: Carnival, Rock in Rio and more. @agenciadutra</p></div>'
    '<div><small>02 · Theme</small><h4>Funk music</h4><p>Brazilian funk, the sound of the country’s streets and charts, and a natural match for her dance-first shows.</p></div>'
    '<div><small>03 · Guests</small><h4>Invite-only</h4><p>Line-up artists, local artists and influencers. No ticket sales.</p></div></div>'
    '<div class="cap" style="top:540px;height:110px;width:1160px;left:60px;padding:0 50px;display:flex;align-items:center;gap:70px">'
    '<div><h3 style="font-size:52px">$0</h3></div><p style="font-size:17px;line-height:1.4;width:760px">'
    '<b>No cost to the artist.</b> The party is fully produced and paid for by Agência Dutra, with no tickets sold.</p></div>'
    + ft("Day 4 · After party", 18))

# =============================================================== 19 dia 5
slide(
    f'<div class="foto" style="right:0;top:0;width:460px;height:720px;background-image:url({IMG["crawl"]});background-position:78% 50%;background-size:auto 100%"></div>'
    + blob(200, 720, 260) + blob(780, 700, 200, "g", .6) +
    f'<div class="hd">{pill("Day 5")}<span>Monday, October 19</span></div>'
    '<h1 class="t2" style="left:60px;top:110px;font-size:62px">São Paulo,<br>then home.</h1>'
    '<div class="it" style="top:300px;width:660px"><small>Daytime</small><h4>Local stores</h4>'
    '<p>Visits to São Paulo’s local stores and labels: a real day in the city, with content along the way.</p></div>'
    '<div class="it" style="top:410px;width:660px"><small>Daytime · TBC</small><h4>A day with ELLE or Vogue</h4>'
    '<p>A day-in-the-life feature with ELLE or Vogue.</p></div>'
    '<div class="it" style="top:520px;width:660px"><small>Night</small><h4>Flight back to the US</h4>'
    '<p>Five days, one show, and a Brazil story told from arrival to departure.</p></div>'
    + '<div class="ft" style="right:500px"><span>Day 5 · Departure</span>'
    f'<span>{TAG}<b class="pn">19</b></span></div>')

# =============================================================== 20 equipe
equipe = [("Steff Lima", "Photo", "@stefflima"), ("Jhuan Martins", "Video", "@jhuanmartins"),
          ("Kaique Brasileiro", "Content coordination + team assistance", "@kaique")]
slide(
    blob(1150, 80, 280) + blob(80, 720, 280, "g", .8) +
    '<h1 class="t" style="top:50px">Local team</h1>'
    f'<span class="pill" style="position:absolute;right:60px;top:50px">On the ground</span>'
    '<p class="big" style="position:absolute;left:60px;top:150px;width:800px;font-size:19px;line-height:1.45">'
    'A local crew that knows the city, the scene and the fans, with her all five days.</p>'
    '<div class="team">' + "".join(
        f'<div>{avatar(n, "", 120)}<small class="lbl">{r}</small><p>{h}</p></div>' for n, r, h in equipe) + '</div>'
    '<div class="box" style="left:60px;top:560px;width:1160px;background:#F2EC1A;display:flex;align-items:center;gap:24px">'
    f'{pill("Press")}<p style="font-size:16px"><b>Need local press relations?</b> We can bring in a Brazilian PR team as well.</p></div>'
    + ft("Local team", 20))

# =============================================================== 21 obrigado
slide(
    blob(1150, 30, 260) + blob(90, 700, 330, "g") + blob(640, 720, 300) +
    f'<img src="{LOGO}" style="position:absolute;left:60px;top:40px;width:230px">'
    '<h1 class="giga" style="top:220px;font-size:190px">Obrigado.</h1>'
    '<p style="position:absolute;left:62px;top:460px;font-size:17px">Meli Music · October 17, 2026 · São Paulo</p>'
    '<div class="rule" style="top:600px;width:440px;right:auto"></div>'
    '<p style="position:absolute;left:62px;top:615px;font-size:17px;font-weight:600">Kaique Brasileiro</p>'
    '<p style="position:absolute;left:62px;top:642px;font-size:13px">Digital Strategy &amp; Fan Engagement</p>'
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
/* capa */
.capa .tr{position:absolute;right:60px;top:52px;text-align:right;font-size:13.5px;font-weight:500;line-height:1.4}
.giga{position:absolute;left:55px;font-size:230px;font-weight:400;letter-spacing:-.05em;line-height:1;z-index:3}
.giga2{position:absolute;left:62px;font-size:120px;font-weight:400;letter-spacing:-.04em;line-height:1;z-index:3}
.oval{position:absolute;border-radius:50%/50%;border:1.4px solid #0B0B0C;background-size:cover;z-index:3}
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
.c2 h3{font-size:40px;font-weight:400;letter-spacing:-.035em;line-height:1}
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
.g2>div{background:#fff;border:1.4px solid #0B0B0C;border-radius:18px;padding:13px 18px;height:122px}
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
"""


def html():
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Normani × Brasil 2026</title>'
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
