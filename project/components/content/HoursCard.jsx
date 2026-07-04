import React from 'react';
import { Badge } from '../core/Badge.jsx';
import { Card } from '../core/Card.jsx';

/** Seasonal office-hours card — splits Tax Season vs After Tax Season, each
 * with a day-range → hours table and an "appointment only" footnote. */
export function HoursCard({
  season = 'tax',
  ...props
}) {
  const data = season === 'tax'
    ? {
        label: 'Tax Season',
        range: 'January – April',
        rows: [
          ['Monday – Saturday', '9am – 7pm'],
          ['Sunday', '10am – 6pm'],
        ],
        footnote: 'After Hours — By Appointment Only',
      }
    : {
        label: 'After Tax Season',
        range: 'May – December',
        rows: [
          ['Monday – Friday', '10am – 6pm'],
          ['Saturday – Sunday', 'By Appointment Only'],
        ],
        footnote: 'After Hours — By Appointment Only',
      };

  return (
    <Card style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
        <h3 style={{ margin: 0, fontFamily: 'var(--font-heading)', fontWeight: 'var(--weight-bold)', fontSize: 'var(--text-lg)', color: 'var(--text-heading)' }}>
          {data.label}
        </h3>
        <Badge tone={season === 'tax' ? 'red' : 'outline'}>{data.range}</Badge>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-body)' }}>
        <tbody>
          {data.rows.map(([day, hours]) => (
            <tr key={day} style={{ borderTop: '1px solid var(--border-subtle)' }}>
              <td style={{ padding: '10px 0', color: 'var(--text-body)', fontSize: 'var(--text-sm)', fontWeight: 'var(--weight-medium)' }}>{day}</td>
              <td style={{ padding: '10px 0', color: 'var(--text-muted)', fontSize: 'var(--text-sm)', textAlign: 'right' }}>{hours}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p style={{ margin: 0, fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontStyle: 'italic' }}>{data.footnote}</p>
    </Card>
  );
}
