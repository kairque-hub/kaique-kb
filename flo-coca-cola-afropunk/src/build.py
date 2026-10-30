#!/usr/bin/env python3
"""Monta o deck FLO × Coca-Cola (HTML com tudo embutido) e gera o PDF."""
import base64, io, pathlib, re, subprocess
from PIL import Image

B = pathlib.Path(__file__).parent
IMG = B.parent/"img"

def uri(p, maxw=1100):
    p = pathlib.Path(p)
    if p.suffix == ".png":
        im = Image.open(p); im.thumbnail((maxw, maxw*2))
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    im = Image.open(p).convert("RGB"); im.thumbnail((maxw, maxw*2))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=84)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

logo = (B/"ext/coca-cola-logo.svg").read_text().replace("#e61d2b", "#ffffff")
LOGO_BRANCO = "data:image/svg+xml;base64," + base64.b64encode(logo.encode()).decode()

def foot(n):
    return (f'<div class="foot"><span></span><div class="r"><span>FLO × Coca-Cola · AFROPUNK Bahia</span>'
            f'<span class="n">{n}</span><img src="{uri(IMG/"logo-brasileiro.png", 300)}"></div></div>')

def membro(img, nome, arroba, seg, txt):
    return f'''<div class="card" style="padding:14px 14px 22px">
  <div style="height:330px;border-radius:20px;overflow:hidden"><img src="{uri(IMG/img)}" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%"></div>
  <div class="anton" style="font-size:44px;margin:16px 6px 8px">{nome}</div>
  <div style="margin:0 6px"><span class="chip on">{arroba}</span><span class="chip" style="background:var(--red);color:#fff">{seg}</span></div>
  <p style="font-size:16px;line-height:1.45;color:#444;margin:4px 6px 0">{txt}</p></div>'''

def faixa(nome, txt):
    return (f'<div style="display:flex;align-items:center;border-bottom:1px solid #eee;padding:9px 0">'
            f'<div class="anton" style="font-size:34px;width:230px;color:var(--red)">{nome}</div>'
            f'<div style="font-size:19px;color:#333">{txt}</div></div>')

def dia(quando, titulo, a1, t1, a2, t2, hi):
    hi = hi.strip()
    bg = "background:var(--ink);color:#fff" if hi else ""
    sub = "color:rgba(255,255,255,.8)" if hi else "color:#555"
    cap = "color:#fff;opacity:.7" if hi else "color:var(--red)"
    bloco2 = (f'<div style="border-top:1px solid {"#444" if hi else "#e5e5e5"};margin-top:14px;padding-top:14px">'
              f'<div style="font-weight:700;font-size:19px">{a2}</div><div style="font-size:15px;{sub};margin-top:4px">{t2}</div></div>') if a2 else ""
    return f'''<div class="card" style="padding:24px;height:330px;{bg}">
  <div class="cap" style="{cap}">{quando}</div>
  <div class="anton" style="font-size:40px;margin-top:6px;padding-bottom:12px;border-bottom:2px solid {"#444" if hi else "#e5e5e5"}">{titulo}</div>
  <div style="margin-top:14px;font-weight:700;font-size:19px">{a1}</div><div style="font-size:15px;{sub};margin-top:4px;line-height:1.4">{t1}</div>{bloco2}</div>'''

def cena(img, num, titulo, txt):
    return f'''<div>
  <div class="photo" style="position:relative;height:380px;border-width:7px"><img src="{uri(IMG/img)}">
    <div class="sticker" style="left:12px;top:12px;font-size:20px;padding:6px 12px;border-radius:10px">{num}</div></div>
  <div style="font-weight:700;font-size:20px;margin-top:20px">{titulo}</div>
  <div style="font-size:15px;line-height:1.4;margin-top:6px;color:rgba(255,255,255,.88)">{txt}</div></div>'''

def post(img, user, legenda):
    return f'''<div>
  <div class="photo" style="position:relative;height:410px;border-width:7px"><img src="{uri(IMG/img)}">
    <div style="position:absolute;left:16px;top:14px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.7)"><div style="font-weight:700;font-size:15px">{user}</div><div style="font-size:12px">Salvador, Bahia</div></div>
    <div style="position:absolute;left:16px;bottom:16px;background:rgba(0,0,0,.65);color:#fff;font-size:13px;font-weight:600;padding:5px 11px;border-radius:8px">cocacola_br</div></div>
  <div style="text-align:center;font-size:17px;margin-top:14px">{legenda}</div></div>'''

MACROS = {"FOOT": foot, "MEMBRO": membro, "FAIXA": faixa, "DIA": dia, "CENA": cena, "POST": post}

html = (B/"deck.template.html").read_text()
html = html.replace("{{LOGO_BRANCO}}", LOGO_BRANCO)
html = re.sub(r"\{\{FONT:([^}]+)\}\}", lambda m: "data:font/ttf;base64," + base64.b64encode((B/"fonts"/m[1]).read_bytes()).decode(), html)
html = re.sub(r"\{\{IMG_EXT:([^}]+)\}\}", lambda m: uri(B/"ext"/m[1], 400), html)
html = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: uri(IMG/m[1], 1300 if m[1].endswith(".jpg") else 800), html)
html = re.sub(r"\{\{([A-Z]+):([^}]+)\}\}", lambda m: MACROS[m[1]](*m[2].split("|")), html)
assert "{{" not in html, re.findall(r"\{\{[^}]*", html)[:3]

out = B/"deck.build.html"
out.write_text(html)
pdf = B.parent/"FLO-x-CocaCola-AFROPUNK-Bahia.pdf"
subprocess.run(["node", str(B/"render.js"), "pdf", str(out), str(pdf), "1600", "900"], check=True)
print(f"{pdf.name}: {pdf.stat().st_size/1024/1024:.2f} MB")
