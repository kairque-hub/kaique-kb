#!/usr/bin/env python3
"""Gera os PDFs do Instituto Vanessa da Mata.

Uso: python3 build.py [loccitane|generico] [--png DIR]
"""
import glob, pathlib, sys
from playwright.sync_api import sync_playwright

B = pathlib.Path(__file__).parent
DECKS = {
    "loccitane": ("loccitane.html", "Instituto-Vanessa-da-Mata-x-LOccitane.pdf"),
    "generico": ("generico.html", "Instituto-Vanessa-da-Mata-Oportunidades-de-marca.pdf"),
}
alvo = [a for a in sys.argv[1:] if a in DECKS] or list(DECKS)
png_dir = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
css = "\n".join((B/"fontes"/f).read_text() for f in ["intertight.css", "instrument.css", "caslon.css"]) + "\n" + (B/"deck.css").read_text()
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    for k in alvo:
        src, out = DECKS[k]
        build = B/f".{k}.build.html"
        build.write_text((B/src).read_text().replace("/*{{CSS}}*/", css))
        pg = b.new_page(viewport={"width": 1200, "height": 675})
        erros = []
        pg.on("pageerror", lambda e: erros.append(str(e)))
        pg.goto(build.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        if png_dir:
            d = pathlib.Path(png_dir)/k; d.mkdir(parents=True, exist_ok=True)
            for i in range(pg.evaluate("document.querySelectorAll('.page').length")):
                pg.locator(".page").nth(i).screenshot(path=str(d/f"{i+1:02d}.png"))
        pg.emulate_media(media="print")
        pg.pdf(path=str(B/out), width="1200px", height="675px", print_background=True, prefer_css_page_size=True)
        pg.close(); build.unlink()
        if erros:
            print("ERROS JS:", erros); sys.exit(1)
        print(f"{out}: {(B/out).stat().st_size/1024/1024:.2f} MB")
    b.close()
