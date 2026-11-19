#!/bin/bash
# Preflight check for the travel-itinerary-pdf skill.
# usage: preflight.sh <work_dir> [--fix]
#   Checks local tools, the Python venv, Chromium and network reach. With --fix it builds the venv
#   (pip + playwright chromium inside <work_dir>/venv). It never installs system packages or edits
#   MCP config: those are printed as commands for the user / Claude to run after asking.
# Output: one line per check, "OK|MISSING|FAIL <name> :: <fix>", then a summary line.
WORK="${1:?usage: preflight.sh <work_dir> [--fix]}"; FIX="$2"
SK="$(cd "$(dirname "$0")/.." && pwd)"
PY="$WORK/venv/bin/python"; bad=0
ok(){ echo "OK      $1"; }
no(){ echo "MISSING $1 :: $2"; bad=$((bad+1)); }
fail(){ echo "FAIL    $1 :: $2"; bad=$((bad+1)); }

# --- system tools
command -v python3 >/dev/null && ok "python3 ($(python3 --version 2>&1))" || no python3 "brew install python  (macOS) | sudo apt install python3 python3-venv"
command -v jq >/dev/null && ok jq || no jq "brew install jq | sudo apt install jq"
command -v curl >/dev/null && ok curl || no curl "brew install curl | sudo apt install curl"
command -v npx >/dev/null && ok "npx (for optional local MCP servers)" || echo "INFO    npx not found: only needed to run a local Firecrawl MCP (brew install node)"

# --- python venv + packages
if [ ! -x "$PY" ] && [ "$FIX" = "--fix" ]; then
  echo "...     creating venv in $WORK/venv"; "$SK/scripts/setup_env.sh" "$WORK" >/dev/null 2>&1
fi
if [ -x "$PY" ]; then
  for m in pymupdf playwright PIL; do
    "$PY" -c "import $m" 2>/dev/null && ok "python module $m" || {
      if [ "$FIX" = "--fix" ]; then "$WORK/venv/bin/pip" install -q pymupdf playwright pillow >/dev/null 2>&1 && ok "python module $m (installed)" || fail "python module $m" "$WORK/venv/bin/pip install pymupdf playwright pillow"; else no "python module $m" "$SK/scripts/preflight.sh $WORK --fix"; fi; }
  done
  if "$PY" - <<'EOF' 2>/dev/null; then ok "chromium for PDF rendering"; else
from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()
EOF
    if [ "$FIX" = "--fix" ]; then "$PY" -m playwright install chromium >/dev/null 2>&1 && ok "chromium (installed)" || fail chromium "$PY -m playwright install chromium"
    else no chromium "$PY -m playwright install chromium"; fi
  fi
else
  no "python venv" "$SK/scripts/preflight.sh $WORK --fix   (or $SK/scripts/setup_env.sh $WORK)"
fi

# --- network reach (photos, fonts, flight sites)
for u in https://commons.wikimedia.org https://cf.bstatic.com https://fonts.googleapis.com https://www.skyscanner.co.in; do
  code=$(curl -s -o /dev/null -m 10 -w '%{http_code}' -A "Mozilla/5.0" "$u")
  if [ "$code" != "000" ]; then ok "reach $u"; else fail "reach $u" "no connection (offline, proxy or firewall): photos/fonts/fares from it will be missing"; fi
done

echo "SUMMARY $bad issue(s)"; exit 0
