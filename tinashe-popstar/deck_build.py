#!/usr/bin/env python3
"""Deck Tinashe × Brasil — semana de lançamento de POPSTAR.
Gera HTML 16:9 (1280x720) e fecha em PDF 13,333in x 7,5in.

Fotos de referência (Lula, Erika Hilton, Anitta, Paolla, Sabrina): coloque em
img/ref/<chave>.jpg e rode de novo. Sem o arquivo, o slot vira um monograma.
Textos dos tweets antigos da Tinashe: preencha TWEETS[..]["texto"].
"""
import base64, glob, math, pathlib, sys
B = pathlib.Path(__file__).parent

def uri(p):
    p = B/p
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

IMG = {k: uri(f"img/{k}.jpg") for k in ("capa-album", "noite", "vinil", "avatar")}
LOGO = uri("img/logo-black.png")
LOGO_W = uri("img/logo-white.png")
FONTES = (B/"fontes/fonts.css").read_text()

Y = "#F3EC1C"    # amarelo
G = "#12B04F"    # verde
GD = "#0A7A36"   # verde escuro (texto sobre claro)
INK = "#0B0B0C"
LAV = "#D4D7E1"  # lavanda-cinza da ref
MUT = "#5C5F68"

S = []
def slide(html, cls="", bg=""):
    S.append(f'<section class="sl {cls}" style="{bg}">{html}</section>')

def blob(x, y, r, cor, a=1.0):
    return (f'<div class="blob" style="left:{x-r}px;top:{y-r}px;width:{2*r}px;height:{2*r}px;'
            f'background:radial-gradient(circle,{cor} 0%,{cor}{int(a*0.55*255):02x} 38%,{cor}00 70%)"></div>')

def pill(t, cls=""):
    return f'<span class="pill {cls}">{t}</span>'

def rodape(n, secao, dark=False):
    return (f'<div class="rod"><span>{secao}</span><span class="rod-r">'
            f'Tinashe × Brasil · Popstar week<b>{n:02d}</b></span></div>')

def fonte(t):
    return f'<p class="fonte">{t}</p>'

# ---------- foto ou monograma ----------
def retrato(chave, nome, papel, tam=112):
    p = B/f"img/ref/{chave}.jpg"
    if p.exists():
        inner = f'<img src="{uri(f"img/ref/{chave}.jpg")}" alt="{nome}">'
    else:
        ini = "".join(w[0] for w in nome.split()[:2]).upper()
        inner = f'<span class="mono" style="font-size:{tam*0.34:.0f}px">{ini}</span>'
    return (f'<div class="ret"><div class="ret-c" style="width:{tam}px;height:{tam}px">{inner}</div>'
            f'<div class="ret-n">{nome}</div><div class="ret-p">{papel}</div></div>')

# ---------- card de tweet ----------
VERIF = ('<svg viewBox="0 0 22 22" class="vf"><path fill="#1D9BF0" d="M20.4 11c0-1.4-.8-2.6-2-3.2.4-1.3.1-2.8-.9-3.8s-2.4-1.3-3.8-.9C13.1 1.9 11.9 1 10.5 1S7.9 1.9 7.3 3.1c-1.3-.4-2.8-.1-3.8.9s-1.3 2.5-.9 3.8C1.4 8.4.6 9.6.6 11s.8 2.6 2 3.2c-.4 1.3-.1 2.8.9 3.8s2.5 1.3 3.8.9c.6 1.2 1.8 2 3.2 2s2.6-.8 3.2-2c1.3.4 2.8.1 3.8-.9s1.3-2.5.9-3.8c1.2-.6 2-1.8 2-3.2z"/>'
         '<path fill="#fff" d="M9.2 15.2 5.6 11.6l1.4-1.4 2.2 2.2 5.3-5.3 1.4 1.4z"/></svg>')

def tweet(pt, en, meta="Sep 24 · 12:00 PM BRT · 8:00 AM PT · proposed", largo=560):
    return (f'<div class="tw" style="width:{largo}px">'
            f'<div class="tw-h"><img src="{IMG["avatar"]}" class="av"><div>'
            f'<div class="tw-n">Tinashe {VERIF}</div><div class="tw-u">@Tinashe</div></div>'
            f'<svg class="xl" viewBox="0 0 24 24"><path d="M18.2 2.3h3.4l-7.4 8.4 8.7 11.5h-6.8l-5.3-7-6.1 7H1.3l7.9-9L.9 2.3h7l4.8 6.4zm-1.2 17.9h1.9L7.1 4.2H5.1z"/></svg></div>'
            f'<p class="tw-t">{pt}</p><div class="tw-m">{meta}</div>'
            f'<div class="tw-en"><span>EN</span>{en}</div></div>')

# ---------- mapa do Brasil em pontos ----------
BR = [(-51.6,4.4),(-50.0,1.8),(-49.2,0.2),(-48.5,-1.2),(-46.5,-1.0),(-44.3,-2.5),(-41.8,-2.9),(-38.5,-3.7),
      (-36.5,-5.0),(-35.2,-5.4),(-34.8,-7.1),(-35.0,-9.0),(-36.4,-10.5),(-37.5,-11.8),(-38.5,-13.0),(-39.0,-15.5),
      (-39.3,-18.0),(-40.3,-20.3),(-41.0,-22.0),(-43.2,-23.0),(-45.0,-23.6),(-46.3,-24.0),(-48.0,-25.5),(-48.6,-27.6),
      (-49.5,-29.0),(-50.5,-30.8),(-52.1,-32.2),(-53.4,-33.7),(-53.5,-32.5),(-55.5,-30.9),(-57.6,-30.2),(-56.0,-28.2),
      (-54.6,-25.6),(-54.3,-24.0),(-55.6,-22.6),(-57.8,-22.1),(-58.0,-20.0),(-57.6,-18.5),(-58.2,-17.3),(-60.2,-16.3),
      (-60.5,-13.8),(-62.5,-13.0),(-65.0,-11.9),(-65.3,-10.8),(-66.6,-9.9),(-69.5,-10.9),(-72.9,-9.0),(-73.8,-7.3),
      (-72.9,-5.2),(-70.0,-4.3),(-69.4,-1.0),(-69.8,1.0),(-67.0,2.0),(-66.9,1.2),(-64.0,1.9),(-63.4,2.2),(-64.0,4.0),
      (-60.7,5.2),(-60.0,3.0),(-58.0,1.5),(-56.5,1.9),(-54.5,2.3),(-52.9,2.2),(-51.6,4.4)]

def dentro(x, y, pol):
    c = False; j = len(pol)-1
    for i in range(len(pol)):
        xi, yi = pol[i]; xj, yj = pol[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/(yj-yi)+xi:
            c = not c
        j = i
    return c

def mapa(pinos, w=470, h=470, passo=0.72, cor="#9EA2AE"):
    lon0, lon1, lat0, lat1 = -74.5, -34.0, 6.0, -34.5
    sx = w/(lon1-lon0); sy = h/(lat0-lat1); s = min(sx, sy)
    def P(lo, la): return ((lo-lon0)*s, (lat0-la)*s)
    out = [f'<svg viewBox="0 0 {w} {h}" class="mapa">']
    la = lat0
    while la > lat1:
        lo = lon0
        while lo < lon1:
            if dentro(lo, la, BR):
                x, y = P(lo, la)
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{cor}"/>')
            lo += passo
        la -= passo
    for (lo, la, rot, sub, lado, dy) in pinos:
        x, y = P(lo, la)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="{Y}" opacity=".55"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{G}" stroke="{INK}" stroke-width="1.5"/>')
        tx = x+16 if lado == "d" else x-16
        anc = "start" if lado == "d" else "end"
        out.append(f'<text x="{tx:.1f}" y="{y-3+dy:.1f}" text-anchor="{anc}" class="m-r">{rot}</text>'
                   f'<text x="{tx:.1f}" y="{y+12+dy:.1f}" text-anchor="{anc}" class="m-s">{sub}</text>')
    out.append('</svg>')
    return "".join(out)

# ============================================================
# 01 CAPA
slide(f"""
{blob(170,720,330,G)}{blob(560,700,300,Y)}{blob(1100,-40,260,Y,.8)}
<div class="capa-top"><img src="{LOGO}" class="logo"><span class="capa-sub">A Brazil-first activation<br>for Popstar release week</span></div>
<div class="capa-rule"></div>
<h1 class="capa-h">Popstar<br><span>× Brasil</span></h1>
{pill("Sep 2026","capa-pill")}
<div class="capa-img"><img src="{IMG['capa-album']}"></div>
<div class="capa-rod">Proposal for Tinashe · X / Twitter · Brazilian fandom</div>
""", bg=f"background:{LAV}")

# 02 INDEX
idx = [("01","Her story with Brazil isn't new"),("02","Brazilian superfans, in numbers"),
       ("03","Cases: Beyoncé, Gaga, Madonna"),("04","Case: Bruno Mars"),("05","Cultural codes"),
       ("06","Brazil, right now"),("07","Idea #1 · Idea #2"),("08","My bet")]
slide(f"""
<div class="half-l"></div><div class="half-r" style="background:linear-gradient(160deg,{Y} 0%,{Y} 45%,#9BDA3F 75%,{G} 100%)"></div>
{blob(640,360,260,Y)}
<div class="idx-top">{pill("INDEX")}<span class="mini">Tinashe × Brasil</span></div>
<div class="idx-l">
  <p class="mini">One tweet. One week. The most engaged fandom on the internet.</p>
  <p class="idx-note">Popstar, 8th studio album<br>Out <b>September 25, 2026</b><br>Nice Life · Atlantic · Tinashe Music · 16 tracks</p>
</div>
<ol class="idx-r">{''.join(f'<li><span>{n}</span>{t}</li>' for n,t in idx)}</ol>
<div class="rule" style="left:700px;right:60px;top:612px"></div>
<div class="idx-f"><span>Receipts</span><span>Data</span><span>Codes</span><span>Tweets</span><span>$0</span></div>
""", bg=f"background:{LAV}")

# 03 OVERVIEW
slide(f"""
<div class="ov-head"><div><span class="ov-s">Executive</span>{pill("INDEX")}</div><h1 class="ov-h">Overview</h1></div>
<div class="ov-pill">
  <div class="ov-l"><div class="big">1 tweet</div><div class="cap">in Portuguese, in release week</div>
     <div class="ov-row"><span class="cap">Paid media</span><b>$0</b></div></div>
  <div class="ov-sep"></div>
  <div class="ov-r">
    <div><b>16 yrs</b><span>talking to Brazil<br>(2010 → 2026)</span></div>
    <div><b>3</b><span>shows in Brazil<br>(2015, 2023)</span></div>
    <div><b>150M</b><span>social media users<br>in Brazil</span></div>
    <div><b>#8</b><span>music market<br>in the world</span></div>
  </div>
  <div class="ov-bot"><span class="cap">Popstar out</span><b>Sep 25</b><span class="cap">Brazil votes</span><b>Oct 4</b></div>
</div>
<p class="ov-txt">Speak to Brazil in its own internet language during Popstar week. Turn the most online fandom
in the world into organic reach, press coverage and new listeners, without spending a cent.</p>
<div class="ov-post"><div class="ch-t">Posting time</div>
  <div class="ov-pt"><div><b>Sep 24</b><span>Thursday</span></div><div><b>12 PM</b><span>Brazil (BRT)</span></div><div><b>8 AM</b><span>Los Angeles (PT)</span></div></div>
  <p>Midday in Brazil gives the tweet a full day to echo across the media.</p></div>
{fonte("Sources: DataReportal Digital 2026 Brazil; IFPI Global Music Report 2026; setlist.fm; The FADER (Jul 2026).")}
""", bg="background:#fff")

# 04 HISTÓRIA — statement
slide(f"""
<div class="st-img"><img src="{IMG['noite']}"></div>
<div class="st-r" style="background:linear-gradient(180deg,{LAV} 0%,#E9EB9A 45%,{Y} 70%,#B9E04A 100%)"></div>
{blob(1000,640,260,G,.9)}
<div class="st-top">{pill("INDEX")}<span class="mini">01 · History</span></div>
<h1 class="st-h">Her story with Brazil<br>isn't new.</h1>
<p class="st-p">Tinashe has been talking to Brazilian fans since 2010, years before her first album,
and has already played for them twice. Popstar week is not an introduction. It's a reunion.</p>
<div class="st-num"><b>2010</b><span>first tweets<br>to Brazil</span></div>
{rodape(4,"Her story with Brazil")}
""", cls="st", bg=f"background:{LAV}")

# 05 TIMELINE
marcos = [
  ("Nov 29, 2010","Early tweets","Still pre-debut, already replying to Brazil and noting she has a lot of Brazilian followers.",False),
  ("Sep 27-28, 2015","Arriving","Tweets from Brazil while on the road with Katy Perry’s Prismatic World Tour.",False),
  ("Sep 29, 2015","Curitiba","Opens for Katy Perry at Pedreira Paulo Leminski. 15,000 people, 40-min set, covers “Lean On”.",True),
  ("Mar 5, 2023","São Paulo","Headliner at Festival GRLS!, an all-women lineup, on the 333 tour.",True),
  ("Mar 6, 2023","São Paulo","Club show at Zig Studio, the same Zig Lily Allen would tweet about in 2026.",True),
  ("Mar 6, 2023","TikTok","“Brazil, te amoooo 💚🧡”: a thank-you to Brazil, in Portuguese, the day after GRLS!.",False),
  ("Sep 25, 2026","Popstar","Release week. The next chapter.",False),
]
n = len(marcos); x0, x1 = 70, 1210
pts = "".join(
  f'<div class="tl-i {"up" if i%2==0 else "dn"} {"ini" if i==0 else "fim" if i==n-1 else ""}" style="left:{x0+(x1-x0)*i/(n-1):.0f}px">'
  f'<div class="tl-d {"show" if sh else ""}"></div>'
  f'<div class="tl-box"><div class="tl-date">{d}</div><div class="tl-t">{t}{" "+pill("LIVE","pl-s") if sh else ""}</div><div class="tl-x">{x}</div></div></div>'
  for i,(d,t,x,sh) in enumerate(marcos))
slide(f"""
{blob(1180,90,230,Y)}{blob(640,800,260,G,.7)}
<div class="hd"><h2>Sixteen years<br>of Brazil</h2>{pill("TIMELINE")}</div>
<div class="tl-line"></div>
{pts}
<div class="tl-leg"><span class="lg-d show"></span>Live in Brazil <span class="lg-d"></span>Online moment</div>
{fonte("Sources: setlist.fm; TMDQA! (Sep 30, 2015 · Mar 4, 2023); @Tinashe on X and TikTok; The FADER (Jul 2026).")}
{rodape(5,"Timeline")}
""", bg=f"background:{LAV}")

# 06 RECIBOS — tweets antigos
TWEETS = [
  {"id":"9360504220819456","data":"Nov 29, 2010 · 7:38 PM BRT","tag":"On her Brazilian followers","texto":""},
  {"id":"9360864784154624","data":"Nov 29, 2010 · 7:39 PM BRT","tag":"Replying to Brazil","texto":""},
  {"id":"648273929853870080","data":"Sep 27, 2015 · 8:12 PM BRT","tag":"Prismatic tour · Brazil leg","texto":""},
  {"id":"648506655798198272","data":"Sep 28, 2015 · 11:36 AM BRT","tag":"Prismatic tour · Brazil leg","texto":""},
  {"id":"648539373122768896","data":"Sep 28, 2015 · 1:46 PM BRT","tag":"Prismatic tour · Brazil leg","texto":""},
]
def recibo(t, dest=False):
    corpo = (f'<p class="rc-q"><span>context</span>{t["tag"]}</p>'
             + (f'<p class="rc-t">{t["texto"]}</p>' if t["texto"] else '<p class="rc-o">Open the original post on X ↗</p>'))
    return (f'<div class="rc {"rc-dest" if dest else ""}"><div class="tw-h"><img src="{IMG["avatar"]}" class="av av-s"><div>'
            f'<div class="tw-n">Tinashe {VERIF}</div><div class="tw-u">@Tinashe · {t["data"]}</div></div></div>'
            f'{corpo}<div class="rc-l">x.com/Tinashe/status/{t["id"]}</div></div>')
slide(f"""
{blob(1150,650,260,Y)}{blob(980,720,200,G,.8)}
<div class="hd"><h2>The receipts</h2>{pill("ON X")}</div>
<p class="lead">Before “Nasty”, before “2 On”, before the first album: Tinashe was already talking to Brazil,
including telling fans she has a lot of followers from Brazil.</p>
<div class="rc-grid">{recibo(TWEETS[0],True)}{recibo(TWEETS[1])}{recibo(TWEETS[2])}{recibo(TWEETS[3])}{recibo(TWEETS[4])}
<div class="rc rc-fan"><div class="big-s">12+ yrs</div><div class="cap">@tinashebr, the Brazilian fan hub on X, running since 2014, calls her “a POPSTAR” in its bio.</div></div></div>
{rodape(6,"Receipts")}
""", bg=f"background:{LAV}")

# 07 SUPERFÃS — dados
def barras(itens, w=520, alt=30, passo=52, maxv=None, rotw=170, fmt=str):
    maxv = maxv or max(v for _,v,_ in itens)
    h = passo*len(itens)
    o = [f'<svg viewBox="0 0 {rotw+w+90} {h}" class="g">']
    for i,(r,v,c) in enumerate(itens):
        y = i*passo; ww = v/maxv*w
        o.append(f'<text x="{rotw-14}" y="{y+alt*.66}" text-anchor="end" class="b-r">{r}</text>'
                 f'<rect x="{rotw}" y="{y}" width="{ww:.1f}" height="{alt}" rx="{alt/2}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
                 f'<text x="{rotw+ww+12}" y="{y+alt*.68}" class="b-v">{fmt(v)}</text>')
    o.append('</svg>'); return "".join(o)
tempo = barras([("Brazil",217,G),("World average",141,"#fff")], w=430, fmt=lambda v:f"{v//60}h{v%60:02d}m")
slide(f"""
<div class="bg-y" style="background:linear-gradient(120deg,{Y} 0%,{Y} 55%,#A6DC3C 80%,{G} 100%)"></div>
<div class="hd"><h2>Brazilian superfans,<br>in numbers</h2>{pill("DATA")}</div>
<div class="sf-grid">
  <div class="sf-k"><b>150M</b><span>social media users, 70.4% of the population</span></div>
  <div class="sf-k"><b>+14.1%</b><span>recorded-music growth in 2025, 16th straight year up</span></div>
  <div class="sf-k"><b>#8</b><span>music market in the world, up from #9 (IFPI 2026)</span></div>
  <div class="sf-k"><b>~83%</b><span>of Brazil’s music revenue comes from streaming</span></div>
</div>
<div class="sf-chart"><div class="ch-t">Daily time on social media</div>{tempo}
  <p class="ch-n">Brazilians spend <b>+54%</b> more time on social than the global average.</p></div>
<div class="sf-side">
  <div class="ch-t">Why superfans matter</div>
  <div class="sf-row"><b>20%</b><span>of listeners are superfans (Luminate / Goldman Sachs)</span></div>
  <div class="sf-row"><b>+80%</b><span>more spent per month than the average listener</span></div>
  <div class="sf-row"><b>2×</b><span>spend on physical products: vinyl, CDs</span></div>
  <div class="sf-row"><b>+17.1%</b><span>Latin America: fastest-growing region in the world</span></div>
</div>
{fonte("Sources: DataReportal Digital 2026 Brazil; IFPI Global Music Report 2026; Pro-Música Brasil (Mar 2026); Luminate 2024-25; Goldman Sachs “Music in the Air”.")}
{rodape(7,"Superfans")}
""")

# 08 CASES — mapa
publico = barras([("Lady Gaga ’25",2.1,G),("Madonna ’24",1.6,Y)], w=250, alt=26, passo=44, rotw=120, fmt=lambda v:f"{v}M")
slide(f"""
{blob(300,400,300,Y,.9)}
<div class="hd"><h2>When pop shows up<br>for Brazil</h2>{pill("CASES")}</div>
<div class="cs-map">{mapa([(-38.5,-12.97,"Salvador","Beyoncé · Dec 2023","e",0),(-43.18,-22.97,"Rio","Madonna ’24 · Gaga ’25","d",0),(-46.63,-23.55,"São Paulo","Tinashe · 2023","e",-16),(-49.27,-25.43,"Curitiba","Tinashe · 2015","e",16)], w=400, h=400)}</div>
<div class="cs-cards">
  <div class="cs"><div class="cs-h"><b>Beyoncé</b>{pill("SALVADOR · DEC 21, 2023","pl-s")}</div>
    <p>A surprise 5-minute appearance for ~4,000 fans at the Brazilian launch of the Renaissance film. The only one of its kind.
    Wrapped in the Bahia flag: <i>“Você é única, Bahia.”</i></p>
    <div class="cs-n"><b>1M+</b><span>posts, the most-discussed topic on Brazilian social media</span></div></div>
  <div class="cs"><div class="cs-h"><b>Lady Gaga</b>{pill("COPACABANA · MAY 3, 2025","pl-s")}</div>
    <p>Free show, “Todo Mundo no Rio”. Largest audience ever for a female artist. Brazil is now her #2 country on Spotify.</p>
    <div class="cs-nn"><div><b>2.1M</b><span>people</span></div><div><b>+60%</b><span>Spotify streams in 7 days</span></div><div><b>4.2M</b><span>posts in 7 days</span></div><div><b>34.5M</b><span>TV viewers</span></div></div></div>
  <div class="cs cs-g"><div class="ch-t">Copacabana, attendance</div>{publico}</div>
</div>
{fonte("Sources: CNN Brasil; Meio & Mensagem (Dec 2023); Riotur / Prefeitura do Rio; Billboard Brasil; Deezer Newsroom (May 2025); Rolling Stone (May 2024).")}
{rodape(8,"Cases")}
""", bg=f"background:{LAV}")

# 09 BRUNO MARS
def colunas(vals, w=520, h=250):
    maxv = 36
    bw = 110; gap = (w-bw*len(vals))/(len(vals)+1)
    o = [f'<svg viewBox="0 0 {w} {h+50}" class="g">']
    for i,(r,v,c,lab) in enumerate(vals):
        x = gap+i*(bw+gap); bh = v/maxv*h
        o.append(f'<rect x="{x:.1f}" y="{h-bh:.1f}" width="{bw}" height="{bh:.1f}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
                 f'<text x="{x+bw/2:.1f}" y="{h-bh+34:.1f}" text-anchor="middle" class="c-v">{lab}</text>'
                 f'<text x="{x+bw/2:.1f}" y="{h+26}" text-anchor="middle" class="c-r">{r}</text>')
    o.append(f'<line x1="0" y1="{h}" x2="{w}" y2="{h}" stroke="{INK}" stroke-width="1.2"/></svg>')
    return "".join(o)
bm = colunas([("Before The Town ’23",29,"#fff","~29M"),("Mar 2024",33,Y,"33M+"),("Growth",4,G,"")], w=470, h=240)
slide(f"""
<div class="bg-y" style="background:linear-gradient(200deg,{Y} 0%,{Y} 50%,#A6DC3C 78%,{G} 100%)"></div>
<div class="hd"><h2>Case: Bruno Mars</h2>{pill("ROLLOUT MADE FOR BRAZIL")}</div>
<p class="lead lead-w">He didn’t just tour Brazil. He built a Brazil-specific rollout, in Portuguese, with local references. Brazil answered.</p>
<div class="bm-chart"><div class="ch-t">Instagram followers</div>{bm}<div class="bm-plus">+4M</div></div>
<div class="bm-k">
  <div><b>50M+</b><span>views on a Brazilian video, his most-watched content at the time</span></div>
  <div><b>358M</b><span>potential reach from the 2024 tour, in just over a month</span></div>
  <div><b>+243%</b><span>Deezer streams during his Brazil run</span></div>
</div>
<div class="bm-single"><div class="bm-st">{pill("SINGLE MADE FOR BRAZIL")}<b>“Bonde do Brunão”</b></div>
  <div class="bm-n"><div><b>13M+</b><span>likes</span></div><div><b>2.3M</b><span>shares</span></div><div><b>687K</b><span>comments</span></div></div></div>
{fonte("Sources: Instagram @brunomars; Deezer; tour social listening (2023-2024).")}
{rodape(9,"Bruno Mars")}
""")

# 10 CÓDIGOS CULTURAIS — Lily Allen
codes = [("Zig","A legendary gay club in São Paulo that became the city’s point of reference. <strong>Tinashe played there in 2023.</strong>"),
         ("Casa da Vita","A nod to <i>Vita’s House</i>, the album by Vita, a trans artist whose tracks took over clubs and the underground."),
         ("Patixa","A national meme: an “influencer” who never made content herself. Every video of her online was made by other people.")]
slide(f"""
{blob(80,80,220,G,.9)}{blob(1220,700,260,Y)}
<div class="cc-top">{pill("CULTURAL CODES")}<span class="mini">05</span></div>
<h1 class="cc-h">The only way to break into the Brazilian market is through <span class="hl">local cultural codes.</span></h1>
<p class="cc-sub">Most international artists ignore this. The ones who don’t get adopted.</p>
<div class="cc-tw"><div class="tw-h"><img src="{uri('img/lily.jpg')}" class="av av-s"><div><div class="tw-n">Lily Allen {VERIF}</div><div class="tw-u">@lilyallen · May 11, 2026</div></div></div>
<p class="tw-t">Quero dançar com os gays na <u>Zig</u>, visitar a <u>casa da Vita</u> e conhecer a <u>Patixa</u></p>
<div class="tw-en"><span>EN</span>I want to dance with the gays at Zig, visit Vita’s house and meet Patixa</div></div>
<div class="cc-grid">{''.join(f'<div class="cc"><div class="cc-n">{i+1:02d}</div><b>{c}</b><p>{d}</p></div>' for i,(c,d) in enumerate(codes))}</div>
<p class="cc-f">Three references only a Brazilian on the internet would get. Result: it went viral across Brazilian stan Twitter, months ahead of her Primavera Sound São Paulo date (Dec 2026).</p>
{rodape(10,"Cultural codes")}
""", bg="background:#fff")

# 11 CONTEXTO
slide(f"""
{blob(1150,120,260,Y)}{blob(1250,560,220,G,.85)}
<div class="hd"><h2>Brazil, right now</h2>{pill("CONTEXT")}</div>
<div class="cx-l">
  <p class="cx-big">It’s election season, and in Brazil, politicians are <span class="hl">pop culture.</span></p>
  <p class="cx-p">First round on <b>October 4</b>, nine days after Popstar drops. The race is <b>Lula</b>, the president and the
  “father” figure of Brazil’s minorities, against <b>Flávio Bolsonaro</b>, son of Jair Bolsonaro, Brazil’s Trump.
  Polls are tight and the whole country is online talking about it.</p>
  <p class="cx-p">Next to Lula stands <b>Erika Hilton</b>, a trans federal deputy and a genuine internet diva, on issues
  that match Tinashe’s values and her fans’.</p>
</div>
<div class="cx-r">
  <div class="ch-t">Who stands with Lula</div>
  <div class="cx-tags"><span>LGBTQIA+</span><span>Black Brazilians</span><span>Women</span><span>Workers</span><span>Young people</span></div>
  <div class="ch-t" style="margin-top:22px">Pop artists in the conversation</div>
  <div class="cx-tags cx-y"><span>Anitta</span><span>Ludmilla</span><span>IZA</span></div>
  <div class="venn"><div class="v1">Tinashe’s<br>values</div><div class="v2">Her Brazilian<br>fandom</div><div class="v3">Lula &amp;<br>Erika’s base</div><div class="vc">overlap</div></div>
</div>
<p class="cx-note">Not an electoral campaign. It’s aligning the artist’s ideals with her fandom’s, in a country starved for attention from international artists.</p>
{fonte("Sources: TSE calendar; Datafolha / Quaest / PoderData (Sep 2026); Al Jazeera (Dec 2025).")}
{rodape(11,"Context")}
""", bg=f"background:{LAV}")

# 12 IDEIA 1
t1 = tweet("brasil, vcs não saem da minha cabeça e já que estamos na semana do lançamento de popstar, quem é um popstar pra vocês por aí? nesse momento pra mim são lula e erika hilton.  quero mostrar minhas novas músicas pra eles.",
           "brazil, you guys have been on my mind nonstop. and since we’re in popstar release week, who’s a popstar to you over there? right now, for me, it’s lula and erika hilton. i wanna show them my new music.", largo=590)
slide(f"""
<div class="bg-y" style="background:linear-gradient(135deg,{LAV} 0%,{LAV} 38%,#E4EA8C 60%,{Y} 78%,{G} 100%)"></div>
<div class="id-top">{pill("IDEA #1")}<span class="mini">The popstars of Brazil</span></div>
<h1 class="id-h">Idea<br>#1</h1>
<p class="id-p">Ask Brazil who its popstars are, then name the two biggest ones on the internet right now. Subtle on the surface, massive and organic underneath.</p>
<div class="id-tw">{t1}</div>
<div class="id-ret">{retrato("lula","Lula","President of Brazil",124)}{retrato("erika","Erika Hilton","Federal deputy",124)}</div>
<div class="id-why"><div><b>Both</b><span>are extremely online and likely to reply</span></div><div><b>Beyond music</b><span>reaches people who don’t follow the release</span></div></div>
{rodape(12,"Idea #1")}
""")

# 13 IDEIA 2
t2 = tweet("brasil, vcs não saem da minha cabeça e já que estamos na semana do lançamento de popstar, quem é uma popstar pra vocês por aí? o que elas estão fazendo? ouvi dizer que anitta agora é rainha da grande rio, paolla oliveira na imperatriz? sabrina na vila isabel. eu queria estar no próximo carnaval também. estou com fomo",
           "brazil, you guys have been on my mind nonstop. and since we’re in popstar release week, who’s a popstar to you over there right now? what are the girls up to? i heard anitta is queen of grande rio now, and paolla oliveira is with imperatriz? sabrina at vila isabel. i wanna be at the next carnival too. major fomo.", largo=590)
slide(f"""
<div class="bg-y" style="background:linear-gradient(135deg,{LAV} 0%,{LAV} 38%,#D8EE9A 60%,{G} 82%,{Y} 100%)"></div>
<div class="id-top">{pill("IDEA #2")}<span class="mini">Carnival queens</span></div>
<h1 class="id-h">Idea<br>#2</h1>
<p class="id-p">Link Popstar to Brazil’s biggest cultural moment. Carnival is only next year, but samba schools are crowning their queens now, and they pick popstars.</p>
<div class="id-tw">{t2}</div>
<div class="id-ret id-ret3">{retrato("anitta","Anitta","Grande Rio",88)}{retrato("paolla","Paolla Oliveira","Imperatriz",88)}{retrato("sabrina","Sabrina Sato","Vila Isabel",88)}</div>
<div class="id-why"><div><b>Lower risk</b><span>pure culture, zero politics</span></div><div><b>Lower impact</b><span>stays inside the pop bubble</span></div></div>
{rodape(13,"Idea #2")}
""")

# 14 MINHA APOSTA
passos = [("T0","The tweet","Tinashe posts Idea #1, in Portuguese."),
          ("T+15min","Pop pages","We fire it to Brazil’s biggest pop & entertainment pages."),
          ("T+2h","Press","News, politics and culture outlets pick it up."),
          ("T+24h","The reply","Lula and/or Erika answer. The story restarts.")]
comp = [("Originality","●●●","●●○"),("Reach beyond music","●●●","●○○"),("Press potential","●●●","●●○"),("Reply potential","●●●","●●○"),("Risk","●●○","●○○")]
slide(f"""
{blob(1180,120,280,G,.85)}{blob(980,40,200,Y)}
<div class="hd"><h2>My bet: <span class="hl">Idea #1</span></h2>{pill("MINHA APOSTA")}</div>
<p class="lead">It’s more original. It reaches people who don’t necessarily know about the release or follow music.
And after the tweet, they will. Right after posting, we push it to the big pop and entertainment pages.</p>
<div class="fl">{''.join(f'<div class="fl-i"><div class="fl-t">{t}</div><b>{a}</b><p>{d}</p></div>' + ('<div class="fl-a">→</div>' if i<3 else '') for i,(t,a,d) in enumerate(passos))}</div>
<table class="cmp"><tr><th></th><th>Idea #1 · Lula &amp; Erika</th><th>Idea #2 · Carnival</th></tr>
{''.join(f'<tr><td>{r}</td><td class="d1">{a}</td><td>{b}</td></tr>' for r,a,b in comp)}</table>
{rodape(14,"My bet")}
""", bg=f"background:{LAV}")

# 15 INVESTIMENTO
slide(f"""
<div class="bg-y" style="background:radial-gradient(circle at 25% 110%,{G} 0%,#7FCF3F 25%,{Y} 55%,{Y} 100%)"></div>
<div class="inv-top">{pill("INDEX")}<span class="mini">Investment</span></div>
<p class="inv-s">INVESTMENT:</p>
<h1 class="inv-h">$0</h1>
<p class="inv-p">One tweet from Tinashe’s own account.<br>No paid media. No boosting. 100% organic.</p>
""")

# 16 OBRIGADO
slide(f"""
{blob(200,720,340,G)}{blob(640,760,300,Y)}{blob(1150,-20,240,Y,.8)}
<img src="{LOGO}" class="ob-logo">
<h1 class="ob-h">Obrigado.</h1>
<p class="ob-p">Popstar · September 25, 2026</p>
<div class="ob-sig"><b>Kaique Brasileiro</b><span>Digital Strategy &amp; Fan Engagement</span></div>
<div class="ob-img"><img src="{IMG['vinil']}"></div>
""", bg=f"background:{LAV}")

# ============================================================
CSS = f"""
@page{{size:13.333in 7.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#999}}
body{{font-family:Inter,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sl{{width:1280px;height:720px;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff}}
.sl>*{{position:absolute}}
.blob{{border-radius:50%;pointer-events:none}}
.pill{{display:inline-block;border:1.4px solid {INK};border-radius:999px;padding:3px 14px 2px;font-size:11px;
  font-weight:500;letter-spacing:.02em;background:transparent;white-space:nowrap}}
.pl-s{{font-size:9px;padding:2px 9px 1px;vertical-align:middle}}
.mini{{font-size:12px;font-weight:500}}
.rule{{height:1.4px;background:{INK}}}
.rod{{left:60px;right:60px;bottom:26px;display:flex;justify-content:space-between;font-size:10.5px;font-weight:500}}
.rod b{{margin-left:14px;border:1.4px solid {INK};border-radius:999px;padding:1px 10px;font-weight:600}}
.fonte{{left:60px;bottom:52px;font-size:9.5px;color:{MUT};max-width:900px}}
.hd{{left:60px;top:50px;right:60px;display:flex;justify-content:space-between;align-items:flex-start}}
.hd h2{{font-size:54px;font-weight:400;letter-spacing:-.045em;line-height:.98}}
.lead{{left:60px;top:175px;width:640px;font-size:17px;line-height:1.4;font-weight:400}}
.hl{{background:linear-gradient(90deg,{Y},#B7E447);padding:0 6px;border-radius:6px}}
.ch-t{{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px}}
.cap{{font-size:11.5px;font-weight:500}}
.bg-y{{inset:0}}
.g{{width:100%;display:block}}
.b-r{{font:600 14px Inter;fill:{INK}}} .b-v{{font:600 18px Inter;fill:{INK};letter-spacing:-.02em}}
.c-v{{font:500 26px Inter;fill:{INK};letter-spacing:-.04em}} .c-r{{font:500 12px Inter;fill:{INK}}}

/* capa */
.capa-top{{left:60px;top:48px;right:60px;display:flex;justify-content:space-between;align-items:center}}
.logo{{height:44px}}
.capa-sub{{font-size:12px;font-weight:500;text-align:right;line-height:1.3}}
.capa-rule{{left:60px;right:60px;top:118px;height:1.4px;background:{INK}}}
.capa-h{{left:52px;top:160px;font-size:236px;font-weight:400;letter-spacing:-.065em;line-height:.8}}
.capa-h span{{font-size:118px;letter-spacing:-.05em;display:inline-block;margin-left:8px;margin-top:28px}}
.capa-pill{{left:470px;top:500px;background:{LAV}}}
.capa-img{{right:60px;top:160px;width:300px;height:390px;border-radius:160px;overflow:hidden;border:1.4px solid {INK}}}
.capa-img img{{width:100%;height:100%;object-fit:cover;object-position:62% 40%}}
.capa-rod{{left:60px;bottom:40px;font-size:12px;font-weight:500}}

/* index */
.half-l{{left:0;top:0;width:640px;height:720px;background:{LAV}}}
.half-r{{left:640px;top:0;width:640px;height:720px}}
.idx-top{{left:60px;top:50px;display:flex;gap:24px;align-items:center}}
.idx-l{{left:60px;top:250px;width:470px}}
.idx-l .mini{{font-size:22px;font-weight:400;letter-spacing:-.03em;line-height:1.2}}
.idx-note{{margin-top:30px;font-size:13px;line-height:1.6}}
.idx-r{{left:700px;top:88px;list-style:none}}
.idx-r li{{font-size:32px;letter-spacing:-.04em;line-height:1.5;font-weight:400}}
.idx-r li span{{font-size:12px;font-weight:600;letter-spacing:0;display:inline-block;width:40px;vertical-align:middle}}
.idx-f{{left:700px;right:60px;top:632px;display:flex;justify-content:space-between;font-size:12px;font-weight:500}}

/* overview */
.ov-head{{left:60px;top:40px;right:60px;display:flex;align-items:flex-end;gap:28px}}
.ov-s{{font-size:30px;letter-spacing:-.04em;display:block;margin-bottom:10px}}
.ov-head .pill{{background:{Y}}}
.ov-h{{font-size:150px;font-weight:400;letter-spacing:-.065em;line-height:.85}}
.ov-pill{{left:40px;right:40px;top:215px;height:300px;border:1.4px solid {INK};border-radius:170px;
  background:linear-gradient(90deg,{G} 0%,#8FD63E 30%,{Y} 60%,#FBF8C9 88%,#fff 100%)}}
.ov-pill>*{{position:absolute}}
.ov-l{{left:100px;top:52px}}
.big{{font-size:84px;letter-spacing:-.06em;line-height:1}}
.ov-l .cap{{display:block;margin-top:8px}}
.ov-row{{margin-top:38px;display:flex;gap:40px;align-items:baseline}}
.ov-row b{{font-size:30px;font-weight:500;letter-spacing:-.04em}}
.ov-sep{{left:500px;top:60px;width:1.4px;height:180px;background:{INK}}}
.ov-r{{left:560px;top:62px;display:flex;gap:44px}}
.ov-r b{{display:block;font-size:40px;font-weight:500;letter-spacing:-.05em}}
.ov-r span{{font-size:11.5px;font-weight:500;line-height:1.3}}
.ov-bot{{left:560px;top:190px;display:flex;gap:16px;align-items:baseline}}
.ov-bot b{{font-size:34px;letter-spacing:-.04em;font-weight:500;margin-right:34px}}
.ov-txt{{left:60px;top:548px;width:560px;font-size:17px;line-height:1.4}}
.ov-post{{left:680px;right:60px;top:535px;border:1.4px solid {INK};border-radius:22px;padding:14px 22px;background:linear-gradient(90deg,#fff 30%,{Y})}}
.ov-post .ch-t{{margin-bottom:4px}}
.ov-pt{{display:flex;gap:34px}}
.ov-pt b{{display:block;font-size:34px;font-weight:500;letter-spacing:-.045em;line-height:1.05}}
.ov-pt span{{font-size:11px;font-weight:500}}
.ov-post p{{font-size:12px;margin-top:6px;font-weight:500}}

/* statement */
.st-img{{left:0;top:0;width:520px;height:720px}}
.st-img img{{width:100%;height:100%;object-fit:cover}}
.st-r{{left:520px;top:0;width:760px;height:720px}}
.st-top{{left:560px;top:50px;display:flex;gap:24px;align-items:center}}
.st-h{{left:560px;top:150px;font-size:76px;font-weight:400;letter-spacing:-.055em;line-height:.98}}
.st-p{{left:564px;top:370px;width:520px;font-size:18px;line-height:1.45}}
.st-num{{left:564px;top:520px;display:flex;align-items:flex-end;gap:16px}}
.st-num b{{font-size:96px;font-weight:400;letter-spacing:-.06em;line-height:.8}}
.st-num span{{font-size:12px;font-weight:500}}
.st .rod{{left:560px}}

/* timeline */
.tl-line{{left:60px;right:60px;top:410px;height:1.4px;background:{INK}}}
.tl-i{{top:410px;width:0}}
.tl-d{{position:absolute;left:-8px;top:-8px;width:16px;height:16px;border-radius:50%;background:{LAV};border:1.4px solid {INK}}}
.tl-d.show{{background:{G};width:22px;height:22px;left:-11px;top:-11px;box-shadow:0 0 0 8px {Y}88}}
.tl-box{{position:absolute;left:-80px;width:170px}}
.tl-i.up .tl-box{{bottom:24px}} .tl-i.dn .tl-box{{top:26px}}
.tl-i.ini .tl-box{{left:-10px}} .tl-i.fim .tl-box{{left:-160px;text-align:right}}
.tl-date{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}}
.tl-t{{font-size:24px;letter-spacing:-.04em;margin:4px 0 6px}}
.tl-x{{font-size:11.5px;line-height:1.4}}
.tl-leg{{right:60px;top:170px;font-size:11px;font-weight:500;display:flex;gap:8px;align-items:center}}
.lg-d{{width:12px;height:12px;border-radius:50%;border:1.4px solid {INK};background:{LAV};display:inline-block;margin-left:10px}}
.lg-d.show{{background:{G}}}

/* recibos */
.rc-grid{{left:60px;right:60px;top:250px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.rc{{background:#fff;border:1.4px solid {INK};border-radius:18px;padding:16px 18px;min-height:150px;position:relative}}
.rc-dest{{background:linear-gradient(135deg,#fff 30%,{Y})}}
.rc-t{{font-size:14px;margin-top:4px;line-height:1.35}}
.rc-q{{font-size:13px;letter-spacing:-.01em;margin-top:10px;color:{GD};font-weight:500}}
.rc-q span{{display:block;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:{MUT};font-weight:600;margin-bottom:2px}}
.rc-o{{font-size:11px;color:{MUT};margin-top:4px}}
.rc-l{{margin-top:10px;font-size:10px;color:{MUT}}}
.rc-fan{{background:{G};color:{INK}}}
.big-s{{font-size:52px;letter-spacing:-.05em;line-height:1}}
.rc-fan .cap{{margin-top:10px;display:block;line-height:1.35}}

/* tweet */
.tw{{background:#fff;border:1.4px solid {INK};border-radius:22px;padding:20px 24px 18px;position:relative}}
.tw-h{{display:flex;gap:10px;align-items:center}}
.av{{width:44px;height:44px;border-radius:50%;object-fit:cover}}
.av-s{{width:36px;height:36px}}
.av-l{{background:{INK};color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600}}
.tw-n{{font-size:15px;font-weight:700;display:flex;align-items:center;gap:4px}}
.vf{{width:17px;height:17px}}
.tw-u{{font-size:13px;color:{MUT}}}
.xl{{position:absolute;right:22px;top:22px;width:20px;height:20px}}
.tw-t{{font-size:19px;line-height:1.36;margin-top:12px;letter-spacing:-.005em}}
.tw-m{{font-size:12px;color:{MUT};margin-top:12px;padding-bottom:12px;border-bottom:1px solid #ddd}}
.tw-en{{font-size:12.5px;line-height:1.45;color:#44474F;margin-top:10px}}
.tw-en span{{font-size:9px;font-weight:700;border:1.2px solid #44474F;border-radius:999px;padding:1px 6px;margin-right:8px;vertical-align:1px}}

/* superfãs */
.sf-grid{{left:60px;right:60px;top:200px;display:grid;grid-template-columns:repeat(4,1fr);border-top:1.4px solid {INK}}}
.sf-k{{padding:16px 20px 0 0}}
.sf-k b{{display:block;font-size:58px;font-weight:400;letter-spacing:-.06em;line-height:1}}
.sf-k span{{display:block;font-size:12px;font-weight:500;margin-top:8px;max-width:220px;line-height:1.35}}
.sf-chart{{left:60px;top:390px;width:600px;background:#fff;border:1.4px solid {INK};border-radius:22px;padding:20px 24px}}
.ch-n{{font-size:13px;margin-top:4px}}
.sf-side{{left:700px;right:60px;top:390px}}
.sf-row{{display:flex;gap:18px;align-items:baseline;border-bottom:1.4px solid {INK};padding:7px 0}}
.sf-row b{{font-size:30px;font-weight:500;letter-spacing:-.05em;width:108px;flex:none}}
.sf-row span{{font-size:12.5px;font-weight:500}}

/* cases */
.cs-map{{left:50px;top:220px;width:400px}}
.mapa{{width:100%;overflow:visible}}
.m-r,.m-s{{paint-order:stroke;stroke:{LAV};stroke-width:4px;stroke-linejoin:round}}
.m-r{{font:600 13px Inter;fill:{INK}}} .m-s{{font:500 10.5px Inter;fill:{INK}}}
.cs-cards{{left:500px;right:60px;top:150px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.cs{{background:#fff;border:1.4px solid {INK};border-radius:20px;padding:18px 20px}}
.cs-h{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}}
.cs-h b{{font-size:26px;font-weight:500;letter-spacing:-.04em}}
.cs p{{font-size:12.5px;line-height:1.45}}
.cs-n{{margin-top:14px;display:flex;gap:12px;align-items:center}}
.cs-n b{{font-size:40px;font-weight:400;letter-spacing:-.05em}}
.cs-n span{{font-size:11.5px;font-weight:500}}
.cs-nn{{margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:6px 12px}}
.cs-nn b{{display:block;font-size:28px;font-weight:400;letter-spacing:-.05em;line-height:1.05}}
.cs-nn span{{font-size:10.5px;font-weight:500}}
.cs-g{{grid-column:1/3;background:linear-gradient(90deg,#fff 40%,{Y})}}

/* bruno */
.lead-w{{width:560px;top:150px}}
.bm-chart{{left:60px;top:260px;width:520px;background:#fff;border:1.4px solid {INK};border-radius:22px;padding:20px 24px 14px}}
.bm-plus{{position:absolute;right:52px;top:210px;font-size:40px;letter-spacing:-.05em;font-weight:500}}
.bm-k{{left:640px;right:60px;top:150px}}
.bm-k>div{{display:flex;gap:20px;align-items:baseline;border-bottom:1.4px solid {INK};padding:10px 0}}
.bm-k b{{font-size:48px;font-weight:400;letter-spacing:-.06em;width:190px;flex:none;line-height:1}}
.bm-k span{{font-size:13px;font-weight:500;line-height:1.35}}
.bm-single{{left:640px;right:60px;top:430px;background:{INK};color:#fff;border-radius:24px;padding:20px 26px}}
.bm-single .pill{{border-color:#fff;color:#fff;margin-right:14px}}
.bm-st b{{font-size:26px;font-weight:500;letter-spacing:-.04em}}
.bm-n{{display:flex;gap:40px;margin-top:14px}}
.bm-n b{{display:block;font-size:40px;font-weight:400;letter-spacing:-.05em;color:{Y}}}
.bm-n span{{font-size:12px}}

/* códigos */
.cc-top{{left:60px;top:44px;right:60px;display:flex;justify-content:space-between}}
.cc-h{{left:60px;top:92px;width:1060px;font-size:50px;font-weight:400;letter-spacing:-.05em;line-height:1.05}}
.cc-sub{{left:60px;top:218px;font-size:17px}}
.cc-tw{{left:60px;top:272px;width:470px;background:#fff;border:1.4px solid {INK};border-radius:22px;padding:18px 22px}}
.cc-tw .tw-t{{font-size:21px}}
.cc-tw u{{text-decoration:none;background:{Y};padding:0 3px;border-radius:4px}}
.cc-grid{{left:560px;right:60px;top:272px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.cc{{border-top:1.4px solid {INK};padding-top:10px}}
.cc-n{{font-size:11px;font-weight:600;color:{GD}}}
.cc b{{display:block;font-size:30px;font-weight:500;letter-spacing:-.045em;margin:4px 0 8px}}
.cc p{{font-size:12.5px;line-height:1.45}}
.cc strong{{background:{Y};padding:0 3px;font-weight:600}}
.cc-f{{left:60px;top:500px;width:1000px;font-size:20px;letter-spacing:-.02em;line-height:1.35;border-top:1.4px solid {INK};padding-top:16px}}

/* contexto */
.cx-l{{left:60px;top:170px;width:600px}}
.cx-big{{font-size:34px;letter-spacing:-.04em;line-height:1.12;margin-bottom:20px}}
.cx-p{{font-size:14px;line-height:1.5;margin-bottom:12px}}
.cx-r{{left:720px;right:60px;top:170px}}
.cx-tags{{display:flex;flex-wrap:wrap;gap:8px}}
.cx-tags span{{border:1.4px solid {INK};border-radius:999px;padding:5px 14px 4px;font-size:13px;font-weight:500;background:#fff}}
.cx-y span{{background:{Y}}}
.venn{{position:relative;height:190px;margin-top:22px}}
.venn>div{{position:absolute;width:150px;height:150px;border-radius:50%;border:1.4px solid {INK};display:flex;
  align-items:center;justify-content:center;text-align:center;font-size:11.5px;font-weight:600;line-height:1.2}}
.v1{{left:20px;top:0;background:{Y}aa;padding-right:40px;padding-bottom:30px}}
.v2{{left:125px;top:0;background:{G}88;padding-left:40px;padding-bottom:30px}}
.v3{{left:72px;top:60px;background:#ffffff88;padding-top:50px;height:130px!important}}
.venn .vc{{left:122px;top:58px;width:56px;height:56px;border:none;background:{INK};color:#fff;font-size:10px}}
.cx-note{{left:60px;top:568px;width:1000px;font-size:13px;font-weight:600;border-left:4px solid {G};padding-left:14px}}

/* ideias */
.id-top{{left:60px;top:44px;display:flex;gap:20px;align-items:center}}
.id-h{{left:56px;top:110px;font-size:150px;font-weight:400;letter-spacing:-.065em;line-height:.82}}
.id-p{{left:60px;top:370px;width:470px;font-size:16px;line-height:1.45}}
.id-tw{{left:630px;top:44px}}
.id-ret{{left:630px;bottom:64px;display:flex;gap:26px}}
.id-ret3{{gap:20px}}
.ret{{width:140px}}
.ret-c{{border-radius:50%;overflow:hidden;border:1.4px solid {INK};background:linear-gradient(135deg,{Y},{G});
  display:flex;align-items:center;justify-content:center}}
.ret-c img{{width:100%;height:100%;object-fit:cover}}
.mono{{font-weight:500;letter-spacing:-.04em}}
.ret-n{{font-size:14px;font-weight:600;margin-top:8px}}
.ret-p{{font-size:11px;font-weight:500;color:{INK}}}
.id-why{{left:60px;width:480px;top:510px;display:flex;gap:30px}}
.id-why>div{{flex:1;border-top:1.4px solid {INK};padding-top:8px}}
.id-why b{{display:block;font-size:26px;font-weight:500;letter-spacing:-.04em}}
.id-why span{{font-size:12px;font-weight:500}}

/* aposta */
.fl{{left:60px;right:60px;top:300px;display:flex;align-items:stretch;gap:10px}}
.fl-i{{flex:1;background:#fff;border:1.4px solid {INK};border-radius:20px;padding:14px 16px}}
.fl-i:first-child{{background:{Y}}}
.fl-t{{font-size:11px;font-weight:700;color:{GD}}}
.fl-i b{{display:block;font-size:22px;font-weight:500;letter-spacing:-.04em;margin:4px 0}}
.fl-i p{{font-size:12px;line-height:1.4}}
.fl-a{{align-self:center;font-size:22px}}
.cmp{{left:60px;top:450px;width:1160px;border-collapse:collapse;font-size:14px;table-layout:fixed}}
.cmp th:first-child{{width:360px}}
.cmp th{{text-align:left;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:6px 0;border-bottom:1.4px solid {INK}}}
.cmp td{{padding:6px 0;border-bottom:1px solid #9a9ca6;font-weight:500}}
.cmp td:nth-child(2),.cmp td:nth-child(3){{font-size:16px;letter-spacing:.2em}}
.cmp .d1{{color:{GD}}}

/* investimento */
.inv-top{{left:60px;top:50px;display:flex;gap:20px;align-items:center}}
.inv-s{{left:66px;top:118px;font-size:48px;letter-spacing:-.04em}}
.inv-h{{left:40px;top:200px;font-size:400px;font-weight:400;letter-spacing:-.07em;line-height:1}}
.inv-p{{right:60px;bottom:70px;text-align:right;font-size:17px;line-height:1.45;font-weight:500}}

/* obrigado */
.ob-logo{{left:60px;top:56px;height:40px}}
.ob-h{{left:48px;top:230px;font-size:176px;font-weight:400;letter-spacing:-.065em;line-height:1}}
.ob-p{{left:62px;top:440px;font-size:16px;font-weight:500}}
.ob-sig{{left:62px;bottom:56px;border-top:1.4px solid {INK};padding-top:12px;width:380px}}
.ob-sig b{{display:block;font-size:18px;font-weight:600;letter-spacing:-.02em}}
.ob-sig span{{font-size:12.5px;font-weight:500}}
.ob-img{{right:60px;top:60px;width:340px;height:600px;border-radius:170px;overflow:hidden;border:1.4px solid {INK}}}
.ob-img img{{width:100%;height:100%;object-fit:cover}}
"""

html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Tinashe × Brasil · Popstar</title>"
        f"<style>{FONTES}\n{CSS}</style></head><body>" + "".join(S) + "</body></html>")
(B/"deck.build.html").write_text(html)

from playwright.sync_api import sync_playwright
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
pdf = B/"Tinashe-Popstar-Brasil-Proposta.pdf"
erros = []
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width":1280,"height":720})
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto((B/"deck.build.html").as_uri()); pg.wait_for_timeout(1000)
    # transbordo: elemento saindo do slide
    over = pg.evaluate("""() => [...document.querySelectorAll('.sl')].map((s,i)=>{
        const r=s.getBoundingClientRect(); const bad=[];
        s.querySelectorAll(':scope>*:not(.blob):not(.bg-y)').forEach(e=>{const q=e.getBoundingClientRect();
          if(q.right>r.right+1||q.bottom>r.bottom+1||q.left<r.left-1) bad.push(e.className)});
        return bad.length?[i+1,bad]:null}).filter(Boolean)""")
    if over: print("TRANSBORDO:", over)
    if "--png" in sys.argv:
        for i, el in enumerate(pg.query_selector_all(".sl")):
            el.screenshot(path=str(B.parent/f"../tmp_png_{i+1:02d}.png") if False else f"{sys.argv[sys.argv.index('--png')+1]}/s{i+1:02d}.png")
    pg.emulate_media(media="print")
    pg.pdf(path=str(pdf), width="13.333in", height="7.5in", print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"})
    b.close()
if erros: print("ERROS:", erros); sys.exit(1)
print(f"{pdf.name}: {pdf.stat().st_size/1024/1024:.2f} MB · {len(S)} slides")
