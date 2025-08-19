
from pydantic import BaseModel
from datetime import datetime

class Tick(BaseModel):
    ts: datetime
    symbol: str
    exchange: str
    bid: float | None = None
    ask: float | None = None
    mid: float | None = None

class ArbSignal(BaseModel):
    ts: datetime
    symbol: str
    buy_exchange: str
    buy_price: float
    sell_exchange: str
    sell_price: float
    spread_bps: float
