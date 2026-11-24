#!/bin/sh
if ! command -v mojo >/dev/null 2>&1; then
  echo "mojo not installed; skipping" >&2
  exit 0
fi
out=$(mojo "$(dirname "$0")/metrics.mojo") || exit 1
[ "$out" = "-25.0" ] || { echo "unexpected: $out" >&2; exit 1; }
