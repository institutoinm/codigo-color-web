"""Utilidades comunes del estudio INM: rutas, ejecución de comandos, ffprobe y registro.

Todo el estudio se resuelve a partir de la carpeta raíz «INM — ESTUDIO AUDIOVISUAL AUTOMÁTICO»,
así que la carpeta puede moverse a otro disco u ordenador sin tocar el código.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = {
    "brutos": RAIZ / "01_BRUTOS",
    "referencias": RAIZ / "02_REFERENCIAS",
    "estilo": RAIZ / "03_ESTILO_INM",
    "guiones": RAIZ / "04_GUIONES",
    "recursos": RAIZ / "05_RECURSOS",
    "proyectos": RAIZ / "06_PROYECTOS",
    "renders": RAIZ / "07_RENDERS",
    "finales": RAIZ / "08_FINALES",
    "portadas": RAIZ / "09_PORTADAS",
    "subtitulos": RAIZ / "10_SUBTITULOS",
    "informes": RAIZ / "11_INFORMES",
    "auto": RAIZ / "12_AUTOMATIZACIONES",
    "herramientas": RAIZ / "_HERRAMIENTAS",
}
FUENTES = D["recursos"] / "fuentes"
MODELOS = D["herramientas"] / "modelos"
VENV_PY = D["herramientas"] / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REGISTRO = D["informes"] / "registro_errores.log"
EXT_VIDEO = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm", ".mts", ".3gp"}

# Variables de entorno para que los modelos se guarden dentro del estudio (portabilidad).
os.environ.setdefault("HF_HOME", str(MODELOS / "hf"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("U2NET_HOME", str(MODELOS / "u2net"))


def ahora() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    print(f"[INM {ahora()}] {msg}", flush=True)


def registrar_error(contexto: str, detalle: str, recuperacion: str = "") -> None:
    """Deja constancia de cada fallo y de cómo se recuperó (SOLUCION-DE-ERRORES)."""
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open("a", encoding="utf-8") as f:
        f.write(f"{ahora()} | {contexto} | {detalle.strip()[:2000]}")
        if recuperacion:
            f.write(f" | RECUPERACIÓN: {recuperacion}")
        f.write("\n")


def run(cmd: list[str], contexto: str = "", check: bool = True, capturar: bool = True) -> subprocess.CompletedProcess:
    """Ejecuta un comando sin shell (sin inyecciones) y registra el error si falla."""
    cmd = [str(c) for c in cmd]
    r = subprocess.run(cmd, capture_output=capturar, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        registrar_error(contexto or cmd[0], (r.stderr or "")[-1500:])
        raise RuntimeError(f"Falló «{contexto or cmd[0]}» (código {r.returncode}).\n{(r.stderr or '')[-1500:]}")
    return r


def ffmpeg(args: list, contexto: str = "ffmpeg") -> subprocess.CompletedProcess:
    return run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], contexto)


def probe(path: Path) -> dict:
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path], "ffprobe")
    return json.loads(r.stdout)


def info_video(path: Path) -> dict:
    p = probe(path)
    v = next((s for s in p["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
    out = {"duracion": float(p["format"].get("duration", 0)), "formato": p["format"].get("format_name")}
    if v:
        num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "30/1").split("/")
        fps = float(num) / float(den) if float(den) else 30.0
        w, h = int(v["width"]), int(v["height"])
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(sd["rotation"])
        rot = int(v.get("tags", {}).get("rotate", rot) or rot)
        if abs(rot) in (90, 270):
            w, h = h, w
        out.update(ancho=w, alto=h, fps=round(fps, 3), vcodec=v.get("codec_name"), pix_fmt=v.get("pix_fmt"),
                   nb_frames=int(v["nb_frames"]) if str(v.get("nb_frames", "")).isdigit() else None,
                   perfil=v.get("profile"), rotacion=rot)
    if a:
        out.update(acodec=a.get("codec_name"), sample_rate=int(a.get("sample_rate", 0)), canales=a.get("channels"))
    return out


def sha256(path: Path, bloque: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(bloque), b""):
            h.update(b)
    return h.hexdigest()


def slug(texto: str, maxlen: int = 40) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
    return (t or "video")[:maxlen]


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9ñ ]+", "", t).strip()


def cargar_estilo() -> dict:
    with (D["estilo"] / "estilo_inm.json").open(encoding="utf-8") as f:
        return json.load(f)


def siguiente_version(base: str) -> int:
    """Nunca sobrescribe: busca el siguiente _vN libre en 08_FINALES."""
    n = 1
    while (D["finales"] / f"{base}_v{n}.mp4").exists():
        n += 1
    return n


def ultimo_bruto() -> Path:
    vids = [p for p in D["brutos"].iterdir() if p.suffix.lower() in EXT_VIDEO and not p.name.startswith(".")]
    if not vids:
        raise FileNotFoundError("No hay vídeos en 01_BRUTOS.")
    return max(vids, key=lambda p: p.stat().st_mtime)


def hex_a_ass(hex_color: str, alfa: int = 0) -> str:
    """#RRGGBB → &HAABBGGRR (formato de color de ASS)."""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alfa:02X}{b}{g}{r}".upper()


def hex_a_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def ruta_filtro(p: Path) -> str:
    """Escapa una ruta para usarla dentro de un filtro de FFmpeg (subtitles=..., fontsdir=...)."""
    s = str(p).replace("\\", "/")
    return s.replace(":", r"\:").replace("'", r"\'").replace(",", r"\,").replace("[", r"\[").replace("]", r"\]")


def comprobar_dependencias() -> dict:
    res = {}
    for b in ["ffmpeg", "ffprobe", "node", "npx"]:
        res[b] = shutil.which(b) is not None
    res["python_venv"] = VENV_PY.exists()
    return res


if __name__ == "__main__":
    print(json.dumps(comprobar_dependencias(), indent=2, ensure_ascii=False))
    sys.exit(0)
