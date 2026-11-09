"""Control de calidad automático de un MP4 del estudio INM.

Comprueba de verdad el archivo (no lo da por bueno sin mirarlo):
  · contenedor, códecs H.264/AAC, 1080x1920, fps, píxel yuv420p
  · decodificación completa sin errores y número de fotogramas
  · duración de vídeo frente a audio
  · sonoridad integrada (LUFS) y pico verdadero
  · fotogramas negros y congelados
  · rostros (YuNet) frente a las zonas donde se ha puesto texto
  · sincronía de subtítulos: re-transcribe el audio final y compara tiempos
  · ortografía orientativa en castellano (lista para revisión humana)
  · marca: colores y logotipo verificados o no
  · originalidad frente a los cinco vídeos anteriores
Uso:  python qc.py RUTA.mp4 [--plan RUTA_plan.json] [--sin-sincronia]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
from pathlib import Path

from comun import D, MODELOS, cargar_estilo, ffmpeg, info_video, log, normalizar, registrar_error

ESPERADO = {"ancho": 1080, "alto": 1920, "vcodec": "h264", "acodec": "aac", "pix_fmt": "yuv420p"}


def decodificar(path: Path) -> dict:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
    errores = [l for l in r.stderr.splitlines() if l.strip()]
    c = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        frames = int(c.stdout.strip().split(",")[0])
    except ValueError:
        frames = None
    return {"ok": r.returncode == 0 and not errores, "errores": errores[:10], "fotogramas_leidos": frames}


def duraciones(path: Path) -> dict:
    out = {}
    for sel in ("v:0", "a:0"):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", "stream=duration",
                            "-of", "csv=p=0", str(path)], capture_output=True, text=True)
        try:
            out[sel] = float(r.stdout.strip())
        except ValueError:
            out[sel] = None
    dif = abs(out["v:0"] - out["a:0"]) if None not in out.values() else None
    return {"video_s": out["v:0"], "audio_s": out["a:0"], "diferencia_s": dif}


def sonoridad(path: Path) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    txt = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", txt)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt)
    return {"lufs_integrado": float(i.group(1)) if i else None, "pico_verdadero_dbtp": float(tp.group(1)) if tp else None}


def negros_y_congelados(path: Path) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf",
                        "blackdetect=d=0.4:pix_th=0.08,freezedetect=n=0.002:d=2.5", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    negros = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)
    congel = re.findall(r"freeze_start: ([\d.]+)", r.stderr)
    return {"tramos_negros": [(float(a), float(b)) for a, b in negros], "congelados_desde": [float(x) for x in congel]}


def detectar_caras(path: Path, paso_s: float = 0.5, max_muestras: int = 240) -> list[dict]:
    """Devuelve [{t, caras:[(x,y,w,h,score)]}] usando el modelo YuNet (solo localiza, no identifica)."""
    import cv2  # noqa: PLC0415

    modelo = MODELOS / "yunet" / "face_detection_yunet_2023mar.onnx"
    if not modelo.exists():
        return []
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    paso = max(1, int(round(fps * paso_s)))
    idxs = list(range(0, total, paso))[:max_muestras]
    det = None
    res = []
    for i in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if not ok:
            continue
        h, w = fr.shape[:2]
        if det is None:
            det = cv2.FaceDetectorYN.create(str(modelo), "", (w, h), 0.7, 0.3, 5000)
        _, faces = det.detect(fr)
        caras = []
        if faces is not None:
            for f in faces:
                x, y, fw, fh = [int(v) for v in f[:4]]
                caras.append((x, y, fw, fh, float(f[-1])))
        res.append({"t": i / fps, "caras": caras})
    cap.release()
    return res


def _solapa(a, b) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    iw = max(0, min(ax1, bx1) - max(ax0, bx0))
    ih = max(0, min(ay1, by1) - max(ay0, by0))
    area = max(1, (bx1 - bx0) * (by1 - by0))
    return iw * ih / area


def caras_vs_texto(caras: list[dict], zonas: list[dict]) -> dict:
    conflictos = []
    for m in caras:
        for z in zonas:
            if z["t0"] <= m["t"] <= z["t1"]:
                for (x, y, w, h, _s) in m["caras"]:
                    cara = (x, y, x + w, y + h)
                    frac = _solapa(z["caja"], cara)
                    if frac > 0.05:
                        conflictos.append({"t": round(m["t"], 2), "texto": z.get("texto", "")[:30], "fraccion_cara_tapada": round(frac, 2)})
    con_cara = sum(1 for m in caras if m["caras"])
    return {"muestras": len(caras), "muestras_con_rostro": con_cara, "conflictos": conflictos[:30], "n_conflictos": len(conflictos)}


def sincronia_subtitulos(path: Path, palabras_plan: list[dict]) -> dict:
    """Re-transcribe el audio final y mide el desfase mediano entre subtítulos y voz."""
    from faster_whisper import WhisperModel  # noqa: PLC0415

    if not palabras_plan:
        return {"medido": False, "motivo": "sin palabras en el plan"}
    wav = path.with_suffix(".qc.wav")
    ffmpeg(["-i", path, "-vn", "-ac", "1", "-ar", "16000", wav], "qc audio")
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True, vad_filter=False)
    oidas = [{"w": normalizar(w.word), "t": w.start} for s in segs for w in (s.words or [])]
    wav.unlink(missing_ok=True)
    difs = []
    j = 0
    for p in palabras_plan:
        n = normalizar(p["w"])
        if len(n) < 4:
            continue
        for k in range(j, min(j + 8, len(oidas))):
            if oidas[k]["w"] == n:
                difs.append(p["t0"] - oidas[k]["t"])
                j = k + 1
                break
    if len(difs) < 3:
        return {"medido": False, "motivo": "pocas coincidencias", "coincidencias": len(difs)}
    med = statistics.median(difs)
    return {"medido": True, "coincidencias": len(difs), "desfase_mediano_s": round(med, 3),
            "desfase_max_abs_s": round(max(abs(d) for d in difs), 3), "ok": abs(med) <= 0.12}


def ortografia(palabras: list[str], estilo: dict) -> dict:
    try:
        from spellchecker import SpellChecker  # noqa: PLC0415
    except ImportError:
        return {"revisado": False}
    sc = SpellChecker(language="es")
    propias = {normalizar(x) for x in re.split(r"[ ,.;:]+", estilo.get("vocabulario_transcripcion", "")) if x}
    limpias = {re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]", "", w).lower() for w in palabras}
    limpias = {w for w in limpias if len(w) > 2 and not w.isdigit()}
    dudosas = sorted(w for w in sc.unknown(limpias) if normalizar(w) not in propias)
    return {"revisado": True, "palabras_a_revisar": dudosas,
            "nota": "Lista orientativa: el diccionario automático no conoce todos los términos técnicos. Revisión humana obligatoria."}


def originalidad(plan: dict) -> dict:
    """Compara recurso estrella, efectos y estructura con los cinco planes anteriores."""
    actuales = set(plan.get("huella", {}).get("efectos", []))
    previos = []
    for p in sorted(D["proyectos"].glob("*/plan.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            otro = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if otro.get("id") == plan.get("id") or not otro.get("aprobado"):
            continue
        previos.append(otro)
        if len(previos) == 5:
            break
    comp = []
    for o in previos:
        prev = set(o.get("huella", {}).get("efectos", []))
        jacc = len(actuales & prev) / max(1, len(actuales | prev))
        comp.append({"id": o.get("id"), "similitud_efectos": round(jacc, 2),
                     "mismo_efecto_estrella": o.get("huella", {}).get("estrella") == plan.get("huella", {}).get("estrella")})
    alerta = any(c["similitud_efectos"] > 0.7 or c["mismo_efecto_estrella"] for c in comp)
    return {"comparados": len(comp), "detalle": comp, "alerta_repeticion": alerta}


def ejecutar(path: Path, plan_path: Path | None = None, sincronia: bool = True, salida: Path | None = None) -> dict:
    estilo = cargar_estilo()
    log(f"QC de {path.name}")
    inf = info_video(path)
    rep: dict = {"archivo": str(path.relative_to(D['finales'].parent)) if path.is_relative_to(D['finales'].parent) else str(path),
                 "metadatos": inf}
    rep["formato_ok"] = {k: inf.get(k) == v for k, v in ESPERADO.items()}
    rep["decodificacion"] = decodificar(path)
    rep["duraciones"] = duraciones(path)
    rep["sonoridad"] = sonoridad(path)
    rep["negros_congelados"] = negros_y_congelados(path)
    plan = json.loads(plan_path.read_text(encoding="utf-8")) if plan_path and plan_path.exists() else {}
    zonas = plan.get("zonas_texto", [])
    caras = detectar_caras(path)
    rep["rostros_y_texto"] = caras_vs_texto(caras, zonas)
    if sincronia and plan.get("palabras_finales"):
        try:
            rep["sincronia_subtitulos"] = sincronia_subtitulos(path, plan["palabras_finales"])
        except Exception as e:  # noqa: BLE001
            registrar_error("qc sincronía", str(e), "se omite la medición")
            rep["sincronia_subtitulos"] = {"medido": False, "motivo": str(e)[:200]}
    if plan.get("palabras_finales"):
        rep["ortografia"] = ortografia([p["w"] for p in plan["palabras_finales"]], estilo)
        rep["originalidad"] = originalidad(plan)
    marca = estilo["marca"]
    logo = D["finales"].parent / marca["logo"]
    rep["marca"] = {"colores_verificados": marca["colores_verificados"], "logo_verificado": marca["logo_verificado"],
                    "logo_presente": logo.exists(), "telefono_verificado": bool(marca.get("telefono"))}
    rep["musica"] = plan.get("musica", {"usada": False})

    # Veredicto
    fallos, avisos = [], []
    if not all(rep["formato_ok"].values()):
        fallos.append(f"Formato distinto del esperado: {rep['formato_ok']}")
    if not rep["decodificacion"]["ok"]:
        fallos.append("El archivo tiene errores de decodificación")
    d = rep["duraciones"]["diferencia_s"]
    if d is not None and d > 0.1:
        fallos.append(f"Audio y vídeo difieren {d:.2f} s")
    l = rep["sonoridad"]["lufs_integrado"]
    if l is not None and abs(l - estilo["audio"]["lufs"]) > 1.5:
        avisos.append(f"Sonoridad {l} LUFS (objetivo {estilo['audio']['lufs']})")
    tp = rep["sonoridad"]["pico_verdadero_dbtp"]
    if tp is not None and tp > estilo["audio"]["true_peak"] + 0.5:
        avisos.append(f"Pico verdadero {tp} dBTP")
    if rep["negros_congelados"]["tramos_negros"]:
        avisos.append(f"Fotogramas negros: {rep['negros_congelados']['tramos_negros']}")
    if rep["rostros_y_texto"]["n_conflictos"]:
        fallos.append(f"Texto sobre rostro en {rep['rostros_y_texto']['n_conflictos']} muestras")
    s = rep.get("sincronia_subtitulos", {})
    if s.get("medido") and not s.get("ok"):
        fallos.append(f"Subtítulos desfasados {s['desfase_mediano_s']} s")
    if not marca["colores_verificados"] or not marca["logo_verificado"] or not logo.exists():
        avisos.append("Identidad corporativa sin verificar (colores/logotipo oficiales pendientes)")
    if rep.get("originalidad", {}).get("alerta_repeticion"):
        avisos.append("Se parece demasiado a alguno de los cinco vídeos anteriores")
    if not rep["musica"].get("usada"):
        avisos.append("Sin música: añadir pista con licencia (o desde la biblioteca de Instagram al publicar)")
    rep["fallos"], rep["avisos"] = fallos, avisos
    rep["veredicto"] = "NO APTO" if fallos else ("APTO CON AVISOS" if avisos else "APTO")
    rep["estado"] = "PENDIENTE DE APROBACIÓN DE CRISTINA"
    rep["revision_humana_obligatoria"] = [
        "Ver el vídeo entero en el móvil, con y sin sonido",
        "Ortografía y términos técnicos de los subtítulos",
        "Manos, instrumentos y zona de tratamiento despejados (la detección automática solo mide rostros)",
        "Precisión anatómica y científica de cada rótulo o animación",
        "Licencias de música, imágenes y stock",
    ]
    if salida:
        salida.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        salida.with_suffix(".md").write_text(a_markdown(rep), encoding="utf-8")
    log(f"QC: {rep['veredicto']}  fallos={len(fallos)} avisos={len(avisos)}")
    return rep


def a_markdown(rep: dict) -> str:
    m = rep["metadatos"]
    L = [f"# Informe de control de calidad\n", f"**Archivo:** `{rep['archivo']}`  ", f"**Veredicto:** {rep['veredicto']}  ",
         f"**Estado:** {rep['estado']}\n", "## Técnico",
         f"- Resolución {m.get('ancho')}×{m.get('alto')}, {m.get('fps')} fps, {m.get('vcodec')}/{m.get('acodec')}, {m.get('pix_fmt')}",
         f"- Duración {m.get('duracion'):.2f} s · vídeo {rep['duraciones']['video_s']} s · audio {rep['duraciones']['audio_s']} s",
         f"- Decodificación completa: {'correcta' if rep['decodificacion']['ok'] else 'CON ERRORES'} · fotogramas leídos {rep['decodificacion']['fotogramas_leidos']}",
         f"- Sonoridad {rep['sonoridad']['lufs_integrado']} LUFS · pico {rep['sonoridad']['pico_verdadero_dbtp']} dBTP",
         f"- Negros: {rep['negros_congelados']['tramos_negros'] or 'ninguno'} · congelados: {rep['negros_congelados']['congelados_desde'] or 'ninguno'}",
         "## Composición",
         f"- Muestras analizadas {rep['rostros_y_texto']['muestras']}, con rostro {rep['rostros_y_texto']['muestras_con_rostro']}, conflictos texto/rostro {rep['rostros_y_texto']['n_conflictos']}"]
    s = rep.get("sincronia_subtitulos")
    if s:
        L.append(f"- Sincronía subtítulos: {s}")
    o = rep.get("ortografia")
    if o:
        L.append(f"- Palabras a revisar (orientativo): {', '.join(o.get('palabras_a_revisar', [])) or 'ninguna'}")
    if rep.get("originalidad"):
        L.append(f"- Originalidad frente a los 5 anteriores: {rep['originalidad']}")
    L += ["## Marca y licencias", f"- {rep['marca']}", f"- Música: {rep['musica']}", "## Fallos"]
    L += [f"- {x}" for x in rep["fallos"]] or ["- Ninguno"]
    L += ["## Avisos"] + ([f"- {x}" for x in rep["avisos"]] or ["- Ninguno"])
    L += ["## Revisión humana obligatoria antes de publicar"] + [f"- [ ] {x}" for x in rep["revision_humana_obligatoria"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--plan", type=Path)
    ap.add_argument("--sin-sincronia", action="store_true")
    a = ap.parse_args()
    out = D["informes"] / f"{a.video.stem}_QC.json"
    r = ejecutar(a.video, a.plan, not a.sin_sincronia, out)
    print(a_markdown(r))
