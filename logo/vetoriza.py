#!/usr/bin/env python3
"""Vetoriza a logo brasil.ir (traços + ponto azul) e exporta SVG, PDF e PNG em alta, com fundo transparente."""
import numpy as np, potrace, cairosvg
from PIL import Image

SRC = "/tmp/claude-0/-home-user-kaique-kb/8d897b1c-61f5-59e3-ab02-292ee75b492b/images/40.png"
a = np.array(Image.open(SRC).convert("RGB").resize((432 * 4, 454 * 4), Image.LANCZOS)).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
blue = (b - r > 60) & (b > 120)
ink = (a.mean(-1) < 110) & ~blue


def paths(mask):
    bm = potrace.Bitmap(~mask)  # potracer traça os pixels False
    pl = bm.trace(turdsize=40, alphamax=1.1, opticurve=True, opttolerance=0.3)
    d = []
    for c in pl:
        s = c.start_point
        d.append(f"M{s.x:.1f},{s.y:.1f}")
        for seg in c.segments:
            if seg.is_corner:
                d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
            else:
                d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        d.append("Z")
    return "".join(d)


ys, xs = np.where(ink | blue)
pad = 20
x0, y0, x1, y1 = xs.min() - pad, ys.min() - pad, xs.max() + pad, ys.max() + pad
P_INK, P_BLUE = paths(ink), paths(blue)
W, H = x1 - x0, y1 - y0
BLUE = "#2A4FBF"
for nome, cor in (("preto", "#0B0B0C"), ("branco", "#FFFFFF")):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {W} {H}" width="{W}" height="{H}">'
           f'<path fill="{cor}" fill-rule="evenodd" d="{P_INK}"/><path fill="{BLUE}" d="{P_BLUE}"/></svg>')
    open(f"brasil-ir-{nome}.svg", "w").write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=f"brasil-ir-{nome}.pdf")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"brasil-ir-{nome}.png", output_width=4000)
print("ok", W, H)
