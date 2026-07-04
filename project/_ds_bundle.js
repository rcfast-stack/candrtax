/* @ds-bundle: {"format":4,"namespace":"CRTaxServicesDesignSystem_70ca00","components":[{"name":"ContactCard","sourcePath":"components/content/ContactCard.jsx"},{"name":"HoursCard","sourcePath":"components/content/HoursCard.jsx"},{"name":"ServiceCategoryCard","sourcePath":"components/content/ServiceCategoryCard.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Icon","sourcePath":"components/core/Icon.jsx"},{"name":"Footer","sourcePath":"components/navigation/Footer.jsx"},{"name":"Header","sourcePath":"components/navigation/Header.jsx"}],"sourceHashes":{"components/content/ContactCard.jsx":"2e020dd92830","components/content/HoursCard.jsx":"0a7a65d0e318","components/content/ServiceCategoryCard.jsx":"1947c5e702a7","components/core/Badge.jsx":"f05cf9bf177d","components/core/Button.jsx":"af450e959d5b","components/core/Card.jsx":"fd5b4040d824","components/core/Icon.jsx":"1f91bfcc2d98","components/navigation/Footer.jsx":"362f3644f8d3","components/navigation/Header.jsx":"fa8cb9d7693d","ui_kits/website/HomePage.jsx":"4ed133165761"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.CRTaxServicesDesignSystem_70ca00 = window.CRTaxServicesDesignSystem_70ca00 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
/** Small pill label — used for hours-status ("Open Today"), category tags,
 * and highlight flags ("Available Any Day and All Year!"). */
function Badge({
  children,
  tone = 'navy',
  style
}) {
  const tones = {
    navy: {
      background: 'var(--color-navy)',
      color: 'var(--text-inverse)'
    },
    ice: {
      background: 'var(--surface-alt)',
      color: 'var(--color-navy)'
    },
    red: {
      background: 'var(--accent-cta)',
      color: 'var(--accent-cta-text)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--color-royal-blue)',
      border: '1px solid var(--border-strong)'
    }
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
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
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Primary UI action button. Growth red is reserved for CTAs only — the
 * "primary" variant uses it; "secondary" and "ghost" stay in the navy/blue
 * family per the brand's accent-restraint rule. */
function Button({
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
    sm: {
      padding: '8px 16px',
      fontSize: 'var(--text-sm)'
    },
    md: {
      padding: '12px 22px',
      fontSize: 'var(--text-base)'
    },
    lg: {
      padding: '16px 30px',
      fontSize: 'var(--text-lg)'
    }
  };
  const variants = {
    primary: {
      background: 'var(--accent-cta)',
      color: 'var(--accent-cta-text)',
      border: '1px solid var(--accent-cta)'
    },
    secondary: {
      background: 'var(--color-navy)',
      color: 'var(--text-inverse)',
      border: '1px solid var(--color-navy)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--color-navy)',
      border: '1px solid var(--color-navy)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--text-link)',
      border: '1px solid transparent'
    }
  };
  const hover = {
    primary: {
      background: 'var(--accent-cta-hover)',
      borderColor: 'var(--accent-cta-hover)'
    },
    secondary: {
      background: 'var(--color-midnight)',
      borderColor: 'var(--color-midnight)'
    },
    outline: {
      background: 'var(--surface-alt)'
    },
    ghost: {
      color: 'var(--text-link-hover)'
    }
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
    ...style
  };
  const [isHover, setHover] = React.useState(false);
  const [isActive, setActive] = React.useState(false);
  const computed = {
    ...base,
    ...(isHover && !disabled ? hover[variant] : {}),
    transform: isActive && !disabled ? 'scale(0.97)' : 'scale(1)'
  };
  const handlers = {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false)
  };
  if (as === 'a' || href) {
    return /*#__PURE__*/React.createElement("a", _extends({
      href: href,
      style: computed,
      onClick: onClick
    }, handlers, rest), children);
  }
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    style: computed,
    onClick: onClick,
    disabled: disabled
  }, handlers, rest), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
/** Generic elevated surface container — the base for service cards, contact
 * cards, and hours cards throughout the site. */
function Card({
  children,
  padding = 'var(--space-8)',
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-sm)',
      padding,
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/content/HoursCard.jsx
try { (() => {
/** Seasonal office-hours card — splits Tax Season vs After Tax Season, each
 * with a day-range → hours table and an "appointment only" footnote. */
function HoursCard({
  season = 'tax',
  ...props
}) {
  const data = season === 'tax' ? {
    label: 'Tax Season',
    range: 'January – April',
    rows: [['Monday – Saturday', '9am – 7pm'], ['Sunday', '10am – 6pm']],
    footnote: 'After Hours — By Appointment Only'
  } : {
    label: 'After Tax Season',
    range: 'May – December',
    rows: [['Monday – Friday', '10am – 6pm'], ['Saturday – Sunday', 'By Appointment Only']],
    footnote: 'After Hours — By Appointment Only'
  };
  return /*#__PURE__*/React.createElement(__ds_scope.Card, {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-lg)',
      color: 'var(--text-heading)'
    }
  }, data.label), /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    tone: season === 'tax' ? 'red' : 'outline'
  }, data.range)), /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      borderCollapse: 'collapse',
      fontFamily: 'var(--font-body)'
    }
  }, /*#__PURE__*/React.createElement("tbody", null, data.rows.map(([day, hours]) => /*#__PURE__*/React.createElement("tr", {
    key: day,
    style: {
      borderTop: '1px solid var(--border-subtle)'
    }
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 0',
      color: 'var(--text-body)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-medium)'
    }
  }, day), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 0',
      color: 'var(--text-muted)',
      fontSize: 'var(--text-sm)',
      textAlign: 'right'
    }
  }, hours))))), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)',
      fontStyle: 'italic'
    }
  }, data.footnote));
}
Object.assign(__ds_scope, { HoursCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/HoursCard.jsx", error: String((e && e.message) || e) }); }

// components/core/Icon.jsx
try { (() => {
/**
 * Icon renders a Lucide icon by name. Requires the consuming page to load
 * the Lucide CDN script (see prompt.md) — this design system has no native
 * icon set, so Lucide (stroke-based, 2px, matches the brand's clean-line feel)
 * is used as a documented CDN substitution.
 */
function Icon({
  name,
  size = 20,
  color = 'currentColor',
  strokeWidth = 2,
  style
}) {
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
        attrs: {
          width: size,
          height: size,
          stroke: color,
          'stroke-width': strokeWidth
        }
      });
    }
  }, [name, size, color, strokeWidth]);
  return /*#__PURE__*/React.createElement("span", {
    ref: ref,
    "aria-hidden": "true",
    style: {
      display: 'inline-flex',
      width: size,
      height: size,
      flexShrink: 0,
      ...style
    }
  });
}
Object.assign(__ds_scope, { Icon });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Icon.jsx", error: String((e && e.message) || e) }); }

// components/content/ContactCard.jsx
try { (() => {
/** Contact-details card — address, phone, email, website, each with an
 * icon + link where relevant. Used on the home page and a dedicated
 * contact section. */
function ContactCard({
  address = '1320 N. Van Ness Ave, Fresno CA 93702',
  areaNote = 'Near Tower District',
  phone = '(559) 962-7503',
  email = 'info@candrtaxservices.com',
  website = 'www.candrtaxservices.com'
}) {
  const rows = [{
    icon: 'map-pin',
    label: address,
    sub: areaNote
  }, {
    icon: 'phone',
    label: phone,
    href: `tel:${phone.replace(/[^\d]/g, '')}`
  }, {
    icon: 'mail',
    label: email,
    href: `mailto:${email}`
  }, {
    icon: 'globe',
    label: website,
    href: `https://${website.replace(/^https?:\/\//, '')}`
  }];
  return /*#__PURE__*/React.createElement(__ds_scope.Card, {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-5)'
    }
  }, rows.map(r => /*#__PURE__*/React.createElement("div", {
    key: r.label,
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: '14px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 36,
      height: 36,
      borderRadius: 'var(--radius-md)',
      background: 'var(--surface-alt)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: r.icon,
    size: 18,
    color: "var(--icon-primary)"
  })), /*#__PURE__*/React.createElement("div", null, r.href ? /*#__PURE__*/React.createElement("a", {
    href: r.href,
    style: {
      color: 'var(--text-link)',
      fontWeight: 'var(--weight-semibold)',
      textDecoration: 'none',
      fontSize: 'var(--text-base)'
    }
  }, r.label) : /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--text-body)',
      fontWeight: 'var(--weight-semibold)',
      fontSize: 'var(--text-base)'
    }
  }, r.label), r.sub && /*#__PURE__*/React.createElement("div", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-sm)'
    }
  }, r.sub)))));
}
Object.assign(__ds_scope, { ContactCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/ContactCard.jsx", error: String((e && e.message) || e) }); }

// components/content/ServiceCategoryCard.jsx
try { (() => {
/** A single service category card — icon, title, and a checklist of
 * sub-services. Used to build the three C&R service groups (Income Tax,
 * Notary & Loan Signing, Livescan Fingerprints). */
function ServiceCategoryCard({
  icon = 'briefcase',
  title,
  note,
  items = []
}) {
  return /*#__PURE__*/React.createElement(__ds_scope.Card, {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-5)',
      height: '100%'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '14px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 'var(--radius-md)',
      background: 'var(--surface-alt)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: icon,
    size: 22,
    color: "var(--icon-primary)"
  })), /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-lg)',
      color: 'var(--text-heading)'
    }
  }, title)), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: 'none',
      margin: 0,
      padding: 0,
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }
  }, items.map(it => /*#__PURE__*/React.createElement("li", {
    key: it,
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: '10px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      color: 'var(--text-body)',
      lineHeight: 'var(--leading-snug)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "check",
    size: 16,
    color: "var(--color-royal-blue)",
    style: {
      marginTop: 2
    }
  }), /*#__PURE__*/React.createElement("span", null, it)))), note && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)',
      fontStyle: 'italic'
    }
  }, note));
}
Object.assign(__ds_scope, { ServiceCategoryCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/ServiceCategoryCard.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Footer.jsx
try { (() => {
/** Site footer — navy background, contact recap, office hours summary,
 * copyright. Mirrors the header's role as the brand-color bookend. */
function Footer({
  address = '1320 N. Van Ness Ave, Fresno CA 93702',
  phone = '(559) 962-7503',
  email = 'info@candrtaxservices.com',
  website = 'www.candrtaxservices.com'
}) {
  const row = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    color: 'var(--text-inverse)',
    fontSize: 'var(--text-sm)'
  };
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      background: 'var(--color-navy)',
      color: 'var(--text-inverse)',
      padding: 'var(--space-16) var(--space-8)',
      fontFamily: 'var(--font-body)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto',
      display: 'flex',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 'var(--space-10)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-lg)'
    }
  }, "C&R Tax Services"), /*#__PURE__*/React.createElement("div", {
    style: row
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "map-pin",
    size: 16,
    color: "var(--icon-on-dark)"
  }), address)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: row
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "phone",
    size: 16,
    color: "var(--icon-on-dark)"
  }), phone), /*#__PURE__*/React.createElement("div", {
    style: row
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "mail",
    size: 16,
    color: "var(--icon-on-dark)"
  }), email), /*#__PURE__*/React.createElement("div", {
    style: row
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "globe",
    size: 16,
    color: "var(--icon-on-dark)"
  }), website))), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: 'var(--space-10) auto 0',
      paddingTop: 'var(--space-6)',
      borderTop: '1px solid rgba(247,248,250,0.15)',
      fontSize: 'var(--text-xs)',
      color: 'var(--color-ice-blue)',
      opacity: 0.7
    }
  }, "\xA9 ", new Date().getFullYear(), " C&R Tax Services. All rights reserved."));
}
Object.assign(__ds_scope, { Footer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Footer.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Header.jsx
try { (() => {
/** Site header — logo, primary nav, and a phone CTA. Sticky, navy-on-white
 * with a thin bottom border; collapses nav into a plain stack under 720px
 * (no hamburger drawer — the nav is short enough to wrap). */
function Header({
  logoSrc,
  navItems = [],
  phone = '(559) 962-7503',
  active
}) {
  return /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 'var(--space-6)',
      padding: '16px var(--space-8)',
      background: 'var(--surface-card)',
      borderBottom: '1px solid var(--border-subtle)',
      fontFamily: 'var(--font-body)',
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    }
  }, logoSrc && /*#__PURE__*/React.createElement("img", {
    src: logoSrc,
    alt: "C&R Tax Services",
    style: {
      height: 40
    }
  })), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: 'var(--space-6)',
      flexWrap: 'wrap'
    }
  }, navItems.map(item => /*#__PURE__*/React.createElement("a", {
    key: item.label,
    href: item.href,
    style: {
      textDecoration: 'none',
      color: item.label === active ? 'var(--color-navy)' : 'var(--text-muted)',
      fontWeight: item.label === active ? 'var(--weight-semibold)' : 'var(--weight-medium)',
      fontSize: 'var(--text-sm)',
      borderBottom: item.label === active ? '2px solid var(--accent-cta)' : '2px solid transparent',
      paddingBottom: 4
    }
  }, item.label))), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    as: "a",
    href: `tel:${phone.replace(/[^\d]/g, '')}`,
    variant: "primary",
    size: "sm"
  }, "Call ", phone));
}
Object.assign(__ds_scope, { Header });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/HomePage.jsx
try { (() => {
const {
  Header,
  Footer,
  Button,
  Badge,
  ServiceCategoryCard,
  ContactCard,
  HoursCard,
  Icon
} = window.CRTaxServicesDesignSystem_70ca00;
function HomePage() {
  const [season, setSeason] = React.useState('tax');
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Header, {
    logoSrc: "../../assets/logo/crts-logo-full.jpg",
    navItems: [{
      label: 'Home',
      href: '#home'
    }, {
      label: 'Services',
      href: '#services'
    }, {
      label: 'Hours',
      href: '#hours'
    }, {
      label: 'Contact',
      href: '#contact'
    }],
    active: "Home"
  }), /*#__PURE__*/React.createElement("section", {
    id: "home",
    style: {
      background: 'var(--color-navy)',
      color: 'var(--text-inverse)',
      padding: 'var(--space-24) var(--space-8)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto',
      display: 'flex',
      flexWrap: 'wrap',
      gap: 'var(--space-16)',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: '1 1 480px'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "red"
  }, "Tax Season Hours In Effect"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-extrabold)',
      fontSize: 'var(--text-5xl)',
      lineHeight: 'var(--leading-tight)',
      margin: '18px 0 20px'
    }
  }, "Welcome to C&R Tax Services"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-lg)',
      lineHeight: 'var(--leading-normal)',
      color: 'var(--color-ice-blue)',
      maxWidth: 560,
      margin: '0 0 32px'
    }
  }, "Fresno\u2019s trusted source for income tax preparation, notary & loan signing, and Livescan fingerprinting \u2014 located near the Tower District."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 14,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    as: "a",
    href: "tel:5599627503",
    variant: "primary",
    size: "lg"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "phone",
    size: 18
  }), " (559) 962-7503"), /*#__PURE__*/React.createElement(Button, {
    as: "a",
    href: "#services",
    variant: "outline",
    size: "lg",
    style: {
      color: 'var(--text-inverse)',
      borderColor: 'rgba(247,248,250,0.4)'
    }
  }, "View Services"))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: '1 1 320px',
      maxWidth: 420
    }
  }, /*#__PURE__*/React.createElement(ContactCard, null)))), /*#__PURE__*/React.createElement("section", {
    id: "services",
    style: {
      padding: 'var(--space-24) var(--space-8)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      marginBottom: 'var(--space-12)'
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-3xl)',
      color: 'var(--text-heading)',
      margin: '0 0 10px'
    }
  }, "Services"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-base)',
      margin: 0
    }
  }, "Three ways we help Fresno families and businesses stay on track.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: 'var(--space-8)'
    }
  }, /*#__PURE__*/React.createElement(ServiceCategoryCard, {
    icon: "calculator",
    title: "Income Tax",
    items: ['Individual', 'Small Business / Self Employed', 'Rental Properties', 'Corporations, Partnerships & LLC\u2019s', 'ITIN Applications', 'Amendments', 'Audit Services', 'Extensions', 'Prior Year Reviews', 'Multi State Returns'],
    note: "Virtual/online tax preparation available any day, all year!"
  }), /*#__PURE__*/React.createElement(ServiceCategoryCard, {
    icon: "stamp",
    title: "Notary Public & Loan Signing Agent",
    items: ['Bank Documents', 'Travel Documents', 'Power of Attorney', 'Real Estate Documents & Forms', 'Legal Documents & Forms'],
    note: "Mobile services available upon request \u2014 travel fees apply."
  }), /*#__PURE__*/React.createElement(ServiceCategoryCard, {
    icon: "fingerprint",
    title: "Livescan Fingerprints",
    items: ['Livescan Background Checks', 'FD-258 Card']
  })))), /*#__PURE__*/React.createElement("section", {
    id: "hours",
    style: {
      background: 'var(--surface-alt)',
      padding: 'var(--space-24) var(--space-8)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 'var(--container-max)',
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      marginBottom: 'var(--space-12)'
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-3xl)',
      color: 'var(--text-heading)',
      margin: '0 0 10px'
    }
  }, "Office Hours"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      gap: 8,
      background: 'var(--surface-card)',
      padding: 4,
      borderRadius: 'var(--radius-pill)',
      border: '1px solid var(--border-subtle)'
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => setSeason('tax'),
    style: {
      border: 'none',
      cursor: 'pointer',
      padding: '8px 18px',
      borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-body)',
      fontWeight: 'var(--weight-semibold)',
      fontSize: 'var(--text-sm)',
      background: season === 'tax' ? 'var(--color-navy)' : 'transparent',
      color: season === 'tax' ? 'var(--text-inverse)' : 'var(--text-muted)'
    }
  }, "Tax Season"), /*#__PURE__*/React.createElement("button", {
    onClick: () => setSeason('off'),
    style: {
      border: 'none',
      cursor: 'pointer',
      padding: '8px 18px',
      borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-body)',
      fontWeight: 'var(--weight-semibold)',
      fontSize: 'var(--text-sm)',
      background: season === 'off' ? 'var(--color-navy)' : 'transparent',
      color: season === 'off' ? 'var(--text-inverse)' : 'var(--text-muted)'
    }
  }, "After Tax Season"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 420,
      width: '100%'
    }
  }, /*#__PURE__*/React.createElement(HoursCard, {
    season: season
  }))))), /*#__PURE__*/React.createElement("section", {
    id: "contact",
    style: {
      padding: 'var(--space-24) var(--space-8)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 640,
      margin: '0 auto',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: 'var(--font-heading)',
      fontWeight: 'var(--weight-bold)',
      fontSize: 'var(--text-3xl)',
      color: 'var(--text-heading)',
      margin: '0 0 10px'
    }
  }, "Get In Touch"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-base)',
      margin: '0 0 32px'
    }
  }, "Stop by, call, or book a virtual appointment \u2014 we\u2019re here all year."), /*#__PURE__*/React.createElement(ContactCard, null))), /*#__PURE__*/React.createElement(Footer, null));
}
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/HomePage.jsx", error: String((e && e.message) || e) }); }

__ds_ns.ContactCard = __ds_scope.ContactCard;

__ds_ns.HoursCard = __ds_scope.HoursCard;

__ds_ns.ServiceCategoryCard = __ds_scope.ServiceCategoryCard;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Icon = __ds_scope.Icon;

__ds_ns.Footer = __ds_scope.Footer;

__ds_ns.Header = __ds_scope.Header;

})();
