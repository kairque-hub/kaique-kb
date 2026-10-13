#!/usr/bin/env python3
"""Normani × Brasil 2026: after party "NORMANI TAKES SÃO PAULO" (2 páginas, 1280x720, em inglês).

Fotos de exemplo do fotógrafo e frames do vídeo do espaço entram sozinhos se existirem:
  img/after/espaco-1.jpg ... espaco-3.jpg   frames do @eventos.notie
  img/after/foto-1.jpg ... foto-3.jpg       exemplos do @rodolfosanchesfoto
"""
import glob, sys
import build_geral as g

YEL, GRN, INK, ORG = "#F2EC1A", "#13B04B", "#0B0B0C", "#E2531B"
ROOM = g.uri("img/notie1.jpg")
V = {k: g.uri(f"img/after/v-{k}.jpg") for k in ("bar", "lounge", "banco", "sala", "caixas", "janela")}
TITLE = "NORMANI TAKES SÃO PAULO"


def ig(handle):
    return f'<a href="https://www.instagram.com/{handle}/">@{handle}</a>'


def foto_ou_ph(path, rot, sub):
    f = g.opt(path)
    if f:
        return f'<div class="a-img" style="background-image:url({f})"></div>'
    return (f'<div class="a-ph"><b>{rot}</b><small>{sub}</small></div>')


def ft(sec, n):
    return (f'<div class="ft a-ft"><span>{sec}</span>'
            f'<span>Normani × Brasil · Meli Music 2026<b class="pn">{n:02d}</b></span></div>')


# ------------------------------------------------------------------ página 1: o after
espaco = "".join(foto_ou_ph(f"img/after/espaco-{i}.jpg", "Venue frame", "@eventos.notie") for i in (1, 2, 3)
                 if g.opt(f"img/after/espaco-{i}.jpg"))
P1 = (
    f'<div class="a-room" style="background-image:url({ROOM})"></div>'
    f'<div class="a-room2" style="top:0;height:356px;background-image:url({V["janela"]});background-position:50% 60%"></div>'
    f'<div class="a-room2" style="top:364px;height:356px;background-image:url({V["bar"]})"></div>'
    '<div class="a-shade"></div>'
    + g.blob(1180, 40, 260) + g.blob(820, 760, 260, "g", .8) +
    f'<div class="hd a-hd">{g.pill("After party", "wl")}<span>After the show · Meli Music</span></div>'
    f'<h1 class="a-title">NORMANI<br>TAKES<br><span>SÃO PAULO</span></h1>'
    '<p class="a-lead">An invite-only after party for the night of the show, produced by <b>Sharp</b>. '
    'Open bar, a São Paulo rooftop, two DJs and the people who move the city’s fashion, music and arts.</p>'
    '<div class="a-facts">'
    '<div><small>When</small><b>1 AM – 5 AM</b><span>right after the Meli Music show</span></div>'
    '<div><small>Guests</small><b>Up to 150</b><span>open bar all night</span></div>'
    '<div><small>Where</small><b>Terraço Notiê</b><span>Rua Formosa, 157 · Centro Histórico, São Paulo<br>access via Shopping Light parking</span></div>'
    '<div><small>Security</small><b>Reinforced</b><span>controlled guest list and entry</span></div>'
    '</div>'
    '<div class="a-cost"><div><small>Cost to Normani</small><b>USD 0</b></div>'
    '<p>All costs covered by <strong>Sharp</strong>.<br>No brand presence. No ticket sales.</p></div>'
    f'<p class="a-cred">Venue: {ig("eventos.notie")}</p>'
    + '<div class="ft a-ft" style="left:600px"><span>After party</span>'
    '<span>Normani × Brasil · Meli Music 2026<b class="pn">01</b></span></div>'
)

# ------------------------------------------------------------------ página 2: o espaço
def tile(k, area, nome, txt, pos="center"):
    return (f'<div class="a-tile" style="grid-area:{area};background-image:url({V[k]});background-position:{pos}">'
            f'<div><b>{nome}</b><span>{txt}</span></div></div>')


PV = (
    g.blob(1200, 30, 220) +
    f'<div class="hd a-hd">{g.pill("The venue", "wl")}<span>{TITLE}</span></div>'
    '<h1 class="a-t2" style="top:84px;font-size:46px">Terraço Notiê</h1>'
    '<p class="a-addr">Rua Formosa, 157 · Centro Histórico, São Paulo · on top of the Shopping Light building, '
    'facing the Theatro Municipal</p>'
    '<div class="a-grid">'
    + tile("bar", "a", "The bar", "A circular bar at the heart of the floor, for the open bar")
    + tile("sala", "b", "Sala de Música", "The music room, with the DJ booth for the night")
    + tile("lounge", "c", "Lounge", "Long tables and velvet booths")
    + tile("banco", "d", "Booths", "Quiet corners to sit and talk")
    + tile("caixas", "e", "Sound", "Vintage horn speakers and turntables")
    + tile("janela", "f", "City view", "Downtown São Paulo from above", "50% 55%")
    + '</div>'
    + ft("After party · The venue", 2)
)

# ------------------------------------------------------------------ página 2: quem está lá
guests = [("Anitta", "Pop · funk"), ("IZA", "Pop · R&B"), ("Pabllo Vittar", "Pop"), ("Gloria Groove", "Pop · rap"),
          ("Liniker", "Soul · R&B"), ("Marina Sena", "Pop"), ("Any Gabrielly", "Pop"), ("Carol Biazin", "Pop"),
          ("Duquesa", "Rap"), ("Budah", "Rap · R&B"), ("Ebony", "Rap"), ("Veigh", "Trap"), ("Teto", "Trap")]


def pessoa(nome, papel, handle, tam=76):
    return (f'<div class="a-pp"><a href="https://www.instagram.com/{handle}/">{g.avatar(nome, "", tam)}</a>'
            f'<small>{papel}</small><p>{ig(handle)}</p></div>')


fotos = pessoa("Rodolfo Sanches", "PHOTO", "rodolfosanchesfoto") + "".join(
    foto_ou_ph(f"img/after/foto-{i}.jpg", "Photo example", "@rodolfosanchesfoto") for i in (1, 2, 3))
P2 = (
    g.blob(1200, 40, 240) + g.blob(80, 760, 280, "g", .8) +
    f'<div class="hd a-hd">{g.pill("The room", "wl")}<span>{TITLE}</span></div>'
    '<h1 class="a-t2">Who’s in the room</h1>'
    '<div class="a-who">'
    '<div><small>01</small><b>Meli Music line-up</b><span>Artists from the festival and their teams</span></div>'
    '<div><small>02</small><b>Tastemakers</b><span>São Paulo’s names in fashion, music and the arts</span></div>'
    '<div><small>03</small><b>Up to 150</b><span>Invite-only, controlled guest list</span></div></div>'
    '<p class="a-lab" style="top:300px">Suggested artist guests <i>(examples, open to other names)</i></p>'
    '<div class="a-guests">' + "".join(g.avatar(n, p, 62) for n, p in guests) + '</div>'
    '<p class="a-lab" style="top:470px">On the decks</p>'
    '<div class="a-crew" style="left:60px">' + pessoa("94tago", "DJ", "94tago") + pessoa("Aisha Mbikila", "DJ", "aishambikila") + '</div>'
    '<p class="a-lab" style="top:470px;left:520px">Photography · Rodolfo Sanches ' + ig("rodolfosanchesfoto") + '</p>'
    f'<div class="a-photos">{fotos}</div>'
    + ft("After party · The room", 3)
)

CSS = g.CSS + f"""
.sl.a-dark{{background:{INK};color:#fff}}
.a-dark .pill{{border-color:#fff;color:#fff}}
.a-hd span{{color:#fff}}
.a-ft{{color:#fff}}.a-ft .pn{{border-color:#fff}}
a{{color:inherit;text-decoration:none}}
.a-room{{position:absolute;left:0;top:0;width:328px;height:720px;background-size:cover;background-position:50% 40%}}
.a-room2{{position:absolute;left:336px;width:224px;background-size:cover;background-position:center}}
.a-shade{{position:absolute;left:0;top:0;width:560px;z-index:1;height:720px;background:linear-gradient(0deg,rgba(11,11,12,.6),rgba(11,11,12,0) 25%),linear-gradient(180deg,rgba(11,11,12,.55),rgba(11,11,12,0) 18%)}}
.a-dark .blob{{opacity:.55}}
.a-title{{position:absolute;left:600px;top:92px;font-size:66px;line-height:.92;font-weight:800;letter-spacing:-.035em;z-index:3}}
.a-title span{{color:{YEL}}}
.a-lead{{position:absolute;left:600px;top:292px;width:620px;font-size:16px;line-height:1.5;color:#ddd;z-index:3}}
.a-lead b{{color:#fff}}
.a-facts{{position:absolute;left:600px;top:372px;width:620px;display:grid;grid-template-columns:1fr 1fr;gap:14px 26px;z-index:3}}
.a-facts div{{border-top:1px solid #444;padding-top:8px}}
.a-facts small,.a-cost small,.a-who small{{display:block;font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{GRN}}}
.a-facts b{{display:block;font-size:22px;font-weight:500;letter-spacing:-.01em;margin-top:3px}}
.a-facts span{{display:block;font-size:12px;color:#bbb;line-height:1.45;margin-top:2px}}
.a-cost{{position:absolute;left:600px;top:566px;width:620px;background:{YEL};color:{INK};border-radius:20px;padding:12px 22px;display:flex;align-items:center;gap:22px;z-index:3}}
.a-cost small{{color:{INK}}}
.a-cost b{{display:block;font-size:44px;font-weight:800;letter-spacing:-.03em;line-height:1}}
.a-cost p{{font-size:13.5px;line-height:1.45}}
.a-cred{{position:absolute;left:20px;top:690px;font-size:11px;color:#ddd;z-index:3}}
.a-t2{{position:absolute;left:60px;top:92px;font-size:56px;font-weight:400;letter-spacing:-.035em;z-index:3}}
.a-who{{position:absolute;left:60px;right:60px;top:180px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;z-index:3}}
.a-who div{{border-top:1px solid #444;padding-top:8px}}
.a-who b{{display:block;font-size:22px;font-weight:500;margin-top:2px}}
.a-who span{{display:block;font-size:13px;color:#bbb;margin-top:2px}}
.a-lab{{position:absolute;left:60px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{YEL};z-index:3}}
.a-lab i{{font-style:normal;color:#999;letter-spacing:.04em;text-transform:none;font-weight:500}}
.a-lab a{{color:#fff;text-transform:none;letter-spacing:0}}
.a-guests{{position:absolute;left:60px;right:60px;top:326px;display:grid;grid-template-columns:repeat(13,1fr);z-index:3}}
.a-guests .pp b{{font-size:11px;color:#fff;margin-top:6px}}
.a-guests .pp small{{font-size:9.5px;color:#999}}
.a-guests .av,.a-crew .av{{border-color:#555}}
.a-crew{{position:absolute;top:496px;display:flex;gap:30px;z-index:3}}
.a-pp{{width:180px;height:160px;background:#17171a;border:1px solid #333;border-radius:18px;padding:12px;display:flex;flex-direction:column;align-items:center;text-align:center}}
.a-pp .pp b{{color:#fff;font-size:14px;margin-top:6px}}
.a-pp small{{font-size:10.5px;font-weight:700;letter-spacing:.14em;color:{GRN};margin-top:4px}}
.a-pp p{{font-size:12px;color:#ccc;margin-top:2px}}
.a-photos{{position:absolute;left:520px;right:60px;top:496px;height:160px;display:grid;grid-template-columns:180px 1fr 1fr 1fr;gap:12px;z-index:3}}
.a-addr{{position:absolute;left:390px;top:104px;width:820px;font-size:14px;color:#bbb;line-height:1.5;z-index:3}}
.a-grid{{position:absolute;left:60px;right:60px;top:168px;height:490px;display:grid;gap:10px;z-index:3;
 grid-template-columns:1fr 1fr 1fr 1fr;grid-template-rows:1.15fr 1fr;grid-template-areas:"a a b b" "c d e f"}}
.a-tile{{position:relative;border-radius:14px;overflow:hidden;background-size:cover}}
.a-tile>div{{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 11px;background:linear-gradient(0deg,rgba(11,11,12,.85),rgba(11,11,12,0))}}
.a-tile b{{display:block;font-size:17px;font-weight:600}}
.a-tile span{{display:block;font-size:11.5px;color:#ddd;margin-top:2px}}
.a-img{{border-radius:14px;background-size:cover;background-position:center}}
.a-ph{{border:1.4px dashed #555;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#999}}
.a-ph b{{font-size:14px;font-weight:500;color:#ccc}}
.a-ph small{{font-size:11px;margin-top:3px}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    body = f'<section class="sl a-dark">{P1}</section><section class="sl a-dark">{PV}</section><section class="sl a-dark">{P2}</section>'
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}</title>'
            f'<style>{g.FONTES}{CSS}</style></head><body>{body}</body></html>')
    out = g.B / "Normani-After-Party.html"
    out.write_text(html)
    pdf = g.B / "Normani-After-Party.pdf"
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.pdf(path=str(pdf), width="1280px", height="720px", print_background=True)
        if "--png" in sys.argv:
            for i, el in enumerate(pg.query_selector_all("section.sl"), 1):
                el.screenshot(path=str(g.B / f"preview-after-{i}.png"))
        b.close()
    print(pdf.name)
