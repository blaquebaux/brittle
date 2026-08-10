#!/usr/bin/python3
# =============================================================================
# brittle_1_premium_illusion.py — BLAQUE BAUX BRITTLE #1 (the Sharpe lies).
#
# Brittle is the SELL side of convexity (mirror of Bleed). Selling volatility / OTM premium
# earns positive carry in calm and posts a decent Sharpe — but the Sharpe is an ILLUSION:
# the distribution is severely negatively skewed and a single vol spike undoes years.
#   - NAKED short-vol (SVXY): Sharpe +0.42 but ~+1% CAGR over a DECADE, -95% drawdown,
#     skew -8.3, worst day -83%. You risked near-total ruin to make nothing.
#   - DEFINED-RISK premium selling (put-write PUTW, covered-call QYLD/XYLD): survivable
#     (Sharpe ~0.6, tail ~-25/-30%) — but it UNDERPERFORMS just holding SPY (+0.82/+14%).
#     A capped-upside/kept-downside risk profile, not alpha.
#
# RESULTS AS TESTED (2016-2026):
#   proxy            Sharpe  CAGR  maxDD  skew  worstDay  CVaR5%
#   SVXY short-vol    +0.42   +1%  -95%   -8.3   -83%     -8.5%
#   PUTW put-write    +0.57   +7%  -28%   -1.8   -11%     -2.2%
#   QYLD covered-call +0.58   +8%  -25%   -1.1   -10%     -2.6%
#   SPY (reference)   +0.82  +14%  -34%   -0.7   -11%     -2.8%
# Read-only.
# =============================================================================
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _brittle_common import align, dist

ds, P = align(["SVXY", "PUTW", "QYLD", "XYLD", "SPY"]); R = {s: P[s][1:] / P[s][:-1] - 1 for s in P}
print("=" * 80, "\nBRITTLE #1 — the premium harvest: Sharpe vs the true distribution\n" + "=" * 80)
print(f"  {'proxy':<20}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'skew':>8}{'worstDay':>10}{'CVaR5%':>9}")
for nm, s in [("SVXY short-vol", "SVXY"), ("PUTW put-write", "PUTW"), ("QYLD covered-call", "QYLD"),
              ("XYLD covered-call", "XYLD"), ("SPY (reference)", "SPY")]:
    d = dist(R[s])
    print(f"  {nm:<20}{d['sh']:>+8.2f}{d['cagr']*100:>+7.0f}%{d['dd']*100:>7.0f}%{d['skew']:>+8.1f}{d['worst']:>+9.0f}%{d['cvar']:>+8.1f}%")
print("\nVERDICT: naked short-vol is a Sharpe illusion — ~1% CAGR for a -95% drawdown and -8.3")
print("skew. Defined-risk premium selling (put-write / covered-call) survives but underperforms")
print("simply holding SPY. Selling convexity is a capped-risk profile, not an edge.")
