# AI ROI Dataset — 200 B2B AI deployments in France (2022-2025)





## Headline figures

The central variable is a **gain-to-investment ratio**, not a net ROI. Any citation must state the scope and the nature of the metric.

| Indicator | Value | Scope | n |
|---|---|---|---|
| **Median annual gain / investment** | **159.8 %** (1.60×) | Deployments carried through to production | 165 |
| Median annual gain / investment | **127.4 %** (1.27×) | Full cohort, failures included | 200 |
| **Production rate** | **82.5 %** | Deployments in production (`failure = 0`) | 165/200 |
| **12-month profitability rate** | **60.5 %** | Annual gain ≥ investment (`roi_percent ≥ 100`) | 121/200 |
| Median annual gain / investment, failed deployments | −3.4 % | Failed deployments | 35 |

> **How to cite.** *"Median annual gain equal to 159.8 % of investment (1.60×) across 165 deployments carried through to production (82.5 % of the cohort); 127.4 % (1.27×) across the full cohort of 200."* Never write "median ROI of 159.8 % across 200 deployments": neither the scope nor the nature of the metric would be accurate.

## Variable definition

```
roi_percent = annual_gain_eur / investment_eur × 100
```

A value of 159.8 % means the annual gain equals **1.598 times** the amount invested. This is **not** a net ROI. Under the standard accounting definition — `(gain − investment) / investment` — the corresponding medians are **59.8 %** (deployments in production) and **27.4 %** (full cohort), exactly 100 points lower.

A previously documented formula, `(2 × annual gain − investment) / investment`, **matches none of the 200 rows** and has been withdrawn. Under that formula the median for deployments in production would be 219.5 %.

`annual_gain_eur` is a twelve-month figure: published values are **annualised, not cumulative**. Earlier references to a "24-month window" described the observation period of the deployments, not a gain accumulation period.

## Known data issue

All 35 failed deployments have `annual_gain_eur = 0`, yet **17 of them carry a positive `roi_percent`** that the formula above cannot reproduce. These values originate from an undocumented earlier entry and **must not be used**. They are kept unchanged so as not to alter the source file, and are flagged here.

## Production rate is not a profitability rate

Among the 165 deployments in production, **44 (26.7 %) have an annual gain lower than the investment** — e.g. P002: €14,533 invested, €1,469 annual gain (10.1 %). They are classified `failure = 0` because they are **in production and in use**, which is the definition applied to that field. The 12-month profitability rate is reported separately: **60.5 %**.

## Reproduction

```bash
python3 verify_metrics.py ai_roi_dataset_200_deployments.csv
```

No external dependency. Any run reproduces the figures above, on all three readings.

## Declared limitations

1. **Observational study**, not experimental: no control group, no randomisation. Observed correlations do not establish causality.
2. **Conflict of interest**: the author acted as consultant or service provider on a majority of the documented deployments.
3. **Acknowledged selection bias**: deployments come from an engagement portfolio, not a random sample of French companies.
4. **Two calculation scopes**: restricting a median to successful cases introduces a survivorship bias; both scopes are therefore published together.
5. **Self-reported data**: gains and investments come from client declarations. Part of the sample underwent documentary review (see `technical_report.md`). No independent external audit was carried out.
6. **Anonymisation**: companies are anonymised for contractual and GDPR reasons, which prevents row-level third-party verification.
7. **Uneven time horizon**: 2025 deployments have less hindsight than 2022 ones.
8. **Not peer-reviewed**: dataset and report are self-published on open platforms (Zenodo, GitHub, Hugging Face, SSRN). The DOI guarantees permanence and citability, not scientific validation.


## Repository contents

| File | Description |
|---|---|
| `ai_roi_dataset_200_deployments.csv` | Data, 200 rows, 20 variables |
| `data_dictionary.md` | Variable dictionary |
| `verify_metrics.py` | Reproduction script for all published figures |
| `technical_report.md` | Methodology, collection, review, limitations |
| `CHANGELOG.md` | Version history and revisions |
| `README.md` | This file |


---
