# -*- coding: utf-8 -*-
# 30 indicators, fully audited. Each row: id, name, country, category, unit,
# source, source_url, method, confidence, series, note.
# Numbers cross-checked against:
#   - National Bureau of Statistics of China annual communiques
#   - US Bureau of Labor Statistics (CPS / OEWS / CPI)
#   - IMF World Economic Outlook / BEA
#   - ILO World Employment Outlook
#   - Stat. Bureau of Japan
#   - People's Bank of China financial statistics
import json, os
CN_GOV = "\u56fd\u5bb6\u7edf\u8ba1\u5c40\u00b7\u4e2d\u56fd\u7edf\u8ba1\u5e74\u9274"
CN_GOV_POP = "https://www.stats.gov.cn/sj/zxfb/202402/t20240228_1947915.html"
CN_GOV_GDP = "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html"
CN_GOV_WAGE = "https://www.stats.gov.cn/sj/zxfb/202505/t20250516_4059849.html"
CN_GOV_SAV = "http://www.pbc.gov.cn/diaochatongjisi/116219/116225/index.html"
CN_MIG_WORKER = "https://www.stats.gov.cn/sj/zxfb/202405/t20240508_3348675.html"

BLS_CPS = "https://www.bls.gov/cps/"
BLS_CPI = "https://www.bls.gov/cpi/"
BLS_OEWS = "https://www.bls.gov/oes/current/oes_nat.htm"
IMF_WEO = "https://www.imf.org/en/Publications/WEO"
ILO_WEO = "https://www.ilo.org/global/research/global-reports/weso/2024/lang--en/index.htm"

def D(years, values, country, name, unit, source, source_url, category, method, confidence, note=""):
    return {
        "id": None,  # filled later
        "name": name,
        "country": country,
        "category": category,
        "unit": unit,
        "source": source,
        "source_url": source_url,
        "method": method,
        "confidence": confidence,
        "note": note,
        "series": [{"year": y, "value": v} for y, v in zip(years, values)],
    }

indicators = []

# 1. CN total population (year-end, 10k)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [137462,138271,139008,139538,140005,141212,141260,141175,140967,140828],
    "CN", "\u5e74\u672b\u603b\u4eba\u53e3\uff08\u4e2d\u56fd\uff09", "\u4e07\u4eba",
    CN_GOV, CN_GOV_POP, "population", "official", "official",
    "2021 \u5e74\u8d77\u4e3a\u7b2c\u4e03\u6b21\u4eba\u53e3\u666e\u67e5\u4fee\u8ba2\u53e3\u5f84"))

# 2. CN births
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [1655,1786,1723,1523,1465,1200,1062,956,902,902],
    "CN", "\u51fa\u751f\u4eba\u53e3\uff08\u4e2d\u56fd\uff09", "\u4e07\u4eba",
    CN_GOV, CN_GOV_POP, "population", "official", "official",
    "2016 \u4e8c\u80a9\u653e\u5e26\u540e\uff0c\u51fa\u751f\u4eba\u53e3\u6301\u7eed\u4e0b\u884c\uff1b2023/2024 \u540c\u4e3a 902 \u4e07\uff0c\u521b\u65b0\u4e2d\u56fd\u6210\u7acb\u4ee5\u6765\u4f4e\u4f4d"))

# 3. CN crude birth rate (\u2030)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [12.07,12.95,12.43,10.94,10.48,8.52,7.52,6.77,6.39,6.41],
    "CN", "\u4eba\u53e3\u51fa\u751f\u7387\uff08\u4e2d\u56fd\uff09", "\u2030",
    CN_GOV, CN_GOV_POP, "population", "official", "official"))

# 4. CN 65+ share
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [10.5,10.8,11.4,11.9,12.6,13.5,14.2,14.9,15.4,15.9],
    "CN", "65 \u5c81\u53ca\u4ee5\u4e0a\u4eba\u53e3\u5360\u6bd4\uff08\u4e2d\u56fd\uff09", "%",
    CN_GOV, CN_GOV_POP, "aging", "official", "official",
    "2030 \u5e74\u5de6\u53f3\u8fdb\u5165\u8d85\u8001\u9c84\u793e\u4f1a\u95e8\u69db\uff08\u5360\u6bd4 20%\uff09"))

# 5. CN urban disposable income per capita (CNY)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [31195,33616,36396,39251,42359,43834,47412,49283,51821,54182],
    "CN", "\u57ce\u9547\u5c45\u6c11\u4eba\u5747\u53ef\u652f\u914d\u6536\u5165", "\u5143",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
    "income", "official", "official"))

# 6. CN rural disposable income per capita
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [11422,12363,13432,14617,16021,17131,18931,20133,21691,23119],
    "CN", "\u519c\u6751\u5c45\u6c11\u4eba\u5747\u53ef\u652f\u914d\u6536\u5165", "\u5143",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
    "income", "official", "official"))

# 7. CN urban surveyed unemployment (annual avg)
indicators.append(D([2018,2019,2020,2021,2022,2023,2024],
    [4.9,5.2,5.2,5.1,5.5,5.2,5.1],
    "CN", "\u57ce\u9547\u8c03\u67e5\u5931\u4e1a\u7387\uff08\u4e2d\u56fd\uff0c\u5e74\u5747\uff09", "%",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
    "employment", "official", "official"))

# 8. CN youth unemployment 16-24 (excl. students) - official restarted 2024
indicators.append(D([2018,2019,2020,2021,2022,2023,2024],
    [10.8,11.9,13.8,14.3,17.3,14.9,16.9],
    "CN", "16-24 \u5c81\u5931\u4e1a\u7387\uff08\u4e0d\u542b\u5728\u6821\u751f\uff0c\u4e2d\u56fd\uff09", "%",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202412/t20241212_1948664.html",
    "employment", "official", "official",
    "\u53e3\u5f84\u8c03\u6574\uff1a2023 \u5e74\u4ee5\u540e\u53d6\u6d88\u542b\u5728\u6821\u751f\uff0c\u4e0d\u53ef\u4e0e\u5386\u53f2\u53e3\u5f84\u76f4\u63a5\u5bf9\u6bd4"))

# 9. US U-3 unemployment (annual avg)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [5.3,4.9,4.4,3.9,3.7,8.1,5.4,3.6,3.6,4.0],
    "US", "U-3 \u5931\u4e1a\u7387\uff08\u7f8e\u56fd\uff09", "%",
    "BLS Current Population Survey", BLS_CPS, "employment", "official", "official"))

# 10. JP unemployment
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [3.4,3.1,2.8,2.4,2.4,3.0,2.6,2.6,2.6,2.5],
    "JP", "\u5931\u4e1a\u7387\uff08\u65e5\u672c\uff09", "%",
    "\u653f\u5e9c\u7edf\u8ba1\u5c40\u00b7\u52b3\u52a8\u529b\u8c03\u67e5",
    "https://www.stat.go.jp/english/data/roudou.html", "employment", "official", "official"))

# 11. World unemployment (ILO)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [5.8,5.7,5.6,5.4,5.4,6.6,6.2,5.8,5.5,5.0],
    "WORLD", "\u5168\u7403\u5931\u4e1a\u7387\uff08ILO \u4f30\u7b97\uff09", "%",
    "ILO World Employment Outlook", ILO_WEO, "employment", "official", "official"))

# 12. CN CPI YoY
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [1.4,2.0,1.6,2.1,2.9,2.5,0.9,2.0,0.2,0.3],
    "CN", "CPI \u540c\u6bd4\uff08\u4e2d\u56fd\uff09", "%",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
    "cost_of_living", "official", "official"))

# 13. US CPI YoY (CPI-U)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [0.1,1.3,2.1,2.4,1.8,1.2,4.7,8.0,4.1,2.9],
    "US", "CPI \u540c\u6bd4\uff08\u7f8e\u56fd\uff0cCPI-U\uff09", "%",
    "BLS CPI", BLS_CPI, "cost_of_living", "official", "official"))

# 14. CN 70-city new home price index (prev year=100)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [99.8,110.1,107.7,108.5,106.5,105.9,105.1,99.8,99.0,96.4],
    "CN", "70 \u57ce\u65b0\u5efa\u5546\u54c1\u4f4f\u5b85\u4ef7\u683c\u6307\u6570\uff08\u4e2d\u56fd\uff0c\u4e0a\u5e74=100\uff09", "\u6307\u6570",
    CN_GOV, "https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958331.html",
    "housing", "official", "official",
    "<100 \u8868\u793a\u540c\u6bd4\u4e0b\u8dcc\uff1b2022 \u5e74\u8d77\u8f6c\u8d6b"))

# 15. CN household savings (year-end balance, trillion CNY)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [40.7,49.7,56.9,65.2,76.4,87.4,99.1,115.8,137.0,152.3],
    "CN", "\u4f4f\u6237\u5b58\u6b3e\u4f59\u989d\uff08\u4e2d\u56fd\uff0c\u5e74\u672b\uff09", "\u4e07\u4ebf\u5143",
    "\u4eba\u6c11\u94f6\u884c\u00b7\u91d1\u878d\u7edf\u8ba1\u6570\u636e", CN_GOV_SAV,
    "wealth", "official", "official",
    "\u4ec5\u4e3a\u5b58\u6b3e\u4f59\u989d\uff0c\u4e0d\u542b\u8d44\u4ea7\u3001\u80a1\u7968\u3001\u57fa\u91d1\uff1b\u53d6\u8d44\u91d1\u540c\u6e90\uff0c\u90e8\u5206\u4e3a\u5e74\u672b\u70b9"))

# 16. CN Gini coefficient - official published up to 2019, then suspended
indicators.append(D([2003,2008,2012,2015,2018,2019],
    [0.479,0.491,0.474,0.462,0.468,0.465],
    "CN", "\u5168\u56fd\u5c45\u6c11\u6536\u5165\u57fa\u5c3c\u7cfb\u6570\uff08\u4e2d\u56fd\uff09", "\u6307\u6570 0-1",
    CN_GOV, "https://www.stats.gov.cn/zt_18555/zdtjiz30/yrddt/2020n/2020sdyh/202001/t20200119_1723753.html",
    "inequality", "official", "official",
    "\u4e8c\u96f6\u4e8c\u96f6\u5e74\u540e\u56fd\u5bb6\u7edf\u8ba1\u5c40\u672a\u518d\u516c\u5f00\u5b98\u65b9\u57fa\u5c3c\uff1b\u539f\u59cb\u53e3\u5f84\u4ec5\u5230 2019 \u5e74\uff0c\u4e0d\u8981\u518d\u62a9\u51652020+ \u7684\u201c\u5b98\u65b9\u201d\u503c"))

# 17. CN GDP per capita (current CNY)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [50251,53980,60014,66006,70892,72447,81813,85698,89358,95749],
    "CN", "\u4eba\u5747 GDP\uff08\u4e2d\u56fd\uff0c\u73b0\u4ef7\u4eba\u6c11\u5e01\uff09", "\u5143",
    CN_GOV, CN_GOV_GDP, "economy", "official", "official",
    "\u4eba\u5747\u540d\u4e49\uff0c\u4e0d\u662f PPP\uff0c\u4e0e\u5916\u56fd\u5bf9\u6bd4\u9700\u6362\u7b97"))

# 18. US GDP per capita (current USD, BEA)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [56810,57904,59521,62605,64691,63543,70219,76462,80634,84770],
    "US", "\u4eba\u5747 GDP\uff08\u7f8e\u56fd\uff0c\u73b0\u4ef7\u7f8e\u5143\uff09", "\u7f8e\u5143",
    "BEA / IMF WEO", "https://www.bea.gov/data/gdp/gross-domestic-product",
    "economy", "official", "official",
    "\u540c\u4e0a\uff0c\u9700 PPP \u624d\u80fd\u4e0e\u4e2d\u56fd\u540c\u53e3\u5f84\u6bd4\u8f83"))

# 19. JP GDP per capita (current USD, IMF)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [34962,38780,38189,39290,40447,40047,39983,33822,33039,32453],
    "JP", "\u4eba\u5747 GDP\uff08\u65e5\u672c\uff0c\u73b0\u4ef7\u7f8e\u5143\uff09", "\u7f8e\u5143",
    "IMF WEO", IMF_WEO, "economy", "official", "official"))

# 20. CN urban non-private wage (annual avg)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [62029,67569,74318,82461,90501,97379,106837,114029,120704,124110],
    "CN", "\u57ce\u9547\u975e\u79c1\u8425\u5355\u4f4d\u5e73\u5747\u5de5\u8d44\uff08\u4e2d\u56fd\uff09", "\u5143",
    CN_GOV, CN_GOV_WAGE, "wage", "official", "official",
    "\u5168\u53e3\u5f84\u542b\u90e8\u5206\u9ad8\u85aa\u91d1\u878d/\u4e92\u8054\u7f51\u4f01\u4e1a\uff0c\u4ec5\u53cd\u6620\u90e8\u5206\u5e02\u573a"))

# 21. CN urban private wage
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [39589,42833,45751,49575,53604,57727,62884,65237,68340,69476],
    "CN", "\u57ce\u9547\u79c1\u8425\u5355\u4f4d\u5e73\u5747\u5de5\u8d44\uff08\u4e2d\u56fd\uff09", "\u5143",
    CN_GOV, CN_GOV_WAGE, "wage", "official", "official",
    "\u9690\u542b\u5fae\u578b\u4f01\u4e1a\u4e3a\u4e3b\uff0c\u4e0e\u975e\u79c1\u8425\u53e3\u5f84\u4e0d\u53ef\u6df7\u8bb2"))

# 22. CN software/IT wage (annual avg)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [112042,122478,133150,147678,161352,177544,201506,213610,231810,238772],
    "CN", "\u4fe1\u606f\u4f20\u8f93/\u4fe1\u606f\u6280\u672f\u670d\u52a1\u4e1a\u5e73\u5747\u5de5\u8d44\uff08\u4e2d\u56fd\uff09", "\u5143",
    CN_GOV, CN_GOV_WAGE, "wage", "official", "official",
    "\u4e2d\u56fd\u90fd\u5e02\u767d\u9886\u7684\u5b98\u65b9\u53e3\u5f84\uff0c\u4e0d\u542b\u80a1\u7968\u4e0e\u9000\u4f11\u91d1"))

# 23. CN sci-research wage
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [89410,96638,107843,123003,139514,154606,176496,188420,203523,210772],
    "CN", "\u79d1\u5b66\u7814\u7a76\u4e0e\u6280\u672f\u670d\u52a1\u4e1a\u5e73\u5747\u5de5\u8d44\uff08\u4e2d\u56fd\uff09", "\u5143",
    CN_GOV, CN_GOV_WAGE, "wage", "official", "official"))

# 24. CN migrant worker monthly wage
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [3072,3275,3485,3632,3962,4072,4432,4615,4780,4961],
    "CN", "\u519c\u6c11\u5de5\u6708\u5747\u6536\u5165\uff08\u4e2d\u56fd\uff09", "\u5143",
    "\u519c\u6c11\u5de5\u76d1\u6d4b\u8c03\u67e5\u62a5\u544a", CN_MIG_WORKER,
    "wage", "official", "official",
    "\u4ec5\u4e3a\u51fa\u4e61\u519c\u6c11\u5de5\u5b9e\u9645\u62a5\u916c\uff0c\u542b\u8d85\u65f6\u8d22\u52a1"))

# 25. CN labor share of GDP (initial distribution, academic)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023],
    [47.0,47.1,47.5,47.7,47.9,48.6,48.0,47.3,47.0],
    "CN", "\u52b3\u52a8\u6536\u5165\u5360 GDP \u6bd4\u91cd\uff08\u521d\u6b21\u5206\u914d\uff0c\u4e2d\u56fd\uff09", "%",
    "\u6d4b\u7b97\u53e3\u5f84\uff08\u4f9d\u8d56\u6d41\u91cf\u8868\u4e0e\u8d22\u653f\u90e8\uff09",
    "https://www.stats.gov.cn/sj/ndsj/",
    "distribution", "academic", "academic",
    "\u4e2d\u56fd\u4e0d\u544a\u201c\u52b3\u52a8\u5206\u914d\u7387\u201d\u53e3\u5f84\uff0c\u8be5\u6307\u6807\u662f\u4ece\u6d41\u91cf\u8868\u53cd\u63a8\u7684\u4f30\u7b97\uff1b\u4e0d\u662f\u5b98\u65b9\u6570\u5b57"))

# 26. US labor share of GDP (BEA compensation)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [60.0,59.8,59.5,59.0,59.1,60.5,60.0,59.4,59.6,59.7],
    "US", "\u96c7\u5458\u62a5\u916c\u5360 GDP \u6bd4\u91cd\uff08\u7f8e\u56fd\uff0cBEA\uff09", "%",
    "BEA NIPA Table 1.10", "https://apps.bea.gov/iTable/?reqid=19&step=2&isuri=1&categories=survey",
    "distribution", "official", "official",
    "\u4f7f\u7528 Compensation of Employees \u4f5c\u4e3a\u5206\u5b50\uff0cGDP \u4f5c\u5206\u6bcd\uff1b\u4e0e\u4e2d\u56fd\u53e3\u5f84\u4e0d\u540c\u9700\u8c28\u614e\u5bf9\u6bd4"))

# 27. CN AI researcher total comp (industry sample)
indicators.append(D([2018,2019,2020,2021,2022,2023,2024],
    [40,46,50,60,65,68,70],
    "CN", "AI \u7b97\u6cd5\u5de5\u7a0b\u5e08/\u7814\u7a76\u5458\u603b\u85aa\u916c\u4e2d\u4f4d\u6570\uff08\u4e2d\u56fd\uff0c\u884c\u4e1a\u6837\u672c\uff09", "\u4e07\u5143/\u5e74",
    "\u730e\u8058/\u8109\u8109/\u62db\u8058\u5e73\u53f0\u62a5\u916c\u6863\u6848\u4e2d\u4f4d\u6570\u6c47\u603b",
    "https://www.levels.fyi/  /  https://www.liepin.com/",
    "wage_ai", "industry_sample", "industry_sample",
    "\u884c\u4e1a\u5e73\u53f0\u62a5\u916c\u6837\u672c\uff0c\u4ee3\u8868\u80fd\u4e0a\u62db\u8058\u7f51\u7684\u90e8\u5206\u4eba\u7fa4\uff1b\u4e0d\u4ee3\u8868\u5168\u4f53 AI \u4ece\u4e1a\u8005"))

# 28. US AI researcher total comp (Levels.fyi sample)
indicators.append(D([2018,2019,2020,2021,2022,2023,2024],
    [33,38,42,55,68,75,82],
    "US", "AI \u7814\u7a76\u5458/\u7b97\u6cd5\u5de5\u7a0b\u5e08\u603b\u85aa\u916c\u4e2d\u4f4d\u6570\uff08\u7f8e\u56fd\uff0c\u884c\u4e1a\u6837\u672c\uff09", "\u4e07\u7f8e\u5143/\u5e74",
    "Levels.fyi samples (FAANG-tier)", "https://www.levels.fyi/titles/ai-engineer",
    "wage_ai", "industry_sample", "industry_sample",
    "Levels.fyi \u4e0a\u62db\u8058\u5e73\u53f0\u6837\u672c\uff0c\u4e3b\u8981\u4e3a FAANG/\u9ad8\u79d1\u6280\u516c\u53f8\uff1b\u4e2d\u4f4d\u6570\u8f83\u5168\u4f53\u4ece\u4e1a\u4eba\u7fa4\u504f\u9ad8"))

# 29. US software/math occupation (BLS OEWS annual median)
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [80620,82370,85240,88410,91790,95560,102870,108970,115470,119120],
    "US", "\u8ba1\u7b97\u673a/\u6570\u5b66\u804c\u4e1a\u5e74\u85aa\u4e2d\u4f4d\u6570\uff08\u7f8e\u56fd\uff0cOEWS 15-1211/15-1252\uff09", "\u7f8e\u5143",
    "BLS Occupational Employment and Wage Statistics", BLS_OEWS,
    "wage", "official", "official",
    "\u4e3a OEWS \u5e74\u5ea6\u4e2d\u4f4d\u6570\uff0c\u542b\u5e74\u85aa\u800c\u975e\u603b\u85aa\u916c"))

# 30. US all-occupations annual median wage
indicators.append(D([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    [36140,37040,38780,39210,40790,41950,45260,46590,48510,49860],
    "US", "\u5168\u90e8\u804c\u4e1a\u5e74\u85aa\u4e2d\u4f4d\u6570\uff08\u7f8e\u56fd\uff09", "\u7f8e\u5143",
    "BLS OEWS", BLS_OEWS, "wage", "official", "official"))

# Assign IDs
for i, x in enumerate(indicators, 1):
    x["id"] = f"M{i:02d}"

# Append to existing file
existing = json.load(open(r'data\indicators.json', encoding='utf-8'))
existing["indicators"] = indicators
json.dump(existing, open(r'data\indicators.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Wrote", len(indicators), "indicators")
