#!/usr/bin/env python3
"""
seed_translations_patch3.py
Adds remaining English strings found on /es/ pages after patch2.
Uses INSERT-if-not-exists to preserve existing records.
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

MISSING = [
    # ── ABOUT ──
    ("Honesty", "Honestidad"),
    ("Accuracy", "Precisión"),
    ("Accessibility", "Accesibilidad"),
    ("Let&#8217;s Talk — We&#8217;d Love to Meet You",
     "Hablemos — Nos Encantaría Conocerte"),
    ("Notary public services &amp; loan signing support",
     "Servicios de notaría pública y apoyo para firma de préstamos"),
    ("ITIN application support", "Apoyo para solicitudes de ITIN"),
    ("Bilingual-friendly service", "Servicio bilingüe disponible"),
    ("Local &amp; Family-Focused", "Local y Enfocado en la Familia"),
    ("If you&#8217;ve been searching for Fresno tax preparation that actually feels personal, we&#8217;d love to be the last search you make. Come by for a friendly, no-pressure conversation about your taxes, your business, or your goals for next year — no jargon, no surprises, just honest help from people who genuinely care.",
     "Si has estado buscando preparación de impuestos en Fresno que realmente se sienta personal, nos encantaría ser la última búsqueda que hagas. Ven para una conversación amistosa y sin presión sobre tus impuestos, tu negocio o tus metas para el próximo año — sin jerga, sin sorpresas, solo ayuda honesta de personas que genuinamente se preocupan."),
    ("These aren&#8217;t just words on a website. They show up in the small things: answering questions patiently, being available year-round, and never treating you like a number in a queue. Because to us, you&#8217;re not a transaction — you&#8217;re a neighbor.",
     "Estas no son solo palabras en un sitio web. Se reflejan en las cosas pequeñas: responder preguntas con paciencia, estar disponibles todo el año y nunca tratarte como un número en una cola. Porque para nosotros, no eres una transacción — eres un vecino."),
    ("Upfront, transparent pricing — you&#8217;ll know exactly what your Fresno tax preparation will cost before we ever file, with no surprise tiers or hidden percentages.",
     "Precios transparentes por adelantado — sabrás exactamente cuánto costará tu preparación de impuestos en Fresno antes de que declaremos nada, sin niveles sorpresa ni porcentajes ocultos."),
    ("When we&#8217;re not helping clients, you&#8217;ll find us involved in the community we serve — because being a good business means being a good neighbor.",
     "Cuando no estamos ayudando a clientes, nos encontrarás involucrados en la comunidad a la que servimos — porque ser un buen negocio significa ser un buen vecino."),
    ("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&amp;R Tax Services is ready when you are. Have a question? Just ask — that&#8217;s what neighbors are for.",
     "Sirviendo a Fresno, Clovis, Selma, Reedley, Sanger y Madera, C&amp;R Tax Services está listo cuando tú lo estés. ¿Tienes una pregunta? Solo pregunta — para eso están los vecinos."),
    ("Tax season shouldn&#8217;t feel like a guessing game — but for too many Central Valley families, that&#8217;s exactly what it is.",
     "La temporada de impuestos no debería sentirse como un juego de adivinanzas — pero para demasiadas familias del Valle Central, eso es exactamente lo que es."),

    # ── NOTARY ──
    ("Mobile Service Available", "Servicio Móvil Disponible"),
    ("Ask About Mobile Service", "Pregunta Sobre Servicio Móvil"),
    ("Bank Documents", "Documentos Bancarios"),
    ("Real Estate Documents &amp; Forms", "Documentos y Formularios de Bienes Raíces"),
    ("Legal Documents &amp; Forms", "Documentos y Formularios Legales"),
    ("Loan Signing Agent Services", "Servicios de Agente de Firma de Préstamos"),
    ("Every page, checked carefully", "Cada página, revisada cuidadosamente"),
    ("A clean notary journal, every time", "Un diario notarial limpio, cada vez"),
    ("📷 A friendly notary at a desk stamping a document while a smiling client looks on.",
     "📷 Un notario amable en un escritorio sellando un documento mientras un cliente sonriente observa."),

    # ── LIVESCAN ──
    ("DOJ-standard equipment", "Equipo con estándar DOJ"),
    ("Clear, upfront pricing", "Precios claros y transparentes"),
    ("Walk-Ins Welcome", "Se aceptan visitas sin cita"),
    ("Walk In Today", "Entra Hoy"),
    ("📷 Friendly technician guiding a client&#8217;s hand on a digital Livescan scanner.",
     "📷 Técnico amable guiando la mano de un cliente en un escáner digital de Livescan."),

    # ── CONTACT ──
    ("Request a Free Quote", "Solicita una Cotización Gratuita"),
    ("How to Reach Us", "Cómo Contactarnos"),
    ("After Hours — By Appointment Only", "Fuera de Horario — Solo con Cita"),
    ("General questions", "Preguntas generales"),
    ("Free quotes", "Cotizaciones gratuitas"),
    ("Get Help Now", "Obtén Ayuda Ahora"),
    ("Let&#8217;s Get Started Today", "Comencemos Hoy"),
    ("Real People, Fast Responses", "Personas Reales, Respuestas Rápidas"),
    ("Notary &amp; Live Scan appointments", "Citas de Notaría y Live Scan"),
    ("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we&#8217;re here after April 15th, not just before it.",
     "C&amp;R Tax Services es de propiedad y operación local, completamente acreditado y comprometido con la precisión en cada declaración — con apoyo durante todo el año, no solo en la temporada de impuestos. Respuestas reales de un equipo local — estamos aquí después del 15 de abril, no solo antes."),
    ("Got an IRS letter or a looming deadline? Call right away, and we&#8217;ll help you respond fast.",
     "¿Recibiste una carta del IRS o tienes un plazo inminente? Llama de inmediato y te ayudaremos a responder rápido."),
    ("Whatever brings you here, we&#8217;re happy to help.",
     "Cualquiera que sea el motivo de tu visita, estamos felices de ayudar."),
    ("January – April", "Enero – Abril"),
    ("May – December", "Mayo – Diciembre"),

    # ── SHARED / ALL PAGES ──
    ("Prefer to talk? Call us at", "¿Prefieres hablar? Llámanos al"),
    ("Send Message", "Enviar Mensaje"),
    ("What Clients Are Saying", "Lo Que Dicen Nuestros Clientes"),
    ("Ready to Maximize Your Return and Minimize Your Stress?",
     "¿Listo para Maximizar su Reembolso y Minimizar su Estrés?"),
    ("Get In Touch", "Contáctanos"),

    # ── NAV / FOOTER ──
    ("Contact Us", "Contáctanos"),
    ("Individual Taxes", "Impuestos Individuales"),
    ("Live Scan &amp; Notary", "Live Scan y Notaría"),
    ("Company", "Empresa"),
    ("Fresno Tax Blog", "Blog de Impuestos de Fresno"),
]


def run():
    print(f"Total pairs to add: {len(MISSING)}\n")

    batch_size = 20
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
        print(f"  Batch {n}: new={r.get('inserted','?') if r else 'ERR'} | err={r.get('err','?') if r else 'ERR'}")

    print(f"\nTotal newly inserted: {total}")

    r = php("global $wpdb; return ['count' => (int)$wpdb->get_var(\"SELECT COUNT(*) FROM {$wpdb->prefix}trp_dictionary_en_us_es_es WHERE status=1\")];")
    print(f"DB approved count: {r}")

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
