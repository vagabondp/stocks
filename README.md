# TradeView Options Coach — Functional MVP

## **Goal**

A web app to:

1. Import stock/option trade history
2. Detect **Wheel** and **Strangle** strategies automatically
3. Suggest **next steps** based on detected strategy status

---

## **Core Features**

* **Auth**: Email login (NextAuth)
* **CSV Import**: Upload transactions (stock + options)
* **Strategy Detection**:

  * Wheel: CSP → Assignment → CC → Called away
  * Strangle: Short/Long strangle pairing by expiry
* **Next Step Suggestions**:

  * Wheel: Sell CSP, Sell CC, Roll, or Restart cycle
  * Strangle: Close at profit target, Roll on breach
* **Portfolio View**: Current holdings, avg. cost, P/L
* **Strategy Timeline**: Steps + Next Step chip

---

## **Tech Stack**

* **Frontend**: Next.js 14 + TailwindCSS + Recharts
* **Backend**: Next.js API routes + Prisma
* **DB**: PostgreSQL (Supabase or RDS)
* **Auth**: NextAuth (email magic link)
* **Testing**: Vitest + Playwright
* **Data Source**: CSV upload (MVP), API feed later

---

## **Data Model**

**Transactions**
`id, ts, instrumentType, action, ticker, qty, price, fee, right, strike, expiry, orderId, isOpening`

**OptionLegs**
`ticker, right, strike, expiry, side, qty, openTs, closeTs`

**StockPositions**
`ticker, shares, avgCost`

**StrategyInstance**
`type{wheel|strangle}, side, ticker, startTs, status, legs`

---

## **Strategy Detection Rules**

**Wheel**

1. Short Put sold
2. If assigned → start CC step (strike ≥ cost basis × 1.02 or call Δ 0.25–0.35)
3. If called away → restart CSP step
4. If expired worthless → sell next CSP

**Strangle**

* Pair same-expiry call + put, same side
* Short: close at 50% profit or roll on breach (Δ ≥ 0.40)
* Long: wait for move/IV expansion

---

## **Next Step Engine (Examples)**

* **Wheel after assignment** → Sell CC, 7–30 DTE, premium ≥ 1–2%/30d
* **Wheel after called away** → Sell CSP, 7–30 DTE, Δ 0.25–0.30
* **Short Strangle breach** → Roll threatened leg
* **Short Strangle profit** → Close both legs

---

## **UI Pages**

* `/login` — Email magic link
* `/dashboard` — Watchlist, portfolio, open strategies
* `/transactions` — CSV import + history
* `/strategies/[ticker]` — Timeline + next step card

---

## **Acceptance Criteria**

* Import CSV → see detected strategies
* Wheel/Strangle shown with correct badge + next step
* Portfolio shows correct holdings + P/L
* Dark mode toggle works
* No crashes, passes lint + tests in CI

