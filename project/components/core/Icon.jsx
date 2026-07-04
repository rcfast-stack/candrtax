import React from 'react';

/**
 * Icon renders a Lucide icon by name. Requires the consuming page to load
 * the Lucide CDN script (see prompt.md) — this design system has no native
 * icon set, so Lucide (stroke-based, 2px, matches the brand's clean-line feel)
 * is used as a documented CDN substitution.
 */
export function Icon({ name, size = 20, color = 'currentColor', strokeWidth = 2, style }) {
  const ref = React.useRef(null);

  React.useEffect(() => {
    const lucide = window.lucide;
    if (lucide && ref.current) {
      ref.current.innerHTML = '';
      const el = document.createElement('i');
      el.setAttribute('data-lucide', name);
      ref.current.appendChild(el);
      lucide.createIcons({
        icons: lucide.icons,
        nameAttr: 'data-lucide',
        attrs: { width: size, height: size, stroke: color, 'stroke-width': strokeWidth },
      });
    }
  }, [name, size, color, strokeWidth]);

  return (
    <span
      ref={ref}
      aria-hidden="true"
      style={{ display: 'inline-flex', width: size, height: size, flexShrink: 0, ...style }}
    />
  );
}
