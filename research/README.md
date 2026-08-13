# Blaque Baux Brittle — research

First-pass Path-A research on the short-volatility / premium-selling sleeve — the SELL side of
convexity, and the mirror of [Bleed](https://github.com/blaquebaux/bleed).
**Data caveat:** a true OTM-option-selling backtest needs historical option chains Alpaca
lacks; this pass uses ETF proxies (SVXY short-vol, PUTW put-write, QYLD/XYLD covered-call,
VIXY long-vol). All sketches read Alpaca SIP daily bars, are read-only, print their results.

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
python research/brittle_1_premium_illusion.py   # the Sharpe lies
python research/brittle_2_tail_and_hedge.py      # the tail is the whole game
```

## Scorecard

| proxy | Sharpe | CAGR | maxDD | skew | worst day | Verdict |
|---|---|---|---|---|---|---|
| SVXY (naked short-vol) | +0.42 | **+1%** | **−95%** | **−8.3** | −83% | ❌ Sharpe illusion / ruin |
| PUTW (put-write) | +0.57 | +7% | −28% | −1.8 | −11% | 🟡 survivable, underperforms SPY |
| QYLD/XYLD (covered-call) | +0.58 | +8% | −25% | −1.1 | −10% | 🟡 same |
| **SPY (reference)** | **+0.82** | **+14%** | −34% | −0.7 | −11% | — |

## The synthesis — the premium is real but the tail reclaims it

- **The Sharpe lies.** Naked short-vol (SVXY) posts a respectable Sharpe (+0.42) but made **~+1%
  CAGR over a decade** while risking a **−95% drawdown**, skew −8.3, worst day −83%. The Sharpe
  is an illusion — a single vol spike undoes years. Picking up pennies in front of a steamroller.

- **The vol risk premium is real but un-harvestable naked.** Long-vol (VIXY) bleeds **−49%/yr** —
  that bleed *is* the premium — yet naked short-vol captured only **+1%/yr** of it. The tail
  reclaims all the carry, exactly as the base's convexity law predicts from the seller's side:
  short-carry earns nothing net once the crisis arrives.

- **The tail cap is the whole game.** In the Feb-2018 volmageddon the −1× SVXY lost **~91% in a
  week**; it survives today only because it was re-capped to −0.5×. Defined-risk selling
  (put-write) barely moved (−5%), and in 2020 even fell *less* than SPY (−28% vs −34%). Defined
  risk is the difference between a sleeve and a blow-up.

- **You cannot fix a naked short by bolting on a hedge.** A static VIXY hedge on naked SVXY does
  not repair the tail (skew *worsens* to −17). The fix is defined-risk **by construction**
  (put-write / spreads), not a bought hedge.

**Verdict.** Reject naked short-vol outright — it is a Sharpe-illusion trap. Defined-risk
premium selling (put-write / covered-call) is the only survivable form, but it **underperforms
simply holding SPY** (+0.6 vs +0.82 Sharpe, +7–8% vs +14% CAGR): a capped-upside/kept-downside
risk profile, an *income* wrapper, not an edge. Brittle's honest contribution is the
quantification — the VRP exists (VIXY −49%/yr) but is a trap to harvest — and the mirror it
completes: **Brittle sells the tail that Bleed buys.** Both, held statically, lose to the tail;
the balanced book pairs a *defined-risk* seller with Bleed's cheap regime-spanning insurance.

## Files
- `_brittle_common.py` — shared helpers (distribution incl. skew/CVaR) + crisis windows.
- `brittle_1_premium_illusion.py` — the harvest table: Sharpe vs the true distribution.
- `brittle_2_tail_and_hedge.py` — the VRP, the tail, and why a bolted-on hedge can't fix it.
