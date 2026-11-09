#!/usr/bin/env bash
# Instalador del Estudio INM para Mac (y Linux).
# Uso:  bash instalar.sh      (desde la carpeta del estudio)
# Pide confirmación antes de instalar programas del sistema con Homebrew.
set -euo pipefail
cd "$(dirname "$0")"
echo "== Estudio INM: comprobando programas =="
faltan=()
command -v ffmpeg >/dev/null || faltan+=(ffmpeg)
command -v node   >/dev/null || faltan+=(node@22)
command -v python3 >/dev/null || faltan+=(python@3.12)
command -v git    >/dev/null || faltan+=(git)
if [ ${#faltan[@]} -gt 0 ]; then
  echo "Faltan: ${faltan[*]}"
  if ! command -v brew >/dev/null; then
    echo "Instala Homebrew (https://brew.sh) o esos programas y vuelve a ejecutar."; exit 1
  fi
  read -r -p "¿Instalarlos con Homebrew (gratuitos)? (s/n) " r
  [ "$r" = "s" ] || { echo "Cancelado."; exit 1; }
  brew install "${faltan[@]}"
fi
node -e 'process.exit(parseInt(process.versions.node)>=22?0:1)' || echo "AVISO: Node.js es anterior a 22; Remotion e HyperFrames piden 22 o superior."
[ -d _HERRAMIENTAS/venv ] || python3 -m venv _HERRAMIENTAS/venv
_HERRAMIENTAS/venv/bin/pip install --upgrade pip
_HERRAMIENTAS/venv/bin/pip install -r _HERRAMIENTAS/requirements.txt
_HERRAMIENTAS/venv/bin/python 12_AUTOMATIZACIONES/sfx.py
_HERRAMIENTAS/venv/bin/python 12_AUTOMATIZACIONES/preparar.py
echo "== Prueba real de 5 segundos =="
_HERRAMIENTAS/venv/bin/python 12_AUTOMATIZACIONES/prueba_5s.py
echo "Listo. Lee COMO-FUNCIONA.md"
