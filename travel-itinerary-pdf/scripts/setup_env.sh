#!/bin/bash
# usage: PYTHON_BIN=/path/to/python3.12 setup_env.sh <work_dir>
set -euo pipefail
WORK="${1:?usage: setup_env.sh <work_dir>}"
SK="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${PYTHON_BIN:-python3.12}"
EXPECTED="$(cat "$SK/.python-version")"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python $EXPECTED required. Install it (e.g. uv python install $EXPECTED) and set PYTHON_BIN." >&2
  exit 1
fi
if [ "$("$PYTHON" -c 'import platform; print(platform.python_version())')" != "$EXPECTED" ]; then
  echo "Python $EXPECTED required; set PYTHON_BIN to that interpreter." >&2
  exit 1
fi
mkdir -p "$WORK"
if [ ! -x "$WORK/venv/bin/python" ]; then
  "$PYTHON" -m venv "$WORK/venv"
fi
if [ "$("$WORK/venv/bin/python" -c 'import platform; print(platform.python_version())')" != "$EXPECTED" ]; then
  echo "Existing venv uses a different Python; use a fresh work directory." >&2
  exit 1
fi
"$WORK/venv/bin/python" -m pip install -q 'pip==25.3'
"$WORK/venv/bin/python" -m pip install -q -r "$SK/requirements.txt"
"$WORK/venv/bin/python" "$SK/scripts/check_toolchain.py"
"$WORK/venv/bin/python" -m playwright install chromium
printf '%s\n' "$WORK/venv/bin/python"
