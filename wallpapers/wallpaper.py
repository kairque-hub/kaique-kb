#!/usr/bin/env python3
"""Wallpaper de iPad, quadrado 2752x2752 (funciona em pé e deitado).
Degradê em malha verde, amarelo e azul profundo, com grão de filme."""
import numpy as np
from PIL import Image

N = 2752
rng = np.random.default_rng(7)
y, x = np.mgrid[0:N, 0:N].astype(np.float32) / N

# malha: cada ponto puxa sua cor, com peso que cai rápido (cores ficam puras, transições suaves)
pts = [(0.08, 0.05, (6, 70, 48)),       # verde mata escuro
       (0.92, 0.12, (246, 222, 52)),    # amarelo
       (0.62, 0.30, (255, 168, 40)),    # âmbar
       (0.18, 0.55, (14, 150, 86)),     # verde
       (0.95, 0.62, (20, 110, 150)),    # azul petróleo
       (0.50, 0.95, (6, 38, 92)),       # azul profundo
       (0.05, 0.95, (4, 46, 40))]       # verde quase preto
acc = np.zeros((N, N, 3), np.float32); wsum = np.zeros((N, N, 1), np.float32)
xw = x + 0.07 * np.sin(y * 5.2 + 1.3) + 0.03 * np.sin(y * 11 + x * 4)   # leve distorção, deixa o degradê orgânico
yw = y + 0.07 * np.sin(x * 4.6 + 0.4) + 0.03 * np.sin(x * 9 - y * 5)
for cx, cy, c in pts:
    d2 = (xw - cx) ** 2 + (yw - cy) ** 2
    w = (1 / (d2 + 0.006) ** 1.35)[..., None]
    acc += w * (np.array(c, np.float32) / 255); wsum += w
img = acc / wsum

# vinheta leve e grão
v = 1 - 0.28 * (((x - .5) ** 2 + (y - .5) ** 2) * 2)[..., None]
img = img * v + rng.normal(0, 0.018, (N, N, 1)).astype(np.float32)
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save("ipad-brasil.png", optimize=True)
print("ok")
