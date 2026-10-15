---
name: minerva
description: "Use Minerva for a paper-first markets desk: market data and execution across Kalshi, Polymarket, and Alpaca paper accounts, with hard guardrails, red-gated live orders, and keyless options-data backtest tooling. Live orders stay disabled unless the operator arms them per session."
license: MIT
compatibility: "Python 3. Public data lanes are keyless; authenticated lanes read venue keys from the environment."
metadata:
  version: 1.0.0
---
# Minerva — Markets Desk

A paper-first trading skill bundle: market data and execution across Kalshi, Polymarket, and Alpaca paper, plus keyless options-data tooling for rigorous backtests. Merged from a set of single-venue client notes (Kalshi, Polymarket, Alpaca paper data + execution, and a keyless options-chain backtest note).

**Standing fleet doctrine: paper-only. Live orders stay disabled until the user explicitly approves them — no exceptions, no workarounds.**

## Guardrails (hard, never auto-tuned)
| Guardrail | Value |
|---|---|
| Max premium per name | 5% of equity |
| DTE range | 30–60 days |
| Target delta | 0.20–0.35 |
| OTM range | 5%–12% |
| Risk type | Long premium only (buy puts); max loss = premium |
| Account mode | PAPER only |

Changing any guardrail is an operator-direct RED gate. Every paper order writes a receipt (account_id, action, max_loss_premium, rationale, guardrails, order_result).

## RED gates (never crossed without the user's direct in-thread seal)
1. Placing a real-money trade.
2. Selling naked / short premium.
3. Raising any hard cap.
4. Touching any account outside the designated paper program.

## Kalshi — bin/kalshi.py (CFTC-regulated US prediction exchange)
- Public lane (keyless): `kalshi.py markets KXBTCD` (daily BTC threshold binaries; also `KXETHD`), `kalshi.py market <ticker>`. Base: `https://api.elections.kalshi.com/trade-api/v2`.
- Authenticated lane: your PEM lives at `~/.kalshi/kalshi-private-key.pem` (mode 600). The script reads it from that file, or from `KALSHI_PRIVATE_KEY_B64` / `KALSHI_PRIVATE_KEY_PEM` env. `kalshi.py balance`, `kalshi.py positions`.
- Design note: Minerva is the strategist skill — a separate scanner/execution program consumes it. Minerva is not a second execution rail.
- `order <ticker> <yes|no> <count> <price_cents> --arm` — **RED-GATED**: refuses without BOTH `--arm` AND per-session `KALSHI_ARMED=ARM`.

## Polymarket — bin/poly.py (Polymarket US, polymarketexchange.com)
- Zero-setup public lane: `poly.py crypto --limit 20` (active crypto markets with implied probabilities), `poly.py market <condition_id>`, `poly.py book <token_id>`. Gamma: `https://gamma-api.polymarket.com` · CLOB: `https://clob.polymarket.com`.
- Note: if you use the authenticated lane, keep your API key at `~/.polymarket/` (mode 600). An account needs funding before any trading; funding is an operator decision.
- `order ... --arm` — **RED-GATED**: refuses without BOTH `--arm` AND per-session `POLY_ARMED=ARM`.

## Alpaca paper (data + execution)
- Paper-trading account only — no funding, no live keys, ever. This skill must never hold live keys; it refuses to run if `account.paper != true`.
- Auth: `APCA-API-KEY-ID` / `APCA-API-SECRET-KEY` headers (paper keys from app.alpaca.markets → Paper Trading).
- Data (free): latest IEX stock trade, daily bars, **options snapshots with greeks/IV** (indicative 15-min delayed) — `GET https://data.alpaca.markets/v1beta1/options/snapshots/{UNDERLYING}?feed=indicative&limit=1000`. ETF universe: SPY, QQQ, IWM, GLD/SLV, USO, TLT, HYG, FXE.
- Execution: `account_check.py` (read-only: paper mode, buying power, cash, equity, positions) and `submit_put.py` (BUY-to-open put with guardrail enforcement). Provision paper keys from the Alpaca dashboard (Paper Trading) and export them as env vars.
- Display law: raw option quotes stay INTERNAL (OPRA licensing) — publish only derived signals (VRP spreads, docket cards), never raw chains.

## Keyless backtest tooling (no credentials)
- **DoltHub options**: real EOD US-equity option chains via DoltHub's keyless HTTP SQL API (date, act_symbol, expiration, strike, call_put, bid, ask, IV, greeks). Coverage ~Feb 2019 → live. ALWAYS constrain by `date` (indexed leading column) — full-table scans hit context-deadline by design.
- **macro_data.py**: FRED (DGS10, VIXCLS, T10Y2Y — keyless CSV) + EDGAR XBRL (needs descriptive User-Agent).
- **real_chain_backtest.py**: rigorous put backtest on REAL chains (entry at actual ASK, exit at actual BID).
- Door-verify every data source before trusting it: a recon agent's claimed "philippdubach/options-data" repo was a hallucination (404s).

## Credential inventory (names only)
`KALSHI_KEY_ID`/`KALSHI_PRIVATE_KEY_PEM` (your file: `~/.kalshi/`); `POLY_PRIVATE_KEY` (your file: `~/.polymarket/`); `ALPACA_KEY_ID`/`ALPACA_SECRET` (paper keys, env). DoltHub/FRED/SEC EDGAR lanes are keyless.
