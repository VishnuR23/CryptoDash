
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/cryptoquant")
engine = create_async_engine(DATABASE_URL, future=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def recent_signals(limit: int = 50):
    async with SessionLocal() as session:
        rows = (await session.execute(text("""
            SELECT ts, symbol, buy_exchange, buy_price, sell_exchange, sell_price, spread_bps
            FROM arbitrage_signals ORDER BY ts DESC LIMIT :lim
        """))).params(lim=limit).fetchall()
        return [dict(r._mapping) for r in rows]
