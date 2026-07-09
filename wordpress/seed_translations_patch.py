#!/usr/bin/env python3
"""
seed_translations_patch.py
Adds missing translation pairs without truncating existing records.
Uses INSERT IGNORE so existing translations are preserved.
"""

import requests, json

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

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
    }, timeout=60)
    raw = r.json()["result"]["content"][0]["text"]
    parsed = json.loads(raw)
    data = parsed.get("data", parsed)
    return data.get("return_value", data)

# Strings missing from the current dictionary.
# Source strings use exact HTML entity form as rendered by WordPress/Elementor.
MISSING = [
    # ── NAV ──
    ("Home", "Inicio"),
    ("About", "Nosotros"),
    ("Income Tax", "Impuestos"),
    ("Notary", "Notaría"),
    ("Livescan", "Livescan"),
    ("Contact", "Contacto"),
    ("Call (559) 962-7503", "Llame al (559) 962-7503"),

    # ── HOME PAGE ──
    ("Schedule an Appointment", "Programe una Cita"),
    ("A friendly tax preparer smiling across a desk from a relaxed client, documents and laptop visible, warm office lighting.", "Un preparador de impuestos amigable sonriendo desde un escritorio frente a un cliente relajado, documentos y laptop visibles, iluminación cálida de oficina."),
    ("Full-Service Offerings", "Servicios Completos"),
    ("Individual &amp; Rental Property Taxes", "Impuestos Individuales y de Propiedades de Alquiler"),
    ("For a lot of people, filing personal taxes feels like a guessing game. Did you claim every deduction you qualify for? Was that side income reported the right way? Is your refund as big as it should be? Filing alone, or with generic software, often leaves those questions hanging in the air.",
     "Para mucha gente, presentar los impuestos personales se siente como un juego de adivinanzas. ¿Reclamaste cada deducción para la que calificas? ¿Se reportó correctamente ese ingreso adicional? ¿Es tu reembolso tan grande como debería ser? Declarar solo, o con software genérico, a menudo deja esas preguntas en el aire."),
    ("&#10003; Individual", "✓ Individual"),
    ("&#10003; Rental Properties", "✓ Propiedades de Alquiler"),
    ("Small Business &amp; Corporate Business Taxes", "Impuestos de Pequeños Negocios y Corporaciones"),
    ("&#10003; Small Business / Self Employed", "✓ Pequeño Negocio / Trabajador Independiente"),
    ("&#10003; Corporations, Partnerships, &amp; LLC&rsquo;s", "✓ Corporaciones, Sociedades y LLC"),
    ("ITIN Applications &amp; Multi-State Returns", "Solicitudes de ITIN y Declaraciones Multi-Estado"),
    ("&#10003; ITIN Applications", "✓ Solicitudes de ITIN"),
    ("&#10003; Multi State Returns", "✓ Declaraciones Multi-Estado"),
    ("If an old return needs fixing, our tax amendment service sets the record straight. And if life simply got in the way this year, we can file your tax extension quickly so you get breathing room without late-filing penalties.",
     "Si una declaración antigua necesita corrección, nuestro servicio de enmiendas fiscales pone el registro en orden. Y si la vida simplemente se interpuso este año, podemos presentar tu extensión fiscal rápidamente para que tengas margen sin penalidades por presentación tardía."),
    ("&#10003; Amendments", "✓ Enmiendas"),
    ("&#10003; Extensions", "✓ Extensiones"),
    ("&#10003; Prior Year Reviews", "✓ Revisiones de Años Anteriores"),
    ("Notary Public, Loan Signing &amp; Live Scan Fingerprints", "Notario Público, Firma de Préstamos y Huellas Digitales Live Scan"),
    ("Need something notarized for a real estate deal, a power of attorney, or a business agreement? We handle it promptly. Closing on a loan? Our certified loan signing service walks you through the entire signing package. Applying for a job or license that requires a background check? Our state-compliant Live Scan fingerprinting captures and submits your prints correctly the first time.",
     "¿Necesita algo notarizado para una transacción de bienes raíces, un poder notarial o un acuerdo comercial? Lo manejamos con prontitud. ¿Cerrando un préstamo? Nuestro servicio certificado de firma de préstamos le guía por todo el paquete de firma. ¿Solicitando un trabajo o licencia que requiere verificación de antecedentes? Nuestras huellas dactilares Live Scan compatibles con el estado capturan y envían sus huellas correctamente desde la primera vez."),
    ("&#10003; Bank Documents", "✓ Documentos Bancarios"),
    ("&#10003; Travel Documents", "✓ Documentos de Viaje"),
    ("&#10003; Real Estate Documents &amp; Forms", "✓ Documentos y Formularios de Bienes Raíces"),
    ("&#10003; Legal Documents &amp; Forms", "✓ Documentos y Formularios Legales"),
    ("&#10003; Livescan Background Checks", "✓ Verificaciones de Antecedentes Livescan"),
    ("&#10003; FD-258 Card", "✓ Tarjeta FD-258"),
    ("📷 A clean collage or split-panel showing a tax document review, a notary stamp on paperwork, and a Live Scan fingerprint device.",
     "📷 Un collage limpio o panel dividido que muestra una revisión de documentos fiscales, un sello notarial en papeleo y un dispositivo de huellas dactilares Live Scan."),
    ("One thing that sets us apart is our Spanish-language tax preparation. For thousands of Central Valley families, taxes are stressful enough without a language barrier in the middle of it. Here, you can explain your situation, ask every question on your mind, and understand every line of your return completely in Spanish.",
     "Lo que nos distingue es nuestra preparación de impuestos en español. Para miles de familias del Valle Central, los impuestos son suficientemente estresantes sin una barrera del idioma en medio. Aquí puede explicar su situación, hacer cada pregunta que tenga en mente y entender cada línea de su declaración completamente en español."),
    ("Because we live and work in the Central Valley ourselves, we understand the financial realities our neighbors face. And with our secure virtual tax preparation option, distance is never a barrier.",
     "Porque vivimos y trabajamos en el Valle Central, entendemos las realidades financieras que enfrentan nuestros vecinos. Y con nuestra opción de preparación de impuestos virtual segura, la distancia nunca es una barrera."),
    ("A scenic Central Valley shot (orchards or the Fresno skyline at golden hour) with a subtle map-pin graphic marking the five service cities.",
     "Una foto panorámica del Valle Central (huertos o el horizonte de Fresno a la hora dorada) con un gráfico sutil de pin de mapa marcando las cinco ciudades de servicio."),
    ("What Clients Are Saying", "Lo Que Dicen Nuestros Clientes"),
    ("Verified client reviews will go here once collected via Google Business Profile.",
     "Las reseñas verificadas de clientes irán aquí una vez recopiladas a través de Google Business Profile."),
    ("Ready to Maximize Your Return and Minimize Your Stress?", "¿Listo para Maximizar su Reembolso y Minimizar su Estrés?"),
    ("Get Started Now &mdash; Schedule My Appointment", "Comience Ahora — Programe Mi Cita"),
    ("A relieved, smiling client shaking hands with a preparer, finished return folder on the desk, or a person happily uploading documents from their phone at home.",
     "Un cliente aliviado y sonriente estrechando la mano de un preparador, carpeta de declaración terminada en el escritorio, o una persona cargando felizmente documentos desde su teléfono en casa."),
    ("Office Hours", "Horario de Oficina"),
    ("Tax Season", "Temporada de Impuestos"),
    ("After Tax Season", "Fuera de Temporada"),
    ("Monday &ndash; Saturday", "Lunes – Sábado"),
    ("9:00 am &ndash; 7:00 pm", "9:00 am – 7:00 pm"),
    ("Sunday", "Domingo"),
    ("10:00 am &ndash; 6:00 pm", "10:00 am – 6:00 pm"),
    ("After Hours &mdash; By Appointment Only", "Fuera de Horario — Solo con Cita"),
    ("Monday &ndash; Friday", "Lunes – Viernes"),
    ("Saturday &ndash; Sunday", "Sábado – Domingo"),
    ("By Appointment Only", "Solo con Cita"),
    ("Get In Touch", "Contáctanos"),
    ("1320 N. Van Ness Ave, Fresno CA 93702", "1320 N. Van Ness Ave, Fresno CA 93702"),
    ("Near Tower District", "Cerca del Distrito Tower"),

    # ── INCOME TAX PAGE ──
    ("Available Any Day and All Year!", "¡Disponible Cualquier Día y Todo el Año!"),
    ("Upload Your Docs (Virtual Prep)", "Sube tus Documentos (Preparación Virtual)"),
    ("📷 Warm photo of a preparer greeting a Fresno family across a desk, documents organized neatly.",
     "📷 Foto cálida de un preparador saludando a una familia de Fresno en un escritorio, documentos organizados ordenadamente."),
    ("What This Service Solves", "Qué Resuelve Este Servicio"),
    ("Others come to us after a mistake has already happened: a missed form, a return filed under the wrong status, an IRS notice sitting unopened on the kitchen counter. Professional tax preparation solves these problems before they grow. We handle amendments to fix past returns, extensions when you need more time, prior-year reviews to recover money you may have left on the table, and audit support when a notice arrives and you need someone in your corner.",
     "Otros vienen a nosotros después de que ya ocurrió un error: un formulario omitido, una declaración presentada bajo el estado incorrecto, un aviso del IRS sin abrir en el mostrador de la cocina. La preparación profesional de impuestos resuelve estos problemas antes de que crezcan. Manejamos enmiendas para corregir declaraciones pasadas, extensiones cuando necesitas más tiempo, revisiones de años anteriores para recuperar dinero que puedas haber dejado sobre la mesa y apoyo en auditorías cuando llega un aviso y necesitas a alguien de tu lado."),
    ("📷 Split image or collage — a rideshare driver, a small storefront, and a rental home &#8216;For Rent&#8217; sign.",
     "📷 Imagen dividida o collage — un conductor de transporte compartido, una pequeña tienda y un letrero de casa de alquiler 'Se Alquila'."),
    ("Every Situation We Handle", "Cada Situación que Manejamos"),
    ("Individual", "Individual"),
    ("Small Business / Self Employed", "Pequeño Negocio / Trabajador Independiente"),
    ("Rental Properties", "Propiedades de Alquiler"),
    ("Corporations, Partnerships, &amp; LLC&rsquo;s", "Corporaciones, Sociedades y LLC"),
    ("ITIN Applications", "Solicitudes de ITIN"),
    ("Amendments", "Enmiendas"),
    ("Audit Services", "Servicios de Auditoría"),
    ("Extensions", "Extensiones"),
    ("Prior Year Reviews", "Revisiones de Años Anteriores"),
    ("Multi State Returns", "Declaraciones Multi-Estado"),
    ("We serve you in your language", "Te servimos en tu idioma"),
    ("Se habla espa&ntilde;ol, from your first phone call to your final signature.",
     "Se habla español, desde tu primera llamada hasta tu firma final."),
    ("Upfront, transparent pricing", "Precios transparentes por adelantado"),
    ("If we make an error on your return, we cover the adjustment costs and amend it for free.",
     "Si cometemos un error en tu declaración, cubrimos los costos de ajuste y la enmendamos gratis."),
    ("Secure virtual tax preparation", "Preparación de impuestos virtual segura"),
    ("Upload your documents from Fresno, Clovis, Sanger, Selma, or Madera and file without hunting for parking.",
     "Sube tus documentos desde Fresno, Clovis, Sanger, Selma o Madera y declara sin buscar estacionamiento."),
    ("📷 Screenshot-style graphic of the secure document upload portal on a phone, with a Central Valley orchard or Fresno skyline in the background.",
     "📷 Gráfico estilo captura de pantalla del portal seguro de carga de documentos en un teléfono, con un huerto del Valle Central o el horizonte de Fresno de fondo."),
    ("Real-World Results", "Resultados Reales"),
    ("Local Trust &amp; Licensing", "Confianza Local y Licencias"),
    ("📷 Simple map graphic highlighting the Fresno, Clovis, Sanger, Selma, and Madera service areas.",
     "📷 Gráfico de mapa simple que resalta las áreas de servicio de Fresno, Clovis, Sanger, Selma y Madera."),
    ("You Work Hard for Your Money — This Is the Year to Keep More of It",
     "Trabajas Duro por Tu Dinero — Este Es el Año para Conservar Más"),
    ("Request a Free Estimate", "Solicita una Estimación Gratuita"),
    ("Tell us about your filing situation and we'll follow up the same business day.",
     "Cuéntanos sobre tu situación de declaración y te responderemos el mismo día hábil."),
    ("Name", "Nombre"),
    ("Email", "Correo Electrónico"),
    ("What do you need help with?", "¿En qué necesitas ayuda?"),
    ("Income Tax Preparation", "Preparación de Impuestos sobre la Renta"),
    ("Notary Services", "Servicios de Notaría"),
    ("Livescan Fingerprinting", "Huellas Dactilares Livescan"),
    ("100% accuracy guarantee", "Garantía de precisión al 100%"),
    ("We also believe you should know your price", "También creemos que debes conocer tu precio"),
    ("before", "antes"),
    ("We serve you in your language", "Te servimos en tu idioma"),

    # ── ABOUT PAGE ──
    ("Meet the Team", "Conoce al Equipo"),
    ("Our Story", "Nuestra Historia"),
    ("Our Values", "Nuestros Valores"),

    # ── CONTACT PAGE ──
    ("Other", "Otro"),
    ("Message", "Mensaje"),
    ("Submit", "Enviar"),
    ("Phone", "Teléfono"),
    ("Address", "Dirección"),
    ("Hours", "Horario"),

    # ── FOOTER / SHARED ──
    ("Get Started", "Comenzar"),
    ("Learn More", "Conoce Más"),
    ("Schedule My Appointment", "Programar Mi Cita"),
    ("Book Appointment", "Reservar Cita"),
    ("Services", "Servicios"),
    ("Tax Preparation", "Preparación de Impuestos"),
    ("Virtual Tax Prep", "Preparación Virtual de Impuestos"),
    ("Se habla espa&ntilde;ol", "Se habla español"),
    ("Individual &amp; Business Tax Preparation", "Preparación de Impuestos Individuales y Empresariales"),
    ("Income Tax Services", "Servicios de Impuestos sobre la Renta"),
    ("Notary &amp; Loan Signing", "Notaría y Firma de Préstamos"),
    ("Live Scan Fingerprinting", "Huellas Dactilares Live Scan"),
]


def run():
    print(f"Total pairs to patch: {len(MISSING)}\n")

    batch_size = 30
    total = 0
    for i in range(0, len(MISSING), batch_size):
        batch = MISSING[i:i+batch_size]
        pairs_json = json.dumps([[en, es] for en, es in batch], ensure_ascii=False)
        pairs_json_esc = pairs_json.replace("'", "\\'")
        code = f"""
global $wpdb;
$pairs = json_decode('{pairs_json_esc}', true);
$inserted = 0;
foreach ($pairs as $pair) {{
    // Check if already exists
    $exists = $wpdb->get_var($wpdb->prepare(
        "SELECT id FROM {{$wpdb->prefix}}trp_dictionary_en_us_es_es WHERE original = %s LIMIT 1",
        $pair[0]
    ));
    if (!$exists) {{
        $r = $wpdb->insert(
            $wpdb->prefix . 'trp_dictionary_en_us_es_es',
            ['original' => $pair[0], 'translated' => $pair[1], 'status' => 1, 'block_type' => 2],
            ['%s','%s','%d','%d']
        );
        if ($r !== false) $inserted++;
    }}
}}
return ['inserted' => $inserted, 'err' => $wpdb->last_error ?: 'none'];
"""
        r = php(code)
        total += r.get('inserted', 0) if r else 0
        n = i // batch_size + 1
        print(f"  Batch {n}: {len(batch)} pairs | new: {r.get('inserted','?') if r else 'ERR'} | err: {r.get('err','?') if r else 'ERR'}")

    print(f"\nTotal newly inserted: {total}")

    # Final count
    r = php("global $wpdb; return ['count' => (int)$wpdb->get_var(\"SELECT COUNT(*) FROM {$wpdb->prefix}trp_dictionary_en_us_es_es WHERE status=1\")];")
    print(f"DB approved count: {r}")

    # Clear caches
    print("\nClearing caches...")
    php("""
if (function_exists('breeze_clear_all_cache')) breeze_clear_all_cache();
$cache_dir = WP_CONTENT_DIR . '/cache/breeze/';
if (is_dir($cache_dir)) {
    $it = new RecursiveDirectoryIterator($cache_dir, RecursiveDirectoryIterator::SKIP_DOTS);
    foreach (new RecursiveIteratorIterator($it, RecursiveIteratorIterator::CHILD_FIRST) as $f) {
        $f->isDir() ? rmdir($f) : unlink($f);
    }
}
wp_cache_flush();
delete_transient('trp_cache_languages');
return ['ok' => true];
""")
    print("Done!")


if __name__ == "__main__":
    run()
