"""Genera efectos de sonido propios (síntesis matemática, sin muestras de terceros).

Al estar creados desde cero por este script, son material original del INM: no hay licencia ajena.
Salida: 05_RECURSOS/sfx/*.wav (48 kHz, estéreo).
Uso:  python sfx.py
"""
from __future__ import annotations

import wave

import numpy as np

from comun import D, log

SR = 48000
rng = np.random.default_rng(7)


def _guardar(nombre: str, x: np.ndarray) -> None:
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    est = np.stack([x, x], axis=1)
    pcm = (est * 32767).astype("<i2")
    out = D["recursos"] / "sfx" / f"{nombre}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    log(f"SFX creado: {out.name}")


def _lp(x: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Filtro paso bajo de un polo con coeficiente variable (barrido)."""
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def whoosh(dur=0.55):
    n = int(SR * dur)
    t = np.linspace(0, 1, n)
    ruido = rng.standard_normal(n)
    barrido = 0.02 + 0.35 * np.sin(np.pi * t) ** 2
    y = _lp(ruido, barrido) - _lp(ruido, barrido * 0.15)
    env = np.sin(np.pi * t) ** 1.6
    return y * env


def impacto(dur=0.7):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 95 * np.exp(-t * 6) + 38
    fase = 2 * np.pi * np.cumsum(f) / SR
    grave = np.sin(fase) * np.exp(-t * 5.5)
    golpe = rng.standard_normal(n) * np.exp(-t * 60) * 0.5
    return grave + golpe


def pop(dur=0.12):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 25) + 420
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38)


def brillo(dur=0.9):
    n = int(SR * dur)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k, fr in enumerate([1568, 2093, 2637, 3136]):
        ini = int(k * 0.06 * SR)
        tt = t[: n - ini]
        y[ini:] += np.sin(2 * np.pi * fr * tt) * np.exp(-tt * 7) * 0.5
    return y


def tic(dur=0.05):
    n = int(SR * dur)
    t = np.arange(n) / SR
    return rng.standard_normal(n) * np.exp(-t * 180)


if __name__ == "__main__":
    for nombre, fn in [("whoosh", whoosh), ("impacto", impacto), ("pop", pop), ("brillo", brillo), ("tic", tic)]:
        _guardar(nombre, fn())
    (D["recursos"] / "sfx" / "LICENCIA.txt").write_text(
        "Efectos generados por síntesis con 12_AUTOMATIZACIONES/sfx.py. Material original del INM, sin muestras de terceros.\n",
        encoding="utf-8")
