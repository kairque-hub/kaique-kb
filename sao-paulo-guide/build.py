#!/usr/bin/env python3
"""São Paulo guide for Team Normani (in English). Portrait pages 1080x1350, exported to PDF.

Data lives in data.json; photos in img/<slug>.jpg (missing photo -> colour block).
"""
import base64, glob, json, pathlib, sys

B = pathlib.Path(__file__).parent
D = json.loads((B / "data.json").read_text())
INTER = (B.parent / "normani-brasil/fontes/inter.css").read_text()
SERIF = base64.b64encode((B.parent / "normani-brasil/fontes/InstrumentSerif-italic.woff2").read_bytes()).decode()
SERIF_N = base64.b64encode((B.parent / "normani-brasil/fontes/InstrumentSerif-normal.woff2").read_bytes()).decode()
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}


def img(slug):
    for f in sorted((B / "img").glob(f"{slug}.*")):
        return f"data:{MIME[f.suffix.lower()]};base64," + base64.b64encode(f.read_bytes()).decode()
    return None


BG = img("_bg")
AG = img("_agency")
GRN, YEL, INK, CREAM, DEEP = "#13B04B", "#F2EC1A", "#0B0B0C", "#F4F1E6", "#0E3B2A"
PAGES = []


def page(html, cls="", style=""):
    n = len(PAGES) + 1
    PAGES.append(f'<section class="p {cls}" style="{style}">{html}'
                 f'<div class="pf"><span>São Paulo · Team Normani</span><b>{n:02d}</b></div></section>')


def head(kicker, title, sub=""):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="hd"><span class="kick">{kicker}</span><h1>{title}</h1>{s}</div>'


def maps(addr):
    from urllib.parse import quote
    return "https://www.google.com/maps/search/?api=1&query=" + quote(addr + ", São Paulo")


def card(it, kind):
    ph = img(it["slug"])
    pic = (f'<div class="ph" style="background-image:url({ph})"></div>' if ph
           else f'<div class="ph none"><span>{it["name"]}</span></div>')
    tag = it.get("type") or it.get("what") or it.get("vibe") or ""
    order = ""
    if kind == "food" and it.get("signature_dish"):
        order = f'<p class="ord"><small>Order</small>{it["signature_dish"]}</p>'
    if kind == "bar" and it.get("signature_drink"):
        order = f'<p class="ord"><small>Drink</small>{it["signature_drink"]}</p>'
    ig = f' · <a href="https://www.instagram.com/{it["instagram"].lstrip("@")}/">@{it["instagram"].lstrip("@")}</a>' if it.get("instagram") else ""
    addr = it.get("address") or ""
    hood = it.get("neighborhood") or ""
    linkable = any(ch.isdigit() for ch in addr) or "Shopping" in addr or "Praça" in addr
    link = f'<a href="{maps(addr)}">{addr}</a>' if linkable else addr
    return (f'<div class="c">{pic}<div class="cb"><span class="tg">{tag}</span>'
            f'<h3>{it["name"]}</h3>{order}'
            f'<p class="ad">{link}{" · " + hood if hood else ""}{ig}</p></div></div>')


TIPS = {"food": ("Book ahead", "The hottest tables (Le Freak, A Casa do Porco, Tan Tan) fill up fast. Ask the Rosewood concierge to reserve for you."),
        "shop": ("Two in one street", "Misci and Francesca face each other on Rua Mateus Grou, Pinheiros. And Varal bar is hidden behind the Misci store there."),
        "bar": ("Centro by night", "Bar do Cofre, Bar dos Arcos and Balsa are a few minutes apart downtown. Go by Uber or 99, not on foot.")}


def tip(kind):
    t, x = TIPS[kind]
    return f'<div class="c tip"><span class="tg">Tip</span><h3>{t}</h3><p>{x}</p></div>'


def grid_pages(items, kind, kicker, title, sub, per=6, more=8):
    first = items[:per]
    page(head(kicker, title, sub) + f'<div class="g">{"".join(card(x, kind) for x in first)}{tip(kind) if len(first) % 2 else ""}</div>', "lt")
    rest = items[per:]
    for i in range(0, len(rest), more):
        page(f'<div class="hd sm"><span class="kick">{kicker}</span><h1>{title}, cont.</h1></div>'
             f'<div class="g cmp">{"".join(card(x, kind) for x in rest[i:i + more])}{tip(kind) if len(rest[i:i + more]) % 2 else ""}</div>', "lt")


# ---------------------------------------------------------------- cover
page(f'<div class="cv-bg" style="background-image:url({BG})"></div>'
     f'<img class="ag" src="{AG}">'
     '<div class="cv">'
     '<span class="kick y">Team Normani · October 2026</span>'
     '<h1 class="cv-t">São<br>Paulo</h1>'
     '<p class="cv-s"><i>a field guide</i> to eating, shopping<br>and going out in the city</p>'
     '<div class="cv-idx"><span>Eat</span><span>Shop</span><span>Drink</span><span>Listen</span><span>Know</span><span>Don’ts</span><span>Help</span></div>'
     '</div>', "dk")

# ---------------------------------------------------------------- about the city
nums = [("11.9M", "people in the city (IBGE 2026 est.), the largest city in the Southern Hemisphere"),
        ("1554", "founded on January 25 by Jesuit priests"),
        ("#1", "Brazil has the largest Japanese community outside Japan. Its heart is Liberdade, in São Paulo"),
        ("760 m", "above sea level: warm days, cool nights. Bring a light jacket")]
facts = [("Paulistanos", "Locals are called paulistanos. The city never really sleeps: dinner at 10 PM is normal, parties end at sunrise."),
         ("Sunday on Paulista", "Avenida Paulista closes to cars on Sundays and turns into a giant open-air street party."),
         ("A city of immigrants", "Italian, Japanese, Lebanese, Korean and Northeastern Brazilian cooking all live here, often on the same block."),
        ("Street art", "Graffiti and murals are everywhere; walk Beco do Batman in Vila Madalena for the classic tour.")]
crea = [("SPFW · Oct 13–18, 2026", "Latin America’s biggest fashion week, since 1995, runs the same week you’re here."),
        ("Bienal de São Paulo", "Created in 1951, the second-oldest art biennial in the world after Venice."),
        ("MASP", "Lina Bo Bardi’s red-framed museum on Paulista, floating over a free public plaza."),
        ("Pride", "São Paulo’s Pride Parade on Paulista is one of the largest in the world, with millions on the street."),
        ("The new Centro", "Old downtown buildings now host the city’s hottest bars, restaurants and studios. Le Freak, Bar dos Arcos and Brim are all here.")]
page(f'<div class="cv-bg" style="background-image:url({BG});opacity:.28"></div>'
     + head("Meet the city", "São Paulo,<br>in numbers") +
     '<div class="nm4">' + "".join(f'<div><b>{n}</b><p>{t}</p></div>' for n, t in nums) + '</div>'
     '<div class="ab2"><div><span class="kick y">Good to know</span>' +
     "".join(f'<h3>{t}</h3><p>{x}</p>' for t, x in facts) + '</div>'
     '<div><span class="kick y">The creative city</span>' +
     "".join(f'<h3>{t}</h3><p>{x}</p>' for t, x in crea) + '</div></div>', "dk")

# ---------------------------------------------------------------- basics
H = D["hotel"]
page(head("Before you go", "The basics", "Everything you need in your pocket for the week.") +
     '<div class="bas">'
     f'<div class="b1"><small>Home base</small><h2>{H["name"]}</h2><p>{H["address"]}</p>'
     f'<p class="mut">{H["note"]}</p></div>'
     '<div><small>Getting around</small><h3>Uber or 99</h3><p>The two ride apps everyone uses. '
     '99 is the local one and works just like Uber. Download both before you land.</p></div>'
     '<div><small>Money</small><h3>Brazilian Real · R$</h3><p>Cards (and Apple / Google Pay) work almost everywhere. '
     'Keep a little cash for small bars and street vendors.</p></div>'
     '<div><small>Food delivery</small><h3>iFood</h3><p>The most popular delivery app in Brazil. '
     'Uber Eats works too.</p></div>'
     '<div><small>Tipping</small><h3>10% is on the bill</h3><p>Restaurants add a 10% service charge ("serviço"). '
     'No need to tip on top.</p></div>'
     '</div>', "lt")

grid_pages(D["restaurants"], "food", "Eat", "Restaurants", "Our picks, from fine dining to the corner boteco. Tap an address to open it in Maps.")
grid_pages(D["shops"], "shop", "Shop", "Stores", "Brazilian brands, design and the best second-hand in town.")
grid_pages(D["bars"], "bar", "Drink", "Bars", "Where São Paulo actually goes out.")

# ---------------------------------------------------------------- brazilian pop
ARTS = [("anitta", "Anitta", "Brazil’s global pop superstar, from funk carioca to the world.", "Envolver"),
        ("ludmilla", "Ludmilla", "Funk and pagode queen, one of the biggest voices in the country.", "Rainha da Favela"),
        ("pabllo-vittar", "Pabllo Vittar", "Drag pop icon mixing pop with Northeastern rhythms.", "K.O."),
        ("gloria-groove", "Gloria Groove", "Drag artist, rapper and pop star from São Paulo.", "Bonekinha"),
        ("marina-sena", "Marina Sena", "The new face of Brazilian pop, sensual and sunny.", "Por Supuesto"),
        ("pedro-sampaio", "Pedro Sampaio", "DJ and producer behind the funk hits that run every party.", "Galopa"),
        ("luisa-sonza", "Luísa Sonza", "Pop star with chart-topping albums and viral hits.", "Chico"),
        ("liniker", "Liniker", "Soul and MPB, one of the most acclaimed voices of her generation.", "Psiu"),
        ("iza", "IZA", "Pop, R&B and funk with a powerhouse voice.", "Dona de Mim"),
        ("duquesa", "Duquesa", "Rapper from Bahia leading the new wave of Brazilian rap.", "99 Problemas")]
page(head("Listen", "Brazilian pop, now", "The names you’ll hear everywhere this week, and one song to start with.") +
     '<div class="ar">' + "".join(
         f'<div><img src="{img("art-" + k)}"><div><h3>{n}</h3><p>{d}</p>'
         f'<span>▶ {t}</span></div></div>' for k, n, d, t in ARTS) + '</div>', "lt")

# ---------------------------------------------------------------- don'ts
donts = [
    ("Phones near the hotel", "The area around the hotel is great, which also makes it a target. Don’t walk around with your phone out on the street."),
    ("Gold & chains on busy streets", "Skip gold chains and flashy jewellery in crowded places like Avenida Paulista."),
    ("Candy or water from drivers", "Politely say no if a ride-app driver offers you candy or water."),
    ("Cigarettes from strangers", "Don’t accept cigarettes from people you don’t know."),
    ("Kids on bikes around Paulista", "Keep an eye out for young guys on bicycles around Avenida Paulista: phone snatching is their move."),
    ("Check the card machine", "When paying by card, always look at the amount on the machine before you tap or enter your PIN."),
]
page(f'<div class="cv-bg" style="background-image:url({BG});opacity:.35"></div>' +
     head("Stay sharp", "São Paulo don’ts", "The city is warm and welcoming. A few habits keep it that way.") +
     '<div class="dn">' + "".join(f'<div><b>{i:02d}</b><h3>Don’t: {t}</h3><p>{x}</p></div>'
                                 for i, (t, x) in enumerate(donts, 1)) + '</div>', "dk")

# ---------------------------------------------------------------- phrases + emergency
E = D["emergency"]
phr = [("Muito obrigado / obrigada", "Thank you very much", "MOON-too oh-bree-GAH-doo / -dah"),
       ("Por favor", "Please", "por fah-VOR"),
       ("Meu nome é…", "My name is…", "meh-oo NOH-mee eh"),
       ("Eu não falo português", "I don’t speak Portuguese", "eh-oo nowm FAH-loo por-too-GAYZ")]
page(head("Say it", "Useful Portuguese") +
     '<div class="ph2">' + "".join(f'<div><h2>{p}</h2><p>{e}</p><small>{s}</small></div>' for p, e, s in phr) + '</div>'
     '<div class="em"><span class="kick">Emergency</span><div class="emg">' +
     "".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in E["numbers"]) +
     f'</div><p>{E["note"]}</p></div>', "lt")

# ---------------------------------------------------------------- back cover
page(f'<div class="cv-bg" style="background-image:url({BG})"></div>'
     '<div class="bk"><h1>Obrigado.</h1>'
     f'<img src="{AG}">'
     '<p>Prepared by <b>Kaique Brasileiro</b> for <b>Avery Schiff</b> &amp; Team Normani.</p></div>', "dk")

CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url(data:font/woff2;base64,{SERIF})}}
@font-face{{font-family:'IS';font-style:normal;src:url(data:font/woff2;base64,{SERIF_N})}}
*{{margin:0;padding:0;box-sizing:border-box}}
@page{{size:1080px 1350px;margin:0}}
body{{font-family:Inter,sans-serif}}
a{{color:inherit;text-decoration:none}}
.p{{position:relative;width:1080px;height:1350px;overflow:hidden;break-after:page;padding:84px 72px}}
.lt{{background:{CREAM};color:{INK}}}
.dk{{background:{DEEP};color:#fff}}
.pf{{position:absolute;left:72px;right:72px;bottom:40px;display:flex;justify-content:space-between;font-size:13px;font-weight:600;letter-spacing:.04em;opacity:.7;z-index:3}}
.kick{{display:inline-block;font-size:13px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:{GRN}}}
.kick.y{{color:{YEL}}}
.hd{{position:relative;z-index:3;margin-bottom:40px}}
.hd h1{{font-family:'IS';font-weight:400;font-size:104px;line-height:.95;letter-spacing:-.02em;margin-top:10px}}
.hd .sub{{font-size:19px;line-height:1.45;margin-top:14px;max-width:760px;opacity:.75}}
.cv-bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.cv{{position:relative;z-index:2;height:100%;display:flex;flex-direction:column}}
.cv-t{{font-family:'IS';font-weight:400;font-size:260px;line-height:.86;letter-spacing:-.03em;margin-top:auto}}
.cv-s{{font-size:30px;line-height:1.3;margin-top:26px}}
.cv-s i{{font-family:'IS';font-size:40px;color:{YEL}}}
.cv-idx{{display:flex;gap:28px;margin-top:70px;margin-bottom:60px;padding-top:22px;border-top:1.5px solid rgba(255,255,255,.5);font-size:17px;font-weight:600;letter-spacing:.06em;text-transform:uppercase}}
.bas{{display:grid;grid-template-columns:1fr 1fr;gap:26px;position:relative;z-index:3}}
.bas>div{{border-top:2px solid {INK};padding-top:16px}}
.bas small{{font-size:12px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{GRN}}}
.bas h2{{font-family:'IS';font-weight:400;font-size:64px;line-height:1;margin:8px 0 10px}}
.bas h3{{font-size:28px;font-weight:600;letter-spacing:-.01em;margin:8px 0 8px}}
.bas p{{font-size:17px;line-height:1.5}}
.bas .mut{{opacity:.65;margin-top:8px;font-size:15px}}
.bas .b1{{grid-column:span 2;background:{GRN};color:#fff;border:0;border-radius:28px;padding:30px 34px}}
.bas .b1 small{{color:{YEL}}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:22px 24px;position:relative;z-index:3}}
.c{{background:#fff;border-radius:22px;overflow:hidden;display:flex;flex-direction:column;height:300px}}
.c .ph{{height:142px;background-size:cover;background-position:center;flex:none}}
.c .ph.none{{background:linear-gradient(120deg,{GRN},{YEL});display:flex;align-items:flex-end;padding:14px 18px}}
.c .ph.none span{{font-family:'IS';font-size:34px;color:{INK}}}
.cb{{padding:14px 18px 16px;display:flex;flex-direction:column;flex:1}}
.tg{{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:{GRN}}}
.c h3{{font-size:26px;font-weight:600;letter-spacing:-.015em;margin:3px 0 6px;line-height:1.05}}
.ord{{font-size:14.5px;line-height:1.35}}
.ord small{{display:inline-block;background:{YEL};font-size:10.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:2px 7px;border-radius:5px;margin-right:7px;vertical-align:1px}}
.ad{{font-size:12.5px;line-height:1.4;opacity:.7;margin-top:auto}}
.c.tip{{background:{GRN};color:#fff;padding:22px 24px;justify-content:center}}
.c.tip .tg{{color:{YEL}}}.g .c.tip h3{{font-family:'IS';font-weight:400;font-size:40px;margin:6px 0 10px}}.c.tip p{{font-size:16px;line-height:1.5}}
.nm4{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;position:relative;z-index:3;border-top:1.5px solid rgba(255,255,255,.4);padding-top:18px}}
.nm4 b{{display:block;font-family:'IS';font-weight:400;font-size:84px;line-height:1;color:{YEL}}}
.nm4 p{{font-size:16px;line-height:1.45;margin-top:8px;opacity:.85}}
.ab2{{display:grid;grid-template-columns:1fr 1.25fr;gap:44px;margin-top:56px;position:relative;z-index:3}}
.ab2 h3{{font-size:24px;font-weight:600;margin-top:24px}}
.ab2 p{{font-size:17px;line-height:1.5;opacity:.82;margin-top:3px}}
.ag{{position:absolute;right:72px;top:64px;width:120px;z-index:4}}
.bk{{position:relative;z-index:3;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.bk h1{{font-family:'IS';font-weight:400;font-size:220px;line-height:1;letter-spacing:-.03em}}
.bk img{{width:150px;margin:50px 0 30px}}
.bk p{{font-size:17px;opacity:.9}}
.ar{{display:grid;grid-template-columns:1fr 1fr;gap:20px 22px;position:relative;z-index:3}}
.ar>div{{display:flex;gap:18px;align-items:center;background:#fff;border-radius:20px;padding:14px}}
.ar img{{width:140px;height:140px;border-radius:14px;object-fit:cover;flex:none}}
.ar h3{{font-size:23px;font-weight:600;letter-spacing:-.01em}}
.ar p{{font-size:13.5px;line-height:1.4;margin-top:3px;opacity:.75}}
.ar span{{display:inline-block;margin-top:8px;background:{YEL};font-size:12.5px;font-weight:700;padding:3px 9px;border-radius:6px}}
.hd.sm{{margin-bottom:26px}}.hd.sm h1{{font-size:64px}}
.cmp .c{{height:240px}}.cmp .c .ph{{height:104px}}.cmp .cb{{padding:11px 18px 13px}}.cmp .c h3{{font-size:23px}}
.dn{{display:grid;grid-template-columns:1fr 1fr;gap:30px 30px;position:relative;z-index:3}}
.dn>div{{border-top:1.5px solid rgba(255,255,255,.35);padding-top:16px}}
.dn b{{font-size:15px;color:{YEL};font-weight:700}}
.dn h3{{font-size:27px;font-weight:600;line-height:1.15;margin:6px 0 10px;letter-spacing:-.01em}}
.dn p{{font-size:17px;line-height:1.5;opacity:.85}}
.ph2{{display:grid;grid-template-columns:1fr 1fr;gap:22px;position:relative;z-index:3}}
.ph2>div{{background:#fff;border-radius:24px;padding:24px 26px}}
.ph2 h2{{font-family:'IS';font-weight:400;font-size:44px;line-height:1}}
.ph2 p{{font-size:18px;font-weight:600;margin-top:10px}}
.ph2 small{{display:block;font-size:14px;opacity:.6;margin-top:4px}}
.em{{margin-top:40px;background:{INK};color:#fff;border-radius:28px;padding:30px 34px;position:relative;z-index:3}}
.em .kick{{color:{YEL}}}
.emg{{display:flex;gap:46px;margin:14px 0 14px}}
.emg b{{display:block;font-size:84px;font-weight:800;color:{YEL};letter-spacing:-.03em;line-height:1}}
.emg span{{display:block;font-size:15px;font-weight:600;margin-top:4px}}
.em p{{font-size:15px;line-height:1.5;opacity:.75}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>São Paulo · Team Normani</title>'
            f'<style>{INTER}{CSS}</style></head><body>{"".join(PAGES)}</body></html>')
    out = B / "Sao-Paulo-Guide.html"
    out.write_text(html)
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(900)
        pg.pdf(path=str(B / "Sao-Paulo-Guide.pdf"), width="1080px", height="1350px", print_background=True)
        if "--png" in sys.argv:
            (B / "preview").mkdir(exist_ok=True)
            for i, el in enumerate(pg.query_selector_all("section.p"), 1):
                el.screenshot(path=str(B / f"preview/{i:02d}.png"))
        b.close()
    print(f"Sao-Paulo-Guide.pdf: {len(PAGES)} pages")
