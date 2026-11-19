#!/bin/bash
# Create a private venv with the PDF toolchain. usage: setup_env.sh <dir>  -> <dir>/venv
set -e
python3 -m venv "$1/venv"
"$1/venv/bin/pip" install -q pymupdf playwright pillow
"$1/venv/bin/python" -m playwright install chromium >/dev/null
echo "$1/venv/bin/python"
