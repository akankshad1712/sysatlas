#!/bin/sh
set -eu
BIN=${1:-./build/sysatlas-collector}
ROOT=$(mktemp -d)
trap 'rm -rf "$ROOT"' EXIT
cat > "$ROOT/stat" <<'EOT'
cpu 10 2 3 40 0 0 0 0
EOT
cat > "$ROOT/meminfo" <<'EOT'
MemTotal:       1000 kB
MemAvailable:    600 kB
EOT
echo '123.5 0.0' > "$ROOT/uptime"
echo '0.10 0.20 0.30 1/100 10' > "$ROOT/loadavg"
OUT=$(SYSATLAS_PROC_ROOT="$ROOT" "$BIN")
printf '%s' "$OUT" | grep -q '"protocol_version":1'
printf '%s' "$OUT" | grep -q '"total_kib":1000'
if SYSATLAS_PROC_ROOT="$ROOT/missing" "$BIN" >/dev/null 2>&1; then echo 'expected failure for missing proc root' >&2; exit 1; fi
echo 'collector fixture tests: PASS'
