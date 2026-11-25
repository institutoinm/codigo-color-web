#!/usr/bin/env bash
# Codifica las secuencias PNG (12 poses/s, stop motion "on twos") a MP4 H.264,
# WebM VP9 y pósteres WebP/JPEG, para escritorio (16x9) y móvil (9x16).
set -euo pipefail
cd "$(dirname "$0")/../assets"
for dir in video/_frames/*/; do
  name=$(basename "$dir")                     # p. ej. adn-del-color_16x9
  n=$(ls "$dir"/*.png 2>/dev/null | wc -l)
  [ "$n" -lt 2 ] && { echo "sin fotogramas: $name"; continue; }
  ffmpeg -loglevel error -y -framerate 12 -pattern_type glob -i "$dir/*.png" \
    -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart -an "video/$name.mp4"
  ffmpeg -loglevel error -y -framerate 12 -pattern_type glob -i "$dir/*.png" \
    -c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 -an "video/$name.webm"
  last=$(ls "$dir"/*.png | tail -1)
  ffmpeg -loglevel error -y -i "$last" -c:v libwebp -quality 80 "posters/$name.webp"
  ffmpeg -loglevel error -y -i "$last" -q:v 4 "posters/$name.jpg"
  echo "codificado: $name ($n poses)"
done
ls -la video posters | grep -v _frames
