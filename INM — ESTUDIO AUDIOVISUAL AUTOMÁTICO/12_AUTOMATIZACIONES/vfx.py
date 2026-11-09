"""BIBLIOTECA VFX LOCAL del INM (sin servicios de pago). Cada efecto es una función y un comando.

  texto-detras   Texto grande que pasa POR DETRÁS de Cristina (rotoscopia automática con rembg u2net_human_seg)
  mini           Mini-Cristina / duplicación: recorta a la persona y la coloca a escala con sombra de contacto
  dividida       Pantalla dividida (dos tomas o técnica A/B) con rótulos
  crash-zoom     Zoom cinematográfico de impacto con desenfoque de movimiento
  particulas     Partículas de pigmento sobre el plano (capa generada, color de marca)

Todos trabajan sobre 1080x1920, conservan el audio y escriben en 07_RENDERS/vfx/. Ejemplos:
  python vfx.py texto-detras ENTRADA.mp4 --texto "PIGMENTO" --desde 1 --hasta 3
  python vfx.py mini ENTRADA.mp4 --desde 0 --hasta 3 --escala 0.38 --x 0.72 --y 0.80
  python vfx.py dividida A.mp4 B.mp4 --rotulo-a "PELO A PELO" --rotulo-b "POWDER"
  python vfx.py crash-zoom ENTRADA.mp4 --en 1.2
  python vfx.py particulas ENTRADA.mp4 --desde 0.5 --hasta 2.5
Lo que NO es: no es 3D real. Son composiciones 2D/2,5D. El 3D real (folículo, capas de piel giratorias,
cámara virtual) requiere Blender o un servicio generativo: ver 03_ESTILO_INM/BIBLIOTECA-VFX.md.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from comun import D, FUENTES, cargar_estilo, ffmpeg, hex_a_rgb, info_video, log

W, H = 1080, 1920
SALIDA = D["renders"] / "vfx"


def _frames(video: Path, t0: float, t1: float, fps: int):
    """Generador de fotogramas RGB (numpy) del tramo [t0, t1]."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", str(video), "-vf", f"scale={W}:{H},fps={fps}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.wait()


class Escritor:
    def __init__(self, ruta: Path, fps: int):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                   "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "fast",
                                   "-pix_fmt", "yuv420p", str(ruta)], stdin=subprocess.PIPE)

    def __call__(self, fr: np.ndarray):
        self.p.stdin.write(np.ascontiguousarray(fr, dtype=np.uint8).tobytes())

    def cerrar(self):
        self.p.stdin.close()
        self.p.wait()


class Mascara:
    """Rotoscopia automática de personas (rembg u2net_human_seg), a media resolución para ir rápido."""

    def __init__(self):
        from rembg import new_session

        self.s = new_session("u2net_human_seg")

    def __call__(self, fr: np.ndarray) -> np.ndarray:
        from PIL import Image
        from rembg import remove

        peq = Image.fromarray(fr).resize((W // 2, H // 2))
        m = remove(peq, session=self.s, only_mask=True, post_process_mask=True)
        m = np.asarray(m.resize((W, H), Image.BILINEAR), dtype=np.float32) / 255.0
        return m[..., None]


def _componer_tramo(video: Path, t0: float, t1: float, fn, nombre: str) -> Path:
    """Aplica fn(fotograma, índice, mascara) al tramo y lo vuelve a insertar en el vídeo completo con su audio."""
    inf = info_video(video)
    fps = int(round(inf.get("fps", 30)))
    SALIDA.mkdir(parents=True, exist_ok=True)
    out = SALIDA / f"{video.stem}_{nombre}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        tramo = Path(tmp) / "tramo.mp4"
        esc = Escritor(tramo, fps)
        for i, fr in enumerate(_frames(video, t0, t1, fps)):
            esc(fn(fr.copy(), i, fps))
        esc.cerrar()
        dur = inf["duracion"]
        partes, filtros, k = [], [], 0
        ent = ["-i", video, "-i", tramo]
        if t0 > 0.01:
            filtros.append(f"[0:v]trim=0:{t0},setpts=PTS-STARTPTS,scale={W}:{H},fps={fps},setsar=1[p{k}]")
            partes.append(f"[p{k}]")
            k += 1
        filtros.append(f"[1:v]setpts=PTS-STARTPTS,fps={fps},setsar=1[p{k}]")
        partes.append(f"[p{k}]")
        k += 1
        if t1 < dur - 0.01:
            filtros.append(f"[0:v]trim={t1}:{dur},setpts=PTS-STARTPTS,scale={W}:{H},fps={fps},setsar=1[p{k}]")
            partes.append(f"[p{k}]")
            k += 1
        filtros.append(f"{''.join(partes)}concat=n={k}:v=1:a=0[v]")
        ffmpeg([*ent, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out], f"vfx {nombre}")
    log(f"VFX «{nombre}» → {out}")
    return out


def _texto_rgba(texto: str, tam: int, color: tuple, contorno: tuple | None = None):
    from PIL import Image, ImageDraw, ImageFont

    f = ImageFont.truetype(str(FUENTES / "Montserrat-Black.ttf"), tam)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), texto, font=f, stroke_width=6 if contorno else 0)
    im = Image.new("RGBA", (x1 - x0 + 20, y1 - y0 + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - x0, 10 - y0), texto, font=f, fill=color + (255,),
                            stroke_width=6 if contorno else 0, stroke_fill=(contorno + (255,)) if contorno else None)
    return np.asarray(im, dtype=np.float32) / 255.0


def texto_detras(video: Path, texto: str, desde: float, hasta: float, y_rel: float = 0.33) -> Path:
    """Texto gigante en el fondo; la persona queda por delante gracias a la máscara."""
    estilo = cargar_estilo()
    color = hex_a_rgb(estilo["marca"]["colores"]["texto"])
    rotos = Mascara()
    # Tamaño máximo que cabe en el ancho
    tam = 330
    while True:
        capa = _texto_rgba(texto, tam, color)
        if capa.shape[1] <= W - 60 or tam < 80:
            break
        tam -= 10
    th, tw = capa.shape[:2]
    x0, y0 = (W - tw) // 2, int(H * y_rel - th / 2)

    def fn(fr, i, fps):
        t = i / fps
        a = min(1.0, t / 0.35) * min(1.0, max(0.0, (hasta - desde - t) / 0.3))
        sube = int((1 - min(1.0, t / 0.35)) * 80)
        m = rotos(fr)
        base = fr.astype(np.float32) / 255.0
        lienzo = base.copy()
        yy0 = max(0, y0 + sube)
        reg = lienzo[yy0:yy0 + th, x0:x0 + tw]
        cap = capa[: reg.shape[0], : reg.shape[1]]
        alfa = cap[..., 3:4] * a
        reg[:] = reg * (1 - alfa) + cap[..., :3] * alfa
        out = lienzo * (1 - m) + base * m  # la persona (m=1) vuelve a quedar delante
        return (out * 255).clip(0, 255)

    return _componer_tramo(video, desde, hasta, fn, "texto_detras")


def mini(video: Path, desde: float, hasta: float, escala: float = 0.38, x_rel: float = 0.74, y_rel: float = 0.84) -> Path:
    """Mini-Cristina: la misma toma recortada, reducida, con sombra de contacto (sin alterar rasgos)."""
    from PIL import Image, ImageFilter

    rotos = Mascara()

    def fn(fr, i, fps):
        t = i / fps
        m = rotos(fr)
        rgba = np.concatenate([fr.astype(np.float32) / 255.0, m], axis=2)
        im = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
        bbox = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
        base = Image.fromarray(fr).convert("RGBA")
        if not bbox:
            return np.asarray(base.convert("RGB"))
        persona = im.crop(bbox)
        aparece = min(1.0, t / 0.4)
        e = escala * (0.7 + 0.3 * aparece)
        pw, ph = max(2, int(persona.width * e)), max(2, int(persona.height * e))
        persona = persona.resize((pw, ph), Image.LANCZOS)
        px, py = int(W * x_rel - pw / 2), int(H * y_rel - ph)
        # sombra de contacto: elipse desenfocada bajo los pies
        sombra = Image.new("RGBA", (pw, max(8, ph // 10)), (0, 0, 0, 0))
        from PIL import ImageDraw

        ImageDraw.Draw(sombra).ellipse((pw * 0.1, 0, pw * 0.9, sombra.height), fill=(0, 0, 0, int(120 * aparece)))
        sombra = sombra.filter(ImageFilter.GaussianBlur(8))
        base.alpha_composite(sombra, (px, py + ph - sombra.height // 2))
        a = persona.getchannel("A").point(lambda v: int(v * aparece))
        persona.putalpha(a)
        base.alpha_composite(persona, (px, py))
        return np.asarray(base.convert("RGB"))

    return _componer_tramo(video, desde, hasta, fn, "mini")


def dividida(a: Path, b: Path, rotulo_a: str = "", rotulo_b: str = "", dur: float | None = None) -> Path:
    estilo = cargar_estilo()
    c = estilo["marca"]["colores"]
    SALIDA.mkdir(parents=True, exist_ok=True)
    out = SALIDA / f"{a.stem}_dividida.mp4"
    d = dur or min(info_video(a)["duracion"], info_video(b)["duracion"])
    fd = str(FUENTES / "Montserrat-Black.ttf").replace("\\", "/").replace(":", r"\:")
    txt = lambda t, y: (f",drawtext=fontfile='{fd}':text='{t}':fontsize=64:fontcolor=white:borderw=5:bordercolor=0x{c['contorno'].lstrip('#')}"  # noqa: E731
                        f":x=(w-text_w)/2:y={y}") if t else ""
    ffmpeg(["-i", a, "-i", b, "-filter_complex",
            f"[0:v]scale={W}:-2,crop={W}:{H//2}{txt(rotulo_a, 60)}[a];[1:v]scale={W}:-2,crop={W}:{H//2}{txt(rotulo_b, 60)}[b];"
            f"[a][b]vstack,drawbox=x=0:y={H//2-3}:w={W}:h=6:color=0x{c['resalte'].lstrip('#')}:t=fill,format=yuv420p[v]",
            "-map", "[v]", "-map", "0:a?", "-t", f"{d:.2f}", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", out], "vfx dividida")
    log(f"VFX «dividida» → {out}")
    return out


def crash_zoom(video: Path, en: float, dur: float = 0.45, factor: float = 1.6) -> Path:
    """Zoom de impacto: acerca de 1x a factor en `dur` s con desenfoque de movimiento, y mantiene."""
    inf = info_video(video)
    fps = int(round(inf.get("fps", 30)))
    SALIDA.mkdir(parents=True, exist_ok=True)
    out = SALIDA / f"{video.stem}_crashzoom.mp4"
    z = f"if(lt(t,{en}),1,min({factor},1+({factor}-1)*pow((t-{en})/{dur},0.6)))"
    ffmpeg(["-i", video, "-filter_complex",
            f"[0:v]scale={W}:{H},setsar=1,scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame,"
            f"crop={W}:{H}:(in_w-{W})/2:(in_h-{H})*0.35,tmix=frames=3:weights='1 2 1',fps={fps},format=yuv420p[v]",
            "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-c:a", "copy", out], "vfx crash-zoom")
    log(f"VFX «crash-zoom» → {out}")
    return out


def particulas(video: Path, desde: float, hasta: float, n: int = 160) -> Path:
    """Partículas de pigmento que ascienden y brillan (determinista, color de resalte de marca)."""
    estilo = cargar_estilo()
    col = np.array(hex_a_rgb(estilo["marca"]["colores"]["resalte"]), dtype=np.float32) / 255.0
    rng = np.random.default_rng(3)
    px, py = rng.uniform(0, W, n), rng.uniform(H * 0.35, H * 1.05, n)
    vel, rad, fase = rng.uniform(60, 220, n), rng.uniform(2, 7, n), rng.uniform(0, 6.28, n)
    yy, xx = np.mgrid[0:H, 0:W]

    def fn(fr, i, fps):
        t = i / fps
        capa = np.zeros((H, W), np.float32)
        ys = py - vel * t
        for k in range(n):
            x, y, r = int(px[k] + 18 * np.sin(t * 2 + fase[k])), int(ys[k]), rad[k]
            if 0 <= y < H:
                x0, x1, y0, y1 = max(0, x - 12), min(W, x + 12), max(0, y - 12), min(H, y + 12)
                d2 = (xx[y0:y1, x0:x1] - x) ** 2 + (yy[y0:y1, x0:x1] - y) ** 2
                capa[y0:y1, x0:x1] = np.maximum(capa[y0:y1, x0:x1], np.exp(-d2 / (2 * r * r)) * (0.6 + 0.4 * np.sin(t * 6 + fase[k])))
        env = min(1.0, t / 0.3) * min(1.0, max(0.0, (hasta - desde - t) / 0.4))
        a = (capa * env)[..., None]
        base = fr.astype(np.float32) / 255.0
        out = 1 - (1 - base) * (1 - a * col)  # mezcla «pantalla»
        return (out * 255).clip(0, 255)

    return _componer_tramo(video, desde, hasta, fn, "particulas")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("texto-detras"); p.add_argument("video", type=Path); p.add_argument("--texto", required=True)
    p.add_argument("--desde", type=float, default=0); p.add_argument("--hasta", type=float, default=2.5); p.add_argument("--y", type=float, default=0.33)
    p = sp.add_parser("mini"); p.add_argument("video", type=Path); p.add_argument("--desde", type=float, default=0)
    p.add_argument("--hasta", type=float, default=3); p.add_argument("--escala", type=float, default=0.38)
    p.add_argument("--x", type=float, default=0.74); p.add_argument("--y", type=float, default=0.84)
    p = sp.add_parser("dividida"); p.add_argument("a", type=Path); p.add_argument("b", type=Path)
    p.add_argument("--rotulo-a", default=""); p.add_argument("--rotulo-b", default="")
    p = sp.add_parser("crash-zoom"); p.add_argument("video", type=Path); p.add_argument("--en", type=float, required=True)
    p = sp.add_parser("particulas"); p.add_argument("video", type=Path); p.add_argument("--desde", type=float, default=0)
    p.add_argument("--hasta", type=float, default=2.5)
    a = ap.parse_args()
    if a.cmd == "texto-detras":
        texto_detras(a.video, a.texto, a.desde, a.hasta, a.y)
    elif a.cmd == "mini":
        mini(a.video, a.desde, a.hasta, a.escala, a.x, a.y)
    elif a.cmd == "dividida":
        dividida(a.a, a.b, a.rotulo_a, a.rotulo_b)
    elif a.cmd == "crash-zoom":
        crash_zoom(a.video, a.en)
    else:
        particulas(a.video, a.desde, a.hasta)
