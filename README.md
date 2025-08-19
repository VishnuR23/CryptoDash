
# CryptoQuant — Real-Time Crypto & Market Data Analytics Engine

**CryptoQuant** ingests live (or replayed) crypto ticks, detects **arbitrage opportunities** across exchanges, computes rolling metrics, and exposes **REST + WebSocket** APIs. It's a portfolio-ready project tailored for **crypto + fintech + market-data** companies.

## Highlights
- 🧩 **Services:** `ingestor` (streams ticks) → `analyzer` (detects arbitrage, aggregates metrics) → `api` (FastAPI REST + WebSocket).
- 🗃️ **Infra:** Kafka (streams), Postgres (storage), Redis (cache/pubsub), Docker Compose (one command to run).
- ⚙️ **Clean design:** typed Python, modular packages, optional C++ core (for algorithms) included in `cpp-core/`.
- 🧪 **Replay mode:** ships with synthetic tick data so you can demo offline.

## Architecture
```
[ Ingestor ] --ticks--> [ Kafka ] --ticks--> [ Analyzer ] --writes--> [ Postgres ]
      |                                                       |--pub--> [ Redis ]
      |                                                                   |
      +-------------------------------------------------------> [ API ] <-+
                                                     REST / WebSocket clients
```

## Quickstart
```bash
# start everything
docker compose up -d --build

# API docs
open http://localhost:8000/docs

# Dashboard
open http://localhost:5173
```

### Local dev without Docker
```bash
# infra
docker compose up -d kafka zookeeper postgres redis

# analyzer
python -m venv .venv && source .venv/bin/activate
pip install -r services/analyzer/requirements.txt
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cryptoquant REDIS_URL=redis://localhost:6379 KAFKA_BOOTSTRAP=localhost:29092 python services/analyzer/app.py

# ingestor (replay sample data)
pip install -r services/ingestor/requirements.txt
KAFKA_BOOTSTRAP=localhost:29092 python services/ingestor/app.py

# api
pip install -r services/api/requirements.txt
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cryptoquant REDIS_URL=redis://localhost:6379 uvicorn services.api.main:app --reload --port 8000

# dashboard
cd webapp && npm install && npm run dev
```

## Web Dashboard (React + Vite)
- Live Recharts line chart of arbitrage spread (bps)
- Real-time table of recent signals via WebSocket

### Run Dashboard
```bash
docker compose up -d --build dashboard
open http://localhost:5173
```
The dashboard connects to the API at `http://localhost:8000` and `ws://localhost:8000/ws/arbitrage`.

## Talking Points (for interviews)
- **Streaming pipelines** (Kafka), **stateful analytics** (arbitrage, rolling metrics), **low-latency push** (WebSocket), and **operational infra** (Docker Compose).
- Clean module boundaries (ingest vs. analyze vs. serve), typed Python, and optional **C++ algorithms** as a performance path.
- Can extend with ML (anomaly detection), portfolio analytics, or L2/DEX data.

> Educational demo. Do not use for live trading decisions.
