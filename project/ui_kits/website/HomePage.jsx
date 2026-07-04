const { Header, Footer, Button, Badge, ServiceCategoryCard, ContactCard, HoursCard, Icon } =
  window.CRTaxServicesDesignSystem_70ca00;

function HomePage() {
  const [season, setSeason] = React.useState('tax');

  return (
    <div>
      <Header
        logoSrc="../../assets/logo/crts-logo-full.jpg"
        navItems={[
          { label: 'Home', href: '#home' },
          { label: 'Services', href: '#services' },
          { label: 'Hours', href: '#hours' },
          { label: 'Contact', href: '#contact' },
        ]}
        active="Home"
      />

      {/* Hero */}
      <section
        id="home"
        style={{
          background: 'var(--color-navy)',
          color: 'var(--text-inverse)',
          padding: 'var(--space-24) var(--space-8)',
        }}
      >
        <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto', display: 'flex', flexWrap: 'wrap', gap: 'var(--space-16)', alignItems: 'center' }}>
          <div style={{ flex: '1 1 480px' }}>
            <Badge tone="red">Tax Season Hours In Effect</Badge>
            <h1
              style={{
                fontFamily: 'var(--font-heading)',
                fontWeight: 'var(--weight-extrabold)',
                fontSize: 'var(--text-5xl)',
                lineHeight: 'var(--leading-tight)',
                margin: '18px 0 20px',
              }}
            >
              Welcome to C&amp;R Tax Services
            </h1>
            <p style={{ fontSize: 'var(--text-lg)', lineHeight: 'var(--leading-normal)', color: 'var(--color-ice-blue)', maxWidth: 560, margin: '0 0 32px' }}>
              Fresno&rsquo;s trusted source for income tax preparation, notary &amp; loan
              signing, and Livescan fingerprinting — located near the Tower District.
            </p>
            <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
              <Button as="a" href="tel:5599627503" variant="primary" size="lg">
                <Icon name="phone" size={18} /> (559) 962-7503
              </Button>
              <Button as="a" href="#services" variant="outline" size="lg" style={{ color: 'var(--text-inverse)', borderColor: 'rgba(247,248,250,0.4)' }}>
                View Services
              </Button>
            </div>
          </div>
          <div style={{ flex: '1 1 320px', maxWidth: 420 }}>
            <ContactCard />
          </div>
        </div>
      </section>

      {/* Services */}
      <section id="services" style={{ padding: 'var(--space-24) var(--space-8)' }}>
        <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-12)' }}>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontWeight: 'var(--weight-bold)', fontSize: 'var(--text-3xl)', color: 'var(--text-heading)', margin: '0 0 10px' }}>
              Services
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: 'var(--text-base)', margin: 0 }}>
              Three ways we help Fresno families and businesses stay on track.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 'var(--space-8)' }}>
            <ServiceCategoryCard
              icon="calculator"
              title="Income Tax"
              items={[
                'Individual',
                'Small Business / Self Employed',
                'Rental Properties',
                'Corporations, Partnerships & LLC\u2019s',
                'ITIN Applications',
                'Amendments',
                'Audit Services',
                'Extensions',
                'Prior Year Reviews',
                'Multi State Returns',
              ]}
              note="Virtual/online tax preparation available any day, all year!"
            />
            <ServiceCategoryCard
              icon="stamp"
              title="Notary Public & Loan Signing Agent"
              items={[
                'Bank Documents',
                'Travel Documents',
                'Power of Attorney',
                'Real Estate Documents & Forms',
                'Legal Documents & Forms',
              ]}
              note="Mobile services available upon request — travel fees apply."
            />
            <ServiceCategoryCard
              icon="fingerprint"
              title="Livescan Fingerprints"
              items={[
                'Livescan Background Checks',
                'FD-258 Card',
              ]}
            />
          </div>
        </div>
      </section>

      {/* Hours */}
      <section id="hours" style={{ background: 'var(--surface-alt)', padding: 'var(--space-24) var(--space-8)' }}>
        <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-12)' }}>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontWeight: 'var(--weight-bold)', fontSize: 'var(--text-3xl)', color: 'var(--text-heading)', margin: '0 0 10px' }}>
              Office Hours
            </h2>
            <div style={{ display: 'inline-flex', gap: 8, background: 'var(--surface-card)', padding: 4, borderRadius: 'var(--radius-pill)', border: '1px solid var(--border-subtle)' }}>
              <button
                onClick={() => setSeason('tax')}
                style={{
                  border: 'none', cursor: 'pointer', padding: '8px 18px', borderRadius: 'var(--radius-pill)',
                  fontFamily: 'var(--font-body)', fontWeight: 'var(--weight-semibold)', fontSize: 'var(--text-sm)',
                  background: season === 'tax' ? 'var(--color-navy)' : 'transparent',
                  color: season === 'tax' ? 'var(--text-inverse)' : 'var(--text-muted)',
                }}
              >
                Tax Season
              </button>
              <button
                onClick={() => setSeason('off')}
                style={{
                  border: 'none', cursor: 'pointer', padding: '8px 18px', borderRadius: 'var(--radius-pill)',
                  fontFamily: 'var(--font-body)', fontWeight: 'var(--weight-semibold)', fontSize: 'var(--text-sm)',
                  background: season === 'off' ? 'var(--color-navy)' : 'transparent',
                  color: season === 'off' ? 'var(--text-inverse)' : 'var(--text-muted)',
                }}
              >
                After Tax Season
              </button>
            </div>
          </div>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div style={{ maxWidth: 420, width: '100%' }}>
              <HoursCard season={season} />
            </div>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section id="contact" style={{ padding: 'var(--space-24) var(--space-8)' }}>
        <div style={{ maxWidth: 640, margin: '0 auto', textAlign: 'center' }}>
          <h2 style={{ fontFamily: 'var(--font-heading)', fontWeight: 'var(--weight-bold)', fontSize: 'var(--text-3xl)', color: 'var(--text-heading)', margin: '0 0 10px' }}>
            Get In Touch
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--text-base)', margin: '0 0 32px' }}>
            Stop by, call, or book a virtual appointment — we&rsquo;re here all year.
          </p>
          <ContactCard />
        </div>
      </section>

      <Footer />
    </div>
  );
}
