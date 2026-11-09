# INSTALACIÓN

## Dónde está construido
El estudio se construyó y probó en un contenedor Linux en la nube (Claude Code en la web) y está guardado en GitHub:
`institutoinm/codigo-color-web`, rama `claude/vigilant-heisenberg-karvaj`, carpeta `INM — ESTUDIO AUDIOVISUAL AUTOMÁTICO/`.
En GitHub **no** van vídeos, modelos ni dependencias (pesan varios GB y algunos son privados): el instalador los descarga.

## En tu portátil (Windows)
1. Descarga la carpeta: en Claude Desktop / Cowork o Claude Code, con una carpeta conectada, escribe:
   *«Clona la rama claude/vigilant-heisenberg-karvaj de github.com/institutoinm/codigo-color-web y ejecuta el instalador del estudio INM»*.
   (O a mano: `git clone -b claude/vigilant-heisenberg-karvaj https://github.com/institutoinm/codigo-color-web.git`.)
2. Abre la carpeta `INM — ESTUDIO AUDIOVISUAL AUTOMÁTICO` y ejecuta:
   ```powershell
   powershell -ExecutionPolicy Bypass -File instalar.ps1
   ```
   Si faltan FFmpeg, Node.js, Python o Git, **te pregunta** antes de instalarlos con `winget` (gratuitos; Windows puede pedir permiso de administrador).
   Después vuelve a ejecutarlo una vez para que Windows vea los programas nuevos.

## En Mac
```bash
bash instalar.sh
```
Usa Homebrew (te pregunta antes de instalar nada).

## Qué hace el instalador (idempotente: se puede repetir sin romper nada)
1. Comprueba FFmpeg/FFprobe, Node.js ≥ 22, Python ≥ 3.10 y Git.
2. Crea un entorno aislado `_HERRAMIENTAS/venv` e instala `_HERRAMIENTAS/requirements.txt` (versiones fijadas).
3. Genera los efectos de sonido propios (`sfx.py`).
4. `preparar.py`: descarga el modelo de transcripción (faster-whisper «small», ~460 MB), el de recorte de personas (rembg `u2net_human_seg`, 176 MB), el detector de caras YuNet (230 kB), clona las 4 guías/repositorios, instala Remotion 4.0.542 y prepara la plantilla de HyperFrames 0.9.26 con GSAP local.
5. Hace la **prueba real de 5 s** y su control de calidad.

Espacio necesario: unos 2,5 GB. Tiempo: 10–20 min según conexión.

## Sin permisos de administrador
Todo lo de Python y Node se instala dentro de la carpeta. Solo FFmpeg/Node/Python/Git son programas del sistema; si no puedes instalarlos, pídeselo a quien administre el portátil.

## Comprobar sin instalar
```bash
_HERRAMIENTAS/venv/bin/python 12_AUTOMATIZACIONES/preparar.py --comprobar
```
(En Windows: `_HERRAMIENTAS\venv\Scripts\python.exe 12_AUTOMATIZACIONES\preparar.py --comprobar`.)

## Red necesaria (solo durante la instalación)
pypi.org, registry.npmjs.org, github.com y media.githubusercontent.com, huggingface.co (+ su CDN `us.aws.cdn.hf.co`).
Después, **editar funciona sin internet** (salvo Remotion la primera vez, que descarga su navegador).
