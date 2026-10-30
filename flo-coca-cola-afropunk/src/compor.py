#!/usr/bin/env python3
"""Aplica a lata ilustrativa nas fotos da FLO (cobrindo o pacote da proposta anterior quando houver)."""
import pathlib
from PIL import Image

B = pathlib.Path(__file__).parent
LATA = {k: Image.open(B/f"ext/lata-{k}.png") for k in ("original", "zero")}

# foto de origem, saída, [(lata, centro_x, base_y, largura, rotação)] em frações da imagem
CENAS = [
    ("i-040.jpg", "01-arrumando.jpg", [("original", .22, .97, .22, 8)]),
    ("i-039.jpg", "02-van.jpg",       [("original", .68, .80, .17, -10)]),
    ("i-047.jpg", "03-palco.jpg",     [("original", .205, .885, .25, -6)]),
    ("i-042.jpg", "04-mesa.jpg",      [("original", .30, .76, .17, -4), ("original", .52, .62, .13, 5), ("original", .80, .70, .15, -3)]),
    ("i-049.jpg", "05-hotel.jpg",     [("zero", .47, .975, .19, 6)]),
    ("i-052.jpg", "car-jorja.jpg",    [("original", .77, .97, .27, 7)]),
    ("i-053.jpg", "car-renee.jpg",    [("original", .74, .965, .29, -5)]),
    ("i-054.jpg", "car-stella.jpg",   [("original", .205, .96, .27, 4)]),
    ("i-041.jpg", "trio.jpg",         []),
    ("i-038.jpg", "hotel-vista.jpg",  []),
    ("i-042.jpg", "mesa-limpa.jpg",   []),
]

for src, out, latas in CENAS:
    im = Image.open(B/"raw"/src).convert("RGBA")
    W, H = im.size
    for k, cx, by, lw, rot in latas:
        w = int(W*lw); h = int(w*LATA[k].height/LATA[k].width)
        l = LATA[k].resize((w, h), Image.LANCZOS)
        # sombra suave
        sombra = Image.new("RGBA", l.size, (0, 0, 0, 0))
        sombra.putalpha(l.getchannel("A").point(lambda a: int(a*.45)))
        from PIL import ImageFilter
        sombra = sombra.filter(ImageFilter.GaussianBlur(w*.06))
        l = l.rotate(rot, expand=True, resample=Image.BICUBIC)
        sombra = sombra.rotate(rot, expand=True, resample=Image.BICUBIC)
        x = int(W*cx - l.width/2); y = int(H*by - l.height)
        im.alpha_composite(sombra, (x+int(w*.06), y+int(w*.08)))
        im.alpha_composite(l, (x, y))
    im.convert("RGB").save(B/"../img"/out, quality=88)
print("ok")
