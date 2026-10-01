#!/usr/bin/env python3
"""Gera os PDFs dos decks (TIM MUSIC e Petra) a partir dos HTMLs.

Uso: python3 build.py [tim|petra] [--png DIR]
"""
import glob, pathlib, sys
from playwright.sync_api import sync_playwright

B = pathlib.Path(__file__).parent
DECKS = {
    "tim": ("tim.html", "TIM-MUSIC-x-Zuca-Cultura-Artistica.pdf"),
    "petra": ("petra.html", "Petra-x-Zuca-Cultura-Artistica.pdf"),
    "geral": ("geral.html", "Zuca-Cultura-Artistica-Oportunidades-de-marca.pdf"),
    "semmarca": ("geral_sem_marca.html", "Casa-da-Musica-Brasileira-Cultura-Artistica.pdf"),
}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
png_dir = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
if png_dir in args:
    args.remove(png_dir)
alvo = args or list(DECKS)

css = (B/"fontes/intertight.css").read_text() + "\n" + (B/"fontes/fraunces.css").read_text() + "\n" + (B/"fontes/instrument.css").read_text() + "\n" + (B/"fontes/notosans.css").read_text() + "\n" + (B/"deck.css").read_text()
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    for k in alvo:
        src, out = DECKS[k]
        html = (B/src).read_text().replace("/*{{CSS}}*/", css)
        build = B/f".{k}.build.html"
        build.write_text(html)
        erros = []
        pg = b.new_page(viewport={"width": 1200, "height": 675})
        pg.on("pageerror", lambda e: erros.append(str(e)))
        pg.goto(build.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        if png_dir:
            d = pathlib.Path(png_dir)/k
            d.mkdir(parents=True, exist_ok=True)
            n = pg.evaluate("document.querySelectorAll('.page').length")
            for i in range(n):
                pg.locator(".page").nth(i).screenshot(path=str(d/f"{i+1:02d}.png"))
        pg.emulate_media(media="print")
        pg.pdf(path=str(B/out), width="1200px", height="675px", print_background=True,
               prefer_css_page_size=True)
        pg.close()
        build.unlink()
        if erros:
            print("ERROS JS:", erros); sys.exit(1)
        print(f"{out}: {(B/out).stat().st_size/1024/1024:.2f} MB")
    b.close()
