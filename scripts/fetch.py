# -*- coding: utf-8 -*-
# fetch.py - 拉取/校验 primary-source 数据。
# 设计原则：宁可本次少更，绝不静默补数据。失败用上次值。
#
# 用法（在 GitHub Actions 里）：
#   python scripts/fetch.py            # 跑所有 fetcher
#   python scripts/fetch.py --dry-run  # 只打印计划
#
# 拉到的原始 JSON/HTML 落到 data/.cache/（gitignore），避免重复抓。
import json, os, sys, io, re, time, hashlib, argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IsChinaHealthBot/0.2; +https://github.com/IsChinaHealth/IsChinaHealth)"
}
TIMEOUT = 25

def cache_path(url):
    os.makedirs("data/.cache", exist_ok=True)
    return "data/.cache/" + hashlib.sha256(url.encode()).hexdigest()[:16] + ".bin"

def http_get(url, max_age_days=30):
    p = cache_path(url)
    fresh = os.path.exists(p) and (time.time() - os.path.getmtime(p)) < max_age_days*86400
    if fresh:
        return open(p, "rb").read()
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=TIMEOUT) as r:
        body = r.read()
    open(p, "wb").write(body)
    return body

# ---- parsers: 每个必须保守，parse 不到就返回 [] ----

def find_int_in_paragraph(body, year, before_regex, after_regex, max_skip=8000):
    """Find a year/.../N <after> in HTML text near <before> context."""
    text = re.sub(r"<[^>]+>", " ", body.decode("utf-8", errors="ignore"))
    text = re.sub(r"\s+", " ", text)
    # Try direct: \u5e74\u672b\u603b\u4eba\u53e3 140828 \u4e07\u4eba
    for m in re.finditer(before_regex + r"[^0-9-]{0,40}?(\d{2,7}(?:\.\d+)?)\s*" + after_regex, text):
        return float(m.group(1))
    return None

# --- Population (CN, year-end, 10000) ---
def parse_cn_population(body):
    v = find_int_in_paragraph(body, 0, r"\u5e74\u672b\u603b\u4eba\u53e3", r"\u4e07\u4eba")
    return [(int(time.strftime("%Y")), v)] if v else []

# --- CN births ---
def parse_cn_births(body):
    text = re.sub(r"<[^>]+>", " ", body.decode("utf-8", errors="ignore"))
    m = re.search(r"\u51fa\u751f\u4eba\u53e3[^0-9]{0,30}(\d{3,5})\s*\u4e07\u4eba", text)
    if not m: return []
    return [(int(time.strftime("%Y")), float(m.group(1)))]

# --- Generic China NBS year-list scraper: page lists years+values ---
# e.g. "\u57ce\u9547\u5c45\u6c11...  31195  33616  36396  ..."  (multi-year inline)
def parse_cn_yoy_series(body, label_regex, value_count=10):
    text = re.sub(r"<[^>]+>", " ", body.decode("utf-8", errors="ignore"))
    text = re.sub(r"\s+", " ", text)
    m = re.search(label_regex + r"(.+?)", text)
    if not m: return []
    chunk = m.group(1)[:1200]
    nums = re.findall(r"-?\d{1,7}(?:\.\d+)?", chunk)
    if len(nums) < value_count: return []
    cur_year = int(time.strftime("%Y"))
    start = cur_year - value_count + 1
    return [(start + i, float(n)) for i, n in enumerate(nums[:value_count])]

# --- World / US / JP from IMF WEO CSV ---
def parse_imf_weo_csv(body, country_code, indicator):
    """IMF WEO CSVs from imf.org. Expected columns: Country, Subject Descriptor, Units, Scale, 2015, 2016..."""
    text = body.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    header = [h.strip('"') for h in lines[0].split(",")]
    if not any(c == country_code for c in header[:5]):
        return []
    out = []
    for row in lines[1:]:
        cells = [c.strip('"') for c in row.split(",")]
        if cells[0] != country_code: continue
        if indicator.lower() not in cells[1].lower() and indicator.lower() not in cells[2].lower(): continue
        for y_str in header[9:]:
            if not y_str.isdigit(): continue
            v = cells[header.index(y_str)]
            try:
                out.append((int(y_str), float(v)))
            except (ValueError, IndexError):
                pass
    return out

# --- US BLS CPS unemployment: a series table with year and annual avg ---
def parse_bls_cps_annual(body):
    text = body.decode("utf-8", errors="ignore")
    out = []
    for m in re.finditer(r"(20\d{2})\D{0,10}(\d{1,2}\.\d)", text):
        out.append((int(m.group(1)), float(m.group(2))))
    return out

# ---- fetcher spec list ----
# (id, url, parser, kw)
FETCHERS = [
    ("M01", "https://www.stats.gov.cn/sj/zxfb/202402/t20240228_1947915.html", parse_cn_population, {}),
    ("M02", "https://www.stats.gov.cn/sj/zxfb/202402/t20240228_1947915.html", parse_cn_births, {}),
    ("M05", "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
     parse_cn_yoy_series,
     {"label_regex": r"\u57ce\u9547\u5c45\u6c11\u4eba\u5747\u53ef\u652f\u914d\u6536\u5165", "value_count": 10}),
    ("M06", "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
     parse_cn_yoy_series,
     {"label_regex": r"\u519c\u6751\u5c45\u6c11\u4eba\u5747\u53ef\u652f\u914d\u6536\u5165", "value_count": 10}),
    ("M09", "https://www.bls.gov/cps/", parse_bls_cps_annual, {}),
]

def dry_run():
    print(f"DRY RUN: {len(FETCHERS)} fetchers defined")
    for spec in FETCHERS:
        print("  ", spec[0], spec[1])

def real_run():
    data = json.load(open("data/indicators.json", encoding="utf-8"))
    for ind in data["indicators"]:
        spec = next((s for s in FETCHERS if s[0] == ind["id"]), None)
        if not spec: continue
        _, url, parser, kw = spec
        try:
            body = http_get(url)
        except Exception as e:
            print(f"FAIL {ind['id']}: {e} (keeping previous value)")
            continue
        try:
            series = parser(body, **kw) if kw else parser(body)
        except Exception as e:
            print(f"PARSE-FAIL {ind['id']}: {e}")
            continue
        if not series:
            print(f"EMPTY {ind['id']} (page shape changed or year missing)")
            continue
        # audit
        existing_years = {p["year"] for p in ind["series"]}
        appended = 0
        for y, v in series:
            if y in existing_years:
                # update if value changed > 0.5%
                old = next(p for p in ind["series"] if p["year"] == y)["value"]
                if old and abs(v - old) / abs(old) > 0.005:
                    print(f"REVISED {ind['id']} {y}: {old} -> {v}")
                    ind["series"] = [p for p in ind["series"] if p["year"] != y]
                    ind["series"].append({"year": y, "value": v})
            else:
                ind["series"].append({"year": y, "value": v})
                appended += 1
        if appended:
            print(f"OK {ind['id']} +{appended}")
    data["meta"]["last_updated"] = time.strftime("%Y-%m-%d")
    json.dump(data, open("data/indicators.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.dry_run:
        dry_run()
    else:
        real_run()
