
import os, asyncio, csv
from aiokafka import AIOKafkaProducer
from models import Tick

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:29092")
CSV_PATH = os.getenv("CSV_PATH", "sample_data/crypto_ticks.csv")
TOPIC = os.getenv("TOPIC", "ticks")

async def main():
    prod = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP, linger_ms=5, acks="1", value_serializer=lambda v: v.encode())
    await prod.start()
    try:
        print(f"[ingestor] streaming {CSV_PATH} -> kafka://{BOOTSTRAP}/{TOPIC}")
        with open(CSV_PATH) as f:
            rd = csv.DictReader(f)
            for i, row in enumerate(rd):
                tick = Tick(**row)
                key = f"{tick.symbol}:{tick.exchange}".encode()
                await prod.send_and_wait(TOPIC, key=key, value=tick.model_dump_json())
                await asyncio.sleep(0.01)
    finally:
        await prod.stop()

if __name__ == "__main__":
    asyncio.run(main())
