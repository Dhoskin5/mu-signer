#!/bin/bash
set -euo pipefail

IMG="mu-signer:latest"
TAR="mu-signer.tar"
CACHE_DIR=".buildcache"
PLATFORM="linux/amd64"
CONTEXT="."

echo "Building Docker image: $IMG"

docker buildx build \
  --platform "$PLATFORM" \
  --cache-from=type=local,src="$CACHE_DIR" \
  --cache-to=type=local,dest="$CACHE_DIR",mode=max \
  -t "$IMG" \
  -o type=docker,dest="$TAR" \
  -f Dockerfile "$CONTEXT"

echo "Build complete: $TAR"

