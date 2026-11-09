"""Deja el estudio listo: descarga modelos, guías de herramientas y comprueba que todo responde.

Lo llaman los instaladores (instalar.ps1 / instalar.sh) y también puede ejecutarse a mano:
    python 12_AUTOMATIZACIONES/preparar.py            (todo)
    python 12_AUTOMATIZACIONES/preparar.py --comprobar (solo comprobar, sin descargar)
Es idempotente: si algo ya está, no lo vuelve a descargar.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import urllib.request

from comun import D, MODELOS, log, registrar_error

REPOS = {
    "reels-montage": "https://github.com/itpartypattaya/reels-montage.git",
    "hyperframes": "https://github.com/heygen-com/hyperframes.git",
    "remotion-skills": "https://github.com/remotion-dev/skills.git",
    "yt-dlp": "https://github.com/yt-dlp/yt-dlp.git",
}
YUNET = "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"


def paso(nombre, fn, comprobar_solo):
    try:
        r = fn(comprobar_solo)
        log(f"✔ {nombre}: {r}")
        return True, r
    except Exception as e:  # noqa: BLE001
        registrar_error(f"preparar/{nombre}", str(e), "revisar SOLUCION-DE-ERRORES.md")
        log(f"✘ {nombre}: {e}")
        return False, str(e)


def whisper(c):
    from faster_whisper import WhisperModel

    if c and not any((MODELOS / "hf").rglob("model.bin")):
        return "falta el modelo (ejecuta sin --comprobar)"
    WhisperModel("small", device="cpu", compute_type="int8")
    return "modelo small listo"


def rembg_m(c):
    ruta = MODELOS / "u2net" / "models" / "u2net_human_seg"
    if c:
        return "presente" if ruta.exists() or (MODELOS / "u2net" / "u2net_human_seg.onnx").exists() else "falta"
    from rembg import new_session

    new_session("u2net_human_seg")
    return "u2net_human_seg listo"


def yunet(c):
    dst = MODELOS / "yunet" / "face_detection_yunet_2023mar.onnx"
    if not dst.exists() and not c:
        dst.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(YUNET, dst)
    return f"{'presente' if dst.exists() else 'falta'} ({dst.stat().st_size if dst.exists() else 0} bytes)"


def repos(c):
    base = D["herramientas"] / "repos"
    base.mkdir(exist_ok=True)
    estado = {}
    for n, url in REPOS.items():
        d = base / n
        if not d.exists() and not c:
            subprocess.run(["git", "clone", "--depth", "1", url, str(d)], check=True, capture_output=True)
        estado[n] = "ok" if d.exists() else "falta"
    return estado


def remotion(c):
    d = D["herramientas"] / "remotion-inm"
    if not (d / "node_modules" / "remotion").exists() and not c:
        npm = shutil.which("npm") or shutil.which("npm.cmd")
        subprocess.run([npm, "install", "--no-audit", "--no-fund"], cwd=d, check=True)
    return "instalado" if (d / "node_modules" / "remotion").exists() else "falta"


def binarios(_c):
    out = {}
    for b in ["ffmpeg", "ffprobe", "node", "git"]:
        p = shutil.which(b)
        if p:
            v = subprocess.run([b, "-version" if b.startswith("ff") else "--version"], capture_output=True, text=True).stdout.splitlines()[0]
            out[b] = v[:60]
        else:
            out[b] = "NO ENCONTRADO"
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--comprobar", action="store_true")
    a = ap.parse_args()
    res = {}
    for n, f in [("binarios", binarios), ("whisper", whisper), ("rembg", rembg_m), ("yunet", yunet),
                 ("repositorios", repos), ("remotion", remotion)]:
        res[n] = paso(n, f, a.comprobar)
    (D["informes"] / "estado_herramientas.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    fallos = [n for n, (ok, _) in res.items() if not ok]
    print("\nTODO LISTO" if not fallos else f"\nPENDIENTE: {', '.join(fallos)} (ver 11_INFORMES/registro_errores.log)")
