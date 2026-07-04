import React from 'react';

/** Small pill label — used for hours-status ("Open Today"), category tags,
 * and highlight flags ("Available Any Day and All Year!"). */
export function Badge({ children, tone = 'navy', style }) {
  const tones = {
    navy: { background: 'var(--color-navy)', color: 'var(--text-inverse)' },
    ice: { background: 'var(--surface-alt)', color: 'var(--color-navy)' },
    red: { background: 'var(--accent-cta)', color: 'var(--accent-cta-text)' },
    outline: { background: 'transparent', color: 'var(--color-royal-blue)', border: '1px solid var(--border-strong)' },
  };

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '5px 14px',
        borderRadius: 'var(--radius-pill)',
        fontFamily: 'var(--font-body)',
        fontWeight: 'var(--weight-semibold)',
        fontSize: 'var(--text-xs)',
        letterSpacing: 'var(--tracking-wide)',
        textTransform: 'uppercase',
        ...tones[tone],
        ...style,
      }}
    >
      {children}
    </span>
  );
}
