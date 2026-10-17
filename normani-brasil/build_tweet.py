#!/usr/bin/env python3
"""Ideia de tweet "Brazil, I'm MOTIVADED": uma página em formato story (1080x1920), no visual do guia de SP."""
import base64, glob, pathlib, sys

B = pathlib.Path(__file__).parent
G = B.parent / "sao-paulo-guide"
F = lambda p: base64.b64encode(p.read_bytes()).decode()
U = lambda p, m="image/jpeg": f"data:{m};base64," + F(p)
INTER = (B / "fontes/inter.css").read_text()
SERIF_I, SERIF_N = F(B / "fontes/InstrumentSerif-italic.woff2"), F(B / "fontes/InstrumentSerif-normal.woff2")
BG = U(G / "img/_bg.jpg")
AG = U(G / "img/_agency.png", "image/png")
GAGA = U(B / "img/gaga-avatar.jpg")
NORM = U(B / "img/avatar.jpg")
GRN, YEL, INK, CREAM = "#13B04B", "#F2EC1A", "#0B0B0C", "#F4F1E6"

VF = ('<svg class="vf" viewBox="0 0 24 24"><path fill="#1D9BF0" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91C2.63 9.33 1.75 10.57 1.75 12s.88 2.67 2.19 3.34c-.46 1.39-.2 2.9.81 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.46 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34z"/>'
      '<path fill="#fff" d="M10.1 16.3l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>')


def tweet(av, name, handle, body, meta, cls=""):
    return (f'<div class="tw {cls}"><div class="who"><img src="{av}"><div><b>{name} {VF}</b><span>@{handle}</span></div>'
            f'<svg class="x" viewBox="0 0 24 24"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.2l-4.9-6.4L6.3 22H3.2l7.3-8.3L1 2h6.4l4.4 5.8zM17.8 20h1.7L6.3 3.9H4.5z"/></svg></div>'
            f'<p class="bd">{body}</p><p class="mt">{meta}</p></div>')


GAGA_T = "Brazil, I’m devastated that I’m not well enough 2 come to Rock In Rio. I would do anything 4 u but I have to take care of my body right now."
NORM_T = ("<mark>Brasil, I’m not devastated. I’m MOTIVADED.</mark> Nem acredito que estou aqui depois de tanto tempo. "
          "Cheguei aqui ouvindo músicas de várias artistas pretinhas tipo Duquesa, Budah, Iza. Quem mais preciso ouvir? "
          "Mal posso esperar pro show amanhã. Amo vocês ❤️")
NORM_EN = ("Brazil, I’m not devastated. I’m MOTIVADED! I can’t believe I’m finally here after so long. I landed listening to "
           "some amazing Black Brazilian girlies like Duquesa, Budah, and IZA. Who else should I be listening to? "
           "I can’t wait for tomorrow’s show. Love y’all ❤️")

WHY = [("Flips a national meme", "Gaga’s 2017 cancellation tweet became Brazil’s go-to opener for bad news. Normani turns it into good news."),
       ("Miss Motivation", "Brazilian fans already call her Miss Motivation. “MOTIVADED” is her song and the meme in one word."),
       ("Brings other fandoms in", "Duquesa, Budah and IZA are safe picks: no controversies, strong fanbases. Their fans will share it too."),
       ("Asks a question", "“Who else should I be listening to?” invites thousands of replies, and Brazilian Twitter loves to answer.")]

HTML = f"""
<section class="p">
  <div class="top" style="background-image:url({BG})">
    <img class="ag" src="{AG}">
    <span class="kick">Content idea · Arrival tweet</span>
    <h1>Brazil, I’m<br><i>MOTIVADED.</i></h1>
    <p class="lead">One tweet, posted when she lands. A Brazilian meme flipped into a love letter to the fans.</p>
  </div>
  <div class="body">
    <div class="step"><span class="n">01 · The meme</span>
      {tweet(GAGA, "Lady Gaga", "ladygaga", GAGA_T, "Sep 14, 2017 · Rock in Rio cancellation", "old")}
      <p class="note">Since then, Brazilians open every piece of bad news online with <b>“Brazil, I’m devastated.”</b></p>
    </div>
    <div class="step"><span class="n">02 · The flip</span>
      {tweet(NORM, "Normani", "Normani", NORM_T, "Arrival day · São Paulo · simulation", "new")}
      <p class="en"><small>EN</small>{NORM_EN}</p>
    </div>
    <div class="step"><span class="n">03 · Why it works</span>
      <div class="why">{"".join(f'<div><h3>{t}</h3><p>{x}</p></div>' for t, x in WHY)}</div>
    </div>
    <div class="bet"><b>Huge viral potential.</b> Brazilian pop pages and press will pick it up within hours.</div>
  </div>
</section>"""

CSS = f"""
@font-face{{font-family:'IS';font-style:italic;src:url(data:font/woff2;base64,{SERIF_I})}}
@font-face{{font-family:'IS';font-style:normal;src:url(data:font/woff2;base64,{SERIF_N})}}
*{{margin:0;padding:0;box-sizing:border-box}}
@page{{size:1080px 1920px;margin:0}}
body{{font-family:Inter,sans-serif;color:{INK}}}
.p{{width:1080px;height:1920px;position:relative;overflow:hidden;background:{CREAM}}}
.top{{position:relative;height:600px;background-size:cover;background-position:center 40%;color:#fff;padding:84px 72px 0}}
.ag{{position:absolute;right:72px;top:70px;width:118px}}
.kick{{font-size:16px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{YEL}}}
h1{{font-family:'IS';font-weight:400;font-size:132px;line-height:.92;letter-spacing:-.02em;margin-top:30px}}
h1 i{{color:{YEL}}}
.lead{{font-size:23px;line-height:1.4;margin-top:26px;max-width:800px}}
.body{{padding:60px 72px 0}}
.step{{margin-bottom:50px}}
.n{{display:block;font-size:14px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{GRN};margin-bottom:14px}}
.tw{{background:#fff;border-radius:24px;padding:24px 28px;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
.tw.old{{opacity:.92}}
.tw.new{{border:3px solid {YEL}}}
.who{{display:flex;align-items:center;gap:14px}}
.who img{{width:58px;height:58px;border-radius:50%;object-fit:cover}}
.who b{{display:flex;align-items:center;gap:6px;font-size:21px}}
.who span{{font-size:17px;color:#536471}}
.vf{{width:21px;height:21px}}
.x{{width:26px;height:26px;margin-left:auto;fill:{INK}}}
.bd{{font-size:23px;line-height:1.42;margin-top:14px}}
.bd mark{{background:{YEL};padding:0 4px;border-radius:4px}}
.mt{{font-size:15px;color:#536471;margin-top:12px}}
.note{{font-size:18px;line-height:1.45;margin-top:14px;opacity:.8}}
.en{{font-size:16px;line-height:1.5;margin-top:14px;opacity:.7;font-style:italic}}
.en small{{font-style:normal;font-size:11px;font-weight:800;letter-spacing:.1em;border:1.5px solid {INK};border-radius:5px;padding:1px 6px;margin-right:8px;vertical-align:2px}}
.why{{display:grid;grid-template-columns:1fr 1fr;gap:16px 26px}}
.why div{{border-top:2px solid {INK};padding-top:10px}}
.why h3{{font-size:21px;font-weight:600}}
.why p{{font-size:15.5px;line-height:1.45;margin-top:5px;opacity:.8}}
.bet{{background:{GRN};color:#fff;border-radius:22px;padding:22px 28px;font-size:21px;line-height:1.4}}
.bet b{{color:{YEL}}}
"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Brazil, I’m MOTIVADED</title><style>{INTER}{CSS}</style></head><body>{HTML}</body></html>'
    out = B / "Tweet-Motivaded.html"
    out.write_text(html)
    exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(out.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.screenshot(path=str(B / "Tweet-Motivaded.png"))
        pg.pdf(path=str(B / "Tweet-Motivaded.pdf"), width="1080px", height="1920px", print_background=True)
        b.close()
    print("ok")
