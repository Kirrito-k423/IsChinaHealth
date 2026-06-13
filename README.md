# IsChinaHealth

> A data-driven, non-sensational look at how life is actually going for people
> in China, the US, Japan, and the world — with full source citations on every chart.

中文简介见下文。

---

## What this project is

A continuously-updated, fully-cited, **static** data dashboard that compares
real-world wellbeing indicators across China, the US, Japan, and the world,
with sub-cuts for:

- 全体居民 / 城市居民 / 农村居民 / 农民工
- 计算机 / 软件行业平均工资
- AI 研究员 / 算法工程师总薪酬

It exists to push back against the wave of AI-generated, engagement-bait
"China is collapsing" or "AI will eat everyone's job" content on Bilibili,
Zhihu, and Xiaohongshu, by anchoring every claim to a **verifiable primary
source** and labelling each indicator's confidence level honestly.

## Confidence levels

Every chart carries a coloured border:

| Border | Tag | Meaning |
|---|---|---|
| 🟢 green | `official` | Government / IGO data, directly traceable to source URL |
| 🟡 amber | `academic` | Academic / think-tank estimate (e.g. labour share) |
| 🔴 red | `industry_sample` | Industry-platform sample (Levels.fyi / 脉脉 / 猎聘) — *not* representative of the whole occupation |

A red border is **not** "this is wrong" — it is "this comes from a non-random
sample, so the number is real but the population it represents is narrower
than the chart title suggests". The page always shows the source URL inline
so you can verify the figure yourself.

## Tech

- **Static**: pure `docs/index.html` + Chart.js (CDN), no build step, no
  framework. Open it from `file://` or any static host.
- **Data**: `data/indicators.json` is the single source of truth. 30 indicators,
  each with `id / name / country / category / unit / source / source_url /
  method / confidence / series / note`.
- **Auto-update**: `.github/workflows/weekly.yml` runs every Monday 06:00 UTC
  to (1) pull primary-source updates via `scripts/fetch.py`,
  (2) commit any new data, (3) redeploy GitHub Pages.

## Local run

```bash
# 1. serve the docs/ directory
cd docs
python -m http.server 8000
# open http://127.0.0.1:8000/
```

The page reads `../data/indicators.json` — for GitHub Pages this resolves to
the repo root; for local `python -m http.server` started inside `docs/` it
resolves to the parent. Don't move the data file.

## Add a new indicator

1. Add a new entry to `data/indicators.json` with all required fields
   (see `scripts/validate.py` for the schema).
2. Pick a `confidence` value that matches the **strongest** claim you make.
3. Add a fetcher spec in `scripts/fetch.py` so the next weekly run can update it.
4. Open a PR. CI will reject the change if any field is missing or
   the series is not sorted.

## Project structure

```
.
├── data/
│   ├── indicators.json     # single source of truth, 30 indicators
│   └── .cache/             # ignored: 30-day HTTP cache for fetcher
├── docs/
│   └── index.html          # the dashboard
├── scripts/
│   ├── fetch.py            # pull primary-source data
│   ├── validate.py         # CI gate
│   ├── build_data.py       # one-time seed script
│   └── build_meta.py       # one-time meta seed
└── .github/workflows/
    └── weekly.yml          # cron + Pages deploy
```

## License

- **Data**: each indicator's source URL points to the publisher; data
  copyrights remain with the original publishers.
- **This compilation, code, and text**: CC BY 4.0.

---

## 中文简介

这个项目做一件事：用可验证的官方数据，做一份"中/美/世界民生关键指标"
的持续更新可视化看板，覆盖：

- 人口：总人口、出生人口、出生率、老龄化（65+ 占比）
- 收入：城镇/农村居民人均可支配收入、人均 GDP
- 工资：城镇非私营/私营、信息传输/IT、科学研究、农民工月均
  - **AI 研究员/算法工程师总薪酬**（中美对比，行业样本）
  - 美国 OEWS 全部职业 + 计算机/数学职业年薪中位数
- 就业：城镇调查失业率、16-24 岁青年失业率（不含在校生）、U-3、
  日本失业率、ILO 全球失业率
- 生活成本：CPI 同比（中/美）
- 住房：70 城新建商品住宅价格指数
- 财富与差距：住户存款余额、基尼系数、劳动分配率

### 为什么做这个

B 站、知乎、小红书上有大量以"贫富差距""出生率""老龄化""低工资"为题
的视频，但很多内容：

- 引用了**部分数据但未给出原始来源**；
- 把**短期数据**和**长期趋势**混用，渲染情绪；
- 把**官方统计**和**行业样本**混为一谈。

本项目坚持：

1. **每张图都标 source URL**，可直接跳转到国家统计局 / 美国 BLS / IMF /
   ILO 原文；
2. **每张图都标 confidence**：🟢 official / 🟡 academic / 🔴 industry_sample；
3. **不静默补充**：fetcher 拿不到的数据点会保留原值并打 `EMPTY` 日志，
   不会为了"完整"而编造。

### 自动更新

`.github/workflows/weekly.yml`：

- 每周一 06:00 UTC（北京时间 14:00）拉取主源；
- 校验 JSON；
- 部署到 GitHub Pages。

### 部署

1. 在 GitHub 仓库 **Settings → Pages** 选 **Source: GitHub Actions**；
2. 第一次 push 到 `main` 会触发 workflow，自动部署；
3. 之后每周自动更新。

### 本地运行

```bash
cd docs
python -m http.server 8000
# 浏览器打开 http://127.0.0.1:8000/
```

### 提 PR 加新指标

1. 在 `data/indicators.json` 加一条；
2. 在 `scripts/fetch.py` 加对应 fetcher；
3. CI 自动校验 schema。

---

> 重要提示：本页面是个人/社区性质的数据整理，**不构成投资建议、
> 政策建议或对任何国家的整体评价**。所有数据原始版权归原始发布机构。
