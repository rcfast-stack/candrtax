#!/usr/bin/env python3
"""
seed_translations_v3.py
Re-seeds TRP dictionary using exact HTML entity strings from rendered pages.
TRP PHP translator matches raw HTML output, so source strings must use entities
(&rsquo; &mdash; &amp; etc.) exactly as they appear in the page HTML.
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
    # Response: {"success":true, "data":{"success":true, "return_value":{...}}}
    data = parsed.get("data", parsed)
    return data.get("return_value", data)

# ─────────────────────────────────────────────────
# Translation pairs: (english_source_as_in_html, spanish_translation)
# Source strings use HTML entities exactly as found in rendered page HTML.
# Spanish translations use plain Unicode (will be inserted as-is).
# ─────────────────────────────────────────────────
TRANSLATIONS = [

    # ── SITE-WIDE / HEADER ──
    ("C&amp;R Tax Services",
     "C&amp;R Tax Services"),  # brand name – keep as-is

    ("Fresno &amp; the Central Valley",
     "Fresno y el Valle Central"),

    ("Llame al (559) 962-7503",
     "Llame al (559) 962-7503"),

    ("Language Switcher",
     "Cambiar Idioma"),

    # ── HOME PAGE ──
    ("Tax Season Doesn&rsquo;t Have to Be Stressful.",
     "La Temporada de Impuestos No Tiene Que Ser Estresante."),

    ("Accurate, dependable income tax preparation for individuals, small businesses, and corporations across Fresno and the Central Valley &mdash; offered in person or fully virtual, in English or Spanish.",
     "Preparación de impuestos precisa y confiable para individuos, pequeños negocios y corporaciones en Fresno y el Valle Central — en persona o completamente virtual, en inglés o español."),

    ("Tax season has a way of sneaking up on you. One day life is moving along just fine, and the next you&rsquo;re sitting at the kitchen table with a stack of W-2s, 1099s, and maybe a letter from the IRS, wondering if you&rsquo;re missing something. If you&rsquo;ve ever felt that knot in your stomach in early spring, you&rsquo;re in good company.",
     "La temporada de impuestos tiene una manera de sorprenderte. Un día la vida va bien, y al siguiente estás sentado en la mesa de la cocina con una pila de W-2, 1099 y quizás una carta del IRS, preguntándote si te estás perdiendo algo. Si alguna vez has sentido ese nudo en el estómago a principios de la primavera, no estás solo."),

    ("At C&amp;R Tax Services, our job is to take that weight off your shoulders &mdash; with careful, personal attention on every return, and complete tax preparation available in Spanish.",
     "En C&amp;R Tax Services, nuestro trabajo es quitarte ese peso de los hombros — con atención cuidadosa y personal en cada declaración, y preparación completa de impuestos disponible en español."),

    ("Upload Your Docs &mdash; Virtual Prep",
     "Sube tus Documentos — Preparación Virtual"),

    ("Our Featured Tax &amp; Business Services",
     "Nuestros Servicios Destacados de Impuestos y Negocios"),

    ("We do it differently. At C&amp;R Tax Services, we sit down with you, in person or virtually, and walk through your full financial picture together, and make sure every credit and deduction you&rsquo;re entitled to actually lands on your return.",
     "Lo hacemos diferente. En C&amp;R Tax Services, nos sentamos contigo, en persona o virtualmente, y revisamos juntos tu panorama financiero completo, asegurándonos de que cada crédito y deducción al que tienes derecho realmente aparezca en tu declaración."),

    ("If you own rental property, we dig even deeper &mdash; Schedule E filings, depreciation, and the rules around passive income, tracked carefully so your rental income works for you instead of against you.",
     "Si tienes propiedades de alquiler, profundizamos aún más — formularios Schedule E, depreciación y las reglas sobre ingresos pasivos, rastreados cuidadosamente para que tu ingreso de alquiler trabaje a tu favor y no en tu contra."),

    ("&#10003; Virtual/Online Tax Preparation &ndash; Available Any Day and All Year!",
     "✓ Preparación de Impuestos Virtual/En Línea — ¡Disponible Cualquier Día y Todo el Año!"),

    ("Learn more about our Individual Tax Services &#10230;",
     "Conoce más sobre nuestros Servicios de Impuestos Individuales ⟶"),

    ("Running a business in the Central Valley is demanding enough without the IRS piling onto your to-do list. Between quarterly estimates, payroll questions, entity rules, and California&rsquo;s own layer of requirements, small business taxes can eat up hours you don&rsquo;t have.",
     "Dirigir un negocio en el Valle Central ya es suficientemente exigente sin que el IRS agregue más a tu lista de pendientes. Entre los estimados trimestrales, las preguntas de nómina, las reglas de entidades y la capa adicional de requisitos de California, los impuestos de pequeños negocios pueden consumir horas que no tienes."),

    ("C&amp;R Tax Services handles small business and corporate business taxes for sole proprietors, partnerships, LLCs, S-Corps, and C-Corps across Fresno &mdash; and if your business operates across state lines, our multi-state return experience keeps every jurisdiction squared away.",
     "C&amp;R Tax Services maneja los impuestos de pequeños negocios y corporaciones para propietarios únicos, sociedades, LLC, S-Corps y C-Corps en todo Fresno — y si tu negocio opera en varios estados, nuestra experiencia con declaraciones multi-estado mantiene cada jurisdicción en orden."),

    ("Learn more about our Business Tax Preparation &#10230;",
     "Conoce más sobre nuestra Preparación de Impuestos Empresariales ⟶"),

    ("If you don&rsquo;t have a Social Security number, filing taxes can feel like a door that&rsquo;s closed to you. It isn&rsquo;t. C&amp;R Tax Services provides professional support for ITIN applications, helping non-SSN filers in Fresno get the Individual Taxpayer Identification Number they need to file correctly and claim eligible credits.",
     "Si no tienes un número de Seguro Social, presentar impuestos puede sentirse como una puerta cerrada. No lo es. C&amp;R Tax Services brinda apoyo profesional para solicitudes de ITIN, ayudando a los contribuyentes sin SSN en Fresno a obtener el Número de Identificación Personal del Contribuyente que necesitan para declarar correctamente y reclamar los créditos elegibles."),

    ("We also prepare multi-state returns for anyone who earned income in more than one state &mdash; sorting out exactly what each state is owed so you never pay twice or file incorrectly.",
     "También preparamos declaraciones multi-estado para cualquiera que haya obtenido ingresos en más de un estado — determinando exactamente lo que cada estado requiere para que nunca pagues dos veces ni declares incorrectamente."),

    ("Learn more about ITIN &amp; Multi-State Services &#10230;",
     "Conoce más sobre los Servicios de ITIN y Multi-Estado ⟶"),

    ("Audit Services, Tax Extensions &amp; Amendments",
     "Servicios de Auditoría, Extensiones y Enmiendas Fiscales"),

    ("Few things ruin a week faster than an envelope from the IRS. C&amp;R Tax Services provides professional audit services and IRS notice support for taxpayers across the Fresno area &mdash; we read the notice with you and help you respond correctly and on time.",
     "Pocas cosas arruinan una semana más rápido que un sobre del IRS. C&amp;R Tax Services ofrece servicios profesionales de auditoría y apoyo con avisos del IRS para contribuyentes en el área de Fresno — leemos el aviso contigo y te ayudamos a responder correctamente y a tiempo."),

    ("&#10003; Audit Services",
     "✓ Servicios de Auditoría"),

    ("Learn more about Audit, Extension &amp; Amendment Services &#10230;",
     "Conoce más sobre los Servicios de Auditoría, Extensión y Enmienda ⟶"),

    ("Taxes aren&rsquo;t the only paperwork life throws your way. C&amp;R Tax Services also serves Fresno as a Notary Public and Loan Signing Agent and provides Live Scan fingerprint services &mdash; a convenient one-stop shop for the documents and verifications that keep your life and business moving.",
     "Los impuestos no son el único papeleo que la vida te presenta. C&amp;R Tax Services también sirve a Fresno como Notario Público y Agente de Firma de Préstamos, y ofrece servicios de huellas dactilares Live Scan — una conveniente ventanilla única para los documentos y verificaciones que mantienen tu vida y negocio en movimiento."),

    ("&#10003; Power of Attorney",
     "✓ Poder Notarial"),

    ("Mobile Services available upon request &ndash; Travel fees will be applied.",
     "Servicios Móviles disponibles bajo solicitud — Se aplicarán tarifas de desplazamiento."),

    ("Learn more about Notary &amp; Live Scan Services &#10230;",
     "Conoce más sobre los Servicios de Notaría y Live Scan ⟶"),

    ('alt: &ldquo;Tax preparation, notary public, and Live Scan fingerprint services in Fresno&rdquo;',
     'alt: "Preparación de impuestos, notario público y servicios de huellas dactilares Live Scan en Fresno"'),

    ("Why Fresno Trusts C&amp;R Tax Services",
     "Por Qué Fresno Confía en C&amp;R Tax Services"),

    ("There&rsquo;s no shortage of ways to get your taxes done in Fresno. Big-box franchises pop up every January, and online software promises easy filing in minutes. So why do local families and business owners keep choosing C&amp;R Tax Services? Because we offer something those options can&rsquo;t: a real, local professional who knows your name, answers your questions honestly, and treats your return like it matters. Because it does.",
     "No faltan opciones para hacer tus impuestos en Fresno. Las franquicias aparecen cada enero y el software en línea promete una declaración fácil en minutos. ¿Por qué entonces las familias locales y propietarios de negocios siguen eligiendo C&amp;R Tax Services? Porque ofrecemos algo que esas opciones no pueden: un profesional local real que conoce tu nombre, responde tus preguntas honestamente y trata tu declaración como si importara. Porque importa."),

    ("We also believe in doing business the straightforward way: upfront, transparent pricing, accuracy you can count on, and year-round support. With us, you&rsquo;re never a ticket number in a queue. You&rsquo;re a neighbor, and we treat you like one.",
     "También creemos en hacer negocios de manera directa: precios claros y transparentes, precisión en la que puedes confiar y apoyo durante todo el año. Con nosotros, nunca eres un número en una cola. Eres un vecino, y te tratamos como tal."),

    ("The C&amp;R team (or preparer) greeting a multigenerational local family at the office entrance, handshake or warm welcome moment.",
     "El equipo de C&amp;R (o preparador) saludando a una familia local multigeneracional en la entrada de la oficina, apretón de manos o momento de bienvenida cálida."),

    ("Proudly Serving Fresno &amp; the Central Valley",
     "Sirviendo con Orgullo a Fresno y el Valle Central"),

    ("C&amp;R Tax Services is based in Fresno, and our roots here run deep. But our service area reaches well beyond one zip code. We proudly provide income tax preparation, ITIN applications, business tax services, notary work, and Live Scan fingerprinting to families and businesses throughout the Central Valley.",
     "C&amp;R Tax Services está ubicado en Fresno y nuestras raíces aquí son profundas. Pero nuestra área de servicio se extiende mucho más allá de un código postal. Con orgullo ofrecemos preparación de impuestos, solicitudes de ITIN, servicios de impuestos empresariales, notaría y huellas dactilares Live Scan a familias y negocios en todo el Valle Central."),

    ("Ask around Fresno about what matters most in a tax preparer, and you&rsquo;ll hear the same answers again and again: patience, honesty, clear explanations, and getting every dollar you deserve. From first-time filers to business owners untangling multi-state returns, our clients tend to tell us the same thing: working with C&amp;R Tax Services made taxes feel simple for the first time.",
     "Pregunta en Fresno qué es lo más importante en un preparador de impuestos y escucharás las mismas respuestas una y otra vez: paciencia, honestidad, explicaciones claras y obtener cada dólar que mereces. Desde quienes declaran por primera vez hasta propietarios de negocios con declaraciones multi-estado, nuestros clientes suelen decirnos lo mismo: trabajar con C&amp;R Tax Services hizo que los impuestos se sintieran simples por primera vez."),

    ("Whether you need straightforward individual tax preparation, full small business and corporate tax support, help with an ITIN application, or a calm, fast answer to a scary IRS letter, C&amp;R Tax Services is ready, in English or Spanish, in our office or completely online.",
     "Ya sea que necesites una preparación de impuestos individual sencilla, soporte completo para impuestos de pequeños negocios y corporaciones, ayuda con una solicitud de ITIN o una respuesta tranquila y rápida a una carta atemorizante del IRS, C&amp;R Tax Services está listo, en inglés o español, en nuestra oficina o completamente en línea."),

    ("Tax season: January &ndash; April. After tax season: May &ndash; December.",
     "Temporada de impuestos: Enero – Abril. Después de la temporada: Mayo – Diciembre."),

    ("Tax Season (Jan &ndash; Apr)",
     "Temporada de Impuestos (Ene – Abr)"),

    ("After Tax Season (May &ndash; Dec)",
     "Fuera de Temporada (May – Dic)"),

    ("Stop by, call, or book a virtual appointment &mdash; we&rsquo;re here all year.",
     "Visítanos, llama o reserva una cita virtual — estamos aquí todo el año."),

    ("At C&amp;R Tax Services, numbers are the foundation of your family&rsquo;s and your business&rsquo;s financial peace of mind. Let our family protect yours this season.",
     "En C&amp;R Tax Services, los números son la base de la tranquilidad financiera de tu familia y tu negocio. Deja que nuestra familia proteja la tuya esta temporada."),

    ("&copy; 2026 C&amp;R Tax Services. All rights reserved.",
     "&copy; 2026 C&amp;R Tax Services. Todos los derechos reservados."),

    # ── INCOME TAX PAGE ──
    ("Income Tax &#8211; C&amp;R Tax Services",
     "Impuestos sobre la Renta &#8211; C&amp;R Tax Services"),

    ("The Best Tax Preparation in the Central Valley &mdash; Without the Stress, Surprises, or Confusing Fine Print",
     "La Mejor Preparación de Impuestos en el Valle Central — Sin Estrés, Sorpresas ni Letra Pequeña Confusa"),

    ("Full-service preparation for individuals, small businesses, and every filing situation in between &mdash; plus virtual and online tax preparation, available any day, all year.",
     "Preparación de servicio completo para individuos, pequeños negocios y cada situación de declaración — más preparación de impuestos virtual y en línea, disponible cualquier día, todo el año."),

    ("Tax season has a way of sneaking up on you. One day you&rsquo;re enjoying the holidays. The next, you&rsquo;re staring at a pile of W-2s, 1099s, and receipts, wondering if you&rsquo;re about to miss a deduction &mdash; or worse, make a mistake that brings a letter from the IRS. Families and business owners all over Fresno feel that knot in their stomach every year.",
     "La temporada de impuestos tiene una manera de sorprenderte. Un día estás disfrutando las fiestas. Al siguiente, estás mirando una pila de W-2, 1099 y recibos, preguntándote si estás a punto de perder una deducción — o peor, cometer un error que traiga una carta del IRS. Familias y propietarios de negocios en todo Fresno sienten ese nudo en el estómago cada año."),

    ("That&rsquo;s exactly why C&amp;R Tax Services exists. We&rsquo;re a local, bilingual tax preparation firm built to make filing simple, accurate, and honest. Whether you&rsquo;re filing a basic personal return, running a small business, managing rental properties, or applying for an ITIN, we walk you through every step in plain language &mdash; English or Spanish.",
     "Por eso exactamente existe C&amp;R Tax Services. Somos una firma local y bilingüe de preparación de impuestos creada para hacer la declaración simple, precisa y honesta. Ya sea que estés presentando una declaración personal básica, dirigiendo un pequeño negocio, administrando propiedades de alquiler o solicitando un ITIN, te guiamos en cada paso en lenguaje sencillo — inglés o español."),

    (", and we mean it. You&rsquo;ll never leave our office wondering what was filed or why.",
     ", y lo decimos en serio. Nunca saldrás de nuestra oficina preguntándote qué se declaró o por qué."),

    ("we file, not after &mdash; no hidden fees, no surprise upgrades. Our team is registered, meets every federal and California filing requirement, and stays open year-round. So when the IRS sends a letter in August, we&rsquo;re still here to help you answer it.",
     "antes de declarar, no después — sin tarifas ocultas ni actualizaciones sorpresa. Nuestro equipo está registrado, cumple con todos los requisitos federales y de California, y permanece abierto todo el año. Así que cuando el IRS envíe una carta en agosto, seguimos aquí para ayudarte a responderla."),

    ('alt: &ldquo;Bilingual tax preparation appointment at C&#038;R Tax Services in Fresno, CA&rdquo;',
     'alt: "Cita de preparación de impuestos bilingüe en C&R Tax Services en Fresno, CA"'),

    ("Most people don&rsquo;t call a tax professional when things are going smoothly. They call because something changed &mdash; a side business, a delivery-app job, a rental property in Clovis with a Schedule E they&rsquo;ve never filed, or a mid-year move to California that turned into a multi-state return their old software can&rsquo;t handle.",
     "La mayoría de las personas no llaman a un profesional de impuestos cuando todo va bien. Llaman porque algo cambió — un negocio secundario, un trabajo de entrega, una propiedad de alquiler en Clovis con un Schedule E que nunca han declarado, o una mudanza a mitad de año a California que se convirtió en una declaración multi-estado que su software antiguo no puede manejar."),

    ("For many Central Valley families, there&rsquo;s one more hurdle: filing without a Social Security number. As certified ITIN application specialists, we help non-SSN filers get set up correctly the first time. Whatever brought you here &mdash; a new business, a new property, a new country, or just a new season of life &mdash; accurate tax preparation is how you protect what you&rsquo;ve earned.",
     "Para muchas familias del Valle Central, hay un obstáculo más: declarar sin número de Seguro Social. Como especialistas certificados en solicitudes de ITIN, ayudamos a los declarantes sin SSN a configurarse correctamente desde la primera vez. Sea lo que sea que te trajo aquí — un nuevo negocio, una nueva propiedad, un nuevo país o simplemente una nueva etapa de vida — la preparación precisa de impuestos es cómo proteges lo que has ganado."),

    ('alt: &ldquo;Common situations that call for professional tax preparation in Fresno — self-employment, small business, and rental property taxes&rdquo;',
     'alt: "Situaciones comunes que requieren preparación profesional de impuestos en Fresno — trabajo por cuenta propia, pequeños negocios e impuestos de propiedades de alquiler"'),

    ("Virtual/Online Tax Preparation &ndash; Available Any Day and All Year!",
     "Preparación de Impuestos Virtual/En Línea — ¡Disponible Cualquier Día y Todo el Año!"),

    ("How C&amp;R Tax Services Does It Better",
     "Cómo C&amp;R Tax Services Lo Hace Mejor"),

    ("Big-box tax chains and DIY software treat you like a ticket number. We treat you like a neighbor, because you are one. Every return starts with a real conversation about your year &mdash; what changed, what you earned, what you&rsquo;re hoping to accomplish. From there, we build your return line by line, checking for every credit and deduction you legally qualify for, whether it&rsquo;s a simple individual return or a complex filing for a corporation, partnership, or LLC.",
     "Las cadenas de impuestos grandes y el software hazlo-tú-mismo te tratan como un número de ticket. Nosotros te tratamos como un vecino, porque lo eres. Cada declaración comienza con una conversación real sobre tu año — qué cambió, qué ganaste, qué esperas lograr. A partir de ahí, construimos tu declaración línea por línea, verificando cada crédito y deducción para la que calificas legalmente, ya sea una declaración individual simple o una presentación compleja para una corporación, sociedad o LLC."),

    ("We built this firm for the Central Valley &mdash; for the farm families, the small business owners, the young professionals, and the hardworking households that keep this region running. When you sit down with us, in person or online, you get local knowledge of California tax rules paired with the patience to actually explain them.",
     "Construimos esta firma para el Valle Central — para las familias de agricultores, los propietarios de pequeños negocios, los jóvenes profesionales y los hogares trabajadores que mantienen esta región en marcha. Cuando te sientas con nosotros, en persona o en línea, obtienes conocimiento local de las reglas fiscales de California combinado con la paciencia para explicarlas realmente."),

    ("You&rsquo;ll know your cost before we file. Period.",
     "Sabrás tu costo antes de que declaremos. Punto."),

    ('alt: &ldquo;Virtual tax preparation and secure document upload for Central Valley clients of C&#038;R Tax Services&rdquo;',
     'alt: "Preparación de impuestos virtual y carga segura de documentos para clientes del Valle Central de C&R Tax Services"'),

    ("Ask around the Central Valley and you&rsquo;ll hear the same words used to describe a great tax preparer: patient, thorough, honest about pricing, and focused on getting you every dollar you deserve. Clients tell us the biggest relief isn&rsquo;t just the refund &mdash; it&rsquo;s finally understanding their own taxes, and knowing nothing was missed or hidden.",
     "Pregunta por el Valle Central y escucharás las mismas palabras para describir a un gran preparador de impuestos: paciente, minucioso, honesto sobre los precios y enfocado en conseguirte cada dólar que mereces. Los clientes nos dicen que el mayor alivio no es solo el reembolso — es finalmente entender sus propios impuestos y saber que nada se pasó por alto ni se ocultó."),

    ("It&rsquo;s the small business owner who stopped dreading quarterly deadlines. It&rsquo;s the family who fixed a prior-year mistake and recovered money they didn&rsquo;t know they&rsquo;d lost. It&rsquo;s the ITIN applicant who filed correctly the first time instead of waiting months on a rejected application. When your taxes are done right, you get your time, your money, and your calm back.",
     "Es el dueño de un pequeño negocio que dejó de temer los plazos trimestrales. Es la familia que corrigió un error de años anteriores y recuperó dinero que no sabía que había perdido. Es el solicitante de ITIN que declaró correctamente la primera vez en lugar de esperar meses por una solicitud rechazada. Cuando tus impuestos se hacen bien, recuperas tu tiempo, tu dinero y tu tranquilidad."),

    ("C&amp;R Tax Services proudly serves families and business owners across Fresno, Clovis, Sanger, Selma, and Madera. We&rsquo;re not a seasonal pop-up that disappears the day after the deadline &mdash; we&rsquo;re a year-round Central Valley firm. When you get an IRS letter in July, need an extension in October, or want a prior-year review in November, our door is open and our phone gets answered.",
     "C&amp;R Tax Services sirve con orgullo a familias y propietarios de negocios en Fresno, Clovis, Sanger, Selma y Madera. No somos un negocio temporal que desaparece el día después del plazo — somos una firma del Valle Central disponible todo el año. Cuando recibes una carta del IRS en julio, necesitas una extensión en octubre o quieres una revisión de años anteriores en noviembre, nuestra puerta está abierta y nuestro teléfono se contesta."),

    ("Every return we prepare meets federal and California registration and compliance standards, and your documents are always handled through secure, protected channels &mdash; whether you file in person or through our virtual portal.",
     "Cada declaración que preparamos cumple con los estándares federales y de California de registro y cumplimiento, y tus documentos siempre se manejan a través de canales seguros y protegidos — ya sea que declares en persona o a través de nuestro portal virtual."),

    ('alt: &ldquo;C&#038;R Tax Services tax preparation service areas across the Central Valley including Fresno, Clovis, Sanger, Selma, and Madera&rdquo;',
     'alt: "Áreas de servicio de preparación de impuestos de C&R Tax Services en todo el Valle Central incluyendo Fresno, Clovis, Sanger, Selma y Madera"'),

    ("The forms aren't getting simpler and California's rules aren't getting easier. You deserve a friendly, local expert who does this every day, explains everything clearly, and guarantees the work. Call C&amp;R Tax Services to schedule your appointment, or send us a message below. Se habla español.",
     "Los formularios no se están simplificando y las reglas de California no se están volviendo más fáciles. Mereces un experto local y amigable que hace esto todos los días, explica todo claramente y garantiza el trabajo. Llama a C&amp;R Tax Services para programar tu cita, o envíanos un mensaje abajo. Se habla español."),

    # ── ABOUT PAGE ──
    ("About &#8211; C&amp;R Tax Services",
     "Nosotros &#8211; C&amp;R Tax Services"),

    ("Why We Started C&amp;R Tax Services",
     "Por Qué Fundamos C&amp;R Tax Services"),

    ("Tax season shouldn&#8217;t feel like a guessing game. But for too many families and small business owners here in the Central Valley, that&#8217;s exactly what it&#8217;s become — confusing software, pop-up franchise offices that disappear on April 16th, and preparers who rush you out the door without ever explaining what they filed on your behalf. C&amp;R Tax Services was founded to be the opposite of all that.",
     "La temporada de impuestos no debería sentirse como un juego de adivinanzas. Pero para demasiadas familias y propietarios de pequeños negocios aquí en el Valle Central, eso es exactamente en lo que se ha convertido — software confuso, oficinas de franquicias temporales que desaparecen el 16 de abril y preparadores que te sacan corriendo por la puerta sin explicar nunca qué presentaron en tu nombre. C&amp;R Tax Services fue fundado para ser todo lo contrario."),

    ("At its heart, C&amp;R Tax Services was built on a simple promise: treat every return like it belongs to family. Whether you&#8217;re filing a straightforward W-2, applying for an ITIN, or untangling a multi-state small business return, we want you to walk out of our office feeling something most people never associate with taxes — genuine peace of mind.",
     "En su esencia, C&amp;R Tax Services fue construido sobre una promesa simple: tratar cada declaración como si perteneciera a la familia. Ya sea que estés presentando un W-2 sencillo, solicitando un ITIN o desenredando una declaración de pequeño negocio multi-estado, queremos que salgas de nuestra oficina sintiendo algo que la mayoría nunca asocia con los impuestos — genuina tranquilidad."),

    ("Everything we do at C&amp;R Tax Services comes back to three values: honesty, accuracy, and accessibility. Taxes are stressful enough without feeling talked down to, so we take the time to explain your return in plain language — what you&#8217;re claiming, why it matters, and how to plan smarter for next year.",
     "Todo lo que hacemos en C&amp;R Tax Services vuelve a tres valores: honestidad, precisión y accesibilidad. Los impuestos ya son suficientemente estresantes sin sentir que te hablan con condescendencia, así que nos tomamos el tiempo de explicar tu declaración en lenguaje sencillo — qué estás reclamando, por qué importa y cómo planificar de manera más inteligente para el próximo año."),

    ("Meet the People Behind C&amp;R",
     "Conoce a las Personas Detrás de C&amp;R"),

    ("C&amp;R Tax Services is led by",
     "C&amp;R Tax Services es dirigido por"),

    ("Credentials &amp; Services",
     "Credenciales y Servicios"),

    ("Why Homeowners and Local Families Trust C&amp;R Tax Services",
     "Por Qué los Propietarios y Familias Locales Confían en C&amp;R Tax Services"),

    ("We built C&amp;R Tax Services specifically to put those fears to rest. Unlike seasonal franchise offices, we&#8217;re a local firm with year-round support — if a notice arrives in August, we&#8217;re here to handle it.",
     "Construimos C&amp;R Tax Services específicamente para poner esos miedos a descansar. A diferencia de las oficinas de franquicias de temporada, somos una firma local con apoyo durante todo el año — si llega un aviso en agosto, estamos aquí para manejarlo."),

    ("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&amp;R Tax Services is ready when you are. Have a question? Just ask — that&rsquo;s what neighbors are for.",
     "Sirviendo a Fresno, Clovis, Selma, Reedley, Sanger y Madera, C&amp;R Tax Services está listo cuando tú lo estés. ¿Tienes una pregunta? Solo pregunta — para eso son los vecinos."),

    # ── NOTARY PAGE ──
    ("Notary &#8211; C&amp;R Tax Services",
     "Notaría &#8211; C&amp;R Tax Services"),

    ("The Best Notary in the Central Valley &mdash; Fast, Friendly, and Right Here in Fresno",
     "El Mejor Notario en el Valle Central — Rápido, Amigable y Aquí Mismo en Fresno"),

    ("Certified notarization and loan signing for the documents that matter most &mdash; in-office or on the road.",
     "Notarización certificada y firma de préstamos para los documentos que más importan — en la oficina o en carretera."),

    ("The paperwork you&rsquo;ve been waiting on finally arrived &mdash; maybe a loan packet, a power of attorney, or travel consent forms for your kids. There&rsquo;s just one catch: none of it counts until it&rsquo;s notarized. Now you&rsquo;re stuck searching for someone who can do it right, do it soon, and not make you feel rushed or confused along the way.",
     "Los documentos que has estado esperando finalmente llegaron — quizás un paquete de préstamo, un poder notarial o formularios de consentimiento de viaje para tus hijos. Hay solo un inconveniente: nada de eso cuenta hasta que esté notarizado. Ahora estás buscando a alguien que pueda hacerlo bien, hacerlo pronto y no hacerte sentir apresurado ni confundido en el camino."),

    ("That&rsquo;s where C&amp;R Tax Services comes in. We&rsquo;re a local Fresno office offering notary public and loan signing agent services for bank documents, real estate paperwork, powers of attorney, travel documents, and legal forms of every kind. Because we&rsquo;re also a full tax preparation office, handling sensitive paperwork isn&rsquo;t a side gig for us &mdash; it&rsquo;s what we do all day, every day.",
     "Ahí es donde entra C&amp;R Tax Services. Somos una oficina local en Fresno que ofrece servicios de notario público y agente de firma de préstamos para documentos bancarios, papeleo de bienes raíces, poderes notariales, documentos de viaje y formularios legales de todo tipo. Como también somos una oficina completa de preparación de impuestos, manejar papeleo sensible no es un trabajo secundario para nosotros — es lo que hacemos todo el día, todos los días."),

    ("Our notaries are commissioned by the State of California, bonded, and trained to walk you through every signature and stamp. If Spanish is your first language, you&rsquo;re in the right place, too.",
     "Nuestros notarios están comisionados por el Estado de California, asegurados y capacitados para guiarte en cada firma y sello. Si el español es tu primer idioma, también estás en el lugar correcto."),

    ("You&rsquo;ll never have to guess what you&rsquo;re signing or bring a friend along to translate.",
     "Nunca tendrás que adivinar qué estás firmando ni traer un amigo para traducir."),

    ('alt: &ldquo;Fresno notary public notarizing legal documents for a local client at C&#038;R Tax Services&rdquo;',
     'alt: "Notario público de Fresno notarizando documentos legales para un cliente local en C&R Tax Services"'),

    ("Life has a way of handing you paperwork at the worst possible moments. Maybe you&rsquo;re closing on a home in Fresno or Clovis and the lender needs a certified loan signing agent before the deal can fund. Maybe a parent&rsquo;s health is declining and your family needs a power of attorney notarized this week, not next month. Or maybe your child is flying to visit family in Mexico, and the airline won&rsquo;t let them board without a notarized travel consent letter.",
     "La vida tiene una manera de entregarte papeleo en los peores momentos posibles. Quizás estás cerrando la compra de una casa en Fresno o Clovis y el prestamista necesita un agente certificado de firma de préstamos antes de que el trato pueda financiarse. Quizás la salud de un padre está deteriorándose y tu familia necesita un poder notarial notarizado esta semana, no el próximo mes. O quizás tu hijo vuela a visitar a la familia en México y la aerolínea no lo dejará abordar sin una carta de consentimiento de viaje notarizada."),

    ("These aren&rsquo;t rare situations. They&rsquo;re everyday moments for Central Valley families, and every one comes with a deadline. When a signature is missing or a stamp is done wrong, closings get delayed, court filings get rejected, and travel plans fall apart. A good notary does more than witness a signature &mdash; they protect you from expensive do-overs.",
     "Estas no son situaciones raras. Son momentos cotidianos para las familias del Valle Central, y cada uno viene con un plazo. Cuando falta una firma o un sello se hace mal, los cierres se retrasan, las presentaciones judiciales se rechazan y los planes de viaje se desmoronan. Un buen notario hace más que atestiguar una firma — te protege de costosas repeticiones."),

    ("Many of our notary clients first found us through our tax work, and that&rsquo;s no coincidence. The same people who need help with tax preparation in Fresno often need an ITIN form certified, a bank document witnessed, or real estate paperwork signed and sealed. Having one trusted local office for both means fewer trips and a lot less stress.",
     "Muchos de nuestros clientes de notaría nos encontraron primero a través de nuestro trabajo de impuestos, y eso no es coincidencia. Las mismas personas que necesitan ayuda con la preparación de impuestos en Fresno a menudo necesitan un formulario ITIN certificado, un documento bancario atestiguado o papeleo de bienes raíces firmado y sellado. Tener una oficina local de confianza para ambos significa menos viajes y mucho menos estrés."),

    ('alt: &ldquo;Loan signing agent in Fresno helping a homeowner complete real estate closing documents&rdquo;',
     'alt: "Agente de firma de préstamos en Fresno ayudando a un propietario a completar documentos de cierre de bienes raíces"'),

    ("How C&amp;R Tax Services Does It Better",
     "Cómo C&amp;R Tax Services Lo Hace Mejor"),

    ("Plenty of places in Fresno can stamp a document. What sets us apart is how we treat the person holding it. You call or book online, and we tell you exactly what to bring. When you arrive, we take our time &mdash; we check every page, confirm every name matches, and make sure each signature lands exactly where it belongs. One missed initial on a loan package can delay a closing by days, so we don&rsquo;t leave anything to chance.",
     "Muchos lugares en Fresno pueden sellar un documento. Lo que nos distingue es cómo tratamos a la persona que lo sostiene. Llamas o reservas en línea, y te decimos exactamente qué traer. Cuando llegas, nos tomamos nuestro tiempo — revisamos cada página, confirmamos que cada nombre coincida y nos aseguramos de que cada firma quede exactamente donde corresponde. Una inicial olvidada en un paquete de préstamo puede retrasar un cierre por días, así que no dejamos nada al azar."),

    ("Usually just a valid, unexpired photo ID and your unsigned documents &mdash; no guesswork.",
     "Generalmente solo una identificación con foto válida y vigente y tus documentos sin firmar — sin adivinar."),

    ("Kept on every transaction, just as California law requires, so there&rsquo;s always a record protecting you.",
     "Guardado en cada transacción, tal como lo requiere la ley de California, para que siempre haya un registro que te proteja."),

    ("We explain every signature and stamp clearly, in the language you&rsquo;re most comfortable with.",
     "Explicamos cada firma y sello claramente, en el idioma con el que te sientes más cómodo."),

    ("📷 Bilingual &#8216;Se Habla Español&#8217; signage in the office window, or a team member greeting a Spanish-speaking family.",
     "📷 Letrero bilingüe 'Se Habla Español' en la ventana de la oficina, o un miembro del equipo saludando a una familia de habla hispana."),

    ('alt: &ldquo;Bilingual notary services in Fresno — se habla español at C&#038;R Tax Services&rdquo;',
     'alt: "Servicios de notaría bilingüe en Fresno — se habla español en C&R Tax Services"'),

    ("The moments right after a notarization are often the best part of our job. We&rsquo;ve watched a daughter breathe a sigh of relief after finalizing a power of attorney, knowing she could finally manage her mother&rsquo;s care without one more legal roadblock. We&rsquo;ve seen first-time homebuyers walk out of a loan signing and tell us it was the first time in the entire process someone actually explained what they were signing.",
     "Los momentos justo después de una notarización son a menudo la mejor parte de nuestro trabajo. Hemos visto a una hija suspirar de alivio después de finalizar un poder notarial, sabiendo que finalmente podía gestionar el cuidado de su madre sin otro obstáculo legal. Hemos visto a compradores de casa por primera vez salir de una firma de préstamo y decirnos que fue la primera vez en todo el proceso que alguien realmente explicó lo que estaban firmando."),

    ("Clients across the Fresno area tell us the same things they say about our tax work: that we&rsquo;re patient, that we explain everything, and that we make stressful paperwork feel simple. When you leave our office, your documents are done right, and you know exactly what you signed.",
     "Los clientes del área de Fresno nos dicen lo mismo que dicen sobre nuestro trabajo de impuestos: que somos pacientes, que explicamos todo y que hacemos que el papeleo estresante se sienta simple. Cuando sales de nuestra oficina, tus documentos están bien hechos y sabes exactamente lo que firmaste."),

    ("C&amp;R Tax Services is proudly local. We serve families and business owners across Fresno, Clovis, Sanger, Selma, and Madera, and we&rsquo;re not a pop-up kiosk or an out-of-town chain. We&rsquo;re your neighbors, and our office stays open year-round &mdash; notary needs don&rsquo;t follow a calendar.",
     "C&amp;R Tax Services es orgullosamente local. Servimos a familias y propietarios de negocios en Fresno, Clovis, Sanger, Selma y Madera, y no somos un quiosco temporal ni una cadena de fuera de la ciudad. Somos tus vecinos, y nuestra oficina permanece abierta todo el año — las necesidades notariales no siguen un calendario."),

    ("Every notarization we perform is backed by an active California notary commission and the state-required bond. Our loan signing work follows the strict standards that title companies and lenders expect, and the trust we&rsquo;ve earned as a Fresno tax preparation office means your documents and privacy are always in careful hands.",
     "Cada notarización que realizamos está respaldada por una comisión notarial activa de California y la fianza requerida por el estado. Nuestro trabajo de firma de préstamos sigue los estrictos estándares que las compañías de títulos y los prestamistas esperan, y la confianza que hemos ganado como oficina de preparación de impuestos en Fresno significa que tus documentos y privacidad siempre están en manos cuidadosas."),

    ("📷 Exterior shot of the C&#038;R Tax Services office with clear signage, or a framed California notary commission certificate.",
     "📷 Foto exterior de la oficina de C&R Tax Services con señalización clara, o un certificado enmarcado de comisión notarial de California."),

    ('alt: &ldquo;C&#038;R Tax Services office in Fresno offering licensed notary public services to the Central Valley&rdquo;',
     'alt: "Oficina de C&R Tax Services en Fresno ofreciendo servicios de notario público con licencia al Valle Central"'),

    ("Whether it's a loan closing on the calendar, a power of attorney your family needs this week, or travel documents that must be certified before a flight, the fastest way to stop worrying is to get it done right, the first time. Call C&amp;R Tax Services today, or send us the details below and we'll tell you exactly what to bring. Se habla español.",
     "Ya sea un cierre de préstamo en el calendario, un poder notarial que tu familia necesita esta semana o documentos de viaje que deben certificarse antes de un vuelo, la forma más rápida de dejar de preocuparte es hacerlo bien desde la primera vez. Llama a C&amp;R Tax Services hoy, o envíanos los detalles a continuación y te diremos exactamente qué traer. Se habla español."),

    # ── LIVESCAN PAGE ──
    ("Livescan &#8211; C&amp;R Tax Services",
     "Livescan &#8211; C&amp;R Tax Services"),

    ("Full Service Fingerprints in Fresno &mdash; Fast, Certified, and Stress-Free",
     "Huellas Dactilares de Servicio Completo en Fresno — Rápidas, Certificadas y Sin Estrés"),

    ("Livescan submissions, background checks, and FD-258 ink cards &mdash; all under one roof, done right the first time.",
     "Envíos de Livescan, verificaciones de antecedentes y tarjetas de tinta FD-258 — todo bajo un mismo techo, hecho correctamente la primera vez."),

    ("So you just found out you need fingerprints. Maybe it&rsquo;s for a new job, a license, or a certification. The deadline is close, and you&rsquo;re not sure where to go. Some places make you wait days for an appointment. Others rush you through the door and leave you wondering if it was even done right. When your career is on the line, guessing isn&rsquo;t good enough.",
     "Así que acabas de enterarte de que necesitas huellas dactilares. Quizás es para un nuevo trabajo, una licencia o una certificación. El plazo se acerca y no estás seguro de adónde ir. Algunos lugares te hacen esperar días para una cita. Otros te hacen pasar rápido y te dejan preguntándote si siquiera se hizo bien. Cuando tu carrera está en juego, adivinar no es suficiente."),

    ("At C&amp;R Tax Services, we make Fresno Livescan fingerprinting simple. We offer full service fingerprints under one roof: digital Livescan submissions, Livescan background checks, and traditional FD-258 ink cards. Walk in with your form, and walk out knowing the job was done right the first time.",
     "En C&amp;R Tax Services, hacemos que las huellas dactilares Livescan en Fresno sean simples. Ofrecemos huellas dactilares de servicio completo bajo un mismo techo: envíos digitales de Livescan, verificaciones de antecedentes Livescan y tarjetas de tinta tradicionales FD-258. Entra con tu formulario y sal sabiendo que el trabajo se hizo correctamente la primera vez."),

    ("We&rsquo;re a local Fresno firm, not a pop-up kiosk. Our team is trained and certified to capture and submit prints that meet California Department of Justice and FBI standards. And because Fresno is a community of many voices,",
     "Somos una firma local de Fresno, no un quiosco temporal. Nuestro equipo está capacitado y certificado para capturar y enviar huellas que cumplen con los estándares del Departamento de Justicia de California y el FBI. Y porque Fresno es una comunidad de muchas voces,"),

    (". You can ask every question in the language you&rsquo;re most comfortable with.",
     ". Puedes hacer cada pregunta en el idioma con el que te sientes más cómodo."),

    ('alt: &ldquo;Certified technician performing Livescan fingerprints in Fresno&rdquo;',
     'alt: "Técnico certificado realizando huellas dactilares Livescan en Fresno"'),

    ("Fingerprinting requests almost always come with a deadline. Maybe your new employer needs a background check before your start date. Maybe you&rsquo;re applying for a teaching credential, a nursing license, a real estate license, or a childcare permit. Foster care and adoption applications, notary commissions, and security guard cards all require prints too. Whatever the reason, the state won&rsquo;t move forward until your prints are in the system.",
     "Las solicitudes de huellas dactilares casi siempre vienen con un plazo. Quizás tu nuevo empleador necesita una verificación de antecedentes antes de tu fecha de inicio. Quizás estás solicitando una credencial de enseñanza, una licencia de enfermería, una licencia de bienes raíces o un permiso de cuidado infantil. Las solicitudes de cuidado de crianza y adopción, las comisiones notariales y las tarjetas de guardia de seguridad también requieren huellas. Sea cual sea la razón, el estado no avanzará hasta que tus huellas estén en el sistema."),

    ("Here&rsquo;s the tricky part: many people don&rsquo;t know which type of fingerprinting they need. California agencies usually want a digital Livescan submission, which sends your prints straight to the DOJ. But out-of-state employers and federal agencies often ask for a physical FD-258 fingerprint card instead. Show up at the wrong place with the wrong form, and you can lose a day. Sometimes a whole week.",
     "Aquí está la parte difícil: muchas personas no saben qué tipo de huellas dactilares necesitan. Las agencias de California generalmente quieren un envío digital de Livescan, que envía tus huellas directamente al DOJ. Pero los empleadores fuera del estado y las agencias federales a menudo piden en cambio una tarjeta física de huellas FD-258. Presentarte en el lugar equivocado con el formulario equivocado puede costarte un día. A veces toda una semana."),

    ("That&rsquo;s why workers, families, and business owners across Fresno choose a provider that handles it all. As a full service fingerprints location, we take care of Livescan submissions, Livescan background checks, and FD-258 ink cards in one visit. You bring your request form, and we handle the rest. No bouncing between offices, and no wondering whether the fingerprints Fresno agencies require were submitted the right way.",
     "Por eso los trabajadores, familias y propietarios de negocios en todo Fresno eligen un proveedor que lo maneja todo. Como ubicación de huellas dactilares de servicio completo, nos encargamos de los envíos de Livescan, las verificaciones de antecedentes Livescan y las tarjetas de tinta FD-258 en una sola visita. Tú traes tu formulario de solicitud y nosotros hacemos el resto. Sin rebotar entre oficinas y sin preguntarte si las huellas que requieren las agencias de Fresno se enviaron de la manera correcta."),

    ('alt: &ldquo;FD-258 fingerprint card and Livescan form at a Fresno fingerprinting office&rdquo;',
     'alt: "Tarjeta de huellas FD-258 y formulario de Livescan en una oficina de huellas dactilares en Fresno"'),

    ("Walk-ins welcome &ndash; most visits take 15 minutes or less.",
     "Visitas sin cita bienvenidas — la mayoría de las visitas toman 15 minutos o menos."),

    ("A lot of fingerprinting spots treat you like a number. You wait in line, get rolled through the process, and leave with a receipt and zero explanation. We do things differently. When you visit our Fresno office, a real person walks you through every step. We check your request form before we scan, so common mistakes &mdash; a wrong ORI code or a missing applicant type &mdash; get caught before they cost you a rejection.",
     "Muchos lugares de huellas dactilares te tratan como un número. Esperas en fila, te pasan por el proceso y sales con un recibo y cero explicaciones. Nosotros hacemos las cosas diferente. Cuando visitas nuestra oficina en Fresno, una persona real te guía en cada paso. Revisamos tu formulario de solicitud antes de escanear, para que los errores comunes — un código ORI incorrecto o un tipo de solicitante faltante — se detecten antes de que te cuesten un rechazo."),

    ("Our equipment and process meet California DOJ standards, which means clean captures and fewer rejected prints. And if an agency ever sends a submission back for image quality, we make it right. We also keep our pricing clear and upfront, just like we do with our tax and notary services. You&rsquo;ll know exactly what your visit costs before we ever touch the scanner.",
     "Nuestro equipo y proceso cumplen con los estándares del DOJ de California, lo que significa capturas limpias y menos huellas rechazadas. Y si alguna agencia devuelve un envío por calidad de imagen, lo corregimos. También mantenemos nuestros precios claros y transparentes, igual que con nuestros servicios de impuestos y notaría. Sabrás exactamente cuánto cuesta tu visita antes de que toquemos el escáner."),

    ("Clean captures and fewer rejected prints &mdash; and if an agency ever sends one back, we make it right.",
     "Capturas limpias y menos huellas rechazadas — y si alguna agencia devuelve una, la corregimos."),

    ("You&rsquo;ll know exactly what your visit costs before we ever touch the scanner.",
     "Sabrás exactamente cuánto cuesta tu visita antes de que toquemos el escáner."),

    ("We explain the process, the forms, and the results in plain language &mdash; English or Spanish.",
     "Explicamos el proceso, los formularios y los resultados en lenguaje sencillo — inglés o español."),

    ("📷 Bilingual staff member at the front desk with &#8216;Se Habla Español&#8217; signage visible.",
     "📷 Personal bilingüe en la recepción con letrero 'Se Habla Español' visible."),

    ('alt: &ldquo;Bilingual fingerprinting service in Fresno with Spanish-speaking staff&rdquo;',
     'alt: "Servicio de huellas dactilares bilingüe en Fresno con personal de habla hispana"'),

    ("Clients tell us the best part of working with our team is how patient and clear we are. One local client came in stressed. She had a job offer that hinged on a background check, and the deadline was days away. We reviewed her Livescan form, caught an error in the agency code, fixed it, and submitted her prints the same day. She started her new job on time &mdash; and told us she wished she&rsquo;d come to us first.",
     "Los clientes nos dicen que la mejor parte de trabajar con nuestro equipo es lo pacientes y claros que somos. Una cliente local llegó estresada. Tenía una oferta de trabajo que dependía de una verificación de antecedentes, y el plazo estaba a días de distancia. Revisamos su formulario de Livescan, detectamos un error en el código de la agencia, lo corregimos y enviamos sus huellas el mismo día. Comenzó su nuevo trabajo a tiempo — y nos dijo que ojalá hubiera venido con nosotros primero."),

    ("That&rsquo;s the outcome we aim for every single time: peace of mind. Whether it&rsquo;s a nurse renewing a license, a new notary getting commissioned, or a parent completing a foster care application, our clients leave knowing their fingerprints were captured correctly and sent where they need to go. No re-dos, no lost time, no surprises.",
     "Ese es el resultado al que apuntamos cada vez: tranquilidad. Ya sea una enfermera renovando una licencia, un nuevo notario siendo comisionado o un padre completando una solicitud de cuidado de crianza, nuestros clientes se van sabiendo que sus huellas dactilares fueron capturadas correctamente y enviadas adonde necesitan ir. Sin repeticiones, sin tiempo perdido, sin sorpresas."),

    ("C&amp;R Tax Services is a Fresno-based firm serving families and business owners across the Central Valley, including Clovis, Sanger, Selma, and Madera. Unlike seasonal offices that vanish after tax season, we&rsquo;re open year-round. So when your employer or licensing board says &ldquo;we need your prints this week,&rdquo; we&rsquo;re here.",
     "C&amp;R Tax Services es una firma con sede en Fresno que sirve a familias y propietarios de negocios en todo el Valle Central, incluyendo Clovis, Sanger, Selma y Madera. A diferencia de las oficinas de temporada que desaparecen después de la temporada de impuestos, estamos abiertos todo el año. Así que cuando tu empleador o junta de licencias diga \"necesitamos tus huellas esta semana\", estamos aquí."),

    ("Every fingerprinting service is performed by trained, certified technicians, and every Livescan submission follows California DOJ requirements. We&rsquo;re the same trusted local team that handles tax preparation, notary public services, and loan signings for our community. That means we already live and breathe official documents, compliance, and deadlines. Your paperwork is in careful, experienced hands.",
     "Cada servicio de huellas dactilares es realizado por técnicos capacitados y certificados, y cada envío de Livescan sigue los requisitos del DOJ de California. Somos el mismo equipo local de confianza que maneja la preparación de impuestos, servicios de notaría pública y firmas de préstamos para nuestra comunidad. Eso significa que ya vivimos y respiramos documentos oficiales, cumplimiento y plazos. Tu papeleo está en manos cuidadosas y experimentadas."),

    ('alt: &ldquo;C&#038;R Tax Services Fresno office offering Livescan fingerprinting&rdquo;',
     'alt: "Oficina de C&R Tax Services en Fresno ofreciendo huellas dactilares Livescan"'),

    # ── CONTACT PAGE ──
    ("Contact &#8211; C&amp;R Tax Services",
     "Contacto &#8211; C&amp;R Tax Services"),

    ("We&#8217;re Glad You&#8217;re Here",
     "Nos Alegra que Estés Aquí"),

    ("Thanks for stopping by! If you&#8217;ve been looking for trusted Fresno tax preparation, you&#8217;re in the right place. At C&amp;R Tax Services, there&#8217;s no automated runaround and no call center in another state. You&#8217;ll talk with real, friendly people right here in Fresno — ready to listen, answer your questions, and help you feel good about your taxes.",
     "¡Gracias por visitarnos! Si has estado buscando una preparación de impuestos confiable en Fresno, estás en el lugar correcto. En C&amp;R Tax Services, no hay ruedas de prensa automatizadas ni centros de llamadas en otro estado. Hablarás con personas reales y amigables aquí mismo en Fresno — listas para escuchar, responder tus preguntas y ayudarte a sentirte bien con tus impuestos."),

    ("Tell us a bit about what you need, and we&#8217;ll get back to you the same business day.",
     "Cuéntanos un poco sobre lo que necesitas y te responderemos el mismo día hábil."),

    ("Ask your questions in the language you&rsquo;re most comfortable with. No pressure, no obligation — just honest help.",
     "Haz tus preguntas en el idioma con el que te sientas más cómodo. Sin presión, sin obligación — solo ayuda honesta."),

    ("Whatever brings you here, we&rsquo;re happy to help.",
     "Sea lo que sea que te traiga aquí, estamos felices de ayudar."),

    ("Got an IRS letter or a looming deadline? Call right away, and we&rsquo;ll help you respond fast.",
     "¿Tienes una carta del IRS o un plazo inminente? Llama de inmediato y te ayudaremos a responder rápido."),

    ("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we&rsquo;re here after April 15th, not just before it.",
     "C&amp;R Tax Services es de propiedad y operación local, completamente acreditado y comprometido con la precisión en cada declaración — con apoyo durante todo el año, no solo en la temporada de impuestos. Respuestas reales de un equipo local — estamos aquí después del 15 de abril, no solo antes."),

    ("Tax questions don&#8217;t get easier by waiting — but they do get easier with the right team in your corner. Call now or reach out below. A local, professional team you can actually talk to will take the stress off your plate.",
     "Las preguntas de impuestos no se vuelven más fáciles esperando — pero sí se vuelven más fáciles con el equipo correcto de tu lado. Llama ahora o comunícate a continuación. Un equipo local y profesional con el que realmente puedes hablar quitará el estrés de tu plato."),
]


def run():
    print(f"Total translation pairs: {len(TRANSLATIONS)}\n")

    # Truncate old dictionary
    print("Clearing old dictionary...")
    r = php("""
global $wpdb;
$wpdb->query("TRUNCATE TABLE {$wpdb->prefix}trp_dictionary_en_us_es_es");
return ['cleared' => true];
""")
    print(f"Cleared: {r}")

    # Insert in batches using JSON to safely pass strings with HTML entities
    batch_size = 30
    total = 0
    for i in range(0, len(TRANSLATIONS), batch_size):
        batch = TRANSLATIONS[i:i+batch_size]
        pairs_json = json.dumps([[en, es] for en, es in batch], ensure_ascii=False)
        pairs_json_esc = pairs_json.replace("'", "\\'")
        code = f"""
global $wpdb;
$pairs = json_decode('{pairs_json_esc}', true);
$inserted = 0;
foreach ($pairs as $pair) {{
    $r = $wpdb->insert(
        $wpdb->prefix . 'trp_dictionary_en_us_es_es',
        ['original' => $pair[0], 'translated' => $pair[1], 'status' => 1, 'block_type' => 2],
        ['%s','%s','%d','%d']
    );
    if ($r !== false) $inserted++;
}}
return ['inserted' => $inserted, 'err' => $wpdb->last_error ?: 'none'];
"""
        r = php(code)
        total += r.get('inserted', 0) if r else 0
        n = i // batch_size + 1
        print(f"  Batch {n}: {len(batch)} pairs | inserted: {r.get('inserted','?') if r else 'ERR'} | err: {r.get('err','?') if r else 'ERR'}")

    print(f"\nTotal inserted: {total}")

    # Verify count
    r = php("global $wpdb; return ['count' => (int)$wpdb->get_var(\"SELECT COUNT(*) FROM {$wpdb->prefix}trp_dictionary_en_us_es_es WHERE status=1\")];")
    print(f"DB approved count: {r}")

    # Clear caches
    print("\nClearing caches...")
    php("""
// Breeze cache
if (function_exists('breeze_clear_all_cache')) breeze_clear_all_cache();
$cache_dir = WP_CONTENT_DIR . '/cache/breeze/';
if (is_dir($cache_dir)) {
    $it = new RecursiveDirectoryIterator($cache_dir, RecursiveDirectoryIterator::SKIP_DOTS);
    foreach (new RecursiveIteratorIterator($it, RecursiveIteratorIterator::CHILD_FIRST) as $f) {
        $f->isDir() ? rmdir($f) : unlink($f);
    }
}
// Object cache
wp_cache_flush();
// TRP cache
delete_transient('trp_cache_languages');
return ['ok' => true];
""")
    print("Caches cleared. Done!")


if __name__ == "__main__":
    run()
