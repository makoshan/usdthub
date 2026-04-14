#!/usr/bin/env bash
# Build the Jekyll site, verify it, push docs/ to GitHub Pages, and smoke-test the live URL.
# Usage: ./scripts/deploy.sh ["optional commit message"]

set -euo pipefail

cd "$(dirname "$0")/.."

LIVE_URL="https://makoshan.github.io/usdthub/"
EXPECTED_CSS="/usdthub/assets/css/style.css"
msg="${1:-Rebuild site}"

red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
blue()  { printf '\033[34m%s\033[0m\n' "$*"; }

# 1. Refuse to deploy if `jekyll serve` is running — it taints docs/sitemap.xml
#    with localhost URLs via auto-regeneration.
if lsof -ti:4000 >/dev/null 2>&1; then
  red "==> jekyll serve is running on :4000 — kill it first (it overwrites docs/ with localhost URLs)"
  red "    pid: $(lsof -ti:4000)"
  exit 1
fi

# 2. Refuse to deploy with a dirty source tree (anything outside docs/).
if ! git diff --quiet -- ':!docs'; then
  red "==> uncommitted changes outside docs/ — commit or stash them first"
  git status --short -- ':!docs'
  exit 1
fi

# 3. Build with explicit production config (defensive — _config.yml already has the right url).
blue "==> jekyll build"
JEKYLL_ENV=production bundle exec jekyll build

# 4. Verify the build with the existing site checker (broken links, missing meta, etc).
blue "==> scripts/check_site.py"
python3 scripts/check_site.py

# 5. Defense in depth: every built HTML page must reference the production CSS.
blue "==> verifying every built page links the production stylesheet"
missing=()
for f in docs/*.html; do
  if ! grep -q "$EXPECTED_CSS" "$f"; then
    missing+=("$f")
  fi
done
if [ "${#missing[@]}" -gt 0 ]; then
  red "==> these pages are missing the stylesheet link:"
  printf '    %s\n' "${missing[@]}"
  exit 1
fi

# 6. Defense in depth: no localhost leakage in any built file.
if grep -rIl "localhost:4000" docs/ >/dev/null 2>&1; then
  red "==> localhost:4000 leaked into docs/ — re-run after killing jekyll serve"
  grep -rIl "localhost:4000" docs/
  exit 1
fi

# 7. Commit only if docs/ actually changed.
if git diff --quiet --exit-code docs/ && [ -z "$(git ls-files --others --exclude-standard docs/)" ]; then
  green "==> docs/ unchanged, nothing to deploy"
  exit 0
fi

blue "==> committing docs/"
git add docs/
git commit -m "$msg"

blue "==> pushing to origin"
branch="$(git rev-parse --abbrev-ref HEAD)"
git push origin "$branch"

# 8. Live smoke test: poll the production URL until the new CSS link appears.
blue "==> smoke-testing $LIVE_URL"
for i in $(seq 1 12); do
  if curl -sf "$LIVE_URL" | grep -q "$EXPECTED_CSS"; then
    green "==> live (attempt $i): $LIVE_URL"
    exit 0
  fi
  printf '    attempt %d/12 — Pages still building, waiting 15s\n' "$i"
  sleep 15
done

red "==> smoke test timed out after 3 min — Pages may still be building. Check:"
red "    https://github.com/makoshan/usdthub/actions"
exit 1
