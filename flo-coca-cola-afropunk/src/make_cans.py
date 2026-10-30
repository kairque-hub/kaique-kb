#!/usr/bin/env python3
"""Desenha as latas ilustrativas (Original e Zero Cafeína) em PNG transparente."""
import pathlib, re, subprocess

B = pathlib.Path(__file__).parent
logo = (B/"ext/coca-cola-logo.svg").read_text()
path = re.search(r'<path[^>]*d="([^"]+)"', logo).group(1)

def lata(nome, corpo, corpo2, tinta, faixa, rodape, tam=12):
    return f'''<svg id="{nome}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 400" width="440" height="800">
<defs>
 <linearGradient id="c{nome}" x1="0" x2="1"><stop offset="0" stop-color="{corpo2}"/><stop offset=".22" stop-color="{corpo}"/>
  <stop offset=".38" stop-color="#fff" stop-opacity=".18"/><stop offset=".46" stop-color="{corpo}"/><stop offset="1" stop-color="{corpo2}"/></linearGradient>
 <linearGradient id="m{nome}" x1="0" x2="1"><stop offset="0" stop-color="#8a8f96"/><stop offset=".35" stop-color="#f4f6f8"/><stop offset=".6" stop-color="#b8bec5"/><stop offset="1" stop-color="#6d7279"/></linearGradient>
 <linearGradient id="s{nome}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".3" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></linearGradient>
 <clipPath id="k{nome}"><rect x="10" y="30" width="200" height="340" rx="14"/></clipPath>
</defs>
<path d="M30 30 Q34 8 60 6 H160 Q186 8 190 30 Z" fill="url(#m{nome})"/>
<ellipse cx="110" cy="8" rx="52" ry="5" fill="#c9ced4"/>
<g clip-path="url(#k{nome})">
 <rect x="10" y="30" width="200" height="340" fill="{corpo}"/>
 <rect x="10" y="30" width="200" height="340" fill="url(#c{nome})"/>
 <path d="M10 312 C70 292 140 340 210 300 V318 C140 360 70 312 10 334 Z" fill="{faixa}"/>
 <g transform="translate(72 290) rotate(-90) scale(.39)"><path d="{path}" fill="{tinta}"/></g>
 <text x="110" y="358" text-anchor="middle" font-family="Inter" font-weight="800" font-size="{tam}" letter-spacing="1" fill="{tinta}">{rodape}</text>
 <rect x="10" y="30" width="200" height="340" fill="url(#s{nome})"/>
</g>
<path d="M10 360 Q12 388 40 392 H180 Q208 388 210 360 Z" fill="url(#m{nome})"/>
</svg>'''

html = "<html><body style='margin:0;background:transparent'>" + \
    lata("original", "#e61d2b", "#9e0d16", "#fff", "#fff", "ORIGINAL") + \
    lata("zero", "#1a1a1a", "#000", "#d6b25e", "#d6b25e", "ZERO AÇÚCAR · ZERO CAFEÍNA", 9.5) + "</body></html>"
tmp = B/"ext/latas.build.html"
tmp.write_text(html)
subprocess.run(["node", str(B/"render.js"), "shot", str(tmp),
                f"#original={B/'ext/lata-original.png'}", f"#zero={B/'ext/lata-zero.png'}"], check=True)
print("ok")
