#!/usr/bin/env python3
"""
seed_translations_patch2.py
Adds remaining missing translations identified from live /es/ pages.
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
    # ── HOME ──
    ("About Our Team", "Sobre Nuestro Equipo"),

    # ── INCOME TAX ──
    # Note: curly apostrophe in "we'll" is Unicode U+2019, not &rsquo;
    ("Tell us about your filing situation and we’ll follow up the same business day.",
     "Cuéntanos sobre tu situación de declaración y te responderemos el mismo día hábil."),
    # Straight apostrophe variant (WPForms may render either)
    ("Tell us about your filing situation and we'll follow up the same business day.",
     "Cuéntanos sobre tu situación de declaración y te responderemos el mismo día hábil."),
    ("Please enable JavaScript in your browser to complete this form.",
     "Por favor habilita JavaScript en tu navegador para completar este formulario."),

    # ── ABOUT ──
    ("We started this firm right here in Fresno because we believe our neighbors deserve a tax preparer who actually knows them — someone who picks up the phone in July when an IRS letter shows up, not just in March when a refund is on the line. Our roots are in this community. We shop where you shop, our kids go to the same schools, and we understand the real financial pressures Central Valley families face.",
     "Fundamos esta firma aquí mismo en Fresno porque creemos que nuestros vecinos merecen un preparador de impuestos que realmente los conozca — alguien que conteste el teléfono en julio cuando llega una carta del IRS, no solo en marzo cuando hay un reembolso en juego. Nuestras raíces están en esta comunidad. Compramos donde tú compras, nuestros hijos van a las mismas escuelas y entendemos las presiones financieras reales que enfrentan las familias del Valle Central."),
    ("What We Stand For", "Lo Que Defendemos"),
    ("We stand behind every return we prepare. If we make an error, we make it right — covering the adjustment costs and amending your return at no charge.",
     "Respaldamos cada declaración que preparamos. Si cometemos un error, lo corregimos — cubriendo los costos de ajuste y enmendando tu declaración sin cargo."),
    ("We explain your return in plain language, and offer both in-person and secure virtual tax preparation — so getting your taxes done right fits into your life.",
     "Explicamos tu declaración en lenguaje sencillo y ofrecemos preparación de impuestos tanto en persona como virtual y segura — para que hacer tus impuestos correctamente se adapte a tu vida."),
    (", [a Fresno local / lifelong Central Valley resident] with a passion for helping working families and small business owners keep more of what they earn.",
     ", [un residente local de Fresno / residente de toda la vida del Valle Central] con pasión por ayudar a las familias trabajadoras y propietarios de pequeños negocios a conservar más de lo que ganan."),
    ("Beyond tax preparation, our team is [certified/registered] to provide notary public services, loan signing support, and Live Scan fingerprinting — making us a true one-stop compliance resource for local startups, caregivers, and real estate professionals.",
     "Más allá de la preparación de impuestos, nuestro equipo está [certificado/registrado] para proporcionar servicios de notaría pública, apoyo en firma de préstamos y huellas dactilares Live Scan — convirtiéndonos en un verdadero recurso integral de cumplimiento para startups locales, cuidadores y profesionales de bienes raíces."),
    ("[Certified Acceptance Agent status for ITIN applications]",
     "[Estatus de Agente Aceptador Certificado para solicitudes de ITIN]"),
    ("We know what keeps you up at night during tax season:",
     "Sabemos lo que te quita el sueño durante la temporada de impuestos:"),
    ("Did I miss a deduction? Is this preparer going to disappear if the IRS sends me a letter? Am I being overcharged?",
     "¿Perdí una deducción? ¿Este preparador va a desaparecer si el IRS me manda una carta? ¿Me están cobrando de más?"),
    ("And because we also offer notary and Live Scan fingerprinting services under the same roof, many of our clients discover we can handle far more than just their taxes.",
     "Y porque también ofrecemos servicios de notaría y huellas dactilares Live Scan bajo el mismo techo, muchos de nuestros clientes descubren que podemos manejar mucho más que solo sus impuestos."),
    ("Serving the Central Valley", "Sirviendo al Valle Central"),
    ("Get in Touch", "Contáctanos"),
    ("Schedule Your Appointment", "Programa Tu Cita"),

    # ── NOTARY ──
    ("Book Your Appointment", "Reserva Tu Cita"),
    ("Documents We Handle", "Documentos que Manejamos"),
    ("Power of Attorney", "Poder Notarial"),
    ("For loan signings, we follow lender and title company instructions to the letter. Bank documents, deeds, refinance packets, powers of attorney, and legal forms all get the same careful, page-by-page review, with a clean notary journal kept on every transaction.",
     "Para firmas de préstamos, seguimos las instrucciones del prestamista y la compañía de títulos al pie de la letra. Documentos bancarios, escrituras, paquetes de refinanciamiento, poderes notariales y formularios legales reciben la misma revisión cuidadosa página por página, con un diario notarial limpio en cada transacción."),
    ("We tell you exactly what to bring", "Te decimos exactamente qué traer"),
    ("We confirm every name matches and every signature lands exactly where it belongs.",
     "Confirmamos que cada nombre coincida y que cada firma quede exactamente donde corresponde."),
    # Unicode dashes/apostrophes in this string
    ("Deadlines Don’t Wait — Let’s Get It Signed, Sealed, and Off Your Plate",
     "Los Plazos No Esperan — Firmemos, Sellemos y Quitemos Eso de Tu Plato"),
    # Also try straight apostrophe variant
    ("Deadlines Don't Wait — Let's Get It Signed, Sealed, and Off Your Plate",
     "Los Plazos No Esperan — Firmemos, Sellemos y Quitemos Eso de Tu Plato"),
    ("Tell us what needs notarizing and when — we’ll follow up the same business day.",
     "Cuéntanos qué necesita notarización y cuándo — te responderemos el mismo día hábil."),
    ("Tell us what needs notarizing and when — we'll follow up the same business day.",
     "Cuéntanos qué necesita notarización y cuándo — te responderemos el mismo día hábil."),
    ("📷 Close-up of hands signing a real estate loan document with a notary seal visible.",
     "📷 Primer plano de manos firmando un documento de préstamo de bienes raíces con un sello notarial visible."),

    # ── LIVESCAN ──
    ("Walk In Today", "Entra Hoy"),
    ("What We Offer", "Lo Que Ofrecemos"),
    ("We check your form first", "Revisamos tu formulario primero"),
    ("A wrong ORI code or missing applicant type gets caught before it costs you a rejection.",
     "Un código ORI incorrecto o un tipo de solicitante faltante se detecta antes de que te cueste un rechazo."),
    ("Don’t Let Fingerprinting Hold Up Your Job, License, or Certification",
     "No Dejes que las Huellas Dactilares Retrasen Tu Trabajo, Licencia o Certificación"),
    ("Don't Let Fingerprinting Hold Up Your Job, License, or Certification",
     "No Dejes que las Huellas Dactilares Retrasen Tu Trabajo, Licencia o Certificación"),
    ("Walk In or Book Ahead", "Entra Sin Cita o Reserva con Anticipación"),
    ("Tell us what your fingerprints are for and we’ll confirm what to bring.",
     "Cuéntanos para qué son tus huellas y confirmaremos qué traer."),
    ("Tell us what your fingerprints are for and we'll confirm what to bring.",
     "Cuéntanos para qué son tus huellas y confirmaremos qué traer."),
    ("📷 Close-up of a completed FD-258 fingerprint card next to a Livescan request form.",
     "📷 Primer plano de una tarjeta de huellas FD-258 completada junto a un formulario de solicitud Livescan."),
    ("📷 Exterior shot of the Fresno office with signage, or a map graphic of Central Valley service areas.",
     "📷 Foto exterior de la oficina de Fresno con letreros, o un gráfico de mapa de las áreas de servicio del Valle Central."),

    # ── CONTACT ──
    ("Getting in touch is easy. Fill out the form, or pick whatever works best for you below.",
     "Ponerse en contacto es fácil. Llena el formulario o elige lo que mejor te funcione a continuación."),
    ("Not sure which documents you need? Wondering about an extension? Just ask.",
     "¿No estás seguro de qué documentos necesitas? ¿Tienes dudas sobre una extensión? Solo pregunta."),
    ("Get upfront, honest pricing for your tax preparation before we file a thing.",
     "Obtén precios honestos y transparentes para tu preparación de impuestos antes de que declaremos nada."),
    ("Need a document notarized or Live Scan fingerprints for a job or license? We can usually get you in quickly.",
     "¿Necesitas un documento notarizado o huellas dactilares Live Scan para un trabajo o licencia? Generalmente podemos atenderte rápidamente."),
    ("Your Trusted Local Team", "Tu Equipo Local de Confianza"),
    ("Proudly Serving the Central Valley", "Sirviendo con Orgullo al Valle Central"),

    # ── SHARED / MISC ──
    ("Fully credentialed and locally owned in Fresno — your neighbors, not a national chain.",
     "Completamente acreditados y de propiedad local en Fresno — tus vecinos, no una cadena nacional."),
    ("Fully credentialed and locally owned in Fresno — your neighbors, not a national chain.",
     "Completamente acreditados y de propiedad local en Fresno — tus vecinos, no una cadena nacional."),
    ("100% Accuracy Guarantee", "Garantía de Precisión al 100%"),
    ("Se Habla Español", "Se Habla Español"),
    ("Virtual Tax Preparation Available", "Preparación de Impuestos Virtual Disponible"),
    ("In-Person &amp; Virtual", "En Persona y Virtual"),
    ("In-Person and Virtual", "En Persona y Virtual"),
    ("Year-Round Support", "Apoyo Durante Todo el Año"),
    ("Upfront Pricing", "Precios Transparentes"),
    ("Free Consultation", "Consulta Gratuita"),
    ("Tax Season Ready", "Listo para la Temporada de Impuestos"),
    ("About Our Team", "Sobre Nuestro Equipo"),
    ("Meet Our Team", "Conoce a Nuestro Equipo"),
    ("Get Started Today", "Comienza Hoy"),
    ("Book a Free Consultation", "Reserva una Consulta Gratuita"),
    ("Request an Appointment", "Solicita una Cita"),
    ("View All Services", "Ver Todos los Servicios"),
    ("Back to Top", "Volver Arriba"),
    ("Privacy Policy", "Política de Privacidad"),
    ("Terms of Service", "Términos de Servicio"),
    ("All Rights Reserved", "Todos los Derechos Reservados"),
    ("Fresno, CA", "Fresno, CA"),
    ("Central Valley", "Valle Central"),
    ("Tax Preparation Services", "Servicios de Preparación de Impuestos"),
    ("Professional Tax Services", "Servicios Profesionales de Impuestos"),
    ("IRS Notice Support", "Apoyo con Avisos del IRS"),
    ("Prior Year Returns", "Declaraciones de Años Anteriores"),
    ("Tax Amendment", "Enmienda Fiscal"),
    ("Tax Extension", "Extensión Fiscal"),
    ("Business Tax", "Impuestos Empresariales"),
    ("Personal Tax", "Impuestos Personales"),
    ("Corporate Tax", "Impuestos Corporativos"),
    ("Notary Public", "Notario Público"),
    ("Loan Signing Agent", "Agente de Firma de Préstamos"),
    ("Live Scan Fingerprinting", "Huellas Dactilares Live Scan"),
    ("Background Check", "Verificación de Antecedentes"),
    ("ITIN Application", "Solicitud de ITIN"),
    ("Virtual Appointment", "Cita Virtual"),
    ("In-Person Appointment", "Cita en Persona"),
    ("Upload Documents", "Subir Documentos"),
    ("Secure Upload", "Carga Segura"),
    ("File Online", "Declarar en Línea"),
    ("Get Your Refund", "Obtén Tu Reembolso"),
    ("Maximize Your Refund", "Maximiza Tu Reembolso"),
    ("Tax Return", "Declaración de Impuestos"),
    ("W-2", "W-2"),
    ("1099", "1099"),
    ("Schedule E", "Schedule E"),
    ("Schedule C", "Schedule C"),
    ("LLC", "LLC"),
    ("S-Corp", "S-Corp"),
    ("C-Corp", "C-Corp"),
    ("Sole Proprietor", "Propietario Único"),
    ("Partnership", "Sociedad"),
    ("Corporation", "Corporación"),
]


def run():
    print(f"Total pairs to add: {len(MISSING)}\n")

    batch_size = 25
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

    # Clear all caches
    php("""
if (function_exists('breeze_clear_all_cache')) breeze_clear_all_cache();
$cache_dir = WP_CONTENT_DIR . '/cache/breeze/';
if (is_dir($cache_dir)) {
    $it = new RecursiveDirectoryIterator($cache_dir, RecursiveDirectoryIterator::SKIP_DOTS);
    foreach (new RecursiveIteratorIterator($it, RecursiveIteratorIterator::CHILD_FIRST) as $f) {
        $f->isFile() ? unlink($f->getRealPath()) : rmdir($f->getRealPath());
    }
}
wp_cache_flush();
global $wpdb;
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_trp%'");
return ['ok' => true];
""")
    print("Caches cleared. Done!")


if __name__ == "__main__":
    run()
