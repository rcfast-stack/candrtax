import React from 'react';
import { Icon } from '../core/Icon.jsx';

/** Site footer — navy background, contact recap, office hours summary,
 * copyright. Mirrors the header's role as the brand-color bookend. */
export function Footer({
  address = '1320 N. Van Ness Ave, Fresno CA 93702',
  phone = '(559) 962-7503',
  email = 'info@candrtaxservices.com',
  website = 'www.candrtaxservices.com',
}) {
  const row = { display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--text-inverse)', fontSize: 'var(--text-sm)' };
  return (
    <footer
      style={{
        background: 'var(--color-navy)',
        color: 'var(--text-inverse)',
        padding: 'var(--space-16) var(--space-8)',
        fontFamily: 'var(--font-body)',
      }}
    >
      <div
        style={{
          maxWidth: 'var(--container-max)',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: 'var(--space-10)',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 'var(--weight-bold)', fontSize: 'var(--text-lg)' }}>
            C&amp;R Tax Services
          </div>
          <div style={row}><Icon name="map-pin" size={16} color="var(--icon-on-dark)" />{address}</div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div style={row}><Icon name="phone" size={16} color="var(--icon-on-dark)" />{phone}</div>
          <div style={row}><Icon name="mail" size={16} color="var(--icon-on-dark)" />{email}</div>
          <div style={row}><Icon name="globe" size={16} color="var(--icon-on-dark)" />{website}</div>
        </div>
      </div>

      <div
        style={{
          maxWidth: 'var(--container-max)',
          margin: 'var(--space-10) auto 0',
          paddingTop: 'var(--space-6)',
          borderTop: '1px solid rgba(247,248,250,0.15)',
          fontSize: 'var(--text-xs)',
          color: 'var(--color-ice-blue)',
          opacity: 0.7,
        }}
      >
        © {new Date().getFullYear()} C&amp;R Tax Services. All rights reserved.
      </div>
    </footer>
  );
}
