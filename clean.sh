#!/bin/bash
set -euo pipefail

IMG="mu-signer:latest"
TAR="mu-signer.tar"
CACHE_DIR=".buildcache"

echo " Removing image: $IMG"
docker rmi "$IMG" || echo "  Image not found. Skipping."

echo " Removing tarball: $TAR"
rm -f "$TAR"

if [[ "${1:-}" == "-all" ]]; then
  echo " Full clean: removing build cache"
  rm -rf "$CACHE_DIR"
fi

