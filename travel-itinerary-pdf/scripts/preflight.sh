#!/bin/bash
# Checks all requirements; --fix installs only in the supplied work directory.
set -uo pipefail
WORK="${1:?usage: preflight.sh <work_dir> [--fix]}"
FIX="${2:-}"
if [ -n "$FIX" ] && [ "$FIX" != "--fix" ]; then
  echo 'usage: preflight.sh <work_dir> [--fix]' >&2
  exit 2
fi
SK="$(cd "$(dirname "$0")/.." && pwd)"
PY="$WORK/venv/bin/python"
bad=0
ok(){ echo "OK      $1"; }
no(){ echo "MISSING $1 :: $2"; bad=$((bad+1)); }
fail(){ echo "FAIL    $1 :: $2"; bad=$((bad+1)); }
for tool in jq curl; do
  command -v "$tool" >/dev/null 2>&1 && ok "$tool" || no "$tool" "Install $tool with your system package manager"
done
if [ "$FIX" = '--fix' ]; then
  "$SK/scripts/setup_env.sh" "$WORK" || fail setup "setup_env.sh failed; see output above"
fi
if [ -x "$PY" ]; then
  "$PY" "$SK/scripts/check_toolchain.py" && ok 'pinned Python toolchain' || fail toolchain "Run preflight.sh $WORK --fix with Python $(cat "$SK/.python-version")"
  if "$PY" - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
PY
  then ok 'chromium launch'
  else fail chromium "Run $PY -m playwright install chromium; check browser launch dependencies"
  fi
else
  no 'python venv' "Run preflight.sh $WORK --fix"
fi
# HTTP errors still demonstrate reachability; they do not verify search access or quotes.
for url in https://commons.wikimedia.org https://cf.bstatic.com https://fonts.googleapis.com https://www.skyscanner.co.in; do
  if code=$(curl -s -o /dev/null -m 10 -w '%{http_code}' -A 'Mozilla/5.0' "$url") && [ "$code" != '000' ]; then
    ok "reach $url (HTTP $code; connectivity only)"
  else
    fail "reach $url" 'Connection failed; check network/proxy'
  fi
done
echo "SUMMARY $bad issue(s)"
[ "$bad" -eq 0 ]
