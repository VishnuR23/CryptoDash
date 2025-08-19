
import os, asyncio, json
from collections import defaultdict
from aiokafka import AIOKafkaConsumer
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from models import Tick, ArbSignal
from db import SessionLocal, insert_tick, insert_signal

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:29092")
TOPIC = os.getenv("TOPIC", "ticks")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

best_bid = defaultdict(lambda: defaultdict(lambda: None))
best_ask = defaultdict(lambda: defaultdict(lambda: None))

async def publish_signal(r: redis.Redis, sig: ArbSignal):
    await r.publish("arb_stream", sig.model_dump_json())

def check_arbitrage(symbol: str):
    bids = {ex: px for ex, px in best_bid[symbol].items() if px is not None}
    asks = {ex: px for ex, px in best_ask[symbol].items() if px is not None}
    if not bids or not asks: return None
    sell_ex, sell_px = max(bids.items(), key=lambda kv: kv[1])
    buy_ex, buy_px = min(asks.items(), key=lambda kv: kv[1])
    if buy_ex == sell_ex: return None
    spread_bps = (sell_px - buy_px) / buy_px * 1e4
    if spread_bps > 5.0:
        return buy_ex, buy_px, sell_ex, sell_px, spread_bps
    return None

async def consume_loop():
    consumer = AIOKafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP, enable_auto_commit=True,
                                value_deserializer=lambda v: json.loads(v.decode()))
    await consumer.start()
    r = await redis.from_url(REDIS_URL)
    try:
        async with SessionLocal() as session:
            async for msg in consumer:
                t = Tick(**msg.value)
                if t.bid is not None: best_bid[t.symbol][t.exchange] = t.bid
                if t.ask is not None: best_ask[t.symbol][t.exchange] = t.ask
                await insert_tick(session, t)
                sig = check_arbitrage(t.symbol)
                if sig:
                    buy_ex, buy_px, sell_ex, sell_px, bps = sig
                    s = ArbSignal(ts=t.ts, symbol=t.symbol, buy_exchange=buy_ex, buy_price=buy_px,
                                  sell_exchange=sell_ex, sell_price=sell_px, spread_bps=bps)
                    await insert_signal(session, s)
                    await publish_signal(r, s)
                await session.commit()
    finally:
        await consumer.stop()
        await r.close()

if __name__ == "__main__":
    asyncio.run(consume_loop())
