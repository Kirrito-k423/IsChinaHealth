# -*- coding: utf-8 -*-
# validate.py
import json, sys
REQUIRED = ["id","name","country","category","unit","source","source_url",
            "method","confidence","note"]
CONF_OK = {"official","academic","industry_sample"}
COUNTRIES = {"CN","US","JP","WORLD"}
CATS = {"population","aging","income","employment","cost_of_living","housing",
        "wealth","inequality","economy","wage","wage_ai","distribution"}
PYRAMID_KEYS = {"age_group","male","female"}
COMPARE_KEYS = {"CN","US","JP","WORLD"}
INCOME_KEYS = {"decile","male","female"}
WAGE_KEYS = {"sector","CN","US","JP","WORLD"}

def main():
    data = json.load(open("data/indicators.json", encoding="utf-8"))
    meta = data.get("meta", {})
    assert "version" in meta and "last_updated" in meta
    inds = data["indicators"]
    seen = set()
    for x in inds:
        for k in REQUIRED:
            assert k in x, f"{x.get('id','?')} missing {k}"
        assert x["id"] not in seen, f"dup id {x['id']}"
        seen.add(x["id"])
        assert x["country"] in COUNTRIES
        assert x["category"] in CATS
        assert x["confidence"] in CONF_OK
        assert x["source_url"].startswith("http")

        ct = x.get("chart_type", "line")
        if ct == "pyramid":
            assert "series" in x
            assert len(x["series"]) >= 5
            for p in x["series"]:
                for k in PYRAMID_KEYS:
                    assert k in p
                assert isinstance(p["male"], (int,float))
                assert isinstance(p["female"], (int,float))
        elif ct == "compare":
            assert isinstance(x.get("compare"), dict)
            assert set(x["compare"].keys()) == COMPARE_KEYS
            for ctry, series in x["compare"].items():
                yrs = [p["year"] for p in series]
                assert yrs == sorted(yrs)
                for p in series:
                    assert isinstance(p["year"], int) and 1990 <= p["year"] <= 2100
                    assert isinstance(p["value"], (int,float))
        elif ct == "income_pyramid":
            assert "series" in x
            assert len(x["series"]) >= 5
            for p in x["series"]:
                for k in INCOME_KEYS:
                    assert k in p, f"{x['id']} income_pyramid point missing {k}"
                assert isinstance(p["male"], (int,float))
                assert isinstance(p["female"], (int,float))
        elif ct == "wage_table":
            assert "rows" in x and len(x["rows"]) >= 3
            for r in x["rows"]:
                for k in WAGE_KEYS:
                    assert k in r, f"{x['id']} wage row missing {k}"
                for c in ("CN","US","JP","WORLD"):
                    v = r[c]
                    assert v is None or isinstance(v, (int,float)), f"{x['id']} {r['sector']} {c} not None/number"
        else:
            assert "series" in x
            assert len(x["series"]) >= 2
            yrs = [p["year"] for p in x["series"]]
            assert yrs == sorted(yrs)
            for p in x["series"]:
                assert isinstance(p["year"], int) and 1990 <= p["year"] <= 2100
                assert isinstance(p["value"], (int,float))
    print(f"OK: {len(inds)} indicators validated, last_updated={meta['last_updated']}")

if __name__ == "__main__":
    main()
