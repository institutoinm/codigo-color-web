"""Renderiza una composición de Remotion y la deja en el estándar del estudio.

Remotion entrega yuvj420p y sin normalizar el sonido; aquí se re-encapsula a H.264 yuv420p
(rango limitado, el que esperan Instagram/TikTok), AAC 48 kHz y -14 LUFS, y se pasa el QC.
También sirve para generar rótulos con transparencia (ProRes 4444) que el editor superpone.

Uso:
  python remotion_render.py TituloINM --props '{"titulo":"¿QUÉ ES UN PIGMENTO?"}' --salida 08_FINALES/titulo.mp4
  python remotion_render.py TituloINMTransparente --alfa --props '{"titulo":"GANCHO"}' --salida 05_RECURSOS/vfx/gancho.mov
Licencia: Remotion es gratis para particulares y empresas de hasta 3 empleados; con 4 o más
personas en total hace falta licencia de empresa (ver HERRAMIENTAS-INSTALADAS.md).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from comun import D, RAIZ, cargar_estilo, ffmpeg, log, registrar_error

PROYECTO = D["herramientas"] / "remotion-inm"


def navegador() -> list[str]:
    """Usa un Chrome Headless Shell ya instalado si se indica; si no, Remotion descarga el suyo."""
    ruta = os.environ.get("REMOTION_BROWSER") or ""
    if not ruta:
        cand = Path("/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
        ruta = str(cand) if cand.exists() else ""
    return [f"--browser-executable={ruta}"] if ruta else []


def render(composicion: str, props: dict, salida: Path, alfa: bool = False, qc_final: bool = True) -> Path:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        raise SystemExit("Falta Node.js/npx. Ejecuta el instalador.")
    estilo = cargar_estilo()
    c = estilo["marca"]["colores"]
    props = {"colorPrimario": c["primario"], "colorSecundario": c["secundario"], "colorResalte": c["resalte"], **props}
    salida = salida if salida.is_absolute() else RAIZ / salida
    salida.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        bruto = Path(tmp) / ("r.mov" if alfa else "r.mp4")
        args = [npx, "remotion", "render", "src/index.ts", composicion, str(bruto), f"--props={json.dumps(props, ensure_ascii=False)}",
                *navegador()]
        args += ["--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png"] if alfa else \
                ["--codec=h264", "--crf=16", "--audio-codec=aac"]
        log(f"Remotion: renderizando {composicion}…")
        r = subprocess.run(args, cwd=PROYECTO, capture_output=True, text=True)
        if r.returncode != 0:
            registrar_error("remotion render", r.stderr[-1500:] or r.stdout[-1500:])
            raise RuntimeError("Remotion falló; detalle en 11_INFORMES/registro_errores.log")
        if alfa:
            shutil.copy2(bruto, salida)
        else:
            from comun import info_video
            from editar import loudnorm_2pasos

            dur_v = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                                          "-of", "csv=p=0", str(bruto)], capture_output=True, text=True).stdout.split(",")[0])
            norm = loudnorm_2pasos(["-i", bruto], "[0:a]anull", estilo)
            ffmpeg(["-i", bruto, "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
                    "-af", f"{norm},aresample=48000", "-t", f"{dur_v:.3f}", "-ar", "48000",
                    "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", salida], "normalizar salida Remotion")
    log(f"Listo: {salida.relative_to(RAIZ) if salida.is_relative_to(RAIZ) else salida}")
    if qc_final and not alfa:
        import qc

        qc.ejecutar(salida, None, sincronia=False, salida=D["informes"] / f"{salida.stem}_QC.json")
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("composicion")
    ap.add_argument("--props", default="{}")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--alfa", action="store_true", help="ProRes 4444 con transparencia, para superponer")
    a = ap.parse_args()
    render(a.composicion, json.loads(a.props), a.salida, a.alfa)
