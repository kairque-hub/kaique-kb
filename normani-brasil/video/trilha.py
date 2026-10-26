#!/usr/bin/env python3
"""Trilha original do vídeo (R&B escuro, meio tempo sobre 122 BPM): Rhodes, pad, 808, clap e hi-hats.
Tudo sintetizado aqui com numpy, sem samples nem direitos de terceiros.

make(path, dur, drop, breakdown, outro, dings) grava um WAV estéreo:
  drop       início da batida cheia (fim da abertura)
  breakdown  a bateria sai e fica só teclado e pad (agradecimento dela)
  outro      a batida volta suave no fechamento
  dings      instantes do "barulhinho" (ápice do gráfico)
"""
import wave
import numpy as np

SR = 44100
BEAT = 60 / 122
STEP = BEAT / 4                     # semicolcheia
BAR = BEAT * 4
rng = np.random.default_rng(7)

# Fm9 | Dbmaj9 | Bbm9 | C7(b9)  (MIDI)
CHORDS = [([53, 56, 60, 63, 67], 41), ([49, 53, 56, 60, 63], 37), ([46, 49, 53, 56, 60], 34), ([48, 52, 55, 58, 61], 36)]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
    return e


def lowpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def highpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (1 / np.sqrt(1 + (fc / np.maximum(f, 1)) ** 4)), len(x))


def rhodes(m, n, vel=0.5):
    t = np.arange(n) / SR
    f = hz(m)
    idx = 1.8 * np.exp(-t / 0.35) + 0.25
    tone = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    tine = 0.18 * np.sin(2 * np.pi * f * 7.02 * t) * np.exp(-t / 0.05)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.2 * t)
    return vel * (tone + tine) * env(n, 0.004, 1.9) * trem


def pad(ms, n):
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            ph = 2 * np.pi * hz(m + det) * t + rng.uniform(0, 6.28)
            x += (2 * ((ph / (2 * np.pi)) % 1) - 1) * 0.2
    x = lowpass(x, 900)
    fade = np.minimum(np.minimum(t / 0.5, 1), np.minimum((n / SR - t) / 0.4, 1))
    return x * fade * 0.08


def kick808(m, n):
    t = np.arange(n) / SR
    f = hz(m) * (1 + 2.2 * np.exp(-t / 0.025))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 0.75)
    click = np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.004) * 0.3
    return np.tanh(2.2 * x) * 0.9 + click


def clap(n):
    t = np.arange(n) / SR
    noise = highpass(rng.standard_normal(n), 900)
    e = sum(np.exp(-np.maximum(t - k * 0.009, 0) / (0.008 if k < 2 else 0.12)) * (t >= k * 0.009) for k in range(3))
    body = np.sin(2 * np.pi * 210 * t) * np.exp(-t / 0.05) * 0.4
    return (noise * e * 0.16 + body) * 0.8


def hat(n, open_=False):
    t = np.arange(n) / SR
    x = highpass(rng.standard_normal(n), 8500)
    return x * np.exp(-t / (0.09 if open_ else 0.014)) * 0.16


def chime(n):
    """o "barulhinho": arpejo de sino brilhante + brilho"""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for i, m in enumerate([84, 88, 91, 96, 100]):
        o = int(i * 0.045 * SR)
        tt = t[: n - o]
        f = hz(m)
        bell = np.sin(2 * np.pi * f * tt + 1.2 * np.exp(-tt / 0.3) * np.sin(2 * np.pi * f * 3.5 * tt))
        x[o:] += bell * np.exp(-tt / 0.9) * (0.5 - i * 0.06)
    sparkle = highpass(rng.standard_normal(n), 9000) * np.exp(-t / 0.35) * 0.08
    return x + sparkle


def reverb(x, secs=2.2, decay=0.55, seed=1):
    r = np.random.default_rng(seed)
    n = int(secs * SR)
    ir = r.standard_normal(n) * np.exp(-np.arange(n) / SR / decay)
    ir = lowpass(ir, 6000)
    ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[: len(x)]
    return y


def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def make(path, dur, drop, breakdown, outro, dings=()):
    n = int((dur + 0.5) * SR)
    keys, pads, drums, bass, fx = (np.zeros(n) for _ in range(5))
    nbars = int(dur / BAR) + 2
    for b in range(nbars):
        t0 = b * BAR
        ms, root = CHORDS[b % 4]
        for k, m in enumerate(ms):                       # acorde de Rhodes levemente arpejado
            place(keys, rhodes(m, int(2.4 * SR), 0.22 + 0.03 * k), t0 + k * 0.012)
        place(keys, rhodes(ms[-1] + 12, int(1.0 * SR), 0.12), t0 + 10 * STEP)   # resposta no contratempo
        place(pads, pad(ms, int(BAR * SR) + 2000), t0)
        full = drop <= t0 < breakdown or t0 >= outro
        if t0 < drop:
            continue
        for s in range(16):                              # hats em colcheia, rolos no fim de cada 2 compassos
            ts = t0 + s * STEP
            if s % 2 == 0:
                place(drums, hat(int(0.2 * SR)), ts, 0.55 * (1 if s % 4 == 0 else 0.7) * rng.uniform(.85, 1))
            if b % 2 == 1 and s >= 13 and full:
                for r in range(2):
                    place(drums, hat(int(0.1 * SR)), ts + r * STEP / 2, 0.35)
        if not full:
            continue
        place(drums, hat(int(0.4 * SR), True), t0 + 14 * STEP, 0.3)
        place(drums, clap(int(0.5 * SR)), t0 + 8 * STEP, 0.9)              # meio tempo: clap no 3
        for s, lv in [(0, 1.0), (7, 0.75), (10, 0.85)]:                   # 808 seguindo a fundamental
            place(bass, kick808(root - 12 if s else root - 12, int(0.9 * SR)), t0 + s * STEP, lv)
    # subida antes do drop
    sw = int(BAR * SR)
    swell = highpass(rng.standard_normal(sw), 3000) * np.linspace(0, 1, sw) ** 3 * 0.12
    place(fx, swell, drop - BAR)
    for d in dings:
        place(fx, chime(int(2.5 * SR)), d, 0.9)
    wet = reverb(keys * 0.7 + pads + drums * 0.04 + fx * 0.8)
    mix = keys * 1.3 + pads * 1.2 + drums + bass * 0.75 + fx + wet * 0.35
    st = np.stack([mix + 0.08 * reverb(keys, seed=2), mix + 0.08 * reverb(keys, seed=3)], 1)
    t = np.arange(n) / SR
    st *= np.minimum(1, np.maximum(0, (dur - t) / 2.5))[:, None]          # fade final
    st = np.tanh(st * 0.9)
    st /= np.abs(st).max() / 0.89
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st[: int(dur * SR)] * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    import sys
    make(sys.argv[1] if len(sys.argv) > 1 else "trilha.wav", 30, BAR * 2, 20, 26, [12.0])
