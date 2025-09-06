#!/bin/sh
set -e

mkdir -p /app/data

ASSET_URL="https://github.com/sammyyo/qandro-pop-service/releases/download/worldpop-v1/worldpop_2023_region.tif"
ASSET_SHA256="63d518ba50866dac84db0bfae4eeba950e6017f0a8702d8c3f58491fe55a1830"
TARGET="/app/data/worldpop_2023_region.tif"

if [ ! -f "$TARGET" ]; then
  echo "[start] Downloading WorldPop TIFF..."
  curl -L "$ASSET_URL" -o "$TARGET"

  echo "[start] Verifying SHA256..."
  # Busybox/Alpine may use 'sha256sum'; Debian slim has it via coreutils
  echo "$ASSET_SHA256  $TARGET" | sha256sum -c -

  echo "[start] Download complete & verified."
else
  echo "[start] Using cached WorldPop TIFF from volume."
fi

exec uvicorn app:app --host 0.0.0.0 --port "$PORT" --proxy-headers
