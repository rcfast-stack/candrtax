import React from 'react';

/** Generic elevated surface container — the base for service cards, contact
 * cards, and hours cards throughout the site. */
export function Card({ children, padding = 'var(--space-8)', style }) {
  return (
    <div
      style={{
        background: 'var(--surface-card)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        padding,
        ...style,
      }}
    >
      {children}
    </div>
  );
}
