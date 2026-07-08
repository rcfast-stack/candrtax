#!/usr/bin/env python3
"""
C&R Tax Services — v8 Form Update
- Creates a WPForms contact form (Name, Phone, Email, Service, Message)
- Contact page (post 38): adds form + contact info layout in "How to Reach Us"
- Income Tax (post 28): replaces final CTA with two-column text+form layout
- Notary (post 29): same
- Livescan (post 30): same
"""
import json, random, string, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

NAVY       = "#1B2A5E"; ROYAL_BLUE = "#0A4A93"; RED   = "#E23A28"
ICE_BLUE   = "#EAF0F8"; OFF_WHITE  = "#F7F8FA"
WHITE      = "#FFFFFF"; BORDER     = "#D7DEEA"; SURFACE_ALT = "#F7F8FA"
SURFACE_CARD = "#FFFFFF"
TEXT_BODY  = "#374151"; TEXT_HEAD  = "#111827"; TEXT_MUTED = "#6B7280"
SP = {6:24,8:32,10:40,12:48,20:80,24:96}
T  = {"sm":15,"base":17,"lg":20,"2xl":30,"3xl":38,"4xl":50}

# ── MCP ──────────────────────────────────────────────────────────────────────
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
    parsed = json.loads(r.json()["result"]["content"][0]["text"])
    return parsed.get("data", parsed)

def write_file(path, content):
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess()}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/write-file",
                               "parameters":{"path":path,"content":content}}}
    })
    result = json.loads(r.json()["result"]["content"][0]["text"])
    return result.get("data", result)

# ── Elementor helpers ─────────────────────────────────────────────────────────
def uid(): return "".join(random.choices(string.ascii_lowercase+string.digits, k=7))

def wgt(wtype, settings):
    return {"id": uid(), "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": []}

def con(settings, elements, is_inner=True):
    return {"id": uid(), "elType": "container", "isInner": is_inner,
            "settings": settings, "elements": elements}

def pad(t, r, b, l, u="px"):
    return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}

def size(v, u="px"):
    return {"size": v, "unit": u}

def gap(v, unit="px"):
    return {"column": v, "row": v, "unit": unit, "isLinked": True}

def text(html):
    return wgt("text-editor", {"editor": html})

def spacer(h):
    return wgt("spacer", {"space": size(h)})

def shortcode_widget(code):
    return wgt("shortcode", {"shortcode": code})

def p_html(t, last=False):
    mb = "0" if last else "16px"
    return (f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
            f'color:{TEXT_BODY};margin:0 0 {mb};">{t}</p>')

def p_inv(t, last=False):
    mb = "0" if last else "28px"
    return (f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
            f'color:{ICE_BLUE};margin:0 0 {mb};max-width:500px;">{t}</p>')

def h2_inv(t):
    return (f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
            f'color:{WHITE};margin:0 0 16px;">{t}</h2>')

def btn_link(label, href, primary=True):
    if primary:
        bg, color, border = RED, WHITE, RED
    else:
        bg, color, border = "transparent", WHITE, WHITE
    return (f'<a href="{href}" style="display:inline-flex;align-items:center;gap:8px;'
            f'background:{bg};color:{color};border:2px solid {border};'
            f'font-family:Inter,sans-serif;font-weight:600;font-size:17px;'
            f'padding:14px 28px;border-radius:8px;text-decoration:none;">'
            f'<i class="fas fa-phone" style="font-size:16px;"></i> {label}</a>')

def icon_box_html(icon_fa):
    return (f'<div style="width:40px;height:40px;border-radius:10px;background:{NAVY};'
            f'display:flex;align-items:center;justify-content:center;margin-bottom:12px;">'
            f'<i class="fas fa-{icon_fa}" style="font-size:20px;color:{OFF_WHITE};"></i>'
            f'</div>')

def diff_card_html(icon_fa, title, body):
    return (f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
            f'border-radius:10px;padding:24px;">'
            f'{icon_box_html(icon_fa)}'
            f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
            f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
            f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{TEXT_BODY};'
            f'line-height:1.6;margin:0;">{body}</p>'
            f'</div>')

def diff_grid_html(cards):
    cards_html = "".join(diff_card_html(*c) for c in cards)
    return text(
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));'
        f'gap:24px;margin-top:32px;margin-bottom:32px;">{cards_html}</div>'
    )

def city_pills_html(cities):
    pills = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
        f'border-radius:999px;background:{SURFACE_ALT};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-map-marker-alt" style="font-size:14px;color:{ROYAL_BLUE};"></i>'
        f'{c}</span>'
        for c in cities
    )
    return text(f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px;">{pills}</div>')

def contact_card_html():
    rows = [
        ("map-marker-alt", "1320 N. Van Ness Ave, Fresno CA 93702", "Near Tower District", None),
        ("phone", "(559) 962-7503", None, "tel:5599627503"),
        ("envelope", "info@candrtaxservices.com", None, "mailto:info@candrtaxservices.com"),
        ("globe", "www.candrtaxservices.com", None, "https://www.candrtaxservices.com"),
    ]
    rows_html = ""
    for icon_fa, label, sub, href in rows:
        lbl = (f'<a href="{href}" style="color:{ROYAL_BLUE};font-weight:600;font-size:17px;text-decoration:none;">{label}</a>'
               if href else f'<div style="color:{TEXT_BODY};font-weight:600;font-size:17px;">{label}</div>')
        sub_html = f'<div style="color:{TEXT_MUTED};font-size:15px;">{sub}</div>' if sub else ""
        rows_html += (
            f'<div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:20px;">'
            f'<div style="width:36px;height:36px;border-radius:10px;background:{SURFACE_ALT};'
            f'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<i class="fas fa-{icon_fa}" style="font-size:18px;color:{ROYAL_BLUE};"></i>'
            f'</div><div>{lbl}{sub_html}</div></div>'
        )
    return (f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
            f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:32px;">'
            f'{rows_html}</div>')

def hours_card_html(season="tax"):
    if season == "tax":
        label, rng = "Tax Season", "January – April"
        rows = [("Monday – Saturday", "9am – 7pm"), ("Sunday", "10am – 6pm")]
        badge_color = RED
    else:
        label, rng = "After Tax Season", "May – December"
        rows = [("Monday – Friday", "10am – 6pm"), ("Saturday – Sunday", "By Appointment Only")]
        badge_color = "#5A6B8C"
    rows_html = "".join(
        f'<tr style="border-top:1px solid {BORDER};">'
        f'<td style="padding:10px 0;color:{TEXT_BODY};font-size:15px;font-weight:500;">{d}</td>'
        f'<td style="padding:10px 0;color:{TEXT_MUTED};font-size:15px;text-align:right;">{h}</td>'
        f'</tr>'
        for d, h in rows
    )
    return (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:32px;margin-top:24px;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'flex-wrap:wrap;gap:8px;margin-bottom:16px;">'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:700;font-size:20px;'
        f'color:{TEXT_HEAD};margin:0;">{label}</h3>'
        f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;'
        f'background:{badge_color};color:{WHITE};font-family:Inter,sans-serif;'
        f'font-size:13px;font-weight:600;">{rng}</span></div>'
        f'<table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;">'
        f'<tbody>{rows_html}</tbody></table>'
        f'<p style="margin:12px 0 0;font-size:13px;color:{TEXT_MUTED};font-style:italic;">'
        f'After Hours — By Appointment Only</p></div>'
    )

# ── Form card wrapper (white card on navy bg) ─────────────────────────────────

def form_card(form_id, title, subtitle):
    header = (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:16px 16px 0 0;padding:28px 28px 0;">'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:700;font-size:20px;'
        f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
        f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{TEXT_MUTED};'
        f'line-height:1.5;margin:0 0 20px;">{subtitle}</p></div>'
    )
    footer = (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-top:none;border-radius:0 0 16px 16px;padding:0 28px 8px;">'
        f'<p style="font-family:Inter,sans-serif;font-size:13px;color:{TEXT_MUTED};'
        f'text-align:center;margin:0 0 16px;">Prefer to talk? Call us at '
        f'<a href="tel:5599627503" style="color:{ROYAL_BLUE};font-weight:600;">'
        f'(559) 962-7503</a>.</p></div>'
    )
    # The form shortcode goes in a div with matching style
    form_wrapper_open = (
        f'<div style="background:{SURFACE_CARD};border-left:1px solid {BORDER};'
        f'border-right:1px solid {BORDER};padding:0 28px;">'
    )
    form_wrapper_close = '</div>'
    return [
        text(header),
        text(form_wrapper_open),
        shortcode_widget(f'[wpforms id="{form_id}"]'),
        text(form_wrapper_close + footer),
    ]

# ── WPForms form creation ────────────────────────────────────────────────────

def create_or_get_form():
    result = php("""
$title = 'Contact Form - CR Tax Services';

// Check if already exists
$existing = get_posts([
    'post_type'   => 'wpforms',
    'post_status' => 'any',
    'numberposts' => 1,
    'title'       => $title,
]);
if ($existing) {
    return ['form_id' => (int)$existing[0]->ID, 'created' => false];
}

// Create via wp_insert_post
$form_id = wp_insert_post([
    'post_type'    => 'wpforms',
    'post_title'   => $title,
    'post_status'  => 'publish',
    'post_content' => '',
]);

if (is_wp_error($form_id)) {
    return ['error' => $form_id->get_error_message()];
}

$form_data = [
    'id'       => $form_id,
    'field_id' => 5,
    'fields'   => [
        '1' => ['id'=>'1','type'=>'name','label'=>'Name','format'=>'simple',
                'required'=>'1','size'=>'medium'],
        '2' => ['id'=>'2','type'=>'phone','label'=>'Phone (optional)',
                'required'=>'0','size'=>'medium','placeholder'=>'(559) 000-0000'],
        '3' => ['id'=>'3','type'=>'email','label'=>'Email',
                'required'=>'1','size'=>'medium','placeholder'=>'you@example.com'],
        '4' => ['id'=>'4','type'=>'select','label'=>'What do you need help with?',
                'choices'=>[
                    ['label'=>'Income Tax Preparation','value'=>'Income Tax Preparation'],
                    ['label'=>'Notary Services','value'=>'Notary Services'],
                    ['label'=>'Livescan Fingerprinting','value'=>'Livescan Fingerprinting'],
                    ['label'=>'Not sure / other','value'=>'Not sure / other'],
                ],
                'required'=>'0','size'=>'medium'],
        '5' => ['id'=>'5','type'=>'textarea','label'=>'Message','required'=>'1',
                'size'=>'medium','placeholder'=>'Tell us a little about your situation...'],
    ],
    'settings' => [
        'form_title'               => $title,
        'form_desc'                => '',
        'submit_text'              => 'Send Message',
        'submit_text_processing'   => 'Sending...',
        'antispam'                 => '1',
        'notification_enable'      => '1',
        'notifications'            => [
            '1' => [
                'enable'         => '1',
                'email'          => 'info@candrtaxservices.com',
                'subject'        => 'New Contact Form Submission - C&R Tax Services',
                'sender_name'    => 'C&R Tax Services Website',
                'sender_address' => '{field_id="3"}',
                'replyto'        => '{field_id="3"}',
                'message'        => '{all_fields}',
            ],
        ],
        'confirmation_type'    => 'message',
        'confirmation_message' => '<p>Thanks! A member of our team will reach out the same business day. <strong>\\u00a1Se habla espa\\u00f1ol!</strong></p>',
    ],
    'meta' => ['template' => 'blank'],
];

wp_update_post([
    'ID'           => $form_id,
    'post_content' => wp_json_encode($form_data),
]);

return ['form_id' => (int)$form_id, 'created' => true];
""")
    rv = result.get("return_value", result) if isinstance(result, dict) else {}
    return rv

# ── Section builders ──────────────────────────────────────────────────────────

def service_cta_section(h2_text, body_text, btn_label, form_id, form_title, form_subtitle):
    """Two-column CTA section: left=text+button, right=form card"""
    left_html = (
        h2_inv(h2_text) +
        p_inv(body_text) +
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;">'
        f'{btn_link(btn_label, "tel:5599627503", primary=True)}'
        f'</div>'
    )
    form_elements = form_card(form_id, form_title, form_subtitle)

    return {
        "id": uid(), "elType": "section",
        "settings": {
            "background_background": "classic",
            "background_color": NAVY,
            "padding": pad(96, 32, 96, 32),
            "content_width": {"size": 1000, "unit": "px"},
        },
        "elements": [
            con(
                {"flex_direction": "row", "flex_wrap": "wrap",
                 "flex_gap": gap(48), "flex_align_items": "flex-start",
                 "padding": pad(0, 0, 0, 0)},
                [
                    con({"flex": "1 1 420px", "flex_direction": "column",
                         "padding": pad(0, 0, 0, 0)},
                        [text(left_html)]),
                    con({"flex": "1 1 340px", "max_width": size(440),
                         "flex_direction": "column", "padding": pad(0, 0, 0, 0)},
                        form_elements),
                ],
                is_inner=False,
            )
        ],
    }


def contact_page_sections(form_id):
    """Full Contact page with form in 'How to Reach Us' section."""
    REASONS = [
        ("question-circle", "General questions",
         "Not sure which documents you need? Wondering about an extension? Just ask."),
        ("tag", "Free quotes",
         "Get upfront, honest pricing for your tax preparation before we file a thing."),
        ("exclamation-triangle", "Urgent tax matters",
         "Got an IRS letter or a looming deadline? Call right away, and we'll help you respond fast."),
        ("stamp", "Notary &amp; Live Scan appointments",
         "Need a document notarized or Live Scan fingerprints for a job or license? We can usually get you in quickly."),
    ]
    CITIES = ["Fresno", "Selma", "Reedley", "Clovis", "Madera", "Sanger"]

    def sec(elements, bg=None, pad_top=80, pad_bot=80, max_w=760):
        s = {"padding": pad(pad_top, 32, pad_bot, 32),
             "content_width": {"size": max_w, "unit": "px"}}
        if bg:
            s["background_background"] = "classic"
            s["background_color"] = bg
        return {"id": uid(), "elType": "section", "settings": s,
                "elements": [con({"flex_direction":"column","padding":pad(0,0,0,0)},
                                 elements, is_inner=False)]}

    def h2(t):
        return text(f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
                    f'color:{TEXT_HEAD};margin:0 0 20px;">{t}</h2>')

    # Hero
    hero_content = (
        f'<div style="width:56px;height:56px;border-radius:10px;'
        f'background:rgba(247,248,250,0.12);display:flex;align-items:center;'
        f'justify-content:center;margin-bottom:24px;">'
        f'<i class="fas fa-comment-alt" style="font-size:28px;color:{OFF_WHITE};"></i></div>'
        f'<span style="display:inline-block;background:{RED};color:{WHITE};'
        f'font-family:Inter,sans-serif;font-size:13px;font-weight:700;'
        f'padding:4px 14px;border-radius:999px;margin-bottom:18px;">Real People, Fast Responses</span><br>'
        f'<h1 style="font-family:Poppins,sans-serif;font-weight:800;font-size:50px;'
        f'line-height:1.15;color:{WHITE};margin:0 0 16px;max-width:680px;">We\'re Glad You\'re Here</h1>'
        f'<p style="font-family:Inter,sans-serif;font-size:20px;color:{ICE_BLUE};'
        f'line-height:1.6;margin:0 0 28px;max-width:620px;">'
        f'Thanks for stopping by! If you\'ve been looking for trusted Fresno tax preparation, '
        f'you\'re in the right place. At C&amp;R Tax Services, there\'s no automated runaround '
        f'and no call center in another state. You\'ll talk with real, friendly people right '
        f'here in Fresno — ready to listen, answer your questions, and help you feel good '
        f'about your taxes.</p>'
        f'<a href="#contact-form" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:{RED};color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;">'
        f'Request a Free Quote</a>'
    )
    hero = {
        "id": uid(), "elType": "section",
        "settings": {"background_background": "classic", "background_color": NAVY,
                     "padding": pad(80, 32, 80, 32),
                     "content_width": {"size": 780, "unit": "px"}},
        "elements": [con({"flex_direction":"column","padding":pad(0,0,0,0)},
                         [text(hero_content)], is_inner=False)]
    }

    # How to reach us — form left, contact+hours right
    reach_right = (
        contact_card_html() +
        hours_card_html("tax") +
        hours_card_html("after") +
        f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
        f'color:{TEXT_BODY};margin:24px 0 0;">'
        f'<strong>¡Se habla español!</strong> Ask your questions in the language you\'re most '
        f'comfortable with. No pressure, no obligation — just honest help.</p>'
    )
    reach = {
        "id": uid(), "elType": "section",
        "settings": {"padding": pad(80, 32, 80, 32),
                     "content_width": {"size": 1000, "unit": "px"},
                     "_element_id": "contact-form"},
        "elements": [con(
            {"flex_direction": "column", "padding": pad(0,0,0,0)},
            [
                h2("How to Reach Us"),
                text(p_html("Getting in touch is easy. Fill out the form, or pick whatever works best for you below.", last=True)),
                spacer(32),
                con(
                    {"flex_direction": "row", "flex_wrap": "wrap",
                     "flex_gap": gap(40), "flex_align_items": "flex-start",
                     "padding": pad(0,0,0,0)},
                    [
                        con({"flex": "1 1 380px", "max_width": size(460),
                             "flex_direction": "column", "padding": pad(0,0,0,0)},
                            form_card(form_id, "Send Us a Message",
                                      "Tell us a bit about what you need, and we'll get back to you the same business day.")),
                        con({"flex": "1 1 300px", "flex_direction": "column",
                             "padding": pad(0,0,0,0)},
                            [text(reach_right)]),
                    ]
                ),
            ],
            is_inner=False,
        )]
    }

    # Why reach out
    reasons_html = "".join(diff_card_html(r[0], r[1], r[2]) for r in REASONS)
    why = sec([
        h2("Why Reach Out?"),
        text(p_html("Whatever brings you here, we're happy to help.", last=True)),
        text(f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));'
             f'gap:24px;margin-top:32px;">{reasons_html}</div>'),
    ], bg=SURFACE_ALT)

    # Trust + cities
    trust = sec([
        h2("Your Trusted Local Team"),
        text(p_html("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we're here after April 15th, not just before it.") +
             p_html("Fully credentialed and locally owned in Fresno — your neighbors, not a national chain.", last=True)),
        spacer(32),
        text(f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
             f'color:{TEXT_HEAD};margin:0 0 12px;">Proudly Serving the Central Valley</h3>'),
        city_pills_html(CITIES),
    ])

    # Final CTA
    final_html = (
        h2_inv("Let's Get Started Today") +
        p_inv("Tax questions don't get easier by waiting — but they do get easier with the "
              "right team in your corner. Call now or reach out below. A local, professional team "
              "you can actually talk to will take the stress off your plate.") +
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;">'
        f'{btn_link("Request a Free Quote", "tel:5599627503", True)}'
        f'{btn_link("Get Help Now", "tel:5599627503", False)}'
        f'</div>'
    )
    final = {
        "id": uid(), "elType": "section",
        "settings": {"background_background": "classic", "background_color": NAVY,
                     "padding": pad(96, 32, 96, 32),
                     "content_width": {"size": 780, "unit": "px"}},
        "elements": [con({"flex_direction":"column","padding":pad(0,0,0,0)},
                         [text(final_html)], is_inner=False)]
    }

    return [hero, reach, why, trust, final]


# ── Save helpers ──────────────────────────────────────────────────────────────

def save_page(post_id, sections):
    path = f"wp-content/novamira-sandbox/el_{post_id}.json"
    write_file(path, json.dumps(sections))
    result = php(f"""
$j = file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$d = json_decode($j, true);
$s = wp_slash(json_encode($d));
update_post_meta({post_id}, '_elementor_data', $s);
update_post_meta({post_id}, '_elementor_draft_data', $s);
$a = wp_get_post_autosave({post_id});
if($a) wp_delete_post_revision($a->ID);
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$css = new Elementor\\Core\\Files\\CSS\\Post({post_id}); $css->update();
update_post_meta({post_id}, '_elementor_edit_mode', 'builder');
update_post_meta({post_id}, '_wp_page_template', 'elementor_header_footer');
return ['saved'=>true,'sections'=>count($d),'css_len'=>strlen($css->get_content())];
""")
    rv = result.get("return_value", result) if isinstance(result, dict) else result
    return rv


def replace_last_section(post_id, new_section):
    """Fetch existing Elementor data, replace the final section, save back."""
    path = f"wp-content/novamira-sandbox/el_{post_id}_new_last.json"
    write_file(path, json.dumps(new_section))
    result = php(f"""
$existing = json_decode(get_post_meta({post_id}, '_elementor_data', true), true);
if (!$existing) return ['error' => 'no existing data for post {post_id}'];
$new_last = json_decode(file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}_new_last.json'), true);
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}_new_last.json');
// Replace last section
array_pop($existing);
$existing[] = $new_last;
$s = wp_slash(json_encode($existing));
update_post_meta({post_id}, '_elementor_data', $s);
update_post_meta({post_id}, '_elementor_draft_data', $s);
$a = wp_get_post_autosave({post_id});
if($a) wp_delete_post_revision($a->ID);
$css = new Elementor\\Core\\Files\\CSS\\Post({post_id}); $css->update();
return ['saved'=>true,'sections'=>count($existing),'css_len'=>strlen($css->get_content())];
""")
    rv = result.get("return_value", result) if isinstance(result, dict) else result
    return rv


def clear_cache():
    php("""
Elementor\\Plugin::$instance->files_manager->clear_cache();
do_action('breeze_clear_all_cache');
foreach([WP_CONTENT_DIR.'/cache/breeze/',WP_CONTENT_DIR.'/cache/breeze-minification/'] as $d){
if(!is_dir($d))continue;
$it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($d,FilesystemIterator::SKIP_DOTS),RecursiveIteratorIterator::CHILD_FIRST);
foreach($it as $f){if($f->isFile())@unlink($f->getPathname());}}
return true;
""")


# ── Main ─────────────────────────────────────────────────────────────────────

def build():
    print("=== v8 Form Update ===\n")

    print("1. Creating WPForms form...")
    form_result = create_or_get_form()
    print(f"   Result: {form_result}")
    form_id = form_result.get("form_id") if isinstance(form_result, dict) else None
    if not form_id:
        print("   ERROR: could not create form")
        return
    print(f"   Form ID: {form_id}")

    print("\n2. Contact page (post 38) — full rebuild with form...")
    sections = contact_page_sections(form_id)
    r = save_page(38, sections)
    print(f"   Saved: {r}")

    print("\n3. Income Tax page (post 28) — replacing final CTA with form...")
    new_cta = service_cta_section(
        "You Work Hard for Your Money — This Is the Year to Keep More of It",
        "The forms aren’t getting simpler and California’s rules aren’t getting easier. "
        "You deserve a friendly, local expert who does this every day, explains everything clearly, "
        "and guarantees the work. Call C&amp;R Tax Services to schedule your appointment, or send "
        "us a message below. Se habla español.",
        "Schedule an Appointment",
        form_id,
        "Request a Free Estimate",
        "Tell us about your filing situation and we’ll follow up the same business day.",
    )
    r = replace_last_section(28, new_cta)
    print(f"   Saved: {r}")

    print("\n4. Notary page (post 29) — replacing final CTA with form...")
    new_cta = service_cta_section(
        "Deadlines Don’t Wait — Let’s Get It Signed, Sealed, and Off Your Plate",
        "Whether it’s a loan closing on the calendar, a power of attorney your family needs "
        "this week, or travel documents that must be certified before a flight, the fastest way "
        "to stop worrying is to get it done right, the first time. Call C&amp;R Tax Services "
        "today, or send us the details below and we’ll tell you exactly what to bring. "
        "Se habla español.",
        "Book Your Appointment",
        form_id,
        "Ask About Mobile Service",
        "Tell us what needs notarizing and when — we’ll follow up the same business day.",
    )
    r = replace_last_section(29, new_cta)
    print(f"   Saved: {r}")

    print("\n5. Livescan page (post 30) — replacing final CTA with form...")
    new_cta = service_cta_section(
        "Don’t Let Fingerprinting Hold Up Your Job, License, or Certification",
        "Rejected prints and wrong forms can set your plans back by weeks, and almost all of "
        "those delays are avoidable. Call us, stop by our Fresno office, or send us your details "
        "below. Walk-ins are welcome — just bring your request form and a valid photo ID. "
        "¡Se habla español! Llámenos hoy.",
        "Schedule Your Appointment",
        form_id,
        "Walk In or Book Ahead",
        "Tell us what your fingerprints are for and we’ll confirm what to bring.",
    )
    r = replace_last_section(30, new_cta)
    print(f"   Saved: {r}")

    print("\n6. Clearing caches...")
    clear_cache()
    print("\n=== DONE ===")
    print(f"   WPForms form ID: {form_id}  →  [wpforms id=\"{form_id}\"]")
    print("   Contact page: /contact (post 38)")
    print("   Income Tax:   /income-tax (post 28)")
    print("   Notary:       /notary (post 29)")
    print("   Livescan:     /livescan (post 30)")


if __name__ == "__main__":
    build()
