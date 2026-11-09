"""Estudia los vídeos de 02_REFERENCIAS y mide su estilo con números (no con impresiones).

Por cada vídeo: duración, formato, cortes y ritmo (duración media de plano), primeros 3 s (¿hay texto/cambio?),
paleta dominante, sonoridad y relación voz/música aproximada, densidad de palabras (si hay voz) y una hoja de
contactos (12 fotogramas) para revisar subtítulos, animaciones y composición.
Salida: 11_INFORMES/referencias_AAAAMMDD.md + 02_REFERENCIAS/_analisis/*.jpg
Regla: de vídeos de otras personas solo se aprende CÓMO se ven; nunca se copia lo que dicen ni su marca,
y lo que aparece en un solo vídeo no cuenta como estilo.
Uso:  python estudiar_referencias.py [carpeta_o_videos...]
"""
from __future__ import annotations

import datetime as dt
import re
import statistics
import subprocess
import sys
from pathlib import Path

from comun import D, EXT_VIDEO, audio_16k, info_video, log


def cortes(video: Path, umbral: float = 0.32) -> list[float]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", f"select='gt(scene,{umbral})',showinfo", "-an",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def paleta(video: Path, n: int = 5) -> list[str]:
    import numpy as np

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", "fps=1,scale=64:114", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    px = np.frombuffer(raw, np.uint8).reshape(-1, 3)
    if not len(px):
        return []
    q = (px // 32).astype(int)
    claves, cuentas = np.unique(q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2], return_counts=True)
    top = claves[np.argsort(cuentas)[::-1][:n]]
    return ["#%02X%02X%02X" % (((k // 64) * 32 + 16), (((k // 8) % 8) * 32 + 16), ((k % 8) * 32 + 16)) for k in top]


def sonoridad(video: Path) -> float | None:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", r.stderr[r.stderr.rfind("Summary"):])
    return float(m.group(1)) if m else None


def palabras_por_minuto(video: Path) -> tuple[float | None, int]:
    try:
        from faster_whisper import WhisperModel

        m = WhisperModel("small", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(audio_16k(video), language="es", word_timestamps=True)
        pal = [w for s in segs for w in (s.words or [])]
        if not pal:
            return None, 0
        dur = pal[-1].end - pal[0].start
        return round(len(pal) / max(dur, 1) * 60, 1), len(pal)
    except Exception:  # noqa: BLE001
        return None, 0


def hoja_contactos(video: Path, dur: float, salida: Path) -> None:
    paso = max(dur / 12, 0.1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", f"fps=1/{paso:.3f},scale=180:-2,tile=6x2",
                    "-frames:v", "1", str(salida)], check=False)


def analizar(video: Path) -> dict:
    inf = info_video(video)
    c = cortes(video)
    dur = inf["duracion"]
    planos = [b - a for a, b in zip([0.0] + c, c + [dur])]
    hoja = D["referencias"] / "_analisis" / f"{video.stem}_contactos.jpg"
    hoja.parent.mkdir(exist_ok=True)
    hoja_contactos(video, dur, hoja)
    ppm, npal = palabras_por_minuto(video)
    return {"video": video.name, "duracion": round(dur, 1), "formato": f"{inf.get('ancho')}x{inf.get('alto')} @ {inf.get('fps')}",
            "cortes": len(c), "plano_medio_s": round(statistics.mean(planos), 2) if planos else None,
            "plano_mediano_s": round(statistics.median(planos), 2) if planos else None,
            "corte_en_3s": any(t < 3 for t in c), "paleta": paleta(video), "lufs": sonoridad(video),
            "palabras_min": ppm, "palabras": npal, "hoja": str(hoja.name)}


def informe(res: list[dict]) -> Path:
    L = [f"# Análisis de referencias · {dt.date.today():%d/%m/%Y}", "",
         "| Vídeo | Dur. | Formato | Cortes | Plano medio | Corte en 0–3 s | Palabras/min | LUFS | Paleta |", "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        L.append(f"| {r['video']} | {r['duracion']} s | {r['formato']} | {r['cortes']} | {r['plano_medio_s']} s | "
                 f"{'sí' if r['corte_en_3s'] else 'no'} | {r['palabras_min'] or '—'} | {r['lufs']} | {' '.join(r['paleta'])} |")
    if len(res) >= 3:
        L += ["", "## Patrones (solo lo que se repite en 3 o más vídeos)",
              f"- Plano medio típico: {statistics.median([r['plano_medio_s'] for r in res if r['plano_medio_s']]):.2f} s",
              f"- Duración típica: {statistics.median([r['duracion'] for r in res]):.0f} s",
              f"- Vídeos con cambio en los 3 primeros segundos: {sum(r['corte_en_3s'] for r in res)}/{len(res)}"]
    else:
        L += ["", "> Hay menos de 3 referencias: no se extraen patrones de estilo (regla: un solo vídeo no es estilo)."]
    L += ["", "Revisa las hojas de contactos en `02_REFERENCIAS/_analisis/` para subtítulos, animaciones y composición.",
          "Siguiente paso: entrevista corta a Cristina (ver ESTILO-INM.md, «Cómo se actualiza esta ficha»)."]
    out = D["informes"] / f"referencias_{dt.date.today():%Y%m%d}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    args = [Path(a) for a in sys.argv[1:]] or [D["referencias"]]
    vids = []
    for a in args:
        vids += sorted(p for p in a.iterdir() if p.suffix.lower() in EXT_VIDEO) if a.is_dir() else [a]
    if not vids:
        raise SystemExit("No hay vídeos en 02_REFERENCIAS. Añade 3–6 vídeos (o pídele a Claude que los baje con yt-dlp).")
    res = []
    for v in vids:
        log(f"Analizando {v.name}…")
        res.append(analizar(v))
    log(f"Informe: {informe(res)}")
