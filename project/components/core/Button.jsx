import React from 'react';

/** Primary UI action button. Growth red is reserved for CTAs only — the
 * "primary" variant uses it; "secondary" and "ghost" stay in the navy/blue
 * family per the brand's accent-restraint rule. */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  as = 'button',
  href,
  onClick,
  disabled = false,
  style,
  ...rest
}) {
  const sizes = {
    sm: { padding: '8px 16px', fontSize: 'var(--text-sm)' },
    md: { padding: '12px 22px', fontSize: 'var(--text-base)' },
    lg: { padding: '16px 30px', fontSize: 'var(--text-lg)' },
  };

  const variants = {
    primary: {
      background: 'var(--accent-cta)',
      color: 'var(--accent-cta-text)',
      border: '1px solid var(--accent-cta)',
    },
    secondary: {
      background: 'var(--color-navy)',
      color: 'var(--text-inverse)',
      border: '1px solid var(--color-navy)',
    },
    outline: {
      background: 'transparent',
      color: 'var(--color-navy)',
      border: '1px solid var(--color-navy)',
    },
    ghost: {
      background: 'transparent',
      color: 'var(--text-link)',
      border: '1px solid transparent',
    },
  };

  const hover = {
    primary: { background: 'var(--accent-cta-hover)', borderColor: 'var(--accent-cta-hover)' },
    secondary: { background: 'var(--color-midnight)', borderColor: 'var(--color-midnight)' },
    outline: { background: 'var(--surface-alt)' },
    ghost: { color: 'var(--text-link-hover)' },
  };

  const base = {
    fontFamily: 'var(--font-body)',
    fontWeight: 'var(--weight-semibold)',
    borderRadius: 'var(--radius-pill)',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    lineHeight: 1,
    textDecoration: 'none',
    transition: 'background 0.15s ease, border-color 0.15s ease, transform 0.05s ease',
    ...sizes[size],
    ...variants[variant],
    ...style,
  };

  const [isHover, setHover] = React.useState(false);
  const [isActive, setActive] = React.useState(false);

  const computed = {
    ...base,
    ...(isHover && !disabled ? hover[variant] : {}),
    transform: isActive && !disabled ? 'scale(0.97)' : 'scale(1)',
  };

  const handlers = {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => { setHover(false); setActive(false); },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
  };

  if (as === 'a' || href) {
    return (
      <a href={href} style={computed} onClick={onClick} {...handlers} {...rest}>
        {children}
      </a>
    );
  }

  return (
    <button type="button" style={computed} onClick={onClick} disabled={disabled} {...handlers} {...rest}>
      {children}
    </button>
  );
}
