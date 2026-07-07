#!/usr/bin/env python3
"""
Home page rebuild v3 — matches updated design with:
 - New Hero: editorial copy, 2 CTAs, image placeholder (no contact card)
 - FeaturedServices: long-form editorial service blocks
 - WhyTrust: trust/differentiation section
 - ServiceArea: cities served + image placeholder
 - Testimonials: placeholder for Google reviews
 - FinalCTA: navy conversion strip
 - FooterLinks: midnight nav strip before XPRO footer
 - Hours + Contact sections remain (same as v2)
"""
import requests, json, random, string, sys
sys.path.insert(0, '/home/user/candrtax/wordpress')
from mcp_php import init_session as _init

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

NAVY       = "#1B2A5E"
ROYAL_BLUE = "#0A4A93"
GROWTH_RED = "#E23A28"
RED_HOVER  = "#C22E1F"
ICE_BLUE   = "#EAF0F8"
OFF_WHITE  = "#F7F8FA"
SLATE      = "#5A6B8C"
MIDNIGHT   = "#121D42"
WHITE      = "#FFFFFF"
BORDER     = "#D7DEEA"

_sess = None

def sess():
    global _sess
    if not _sess:
        _sess = _init()
    return _sess

def php(code):
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess()}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/execute-php","parameters":{"code":code}}}
    })
    d = r.json()
    content = d["result"]["content"][0]["text"]
    parsed = json.loads(content)
    return parsed.get("data", parsed)

def write_file(path, content):
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess()}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/write-file",
                               "parameters":{"path":path,"content":content}}}
    })
    d = r.json()
    result = json.loads(d["result"]["content"][0]["text"])
    return result.get("data", result)

def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def pad(t, r, b, l, u="px"):
    return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}

def size(v, u="px"):
    return {"size":v,"unit":u}

def gap(v, u="px"):
    return {"column":v,"row":v,"unit":u,"isLinked":True}

def typo(fam, wt, sz, u="px"):
    return {"typography_typography":"custom","typography_font_family":fam,
            "typography_font_weight":str(wt),"typography_font_size":size(sz,u)}

def con(settings, elements, inner=True):
    renames = {"justify_content":"flex_justify_content","align_items":"flex_align_items"}
    fixed = {}
    for k, v in settings.items():
        k2 = renames.get(k, k)
        if k == "background_color" and "background_background" not in settings:
            fixed["background_background"] = "classic"
        fixed[k2] = v
    return {"id":uid(),"elType":"container","isInner":inner,"settings":fixed,"elements":elements}

def sec(settings, elements):
    return con(settings, elements, inner=False)

def wgt(t, s):
    s2 = dict(s)
    if t == "button":
        if "background_color" in s2 and "background_background" not in s2:
            s2["background_background"] = "classic"
        if "hover_background_color" in s2:
            s2["button_background_hover_color"] = s2.pop("hover_background_color")
            s2["button_background_hover_background"] = "classic"
    return {"id":uid(),"elType":"widget","isInner":False,"widgetType":t,"settings":s2,"elements":[]}

def red_btn(text, url, sz="lg"):
    return wgt("button", {
        "text":text,"link":{"url":url},"size":sz,
        "background_color":GROWTH_RED,"button_text_color":OFF_WHITE,
        "hover_background_color":RED_HOVER,"border_radius":pad(50,50,50,50),
        **typo("Inter",600,16 if sz=="lg" else 15),
    })

def outline_btn(text, url, sz="lg"):
    return wgt("button", {
        "text":text,"link":{"url":url},"size":sz,
        "background_color":"transparent","background_background":"classic",
        "button_text_color":WHITE,
        "hover_background_color":"rgba(255,255,255,0.1)",
        "button_background_hover_background":"classic",
        "border_border":"solid","border_width":pad(2,2,2,2),
        "border_color":"rgba(255,255,255,0.4)","border_radius":pad(50,50,50,50),
        **typo("Inter",600,16),
    })

def body_text(html, color=None):
    """Text editor widget with optional color override."""
    if color:
        return wgt("text-editor", {"editor": html})
    return wgt("text-editor", {"editor": html})

def img_placeholder(caption, height=320):
    """Styled image placeholder matching the design's ImagePlaceholder component."""
    return con(
        {
            "background_color": ICE_BLUE,
            "border_border": "dashed",
            "border_width": pad(2,2,2,2),
            "border_color": SLATE,
            "border_radius": pad(16,16,16,16),
            "min_height": size(height),
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "flex_gap": gap(10),
            "padding": pad(32,32,32,32),
        },
        [
            wgt("icon", {
                "selected_icon": {"library":"fa-solid","value":"fas fa-image"},
                "icon_size": size(28),
                "primary_color": SLATE,
            }),
            wgt("text-editor", {
                "editor": f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{SLATE};text-align:center;margin:0;max-width:380px;">{caption}</p>',
            }),
        ]
    )

# ── HERO ────────────────────────────────────────────────────────────────────

def home_hero():
    badge = wgt("text-editor", {
        "editor": f'<span style="background:{GROWTH_RED};color:{OFF_WHITE};font-family:Inter,sans-serif;font-weight:600;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;padding:6px 14px;border-radius:999px;display:inline-block;">Fresno &amp; the Central Valley</span>',
    })
    h1 = wgt("heading", {
        "title": "Tax Season Doesn&rsquo;t Have to Be Stressful.",
        "header_size": "h1",
        "align": "left",
        "title_color": WHITE,
        **typo("Poppins", 800, 52),
        "typography_line_height": size(1.15, "em"),
    })
    p1 = wgt("text-editor", {
        "editor": f'<p style="font-family:Inter,sans-serif;font-size:18px;line-height:1.6;color:{ICE_BLUE};margin:0;">Accurate, dependable income tax preparation for individuals, small businesses, and corporations across Fresno and the Central Valley &mdash; offered in person or fully virtual, in English or Spanish.</p>',
    })
    p2 = wgt("text-editor", {
        "editor": f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{ICE_BLUE};margin:0;opacity:0.92;">Tax season has a way of sneaking up on you. One day life is moving along just fine, and the next you&rsquo;re sitting at the kitchen table with a stack of W-2s, 1099s, and maybe a letter from the IRS, wondering if you&rsquo;re missing something. If you&rsquo;ve ever felt that knot in your stomach in early spring, you&rsquo;re in good company.</p>',
    })
    p3 = wgt("text-editor", {
        "editor": f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{ICE_BLUE};margin:0;opacity:0.92;">At C&amp;R Tax Services, our job is to take that weight off your shoulders &mdash; with careful, personal attention on every return, and complete tax preparation available in Spanish.</p>',
    })
    btns = con(
        {"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(14)},
        [red_btn("Schedule an Appointment","tel:5599627503"),
         outline_btn("Upload Your Docs &mdash; Virtual Prep","#contact")]
    )
    left_col = con(
        {"flex_direction":"column","flex_gap":gap(20)},
        [badge, h1, p1, p2, p3, btns]
    )
    right_col = img_placeholder(
        "A friendly tax preparer smiling across a desk from a relaxed client, documents and laptop visible, warm office lighting.",
        height=340
    )
    inner = con(
        {"content_width":"boxed","flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(64),"align_items":"center"},
        [left_col, right_col]
    )
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(96,0,96,0),"_element_id":"home","html_tag":"section"},
        [inner]
    )


# ── FEATURED SERVICES ────────────────────────────────────────────────────────

def featured_service_block(title, paragraphs, link_label, link_href, last=False):
    """One editorial service block with divider."""
    elements = [
        wgt("heading", {
            "title": title,
            "header_size": "h3",
            "title_color": MIDNIGHT,
            **typo("Poppins", 700, 30),
        }),
    ]
    for p in paragraphs:
        elements.append(wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{MIDNIGHT};margin:0;">{p}</p>',
        }))
    elements.append(wgt("text-editor", {
        "editor": f'<p style="margin:0;"><a href="{link_href}" style="color:{ROYAL_BLUE};font-family:Inter,sans-serif;font-weight:600;font-size:15px;text-decoration:none;">{link_label} &#10230;</a></p>',
    }))

    block_settings = {
        "flex_direction": "column",
        "flex_gap": gap(16),
    }
    if not last:
        block_settings.update({
            "border_border": "solid",
            "border_width": pad(0,0,1,0),
            "border_color": BORDER,
            "padding": pad(0,0,48,0),
        })

    return con(block_settings, elements)


def home_featured_services():
    blocks = [
        featured_service_block(
            "Individual &amp; Rental Property Taxes",
            [
                "For a lot of people, filing personal taxes feels like a guessing game. Did you claim every deduction you qualify for? Was that side income reported the right way? Is your refund as big as it should be? Filing alone, or with generic software, often leaves those questions hanging in the air.",
                "We do it differently. At C&amp;R Tax Services, we sit down with you, in person or virtually, and walk through your full financial picture together, and make sure every credit and deduction you&rsquo;re entitled to actually lands on your return.",
                "If you own rental property, we dig even deeper &mdash; Schedule E filings, depreciation, and the rules around passive income, tracked carefully so your rental income works for you instead of against you.",
            ],
            "Learn more about our Individual Tax Services",
            "/income-tax/",
        ),
        featured_service_block(
            "Small Business &amp; Corporate Business Taxes",
            [
                "Running a business in the Central Valley is demanding enough without the IRS piling onto your to-do list. Between quarterly estimates, payroll questions, entity rules, and California&rsquo;s own layer of requirements, small business taxes can eat up hours you don&rsquo;t have.",
                "C&amp;R Tax Services handles small business and corporate business taxes for sole proprietors, partnerships, LLCs, S-Corps, and C-Corps across Fresno &mdash; and if your business operates across state lines, our multi-state return experience keeps every jurisdiction squared away.",
            ],
            "Learn more about our Business Tax Preparation",
            "/income-tax/",
        ),
        featured_service_block(
            "ITIN Applications &amp; Multi-State Returns",
            [
                "If you don&rsquo;t have a Social Security number, filing taxes can feel like a door that&rsquo;s closed to you. It isn&rsquo;t. C&amp;R Tax Services provides professional support for ITIN applications, helping non-SSN filers in Fresno get the Individual Taxpayer Identification Number they need to file correctly and claim eligible credits.",
                "We also prepare multi-state returns for anyone who earned income in more than one state &mdash; sorting out exactly what each state is owed so you never pay twice or file incorrectly.",
            ],
            "Learn more about ITIN &amp; Multi-State Services",
            "/income-tax/",
        ),
        featured_service_block(
            "Audit Services, Tax Extensions &amp; Amendments",
            [
                "Few things ruin a week faster than an envelope from the IRS. C&amp;R Tax Services provides professional audit services and IRS notice support for taxpayers across the Fresno area &mdash; we read the notice with you and help you respond correctly and on time.",
                "If an old return needs fixing, our tax amendment service sets the record straight. And if life simply got in the way this year, we can file your tax extension quickly so you get breathing room without late-filing penalties.",
            ],
            "Learn more about Audit, Extension &amp; Amendment Services",
            "/income-tax/",
        ),
        featured_service_block(
            "Notary Public, Loan Signing &amp; Live Scan Fingerprints",
            [
                "Taxes aren&rsquo;t the only paperwork life throws your way. C&amp;R Tax Services also serves Fresno as a Notary Public and Loan Signing Agent and provides Live Scan fingerprint services &mdash; a convenient one-stop shop for the documents and verifications that keep your life and business moving.",
                "Need something notarized for a real estate deal, a power of attorney, or a business agreement? We handle it promptly. Closing on a loan? Our certified loan signing service walks you through the entire signing package. Applying for a job or license that requires a background check? Our state-compliant Live Scan fingerprinting captures and submits your prints correctly the first time.",
            ],
            "Learn more about Notary &amp; Live Scan Services",
            "/notary/",
            last=True,
        ),
    ]

    placeholder = img_placeholder(
        "A clean collage or split-panel showing a tax document review, a notary stamp on paperwork, and a Live Scan fingerprint device.",
        height=280
    )

    inner = con(
        {"content_width":"boxed","boxed_width":size(760),"flex_direction":"column","flex_gap":gap(48)},
        [
            con(
                {"flex_direction":"column","align_items":"center"},
                [wgt("heading", {
                    "title":"Our Featured Tax &amp; Business Services",
                    "header_size":"h2","align":"center","title_color":MIDNIGHT,
                    **typo("Poppins",700,38),
                })]
            ),
        ] + blocks + [placeholder]
    )
    return sec(
        {"content_width":"full","background_color":WHITE,"padding":pad(96,0,96,0),"_element_id":"services"},
        [inner]
    )


# ── WHY TRUST ────────────────────────────────────────────────────────────────

def home_why_trust():
    paragraphs = [
        "There&rsquo;s no shortage of ways to get your taxes done in Fresno. Big-box franchises pop up every January, and online software promises easy filing in minutes. So why do local families and business owners keep choosing C&amp;R Tax Services? Because we offer something those options can&rsquo;t: a real, local professional who knows your name, answers your questions honestly, and treats your return like it matters. Because it does.",
        "One thing that sets us apart is our Spanish-language tax preparation. For thousands of Central Valley families, taxes are stressful enough without a language barrier in the middle of it. Here, you can explain your situation, ask every question on your mind, and understand every line of your return completely in Spanish.",
        "We also believe in doing business the straightforward way: upfront, transparent pricing, accuracy you can count on, and year-round support. With us, you&rsquo;re never a ticket number in a queue. You&rsquo;re a neighbor, and we treat you like one.",
    ]
    elements = [
        wgt("heading", {
            "title":"Why Fresno Trusts C&amp;R Tax Services",
            "header_size":"h2","align":"center","title_color":MIDNIGHT,
            **typo("Poppins",700,38),
        }),
    ]
    for p in paragraphs:
        elements.append(wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{MIDNIGHT};margin:0;">{p}</p>',
        }))
    elements.append(img_placeholder(
        "The C&amp;R team (or preparer) greeting a multigenerational local family at the office entrance, handshake or warm welcome moment.",
        height=280
    ))
    inner = con(
        {"content_width":"boxed","boxed_width":size(760),"flex_direction":"column","flex_gap":gap(24)},
        elements
    )
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(96,0,96,0)},
        [inner]
    )


# ── SERVICE AREA ─────────────────────────────────────────────────────────────

def home_service_area():
    cities = ["Fresno","Clovis","Sanger","Selma","Madera"]
    city_pills = []
    for city in cities:
        city_pills.append(con(
            {
                "background_color":ICE_BLUE,
                "border_border":"solid","border_width":pad(1,1,1,1),"border_color":BORDER,
                "border_radius":pad(999,999,999,999),
                "padding":pad(10,18,10,18),
                "flex_direction":"row","align_items":"center","flex_gap":gap(8),
            },
            [
                wgt("icon", {"selected_icon":{"library":"fa-solid","value":"fas fa-map-marker-alt"},"icon_size":size(14),"primary_color":ROYAL_BLUE}),
                wgt("text-editor", {"editor":f'<span style="font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">{city}</span>'}),
            ]
        ))

    pills_row = con(
        {"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(12)},
        city_pills
    )

    inner = con(
        {"content_width":"boxed","boxed_width":size(760),"flex_direction":"column","flex_gap":gap(24)},
        [
            wgt("heading", {
                "title":"Proudly Serving Fresno &amp; the Central Valley",
                "header_size":"h2","align":"center","title_color":MIDNIGHT,
                **typo("Poppins",700,38),
            }),
            wgt("text-editor", {"editor":f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{MIDNIGHT};margin:0;">C&amp;R Tax Services is based in Fresno, and our roots here run deep. But our service area reaches well beyond one zip code. We proudly provide income tax preparation, ITIN applications, business tax services, notary work, and Live Scan fingerprinting to families and businesses throughout the Central Valley.</p>'}),
            wgt("text-editor", {"editor":f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{MIDNIGHT};margin:0;">Because we live and work in the Central Valley ourselves, we understand the financial realities our neighbors face. And with our secure virtual tax preparation option, distance is never a barrier.</p>'}),
            pills_row,
            img_placeholder(
                "A scenic Central Valley shot (orchards or the Fresno skyline at golden hour) with a subtle map-pin graphic marking the five service cities.",
                height=260
            ),
        ]
    )
    return sec(
        {"content_width":"full","background_color":WHITE,"padding":pad(96,0,96,0)},
        [inner]
    )


# ── TESTIMONIALS ─────────────────────────────────────────────────────────────

def home_testimonials():
    placeholder_box = con(
        {
            "background_color":WHITE,
            "border_border":"dashed","border_width":pad(1,1,1,1),"border_color":SLATE,
            "border_radius":pad(10,10,10,10),
            "padding":pad(18,22,18,22),
        },
        [wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{SLATE};font-style:italic;text-align:center;margin:0;">Verified client reviews will go here once collected via Google Business Profile.</p>',
        })]
    )
    inner = con(
        {"content_width":"boxed","boxed_width":size(700),"flex_direction":"column","align_items":"center","flex_gap":gap(24)},
        [
            wgt("heading", {
                "title":"What Clients Are Saying",
                "header_size":"h2","align":"center","title_color":MIDNIGHT,
                **typo("Poppins",700,38),
            }),
            wgt("text-editor", {"editor":f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{MIDNIGHT};text-align:center;margin:0;">Ask around Fresno about what matters most in a tax preparer, and you&rsquo;ll hear the same answers again and again: patience, honesty, clear explanations, and getting every dollar you deserve. From first-time filers to business owners untangling multi-state returns, our clients tend to tell us the same thing: working with C&amp;R Tax Services made taxes feel simple for the first time.</p>'}),
            placeholder_box,
        ]
    )
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,0,80,0)},
        [inner]
    )


# ── FINAL CTA ────────────────────────────────────────────────────────────────

def home_final_cta():
    left_col = con(
        {"flex_direction":"column","flex_gap":gap(20)},
        [
            wgt("heading", {
                "title":"Ready to Maximize Your Return and Minimize Your Stress?",
                "header_size":"h2","title_color":WHITE,
                **typo("Poppins",700,32),
                "typography_line_height":size(1.3,"em"),
            }),
            wgt("text-editor", {
                "editor":f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{ICE_BLUE};margin:0;">Whether you need straightforward individual tax preparation, full small business and corporate tax support, help with an ITIN application, or a calm, fast answer to a scary IRS letter, C&amp;R Tax Services is ready, in English or Spanish, in our office or completely online.</p>',
            }),
            red_btn("Get Started Now &mdash; Schedule My Appointment", "tel:5599627503"),
        ]
    )
    right_col = img_placeholder(
        "A relieved, smiling client shaking hands with a preparer, finished return folder on the desk, or a person happily uploading documents from their phone at home.",
        height=220
    )
    inner = con(
        {"content_width":"boxed","boxed_width":size(760),"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(48),"align_items":"center"},
        [left_col, right_col]
    )
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(96,0,96,0)},
        [inner]
    )


# ── HOURS (unchanged from v2) ────────────────────────────────────────────────

def home_hours():
    """Tab switcher with Tax Season / After Tax Season content."""
    def hours_card_html(label, rows):
        rows_html = ""
        for day, time in rows:
            rows_html += f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 20px;border-bottom:1px solid {BORDER};"><span style="font-family:Inter,sans-serif;font-weight:600;color:{MIDNIGHT};font-size:15px;">{day}</span><span style="font-family:Inter,sans-serif;color:{SLATE};font-size:15px;">{time}</span></div>'
        return f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(27,42,94,0.10);max-width:420px;margin:0 auto;"><div style="background:{NAVY};padding:20px 20px 16px;"><span style="font-family:Poppins,sans-serif;font-weight:700;font-size:18px;color:{WHITE};">{label}</span></div>{rows_html}<div style="padding:12px 20px;"><span style="font-family:Inter,sans-serif;font-size:13px;color:{SLATE};font-style:italic;">After Hours &mdash; By Appointment Only</span></div></div>'

    tax_html = hours_card_html(
        "Tax Season (Jan &ndash; Apr)",
        [("Monday &ndash; Saturday","9:00 am &ndash; 7:00 pm"),("Sunday","10:00 am &ndash; 6:00 pm")]
    )
    off_html = hours_card_html(
        "After Tax Season (May &ndash; Dec)",
        [("Monday &ndash; Friday","10:00 am &ndash; 6:00 pm"),("Saturday &ndash; Sunday","By Appointment Only")]
    )

    tabs_widget = wgt("tabs", {
        "_element_id": "season-tabs",
        "tabs": [
            {"tab_title":"Tax Season","tab_content":tax_html,"_id":uid()},
            {"tab_title":"After Tax Season","tab_content":off_html,"_id":uid()},
        ],
        "type": "horizontal",
        "tab_color": SLATE,
        "tab_active_color": NAVY,
        "tab_typography_typography": "custom",
        "tab_typography_font_family": "Inter",
        "tab_typography_font_size": size(15),
        "tab_typography_font_weight": "600",
        "title_align": "center",
    })

    inner = con(
        {"content_width":"boxed","flex_direction":"column","flex_gap":gap(48)},
        [
            con(
                {"flex_direction":"column","align_items":"center","flex_gap":gap(8)},
                [
                    wgt("heading", {"title":"Office Hours","header_size":"h2","align":"center","title_color":MIDNIGHT,**typo("Poppins",700,38)}),
                    wgt("text-editor", {"editor":f'<p style="color:{SLATE};font-family:Inter,sans-serif;font-size:17px;text-align:center;margin:0;">Tax season: January &ndash; April. After tax season: May &ndash; December.</p>'}),
                ]
            ),
            con({"flex_direction":"column","align_items":"center"},[tabs_widget]),
        ]
    )
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(96,0,96,0),"_element_id":"hours"},
        [inner]
    )


# ── CONTACT (unchanged from v2) ──────────────────────────────────────────────

def contact_info_card():
    def row(icon_fa, text_html):
        icon_box = con(
            {"flex_direction":"row","align_items":"center","justify_content":"center",
             "background_color":ICE_BLUE,"border_radius":pad(8,8,8,8),
             "width":size(36),"min_height":size(36)},
            [wgt("icon",{"selected_icon":{"library":"fa-solid","value":icon_fa},"icon_size":size(18),"primary_color":ROYAL_BLUE})]
        )
        return con(
            {"flex_direction":"row","align_items":"flex-start","flex_gap":gap(14)},
            [icon_box, wgt("text-editor",{"editor":f'<div style="line-height:1.4;">{text_html}</div>'})]
        )
    return con(
        {"flex_direction":"column","background_color":WHITE,"border_border":"solid",
         "border_width":pad(1,1,1,1),"border_color":BORDER,"border_radius":pad(16,16,16,16),
         "box_shadow_box_shadow_type":"yes",
         "box_shadow_box_shadow":{"horizontal":0,"vertical":1,"blur":3,"spread":0,"color":"rgba(18,29,66,0.08)","position":"outset"},
         "padding":pad(32,32,32,32),"flex_gap":gap(20)},
        [
            row("fas fa-map-marker-alt", f'<span style="color:{MIDNIGHT};font-weight:600;font-family:Inter,sans-serif;font-size:17px;">1320 N. Van Ness Ave, Fresno CA 93702</span><br><span style="color:{SLATE};font-family:Inter,sans-serif;font-size:15px;">Near Tower District</span>'),
            row("fas fa-phone", f'<a href="tel:5599627503" style="color:{ROYAL_BLUE};font-weight:600;font-family:Inter,sans-serif;font-size:17px;text-decoration:none;">(559) 962-7503</a>'),
            row("fas fa-envelope", f'<a href="mailto:info@candrtaxservices.com" style="color:{ROYAL_BLUE};font-weight:600;font-family:Inter,sans-serif;font-size:17px;text-decoration:none;">info@candrtaxservices.com</a>'),
            row("fas fa-globe", f'<a href="https://www.candrtaxservices.com" style="color:{ROYAL_BLUE};font-weight:600;font-family:Inter,sans-serif;font-size:17px;text-decoration:none;">www.candrtaxservices.com</a>'),
        ]
    )

def home_contact():
    inner = con(
        {"content_width":"boxed","boxed_width":size(640),"flex_direction":"column","align_items":"center","flex_gap":gap(32)},
        [
            con(
                {"flex_direction":"column","align_items":"center","flex_gap":gap(10)},
                [
                    wgt("heading",{"title":"Get In Touch","header_size":"h2","align":"center","title_color":MIDNIGHT,**typo("Poppins",700,38)}),
                    wgt("text-editor",{"editor":f'<p style="color:{SLATE};font-family:Inter,sans-serif;font-size:17px;text-align:center;margin:0;">Stop by, call, or book a virtual appointment &mdash; we&rsquo;re here all year.</p>'}),
                ]
            ),
            contact_info_card(),
        ]
    )
    return sec(
        {"content_width":"full","background_color":WHITE,"padding":pad(96,0,96,0),"_element_id":"contact"},
        [inner]
    )


# ── FOOTER LINKS (new midnight strip before XPRO footer) ────────────────────

def home_footer_links():
    def link_col(heading_text, links):
        elements = [
            wgt("text-editor", {
                "editor":f'<p style="font-family:Poppins,sans-serif;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:0.08em;color:{ICE_BLUE};opacity:0.6;margin:0 0 4px;">{heading_text}</p>',
            }),
        ]
        for label, href in links:
            elements.append(wgt("text-editor", {
                "editor":f'<p style="margin:0;"><a href="{href}" style="color:{ICE_BLUE};font-family:Inter,sans-serif;font-size:15px;text-decoration:none;">{label}</a></p>',
            }))
        return con({"flex_direction":"column","flex_gap":gap(10)}, elements)

    services_col = link_col("Services", [
        ("Individual Taxes","/income-tax/"),
        ("Small Business Taxes","/income-tax/"),
        ("ITIN Applications","/income-tax/"),
        ("Audit Services","/income-tax/"),
        ("Live Scan &amp; Notary","/notary/"),
    ])
    company_col = link_col("Company", [
        ("About Our Team","#"),
        ("Contact Us","#contact"),
        ("Secure Client Document Portal","#"),
        ("Fresno Tax Blog","#"),
    ])

    links_row = con(
        {"content_width":"boxed","flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(64),"flex_justify_content":"space-between","padding":pad(48,0,0,0)},
        [services_col, company_col]
    )
    tagline_row = con(
        {
            "content_width":"boxed",
            "border_border":"solid","border_width":pad(1,0,0,0),"border_color":"rgba(247,248,250,0.12)",
            "padding":pad(24,0,24,0),
        },
        [wgt("text-editor", {
            "editor":f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{ICE_BLUE};opacity:0.85;font-style:italic;margin:0;">At C&amp;R Tax Services, numbers are the foundation of your family&rsquo;s and your business&rsquo;s financial peace of mind. Let our family protect yours this season.</p>',
        })]
    )
    return sec(
        {"content_width":"full","background_color":MIDNIGHT,"padding":pad(0,0,48,0)},
        [links_row, tagline_row]
    )


# ── SAVE ─────────────────────────────────────────────────────────────────────

def save_elementor(post_id, elementor_data):
    el_json = json.dumps(elementor_data)
    path = f"wp-content/novamira-sandbox/el_{post_id}.json"
    wr = write_file(path, el_json)
    if not wr.get("bytes_written") and not wr.get("created"):
        print(f"  Write error for post {post_id}:", wr)
        return False
    result = php(f"""
$j = file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$d = json_decode($j, true);
update_post_meta({post_id}, '_elementor_data', wp_slash(json_encode($d)));
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$css_file = new Elementor\\Core\\Files\\CSS\\Post({post_id});
$css_file->update();
return ['saved'=>true,'elements'=>count($d),'css_len'=>strlen($css_file->get_content())];
""")
    return result.get("return_value", result)


def fix_mu_plugin():
    """Write corrected MU plugin to fix Google Fonts + season-tabs CSS."""
    # write-file is sandbox-only; write there then copy via PHP
    content = r"""<?php
/**
 * C&R Tax Services -- fonts + custom styles loader
 */
add_action('wp_head', function() {
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@700;800&display=swap" rel="stylesheet">
    <style id="crtax-custom">
    #season-tabs .elementor-tabs{display:flex;flex-direction:column;align-items:center;gap:32px;}
    #season-tabs .elementor-tabs-wrapper{display:inline-flex!important;background:#fff;border:1px solid #D7DEEA;border-radius:999px;padding:4px;gap:0;margin-bottom:0!important;}
    #season-tabs .elementor-tab-desktop-title{border:none!important;border-radius:999px!important;padding:8px 18px!important;font-family:Inter,sans-serif!important;font-weight:600!important;font-size:15px!important;color:#5A6B8C!important;background:transparent!important;cursor:pointer;transition:background .15s,color .15s;margin:0!important;}
    #season-tabs .elementor-tab-desktop-title.elementor-active{background:#1B2A5E!important;color:#F7F8FA!important;}
    #season-tabs .elementor-tab-mobile-title{display:none!important;}
    #season-tabs .elementor-tab-content{padding:0!important;border:none!important;background:transparent!important;}
    #season-tabs .elementor-tabs-content-wrapper{width:100%;display:flex;flex-direction:column;align-items:center;}
    .xpro-horizontal-menu a{font-family:Inter,sans-serif!important;}
    </style>
    <?php
}, 1);
"""
    sandbox_path = "wp-content/novamira-sandbox/crtax-fonts.php"
    wr = write_file(sandbox_path, content)
    if not wr.get("bytes_written") and not wr.get("created"):
        print("  write_file error:", wr)
        return wr
    result = php("""
$src = WP_CONTENT_DIR . '/novamira-sandbox/crtax-fonts.php';
$dst = WP_CONTENT_DIR . '/mu-plugins/crtax-fonts.php';
$ok = copy($src, $dst);
@unlink($src);
return ['copied' => $ok, 'exists' => file_exists($dst)];
""")
    return result.get("return_value", result)


def build():
    print("=== C&R Tax Services — Home Page Rebuild v3 ===\n")

    # Fix MU plugin first
    print("0. Fixing MU plugin (crtax-fonts.php)...")
    wr = fix_mu_plugin()
    print(f"   Written: {wr.get('bytes_written',0)} bytes")

    # Build new home page sections
    print("\n1. Building new home page (post 12)...")
    home_data = [
        home_hero(),
        home_featured_services(),
        home_why_trust(),
        home_service_area(),
        home_testimonials(),
        home_final_cta(),
        home_hours(),
        home_contact(),
        home_footer_links(),
    ]
    print(f"   Sections: {len(home_data)}")
    r = save_elementor(12, home_data)
    print(f"   Saved: {r}")

    # Clear caches
    print("\n2. Clearing caches...")
    php("""
do_action('breeze_clear_all_cache');
$dirs = array(WP_CONTENT_DIR.'/cache/breeze/', WP_CONTENT_DIR.'/cache/breeze-minification/');
foreach ($dirs as $dir) {
    if (is_dir($dir)) {
        $rit = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST);
        foreach ($rit as $f) @unlink($f->getPathname());
    }
}
echo 'done';
""")
    print("   Done.")
    print("\n=== BUILD COMPLETE ===")


if __name__ == "__main__":
    build()
