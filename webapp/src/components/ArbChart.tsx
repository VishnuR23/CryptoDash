
import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
type Datum = { t: Date, spread_bps: number }
export function ArbChart({ data }: { data: Datum[] }) {
  const formatted = data.map(d => ({ ...d, tStr: d.t.toLocaleTimeString() }))
  return (
    <div style={{ width: '100%', height: 320 }}>
      <ResponsiveContainer>
        <LineChart data={formatted} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tStr" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip formatter={(v: any) => [v, 'bps']} />
          <Line type="monotone" dataKey="spread_bps" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
