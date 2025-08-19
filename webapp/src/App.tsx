
import React, { useEffect, useMemo, useRef, useState } from 'react'
import { ArbChart } from './components/ArbChart'
import { SignalTable } from './components/SignalTable'

type ArbSignal = {
  ts: string
  symbol: string
  buy_exchange: string
  buy_price: number
  sell_exchange: string
  sell_price: number
  spread_bps: number
}
type WsMessage =
  | { type: 'snapshot', data: ArbSignal[] }
  | { type: 'update', data: ArbSignal }

const wsUrl = () => {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  const host = location.hostname
  const port = 8000
  return `${proto}://${host}:${port}/ws/arbitrage`
}

export default function App() {
  const [signals, setSignals] = useState<ArbSignal[]>([])
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(wsUrl())
    wsRef.current = ws
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (ev) => {
      const msg: WsMessage = JSON.parse(ev.data)
      if (msg.type === 'snapshot') {
        const merged = [...msg.data].sort((a,b) => +new Date(a.ts) - +new Date(b.ts))
        setSignals(merged.slice(-300))
      } else if (msg.type === 'update') {
        setSignals(prev => {
          const next = [...prev, msg.data].sort((a,b) => +new Date(a.ts) - +new Date(b.ts))
          return next.slice(-500)
        })
      }
    }
    return () => { ws.close() }
  }, [])

  const chartData = useMemo(() => {
    return signals.map(s => ({ t: new Date(s.ts), spread_bps: s.spread_bps, symbol: s.symbol }))
  }, [signals])

  return (
    <div className="container">
      <header className="header">
        <h1>CryptoQuant</h1>
        <div className={connected ? 'badge online' : 'badge offline'}>{connected ? 'LIVE' : 'OFFLINE'}</div>
      </header>

      <section className="grid">
        <div className="card">
          <h2>Arbitrage Spread (bps)</h2>
          <ArbChart data={chartData} />
        </div>
        <div className="card">
          <h2>Recent Signals</h2>
          <SignalTable rows={[...signals].reverse().slice(0, 50)} />
        </div>
      </section>

      <footer className="footer">
        <span>API: <code>http://localhost:8000</code> • WS: <code>{wsUrl()}</code></span>
      </footer>
    </div>
  )
}
