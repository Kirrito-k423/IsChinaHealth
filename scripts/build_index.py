"""
build_index.py - Inline data/indicators.json into docs/index.html.

The page has <script type="application/json" id="__INDICATOR_DATA__"></script>
near the end of the file. JS reads its textContent synchronously - no fetch
required. This is robust on any static host (incl. GitHub Pages project sites
where fetch() to relative JSON has historically had CORB / MIME issues).

Run from repo root:
    python scripts/build_index.py

Idempotent. Safe to run multiple times.
"""
import json, sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "docs", "index.html")
JSON_IN = os.path.join(ROOT, "data", "indicators.json")

def fail(msg, code=1):
    print("build_index:", msg, file=sys.stderr)
    sys.exit(code)

if not os.path.isfile(HTML):
    fail(f"missing {HTML}")
if not os.path.isfile(JSON_IN):
    fail(f"missing {JSON_IN}")

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()
with open(JSON_IN, "r", encoding="utf-8") as f:
    data_text = f.read()

# Validate JSON parses (raise on error -> non-zero exit)
try:
    parsed = json.loads(data_text)
except Exception as e:
    fail(f"JSON parse error: {e}")
n_ind = len(parsed.get("indicators", []))
print(f"validating JSON: {n_ind} indicators, version {parsed.get('meta',{}).get('version','?')}")

# Use a regex that finds <script type="application/json" id="__INDICATOR_DATA__">...</script>
# at the END of the file (the placeholder, not the comment in loadData).
pattern = re.compile(
    r'(<script type="application/json" id="__INDICATOR_DATA__">)(.*?)(</script>)',
    re.DOTALL,
)
matches = list(pattern.finditer(html))
if not matches:
    fail("placeholder <script id=__INDICATOR_DATA__> not found in docs/index.html")
# Take the LAST match (defensive - earlier matches might be in JS comments).
m = matches[-1]
new_html = html[:m.start(2)] + data_text + html[m.end(2):]

if new_html == html:
    print("no changes (already up to date)")
else:
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"wrote {HTML}: html {len(html)} -> {len(new_html)} bytes, inlined {len(data_text)} bytes of JSON")
