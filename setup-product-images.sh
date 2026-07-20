#!/bin/bash
# Link or remind about ProductImages for this Codex workspace.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(dirname "$ROOT")/ProductImages"

if [ -e "$ROOT/ProductImages" ]; then
  echo "ProductImages already exists at $ROOT/ProductImages"
  exit 0
fi

if [ -d "$PARENT" ]; then
  ln -s "$PARENT" "$ROOT/ProductImages"
  echo "Linked ProductImages → $PARENT"
else
  echo "ProductImages not found."
  echo "Copy from main workspace:"
  echo "  cp -R '/Users/vikasindoria/Documents/Geo and Seo/ProductImages' '$ROOT/ProductImages'"
  exit 1
fi
