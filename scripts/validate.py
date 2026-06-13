# -*- coding: utf-8 -*-
# validate.py - 校验 data/indicators.json 的所有指标在 CI 入口处合法
import json, sys
REQUIRED = ["id","name","country","category","unit","source","source_url",
            "method","confidence","series","note"]
CONF_OK = {"official","academic","industry_sample"}
COUNTRIES = {"CN","US","JP","WORLD"}
CATS = {"population","aging","income","employment","cost_of_living","housing",
        "wealth","inequality","economy","wage","wage_ai","distribution"}

def main():
    data = json.load(open("data/indicators.json", encoding="utf-8"))
    meta = data.get("meta", {})
    assert "version" in meta and "last_updated" in meta, "meta missing"
    inds = data["indicators"]
    seen = set()
    for x in inds:
        for k in REQUIRED:
            assert k in x, f"{x.get('id','?')} missing {k}"
        assert x["id"] not in seen, f"dup id {x['id']}"
        seen.add(x["id"])
        assert x["country"] in COUNTRIES, f"{x['id']} bad country"
        assert x["category"] in CATS, f"{x['id']} bad category"
        assert x["confidence"] in CONF_OK, f"{x['id']} bad confidence"
        assert x["source_url"].startswith("http"), f"{x['id']} bad url"
        yrs = [p["year"] for p in x["series"]]
        assert yrs == sorted(yrs), f"{x['id']} series not sorted"
        for p in x["series"]:
            assert isinstance(p["year"], int) and 1990 <= p["year"] <= 2100
            assert isinstance(p["value"], (int,float))
    print(f"OK: {len(inds)} indicators validated, last_updated={meta['last_updated']}")

if __name__ == "__main__":
    main()
