
import React from 'react'
type Row = {
  ts: string
  symbol: string
  buy_exchange: string
  buy_price: number
  sell_exchange: string
  sell_price: number
  spread_bps: number
}
export function SignalTable({ rows }: { rows: Row[] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Symbol</th>
            <th>Buy @</th>
            <th>Sell @</th>
            <th>Spread (bps)</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>{new Date(r.ts).toLocaleTimeString()}</td>
              <td>{r.symbol}</td>
              <td>{r.buy_exchange} <span className="muted">@ {r.buy_price.toFixed(2)}</span></td>
              <td>{r.sell_exchange} <span className="muted">@ {r.sell_price.toFixed(2)}</span></td>
              <td className={r.spread_bps > 10 ? 'gain' : ''}>{r.spread_bps.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
