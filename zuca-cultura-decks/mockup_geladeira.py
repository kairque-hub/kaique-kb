#!/usr/bin/env python3
"""Monta a geladeira envelopada Petra na foto do café (mockup ilustrativo).

Uso: python3 mockup_geladeira.py CAMINHO_FONTE_SERIF.ttf
Entrada: img/cafe2_balcao.jpg  ->  Saída: img/cafe2_geladeira.jpg
"""
import pathlib, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

B = pathlib.Path(__file__).parent
serif = sys.argv[1]
foto = Image.open(B/"img/cafe2_balcao.jpg").convert("RGB")
W, H = foto.size
K = 4                                    # supersampling
x0, y0, x1, y1 = 340, 392, 446, 686       # caixa da geladeira na foto (px)
w, h = (x1-x0)*K, (y1-y0)*K
pad = 40*K
lay = Image.new("RGBA", (w+2*pad, h+2*pad), (0, 0, 0, 0))
d = ImageDraw.Draw(lay)
ox, oy = pad, pad

# sombra no piso
sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
ds = ImageDraw.Draw(sh)
ds.ellipse([ox-4*K, oy+h-7*K, ox+w+22*K, oy+h+8*K], fill=(40, 25, 10, 160))
ds.polygon([(ox, oy+h), (ox+w, oy+h), (ox-10*K, oy+h+26*K), (ox-38*K, oy+h+20*K)], fill=(60, 40, 20, 70))
lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(7*K)))
d = ImageDraw.Draw(lay)

# lateral direita (perspectiva em direção ao ponto de fuga)
dp = 15*K
d.polygon([(ox+w-2*K, oy), (ox+w+dp, oy+9*K), (ox+w+dp, oy+h-5*K), (ox+w-2*K, oy+h)], fill=(18, 13, 11, 255))
d.polygon([(ox+w-2*K, oy), (ox+w+dp, oy+9*K), (ox+w+dp, oy+int(h*0.15)+7*K), (ox+w-2*K, oy+int(h*0.15))], fill=(98, 18, 18, 255))
# corpo
d.rounded_rectangle([ox, oy, ox+w, oy+h], radius=4*K, fill=(28, 20, 17, 255))
# testeira vermelha com a marca
th = int(h*0.15)
d.rounded_rectangle([ox, oy, ox+w, oy+th], radius=4*K, fill=(142, 27, 27, 255))
d.rectangle([ox, oy+th-3*K, ox+w, oy+th], fill=(120, 20, 20, 255))
f = ImageFont.truetype(serif, int(th*0.52))
txt = "PETRA"
tw = d.textlength(txt, font=f) + 4*K*(len(txt)-1)
tx = ox + (w - tw)/2
for ch in txt:
    d.text((tx, oy+th*0.2), ch, font=f, fill=(236, 214, 160, 255))
    tx += d.textlength(ch, font=f) + 4*K
# porta de vidro
gx0, gy0, gx1, gy1 = ox+6*K, oy+th+6*K, ox+w-6*K, oy+h-22*K
d.rectangle([gx0-2*K, gy0-2*K, gx1+2*K, gy1+2*K], fill=(70, 70, 72, 255))
inner = Image.new("RGBA", (gx1-gx0, gy1-gy0))
di = ImageDraw.Draw(inner)
for yy in range(inner.height):
    t = yy/inner.height
    di.line([(0, yy), (inner.width, yy)], fill=(int(46-18*t), int(40-16*t), int(36-14*t), 255))
# prateleiras com produtos
random.seed(4)
n = 5
sh_h = inner.height/n
cores_lata = [(201, 164, 92), (163, 35, 31), (200, 200, 200), (43, 43, 43), (236, 232, 222), (120, 22, 22)]
for i in range(n):
    base = int((i+1)*sh_h) - 3*K
    di.rectangle([0, base-1*K, inner.width, base+2*K], fill=(255, 244, 214, 255))      # LED
    di.rectangle([0, base-int(sh_h*0.9), inner.width, base], fill=(255, 236, 190, 18))
    x = 2*K
    garrafa = i in (0, 3)
    while x < inner.width-6*K:
        if garrafa:
            bw = 7*K; bh = int(sh_h*0.78)
            col = (88, 50, 20, 255)
            di.rounded_rectangle([x, base-int(bh*0.62), x+bw, base], radius=2*K, fill=col)
            di.rectangle([x+bw*0.35, base-bh, x+bw*0.65, base-int(bh*0.6)], fill=col)
            di.rectangle([x+1*K, base-int(bh*0.45), x+bw-1*K, base-int(bh*0.25)], fill=(236, 214, 160, 255))
            x += bw + 2*K
        else:
            bw = 8*K; bh = int(sh_h*0.5)
            c = random.choice(cores_lata)
            di.rounded_rectangle([x, base-bh, x+bw, base], radius=2*K, fill=c+(255,))
            di.rectangle([x+1*K, base-bh+2*K, x+2*K, base-2*K], fill=(255, 255, 255, 70))
            x += bw + 2*K
# reflexo diagonal no vidro
rf = Image.new("RGBA", inner.size, (0, 0, 0, 0))
ImageDraw.Draw(rf).polygon([(inner.width*0.55, 0), (inner.width*0.85, 0), (inner.width*0.2, inner.height), (-inner.width*0.1, inner.height)], fill=(255, 250, 235, 38))
inner = Image.alpha_composite(inner, rf)
lay.paste(inner, (gx0, gy0), inner)
d = ImageDraw.Draw(lay)
# puxador e rodapé
d.rounded_rectangle([gx1-5*K, gy0+int((gy1-gy0)*0.3), gx1-3*K, gy0+int((gy1-gy0)*0.62)], radius=1*K, fill=(215, 215, 215, 255))
f2 = ImageFont.truetype(serif, int(11*K))
d.text((ox+w/2, oy+h-11*K), "PETRA", font=f2, fill=(236, 214, 160, 255), anchor="mm")
# luz lateral quente vindo da janela (direita)
lz = Image.new("RGBA", lay.size, (0, 0, 0, 0))
dz = ImageDraw.Draw(lz)
for xx in range(w):
    a = int(40*max(0, (xx/w)-0.55)/0.45)
    dz.line([(ox+xx, oy), (ox+xx, oy+h)], fill=(255, 210, 140, a))
mask = Image.new("L", lay.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([ox, oy, ox+w, oy+h], radius=4*K, fill=255)
lay = Image.composite(Image.alpha_composite(lay, lz), lay, mask)

lay = lay.resize((lay.width//K, lay.height//K), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))
out = foto.convert("RGBA")
out.alpha_composite(lay, (x0-pad//K, y0-pad//K))
out.convert("RGB").save(B/"img/cafe2_geladeira.jpg", quality=92)
print("ok")
