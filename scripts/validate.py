# -*- coding: utf-8 -*-
# validate.py - 校验 data/indicators.json 的所有指标在 CI 入口处合法
import json, sys
REQUIRED = ["id","name","country","category","unit","source","source_url",
            "method","confidence","note"]
CONF_OK = {"official","academic","industry_sample"}
COUNTRIES = {"CN","US","JP","WORLD"}
CATS = {"population","aging","income","employment","cost_of_living","housing",
        "wealth","inequality","economy","wage","wage_ai","distribution"}
PYRAMID_KEYS = {"age_group","male","female"}
COMPARE_KEYS = {"CN","US","JP","WORLD"}

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

        chart_type = x.get("chart_type", "line")

        if chart_type == "pyramid":
            assert "series" in x, f"{x['id']} pyramid: series required"
            assert len(x["series"]) >= 5, f"{x['id']} pyramid too few age groups"
            for p in x["series"]:
                for k in PYRAMID_KEYS:
                    assert k in p, f"{x['id']} pyramid point missing {k}"
                assert isinstance(p["male"], (int,float))
                assert isinstance(p["female"], (int,float))
                assert p["male"] >= 0 and p["female"] >= 0
        elif chart_type == "compare":
            assert isinstance(x.get("compare"), dict), f"{x['id']} compare: dict required"
            assert set(x["compare"].keys()) == COMPARE_KEYS, f"{x['id']} compare needs CN+US+JP+WORLD"
            for ctry, series in x["compare"].items():
                yrs = [p["year"] for p in series]
                assert yrs == sorted(yrs), f"{x['id']} {ctry} series not sorted"
                for p in series:
                    assert isinstance(p["year"], int) and 1990 <= p["year"] <= 2100
                    assert isinstance(p["value"], (int,float))
        else:
            assert "series" in x, f"{x['id']} series required for line chart"
            assert len(x["series"]) >= 2, f"{x['id']} series too short"
            yrs = [p["year"] for p in x["series"]]
            assert yrs == sorted(yrs), f"{x['id']} series not sorted"
            for p in x["series"]:
                assert isinstance(p["year"], int) and 1990 <= p["year"] <= 2100
                assert isinstance(p["value"], (int,float))
    print(f"OK: {len(inds)} indicators validated, last_updated={meta['last_updated']}")

if __name__ == "__main__":
    main()
