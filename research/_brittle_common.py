#!/usr/bin/python3
# =============================================================================
# _brittle_common.py — shared helpers for the Blaque Baux Brittle (short-vol) sketches.
# Alpaca SIP daily bars; reads ALPACA_KEY_ID / ALPACA_SECRET_KEY from env. Read-only.
# NOTE: a true OTM-option-selling backtest needs historical chains Alpaca lacks; these use
# ETF proxies (SVXY short-vol, PUTW put-write, QYLD/XYLD covered-call, VIXY long-vol).
# =============================================================================
import os, json, urllib.request, math
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}

CRISES = [("Feb-2018 volmageddon", "2018-02-01", "2018-02-12"),
          ("2020 COVID crash", "2020-02-19", "2020-03-23")]

def closes(s):
    if s in _cache: return _cache[s]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    b = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40)).get("bars", {}).get(s, [])
    _cache[s] = {x["t"][:10]: x["c"] for x in b}
    return _cache[s]

def align(syms):
    D = {s: closes(s) for s in syms}; D = {s: v for s, v in D.items() if len(v) > 300}
    ds = sorted(set.intersection(*[set(v) for v in D.values()]))
    return ds, {s: np.array([D[s][d] for d in ds]) for s in D}

def dist(r):
    """The full distribution, because the Sharpe alone lies for short-vol."""
    r = np.asarray(r, float); r = r[np.isfinite(r)]; mu, sd = r.mean(), r.std(); cum = np.cumprod(1 + r)
    return dict(sh=mu / sd * math.sqrt(252), cagr=cum[-1] ** (252 / len(r)) - 1,
                dd=(cum / np.maximum.accumulate(cum) - 1).min(), skew=np.mean(((r - mu) / sd) ** 3),
                worst=r.min() * 100, cvar=np.mean(np.sort(r)[:max(1, int(0.05 * len(r)))]) * 100)

def win_ret(ds, P, a, b, s):
    ia = next(k for k, d in enumerate(ds) if d >= a); ib = max(k for k, d in enumerate(ds) if d <= b)
    return P[s][ib] / P[s][ia] - 1
