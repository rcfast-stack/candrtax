#!/usr/bin/env python3
"""
seed_translations_update.py
Updates all status=0 (TRP auto-detected) rows with translations and sets status=1.
Also does UPSERT for any new pairs not yet in the table.
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

# Complete translation map: original (exact HTML entity form) → Spanish translation
# If original is already Spanish or should stay as-is, translated = original
TRANSLATIONS = [
    # ABOUT
    ("Local &amp; Family-Focused", "Local y Enfocado en la Familia"),
    ("Tax season shouldn&#8217;t feel like a guessing game — but for too many Central Valley families, that&#8217;s exactly what it&#8217;s become.",
     "La temporada de impuestos no debería sentirse como un juego de adivinanzas — pero para demasiadas familias del Valle Central, eso es exactamente en lo que se ha convertido."),
    ("These aren&#8217;t just words on a website. They show up in the small things: answering questions patiently, being available year-round, and never treating you like a number in a queue. Because to us, you&#8217;re not a transaction — you&#8217;re a neighbor.",
     "Estas no son solo palabras en un sitio web. Se reflejan en las cosas pequeñas: responder preguntas con paciencia, estar disponibles todo el año y nunca tratarte como un número en una cola. Porque para nosotros, no eres una transacción — eres un vecino."),
    ("Honesty", "Honestidad"),
    ("Upfront, transparent pricing — you&#8217;ll know exactly what your Fresno tax preparation will cost before we ever file, with no surprise tiers or hidden percentages.",
     "Precios transparentes por adelantado — sabrás exactamente cuánto costará tu preparación de impuestos en Fresno antes de que declaremos nada, sin niveles sorpresa ni porcentajes ocultos."),
    ("Accuracy", "Precisión"),
    ("Accessibility", "Accesibilidad"),
    ("[Owner Name(s)]", "[Nombre(s) del Propietario]"),
    ("When we&#8217;re not helping clients, you&#8217;ll find us involved in the community we serve — because we&#8217;re not just building a business in Fresno, we&#8217;re building relationships that last well beyond tax season.",
     "Cuando no estamos ayudando a clientes, nos encontrarás involucrados en la comunidad a la que servimos — porque no solo estamos construyendo un negocio en Fresno, estamos construyendo relaciones que duran mucho más allá de la temporada de impuestos."),
    ("Notary public services &amp; loan signing support", "Servicios de notaría pública y apoyo para firma de préstamos"),
    ("Live Scan fingerprinting", "Huellas Dactilares Live Scan"),
    ("[CTEC registration]", "[Registro CTEC]"),
    ("[IRS PTIN]", "[IRS PTIN]"),
    ("[Commissioned notary / DOJ-certified Live Scan operator]", "[Notario comisionado / Operador de Livescan certificado por el DOJ]"),
    ("Bilingual-friendly service", "Servicio bilingüe disponible"),
    ("ITIN application support", "Apoyo para solicitudes de ITIN"),
    ("Secure virtual filing", "Declaración virtual segura"),
    ("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&amp;R Tax Services is ready when you are. Have a question? Just ask — that&#8217;s what neighbors are for.",
     "Sirviendo a Fresno, Clovis, Selma, Reedley, Sanger y Madera, C&amp;R Tax Services está listo cuando tú lo estés. ¿Tienes una pregunta? Solo pregunta — para eso están los vecinos."),
    # City names - keep as-is
    ("Fresno", "Fresno"),
    ("Clovis", "Clovis"),
    ("Selma", "Selma"),
    ("Reedley", "Reedley"),
    ("Sanger", "Sanger"),
    ("Madera", "Madera"),
    # CTA
    ("Let&#8217;s Talk — We&#8217;d Love to Meet You", "Hablemos — Nos Encantaría Conocerte"),
    ("If you&#8217;ve been searching for Fresno tax preparation that actually feels personal, we&#8217;d love to be the last search you make. Come by for a friendly, no-pressure conversation about your taxes, your business, or your goals for next year — no jargon, no surprises, just honest help from people who genuinely care.",
     "Si has estado buscando preparación de impuestos en Fresno que realmente se sienta personal, nos encantaría ser la última búsqueda que hagas. Ven para una conversación amistosa y sin presión sobre tus impuestos, tu negocio o tus metas para el próximo año — sin jerga, sin sorpresas, solo ayuda honesta de personas que genuinamente se preocupan."),
    ("Get in Touch", "Contáctanos"),
    # Contact info - keep as-is
    ("info@candrtaxservices.com", "info@candrtaxservices.com"),
    ("www.candrtaxservices.com", "www.candrtaxservices.com"),
    ("C&R Tax Services", "C&R Tax Services"),
    # Already Spanish - just approve them
    ("Selector de idioma del sitio web", "Selector de idioma del sitio web"),
    ("Idiomas disponibles", "Idiomas disponibles"),
    # NAV
    ("Individual Taxes", "Impuestos Individuales"),
    ("Small Business Taxes", "Impuestos para Pequeños Negocios"),
    ("Live Scan &amp; Notary", "Live Scan y Notaría"),
    ("Company", "Empresa"),
    ("Contact Us", "Contáctanos"),
    ("Secure Client Document Portal", "Portal Seguro de Documentos del Cliente"),
    ("Fresno Tax Blog", "Blog de Impuestos de Fresno"),
    # Income Tax long CTA
    ("The forms aren&#8217;t getting simpler and California&#8217;s rules aren&#8217;t getting easier. You deserve a friendly, local expert who does this every day, explains everything clearly, and guarantees the work. Call C&amp;R Tax Services to schedule your appointment, or send us a message below. Se habla español.",
     "Los formularios no se están simplificando y las reglas de California no se están facilitando. Mereces un experto local y amigable que haga esto todos los días, lo explique todo claramente y garantice el trabajo. Llama a C&amp;R Tax Services para programar tu cita o envíanos un mensaje a continuación. Se habla español."),
    ("Not sure / other", "No estoy seguro / otro"),
    ("Send Message", "Enviar Mensaje"),
    ("Prefer to talk? Call us at", "¿Prefieres hablar? Llámanos al"),
    ("you@example.com", "you@example.com"),
    ("Tell us a little about your situation...", "Cuéntanos un poco sobre tu situación..."),
    # NOTARY
    ("Mobile Service Available", "Servicio Móvil Disponible"),
    ("Ask About Mobile Service", "Pregunta Sobre Servicio Móvil"),
    ("Se habla espa&ntilde;ol.", "Se habla español."),
    ("📷 A friendly notary at a desk stamping a document while a smiling client looks on.",
     "📷 Un notario amable en un escritorio sellando un documento mientras un cliente sonriente observa."),
    ("Bank Documents", "Documentos Bancarios"),
    ("Travel Documents", "Documentos de Viaje"),
    ("Real Estate Documents &amp; Forms", "Documentos y Formularios de Bienes Raíces"),
    ("Legal Documents &amp; Forms", "Documentos y Formularios Legales"),
    ("Loan Signing Agent Services", "Servicios de Agente de Firma de Préstamos"),
    ("Every page, checked carefully", "Cada página, revisada cuidadosamente"),
    ("A clean notary journal, every time", "Un diario notarial limpio, cada vez"),
    ("Whether it&#8217;s a loan closing on the calendar, a power of attorney your family needs this week, or travel documents that must be certified before a flight, the fastest way to stop worrying is to get it done right, the first time. Call C&amp;R Tax Services today, or send us the details below and we&#8217;ll tell you exactly what to bring. Se habla español.",
     "Ya sea un cierre de préstamo en el calendario, un poder notarial que tu familia necesita esta semana o documentos de viaje que deben ser certificados antes de un vuelo, la forma más rápida de dejar de preocuparte es hacerlo bien desde la primera vez. Llama a C&amp;R Tax Services hoy o envíanos los detalles a continuación y te diremos exactamente qué traer. Se habla español."),
    # CONTACT
    ("Real People, Fast Responses", "Personas Reales, Respuestas Rápidas"),
    ("Request a Free Quote", "Solicita una Cotización Gratuita"),
    ("How to Reach Us", "Cómo Contactarnos"),
    ("Send Us a Message", "Envíanos un Mensaje"),
    ("January – April", "Enero – Abril"),
    ("Monday – Saturday", "Lunes – Sábado"),
    ("9am – 7pm", "9am – 7pm"),
    ("10am – 6pm", "10am – 6pm"),
    ("After Hours — By Appointment Only", "Fuera de Horario — Solo con Cita"),
    ("May – December", "Mayo – Diciembre"),
    ("Monday – Friday", "Lunes – Viernes"),
    ("Saturday – Sunday", "Sábado – Domingo"),
    ("¡Se habla español!", "¡Se habla español!"),
    ("Ask your questions in the language you&#8217;re most comfortable with. No pressure, no obligation — just honest help.",
     "Haz tus preguntas en el idioma en el que te sientas más cómodo. Sin presión, sin obligación — solo ayuda honesta."),
    ("Why Reach Out?", "¿Por Qué Contactarnos?"),
    ("Whatever brings you here, we&#8217;re happy to help.", "Cualquiera que sea el motivo de tu visita, estamos felices de ayudar."),
    ("General questions", "Preguntas generales"),
    ("Free quotes", "Cotizaciones gratuitas"),
    ("Urgent tax matters", "Asuntos fiscales urgentes"),
    ("Got an IRS letter or a looming deadline? Call right away, and we&#8217;ll help you respond fast.",
     "¿Recibiste una carta del IRS o tienes un plazo inminente? Llama de inmediato y te ayudaremos a responder rápido."),
    ("Notary &amp; Live Scan appointments", "Citas de Notaría y Live Scan"),
    ("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we&#8217;re here after April 15th, not just before it.",
     "C&amp;R Tax Services es de propiedad y operación local, completamente acreditado y comprometido con la precisión en cada declaración — con apoyo durante todo el año, no solo en la temporada de impuestos. Respuestas reales de un equipo local — estamos aquí después del 15 de abril, no solo antes."),
    ("Let&#8217;s Get Started Today", "Comencemos Hoy"),
    ("Get Help Now", "Obtén Ayuda Ahora"),
    # LIVESCAN
    ("Walk-Ins Welcome", "Se aceptan visitas sin cita"),
    ("se habla espa&ntilde;ol", "se habla español"),
    ("📷 Friendly technician guiding a client&#8217;s hand on a digital Livescan scanner.",
     "📷 Técnico amable guiando la mano de un cliente en un escáner digital de Livescan."),
    ("Livescan Background Checks", "Verificaciones de Antecedentes Livescan"),
    ("FD-258 Fingerprint Cards", "Tarjetas de Huellas Dactilares FD-258"),
    ("DOJ-standard equipment", "Equipo con estándar DOJ"),
    ("Clear, upfront pricing", "Precios claros y transparentes"),
    ("Rejected prints and wrong forms can set your plans back by weeks, and almost all of those delays are avoidable. Call us, stop by our Fresno office, or send us your details below. Walk-ins are welcome — just bring your request form and a valid photo ID. ¡Se habla español! Llámenos hoy.",
     "Las huellas rechazadas y los formularios incorrectos pueden retrasar tus planes por semanas, y casi todos esos retrasos son evitables. Llámanos, pasa por nuestra oficina en Fresno o envíanos tus datos a continuación. Se aceptan visitas sin cita — solo trae tu formulario de solicitud y una identificación con foto válida. ¡Se habla español! Llámenos hoy."),
]


def run():
    print(f"Total pairs to upsert: {len(TRANSLATIONS)}\n")

    batch_size = 20
    total_inserted = 0
    total_updated = 0

    for i in range(0, len(TRANSLATIONS), batch_size):
        batch = TRANSLATIONS[i:i+batch_size]
        pairs_json = json.dumps([[en, es] for en, es in batch], ensure_ascii=False)
        pairs_json_esc = pairs_json.replace("'", "\\'")
        code = f"""
global $wpdb;
$pairs = json_decode('{pairs_json_esc}', true);
$inserted = 0; $updated = 0;
foreach ($pairs as $pair) {{
    $existing = $wpdb->get_row($wpdb->prepare(
        "SELECT id, status FROM {{$wpdb->prefix}}trp_dictionary_en_us_es_es WHERE original = %s LIMIT 1",
        $pair[0]
    ), ARRAY_A);
    if ($existing) {{
        // Update translation and approve
        $r = $wpdb->update(
            $wpdb->prefix . 'trp_dictionary_en_us_es_es',
            ['translated' => $pair[1], 'status' => 1],
            ['id' => $existing['id']],
            ['%s', '%d'],
            ['%d']
        );
        if ($r !== false) $updated++;
    }} else {{
        $r = $wpdb->insert(
            $wpdb->prefix . 'trp_dictionary_en_us_es_es',
            ['original' => $pair[0], 'translated' => $pair[1], 'status' => 1, 'block_type' => 2],
            ['%s','%s','%d','%d']
        );
        if ($r !== false) $inserted++;
    }}
}}
return ['inserted' => $inserted, 'updated' => $updated, 'err' => $wpdb->last_error ?: 'none'];
"""
        r = php(code)
        total_inserted += r.get('inserted', 0) if r else 0
        total_updated += r.get('updated', 0) if r else 0
        n = i // batch_size + 1
        if r:
            print(f"  Batch {n}: inserted={r.get('inserted','?')} updated={r.get('updated','?')} | err={r.get('err','?')}")
        else:
            print(f"  Batch {n}: ERR")

    print(f"\nTotal inserted: {total_inserted}, updated: {total_updated}")

    r = php("""
global $wpdb;
$s0 = (int)$wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}trp_dictionary_en_us_es_es WHERE status=0");
$s1 = (int)$wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}trp_dictionary_en_us_es_es WHERE status=1");
return ['status0' => $s0, 'status1' => $s1];
""")
    print(f"DB status counts: {r}")

    # Purge Varnish + clear all caches
    php("""
$varnish_ip = '127.0.0.1';
$varnish_port = 8080;
$host = parse_url(get_site_url(), PHP_URL_HOST);
$socket = @fsockopen($varnish_ip, $varnish_port, $errno, $errstr, 5);
if ($socket) {
    fwrite($socket, "PURGE / HTTP/1.1\\r\\nHost: {$host}\\r\\nX-Purge-Method: regex\\r\\nX-Purge-Regex: .*\\r\\nConnection: Close\\r\\n\\r\\n");
    fread($socket, 500);
    fclose($socket);
}
if (function_exists('breeze_clear_all_cache')) breeze_clear_all_cache();
wp_cache_flush();
global $wpdb;
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_trp%'");
return ['ok' => true];
""")
    print("Varnish purged and caches cleared. Done!")


if __name__ == "__main__":
    run()
