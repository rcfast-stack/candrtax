#!/usr/bin/env python3
"""
Deploy TranslatePress (free) and seed English→Spanish translations
for all C&R Tax Services pages.
"""
import json, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

_sess = None
def sess():
    global _sess
    if _sess: return _sess
    r = requests.post(MCP_URL, auth=AUTH, json={
        "jsonrpc":"2.0","id":0,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"claude","version":"1.0"}}
    })
    _sess = r.headers.get("mcp-session-id") or r.headers.get("Mcp-Session-Id")
    return _sess

def php(code):
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess()}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/execute-php","parameters":{"code":code}}}
    })
    raw = r.json()["result"]["content"][0]["text"]
    parsed = json.loads(raw)
    return parsed.get("data", parsed)

# ── Step 1: Install TranslatePress ──────────────────────────────────────────
print("=== Step 1: Installing TranslatePress ===")
install_result = php(r"""
if (!function_exists('plugins_api')) {
    require_once ABSPATH . 'wp-admin/includes/plugin-api.php';
}
require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
require_once ABSPATH . 'wp-admin/includes/plugin.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/misc.php';

$plugin_file = 'translatepress-multilingual/index.php';
$active = is_plugin_active($plugin_file);
if ($active) { return ['status' => 'already_active']; }

$already_installed = file_exists(WP_PLUGIN_DIR . '/' . $plugin_file);
if (!$already_installed) {
    $api = plugins_api('plugin_information', ['slug' => 'translatepress-multilingual', 'fields' => ['downloadlink' => true]]);
    if (is_wp_error($api)) { return ['error' => $api->get_error_message()]; }

    $skin = new Automatic_Upgrader_Skin();
    $upgrader = new Plugin_Upgrader($skin);
    $result = $upgrader->install($api->download_link);
    if (is_wp_error($result) || $result === false) {
        return ['error' => 'install_failed', 'skin' => $skin->get_upgrade_messages()];
    }
}

$activated = activate_plugin($plugin_file);
if (is_wp_error($activated)) { return ['error' => $activated->get_error_message()]; }

return ['installed' => true, 'activated' => true];
""")
print("Install result:", install_result)

# ── Step 2: Configure TranslatePress (add es_ES as secondary language) ───────
print("\n=== Step 2: Configuring TranslatePress for Spanish ===")
config_result = php(r"""
// TranslatePress stores config in trp_settings option
$settings = get_option('trp_settings', []);

// Default settings if not already configured
if (empty($settings)) {
    $settings = [
        'default-language' => 'en_US',
        'translation-languages' => ['en_US', 'es_ES'],
        'native-name' => 'no',
        'english-name' => 'no',
        'flag' => 'no',
        'url-slugs' => ['en_US' => '', 'es_ES' => 'es'],
        'add-subdirectory-to-default-language' => 'no',
        'language-switcher-flags-url' => '',
        'exclude-gettext' => 'no',
        'exclude-gettext-strings' => '',
        'machine-translation' => 'no',
        'trp-ls-shortcode-language' => [],
        'data-trp-translate-id-forced' => 'no',
    ];
} else {
    // Ensure Spanish is in the list
    if (!in_array('es_ES', $settings['translation-languages'])) {
        $settings['translation-languages'][] = 'es_ES';
    }
    $settings['url-slugs']['es_ES'] = 'es';
}

update_option('trp_settings', $settings);

// Also set the trp_language_switcher option to add switcher to nav
$ls_settings = get_option('trp_advanced_settings', []);
update_option('trp_advanced_settings', $ls_settings);

// Create the dictionary table for en_US -> es_ES if it doesn't exist
global $wpdb;
$table = $wpdb->prefix . 'trp_dictionary_en_us_es_es';
$charset_collate = $wpdb->get_charset_collate();
$sql = "CREATE TABLE IF NOT EXISTS $table (
    id bigint(20) NOT NULL AUTO_INCREMENT,
    original text NOT NULL,
    translated text DEFAULT NULL,
    status int(11) DEFAULT 0,
    block_type tinyint(4) DEFAULT 2,
    modified datetime DEFAULT NULL,
    PRIMARY KEY (id),
    KEY status (status),
    KEY block_type (block_type)
) $charset_collate;";
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
dbDelta($sql);

return ['settings' => $settings, 'table_created' => true];
""")
print("Config result:", json.dumps(config_result, indent=2)[:500])

# ── Step 3: Seed Spanish translations ────────────────────────────────────────
print("\n=== Step 3: Seeding Spanish translations ===")

# All the English → Spanish translation pairs
# Covering: nav items, hero headings, section headings, body text, badges,
#           button labels, form labels, hours, contact card, etc.
translations = [
    # ── Nav items ──
    ("Home", "Inicio"),
    ("About", "Nosotros"),
    ("Income Tax", "Impuestos"),
    ("Notary", "Notaría"),
    ("Livescan", "Livescan"),
    ("Contact", "Contacto"),

    # ── Common site-wide ──
    ("Get in Touch", "Contáctenos"),
    ("Schedule Your Appointment", "Agende su Cita"),
    ("Upload Your Docs", "Suba sus Documentos"),
    ("Request a Free Quote", "Solicite una Cotización Gratuita"),
    ("Get Help Now", "Obtenga Ayuda Ahora"),
    ("Get Started Today", "Comience Hoy"),
    ("See Our Services", "Ver Nuestros Servicios"),
    ("Learn More", "Más Información"),
    ("Call Us Today", "Llámenos Hoy"),
    ("Book Your Appointment", "Reserve su Cita"),
    ("Local &amp; Family-Focused", "Local y Enfocado en la Familia"),
    ("Local & Family-Focused", "Local y Enfocado en la Familia"),
    ("Real People, Fast Responses", "Personas Reales, Respuestas Rápidas"),
    ("Fresno, CA Tax Professionals", "Profesionales de Impuestos en Fresno, CA"),

    # ── Footer ──
    ("Income Tax Preparation", "Preparación de Impuestos"),
    ("Notary Services", "Servicios Notariales"),
    ("Livescan Fingerprinting", "Huellas Dactilares Livescan"),
    ("Our Services", "Nuestros Servicios"),
    ("Quick Links", "Enlaces Rápidos"),
    ("Contact Us", "Contáctenos"),
    ("Serving Fresno and the Central Valley", "Sirviendo a Fresno y el Valle Central"),
    ("All rights reserved.", "Todos los derechos reservados."),
    ("Proudly serving Fresno and the Central Valley", "Sirviendo con orgullo a Fresno y el Valle Central"),

    # ── HOME PAGE ──
    # Hero
    ("Fresno&#8217;s Trusted Tax Professionals", "Profesionales de Impuestos de Confianza en Fresno"),
    ("Fresno's Trusted Tax Professionals", "Profesionales de Impuestos de Confianza en Fresno"),
    ("Honest. Accurate. Local.", "Honestos. Precisos. Locales."),
    ("Upfront pricing, year-round support, and real people who know your name &#8212; C&amp;R Tax Services has been the Central Valley&#8217;s go-to tax team for families and small businesses.", "Precios transparentes, soporte todo el año y personas reales que conocen su nombre — C&R Tax Services ha sido el equipo de impuestos de confianza del Valle Central para familias y pequeños negocios."),

    # Services section
    ("What We Do", "Lo Que Hacemos"),
    ("Expert help across all the services you need &#8212; from tax prep to notary to Live Scan &#8212; all under one roof.", "Ayuda experta en todos los servicios que necesita — desde preparación de impuestos hasta notaría y Live Scan — todo bajo un mismo techo."),
    ("Tax Preparation", "Preparación de Impuestos"),
    ("Individual returns, small business, rental income, ITIN applications, and more &#8212; filed accurately the first time.", "Declaraciones individuales, pequeños negocios, ingresos de alquiler, solicitudes de ITIN y más — presentadas con precisión desde la primera vez."),
    ("Notary Public", "Notario Público"),
    ("Certified notary and loan signing agent for real estate closings, legal documents, and business paperwork.", "Notario certificado y agente de firma de préstamos para cierres de bienes raíces, documentos legales y papeleo empresarial."),
    ("Live Scan Fingerprinting", "Huellas Dactilares Live Scan"),
    ("DOJ &amp; FBI-compliant fingerprinting for employment, licensing, and background checks &#8212; fast results.", "Huellas dactilares compatibles con el DOJ y el FBI para empleo, licencias y verificaciones de antecedentes — resultados rápidos."),

    # Why choose us
    ("Why Fresno Families Choose C&amp;R", "Por Qué las Familias de Fresno Eligen C&R"),
    ("Why Fresno Families Choose C&R", "Por Qué las Familias de Fresno Eligen C&R"),
    ("Upfront, Transparent Pricing", "Precios Transparentes y Directos"),
    ("No surprise bills. You know exactly what you&#8217;ll pay before we file.", "Sin facturas sorpresa. Usted sabe exactamente lo que pagará antes de que presentemos."),
    ("100% Accuracy Guarantee", "Garantía de Precisión del 100%"),
    ("If we make an error, we make it right &#8212; at no cost to you.", "Si cometemos un error, lo corregimos — sin costo para usted."),
    ("Year-Round Support", "Soporte Todo el Año"),
    ("We don&#8217;t disappear after April 15th. Call us any time you need us.", "No desaparecemos después del 15 de abril. Llámenos cuando nos necesite."),
    ("Bilingual Service", "Servicio Bilingüe"),
    ("&#161;Se habla espa&#241;ol! Ask your questions in the language you&#8217;re most comfortable with.", "¡Se habla español! Haga sus preguntas en el idioma con el que se sienta más cómodo."),

    # Service area pills
    ("Fresno", "Fresno"),
    ("Clovis", "Clovis"),
    ("Selma", "Selma"),
    ("Reedley", "Reedley"),
    ("Sanger", "Sanger"),
    ("Madera", "Madera"),

    # Serving section
    ("Serving the Central Valley", "Sirviendo al Valle Central"),
    ("Proudly Serving the Central Valley", "Sirviendo con Orgullo al Valle Central"),
    ("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return &#8212; with year-round support, not just at tax time.", "C&R Tax Services es de propiedad y operación local, completamente acreditado y comprometido con la precisión en cada declaración — con soporte durante todo el año, no solo en época de impuestos."),

    # ── ABOUT PAGE ──
    # Hero
    ("Why We Started C&amp;R Tax Services", "Por Qué Fundamos C&R Tax Services"),
    ("Why We Started C&R Tax Services", "Por Qué Fundamos C&R Tax Services"),
    ("Tax season shouldn&#8217;t feel like a guessing game &#8212; but for too many Central Valley families, that&#8217;s exactly what it&#8217;s become.", "La temporada de impuestos no debería sentirse como un juego de adivinanzas — pero para demasiadas familias del Valle Central, eso es exactamente lo que se ha convertido."),

    # Our story
    ("Our Story", "Nuestra Historia"),
    ("What We Stand For", "Lo Que Defendemos"),
    ("Meet the People Behind C&amp;R", "Conozca a las Personas Detrás de C&R"),
    ("Meet the People Behind C&R", "Conozca a las Personas Detrás de C&R"),
    ("Why Homeowners and Local Families Trust C&amp;R Tax Services", "Por Qué los Propietarios y Familias Locales Confían en C&R Tax Services"),
    ("Why Homeowners and Local Families Trust C&R Tax Services", "Por Qué los Propietarios y Familias Locales Confían en C&R Tax Services"),

    # Values
    ("Honesty", "Honestidad"),
    ("Accuracy", "Precisión"),
    ("Accessibility", "Accesibilidad"),
    ("Credentials &amp; Services", "Credenciales y Servicios"),
    ("Credentials & Services", "Credenciales y Servicios"),
    ("Notary public services &amp; loan signing support", "Servicios notariales y soporte de firma de préstamos"),
    ("Live Scan fingerprinting", "Huellas dactilares Live Scan"),

    # CTA
    ("Let&#8217;s Talk &#8212; We&#8217;d Love to Meet You", "Hablemos — Nos Encantaría Conocerlo"),
    ("Let's Talk — We'd Love to Meet You", "Hablemos — Nos Encantaría Conocerlo"),

    # ── CONTACT PAGE ──
    ("We&#8217;re Glad You&#8217;re Here", "Nos Alegra su Visita"),
    ("We're Glad You're Here", "Nos Alegra su Visita"),
    ("How to Reach Us", "Cómo Contactarnos"),
    ("Why Reach Out?", "¿Por Qué Contactarnos?"),
    ("Your Trusted Local Team", "Su Equipo Local de Confianza"),
    ("Let&#8217;s Get Started Today", "Comencemos Hoy"),
    ("Let's Get Started Today", "Comencemos Hoy"),
    ("General questions", "Preguntas Generales"),
    ("Free quotes", "Cotizaciones Gratuitas"),
    ("Urgent tax matters", "Asuntos Fiscales Urgentes"),
    ("Notary &amp; Live Scan appointments", "Citas de Notaría y Live Scan"),
    ("Notary & Live Scan appointments", "Citas de Notaría y Live Scan"),

    # Hours card
    ("Tax Season Hours", "Horario de Temporada de Impuestos"),
    ("After Tax Season Hours", "Horario Fuera de Temporada"),
    ("Tax Season", "Temporada de Impuestos"),
    ("After Tax Season", "Fuera de Temporada"),
    ("Monday", "Lunes"),
    ("Tuesday", "Martes"),
    ("Wednesday", "Miércoles"),
    ("Thursday", "Jueves"),
    ("Friday", "Viernes"),
    ("Saturday", "Sábado"),
    ("Sunday", "Domingo"),
    ("Closed", "Cerrado"),
    ("By appointment", "Con cita previa"),

    # Contact card
    ("Phone", "Teléfono"),
    ("Email", "Correo Electrónico"),
    ("Address", "Dirección"),
    ("Hours", "Horario"),
    ("Walk-ins Welcome", "Se Aceptan Sin Cita"),
    ("&#161;Se habla espa&#241;ol!", "¡Se habla español!"),

    # Contact form labels
    ("Send Us a Message", "Envíenos un Mensaje"),
    ("Tell us a bit about what you need, and we&#8217;ll get back to you the same business day.", "Cuéntenos un poco sobre lo que necesita y le responderemos el mismo día hábil."),
    ("Name", "Nombre"),
    ("Your full name", "Su nombre completo"),
    ("Phone (optional)", "Teléfono (opcional)"),
    ("What do you need help with?", "¿Con qué necesita ayuda?"),
    ("Select a service", "Seleccione un servicio"),
    ("Not sure / other", "No estoy seguro / otro"),
    ("Message", "Mensaje"),
    ("Tell us a little about your situation...", "Cuéntenos un poco sobre su situación..."),
    ("Send Message", "Enviar Mensaje"),
    ("Prefer to talk? Call us at", "¿Prefiere hablar? Llámenos al"),
    ("Message Sent", "Mensaje Enviado"),
    ("Thanks,", "Gracias,"),
    ("A member of our team will reach out the same business day.", "Un miembro de nuestro equipo se pondrá en contacto el mismo día hábil."),

    # ── INCOME TAX PAGE ──
    ("Expert Tax Preparation in Fresno, CA", "Preparación de Impuestos Experta en Fresno, CA"),
    ("Professional. Accurate. Affordable.", "Profesional. Preciso. Asequible."),
    ("Fresno Tax Preparation", "Preparación de Impuestos en Fresno"),
    ("Income Tax Preparation in Fresno", "Preparación de Impuestos en Fresno"),
    ("What We Prepare", "Lo Que Preparamos"),
    ("Individual Tax Returns", "Declaraciones de Impuestos Individuales"),
    ("W-2 income, multiple jobs, investment income, retirement distributions, and more.", "Ingresos W-2, múltiples empleos, ingresos de inversión, distribuciones de jubilación y más."),
    ("Self-Employed &amp; Freelance", "Trabajadores por Cuenta Propia y Freelancers"),
    ("Self-Employed & Freelance", "Trabajadores por Cuenta Propia y Freelancers"),
    ("Schedule C, quarterly estimates, deductions &#8212; we handle the complexity so you don&#8217;t have to.", "Anexo C, estimaciones trimestrales, deducciones — nosotros manejamos la complejidad para que usted no tenga que hacerlo."),
    ("Small Business Returns", "Declaraciones para Pequeños Negocios"),
    ("S-Corps, partnerships, LLCs &#8212; filed accurately with every deduction you&#8217;re entitled to.", "S-Corps, sociedades, LLC — presentadas con precisión con cada deducción a la que tiene derecho."),
    ("Rental Property Income", "Ingresos de Propiedades en Alquiler"),
    ("Schedule E preparation, depreciation, repairs, and landlord-specific deductions.", "Preparación del Anexo E, depreciación, reparaciones y deducciones específicas para propietarios."),
    ("ITIN Applications", "Solicitudes de ITIN"),
    ("We&#8217;re a Certified Acceptance Agent &#8212; we can verify your identity documents and submit your W-7 directly to the IRS.", "Somos un Agente de Aceptación Certificado — podemos verificar sus documentos de identidad y enviar su W-7 directamente al IRS."),
    ("Multi-State Returns", "Declaraciones de Múltiples Estados"),
    ("Lived or worked in more than one state? We untangle the complexity and file correctly in every jurisdiction.", "¿Vivió o trabajó en más de un estado? Desenredamos la complejidad y presentamos correctamente en cada jurisdicción."),
    ("Amended Returns", "Declaraciones Enmendadas"),
    ("Need to fix a prior-year return? We file 1040-X amendments quickly and accurately.", "¿Necesita corregir una declaración de un año anterior? Presentamos enmiendas 1040-X de forma rápida y precisa."),
    ("Prior Year Returns", "Declaraciones de Años Anteriores"),
    ("Behind on filing? We help you get caught up without judgment &#8212; and often find refunds you didn&#8217;t know you were owed.", "¿Atrasado en sus declaraciones? Le ayudamos a ponerse al día sin juzgarlo — y frecuentemente encontramos reembolsos que no sabía que le correspondían."),
    ("How It Works", "Cómo Funciona"),
    ("Gather your documents", "Reúna sus documentos"),
    ("W-2s, 1099s, receipts, last year&#8217;s return &#8212; whatever you have. Not sure what you need? Just call us.", "W-2, 1099, recibos, declaración del año pasado — lo que tenga. ¿No está seguro de lo que necesita? Solo llámenos."),
    ("Meet with us (in person or virtual)", "Reúnase con nosotros (en persona o virtual)"),
    ("We review your documents, ask the right questions, and identify every deduction you qualify for.", "Revisamos sus documentos, hacemos las preguntas correctas e identificamos cada deducción para la que califica."),
    ("We prepare and review your return", "Preparamos y revisamos su declaración"),
    ("You&#8217;ll see exactly what we&#8217;re filing before we submit &#8212; no surprises.", "Verá exactamente lo que estamos presentando antes de enviarlo — sin sorpresas."),
    ("You approve, we file", "Usted aprueba, nosotros presentamos"),
    ("E-file goes out the same day. Refunds typically arrive within 21 days for direct deposit.", "La presentación electrónica se realiza el mismo día. Los reembolsos generalmente llegan dentro de 21 días para depósito directo."),
    ("Pricing", "Precios"),
    ("Upfront Pricing", "Precios Transparentes"),
    ("No hidden fees. We quote your exact price before we file &#8212; period.", "Sin tarifas ocultas. Le cotizamos el precio exacto antes de presentar — punto."),
    ("Simple returns start at $150", "Las declaraciones simples comienzan en $150"),
    ("Complex returns are quoted individually", "Las declaraciones complejas se cotizan individualmente"),
    ("No percentage-of-refund fees &#8212; ever", "Sin tarifas basadas en porcentaje del reembolso — nunca"),
    ("Military discounts available", "Descuentos disponibles para militares"),
    ("Ready to Get Your Taxes Done Right?", "¿Listo para Presentar sus Impuestos Correctamente?"),

    # ── NOTARY PAGE ──
    ("Professional Notary Services in Fresno, CA", "Servicios Notariales Profesionales en Fresno, CA"),
    ("Certified. Convenient. Local.", "Certificado. Conveniente. Local."),
    ("Notary Public in Fresno", "Notario Público en Fresno"),
    ("What We Notarize", "Lo Que Notarizamos"),
    ("Real Estate Documents", "Documentos de Bienes Raíces"),
    ("Grant deeds, trust transfers, quitclaim deeds, and more &#8212; we work with buyers, sellers, and their agents.", "Escrituras de donación, transferencias de fideicomiso, escrituras de renuncia y más — trabajamos con compradores, vendedores y sus agentes."),
    ("Loan Signing", "Firma de Préstamos"),
    ("Certified loan signing agent for mortgage closings, refinances, and HELOCs. We guide you through every page.", "Agente certificado de firma de préstamos para cierres hipotecarios, refinanciamientos y HELOC. Le guiamos por cada página."),
    ("Power of Attorney", "Poder Notarial"),
    ("General, durable, and limited POA documents notarized quickly and correctly.", "Documentos de poder notarial general, duradero y limitado notarizados de forma rápida y correcta."),
    ("Affidavits &amp; Sworn Statements", "Declaraciones Juradas"),
    ("Affidavits & Sworn Statements", "Declaraciones Juradas"),
    ("Personal and business affidavits, statutory declarations, and notarized letters.", "Declaraciones juradas personales y comerciales, declaraciones estatutarias y cartas notarizadas."),
    ("Business Documents", "Documentos Comerciales"),
    ("Articles of organization, operating agreements, corporate resolutions, and more.", "Artículos de organización, acuerdos operativos, resoluciones corporativas y más."),
    ("Immigration Documents", "Documentos de Inmigración"),
    ("Certified translations and notarized copies for USCIS, consulates, and immigration attorneys.", "Traducciones certificadas y copias notarizadas para USCIS, consulados y abogados de inmigración."),
    ("Why Use C&amp;R for Notary Services?", "¿Por Qué Usar C&R para Servicios Notariales?"),
    ("Why Use C&R for Notary Services?", "¿Por Qué Usar C&R para Servicios Notariales?"),
    ("Commissioned California Notary Public", "Notario Público Comisionado de California"),
    ("Certified Loan Signing Agent", "Agente Certificado de Firma de Préstamos"),
    ("Same-day and next-day appointments available", "Citas disponibles el mismo día y al día siguiente"),
    ("Affordable, flat-fee pricing", "Precios asequibles de tarifa fija"),
    ("Bilingual notary &#8212; &#161;se habla espa&#241;ol!", "Notario bilingüe — ¡se habla español!"),
    ("Need a Document Notarized?", "¿Necesita un Documento Notariado?"),

    # ── LIVESCAN PAGE ──
    ("Livescan Fingerprinting in Fresno, CA", "Huellas Dactilares Livescan en Fresno, CA"),
    ("Fast. Accurate. DOJ-Certified.", "Rápido. Preciso. Certificado por el DOJ."),
    ("Live Scan Fingerprinting in Fresno", "Huellas Dactilares Live Scan en Fresno"),
    ("Who Needs Live Scan?", "¿Quién Necesita Live Scan?"),
    ("Teachers &amp; School Staff", "Maestros y Personal Escolar"),
    ("Teachers & School Staff", "Maestros y Personal Escolar"),
    ("Required for all California educators under Education Code 44237.", "Requerido para todos los educadores de California bajo el Código de Educación 44237."),
    ("Healthcare Workers", "Trabajadores de Salud"),
    ("Nurses, CNAs, home health aides, and other licensed healthcare professionals.", "Enfermeras, asistentes de enfermería, auxiliares de salud en el hogar y otros profesionales de salud con licencia."),
    ("Real Estate &amp; Insurance Agents", "Agentes de Bienes Raíces y Seguros"),
    ("Real Estate & Insurance Agents", "Agentes de Bienes Raíces y Seguros"),
    ("Required for DRE and CDI license applications.", "Requerido para solicitudes de licencias DRE y CDI."),
    ("Childcare &amp; Foster Care", "Cuidado Infantil y Hogares de Acogida"),
    ("Childcare & Foster Care", "Cuidado Infantil y Hogares de Acogida"),
    ("All adults in a licensed childcare or foster home must be fingerprinted.", "Todos los adultos en un hogar de cuidado infantil o acogida con licencia deben ser huellas dactilares."),
    ("Security &amp; Guard Card", "Tarjeta de Guardia de Seguridad"),
    ("Security & Guard Card", "Tarjeta de Guardia de Seguridad"),
    ("Required by BSIS for security guard and alarm company licenses.", "Requerido por BSIS para licencias de guardia de seguridad y compañías de alarmas."),
    ("Other Professions &amp; Licensing", "Otras Profesiones y Licencias"),
    ("Other Professions & Licensing", "Otras Profesiones y Licencias"),
    ("Contractors, attorneys, adoption applicants, and anyone else requiring a background check.", "Contratistas, abogados, solicitantes de adopción y cualquier otra persona que requiera una verificación de antecedentes."),
    ("How Our Live Scan Process Works", "Cómo Funciona Nuestro Proceso de Live Scan"),
    ("Book your appointment", "Reserve su cita"),
    ("Call or message us to schedule. We&#8217;ll confirm the ORI number and applicant type your agency requires.", "Llámenos o envíenos un mensaje para programar. Confirmaremos el número ORI y el tipo de solicitante que requiere su agencia."),
    ("Bring your ID", "Traiga su identificación"),
    ("A valid government-issued photo ID is required &#8212; driver&#8217;s license, passport, or state ID.", "Se requiere una identificación fotográfica válida emitida por el gobierno — licencia de conducir, pasaporte o identificación estatal."),
    ("We capture your prints digitally", "Capturamos sus huellas digitalmente"),
    ("Our certified operator scans all ten fingers using DOJ-approved equipment. The whole process takes about 10&#8211;15 minutes.", "Nuestro operador certificado escanea los diez dedos con equipo aprobado por el DOJ. Todo el proceso toma aproximadamente 10-15 minutos."),
    ("Results sent electronically", "Resultados enviados electrónicamente"),
    ("Your prints are transmitted directly to the DOJ and/or FBI. You&#8217;ll receive a confirmation ATI number.", "Sus huellas se transmiten directamente al DOJ y/o FBI. Recibirá un número de confirmación ATI."),
    ("DOJ-Certified Live Scan Operator", "Operador de Live Scan Certificado por el DOJ"),
    ("FBI-channeled submissions", "Envíos canalizados al FBI"),
    ("Fast turnaround &#8212; most results within 72 hours", "Respuesta rápida — la mayoría de los resultados en 72 horas"),
    ("Fast turnaround — most results within 72 hours", "Respuesta rápida — la mayoría de los resultados en 72 horas"),
    ("Walk-in and appointment options", "Opciones de visita sin cita y con cita"),
    ("Bring Your Fingerprints. Leave with Peace of Mind.", "Traiga sus Huellas. Váyase con Tranquilidad."),
    ("Ready to Get Fingerprinted?", "¿Listo para las Huellas Dactilares?"),
]

# Insert in batches of 50
BATCH_SIZE = 50
total = 0
for i in range(0, len(translations), BATCH_SIZE):
    batch = translations[i:i+BATCH_SIZE]
    # Build PHP insert code
    rows = []
    for orig, trans in batch:
        orig_esc  = orig.replace("\\", "\\\\").replace("'", "\\'")
        trans_esc = trans.replace("\\", "\\\\").replace("'", "\\'")
        rows.append(f"('{orig_esc}', '{trans_esc}', 1, 2, NOW())")
    values_sql = ",\n".join(rows)

    insert_code = f"""
global $wpdb;
$table = $wpdb->prefix . 'trp_dictionary_en_us_es_es';
$count_before = $wpdb->get_var("SELECT COUNT(*) FROM $table");
$sql = "INSERT INTO $table (original, translated, status, block_type, modified)
VALUES {values_sql}
ON DUPLICATE KEY UPDATE translated = VALUES(translated), status = 1, modified = NOW()";
$wpdb->query($sql);
$count_after = $wpdb->get_var("SELECT COUNT(*) FROM $table");
return ['inserted_batch' => {len(batch)}, 'total_rows' => (int)$count_after, 'last_error' => $wpdb->last_error];
"""
    result = php(insert_code)
    total += len(batch)
    print(f"  Batch {i//BATCH_SIZE + 1}: inserted {len(batch)} pairs → total in DB: {result.get('total_rows','?')} | err: {result.get('last_error','none')[:80]}")

print(f"\nTotal pairs submitted: {total}")

# ── Step 4: Add language switcher shortcode to footer / nav ──────────────────
print("\n=== Step 4: Enabling language switcher ===")
switcher_result = php(r"""
// Enable the language switcher in TranslatePress settings
$settings = get_option('trp_settings', []);
// The language switcher is a widget/shortcode in TranslatePress free
// Ensure switcher settings exist
if (!isset($settings['trp-ls-shortcode-language'])) {
    $settings['trp-ls-shortcode-language'] = [];
}
// Add the nav menu language switcher item
$settings['add-language-switcher-to-nav-menu'] = 'yes';
update_option('trp_settings', $settings);

// Also flush rewrite rules so /es/ subdirectory works
flush_rewrite_rules(false);

// Check current active plugins
$active = get_option('active_plugins', []);
$tp_active = in_array('translatepress-multilingual/index.php', $active);

return [
    'settings_updated' => true,
    'translatepress_active' => $tp_active,
    'translation_languages' => $settings['translation-languages'],
    'url_slugs' => $settings['url-slugs'],
];
""")
print("Switcher result:", json.dumps(switcher_result, indent=2))

# ── Step 5: Clear caches ─────────────────────────────────────────────────────
print("\n=== Step 5: Clearing caches ===")
cache_result = php(r"""
// Clear Elementor cache
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}
// Clear Breeze cache
do_action('breeze_clear_all_cache');
$breeze_dir = WP_CONTENT_DIR . '/cache/breeze-minification';
if (is_dir($breeze_dir)) {
    $it = new RecursiveDirectoryIterator($breeze_dir, RecursiveDirectoryIterator::SKIP_DOTS);
    $files = new RecursiveIteratorIterator($it, RecursiveIteratorIterator::CHILD_FIRST);
    foreach ($files as $file) {
        if ($file->isDir()) @rmdir($file->getRealPath());
        else @unlink($file->getRealPath());
    }
}
// Clear TranslatePress cache
delete_transient('trp_machine_translation_cache');
return ['cache_cleared' => true];
""")
print("Cache result:", cache_result)

print("\n=== DONE ===")
print("TranslatePress installed, configured for es_ES, and Spanish translations seeded.")
print("Visit /es/ on the site to see Spanish version.")
print("Use TranslatePress editor (front-end) to refine any translations.")
