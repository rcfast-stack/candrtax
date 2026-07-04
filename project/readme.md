# C&R Tax Services — Design System

## Company context

C&R Tax Services is a small, local tax-preparation, notary, and Livescan
fingerprinting business located at 1320 N. Van Ness Ave, Fresno, CA 93702
(near the Tower District). It's a single-location, appointment-driven
business run for individuals and small businesses in the Fresno area.

**Sources provided for this design system:**
- Pasted brief with brand colors and full site copy (home page, services, hours, contact)
- `uploads/CRTS_logo_2.jpg` — the company's primary logo lockup (shield mark + wordmark)

No codebase, Figma file, or existing website was provided. This is a
from-scratch brand system built directly from the color palette and copy
given, plus the one logo asset. There is no existing UI to preserve fidelity
to — component and layout decisions below are original, sized to what a
single-location tax/notary/fingerprinting business site actually needs.

**Products in scope:** one marketing website (home page covering welcome,
services, hours, and contact). No app, no docs site.

## Content fundamentals

- **Voice:** plain, direct, informational — a neighborhood professional
  service, not a fintech startup. No jargon, no hype. Sentences state facts:
  hours, services, contact methods.
- **Person:** mostly third-person/neutral ("We are located at…") with an
  implicit "we" for the business. No customer-facing "you" copy was given —
  keep new copy in the same register (business speaking plainly about itself)
  rather than switching to a marketing "you'll love this" voice.
- **Casing:** Title Case for headings and service names ("Income Tax",
  "Notary Public & Loan Signing Agent"). Body copy is sentence case.
- **Structure:** heavy use of nested bullet lists to enumerate service
  offerings — the source copy is literally an outline (service → sub-services).
  Preserve that enumerdated, scannable structure; don't prose-ify it.
  Example straight from the brief: *"Income Tax → Individual, Small Business /
  Self Employed, Rental Properties, Corporations, Partnerships, & LLC's…"*
- **Urgency/availability flags called out explicitly:** "Available Any Day
  and All Year!", "By Appointment Only", "Mobile Services available upon
  request – Travel fees will be applied." These read as short, italicized or
  badge-style asides, not buried in paragraphs.
- **No emoji, no slang, no exclamation-heavy copy** — the one exclamation
  point in the source ("Available Any Day and All Year!") is the outlier, not
  the norm. Keep new copy restrained.
- **Numbers stay literal:** phone numbers, addresses, and hours are quoted
  exactly as given, never paraphrased ("(559) 962-7503", not "give us a call").

## Visual foundations

- **Color:** Navy (`#1B2A5E`) is the dominant structural color — headers,
  nav, footer, and section anchoring. Royal Blue (`#0A4A93`) is secondary —
  links, icons, secondary actions. Growth Red (`#E23A28`) is reserved
  strictly for CTAs (call/book buttons, urgent badges) — never decorative,
  never a background fill. Ice Blue (`#EAF0F8`) and Off-White (`#F7F8FA`) are
  the two light surfaces (alternate section backgrounds vs. page background).
  Slate (`#5A6B8C`) is muted/secondary text; Midnight (`#121D42`) is body
  text and the darkest surface option.
- **Type:** two-family system. Headings use a bold geometric sans
  (Poppins — see Iconography/Fonts note below on substitution) matching the
  blocky, confident capitals in the wordmark. Body copy uses a clean
  humanist sans (Inter) for the dense, list-heavy service and hours content.
  Headings skew bold/extrabold and tight-leading; body stays regular/medium
  weight with generous (1.6) line-height for scanability.
- **Spacing:** 4px base unit scaling up to 128px for section padding.
  Generous section padding (`--space-24` = 96px) reflects a calm, unhurried
  brand — this isn't a dense SaaS dashboard.
- **Backgrounds:** flat color fields only — no gradients, no photography, no
  illustration, no texture/grain. Alternate sections between off-white and
  ice-blue for rhythm; navy full-bleed for hero and footer bookends.
- **Animation:** minimal. Buttons get a fast (0.15s) color transition on
  hover and a slight scale-down (0.97) on press. No page-load animations,
  no bouncing, no parallax — consistent with a no-nonsense local service
  brand.
- **Hover states:** buttons darken (primary red → deeper red, navy →
  midnight); links shift from royal blue to navy. No lightening — this
  palette reads better going darker on hover.
- **Press states:** scale to 0.97, no color change beyond the hover state
  already applied.
- **Borders:** thin (1px), low-contrast (`--border-subtle` = a soft
  blue-grey), used to separate cards and header/footer edges from
  same-toned backgrounds — never a heavy or colored border.
- **Shadows:** soft and shallow (`--shadow-sm`/`md`/`lg`, navy-tinted at low
  opacity) — cards lift gently off the page, no heavy drop shadows.
- **Corner radii:** 6/10/16px scale (sm/md/lg) for chips/inputs/cards, plus
  a pill radius for buttons and badges. No sharp/square cards.
- **Cards:** white surface, 1px subtle border, soft shadow, 16px radius,
  generous internal padding. This is the one repeating "container" pattern
  in the system — used for services, contact info, and hours.
- **Transparency/blur:** none used — no frosted-glass panels, no translucent
  overlays. The footer's divider line is the only semi-transparent value
  (15% white) used anywhere.
- **Imagery:** none supplied. No photography direction has been established
  — if/when the business supplies real office/team photos, they should be
  warm, natural-light, unfiltered (matching the plain, trustworthy voice) —
  no cool corporate-stock color grading.

## Iconography

No icon system, icon font, or SVG set was provided in the source materials.
**Substitution:** [Lucide](https://lucide.dev) icons (CDN-loaded), a stroke-based
set at 2px stroke weight, chosen because its clean single-weight line style
matches the brand's plain, no-frills visual register and pairs neatly with
the logo's line-drawn arrow motif. This is a flagged substitution — swap in
a brand-specific icon set if the client provides one.
- Loaded via CDN (`unpkg.com/lucide@latest`), never bundled as local SVG
  files, since no source icons exist to copy.
- Used sparingly: contact-method icons (phone/mail/globe/pin), a small
  service-category icon per card (calculator, stamp, fingerprint), and
  inline checkmarks in service lists.
- No emoji, no unicode glyphs used as icons anywhere in this system.
- See `components/core/Icon.jsx` for the wrapper component and usage.

## Fonts — flagged substitution

No font files were supplied. The logo wordmark's bold, blocky capitals
suggested a geometric-sans headline face; **Poppins** (Google Fonts) was
selected for headings and **Inter** (Google Fonts) for body copy as the
closest freely-available match. **Please supply the business's actual brand
fonts (if any exist) and this system will be updated to match exactly.**

## Assets

- `assets/logo/crts-logo-full.jpg` — primary logo lockup (shield mark +
  "C&R Tax Services" wordmark), as supplied. This is the only real brand
  asset available; no icon-only mark, no reversed/white version, and no
  additional imagery were provided. Do not create alternate versions
  (cropped mark, white version, etc.) without a source file to derive them
  from — ask the client for those variants if needed.

## Components

Standard component set, authored from scratch (no source component library
existed to enumerate) and sized to what this one-page marketing site needs:

- **Icon** (`components/core/Icon.jsx`) — Lucide icon wrapper.
- **Button** (`components/core/Button.jsx`) — primary/secondary/outline/ghost, 3 sizes.
- **Badge** (`components/core/Badge.jsx`) — uppercase status/category pill.
- **Card** (`components/core/Card.jsx`) — base elevated surface.
- **Header** (`components/navigation/Header.jsx`) — sticky nav bar with phone CTA.
- **Footer** (`components/navigation/Footer.jsx`) — navy footer with contact recap.
- **ServiceCategoryCard** (`components/content/ServiceCategoryCard.jsx`) — icon + title + checklist, one per service line.
- **ContactCard** (`components/content/ContactCard.jsx`) — address/phone/email/website block.
- **HoursCard** (`components/content/HoursCard.jsx`) — seasonal office-hours table.

### Intentional additions
All nine components above are additions (no source inventory existed to
constrain against) — each was chosen because the provided copy directly
calls for it (services list → ServiceCategoryCard, hours block → HoursCard,
contact block → ContactCard). No speculative components (Toast, Tabs,
Dialog, etc.) were added since nothing in the brief needs them.

## Index / manifest

- `styles.css` — root stylesheet, imports all tokens
- `tokens/colors.css`, `tokens/typography.css`, `tokens/spacing.css`, `tokens/fonts.css`
- `components/core/` — Icon, Button, Badge, Card
- `components/navigation/` — Header, Footer
- `components/content/` — ServiceCategoryCard, ContactCard, HoursCard
- `guidelines/` — foundation specimen cards (Colors, Type, Spacing, Brand)
- `assets/logo/` — the one provided logo file
- `ui_kits/website/` — home page recreation (`index.html` + `HomePage.jsx`)
- `SKILL.md` — portable skill file for use in Claude Code
