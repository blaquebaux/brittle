#!/usr/bin/python3
# =============================================================================
# brittle_2_tail_and_hedge.py — BLAQUE BAUX BRITTLE #2 (the tail is the whole game).
#
#   (a) THE VOL RISK PREMIUM IS REAL BUT UN-HARVESTABLE NAKED. Long-vol (VIXY) bleeds
#       ~-49%/yr — that bleed IS the premium. Yet naked short-vol (SVXY) captured only ~+1%/yr
#       of it: the tail reclaims all the carry. Convexity's law from the seller's side —
#       short-carry earns nothing net once the crisis arrives.
#   (b) THE TAIL CAP IS EVERYTHING. In Feb-2018 volmageddon the -1x SVXY lost ~91% in a WEEK;
#       it only survives now because it was RE-CAPPED to -0.5x. Defined-risk (put-write) barely
#       moved (-5%) and in 2020 even fell LESS than SPY. Defined risk = sleeve vs blowup.
#   (c) YOU CANNOT FIX A NAKED SHORT BY BOLTING ON A HEDGE. Adding a static VIXY hedge to
#       naked SVXY does not repair the tail (skew worsens); the fix is defined-risk BY
#       CONSTRUCTION (put-write / spreads), not a bought hedge.
#
# RESULTS AS TESTED (2016-2026):
#   VRP: VIXY -49%/yr (premium bled by buyers) vs SVXY +1%/yr (harvested — until it isn't)
#   tail: volmageddon SVXY -91% / PUTW -5% / QYLD -3% (SPY -6%); 2020 SVXY -55% / PUTW -28% (SPY -34%)
#   hedge: SVXY+0/10/20% VIXY -> maxDD -95/-89/-80%, skew -8.3/-11.3/-17.4 (does NOT fix it)
# Read-only.
# =============================================================================
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _brittle_common import CRISES, align, dist, win_ret

ds, P = align(["SVXY", "PUTW", "QYLD", "VIXY", "SPY"]); R = {s: P[s][1:] / P[s][:-1] - 1 for s in P}
print("=" * 80, "\nBRITTLE #2 — the vol risk premium, the tail, and why a hedge can't fix it\n" + "=" * 80)
print("(a) the vol risk premium (long-vol bleed = the premium):")
print(f"    VIXY (long-vol) {dist(R['VIXY'])['cagr']*100:+.0f}%/yr bled by BUYERS  vs  SVXY (short-vol) {dist(R['SVXY'])['cagr']*100:+.0f}%/yr harvested by SELLERS")
print("\n(b) the tail is the whole game (crisis-window returns):")
for nm, a, b in CRISES:
    print(f"    {nm:<22} SVXY {win_ret(ds,P,a,b,'SVXY')*100:>+5.0f}%  PUTW {win_ret(ds,P,a,b,'PUTW')*100:>+5.0f}%  QYLD {win_ret(ds,P,a,b,'QYLD')*100:>+5.0f}%  (SPY {win_ret(ds,P,a,b,'SPY')*100:+.0f}%)")
print("\n(c) a static hedge does NOT fix a naked short (defined-risk-by-construction does):")
for h in [0.0, 0.10, 0.20]:
    d = dist((1 - h) * R['SVXY'] + h * R['VIXY'])
    print(f"    SVXY + {int(h*100):>2}% VIXY: maxDD {d['dd']*100:.0f}%  skew {d['skew']:+.1f}  worstDay {d['worst']:+.0f}%  Sharpe {d['sh']:+.2f}")
print("\nVERDICT: the premium is real (VIXY bleeds -49%/yr) but the tail reclaims it — naked")
print("short-vol nets ~0 at -95% drawdown, and no bolted-on hedge repairs it. Brittle is only")
print("viable as DEFINED-RISK selling (put-write/spreads) with a hard tail cap, and even then")
print("it underperforms the index. Brittle's mirror is Bleed: it sells the tail Bleed buys.")
