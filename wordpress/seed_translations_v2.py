#!/usr/bin/env python3
"""
Seed TranslatePress dictionary with exact strings from rendered pages.
Strings use real Unicode chars (em dash —, curly quotes '', etc.) as the
DOM text nodes contain decoded HTML entities, not &mdash; / &#8217; etc.
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
    }, timeout=90)
    raw = r.text
    parsed = json.loads(raw)
    result = parsed.get("result", {})
    text = result.get("content", [{}])[0].get("text", "{}")
    data = json.loads(text)
    return data.get("data", data)

# All English → Spanish pairs using exact rendered text (Unicode, not HTML entities)
TRANSLATIONS = [
    # ── Short labels / nav / badges ──────────────────────────────────────────
    ("About", "Nosotros"),
    ("About Our Team", "Nuestro Equipo"),
    ("Accessibility", "Accesibilidad"),
    ("Accuracy", "Precisión"),
    ("Amendments", "Enmiendas"),
    ("Ask About Mobile Service", "Pregunte por Servicio a Domicilio"),
    ("Audit Services", "Servicios de Auditoría"),
    ("Audit Services, Tax Extensions & Amendments", "Servicios de Auditoría, Extensiones y Enmiendas"),
    ("Available Any Day and All Year!", "¡Disponible Todos los Días y Todo el Año!"),
    ("Bank Documents", "Documentos Bancarios"),
    ("Book Your Appointment", "Reserve su Cita"),
    ("By Appointment Only", "Solo con Cita Previa"),
    ("Call (559) 962-7503", "Llame al (559) 962-7503"),
    ("Clear, upfront pricing", "Precios claros y transparentes"),
    ("Company", "Empresa"),
    ("Contact", "Contacto"),
    ("Contact Us", "Contáctenos"),
    ("Corporations, Partnerships, & LLC’s", "Corporaciones, Sociedades y LLC"),
    ("Credentials & Services", "Credenciales y Servicios"),
    ("DOJ-standard equipment", "Equipo estándar del DOJ"),
    ("Documents We Handle", "Documentos que Manejamos"),
    ("English", "Inglés"),
    ("Every Situation We Handle", "Cada Situación que Atendemos"),
    ("Every page, checked carefully", "Cada página, revisada con cuidado"),
    ("Extensions", "Extensiones"),
    ("FD-258 Fingerprint Cards", "Tarjetas de Huellas FD-258"),
    ("Free quotes", "Cotizaciones gratuitas"),
    ("Fresno & the Central Valley", "Fresno y el Valle Central"),
    ("Fresno Tax Blog", "Blog de Impuestos de Fresno"),
    ("Full Service Fingerprints in Fresno — Fast, Certified, and Stress-Free", "Huellas Dactilares en Fresno — Rápidas, Certificadas y sin Estrés"),
    ("Full-Service Offerings", "Servicios Completos"),
    ("General questions", "Preguntas generales"),
    ("Get In Touch", "Contáctenos"),
    ("Get Started Now — Schedule My Appointment", "Comience Ahora — Programe mi Cita"),
    ("Get upfront, honest pricing for your tax preparation before we file a thing.", "Obtenga precios honestos y transparentes para su preparación de impuestos antes de que presentemos nada."),
    ("Getting in touch is easy. Fill out the form, or pick whatever works best for you below.", "Ponerse en contacto es fácil. Complete el formulario o elija lo que más le convenga a continuación."),
    ("Got an IRS letter or a looming deadline? Call right away, and we’ll help you respond fast.", "¿Recibió una carta del IRS o tiene una fecha límite próxima? Llame de inmediato y le ayudaremos a responder rápido."),
    ("Honesty", "Honestidad"),
    ("How C&R Tax Services Does It Better", "Cómo C&R Tax Services Lo Hace Mejor"),
    ("How to Reach Us", "Cómo Contactarnos"),
    ("ITIN Applications", "Solicitudes de ITIN"),
    ("ITIN Applications & Multi-State Returns", "Solicitudes de ITIN y Declaraciones Multi-Estado"),
    ("Income Tax", "Impuestos"),
    ("Income Tax Preparation", "Preparación de Impuestos"),
    ("Individual", "Individual"),
    ("Individual & Rental Property Taxes", "Impuestos Individuales y de Propiedades en Alquiler"),
    ("Individual Taxes", "Impuestos Individuales"),
    ("January – April", "Enero – Abril"),
    ("Learn more about Audit, Extension & Amendment Services ⟶", "Más sobre Auditoría, Extensiones y Enmiendas ⟶"),
    ("Learn more about ITIN & Multi-State Services ⟶", "Más sobre ITIN y Servicios Multi-Estado ⟶"),
    ("Learn more about Notary & Live Scan Services ⟶", "Más sobre Notaría y Servicios Live Scan ⟶"),
    ("Learn more about our Business Tax Preparation ⟶", "Más sobre nuestra Preparación de Impuestos Empresariales ⟶"),
    ("Learn more about our Individual Tax Services ⟶", "Más sobre nuestros Servicios de Impuestos Individuales ⟶"),
    ("Legal Documents & Forms", "Documentos Legales y Formularios"),
    ("Let’s Get Started Today", "Comencemos Hoy"),
    ("Let’s Talk — We’d Love to Meet You", "Hablemos — Nos Encantaría Conocerle"),
    ("Live Scan & Notary", "Live Scan y Notaría"),
    ("Live Scan fingerprinting", "Huellas Dactilares Live Scan"),
    ("Livescan", "Livescan"),
    ("Livescan Background Checks", "Verificaciones de Antecedentes Livescan"),
    ("Livescan Fingerprinting", "Huellas Dactilares Livescan"),
    ("Livescan submissions, background checks, and FD-258 ink cards — all under one roof, done right the first time.", "Envíos Livescan, verificaciones de antecedentes y tarjetas de tinta FD-258 — todo bajo un mismo techo, hecho bien desde la primera vez."),
    ("Loan Signing Agent Services", "Servicios de Agente de Firma de Préstamos"),
    ("Local & Family-Focused", "Local y Enfocado en la Familia"),
    ("Local Trust & Licensing", "Confianza Local y Licencias"),
    ("May – December", "Mayo – Diciembre"),
    ("Meet the People Behind C&R", "Conozca al Equipo Detrás de C&R"),
    ("Mobile Service Available", "Servicio a Domicilio Disponible"),
    ("Mobile Services available upon request – Travel fees will be applied.", "Servicios a domicilio disponibles bajo petición – Se cobrarán tarifas de desplazamiento."),
    ("Monday – Friday", "Lunes – Viernes"),
    ("Monday – Saturday", "Lunes – Sábado"),
    ("Multi State Returns", "Declaraciones Multi-Estado"),
    ("Near Tower District", "Cerca del Distrito Tower"),
    ("Need a document notarized or Live Scan fingerprints for a job or license? We can usually get you in quickly.", "¿Necesita un documento notariado o huellas Live Scan para un trabajo o licencia? Generalmente podemos atenderle rápidamente."),
    ("Not sure / other", "No estoy seguro / otro"),
    ("Not sure which documents you need? Wondering about an extension? Just ask.", "¿No sabe qué documentos necesita? ¿Tiene preguntas sobre una extensión? Solo pregunte."),
    ("Notary", "Notaría"),
    ("Notary & Live Scan appointments", "Citas de Notaría y Live Scan"),
    ("Notary Public, Loan Signing & Live Scan Fingerprints", "Notario Público, Firma de Préstamos y Huellas Dactilares Live Scan"),
    ("Notary Services", "Servicios Notariales"),
    ("Notary public services & loan signing support", "Servicios notariales y soporte de firma de préstamos"),
    ("Office Hours", "Horario de Oficina"),
    ("Our Featured Tax & Business Services", "Nuestros Servicios Destacados de Impuestos y Negocios"),
    ("Power of Attorney", "Poder Notarial"),
    ("Prior Year Reviews", "Revisiones de Años Anteriores"),
    ("Proudly Serving Fresno & the Central Valley", "Sirviendo con Orgullo a Fresno y el Valle Central"),
    ("Proudly Serving the Central Valley", "Sirviendo con Orgullo al Valle Central"),
    ("Ready to Maximize Your Return and Minimize Your Stress?", "¿Listo para Maximizar su Reembolso y Minimizar su Estrés?"),
    ("Real Estate Documents & Forms", "Documentos y Formularios de Bienes Raíces"),
    ("Real People, Fast Responses", "Personas Reales, Respuestas Rápidas"),
    ("Real-World Results", "Resultados Reales"),
    ("Rental Properties", "Propiedades en Alquiler"),
    ("Request a Free Estimate", "Solicite una Estimación Gratuita"),
    ("Request a Free Quote", "Solicite una Cotización Gratuita"),
    ("Saturday – Sunday", "Sábado – Domingo"),
    ("Schedule Your Appointment", "Programe su Cita"),
    ("Schedule an Appointment", "Programe una Cita"),
    ("Se habla español", "Se habla español"),
    ("Se habla español, from your first phone call to your final signature.", "Se habla español, desde su primera llamada hasta su firma final."),
    ("Secure Client Document Portal", "Portal Seguro de Documentos para Clientes"),
    ("Secure virtual tax preparation", "Preparación de impuestos virtual segura"),
    ("Send Message", "Enviar Mensaje"),
    ("Send Us a Message", "Envíenos un Mensaje"),
    ("Services", "Servicios"),
    ("Serving the Central Valley", "Sirviendo al Valle Central"),
    ("Small Business & Corporate Business Taxes", "Impuestos para Pequeños Negocios y Corporaciones"),
    ("Small Business / Self Employed", "Pequeño Negocio / Trabajador Independiente"),
    ("Small Business Taxes", "Impuestos para Pequeños Negocios"),
    ("Spanish", "Español"),
    ("Stop by, call, or book a virtual appointment — we’re here all year.", "Visítenos, llame o reserve una cita virtual — estamos aquí todo el año."),
    ("Sunday", "Domingo"),
    ("Tax Season", "Temporada de Impuestos"),
    ("Tax Season (Jan – Apr)", "Temporada de Impuestos (Ene – Abr)"),
    ("Tax Season (Jan – Apr)", "Temporada de Impuestos (Ene – Abr)"),
    ("Tax Season Doesn’t Have to Be Stressful.", "La Temporada de Impuestos No Tiene que ser Estresante."),
    ("After Tax Season", "Fuera de Temporada"),
    ("After Tax Season (May – Dec)", "Fuera de Temporada (May – Dic)"),
    ("After Hours — By Appointment Only", "Fuera de Horario — Solo con Cita Previa"),
    ("Travel Documents", "Documentos de Viaje"),
    ("Upfront, transparent pricing", "Precios transparentes y directos"),
    ("Upload Your Docs (Virtual Prep)", "Suba sus Documentos (Preparación Virtual)"),
    ("Upload Your Docs — Virtual Prep", "Suba sus Documentos — Preparación Virtual"),
    ("Urgent tax matters", "Asuntos fiscales urgentes"),
    ("Verified client reviews will go here once collected via Google Business Profile.", "Las reseñas verificadas de clientes irán aquí una vez recopiladas a través de Google Business Profile."),
    ("Virtual/Online Tax Preparation – Available Any Day and All Year!", "Preparación de Impuestos Virtual/En Línea – ¡Disponible Todos los Días y Todo el Año!"),
    ("Walk In Today", "Visítenos Hoy"),
    ("Walk In or Book Ahead", "Visítenos o Reserve con Anticipación"),
    ("Walk-Ins Welcome", "Se Aceptan Sin Cita"),
    ("Walk-ins welcome – most visits take 15 minutes or less.", "Se aceptan sin cita – la mayoría de las visitas toman 15 minutos o menos."),
    ("What Clients Are Saying", "Lo Que Dicen Nuestros Clientes"),
    ("What This Service Solves", "Qué Resuelve Este Servicio"),
    ("What We Offer", "Lo Que Ofrecemos"),
    ("What We Stand For", "Lo Que Defendemos"),
    ("What do you need help with?", "¿Con qué necesita ayuda?"),
    ("Whatever brings you here, we’re happy to help.", "Sea lo que sea que le traiga aquí, estamos felices de ayudar."),
    ("Why Fresno Trusts C&R Tax Services", "Por Qué Fresno Confía en C&R Tax Services"),
    ("Why Homeowners and Local Families Trust C&R Tax Services", "Por Qué los Propietarios y Familias Locales Confían en C&R Tax Services"),
    ("Why Reach Out?", "¿Por Qué Contactarnos?"),
    ("Why We Started C&R Tax Services", "Por Qué Fundamos C&R Tax Services"),
    ("You Work Hard for Your Money — This Is the Year to Keep More of It", "Usted Trabaja Duro por su Dinero — Este Es el Año para Quedarse con Más"),
    ("Your Trusted Local Team", "Su Equipo Local de Confianza"),
    ("You’ll know exactly what your visit costs before we ever touch the scanner.", "Sabrá exactamente cuánto costará su visita antes de que toquemos el escáner."),
    ("You’ll know your cost before we file. Period.", "Sabrá su costo antes de que presentemos. Punto."),
    ("Tax season: January – April. After tax season: May – December.", "Temporada de impuestos: Enero – Abril. Fuera de temporada: Mayo – Diciembre."),
    ("Tell us a bit about what you need, and we’ll get back to you the same business day.", "Cuéntenos un poco sobre lo que necesita y le responderemos el mismo día hábil."),
    ("Tell us about your filing situation and we’ll follow up the same business day.", "Cuéntenos sobre su situación fiscal y le responderemos el mismo día hábil."),
    ("Tell us what needs notarizing and when — we’ll follow up the same business day.", "Díganos qué necesita notarizar y cuándo — le responderemos el mismo día hábil."),
    ("Tell us what your fingerprints are for and we’ll confirm what to bring.", "Díganos para qué son sus huellas y le confirmaremos qué traer."),
    ("Usually just a valid, unexpired photo ID and your unsigned documents — no guesswork.", "Generalmente solo una identificación fotográfica válida y vigente y sus documentos sin firmar — sin adivinar."),
    ("We check your form first", "Revisamos su formulario primero"),
    ("We confirm every name matches and every signature lands exactly where it belongs.", "Confirmamos que cada nombre coincide y que cada firma esté exactamente donde corresponde."),
    ("We explain every signature and stamp clearly, in the language you’re most comfortable with.", "Explicamos cada firma y sello claramente, en el idioma con el que se sienta más cómodo."),
    ("We explain the process, the forms, and the results in plain language — English or Spanish.", "Explicamos el proceso, los formularios y los resultados en lenguaje sencillo — inglés o español."),
    ("We serve you in your language", "Le atendemos en su idioma"),
    ("We tell you exactly what to bring", "Le decimos exactamente qué traer"),
    ("We’re Glad You’re Here", "Nos Alegra su Visita"),

    # ── Checkmark list items ─────────────────────────────────────────────────
    ("✓ Amendments", "✓ Enmiendas"),
    ("✓ Audit Services", "✓ Servicios de Auditoría"),
    ("✓ Bank Documents", "✓ Documentos Bancarios"),
    ("✓ Corporations, Partnerships, & LLC’s", "✓ Corporaciones, Sociedades y LLC"),
    ("✓ Extensions", "✓ Extensiones"),
    ("✓ FD-258 Card", "✓ Tarjeta FD-258"),
    ("✓ ITIN Applications", "✓ Solicitudes de ITIN"),
    ("✓ Individual", "✓ Individual"),
    ("✓ Legal Documents & Forms", "✓ Documentos Legales y Formularios"),
    ("✓ Livescan Background Checks", "✓ Verificaciones de Antecedentes Livescan"),
    ("✓ Multi State Returns", "✓ Declaraciones Multi-Estado"),
    ("✓ Power of Attorney", "✓ Poder Notarial"),
    ("✓ Prior Year Reviews", "✓ Revisiones de Años Anteriores"),
    ("✓ Real Estate Documents & Forms", "✓ Documentos y Formularios de Bienes Raíces"),
    ("✓ Rental Properties", "✓ Propiedades en Alquiler"),
    ("✓ Small Business / Self Employed", "✓ Pequeño Negocio / Trabajador Independiente"),
    ("✓ Travel Documents", "✓ Documentos de Viaje"),
    ("✓ Virtual/Online Tax Preparation – Available Any Day and All Year!", "✓ Preparación de Impuestos Virtual/En Línea – ¡Disponible Todos los Días y Todo el Año!"),

    # ── Longer sentences ─────────────────────────────────────────────────────
    ("100% accuracy guarantee", "Garantía de precisión del 100%"),
    ("A clean notary journal, every time", "Un diario notarial impecable, siempre"),
    ("A wrong ORI code or missing applicant type gets caught before it costs you a rejection.", "Un código ORI incorrecto o un tipo de solicitante faltante se detecta antes de que le cueste un rechazo."),
    ("Accurate, dependable income tax preparation for individuals, small businesses, and corporations across Fresno and the Central Valley — offered in person or fully virtual, in English or Spanish.", "Preparación de impuestos precisa y confiable para individuos, pequeños negocios y corporaciones en Fresno y el Valle Central — en persona o completamente virtual, en inglés o español."),
    ("And because we also offer notary and Live Scan fingerprinting services under the same roof, many of our clients discover we can handle far more than just their taxes.", "Y como también ofrecemos servicios de notaría y huellas dactilares Live Scan bajo el mismo techo, muchos clientes descubren que podemos atender mucho más que solo sus impuestos."),
    ("Ask around Fresno about what matters most in a tax preparer, and you’ll hear the same answers again and again: patience, honesty, clear explanations, and getting every dollar you deserve. From first-time filers to business owners untangling multi-state returns, our clients tend to tell us the same thing: working with C&R Tax Services made taxes feel simple for the first time.", "Pregunte en Fresno qué es lo más importante en un preparador de impuestos y escuchará las mismas respuestas una y otra vez: paciencia, honestidad, explicaciones claras y obtener cada dólar que merece. Desde quienes presentan por primera vez hasta dueños de negocios con declaraciones multi-estado, nuestros clientes nos dicen lo mismo: trabajar con C&R Tax Services hizo que los impuestos se sintieran simples por primera vez."),
    ("Ask around the Central Valley and you’ll hear the same words used to describe a great tax preparer: patient, thorough, honest about pricing, and focused on getting you every dollar you deserve. Clients tell us the biggest relief isn’t just the refund — it’s finally understanding their own taxes, and knowing nothing was missed or hidden.", "Pregunte en el Valle Central y escuchará las mismas palabras para describir un gran preparador de impuestos: paciente, minucioso, honesto con los precios y enfocado en obtenerle cada dólar que merece. Los clientes nos dicen que el mayor alivio no es solo el reembolso — es finalmente entender sus propios impuestos y saber que no se perdió ni se ocultó nada."),
    ("At C&R Tax Services, numbers are the foundation of your family’s and your business’s financial peace of mind. Let our family protect yours this season.", "En C&R Tax Services, los números son la base de la tranquilidad financiera de su familia y su negocio. Deje que nuestra familia proteja la suya esta temporada."),
    ("At C&R Tax Services, our job is to take that weight off your shoulders — with careful, personal attention on every return, and complete tax preparation available in Spanish.", "En C&R Tax Services, nuestro trabajo es quitarle ese peso de encima — con atención cuidadosa y personal en cada declaración, y preparación de impuestos completa disponible en español."),
    ("At C&R Tax Services, we make Fresno Livescan fingerprinting simple. We offer full service fingerprints under one roof: digital Livescan submissions, Livescan background checks, and traditional FD-258 ink cards. Walk in with your form, and walk out knowing the job was done right the first time.", "En C&R Tax Services, hacemos que las huellas dactilares Livescan en Fresno sean simples. Ofrecemos servicio completo de huellas bajo un mismo techo: envíos digitales Livescan, verificaciones de antecedentes Livescan y tarjetas de tinta tradicionales FD-258. Entre con su formulario y salga sabiendo que el trabajo se hizo bien desde la primera vez."),
    ("At its heart, C&R Tax Services was built on a simple promise: treat every return like it belongs to family. Whether you’re filing a straightforward W-2, applying for an ITIN, or untangling a multi-state small business return, we want you to walk out of our office feeling something most people never associate with taxes — genuine peace of mind.", "En su esencia, C&R Tax Services se fundó sobre una promesa simple: tratar cada declaración como si perteneciera a un familiar. Ya sea que presente un W-2 sencillo, solicite un ITIN o desenrede una declaración de pequeño negocio multi-estado, queremos que salga de nuestra oficina sintiendo algo que la mayoría de las personas nunca asocia con los impuestos — verdadera tranquilidad."),
    ("Because we live and work in the Central Valley ourselves, we understand the financial realities our neighbors face. And with our secure virtual tax preparation option, distance is never a barrier.", "Porque vivimos y trabajamos en el Valle Central, entendemos las realidades financieras que enfrentan nuestros vecinos. Y con nuestra opción de preparación de impuestos virtual segura, la distancia nunca es una barrera."),
    ("Beyond tax preparation, our team is [certified/registered] to provide notary public services, loan signing support, and Live Scan fingerprinting — making us a true one-stop compliance resource for local startups, caregivers, and real estate professionals.", "Más allá de la preparación de impuestos, nuestro equipo está certificado para brindar servicios notariales, soporte de firma de préstamos y huellas dactilares Live Scan — lo que nos convierte en un verdadero recurso integral para startups locales, cuidadores y profesionales de bienes raíces."),
    ("Big-box tax chains and DIY software treat you like a ticket number. We treat you like a neighbor, because you are one. Every return starts with a real conversation about your year — what changed, what you earned, what you’re hoping to accomplish. From there, we build your return line by line, checking for every credit and deduction you legally qualify for, whether it’s a simple individual return or a complex filing for a corporation, partnership, or LLC.", "Las grandes cadenas de impuestos y el software de bricolaje le tratan como un número de ticket. Nosotros le tratamos como un vecino, porque lo es. Cada declaración comienza con una conversación real sobre su año — qué cambió, qué ganó, qué espera lograr. A partir de ahí, construimos su declaración línea por línea, verificando cada crédito y deducción que legalmente califica, ya sea una declaración individual simple o una compleja para una corporación, sociedad o LLC."),
    ("C&R Tax Services handles small business and corporate business taxes for sole proprietors, partnerships, LLCs, S-Corps, and C-Corps across Fresno — and if your business operates across state lines, our multi-state return experience keeps every jurisdiction squared away.", "C&R Tax Services maneja los impuestos de pequeños negocios y corporaciones para propietarios únicos, sociedades, LLC, S-Corps y C-Corps en Fresno — y si su negocio opera en varios estados, nuestra experiencia en declaraciones multi-estado mantiene todo en orden en cada jurisdicción."),
    ("C&R Tax Services is a Fresno-based firm serving families and business owners across the Central Valley, including Clovis, Sanger, Selma, and Madera. Unlike seasonal offices that vanish after tax season, we’re open year-round. So when your employer or licensing board says “we need your prints this week,” we’re here.", "C&R Tax Services es una empresa con sede en Fresno que sirve a familias y dueños de negocios en todo el Valle Central, incluyendo Clovis, Sanger, Selma y Madera. A diferencia de las oficinas estacionales que desaparecen después de la temporada de impuestos, estamos abiertos todo el año. Así que cuando su empleador o junta de licencias dice “necesitamos sus huellas esta semana”, estamos aquí."),
    ("C&R Tax Services is based in Fresno, and our roots here run deep. But our service area reaches well beyond one zip code. We proudly provide income tax preparation, ITIN applications, business tax services, notary work, and Live Scan fingerprinting to families and businesses throughout the Central Valley.", "C&R Tax Services tiene su sede en Fresno y nuestras raíces aquí son profundas. Pero nuestra área de servicio se extiende mucho más allá de un código postal. Con orgullo brindamos preparación de impuestos, solicitudes de ITIN, servicios de impuestos empresariales, trabajo notarial y huellas dactilares Live Scan a familias y negocios en todo el Valle Central."),
    ("C&R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we’re here after April 15th, not just before it.", "C&R Tax Services es de propiedad y operación local, completamente acreditado y comprometido con la precisión en cada declaración — con soporte todo el año, no solo en época de impuestos. Respuestas reales de un equipo local — estamos aquí después del 15 de abril, no solo antes."),
    ("C&R Tax Services is proudly local. We serve families and business owners across Fresno, Clovis, Sanger, Selma, and Madera, and we’re not a pop-up kiosk or an out-of-town chain. We’re your neighbors, and our office stays open year-round — notary needs don’t follow a calendar.", "C&R Tax Services es orgullosamente local. Servimos a familias y dueños de negocios en Fresno, Clovis, Sanger, Selma y Madera, y no somos un quiosco temporal ni una cadena foránea. Somos sus vecinos y nuestra oficina permanece abierta todo el año — las necesidades notariales no siguen un calendario."),
    ("C&R Tax Services proudly serves families and business owners across Fresno, Clovis, Sanger, Selma, and Madera. We’re not a seasonal pop-up that disappears the day after the deadline — we’re a year-round Central Valley firm. When you get an IRS letter in July, need an extension in October, or want a prior-year review in November, our door is open and our phone gets answered.", "C&R Tax Services sirve con orgullo a familias y dueños de negocios en Fresno, Clovis, Sanger, Selma y Madera. No somos un negocio temporal que desaparece al día siguiente de la fecha límite — somos una empresa del Valle Central que opera todo el año. Cuando reciba una carta del IRS en julio, necesite una extensión en octubre o quiera una revisión de años anteriores en noviembre, nuestra puerta está abierta y su llamada será respondida."),
    ("Certified notarization and loan signing for the documents that matter most — in-office or on the road.", "Notarización certificada y firma de préstamos para los documentos más importantes — en oficina o a domicilio."),
    ("Clean captures and fewer rejected prints — and if an agency ever sends one back, we make it right.", "Capturas limpias y menos huellas rechazadas — y si una agencia devuelve alguna, lo corregimos."),
    ("Clients across the Fresno area tell us the same things they say about our tax work: that we’re patient, that we explain everything, and that we make stressful paperwork feel simple. When you leave our office, your documents are done right, and you know exactly what you signed.", "Los clientes del área de Fresno nos dicen las mismas cosas que dicen sobre nuestro trabajo de impuestos: que somos pacientes, que explicamos todo y que hacemos que el papeleo estresante se sienta simple. Cuando sale de nuestra oficina, sus documentos están correctamente completados y sabe exactamente lo que firmó."),
    ("Clients tell us the best part of working with our team is how patient and clear we are. One local client came in stressed. She had a job offer that hinged on a background check, and the deadline was days away. We reviewed her Livescan form, caught an error in the agency code, fixed it, and submitted her prints the same day. She started her new job on time — and told us she wished she’d come to us first.", "Los clientes nos dicen que la mejor parte de trabajar con nuestro equipo es lo pacientes y claros que somos. Una cliente local llegó estresada. Tenía una oferta de trabajo que dependía de una verificación de antecedentes y la fecha límite era en días. Revisamos su formulario Livescan, detectamos un error en el código de la agencia, lo corregimos y enviamos sus huellas el mismo día. Comenzó su nuevo trabajo a tiempo — y nos dijo que ojalá hubiera venido a nosotros primero."),
    ("Deadlines Don’t Wait — Let’s Get It Signed, Sealed, and Off Your Plate", "Las Fechas Límite No Esperan — Firmemos, Sellemos y Quitémosle ese Peso de Encima"),
    ("Don’t Let Fingerprinting Hold Up Your Job, License, or Certification", "No Deje que las Huellas Dactilares Retrasen su Trabajo, Licencia o Certificación"),
    ("Every fingerprinting service is performed by trained, certified technicians, and every Livescan submission follows California DOJ requirements. We’re the same trusted local team that handles tax preparation, notary public services, and loan signings for our community. That means we already live and breathe official documents, compliance, and deadlines. Your paperwork is in careful, experienced hands.", "Cada servicio de huellas dactilares es realizado por técnicos entrenados y certificados, y cada envío Livescan sigue los requisitos del DOJ de California. Somos el mismo equipo local de confianza que maneja la preparación de impuestos, los servicios notariales y las firmas de préstamos para nuestra comunidad. Eso significa que ya vivimos y respiramos documentos oficiales, cumplimiento normativo y fechas límite. Su papeleo está en manos cuidadosas y experimentadas."),
    ("Every notarization we perform is backed by an active California notary commission and the state-required bond. Our loan signing work follows the strict standards that title companies and lenders expect, and the trust we’ve earned as a Fresno tax preparation office means your documents and privacy are always in careful hands.", "Cada notarización que realizamos está respaldada por una comisión notarial activa de California y la fianza requerida por el estado. Nuestro trabajo de firma de préstamos sigue los estrictos estándares que esperan las compañías de título y los prestamistas, y la confianza que hemos ganado como oficina de preparación de impuestos en Fresno significa que sus documentos y privacidad siempre están en manos cuidadosas."),
    ("Every return we prepare meets federal and California registration and compliance standards, and your documents are always handled through secure, protected channels — whether you file in person or through our virtual portal.", "Cada declaración que preparamos cumple con los estándares federales y de California en materia de registro y cumplimiento, y sus documentos siempre se manejan a través de canales seguros y protegidos — ya sea que presente en persona o a través de nuestro portal virtual."),
    ("Everything we do at C&R Tax Services comes back to three values: honesty, accuracy, and accessibility. Taxes are stressful enough without feeling talked down to, so we take the time to explain your return in plain language — what you’re claiming, why it matters, and how to plan smarter for next year.", "Todo lo que hacemos en C&R Tax Services vuelve a tres valores: honestidad, precisión y accesibilidad. Los impuestos son suficientemente estresantes sin sentirse menospreciado, por lo que nos tomamos el tiempo de explicar su declaración en lenguaje sencillo — qué está reclamando, por qué importa y cómo planificar mejor para el próximo año."),
    ("Few things ruin a week faster than an envelope from the IRS. C&R Tax Services provides professional audit services and IRS notice support for taxpayers across the Fresno area — we read the notice with you and help you respond correctly and on time.", "Pocas cosas arruinan una semana más rápido que un sobre del IRS. C&R Tax Services brinda servicios profesionales de auditoría y soporte de avisos del IRS para contribuyentes en el área de Fresno — leemos el aviso con usted y le ayudamos a responder correcta y oportunamente."),
    ("Fingerprinting requests almost always come with a deadline. Maybe your new employer needs a background check before your start date. Maybe you’re applying for a teaching credential, a nursing license, a real estate license, or a childcare permit. Foster care and adoption applications, notary commissions, and security guard cards all require prints too. Whatever the reason, the state won’t move forward until your prints are in the system.", "Las solicitudes de huellas dactilares casi siempre vienen con una fecha límite. Quizás su nuevo empleador necesita una verificación de antecedentes antes de su fecha de inicio. Quizás está solicitando una credencial de enseñanza, una licencia de enfermería, una licencia de bienes raíces o un permiso de cuidado infantil. Las solicitudes de hogares de acogida y adopción, las comisiones notariales y las tarjetas de guardia de seguridad también requieren huellas. Sea cual sea el motivo, el estado no avanzará hasta que sus huellas estén en el sistema."),
    ("For a lot of people, filing personal taxes feels like a guessing game. Did you claim every deduction you qualify for? Was that side income reported the right way? Is your refund as big as it should be? Filing alone, or with generic software, often leaves those questions hanging in the air.", "Para muchas personas, presentar los impuestos personales se siente como un juego de adivinanzas. ¿Reclamó cada deducción para la que califica? ¿Se reportó correctamente ese ingreso adicional? ¿Es su reembolso tan grande como debería ser? Presentar solo, o con software genérico, a menudo deja esas preguntas en el aire."),
    ("For loan signings, we follow lender and title company instructions to the letter. Bank documents, deeds, refinance packets, powers of attorney, and legal forms all get the same careful, page-by-page review, with a clean notary journal kept on every transaction.", "Para las firmas de préstamos, seguimos las instrucciones del prestamista y de la compañía de título al pie de la letra. Los documentos bancarios, escrituras, paquetes de refinanciamiento, poderes notariales y formularios legales reciben la misma revisión cuidadosa página por página, con un diario notarial impecable en cada transacción."),
    ("For many Central Valley families, there’s one more hurdle: filing without a Social Security number. As certified ITIN application specialists, we help non-SSN filers get set up correctly the first time. Whatever brought you here — a new business, a new property, a new country, or just a new season of life — accurate tax preparation is how you protect what you’ve earned.", "Para muchas familias del Valle Central, hay un obstáculo más: presentar sin número de Seguro Social. Como especialistas certificados en solicitudes de ITIN, ayudamos a los contribuyentes sin SSN a configurarse correctamente desde la primera vez. Lo que sea que le haya traído aquí — un nuevo negocio, una nueva propiedad, un nuevo país o simplemente una nueva etapa de vida — la preparación precisa de impuestos es como protege lo que ha ganado."),
    ("Fully credentialed and locally owned in Fresno — your neighbors, not a national chain.", "Completamente acreditados y de propiedad local en Fresno — sus vecinos, no una cadena nacional."),
    ("Here’s the tricky part: many people don’t know which type of fingerprinting they need. California agencies usually want a digital Livescan submission, which sends your prints straight to the DOJ. But out-of-state employers and federal agencies often ask for a physical FD-258 fingerprint card instead. Show up at the wrong place with the wrong form, and you can lose a day. Sometimes a whole week.", "Aquí está la parte complicada: muchas personas no saben qué tipo de huellas dactilares necesitan. Las agencias de California generalmente quieren un envío digital Livescan, que envía sus huellas directamente al DOJ. Pero los empleadores fuera del estado y las agencias federales a menudo piden una tarjeta de huellas dactilares física FD-258. Llegar al lugar equivocado con el formulario equivocado puede hacerle perder un día. A veces toda una semana."),
    ("If an old return needs fixing, our tax amendment service sets the record straight. And if life simply got in the way this year, we can file your tax extension quickly so you get breathing room without late-filing penalties.", "Si una declaración antigua necesita corrección, nuestro servicio de enmiendas fiscales pone el registro en orden. Y si la vida simplemente se interpuso este año, podemos presentar su extensión fiscal rápidamente para que tenga margen sin penalidades por presentación tardía."),
    ("If we make an error on your return, we cover the adjustment costs and amend it for free.", "Si cometemos un error en su declaración, cubrimos los costos del ajuste y la enmendamos gratis."),
    ("If you don’t have a Social Security number, filing taxes can feel like a door that’s closed to you. It isn’t. C&R Tax Services provides professional support for ITIN applications, helping non-SSN filers in Fresno get the Individual Taxpayer Identification Number they need to file correctly and claim eligible credits.", "Si no tiene un número de Seguro Social, presentar impuestos puede sentirse como una puerta cerrada. No lo está. C&R Tax Services brinda apoyo profesional para solicitudes de ITIN, ayudando a los contribuyentes sin SSN en Fresno a obtener el Número de Identificación del Contribuyente Individual que necesitan para presentar correctamente y reclamar créditos elegibles."),
    ("If you own rental property, we dig even deeper — Schedule E filings, depreciation, and the rules around passive income, tracked carefully so your rental income works for you instead of against you.", "Si posee propiedades en alquiler, profundizamos aún más — presentaciones del Anexo E, depreciación y las reglas sobre ingresos pasivos, rastreados cuidadosamente para que sus ingresos de alquiler trabajen a su favor en lugar de en contra."),
    ("If you’ve been searching for Fresno tax preparation that actually feels personal, we’d love to be the last search you make. Come by for a friendly, no-pressure conversation about your taxes, your business, or your goals for next year — no jargon, no surprises, just honest help from people who genuinely care.", "Si ha estado buscando preparación de impuestos en Fresno que realmente se sienta personal, nos encantaría ser la última búsqueda que haga. Pase para una conversación amigable y sin presión sobre sus impuestos, su negocio o sus metas para el próximo año — sin jerga, sin sorpresas, solo ayuda honesta de personas que genuinamente se preocupan."),
    ("It’s the small business owner who stopped dreading quarterly deadlines. It’s the family who fixed a prior-year mistake and recovered money they didn’t know they’d lost. It’s the ITIN applicant who filed correctly the first time instead of waiting months on a rejected application. When your taxes are done right, you get your time, your money, and your calm back.", "Es el dueño de un pequeño negocio que dejó de temer las fechas límite trimestrales. Es la familia que corrigió un error de un año anterior y recuperó dinero que no sabía que había perdido. Es el solicitante de ITIN que presentó correctamente la primera vez en lugar de esperar meses por una solicitud rechazada. Cuando sus impuestos se hacen correctamente, recupera su tiempo, su dinero y su tranquilidad."),
    ("Kept on every transaction, just as California law requires, so there’s always a record protecting you.", "Se mantiene en cada transacción, tal como lo requiere la ley de California, para que siempre haya un registro que le proteja."),
    ("Life has a way of handing you paperwork at the worst possible moments. Maybe you’re closing on a home in Fresno or Clovis and the lender needs a certified loan signing agent before the deal can fund. Maybe a parent’s health is declining and your family needs a power of attorney notarized this week, not next month. Or maybe your child is flying to visit family in Mexico, and the airline won’t let them board without a notarized travel consent letter.", "La vida tiene una manera de entregarle papeleo en los peores momentos posibles. Quizás está cerrando una casa en Fresno o Clovis y el prestamista necesita un agente certificado de firma de préstamos antes de que el trato pueda financiarse. Quizás la salud de un padre está decayendo y su familia necesita un poder notarial notarizado esta semana, no el mes que viene. O quizás su hijo viaja a visitar a la familia en México y la aerolínea no le dejará abordar sin una carta de consentimiento de viaje notarizada."),
    ("Many of our notary clients first found us through our tax work, and that’s no coincidence. The same people who need help with tax preparation in Fresno often need an ITIN form certified, a bank document witnessed, or real estate paperwork signed and sealed. Having one trusted local office for both means fewer trips and a lot less stress.", "Muchos de nuestros clientes de notaría nos encontraron primero a través de nuestro trabajo de impuestos, y eso no es casualidad. Las mismas personas que necesitan ayuda con la preparación de impuestos en Fresno a menudo necesitan un formulario ITIN certificado, un documento bancario testificado o papeleo de bienes raíces firmado y sellado. Tener una sola oficina local de confianza para ambos significa menos viajes y mucho menos estrés."),
    ("Most people don’t call a tax professional when things are going smoothly. They call because something changed — a side business, a delivery-app job, a rental property in Clovis with a Schedule E they’ve never filed, or a mid-year move to California that turned into a multi-state return their old software can’t handle.", "La mayoría de las personas no llaman a un profesional de impuestos cuando todo va bien. Llaman porque algo cambió — un negocio secundario, un trabajo de aplicación de entregas, una propiedad en alquiler en Clovis con un Anexo E que nunca han presentado, o una mudanza a mitad de año a California que se convirtió en una declaración multi-estado que su viejo software no puede manejar."),
    ("Need something notarized for a real estate deal, a power of attorney, or a business agreement? We handle it promptly. Closing on a loan? Our certified loan signing service walks you through the entire signing package. Applying for a job or license that requires a background check? Our state-compliant Live Scan fingerprinting captures and submits your prints correctly the first time.", "¿Necesita algo notarizado para una transacción de bienes raíces, un poder notarial o un acuerdo comercial? Lo manejamos con prontitud. ¿Cerrando un préstamo? Nuestro servicio certificado de firma de préstamos le guía por todo el paquete de firma. ¿Solicitando un trabajo o licencia que requiere verificación de antecedentes? Nuestras huellas dactilares Live Scan compatibles con el estado capturan y envían sus huellas correctamente desde la primera vez."),
    ("One thing that sets us apart is our Spanish-language tax preparation. For thousands of Central Valley families, taxes are stressful enough without a language barrier in the middle of it. Here, you can explain your situation, ask every question on your mind, and understand every line of your return completely in Spanish.", "Lo que nos distingue es nuestra preparación de impuestos en español. Para miles de familias del Valle Central, los impuestos son suficientemente estresantes sin una barrera del idioma en medio. Aquí puede explicar su situación, hacer cada pregunta que tenga en mente y entender cada línea de su declaración completamente en español."),
    ("Others come to us after a mistake has already happened: a missed form, a return filed under the wrong status, an IRS notice sitting unopened on the kitchen counter. Professional tax preparation solves these problems before they grow. We handle amendments to fix past returns, extensions when you need more time, prior-year reviews to recover money you may have left on the table, and audit support when a notice arrives and you need someone in your corner.", "Otros vienen a nosotros después de que ya ocurrió un error: un formulario perdido, una declaración presentada con el estado incorrecto, un aviso del IRS sin abrir en el mostrador de la cocina. La preparación profesional de impuestos resuelve estos problemas antes de que crezcan. Manejamos enmiendas para corregir declaraciones pasadas, extensiones cuando necesita más tiempo, revisiones de años anteriores para recuperar dinero que puede haber dejado sobre la mesa y soporte de auditoría cuando llega un aviso y necesita a alguien de su lado."),
    ("Our equipment and process meet California DOJ standards, which means clean captures and fewer rejected prints. And if an agency ever sends a submission back for image quality, we make it right. We also keep our pricing clear and upfront, just like we do with our tax and notary services. You’ll know exactly what your visit costs before we ever touch the scanner.", "Nuestro equipo y proceso cumplen con los estándares del DOJ de California, lo que significa capturas limpias y menos huellas rechazadas. Y si una agencia alguna vez devuelve un envío por calidad de imagen, lo corregimos. También mantenemos nuestros precios claros y transparentes, al igual que con nuestros servicios de impuestos y notaría. Sabrá exactamente cuánto costará su visita antes de que toquemos el escáner."),
    ("Plenty of places in Fresno can stamp a document. What sets us apart is how we treat the person holding it. You call or book online, and we tell you exactly what to bring. When you arrive, we take our time — we check every page, confirm every name matches, and make sure each signature lands exactly where it belongs. One missed initial on a loan package can delay a closing by days, so we don’t leave anything to chance.", "Muchos lugares en Fresno pueden sellar un documento. Lo que nos distingue es cómo tratamos a la persona que lo sostiene. Usted llama o reserva en línea y le decimos exactamente qué traer. Cuando llega, nos tomamos nuestro tiempo — revisamos cada página, confirmamos que cada nombre coincide y nos aseguramos de que cada firma esté exactamente donde corresponde. Una inicial faltante en un paquete de préstamo puede retrasar un cierre días, así que no dejamos nada al azar."),
    ("Rejected prints and wrong forms can set your plans back by weeks, and almost all of those delays are avoidable. Call us, stop by our Fresno office, or send us your details below. Walk-ins are welcome — just bring your request form and a valid photo ID. ¡Se habla español! Llámenos hoy.", "Las huellas rechazadas y los formularios incorrectos pueden retrasar sus planes semanas, y casi todos esos retrasos son evitables. Llámenos, visítenos en nuestra oficina en Fresno o envíenos sus datos a continuación. Se aceptan sin cita — solo traiga su formulario de solicitud y una identificación fotográfica válida. ¡Se habla español! Llámenos hoy."),
    ("Running a business in the Central Valley is demanding enough without the IRS piling onto your to-do list. Between quarterly estimates, payroll questions, entity rules, and California’s own layer of requirements, small business taxes can eat up hours you don’t have.", "Dirigir un negocio en el Valle Central es suficientemente exigente sin que el IRS se agregue a su lista de tareas. Entre las estimaciones trimestrales, las preguntas sobre nómina, las reglas de entidad y los requisitos propios de California, los impuestos de pequeños negocios pueden consumir horas que no tiene."),
    ("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&R Tax Services is ready when you are. Have a question? Just ask — that’s what neighbors are for.", "Sirviendo a Fresno, Clovis, Selma, Reedley, Sanger y Madera, C&R Tax Services está listo cuando usted lo esté. ¿Tiene una pregunta? Solo pregunte — para eso están los vecinos."),
    ("So you just found out you need fingerprints. Maybe it’s for a new job, a license, or a certification. The deadline is close, and you’re not sure where to go. Some places make you wait days for an appointment. Others rush you through the door and leave you wondering if it was even done right. When your career is on the line, guessing isn’t good enough.", "Así que acaba de enterarse de que necesita huellas dactilares. Quizás es para un nuevo trabajo, una licencia o una certificación. La fecha límite está cerca y no sabe a dónde ir. Algunos lugares le hacen esperar días para una cita. Otros le hacen pasar rápido y le dejan preguntándose si siquiera se hizo correctamente. Cuando su carrera está en juego, adivinar no es suficiente."),
    ("Tax Season Doesn’t Have to Be Stressful.", "La Temporada de Impuestos No Tiene que Ser Estresante."),
    ("Tax questions don’t get easier by waiting — but they do get easier with the right team in your corner. Call now or reach out below. A local, professional team you can actually talk to will take the stress off your plate.", "Las preguntas de impuestos no se hacen más fáciles esperando — pero sí se hacen más fáciles con el equipo correcto de su lado. Llame ahora o contáctenos a continuación. Un equipo local y profesional con el que realmente puede hablar le quitará el estrés de encima."),
    ("Tax season has a way of sneaking up on you. One day life is moving along just fine, and the next you’re sitting at the kitchen table with a stack of W-2s, 1099s, and maybe a letter from the IRS, wondering if you’re missing something. If you’ve ever felt that knot in your stomach in early spring, you’re in good company.", "La temporada de impuestos tiene una manera de sorprenderle. Un día la vida va bien y al siguiente está sentado en la mesa de la cocina con una pila de W-2, 1099 y quizás una carta del IRS, preguntándose si le falta algo. Si alguna vez ha sentido ese nudo en el estómago a principios de primavera, está en buena compañía."),
    ("Tax season has a way of sneaking up on you. One day you’re enjoying the holidays. The next, you’re staring at a pile of W-2s, 1099s, and receipts, wondering if you’re about to miss a deduction — or worse, make a mistake that brings a letter from the IRS. Families and business owners all over Fresno feel that knot in their stomach every year.", "La temporada de impuestos tiene una manera de sorprenderle. Un día está disfrutando las fiestas. Al siguiente, está mirando una pila de W-2, 1099 y recibos, preguntándose si está a punto de perder una deducción — o peor, cometer un error que traiga una carta del IRS. Familias y dueños de negocios en todo Fresno sienten ese nudo en el estómago cada año."),
    ("Tax season shouldn’t feel like a guessing game — but for too many Central Valley families, that’s exactly what it’s become.", "La temporada de impuestos no debería sentirse como un juego de adivinanzas — pero para demasiadas familias del Valle Central, eso es exactamente lo que se ha convertido."),
    ("Tax season shouldn’t feel like a guessing game. But for too many families and small business owners here in the Central Valley, that’s exactly what it’s become — confusing software, pop-up franchise offices that disappear on April 16th, and preparers who rush you out the door without ever explaining what they filed on your behalf. C&R Tax Services was founded to be the opposite of all that.", "La temporada de impuestos no debería sentirse como un juego de adivinanzas. Pero para demasiadas familias y dueños de pequeños negocios aquí en el Valle Central, eso es exactamente lo que se ha convertido — software confuso, oficinas de franquicia temporales que desaparecen el 16 de abril y preparadores que le sacan rápido sin explicar nunca lo que presentaron en su nombre. C&R Tax Services fue fundado para ser todo lo contrario."),
    ("Taxes aren’t the only paperwork life throws your way. C&R Tax Services also serves Fresno as a Notary Public and Loan Signing Agent and provides Live Scan fingerprint services — a convenient one-stop shop for the documents and verifications that keep your life and business moving.", "Los impuestos no son el único papeleo que la vida le depara. C&R Tax Services también sirve a Fresno como Notario Público y Agente de Firma de Préstamos y brinda servicios de huellas dactilares Live Scan — una conveniente ventanilla única para los documentos y verificaciones que mantienen su vida y negocio en movimiento."),
    ("That’s the outcome we aim for every single time: peace of mind. Whether it’s a nurse renewing a license, a new notary getting commissioned, or a parent completing a foster care application, our clients leave knowing their fingerprints were captured correctly and sent where they need to go. No re-dos, no lost time, no surprises.", "Ese es el resultado que buscamos cada vez: tranquilidad. Ya sea una enfermera renovando su licencia, un nuevo notario siendo comisionado o un padre completando una solicitud de cuidado de crianza, nuestros clientes se van sabiendo que sus huellas fueron capturadas correctamente y enviadas a donde deben ir. Sin repeticiones, sin tiempo perdido, sin sorpresas."),
    ("That’s where C&R Tax Services comes in. We’re a local Fresno office offering notary public and loan signing agent services for bank documents, real estate paperwork, powers of attorney, travel documents, and legal forms of every kind. Because we’re also a full tax preparation office, handling sensitive paperwork isn’t a side gig for us — it’s what we do all day, every day.", "Ahí es donde entra C&R Tax Services. Somos una oficina local en Fresno que ofrece servicios de notario público y agente de firma de préstamos para documentos bancarios, papeleo de bienes raíces, poderes notariales, documentos de viaje y formularios legales de todo tipo. Porque también somos una oficina completa de preparación de impuestos, manejar papeleo confidencial no es un trabajo secundario para nosotros — es lo que hacemos todo el día, todos los días."),
    ("That’s why workers, families, and business owners across Fresno choose a provider that handles it all. As a full service fingerprints location, we take care of Livescan submissions, Livescan background checks, and FD-258 ink cards in one visit. You bring your request form, and we handle the rest. No bouncing between offices, and no wondering whether the fingerprints Fresno agencies require were submitted the right way.", "Por eso trabajadores, familias y dueños de negocios en todo Fresno eligen un proveedor que lo maneja todo. Como ubicación de servicio completo de huellas, nos encargamos de los envíos Livescan, las verificaciones de antecedentes Livescan y las tarjetas de tinta FD-258 en una sola visita. Usted trae su formulario de solicitud y nosotros nos encargamos del resto. Sin ir de una oficina a otra y sin preguntarse si las huellas que requieren las agencias de Fresno fueron enviadas correctamente."),
    ("The Best Notary in the Central Valley — Fast, Friendly, and Right Here in Fresno", "El Mejor Notario del Valle Central — Rápido, Amigable y Aquí Mismo en Fresno"),
    ("The Best Tax Preparation in the Central Valley — Without the Stress, Surprises, or Confusing Fine Print", "La Mejor Preparación de Impuestos del Valle Central — Sin el Estrés, Sorpresas ni Letra Pequeña Confusa"),
    ("The forms aren’t getting simpler and California’s rules aren’t getting easier. You deserve a friendly, local expert who does this every day, explains everything clearly, and guarantees the work. Call C&R Tax Services to schedule your appointment, or send us a message below. Se habla español.", "Los formularios no se están simplificando y las reglas de California no se están facilitando. Merece un experto local y amigable que haga esto todos los días, explique todo claramente y garantice el trabajo. Llame a C&R Tax Services para programar su cita o envíenos un mensaje a continuación. Se habla español."),
    ("The moments right after a notarization are often the best part of our job. We’ve watched a daughter breathe a sigh of relief after finalizing a power of attorney, knowing she could finally manage her mother’s care without one more legal roadblock. We’ve seen first-time homebuyers walk out of a loan signing and tell us it was the first time in the entire process someone actually explained what they were signing.", "Los momentos justo después de una notarización son a menudo la mejor parte de nuestro trabajo. Hemos visto a una hija respirar aliviada después de finalizar un poder notarial, sabiendo que finalmente podría manejar el cuidado de su madre sin otro obstáculo legal. Hemos visto a compradores de vivienda por primera vez salir de una firma de préstamo y decirnos que fue la primera vez en todo el proceso que alguien realmente les explicó lo que estaban firmando."),
    ("The paperwork you’ve been waiting on finally arrived — maybe a loan packet, a power of attorney, or travel consent forms for your kids. There’s just one catch: none of it counts until it’s notarized. Now you’re stuck searching for someone who can do it right, do it soon, and not make you feel rushed or confused along the way.", "El papeleo que esperaba finalmente llegó — quizás un paquete de préstamo, un poder notarial o formularios de consentimiento de viaje para sus hijos. Solo hay un inconveniente: nada de eso cuenta hasta que esté notarizado. Ahora está buscando a alguien que pueda hacerlo bien, hacerlo pronto y no hacerle sentir apurado o confundido en el proceso."),
    ("There’s no shortage of ways to get your taxes done in Fresno. Big-box franchises pop up every January, and online software promises easy filing in minutes. So why do local families and business owners keep choosing C&R Tax Services? Because we offer something those options can’t: a real, local professional who knows your name, answers your questions honestly, and treats your return like it matters. Because it does.", "No faltan formas de hacer sus impuestos en Fresno. Las grandes franquicias aparecen cada enero y el software en línea promete una presentación fácil en minutos. Entonces, ¿por qué las familias y dueños de negocios locales siguen eligiendo C&R Tax Services? Porque ofrecemos algo que esas opciones no pueden: un profesional local real que conoce su nombre, responde sus preguntas honestamente y trata su declaración como si importara. Porque importa."),
    ("These aren’t just words on a website. They show up in the small things: answering questions patiently, being available year-round, and never treating you like a number in a queue. Because to us, you’re not a transaction — you’re a neighbor.", "Estas no son solo palabras en un sitio web. Se manifiestan en las pequeñas cosas: responder preguntas con paciencia, estar disponibles todo el año y nunca tratarle como un número en una fila. Porque para nosotros, usted no es una transacción — es un vecino."),
    ("These aren’t rare situations. They’re everyday moments for Central Valley families, and every one comes with a deadline. When a signature is missing or a stamp is done wrong, closings get delayed, court filings get rejected, and travel plans fall apart. A good notary does more than witness a signature — they protect you from expensive do-overs.", "Estas no son situaciones raras. Son momentos cotidianos para las familias del Valle Central y cada uno viene con una fecha límite. Cuando falta una firma o un sello se hace mal, los cierres se retrasan, las presentaciones judiciales se rechazan y los planes de viaje se desmoronan. Un buen notario hace más que atestiguar una firma — le protege de costosas repeticiones."),
    ("Upload your documents from Fresno, Clovis, Sanger, Selma, or Madera and file without hunting for parking.", "Suba sus documentos desde Fresno, Clovis, Sanger, Selma o Madera y presente sin buscar estacionamiento."),
    ("We also believe in doing business the straightforward way: upfront, transparent pricing, accuracy you can count on, and year-round support. With us, you’re never a ticket number in a queue. You’re a neighbor, and we treat you like one.", "También creemos en hacer negocios de manera directa: precios transparentes, precisión en la que puede confiar y soporte todo el año. Con nosotros, nunca es un número de ticket en una fila. Es un vecino y le tratamos como tal."),
    ("We also prepare multi-state returns for anyone who earned income in more than one state — sorting out exactly what each state is owed so you never pay twice or file incorrectly.", "También preparamos declaraciones multi-estado para cualquier persona que haya ganado ingresos en más de un estado — determinando exactamente lo que se le debe a cada estado para que nunca pague dos veces ni presente incorrectamente."),
    ("We built this firm for the Central Valley — for the farm families, the small business owners, the young professionals, and the hardworking households that keep this region running. When you sit down with us, in person or online, you get local knowledge of California tax rules paired with the patience to actually explain them.", "Construimos esta empresa para el Valle Central — para las familias agricultoras, los dueños de pequeños negocios, los jóvenes profesionales y los hogares trabajadores que mantienen esta región en marcha. Cuando se sienta con nosotros, en persona o en línea, obtiene conocimiento local de las reglas fiscales de California combinado con la paciencia para realmente explicarlas."),
    ("We do it differently. At C&R Tax Services, we sit down with you, in person or virtually, and walk through your full financial picture together, and make sure every credit and deduction you’re entitled to actually lands on your return.", "Lo hacemos diferente. En C&R Tax Services, nos sentamos con usted, en persona o virtualmente, y repasamos juntos su panorama financiero completo, asegurándonos de que cada crédito y deducción al que tiene derecho realmente aparezca en su declaración."),
    ("We explain your return in plain language, and offer both in-person and secure virtual tax preparation — so getting your taxes done right fits into your life.", "Explicamos su declaración en lenguaje sencillo y ofrecemos preparación de impuestos tanto en persona como virtual segura — para que hacer sus impuestos correctamente se adapte a su vida."),
    ("We stand behind every return we prepare. If we make an error, we make it right — covering the adjustment costs and amending your return at no charge.", "Respaldamos cada declaración que preparamos. Si cometemos un error, lo corregimos — cubriendo los costos del ajuste y enmendando su declaración sin cargo."),
    ("We started this firm right here in Fresno because we believe our neighbors deserve a tax preparer who actually knows them — someone who picks up the phone in July when an IRS letter shows up, not just in March when a refund is on the line. Our roots are in this community. We shop where you shop, our kids go to the same schools, and we understand the real financial pressures Central Valley families face.", "Fundamos esta empresa aquí mismo en Fresno porque creemos que nuestros vecinos merecen un preparador de impuestos que realmente los conozca — alguien que conteste el teléfono en julio cuando llega una carta del IRS, no solo en marzo cuando hay un reembolso en juego. Nuestras raíces están en esta comunidad. Compramos donde usted compra, nuestros hijos van a las mismas escuelas y entendemos las verdaderas presiones financieras que enfrentan las familias del Valle Central."),
    ("What This Service Solves", "Qué Resuelve Este Servicio"),
    ("When we’re not helping clients, you’ll find us involved in the community we serve — because we’re not just building a business in Fresno, we’re building relationships that last well beyond tax season.", "Cuando no estamos ayudando a clientes, nos encontrará involucrados en la comunidad a la que servimos — porque no solo estamos construyendo un negocio en Fresno, estamos construyendo relaciones que duran mucho más allá de la temporada de impuestos."),
    ("Whether it’s a loan closing on the calendar, a power of attorney your family needs this week, or travel documents that must be certified before a flight, the fastest way to stop worrying is to get it done right, the first time. Call C&R Tax Services today, or send us the details below and we’ll tell you exactly what to bring. Se habla español.", "Ya sea un cierre de préstamo en el calendario, un poder notarial que su familia necesita esta semana o documentos de viaje que deben certificarse antes de un vuelo, la forma más rápida de dejar de preocuparse es hacerlo bien desde la primera vez. Llame a C&R Tax Services hoy o envíenos los detalles a continuación y le diremos exactamente qué traer. Se habla español."),
    ("Whether you need straightforward individual tax preparation, full small business and corporate tax support, help with an ITIN application, or a calm, fast answer to a scary IRS letter, C&R Tax Services is ready, in English or Spanish, in our office or completely online.", "Ya sea que necesite preparación de impuestos individual sencilla, soporte completo de impuestos para pequeños negocios y corporaciones, ayuda con una solicitud de ITIN o una respuesta tranquila y rápida a una aterradora carta del IRS, C&R Tax Services está listo, en inglés o español, en nuestra oficina o completamente en línea."),
    ("Full-service preparation for individuals, small businesses, and every filing situation in between — plus virtual and online tax preparation, available any day, all year.", "Preparación completa para individuos, pequeños negocios y cada situación fiscal intermedia — más preparación de impuestos virtual y en línea, disponible cualquier día, todo el año."),
    ("A lot of fingerprinting spots treat you like a number. You wait in line, get rolled through the process, and leave with a receipt and zero explanation. We do things differently. When you visit our Fresno office, a real person walks you through every step. We check your request form before we scan, so common mistakes — a wrong ORI code or a missing applicant type — get caught before they cost you a rejection.", "Muchos lugares de huellas dactilares le tratan como un número. Espera en la fila, lo hacen pasar por el proceso y sale con un recibo y cero explicación. Nosotros hacemos las cosas diferente. Cuando visita nuestra oficina en Fresno, una persona real le guía en cada paso. Revisamos su formulario de solicitud antes de escanear, para que los errores comunes — un código ORI incorrecto o un tipo de solicitante faltante — se detecten antes de que le cuesten un rechazo."),
]

print(f"Total translation pairs to insert: {len(TRANSLATIONS)}")

# Clear old dictionary and insert new correct ones
print("\nClearing old dictionary...")
clear_result = php("""
global $wpdb;
$table = $wpdb->prefix . 'trp_dictionary_en_us_es_es';
$wpdb->query("TRUNCATE TABLE $table");
return array('cleared' => true);
""")
print("Cleared:", clear_result.get("return_value", clear_result))

# Insert in batches
BATCH = 40
total_inserted = 0
for i in range(0, len(TRANSLATIONS), BATCH):
    batch = TRANSLATIONS[i:i+BATCH]
    rows = []
    for orig, trans in batch:
        o = orig.replace("\\", "\\\\").replace("'", "\\'")
        t = trans.replace("\\", "\\\\").replace("'", "\\'")
        rows.append(f"('{o}', '{t}', 1, 2, NOW())")
    values_sql = ",\n".join(rows)
    insert_code = f"""
global $wpdb;
$table = $wpdb->prefix . 'trp_dictionary_en_us_es_es';
$sql = "INSERT INTO $table (original, translated, status, block_type, modified) VALUES {values_sql}
ON DUPLICATE KEY UPDATE translated=VALUES(translated), status=1, modified=NOW()";
$wpdb->query($sql);
return array('batch' => {i//BATCH+1}, 'err' => $wpdb->last_error);
"""
    result = php(insert_code)
    rv = result.get("return_value", result)
    total_inserted += len(batch)
    err = rv.get("err", "")
    print(f"  Batch {i//BATCH+1}: {len(batch)} pairs | err: {err[:60] if err else 'none'}")

print(f"\nTotal inserted: {total_inserted}")

# Verify count
count_result = php("""
global $wpdb;
$table = $wpdb->prefix . 'trp_dictionary_en_us_es_es';
$count = (int)$wpdb->get_var("SELECT COUNT(*) FROM $table WHERE status=1");
return array('approved_translations' => $count);
""")
print("DB count:", count_result.get("return_value", count_result))

# Clear all caches
php("""
do_action('breeze_clear_all_cache');
if (function_exists('wp_cache_flush')) { wp_cache_flush(); }
return true;
""")
print("\nCaches cleared. Done!")
