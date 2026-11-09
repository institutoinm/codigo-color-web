"""Prueba de funcionamiento: MP4 real de 5 s, 1080x1920, texto animado, transición y efectos de sonido.

Genera 08_FINALES/PRUEBA_INM_5s_vN.mp4 (H.264 + AAC) y su informe en 11_INFORMES.
Escena A (0–2,6 s): fondo degradado + título que entra con escala y desenfoque + «pop».
Transición (2,3–2,9 s): barrido xfade (smoothleft) + «whoosh».
Escena B (2,6–5 s): partículas de pigmento + rótulo + «brillo».
Uso:  python prueba_5s.py
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from comun import D, FUENTES, cargar_estilo, ffmpeg, hex_a_ass, log, ruta_filtro, siguiente_version
import qc

W, H, FPS = 1080, 1920, 30


def ass_prueba(estilo: dict) -> str:
    c = estilo["marca"]["colores"]
    blanco, resalte, contorno = hex_a_ass(c["texto"]), hex_a_ass(c["resalte"]), hex_a_ass(c["contorno"])
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat Black,120,{blanco},{blanco},{contorno},&H64000000,0,0,0,0,100,100,0,0,1,6,0,5,60,60,0,1
Style: Sub,Montserrat SemiBold,64,{resalte},{resalte},{contorno},&H64000000,0,0,0,0,100,100,2,0,1,4,0,5,60,60,0,1
Style: Rotulo,Montserrat ExtraBold,96,{blanco},{blanco},{contorno},&H64000000,0,0,0,0,100,100,0,0,1,5,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.15,0:00:02.55,Titulo,,0,0,0,,{{\\pos(540,880)\\fscx60\\fscy60\\blur12\\alpha&HFF&\\t(0,380,\\fscx104\\fscy104\\blur0\\alpha&H00&)\\t(380,560,\\fscx100\\fscy100)\\t(2100,2400,\\alpha&HFF&)}}ESTUDIO INM
Dialogue: 1,0:00:00.55,0:00:02.55,Sub,,0,0,0,,{{\\pos(540,1030)\\alpha&HFF&\\t(0,400,\\alpha&H00&)\\t(1700,2000,\\alpha&HFF&)}}edición automática
Dialogue: 1,0:00:02.75,0:00:04.85,Rotulo,,0,0,0,,{{\\move(540,1060,540,960,0,450)\\alpha&HFF&\\t(0,450,\\alpha&H00&)\\t(1900,2100,\\alpha&HFF&)}}PRUEBA OK
Dialogue: 1,0:00:03.05,0:00:04.85,Sub,,0,0,0,,{{\\pos(540,1090)\\alpha&HFF&\\t(0,350,\\alpha&H00&)\\t(1600,1800,\\alpha&HFF&)}}1080 × 1920 · H.264 · AAC
"""


def main() -> Path:
    estilo = cargar_estilo()
    c = estilo["marca"]["colores"]
    v = siguiente_version("PRUEBA_INM_5s")
    salida = D["finales"] / f"PRUEBA_INM_5s_v{v}.mp4"
    sfx = D["recursos"] / "sfx"
    if not (sfx / "whoosh.wav").exists():
        raise SystemExit("Faltan los SFX: ejecuta primero  python sfx.py")
    with tempfile.TemporaryDirectory() as tmp:
        ass = Path(tmp) / "prueba.ass"
        ass.write_text(ass_prueba(estilo), encoding="utf-8")
        p1, p2 = c["primario"].lstrip("#"), c["secundario"].lstrip("#")
        filtro = (
            # Escena A: degradado vertical animado
            f"[0:v]format=rgb24,geq=r='lerp(0x{p1[0:2]},0x{p2[0:2]},Y/H*0.9+0.1*sin(T*1.5))':"
            f"g='lerp(0x{p1[2:4]},0x{p2[2:4]},Y/H*0.9+0.1*sin(T*1.5))':b='lerp(0x{p1[4:6]},0x{p2[4:6]},Y/H*0.9+0.1*sin(T*1.5))',"
            f"format=yuv420p[a];"
            # Escena B: fondo oscuro + partículas (ruido umbralizado que asciende) en tono de resalte
            f"[1:v]format=gray,geq=lum='if(gt(random(1)*255,252),255,0)',boxblur=2:1,"
            f"scroll=vertical=-0.004,format=rgb24,colorchannelmixer=rr=0.55:gg=0.75:bb=1.0,format=gbrp[part];"
            f"[2:v]format=gbrp[fondo];[fondo][part]blend=all_mode=screen,format=yuv420p[b];"
            f"[a][b]xfade=transition=smoothleft:duration=0.6:offset=2.3,"
            f"subtitles=filename='{ruta_filtro(ass)}':fontsdir='{ruta_filtro(FUENTES)}',format=yuv420p[v];"
            # Audio: pop 0,15 s · whoosh 2,25 s · brillo 2,8 s
            f"[3:a]adelay=150|150,volume=0.8[s1];[4:a]adelay=2250|2250[s2];[5:a]adelay=2800|2800,volume=0.7[s3];"
            f"[6:a][s1][s2][s3]amix=inputs=4:normalize=0:duration=first,volume=-2.1dB,alimiter=limit=0.84:level=false[au]"
        )
        ffmpeg([
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=2.9",
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=2.7",
            "-f", "lavfi", "-i", f"color=c=0x{c['contorno'].lstrip('#')}:s={W}x{H}:r={FPS}:d=2.7",
            "-i", sfx / "pop.wav", "-i", sfx / "whoosh.wav", "-i", sfx / "brillo.wav",
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo:d=5",
            "-filter_complex", filtro, "-map", "[v]", "-map", "[au]",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", "5", "-movflags", "+faststart", salida,
        ], "prueba 5s render")
    log(f"Render creado: {salida}")
    informe = D["informes"] / f"{salida.stem}_QC.json"
    rep = qc.ejecutar(salida, None, sincronia=False, salida=informe)
    # Comprobaciones específicas de la prueba
    extra = {"duracion_ok": abs(rep["metadatos"]["duracion"] - 5.0) < 0.05,
             "fotogramas_esperados": 5 * FPS, "fotogramas_ok": rep["decodificacion"]["fotogramas_leidos"] == 5 * FPS}
    extra["sfx_en_su_sitio"] = medir_sfx(salida)
    rep["prueba"] = extra
    informe.write_text(json.dumps(rep, indent=2, ensure_ascii=False, default=qc._js), encoding="utf-8")
    print(json.dumps(extra, indent=2, ensure_ascii=False))
    return salida


def medir_sfx(path: Path) -> dict:
    """Comprueba la sincronía: el audio debe arrancar donde se programaron los efectos."""
    import subprocess

    import numpy as np

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<f4")
    win = 480  # 10 ms
    n = len(x) // win
    rms = np.sqrt(np.mean(x[: n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    # Ataque = subida de >6 dB respecto al mínimo de los 60 ms previos y por encima de -50 dBFS
    ataques = []
    for i in range(6, n):
        if db[i] > -50 and db[i] - db[i - 6:i].min() > 6 and (not ataques or i * 0.01 - ataques[-1] > 0.2):
            ataques.append(round(i * 0.01, 3))
    esperados = [0.15, 2.25, 2.80]
    res = {"ataques_detectados_s": ataques}
    for e in esperados:
        cerca = min(ataques, key=lambda f: abs(f - e)) if ataques else None
        res[f"{e:.2f}s"] = {"detectado": cerca, "ok": cerca is not None and abs(cerca - e) <= 0.06}
    return res


if __name__ == "__main__":
    main()
