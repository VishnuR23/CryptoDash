
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/cryptoquant")
engine = create_async_engine(DATABASE_URL, future=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def insert_tick(session: AsyncSession, t):
    await session.execute(text("""
        INSERT INTO ticks (ts, symbol, exchange, bid, ask, mid)
        VALUES (:ts, :symbol, :exchange, :bid, :ask, :mid)
    """), dict(ts=t.ts, symbol=t.symbol, exchange=t.exchange, bid=t.bid, ask=t.ask, mid=t.mid))

async def insert_signal(session: AsyncSession, s):
    await session.execute(text("""
        INSERT INTO arbitrage_signals (ts, symbol, buy_exchange, buy_price, sell_exchange, sell_price, spread_bps)
        VALUES (:ts, :symbol, :buy_exchange, :buy_price, :sell_exchange, :sell_price, :spread_bps)
    """), dict(ts=s.ts, symbol=s.symbol, buy_exchange=s.buy_exchange, buy_price=s.buy_price,
                 sell_exchange=s.sell_exchange, sell_price=s.sell_price, spread_bps=s.spread_bps))
