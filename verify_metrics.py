#!/usr/bin/env python3
"""
Reproduction of published metrics — AI ROI Dataset (N=200), ENDKOO / Denis Atlan.
Usage: python3 verify_metrics.py ai_roi_dataset_200_deployments.csv
No external dependencies. Anyone running this script should obtain exactly the
values published in the README and technical report.
"""
import sys, csv, statistics as st
from typing import Optional

def load(path: str):
    with open(path, encoding='utf-8-sig', newline='') as fh:
        return [r for r in csv.DictReader(fh) if r.get('project_id')]

def num(v: object) -> Optional[float]:
    v = str(v).strip().replace(',', '.')
    return float(v) if v not in ('', 'NA') else None

def main(path: str):
    rows = load(path)
    roi_all = [value for r in rows if (value := num(r['roi_percent'])) is not None]
    ok = [value for r in rows if r['failure'] == '0'
          if (value := num(r['roi_percent'])) is not None]
    ko = [value for r in rows if r['failure'] == '1'
          if (value := num(r['roi_percent'])) is not None]

    print(f"N total                          : {len(rows)}")
    print(f"Successful deployments (n)        : {len(ok)}")
    print(f"Failed deployments (n)            : {len(ko)}")
    print(f"Success rate                      : {len(ok)/len(rows)*100:.1f} %")
    print()
    print("--- PRIMARY METRIC: annual gain / investment ratio ---")
    print(f"Median ROI, full cohort           : {st.median(roi_all):.1f} %   <-- reference figure")
    print(f"Mean ROI, full cohort             : {st.mean(roi_all):.1f} %")
    print(f"Q1 / Q3, full cohort              : {st.quantiles(roi_all,n=4)[0]:.1f} % / {st.quantiles(roi_all,n=4)[2]:.1f} %")
    print(f"Min / Max                        : {min(roi_all):.1f} % / {max(roi_all):.1f} %")
    print(f"Deployments with zero/negative ROI: {sum(1 for x in roi_all if x <= 0)}")
    print()
    print("--- SECONDARY METRIC (subpopulation) ---")
    print(f"Median ROI, successful deployments: {st.median(ok):.1f} %   (n={len(ok)}, excluding failures)")
    print(f"Median ROI, failed deployments     : {st.median(ko):.1f} %   (n={len(ko)})")
    print()
    rent = [r for r in rows if (roi := num(r['roi_percent'])) is not None and roi >= 100]
    prod_nonrent = [r for r in rows if r['failure']=='0'
                    and (roi := num(r['roi_percent'])) is not None and roi < 100]
    print(f"12-month profitability rate       : {len(rent)/len(rows)*100:.1f} % ({len(rent)}/{len(rows)}, ratio >= 100%)")
    print(f"In production but not profitable  : {len(prod_nonrent)} of 165 ({len(prod_nonrent)/165*100:.1f} %)")
    print()
    print("--- ALTERNATIVE VIEW: net ROI under the accounting definition (gain - inv)/inv ---")
    def net_roi(r: dict[str, str]) -> Optional[float]:
        gain = num(r['annual_gain_eur'])
        investment = num(r['investment_eur'])
        if gain is None or investment is None or investment == 0:
            return None
        return (gain - investment) / investment * 100

    net_all = [value for r in rows if (value := net_roi(r)) is not None]
    net_ok: list[float] = []
    for r in rows:
        if r['failure'] != '0':
            continue
        gain = num(r['annual_gain_eur'])
        investment = num(r['investment_eur'])
        if gain is not None and investment is not None and investment != 0:
            net_ok.append((gain - investment) / investment * 100)
    print(f"Median net ROI, full cohort       : {st.median(net_all):.1f} %")
    print(f"Median net ROI, in-production     : {st.median(net_ok):.1f} %")
    print()
    print("--- CONSISTENCY CHECK ---")
    ko_zero = [r for r in rows if r['failure']=='1' and num(r['annual_gain_eur'])==0
               and (roi := num(r['roi_percent'])) is not None and roi > 0]
    print(f"Failed deployments with zero gain but roi_percent > 0: {len(ko_zero)} "
          f"(non-reproducible values; see README)")
    print()
    print("--- SEGMENTS (full cohort) ---")
    for size, label in (('PME', 'SME'), ('ETI', 'mid-sized'), ('Grande', 'large')):
        v = [value for r in rows if r['company_size'] == size
             if (value := num(r['roi_percent'])) is not None]
        print(f"  {label:<10} n={len(v):<3} median {st.median(v):6.1f} %")
    print()
    print("--- HUMAN OVERSIGHT (Human in the Loop) ---")
    for flag, lab in (('1', 'with HIL'), ('0', 'without HIL')):
        v = [value for r in rows if r['human_in_loop'] == flag
             if (value := num(r['roi_percent'])) is not None]
        s = sum(1 for r in rows if r['human_in_loop'] == flag and r['failure'] == '0')
        print(f"  {lab:<12} n={len(v):<4} median {st.median(v):6.1f} %   success rate {s/len(v)*100:.1f} %")
    print()
    print("--- TIMING ---")
    d = [value for r in rows
         if (value := num(r['days_to_positive_roi'])) is not None]
    print(f"  Days to positive ROI: median {st.median(d):.0f} (n={len(d)})")
    inv = [value for r in rows if (value := num(r['investment_eur'])) is not None]
    print(f"  Investment: median {st.median(inv):,.0f} EUR".replace(',', ' '))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'ai_roi_dataset_200_deployments.csv')
