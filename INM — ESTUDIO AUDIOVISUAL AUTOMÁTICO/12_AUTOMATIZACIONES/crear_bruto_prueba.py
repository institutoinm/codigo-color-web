"""Crea un BRUTO DE PRUEBA para comprobar el editor sin usar grabaciones reales.

· Voz: síntesis local Piper (es_ES «davefx»). SOLO para pruebas internas: nunca se publica
  y no imita a Cristina (regla: voces sintéticas solo con autorización).
· Imagen: «astronaut» de scikit-image (foto de la NASA, dominio público), en horizontal 1920x1080
  para probar el reencuadre vertical centrado en el rostro.
· Contiene a propósito: silencios largos, una muletilla («eh») y una frase repetida (toma fallida),
  para verificar que el editor los detecta y elimina.
Salida: 01_BRUTOS/DEMO_bruto_prueba.mp4
"""
from __future__ import annotations

import tempfile
import wave
from pathlib import Path

from comun import D, MODELOS, ffmpeg, info_video, log

GUION = [
    ("Hola. Esto es una prueba del editor automático del Instituto.", 0.4),
    ("Eh.", 1.3),
    ("Hoy probamos cómo se cortan los silencios.", 0.9),
    ("Hoy probamos cómo se cortan los silencios y las frases repetidas.", 1.1),
    ("Cuando digo pigmento, aparece un rótulo en pantalla.", 0.5),
    ("Y cuando hablo de la piel, también.", 1.4),
    ("Al final, el cierre lleva la web del Instituto.", 0.8),
]


def main() -> Path:
    from piper import PiperVoice
    from skimage import data
    from PIL import Image

    voz = PiperVoice.load(str(MODELOS / "piper" / "es_ES-davefx-medium.onnx"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        partes = []
        for i, (frase, pausa) in enumerate(GUION):
            f = tmp / f"f{i}.wav"
            with wave.open(str(f), "wb") as w:
                voz.synthesize_wav(frase, w)
            partes += [f"file '{f}'", f"file '{tmp / f'p{i}.wav'}'"]
            ffmpeg(["-f", "lavfi", "-i", f"anullsrc=r={voz.config.sample_rate}:cl=mono", "-t", str(pausa), tmp / f"p{i}.wav"], "silencio")
        lista = tmp / "lista.txt"
        lista.write_text("\n".join(partes), encoding="utf-8")
        voz_wav = tmp / "voz.wav"
        # 0,6 s de aire al principio + ruido de sala leve para que parezca una grabación real
        ffmpeg(["-f", "concat", "-safe", "0", "-i", lista, "-af", "adelay=600,aresample=48000", voz_wav], "concat voz")
        img = tmp / "persona.png"
        Image.fromarray(data.astronaut()).save(img)
        salida = D["brutos"] / "DEMO_bruto_prueba.mp4"
        dur = info_video(voz_wav)["duracion"] + 0.5
        ffmpeg([
            "-loop", "1", "-i", img, "-i", voz_wav,
            "-f", "lavfi", "-i", "anoisesrc=c=pink:a=0.004:r=48000",
            "-filter_complex",
            "[0:v]split[a][b];[a]scale=1920:1080,boxblur=30:5,eq=brightness=-0.08[fondo];"
            "[b]scale=-2:1000[p];[fondo][p]overlay=x=260+40*sin(t/3):y=40,format=yuv420p,fps=30[v];"
            "[1:a][2:a]amix=inputs=2:normalize=0:duration=first[au]",
            "-map", "[v]", "-map", "[au]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "fast",
            "-c:a", "aac", "-b:a", "160k", salida], "bruto de prueba")
    log(f"Bruto de prueba creado: {salida}")
    return salida


if __name__ == "__main__":
    main()
