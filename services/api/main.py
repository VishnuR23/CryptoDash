
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os, json, asyncio, redis.asyncio as redis
from db import recent_signals

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

app = FastAPI(title="CryptoQuant API", version="0.1.0")

@app.get("/health")
async def health(): return {"status": "ok"}

@app.get("/signals/recent")
async def get_recent(limit: int = 50):
    return await recent_signals(limit)

@app.websocket("/ws/arbitrage")
async def ws_arbitrage(ws: WebSocket):
    await ws.accept()
    r = await redis.from_url(REDIS_URL)
    pubsub = r.pubsub()
    await pubsub.subscribe("arb_stream")
    try:
        snapshot = await recent_signals(20)
        await ws.send_text(json.dumps({"type":"snapshot","data":snapshot}))
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                await ws.send_text(json.dumps({"type":"update","data":json.loads(msg["data"].decode())}))
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe("arb_stream")
        await pubsub.close()
        await r.close()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!doctype html>
<html><head><meta charset="utf-8"><title>CryptoQuant Live</title></head>
<body>
<h2>CryptoQuant Arbitrage Stream</h2>
<pre id="out">Connecting...</pre>
<script>
const out = document.getElementById('out');
const ws = new WebSocket('ws://' + location.host + '/ws/arbitrage');
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  out.textContent = JSON.stringify(msg, null, 2) + "\n" + out.textContent.slice(0, 5000);
};
ws.onopen = () => out.textContent = "Connected. Waiting for events...\n";
ws.onclose = () => out.textContent = "Closed.";
</script>
</body></html>
"""
