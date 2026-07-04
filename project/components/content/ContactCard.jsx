import React from 'react';
import { Icon } from '../core/Icon.jsx';
import { Card } from '../core/Card.jsx';

/** Contact-details card — address, phone, email, website, each with an
 * icon + link where relevant. Used on the home page and a dedicated
 * contact section. */
export function ContactCard({
  address = '1320 N. Van Ness Ave, Fresno CA 93702',
  areaNote = 'Near Tower District',
  phone = '(559) 962-7503',
  email = 'info@candrtaxservices.com',
  website = 'www.candrtaxservices.com',
}) {
  const rows = [
    { icon: 'map-pin', label: address, sub: areaNote },
    { icon: 'phone', label: phone, href: `tel:${phone.replace(/[^\d]/g, '')}` },
    { icon: 'mail', label: email, href: `mailto:${email}` },
    { icon: 'globe', label: website, href: `https://${website.replace(/^https?:\/\//, '')}` },
  ];

  return (
    <Card style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
      {rows.map((r) => (
        <div key={r.label} style={{ display: 'flex', alignItems: 'flex-start', gap: '14px' }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 'var(--radius-md)',
              background: 'var(--surface-alt)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <Icon name={r.icon} size={18} color="var(--icon-primary)" />
          </div>
          <div>
            {r.href ? (
              <a
                href={r.href}
                style={{ color: 'var(--text-link)', fontWeight: 'var(--weight-semibold)', textDecoration: 'none', fontSize: 'var(--text-base)' }}
              >
                {r.label}
              </a>
            ) : (
              <div style={{ color: 'var(--text-body)', fontWeight: 'var(--weight-semibold)', fontSize: 'var(--text-base)' }}>{r.label}</div>
            )}
            {r.sub && <div style={{ color: 'var(--text-muted)', fontSize: 'var(--text-sm)' }}>{r.sub}</div>}
          </div>
        </div>
      ))}
    </Card>
  );
}
