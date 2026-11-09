"""EDITOR AUTOMÁTICO DEL INM — de un bruto a una primera edición profesional.

Dos fases, como pide la regla «el guion, antes de editar»:

  1) ANALIZAR  → copia el bruto (nunca lo toca), lee metadatos, transcribe palabra a palabra,
                 detecta silencios, muletillas y tomas repetidas, elige palabras animables y
                 escribe el GUION con la lista de cortes en 04_GUIONES. Estado: PENDIENTE DE APROBACIÓN.
       python editar.py analizar [VIDEO] --tema "..." --para "..." --objetivo "..." --cta "..." --max 60

  2) MONTAR    → solo si el guion está aprobado. Corta, reencuadra 9:16 centrado en el rostro,
                 corrige color, añade zooms, subtítulos palabra a palabra, rótulos/partículas en las
                 palabras clave, gancho, cierre institucional, efectos de sonido, música con licencia
                 (si la hay) con ducking, masteriza a -14 LUFS, exporta H.264/AAC 1080x1920, crea
                 portada, SRT/ASS, EDL editable y pasa el control de calidad.
       python editar.py montar ID --aprobar      (--aprobar = Cristina ha dicho «sí» al guion)

  Atajo:  python editar.py ultimo    → analiza el último vídeo de 01_BRUTOS.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import shutil
import statistics
import subprocess
from pathlib import Path

from comun import (D, audio_16k, FUENTES, RAIZ, cargar_estilo, ffmpeg, hex_a_ass, info_video, log, normalizar,
                   registrar_error, ruta_filtro, sha256, siguiente_version, slug, ultimo_bruto)

W, H = 1080, 1920


# ─────────────────────────────── utilidades de tiempo ───────────────────────────────
def ts_ass(t: float) -> str:
    t = max(0.0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ts_srt(t: float) -> str:
    t = max(0.0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def tc(t: float, fps: int) -> str:
    f = int(round(t * fps))
    h, r = divmod(f, 3600 * fps)
    m, r = divmod(r, 60 * fps)
    s, fr = divmod(r, fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{fr:02d}"


# ─────────────────────────────── FASE 1: ANALIZAR ───────────────────────────────
def transcribir(wav: Path, estilo: dict, modelo: str = "small") -> list[dict]:
    from faster_whisper import WhisperModel

    log(f"Transcribiendo con faster-whisper «{modelo}» (local, sin internet)…")
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, info = m.transcribe(audio_16k(wav), language="es", word_timestamps=True, vad_filter=False, beam_size=5,
                              initial_prompt=estilo.get("vocabulario_transcripcion"), condition_on_previous_text=False)
    palabras = []
    for s in segs:
        for w in s.words or []:
            txt = w.word.strip()
            if txt:
                palabras.append({"w": txt, "t0": round(w.start, 3), "t1": round(w.end, 3), "p": round(w.probability, 3)})
    log(f"{len(palabras)} palabras transcritas.")
    return palabras


def silencios(wav: Path) -> list[tuple[float, float]]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "silencedetect=n=-38dB:d=0.25", "-f", "null", "-"],
                       capture_output=True, text=True)
    ini = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(ini, fin))


def frases(palabras: list[dict], hueco: float = 0.45) -> list[list[int]]:
    out, cur = [], []
    for i, p in enumerate(palabras):
        if cur and (p["t0"] - palabras[cur[-1]]["t1"] > hueco):
            out.append(cur)
            cur = []
        cur.append(i)
        if re.search(r"[.?!…]$", p["w"]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def marcar_eliminaciones(palabras: list[dict], estilo: dict) -> list[dict]:
    """Devuelve lista de cortes [{idx:[...], motivo}] y marca palabras con 'cortar'."""
    mul = estilo["muletillas"]
    siempre = {normalizar(x) for x in mul["siempre"]}
    aisladas = {normalizar(x) for x in mul["si_aisladas"]}
    cortes = []
    fr = frases(palabras)
    textos = [[normalizar(palabras[i]["w"]) for i in f] for f in fr]
    # Muletillas
    for f, t in zip(fr, textos):
        for i, n in zip(f, t):
            if n in siempre:
                palabras[i]["cortar"] = "muletilla"
        if 0 < len(t) <= 2 and all(n in aisladas or n in siempre for n in t):
            for i in f:
                palabras[i]["cortar"] = "muletilla aislada"
        # Palabra suelta, muy corta, aislada por pausas y con baja confianza → casi siempre un titubeo
        if len(f) == 1 and len(t[0]) <= 3 and palabras[f[0]]["p"] < 0.6 and not palabras[f[0]].get("cortar"):
            i = f[0]
            antes = palabras[i]["t0"] - (palabras[i - 1]["t1"] if i else 0)
            despues = (palabras[i + 1]["t0"] if i + 1 < len(palabras) else 1e9) - palabras[i]["t1"]
            if antes > 0.4 and despues > 0.4:
                palabras[i]["cortar"] = "titubeo aislado (revisar)"
    # Tomas repetidas: si una frase empieza igual que otra posterior cercana, se queda la última completa
    for a in range(len(fr)):
        ta = [x for x in textos[a] if x not in siempre]
        if len(ta) < 3:
            continue
        for b in range(a + 1, min(a + 4, len(fr))):
            tb = [x for x in textos[b] if x not in siempre]
            n = min(len(ta), len(tb))
            if n < 3:
                continue
            ratio = difflib.SequenceMatcher(None, ta[:n], tb[:n]).ratio()
            if ratio >= 0.75:
                for i in fr[a]:
                    palabras[i]["cortar"] = f"toma repetida (se queda la del {palabras[fr[b][0]]['t0']:.1f} s)"
                break
    # Agrupar cortes contiguos para el informe
    actual = None
    for i, p in enumerate(palabras):
        if p.get("cortar"):
            if actual and actual["motivo"] == p["cortar"] and actual["idx"][-1] == i - 1:
                actual["idx"].append(i)
            else:
                actual = {"idx": [i], "motivo": p["cortar"]}
                cortes.append(actual)
    for c in cortes:
        c["t0"], c["t1"] = palabras[c["idx"][0]]["t0"], palabras[c["idx"][-1]]["t1"]
        c["texto"] = " ".join(palabras[i]["w"] for i in c["idx"])
    return cortes


def segmentos(palabras: list[dict], estilo: dict, duracion: float) -> list[dict]:
    r = estilo["ritmo"]
    keep = [i for i, p in enumerate(palabras) if not p.get("cortar")]
    segs: list[dict] = []
    for i in keep:
        p = palabras[i]
        if segs and p["t0"] - palabras[segs[-1]["ult"]]["t1"] <= r["pausa_max_s"] and segs[-1]["ult"] == i - 1:
            segs[-1]["ult"] = i
        else:
            segs.append({"pri": i, "ult": i})
    out = []
    for s in segs:
        a, b = palabras[s["pri"]], palabras[s["ult"]]
        t0 = a["t0"] - r["margen_antes_s"]
        t1 = b["t1"] + r["margen_despues_s"]
        # no invadir palabras vecinas eliminadas o conservadas
        if s["pri"] > 0:
            t0 = max(t0, (palabras[s["pri"] - 1]["t1"] + a["t0"]) / 2)
        if s["ult"] + 1 < len(palabras):
            t1 = min(t1, (b["t1"] + palabras[s["ult"] + 1]["t0"]) / 2)
        out.append({"t0": round(max(0, t0), 3), "t1": round(min(duracion, t1), 3), "pri": s["pri"], "ult": s["ult"]})
    # Unir segmentos separados por huecos minúsculos
    unidos = []
    for s in out:
        if unidos and s["t0"] - unidos[-1]["t1"] < r["unir_si_hueco_menor_s"] and \
                not any(palabras[k].get("cortar") for k in range(unidos[-1]["ult"] + 1, s["pri"])):
            unidos[-1]["t1"], unidos[-1]["ult"] = s["t1"], s["ult"]
        else:
            unidos.append(s)
    return unidos


def mapear_tiempos(palabras: list[dict], segs: list[dict]) -> list[dict]:
    """Palabras conservadas con su tiempo en la nueva línea temporal."""
    finales, acum = [], 0.0
    for s in segs:
        for i in range(s["pri"], s["ult"] + 1):
            p = palabras[i]
            if p.get("cortar"):
                continue
            finales.append({"w": p["w"], "t0": round(acum + p["t0"] - s["t0"], 3), "t1": round(acum + p["t1"] - s["t0"], 3),
                            "orig_t0": p["t0"], "p": p["p"]})
        s["nuevo_t0"] = round(acum, 3)
        acum += s["t1"] - s["t0"]
        s["nuevo_t1"] = round(acum, 3)
    return finales


def elegir_animaciones(finales: list[dict], estilo: dict, inicio_min: float) -> list[dict]:
    anim = {k: v for k, v in estilo["palabras_animables"].items() if not k.startswith("_")}
    ef = estilo["efectos"]
    eventos = []
    for p in finales:
        n = normalizar(p["w"])
        for raiz, cfg in anim.items():
            if n.startswith(raiz):
                if p["t0"] < inicio_min:
                    break
                if eventos and p["t0"] - eventos[-1]["t"] < ef["min_separacion_rotulos_s"]:
                    break
                ventana = [e for e in eventos if p["t0"] - e["t"] < 10]
                if len(ventana) >= ef["max_rotulos_por_10s"]:
                    break
                eventos.append({"t": p["t0"], "palabra": p["w"], "recurso": cfg["recurso"], "rotulo": cfg["rotulo"]})
                break
    if eventos:
        eventos[0]["estrella"] = True
    return eventos


def analizar(video: Path | None, tema: str = "", para: str = "", objetivo: str = "", cta: str = "",
             maximo: float | None = None, modelo: str = "small") -> Path:
    estilo = cargar_estilo()
    bruto = Path(video) if video else ultimo_bruto()
    if not bruto.is_absolute():
        bruto = (D["brutos"] / bruto) if (D["brutos"] / bruto).exists() else bruto.resolve()
    if not bruto.exists():
        raise SystemExit(f"No encuentro el vídeo {bruto}")
    huella_antes = sha256(bruto)
    vid = f"{slug(bruto.stem)}_{dt.date.today():%Y%m%d}"
    proy = D["proyectos"] / vid
    proy.mkdir(parents=True, exist_ok=True)
    copia = proy / f"original{bruto.suffix.lower()}"
    if not copia.exists():
        shutil.copy2(bruto, copia)
    log(f"Copia de trabajo: {copia.relative_to(RAIZ)}")
    meta = info_video(copia)
    (proy / "metadatos.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    wav = proy / "voz_16k.wav"
    ffmpeg(["-i", copia, "-vn", "-ac", "1", "-ar", "16000", wav], "extraer audio")
    palabras = transcribir(wav, estilo, modelo)
    if not palabras:
        raise SystemExit("No se ha detectado voz en el vídeo.")
    sil = silencios(wav)
    cortes = marcar_eliminaciones(palabras, estilo)
    segs = segmentos(palabras, estilo, meta["duracion"])
    finales = mapear_tiempos(palabras, segs)
    dur_nueva = segs[-1]["nuevo_t1"] if segs else 0
    eventos = elegir_animaciones(finales, estilo, inicio_min=estilo["ritmo"]["gancho_s"] + 0.3)
    primera = " ".join(p["w"] for p in finales[:8])
    gancho = tema or primera
    plan = {
        "id": vid, "creado": dt.datetime.now().isoformat(timespec="seconds"), "estado": "PENDIENTE DE APROBACIÓN",
        "aprobado": False, "bruto": str(bruto.relative_to(RAIZ)) if bruto.is_relative_to(RAIZ) else str(bruto),
        "bruto_sha256": huella_antes, "copia": str(copia.relative_to(RAIZ)), "metadatos": meta,
        "brief": {"tema": tema, "para": para, "objetivo": objetivo, "cta": cta or estilo["marca"]["cta"], "max_s": maximo},
        "gancho": gancho, "duracion_original_s": meta["duracion"], "duracion_montada_s": round(dur_nueva, 2),
        "silencios_detectados": len(sil), "cortes": cortes, "segmentos": segs, "eventos": eventos,
        "palabras": palabras, "palabras_finales": finales,
    }
    (proy / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    guion = escribir_guion(plan, estilo)
    if sha256(bruto) != huella_antes:
        registrar_error("analizar", "¡El bruto ha cambiado durante el análisis!")
    log(f"Guion listo para revisar: {guion.relative_to(RAIZ)}")
    log(f"Para montar cuando Cristina lo apruebe:  python editar.py montar {vid} --aprobar")
    return guion


def escribir_guion(plan: dict, estilo: dict) -> Path:
    b = plan["brief"]
    L = [f"# GUION · {plan['id']}", "", f"**Estado:** {plan['estado']}  ",
         f"**Bruto:** `{plan['bruto']}` ({plan['duracion_original_s']:.1f} s) → montaje previsto **{plan['duracion_montada_s']:.1f} s** + cierre {estilo['ritmo']['cierre_s']} s  ",
         f"**Tema:** {b['tema'] or '—'} · **Para:** {b['para'] or '—'} · **Objetivo:** {b['objetivo'] or '—'} · **Cierre/CTA:** {b['cta']}", ""]
    if b.get("max_s") and plan["duracion_montada_s"] > b["max_s"]:
        L += [f"> ⚠️ Dura {plan['duracion_montada_s']:.0f} s y pediste como mucho {b['max_s']:.0f} s. "
              "No recorto contenido sin tu permiso: dime qué frase sobra.", ""]
    L += ["## Gancho (primeros 2 s, se entiende sin sonido)", f"«{plan['gancho']}»", "",
          "## Guion por momentos", "", "| Nuevo | Original | Lo que digo | Lo que se ve | Efecto | Herramienta |",
          "|---|---|---|---|---|---|"]
    ev = {round(e["t"], 3): e for e in plan["eventos"]}
    for k, s in enumerate(plan["segmentos"]):
        texto = " ".join(p["w"] for p in plan["palabras"][s["pri"]:s["ult"] + 1] if not p.get("cortar"))
        efectos = ["zoom alterno" if k % 2 else "plano base"]
        for p in plan["palabras_finales"]:
            if s["nuevo_t0"] <= p["t0"] < s["nuevo_t1"] and round(p["t0"], 3) in ev:
                e = ev[round(p["t0"], 3)]
                efectos.append(f"{'★ ' if e.get('estrella') else ''}rótulo «{e['rotulo']}» + {e['recurso']} + whoosh")
        if k == 0:
            efectos.append("título gancho + pop")
        L.append(f"| {s['nuevo_t0']:.1f}–{s['nuevo_t1']:.1f} s | {s['t0']:.1f}–{s['t1']:.1f} s | {texto} | Cristina a cámara (9:16 centrado en rostro) | "
                 f"{'; '.join(efectos)} | FFmpeg + ASS |")
    L.append(f"| final | — | — | Cierre institucional: {estilo['marca']['nombre']}, web, email, «{plan['brief']['cta']}» | brillo | FFmpeg + ASS |")
    L += ["", "## Lista de cortes (lo que se quita y por qué)", "", "| Original | Texto | Motivo |", "|---|---|---|"]
    for c in plan["cortes"]:
        L.append(f"| {c['t0']:.1f}–{c['t1']:.1f} s | {c['texto']} | {c['motivo']} |")
    L.append(f"| — | (silencios) | {plan['silencios_detectados']} pausas detectadas; se comprimen las mayores de {estilo['ritmo']['pausa_max_s']} s |")
    dud = [p for p in plan["palabras_finales"] if p["p"] < 0.6]
    if dud:
        L += ["", "## Palabras con transcripción dudosa (revisa la ortografía)", ", ".join(f"«{p['w']}» ({p['t0']:.1f} s)" for p in dud)]
    L += ["", "## Para aprobar", f"Si está bien, di «sí» o ejecuta: `python 12_AUTOMATIZACIONES/editar.py montar {plan['id']} --aprobar`",
          "Si quieres cambios, dilo con el segundo: «en el 14 repito la frase, quédate con la segunda»."]
    out = D["guiones"] / f"{plan['id']}_guion.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


# ─────────────────────────────── FASE 2: MONTAR ───────────────────────────────
def analizar_rostros(video: Path, t0: float = 0, t1: float | None = None) -> dict:
    import qc

    caras = qc.detectar_caras(video, paso_s=0.5)
    cajas = [max(m["caras"], key=lambda c: c[2] * c[3]) for m in caras if m["caras"] and (t1 is None or t0 <= m["t"] <= t1)]
    if not cajas:
        return {"hay": False, "muestras": caras}
    return {"hay": True, "cx": statistics.median(c[0] + c[2] / 2 for c in cajas),
            "cy": statistics.median(c[1] + c[3] / 2 for c in cajas), "w": statistics.median(c[2] for c in cajas),
            "h": statistics.median(c[3] for c in cajas), "muestras": caras}


def balance_blancos(video: Path) -> tuple[float, float, float]:
    """Mundo gris sobre medios tonos, limitado a ±6 % para que «no se note»."""
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(str(video))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 1)
    medias = []
    for i in np.linspace(0, total - 1, 8).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        ok, fr = cap.read()
        if not ok:
            continue
        f = fr.reshape(-1, 3).astype(float)
        lum = f.mean(axis=1)
        m = f[(lum > 50) & (lum < 205)]
        if len(m):
            medias.append(m.mean(axis=0))
    cap.release()
    if not medias:
        return 1.0, 1.0, 1.0
    b, g, r = np.mean(medias, axis=0)
    gris = (r + g + b) / 3
    lim = lambda x: float(min(1.06, max(0.94, x)))  # noqa: E731
    return lim(gris / r), lim(gris / g), lim(gris / b)


def caja_recorte(meta: dict, cara: dict, zoom: float) -> tuple[int, int, int, int]:
    sw, sh = meta["ancho"], meta["alto"]
    if sw / sh > W / H:
        ch = sh / zoom
        cw = ch * W / H
    else:
        cw = sw / zoom
        ch = cw * H / W
    cx = cara["cx"] if cara.get("hay") else sw / 2
    cy = (cara["cy"] + cara["h"] * 0.25) if cara.get("hay") else sh / 2
    x = min(max(0, cx - cw / 2), sw - cw)
    y = min(max(0, cy - ch / 2), sh - ch)
    par = lambda v: int(v) // 2 * 2  # noqa: E731
    return par(cw), par(ch), par(x), par(y)


def construir_ass(plan: dict, estilo: dict, caras_rough: list[dict], dur: float, cierre_t: float) -> tuple[str, list[dict], list[dict]]:
    c = estilo["marca"]["colores"]
    s = estilo["subtitulos"]
    z = estilo["zonas_seguras"]
    BL, RS, CT, PR = hex_a_ass(c["texto"]), hex_a_ass(c["resalte"]), hex_a_ass(c["contorno"]), hex_a_ass(c["primario"])
    tip = estilo["tipografia"]
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{tip['subtitulos']},{s['tamano']},{BL},{BL},{CT},&H80000000,0,0,0,0,100,100,0,0,1,{s['contorno']},{s['sombra']},5,{z['izquierda']},{z['derecha']},0,1
Style: Gancho,{tip['titulos']},92,{BL},{BL},{CT},&H80000000,0,0,0,0,100,100,0,0,1,7,0,5,80,80,0,1
Style: Rotulo,{tip['titulos']},104,{RS},{RS},{CT},&H80000000,0,0,0,0,100,100,2,0,1,7,0,5,60,60,0,1
Style: Cierre,{tip['titulos']},62,{BL},{BL},{CT},&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,60,60,0,1
Style: CierreTxt,{tip['texto']},44,{BL},{BL},{CT},&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1
Style: Dibujo,{tip['texto']},20,{RS},{RS},{CT},&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, zonas = [], []

    def cara_en(t0: float, t1: float) -> list[tuple]:
        """Todas las cajas de rostro (con margen) presentes en el intervalo, una a una."""
        cajas = []
        for m in caras_rough:
            if t0 - 0.25 <= m["t"] <= t1 + 0.25:
                for (x, y, w_, h_, _s) in m["caras"]:
                    cajas.append((x - 30, y - 40, x + w_ + 30, y + h_ + 60))
        return cajas

    def libre(caja, caras) -> bool:
        return all(caja[2] < c_[0] or caja[0] > c_[2] or caja[3] < c_[1] or caja[1] > c_[3] for c_ in caras)

    def caja_texto(x, y, texto, tam):
        ancho = min(W - 80, len(texto) * tam * 0.62)
        alto = tam * 1.35 * (1 + texto.count("\\N"))
        return (int(x - ancho / 2), int(y - alto / 2), int(x + ancho / 2), int(y + alto / 2))

    def colocar(t0, t1, texto, tam, preferidas):
        cara = cara_en(t0, t1)
        for y in preferidas:
            caja = caja_texto(W / 2, y, texto, tam)
            if libre(caja, cara):
                return y, caja
        # último recurso: la posición que menos rostro tapa
        def tapado(yy):
            cj = caja_texto(W / 2, yy, texto, tam)
            return sum(max(0, min(cj[2], c_[2]) - max(cj[0], c_[0])) * max(0, min(cj[3], c_[3]) - max(cj[1], c_[1])) for c_ in cara)
        candidatas = preferidas + list(range(z["superior"] + 60, H - z["inferior"], 60))
        y = min(candidatas, key=tapado)
        return y, caja_texto(W / 2, y, texto, tam)

    # 1) Gancho
    g = estilo["ritmo"]["gancho_s"]
    gtxt = partir_lineas(plan["gancho"].upper(), 18)
    yg, caja = colocar(0, g, gtxt, 92, [z["superior"] + 170, 1500, 960])
    ev.append(f"Dialogue: 3,{ts_ass(0.05)},{ts_ass(g)},Gancho,,0,0,0,,{{\\pos(540,{yg})\\fscx70\\fscy70\\blur10\\alpha&HFF&"
              f"\\t(0,260,\\fscx104\\fscy104\\blur0\\alpha&H00&)\\t(260,420,\\fscx100\\fscy100)\\t({int(g*1000)-250},{int(g*1000)},\\alpha&HFF&)}}{gtxt}")
    zonas.append({"t0": 0.05, "t1": g, "caja": caja, "texto": plan["gancho"]})
    sfx = [{"t": 0.05, "s": "pop"}]

    # 2) Subtítulos palabra a palabra (bloques de ≤3 palabras / ≤22 caracteres)
    bloques, cur = [], []
    for p in plan["palabras_finales"]:
        txt = " ".join(x["w"] for x in cur + [p])
        if cur and (len(cur) >= s["max_palabras_bloque"] or len(txt) > s["max_caracteres_bloque"]
                    or p["t0"] - cur[-1]["t1"] > 0.35 or re.search(r"[.?!,;:]$", cur[-1]["w"])):
            bloques.append(cur)
            cur = []
        cur.append(p)
    if cur:
        bloques.append(cur)
    for bi, b in enumerate(bloques):
        b_ini = max(b[0]["t0"], g if bi == 0 and b[0]["t0"] < g else b[0]["t0"])
        b_fin = min((bloques[bi + 1][0]["t0"] if bi + 1 < len(bloques) else b[-1]["t1"] + 0.3), cierre_t)
        if b_fin - b_ini < 0.08:
            continue
        palabras_txt = [re.sub(r"[{}\\]", "", x["w"]) for x in b]
        texto_plano = " ".join(palabras_txt)
        y, caja = colocar(b_ini, b_fin, texto_plano, s["tamano"], [s["banda_baja_y"], s["banda_alta_y"] + 120, 1150])
        zonas.append({"t0": b_ini, "t1": b_fin, "caja": caja, "texto": texto_plano})
        for k, x in enumerate(b):
            w0 = max(b_ini, x["t0"]) if k else b_ini
            w1 = b[k + 1]["t0"] if k + 1 < len(b) else b_fin
            if w1 - w0 < 0.02:
                continue
            partes = []
            for j, t in enumerate(palabras_txt):
                partes.append(f"{{\\c{RS}\\fscx108\\fscy108}}{t}{{\\c{BL}\\fscx100\\fscy100}}" if (j == k and s["resaltar_palabra_actual"]) else t)
            entrada = "\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)" if k == 0 else ""
            ev.append(f"Dialogue: 1,{ts_ass(w0)},{ts_ass(w1)},Sub,,0,0,0,,{{\\pos(540,{y}){entrada}}}{' '.join(partes)}")

    # 3) Rótulos / partículas en palabras clave
    dur_r = estilo["efectos"]["duracion_rotulo_s"]
    for e in plan["eventos"]:
        t0, t1 = e["t"], min(e["t"] + dur_r, cierre_t - 0.1)
        y, caja = colocar(t0, t1, e["rotulo"], 104, [z["superior"] + 140, 700, 1550])
        e["y"] = y
        ev.append(f"Dialogue: 4,{ts_ass(t0)},{ts_ass(t1)},Rotulo,,0,0,0,,{{\\pos(540,{y})\\fscx40\\fscy40\\blur14\\alpha&HFF&"
                  f"\\t(0,220,\\fscx108\\fscy108\\blur0\\alpha&H00&)\\t(220,340,\\fscx100\\fscy100)\\t({int((t1-t0)*1000)-220},{int((t1-t0)*1000)},\\alpha&HFF&\\fscx115\\fscy115)}}{e['rotulo']}")
        zonas.append({"t0": t0, "t1": t1, "caja": caja, "texto": e["rotulo"]})
        sfx.append({"t": t0, "s": "impacto" if e.get("estrella") else "whoosh"})
        if e["recurso"] in ("particulas", "capas_piel", "tarjeta", "interrogacion", "aviso"):
            ev += particulas(t0, t1, y, RS)
        if e["recurso"] == "aviso":
            ev.append(f"Dialogue: 4,{ts_ass(t0)},{ts_ass(t1)},Dibujo,,0,0,0,,{{\\pos(500,{y-150})\\c{RS}\\alpha&HFF&\\t(0,200,\\alpha&H00&)\\p1}}m 40 0 l 80 70 l 0 70{{\\p0}}")

    # 4) Cierre institucional
    m = estilo["marca"]
    lineas = [("Cierre", partir_lineas(m["nombre"], 20), 760), ("CierreTxt", m["web"], 1000), ("CierreTxt", m["email"], 1070)]
    if m.get("telefono"):
        lineas.append(("CierreTxt", m["telefono"], 1140))
    lineas.append(("Cierre", plan["brief"]["cta"], 1290))
    for k, (st, tx, y) in enumerate(lineas):
        d = 120 * k
        ev.append(f"Dialogue: 5,{ts_ass(cierre_t + 0.05)},{ts_ass(dur)},{st},,0,0,0,,{{\\pos(540,{y})\\alpha&HFF&\\t({d},{d+300},\\alpha&H00&)}}{tx}")
    ev.append(f"Dialogue: 5,{ts_ass(cierre_t + 0.6)},{ts_ass(dur)},Dibujo,,0,0,0,,{{\\pos(390,1350)\\c{RS}\\p1\\fscx0\\t(0,400,\\fscx100)}}m 0 0 l 300 0 l 300 6 l 0 6{{\\p0}}")
    sfx.append({"t": cierre_t, "s": "brillo"})
    return cab + "\n".join(ev) + "\n", zonas, sfx


def particulas(t0: float, t1: float, y: int, color: str, n: int = 22) -> list[str]:
    """Partículas de pigmento vectoriales que brotan alrededor del rótulo (determinista)."""
    import random

    rnd = random.Random(int(t0 * 1000))
    out = []
    for _ in range(n):
        x0 = 540 + rnd.uniform(-260, 260)
        y0 = y + rnd.uniform(-40, 40)
        x1 = x0 + rnd.uniform(-160, 160)
        y1 = y0 - rnd.uniform(80, 260)
        r = rnd.uniform(4, 11)
        d0 = rnd.randint(0, 250)
        dur = int((t1 - t0) * 1000)
        out.append(f"Dialogue: 2,{ts_ass(t0)},{ts_ass(t1)},Dibujo,,0,0,0,,{{\\move({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f},{d0},{dur})"
                   f"\\c{color}\\blur2\\alpha&HFF&\\t({d0},{d0+150},\\alpha&H30&)\\t({dur-400},{dur},\\alpha&HFF&)\\p1}}"
                   f"m 0 {-r:.0f} b {r:.0f} {-r:.0f} {r:.0f} {r:.0f} 0 {r:.0f} b {-r:.0f} {r:.0f} {-r:.0f} {-r:.0f} 0 {-r:.0f}{{\\p0}}")
    return out


def partir_lineas(t: str, n: int) -> str:
    pal, lin, cur = t.split(), [], ""
    for p in pal:
        if cur and len(cur) + 1 + len(p) > n:
            lin.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip()
    if cur:
        lin.append(cur)
    return "\\N".join(lin[:3])


def elegir_musica() -> dict:
    carpeta = D["recursos"] / "musica"
    for f in sorted(carpeta.glob("*")):
        if f.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}:
            lic = f.with_suffix(f.suffix + ".licencia.txt")
            lic2 = f.with_suffix(".licencia.txt")
            if lic.exists() or lic2.exists():
                return {"usada": True, "archivo": str(f.relative_to(RAIZ)), "licencia": (lic if lic.exists() else lic2).read_text(encoding="utf-8")[:500]}
            log(f"Música «{f.name}» ignorada: no tiene archivo .licencia.txt")
    return {"usada": False, "motivo": "No hay música con licencia en 05_RECURSOS/musica"}


def loudnorm_2pasos(entrada_args: list, filtro_previo: str, estilo: dict) -> str:
    a = estilo["audio"]
    r = subprocess.run(["ffmpeg", "-hide_banner", *map(str, entrada_args), "-filter_complex",
                        f"{filtro_previo},loudnorm=I={a['lufs']}:TP={a['true_peak']}:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    return (f"loudnorm=I={a['lufs']}:TP={a['true_peak']}:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
            f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")


def escribir_edl(plan: dict, fps: int, ruta: Path) -> None:
    L = [f"TITLE: {plan['id']}", "FCM: NON-DROP FRAME", ""]
    for k, s in enumerate(plan["segmentos"], 1):
        L.append(f"{k:03d}  ORIGINAL V     C        {tc(s['t0'], fps)} {tc(s['t1'], fps)} {tc(s['nuevo_t0'], fps)} {tc(s['nuevo_t1'], fps)}")
        L.append(f"{k:03d}  ORIGINAL A     C        {tc(s['t0'], fps)} {tc(s['t1'], fps)} {tc(s['nuevo_t0'], fps)} {tc(s['nuevo_t1'], fps)}")
        L.append(f"* FROM CLIP NAME: {Path(plan['copia']).name}")
        L.append("")
    ruta.write_text("\n".join(L), encoding="utf-8")


def portada(plan: dict, estilo: dict, rough: Path, salida: Path) -> None:
    import cv2
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    cap = cv2.VideoCapture(str(rough))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mejor, mejor_p = None, -1
    for i in range(int(total * 0.05), int(total * 0.6), max(1, int(fps * 0.5))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if not ok:
            continue
        nitidez = cv2.Laplacian(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if nitidez > mejor_p:
            mejor, mejor_p = fr, nitidez
    cap.release()
    img = Image.fromarray(cv2.cvtColor(mejor, cv2.COLOR_BGR2RGB)).convert("RGB")
    c = estilo["marca"]["colores"]
    # degradado inferior para legibilidad
    grad = Image.new("L", (1, H))
    for yy in range(H):
        grad.putpixel((0, yy), int(min(1.0, max(0, (yy - H * 0.42) / (H * 0.30))) * 235))
    sombra = Image.new("RGB", (W, H), tuple(int(c["contorno"][i:i + 2], 16) for i in (1, 3, 5)))
    img = Image.composite(sombra, img, grad.resize((W, H)))
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(str(FUENTES / "Montserrat-Black.ttf"), 96)
    f_cab = ImageFont.truetype(str(FUENTES / "Montserrat-Bold.ttf"), 30)
    cab = estilo["marca"]["nombre"]
    tw = d.textlength(cab, font=f_cab)
    d.text(((W - tw) / 2, 1468), cab, font=f_cab, fill=c["resalte"])
    titulo = (plan["brief"]["tema"] or plan["gancho"]).upper()
    lineas = partir_lineas(titulo, 16).split("\\N")
    y = 1440 - len(lineas) * 112
    for ln in lineas:
        lw = d.textlength(ln, font=f_tit)
        d.text(((W - lw) / 2, y), ln, font=f_tit, fill=c["texto"], stroke_width=4, stroke_fill=c["contorno"])
        y += 112
    logo = RAIZ / estilo["marca"]["logo"]
    if logo.exists():
        lg = Image.open(logo).convert("RGBA")
        lg.thumbnail((260, 140))
        img.paste(lg, ((W - lg.width) // 2, 1560), lg)
    img.save(salida, quality=92)


def aplicar_correcciones(plan: dict, correcciones: list[str], estilo: dict) -> None:
    """«pimiento=pigmento» corrige la transcripción (sin tocar tiempos) y recalcula las animaciones."""
    pares = []
    for c in correcciones:
        if "=" in c:
            mal, bien = c.split("=", 1)
            pares.append((normalizar(mal), bien.strip()))
    n = 0
    for lista in (plan["palabras"], plan["palabras_finales"]):
        for p in lista:
            for mal, bien in pares:
                if normalizar(p["w"]) == mal:
                    punt = re.search(r"[.,;:?!…]+$", p["w"])
                    p["w"] = bien + (punt.group(0) if punt else "")
                    p["p"] = 1.0
                    n += 1
    plan.setdefault("correcciones", []).extend(correcciones)
    plan["eventos"] = elegir_animaciones(plan["palabras_finales"], estilo, inicio_min=estilo["ritmo"]["gancho_s"] + 0.3)
    log(f"Correcciones aplicadas: {n} palabras · rótulos recalculados: {[e['rotulo'] for e in plan['eventos']]}")


def montar(vid: str, aprobar: bool = False, sin_qc: bool = False, correcciones: list[str] | None = None) -> Path:
    estilo = cargar_estilo()
    proy = D["proyectos"] / vid
    plan_p = proy / "plan.json"
    if not plan_p.exists():
        raise SystemExit(f"No existe {plan_p}. Primero: python editar.py analizar")
    plan = json.loads(plan_p.read_text(encoding="utf-8"))
    if not plan.get("aprobado"):
        if not aprobar:
            raise SystemExit("El guion no está aprobado. Revisa 04_GUIONES y, si Cristina dice «sí», añade --aprobar.")
        plan.update(aprobado=True, aprobado_en=dt.datetime.now().isoformat(timespec="seconds"), estado="GUION APROBADO · EN PRODUCCIÓN")
    if correcciones:
        aplicar_correcciones(plan, correcciones, estilo)
    copia = RAIZ / plan["copia"]
    meta = plan["metadatos"]
    fps = int(round(meta.get("fps") or estilo["formato"]["fps_por_defecto"]))
    fps = fps if 23 <= fps <= 60 else 30
    v = siguiente_version(vid)
    base = f"{vid}_v{v}"
    log(f"Montando {base}…")

    # 1) Rostro y color sobre el original
    cara = analizar_rostros(copia)
    rg, gg, bg = balance_blancos(copia)
    log(f"Rostro: {'sí' if cara['hay'] else 'no detectado'} · balance de blancos R{rg:.3f} G{gg:.3f} B{bg:.3f}")
    r = estilo["ritmo"]
    estrella_t = next((e["t"] for e in plan["eventos"] if e.get("estrella")), None)

    # 2) Corte + reencuadre + color + zoom por segmento → rough.mp4
    partes, n = [], len(plan["segmentos"])
    for k, s in enumerate(plan["segmentos"]):
        zoom = 1.0 if k % 2 == 0 else r["zoom_alterno"]
        if estrella_t is not None and s["nuevo_t0"] <= estrella_t < s["nuevo_t1"]:
            zoom = r["zoom_impacto"]
        cw, ch, x, y = caja_recorte(meta, cara, zoom)
        partes.append(
            f"[0:v]trim={s['t0']}:{s['t1']},setpts=PTS-STARTPTS,crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1,fps={fps}[v{k}];"
            f"[0:a]atrim={s['t0']}:{s['t1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, s['t1']-s['t0']-0.015):.3f}:d=0.015[a{k}];")
    cierre = r["cierre_s"]
    c = estilo["marca"]["colores"]
    filtro = "".join(partes) + "".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac];"
    filtro += (f"[vc]colorchannelmixer=rr={rg:.4f}:gg={gg:.4f}:bb={bg:.4f},eq=contrast=1.03:saturation=1.05,format=yuv420p[vcc];"
               f"color=c=0x{c['primario'].lstrip('#')}:s={W}x{H}:r={fps}:d={cierre},format=yuv420p[fin];"
               f"anullsrc=r=48000:cl=stereo:d={cierre}[afin];[ac]aresample=48000,aformat=channel_layouts=stereo[ac2];"
               f"[vcc][ac2][fin][afin]concat=n=2:v=1:a=1[vr][ar]")
    rough = proy / f"{base}_rough.mp4"
    ffmpeg(["-i", copia, "-filter_complex", filtro, "-map", "[vr]", "-map", "[ar]", "-c:v", "libx264", "-crf", "16",
            "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", rough.with_suffix(".mov")], "corte y reencuadre")
    rough = rough.with_suffix(".mov")
    dur = info_video(rough)["duracion"]
    cierre_t = dur - cierre

    # 3) Gráficos (subtítulos, gancho, rótulos, cierre) colocados fuera del rostro
    import qc

    caras_rough = qc.detectar_caras(rough, paso_s=0.25, max_muestras=1000)
    ass_txt, zonas, sfx = construir_ass(plan, estilo, caras_rough, dur, cierre_t)
    ass = proy / f"{base}.ass"
    ass.write_text(ass_txt, encoding="utf-8")

    # 4) Audio: voz limpia + SFX + música con ducking + masterización -14 LUFS (2 pasadas)
    a = estilo["audio"]
    musica = elegir_musica()
    entradas = ["-i", rough]
    mezcla = [f"[0:a]highpass=f={a['highpass_hz']},acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2[voz]"]
    etiquetas = []
    sfx_dir = D["recursos"] / "sfx"
    for k, e in enumerate(sfx):
        entradas += ["-i", sfx_dir / f"{e['s']}.wav"]
        ms = int(max(0, e["t"] - (0.12 if e["s"] == "whoosh" else 0)) * 1000)
        mezcla.append(f"[{k+1}:a]adelay={ms}|{ms},volume={a['sfx_db']}dB[s{k}]")
        etiquetas.append(f"[s{k}]")
    voz = "[voz]"
    if musica["usada"]:
        idx = len(sfx) + 1
        entradas += ["-stream_loop", "-1", "-i", RAIZ / musica["archivo"]]
        mezcla.append(f"[voz]asplit=2[voz][vozsc];[{idx}:a]atrim=0:{dur:.2f},volume={a['musica_db_bajo_voz']}dB,afade=t=out:st={dur-1.5:.2f}:d=1.5[mus];"
                      f"[mus][vozsc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[musd]")
        etiquetas.append("[musd]")
    pre = ";".join(mezcla) + f";{voz}{''.join(etiquetas)}amix=inputs={1+len(etiquetas)}:normalize=0:duration=first"
    norm = loudnorm_2pasos(entradas, pre, estilo)

    # 5) Render final
    render = D["renders"] / f"{base}.mp4"
    filtro_v = f"[0:v]subtitles=filename='{ruta_filtro(ass)}':fontsdir='{ruta_filtro(FUENTES)}',format=yuv420p[vf]"
    logo = RAIZ / estilo["marca"]["logo"]
    if logo.exists():
        entradas += ["-i", logo]
        li = len(entradas) // 2 - 1 if False else sum(1 for x in entradas if x == "-i") - 1
        filtro_v = (f"[0:v]subtitles=filename='{ruta_filtro(ass)}':fontsdir='{ruta_filtro(FUENTES)}'[vs];"
                    f"[{li}:v]scale=220:-1,format=rgba,colorchannelmixer=aa=0.85[lg];"
                    f"[vs][lg]overlay=x=W-w-150:y=170,format=yuv420p[vf]")
    f_total = f"{pre},{norm},aresample=48000[af];{filtro_v}"
    fmt = estilo["formato"]
    ffmpeg([*entradas, "-filter_complex", f_total, "-map", "[vf]", "-map", "[af]", "-c:v", "libx264", "-profile:v", "high",
            "-preset", fmt["preset"], "-crf", str(fmt["crf"]), "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac",
            "-b:a", f"{fmt['audio_kbps']}k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{dur:.3f}", render], "render final")
    final = D["finales"] / f"{base}.mp4"
    shutil.copy2(render, final)
    log(f"Final: {final.relative_to(RAIZ)}")

    # 6) Entregables: subtítulos, portada, EDL, plan actualizado
    srt = D["subtitulos"] / f"{base}.srt"
    srt.write_text(a_srt(plan["palabras_finales"], cierre_t), encoding="utf-8")
    shutil.copy2(ass, D["subtitulos"] / ass.name)
    portada(plan, estilo, rough, D["portadas"] / f"{base}_portada.jpg")
    escribir_edl(plan, fps, proy / f"{base}.edl")
    plan.update(version=v, final=str(final.relative_to(RAIZ)), zonas_texto=zonas, musica=musica, sfx=sfx,
                estado="PENDIENTE DE APROBACIÓN", duracion_final_s=round(dur, 2),
                huella={"estrella": next((e["recurso"] + ":" + e["rotulo"] for e in plan["eventos"] if e.get("estrella")), "ninguno"),
                        "efectos": sorted({e["recurso"] for e in plan["eventos"]} | {"zoom_alterno", "subtitulo_palabra", "gancho", "cierre"})})
    plan_p.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    if sha256(RAIZ / plan["bruto"]) != plan["bruto_sha256"]:
        registrar_error("montar", "El bruto original ha cambiado: revisar")
    if not sin_qc:
        rep = qc.ejecutar(final, plan_p, sincronia=True, salida=D["informes"] / f"{base}_QC.json")
        resumen(plan, rep)
    return final


def a_srt(finales: list[dict], fin: float) -> str:
    bloques, cur = [], []
    for p in finales:
        if cur and (len(cur) >= 7 or p["t0"] - cur[-1]["t1"] > 0.6 or re.search(r"[.?!]$", cur[-1]["w"])):
            bloques.append(cur)
            cur = []
        cur.append(p)
    if cur:
        bloques.append(cur)
    out = []
    for i, b in enumerate(bloques, 1):
        out.append(f"{i}\n{ts_srt(b[0]['t0'])} --> {ts_srt(min(b[-1]['t1'] + 0.2, fin))}\n{' '.join(x['w'] for x in b)}\n")
    return "\n".join(out)


def resumen(plan: dict, rep: dict) -> None:
    print("\n──────── RESUMEN ────────")
    print(f"Vídeo: {plan['final']}  ({plan['duracion_final_s']} s, de {plan['duracion_original_s']:.1f} s de bruto)")
    print(f"Cortes: {len(plan['cortes'])} (muletillas/tomas) · rótulos: {len(plan['eventos'])} · música: {'sí' if plan['musica']['usada'] else 'no'}")
    print(f"QC: {rep['veredicto']} · fallos: {rep['fallos'] or 'ninguno'}")
    print(f"Avisos: {rep['avisos'] or 'ninguno'}")
    print("Estado: PENDIENTE DE APROBACIÓN DE CRISTINA (no se publica nada).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Editor automático INM")
    sp = ap.add_subparsers(dest="cmd", required=True)
    a1 = sp.add_parser("analizar")
    a1.add_argument("video", nargs="?")
    a1.add_argument("--tema", default="")
    a1.add_argument("--para", default="")
    a1.add_argument("--objetivo", default="")
    a1.add_argument("--cta", default="")
    a1.add_argument("--max", type=float)
    a1.add_argument("--modelo", default="small", help="small (rápido) · medium (más preciso, más lento)")
    a2 = sp.add_parser("montar")
    a2.add_argument("id")
    a2.add_argument("--aprobar", action="store_true")
    a2.add_argument("--sin-qc", action="store_true")
    a2.add_argument("--corregir", action="append", default=[], help='Corrige la transcripción: --corregir "pimiento=pigmento"')
    sp.add_parser("ultimo")
    args = ap.parse_args()
    try:
        if args.cmd == "analizar":
            analizar(args.video, args.tema, args.para, args.objetivo, args.cta, args.max, args.modelo)
        elif args.cmd == "ultimo":
            analizar(None)
        else:
            montar(args.id, args.aprobar, args.sin_qc, args.corregir)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        registrar_error(f"editar {args.cmd}", repr(e), "ver SOLUCION-DE-ERRORES.md")
        raise
