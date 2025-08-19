
from pydantic import BaseModel
from datetime import datetime

class Tick(BaseModel):
    ts: datetime
    symbol: str
    exchange: str
    bid: float
    ask: float
    mid: float
