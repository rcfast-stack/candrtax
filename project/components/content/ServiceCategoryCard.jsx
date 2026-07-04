import React from 'react';
import { Icon } from '../core/Icon.jsx';
import { Card } from '../core/Card.jsx';

/** A single service category card — icon, title, and a checklist of
 * sub-services. Used to build the three C&R service groups (Income Tax,
 * Notary & Loan Signing, Livescan Fingerprints). */
export function ServiceCategoryCard({ icon = 'briefcase', title, note, items = [] }) {
  return (
    <Card style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)', height: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: 'var(--radius-md)',
            background: 'var(--surface-alt)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          <Icon name={icon} size={22} color="var(--icon-primary)" />
        </div>
        <h3
          style={{
            margin: 0,
            fontFamily: 'var(--font-heading)',
            fontWeight: 'var(--weight-bold)',
            fontSize: 'var(--text-lg)',
            color: 'var(--text-heading)',
          }}
        >
          {title}
        </h3>
      </div>

      <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {items.map((it) => (
          <li
            key={it}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px',
              fontFamily: 'var(--font-body)',
              fontSize: 'var(--text-sm)',
              color: 'var(--text-body)',
              lineHeight: 'var(--leading-snug)',
            }}
          >
            <Icon name="check" size={16} color="var(--color-royal-blue)" style={{ marginTop: 2 }} />
            <span>{it}</span>
          </li>
        ))}
      </ul>

      {note && (
        <p style={{ margin: 0, fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontStyle: 'italic' }}>
          {note}
        </p>
      )}
    </Card>
  );
}
