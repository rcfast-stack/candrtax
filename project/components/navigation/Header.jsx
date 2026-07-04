import React from 'react';
import { Button } from '../core/Button.jsx';

/** Site header — logo, primary nav, and a phone CTA. Sticky, navy-on-white
 * with a thin bottom border; collapses nav into a plain stack under 720px
 * (no hamburger drawer — the nav is short enough to wrap). */
export function Header({ logoSrc, navItems = [], phone = '(559) 962-7503', active }) {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 'var(--space-6)',
        padding: '16px var(--space-8)',
        background: 'var(--surface-card)',
        borderBottom: '1px solid var(--border-subtle)',
        fontFamily: 'var(--font-body)',
        flexWrap: 'wrap',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {logoSrc && <img src={logoSrc} alt="C&R Tax Services" style={{ height: 40 }} />}
      </div>

      <nav style={{ display: 'flex', gap: 'var(--space-6)', flexWrap: 'wrap' }}>
        {navItems.map((item) => (
          <a
            key={item.label}
            href={item.href}
            style={{
              textDecoration: 'none',
              color: item.label === active ? 'var(--color-navy)' : 'var(--text-muted)',
              fontWeight: item.label === active ? 'var(--weight-semibold)' : 'var(--weight-medium)',
              fontSize: 'var(--text-sm)',
              borderBottom: item.label === active ? '2px solid var(--accent-cta)' : '2px solid transparent',
              paddingBottom: 4,
            }}
          >
            {item.label}
          </a>
        ))}
      </nav>

      <Button as="a" href={`tel:${phone.replace(/[^\d]/g, '')}`} variant="primary" size="sm">
        Call {phone}
      </Button>
    </header>
  );
}
