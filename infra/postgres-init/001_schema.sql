
CREATE TABLE IF NOT EXISTS ticks (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  exchange TEXT NOT NULL,
  bid DOUBLE PRECISION,
  ask DOUBLE PRECISION,
  mid DOUBLE PRECISION
);
CREATE INDEX IF NOT EXISTS idx_ticks_symbol_ts ON ticks(symbol, ts);

CREATE TABLE IF NOT EXISTS arbitrage_signals (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  buy_exchange TEXT NOT NULL,
  buy_price DOUBLE PRECISION NOT NULL,
  sell_exchange TEXT NOT NULL,
  sell_price DOUBLE PRECISION NOT NULL,
  spread_bps DOUBLE PRECISION NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_arb_symbol_ts ON arbitrage_signals(symbol, ts);
