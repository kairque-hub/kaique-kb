#!/usr/bin/env python3
"""Trilha do vídeo: uma faixa da Mixkit (Stock Music Free License: uso comercial em vídeo, sem crédito obrigatório)
editada para acompanhar as cenas.

A faixa é ajustada para 122 BPM (o andamento dos cortes) e recebe uma edição por cima:
  · abertura com filtro abrindo e uma subida que estoura no corte para a primeira cena
  · impactos graves nas viradas importantes (páginas do X, mapa, gráfico, números)
  · o "ding" no ápice do gráfico da conversa
  · queda no agradecimento dela (graves e batida filtrados, mais baixo) e volta cheia no fechamento
"""
import subprocess, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def load(src, start, bpm, dur):
    """trecho da faixa a partir de `start` (s, no tempo original), esticado para 122 BPM, estéreo float"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{(dur + 2) * 122 / bpm:.3f}",
                          "-af", f"atempo={122 / bpm:.5f}", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(float) / 32768
    n = int(dur * SR)
    return np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]


def lowpass(x, fc):
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    if X.ndim > 1: f = f[:, None]
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x), axis=0)


def highpass(x, fc):
    X = np.fft.rfft(x, axis=0)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1)
    if X.ndim > 1: f = f[:, None]
    return np.fft.irfft(X / np.sqrt(1 + (fc / f) ** 4), len(x), axis=0)


def sweep(x, f0, f1):
    """filtro passa-baixa que abre de f0 a f1 ao longo do trecho (blocos com sobreposição)"""
    n, blk = len(x), 4096
    out = np.zeros_like(x)
    win = np.hanning(blk)[:, None]
    for i in range(0, n, blk // 2):
        seg = x[i:i + blk]
        if len(seg) < blk: seg = np.pad(seg, ((0, blk - len(seg)), (0, 0)))
        y = lowpass(seg * win, f0 * (f1 / f0) ** min(1, i / n))
        out[i:i + blk] += y[: min(blk, n - i)]
    return out


def chime(n):
    """o "barulhinho" do ápice: arpejo de sino brilhante"""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for i, m in enumerate([84, 88, 91, 96, 100]):
        o = int(i * 0.045 * SR)
        tt = t[: n - o]
        f = hz(m)
        bell = np.sin(2 * np.pi * f * tt + 1.2 * np.exp(-tt / 0.3) * np.sin(2 * np.pi * f * 3.5 * tt))
        x[o:] += bell * np.exp(-tt / 0.9) * (0.5 - i * 0.06)
    return x + highpass(rng.standard_normal(n), 9000) * np.exp(-t / 0.35) * 0.06


def impact(n):
    t = np.arange(n) / SR
    f = 55 * (1 + 1.5 * np.exp(-t / 0.04))
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.6)
    air = highpass(rng.standard_normal(n), 2500) * np.exp(-t / 0.25) * 0.25
    return np.tanh(1.5 * boom) * 0.8 + air


def riser(n):
    t = np.arange(n) / SR
    k = (t / t[-1]) ** 2.5
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1400 * k) / SR) * 0.15
    return (highpass(rng.standard_normal(n), 1500) * 0.18 + tone) * k


def tick(n, k):
    """tique de contador, discreto e seco: clique abafado com um corpo grave curto"""
    t = np.arange(n) / SR
    click = lowpass(highpass(rng.standard_normal(n), 1200), 4500) * np.exp(-t / 0.003)
    body = np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.012)
    return click * 0.6 + body * 0.5


def reverb(x, secs=2.0, decay=0.5, seed=1):
    r = np.random.default_rng(seed)
    m = int(secs * SR)
    ir = r.standard_normal(m) * np.exp(-np.arange(m) / SR / decay)
    ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + m
    return np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[: len(x)]


def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig))
    s = sig[: j - i] * gain
    buf[i:j] += s[:, None] if s.ndim == 1 else s


def make(path, dur, src, bpm, start, drop, breakdown, outro, dings=(), hits=(), ticks=()):
    x = load(src, start, bpm, dur)
    n = len(x)
    t = np.arange(n) / SR
    i0, i1, i2 = int(drop * SR), int(breakdown * SR), int(outro * SR)
    x[:i0] = sweep(x[:i0], 350, 6000) * np.minimum(1, t[:i0, None] / 0.8)        # abertura: filtro abrindo
    if dings:                                                                    # crescente do drop até o ápice
        g = np.clip((t - drop) / max(1, dings[0] - drop), 0, 1)
        x[i0:] *= (0.62 + 0.38 * g[i0:] ** 1.3)[:, None]
    xf = 0.55 * lowpass(x[i1:i2], 650)                                           # queda no agradecimento
    xf += 0.25 * reverb(xf[:, 0])[:, None]
    k = int(0.25 * SR)
    ramp = np.linspace(0, 1, k)[:, None]
    x[i1:i1 + k] = x[i1:i1 + k] * (1 - ramp) + xf[:k] * ramp
    x[i1 + k:i2] = xf[k:]
    fx = np.zeros((n, 2))
    place(fx, riser(int(2.0 * SR)), drop - 2.0, 0.9)
    place(fx, impact(int(1.6 * SR)), drop, 1.0)
    place(fx, riser(int(1.5 * SR)), outro - 1.5, 0.6)
    place(fx, impact(int(1.6 * SR)), outro, 0.9)
    for h in hits:
        place(fx, impact(int(1.6 * SR)), h, 0.55)
    for i, tk in enumerate(ticks):
        place(fx, tick(int(0.05 * SR), 0), tk, 0.42)
    for d in dings:
        c = chime(int(2.5 * SR))
        place(fx, c, d, 0.75)
        place(fx, 0.3 * reverb(c, 2.5, 0.8, 5), d)
    mix = x * 0.9 + fx
    mix *= np.minimum(1, np.maximum(0, (dur - t) / 2.5))[:, None]               # fade final
    mix = np.tanh(mix * 1.05)
    mix /= np.abs(mix).max() / 0.89
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
