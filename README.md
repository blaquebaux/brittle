# Blaque Baux Brittle

**Harvest what's about to expire worthless. Near-expiry, far-out-of-the-money options and leveraged/expiring products with little chance of finishing in-the-money — sell the lottery ticket, or buy it for pennies.**

Brittle is a member of the Blaque Baux family. The [core repo](https://github.com/Carter-Warrens/blaquebaux)
is the **engine and blueprint**. Brittle points that engine at instruments in their last
days of life — deep-OTM short-dated options, expiring leveraged/decay products — to harvest
the premium of things overwhelmingly likely to expire worthless (and, selectively, to buy
convex tickets for pennies when they're cheap). It inherits the engine's governance
wholesale, which here is not optional garnish but the entire risk.

> **Not investment advice.** Educational/research software. Systematically selling OTM
> premium is picking up pennies in front of a steamroller — a single tail can erase years
> of gains. Nothing here is validated. Defined-risk structures and hard caps are mandatory.
> See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/Carter-Warrens/blaquebaux-brittle.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

This is a **short-gamma / short-vol theta harvest**: high win-rate and smooth returns in
calm regimes, ruinous in tails. The base convexity research names the danger precisely —
short-carry/long-decay strategies bleed the seller nothing in calm and everything in a
sharp crisis, and the payoff is un-timeable. So Brittle's design is governance-first:
**defined-risk spreads, not naked shorts**, hard per-name and gross caps, and a tail budget.
It is the deliberate mirror of **Bleed** — Brittle sells the tail Bleed buys — which makes
the two a natural internal hedge pair.

## Research plan (Path A — not yet built)

- **Defined-risk OTM premium selling** — short-dated far-OTM credit spreads; measure the
  full return distribution (skew, tail CVaR), never Sharpe alone.
- **Expiring-product decay** — leveraged/inverse and dated products near expiry where decay
  is structural.
- **Cheap-ticket buying** — the selective long side: convex tickets when premium is
  mispriced low (a bridge to Bleed).
- **Tail budgeting & caps** — size so the worst plausible gap is survivable by construction.

Data caveat: options coverage depends on the venue's options API; the tradeable, liquid
subset is the real universe.

## Research — first pass done

Full detail in [`research/README.md`](research/README.md). The scorecard:

| proxy | Sharpe | CAGR | maxDD | skew | Verdict |
|---|---|---|---|---|---|
| SVXY (naked short-vol) | +0.42 | **+1%** | **−95%** | **−8.3** | ❌ Sharpe illusion / ruin |
| PUTW / QYLD (defined-risk) | ~+0.58 | +7–8% | −25/−28% | −1 to −2 | 🟡 survivable, underperforms SPY |
| SPY (reference) | +0.82 | +14% | −34% | −0.7 | — |

**The synthesis:** the short-vol premium is real (long-vol VIXY bleeds **−49%/yr**) but a trap
to harvest — naked short-vol (SVXY) captured only ~+1%/yr of it, at a −95% drawdown and −8.3
skew, because **the tail reclaims all the carry** (the base's convexity law, seller's side). The
Sharpe is an illusion: SVXY lost ~91% in a *week* in the 2018 volmageddon and survives now only
because it was re-capped to −0.5×. Defined-risk selling (put-write/covered-call) is the only
survivable form — but it **underperforms simply holding SPY**. A static hedge can't repair a
naked short (skew worsens); the fix is defined-risk *by construction*. **Brittle sells the tail
that Bleed buys** — both lose to the tail held statically; the balanced book pairs a defined-risk
seller with Bleed's cheap insurance.

## Status
**Research: first pass complete — naked short-vol rejected; defined-risk selling survives but
has no edge over the index** (`research/`). The VRP is real but a trap to harvest. No live
driver. Nothing validated to the spine's bar.

## About Blaque Baux

**Blaque Baux** is a quantitative research initiative and a subsidiary of **[Carter Warrens](https://carterwarrens.com)**.
[**BlaqueBaux.com**](https://blaquebaux.com) is the home for the work; the code lives here on GitHub — open to
study, test, and build bespoke strategies on top of.

Anyone can point an AI at a market. The edge is **understanding what the data actually says — and turning it
into something you can act on.** We test relentlessly and put most of it *on the record as rejected, with the
reason*; what survives is built, governed, and validated before it is ever called real. That combination —
honest research, reproducible evidence, and execution you can trust — is why Carter Warrens leads on
**strategy and implementation**, not merely uses the tools everyone now has.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/Carter-Warrens/blaquebaux) is the
base/blueprint and holds the [full family roster](https://github.com/Carter-Warrens/blaquebaux#the-blaque-baux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule → Carter-Warrens/blaquebaux)
research/   two Path-A sketches (premium illusion, tail and hedge) + scorecard
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). © 2026 Carter Warrens.
