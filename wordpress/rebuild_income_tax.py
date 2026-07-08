#!/usr/bin/env python3
"""
C&R Tax Services — Income Tax page rebuild (v5 design)
Post ID: 28
"""
import json, random, string, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

# ── TOKENS ───────────────────────────────────────────────────────────────────
NAVY        = "#1B2A5E"
ROYAL_BLUE  = "#0A4A93"
RED         = "#E23A28"
ICE_BLUE    = "#EAF0F8"
OFF_WHITE   = "#F7F8FA"
SLATE       = "#5A6B8C"
MIDNIGHT    = "#121D42"
WHITE       = "#FFFFFF"
BORDER      = "#D7DEEA"
TEXT_BODY   = "#374151"
TEXT_HEAD   = "#111827"
TEXT_MUTED  = "#6B7280"

# spacing (px)
SP = {1:4,2:8,3:12,4:16,5:20,6:24,8:32,10:40,12:48,16:64,20:80,24:96}

# typography
T = {"sm":15,"base":17,"lg":20,"xl":24,"2xl":30,"3xl":38,"4xl":50,"5xl":64}

# ── MCP ──────────────────────────────────────────────────────────────────────
_sess = None
def sess():
    global _sess
    if not _sess:
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

# ── ELEMENT BUILDERS ─────────────────────────────────────────────────────────
def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def pad(t, r, b, l, u="px"):
    return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}

def size(v, u="px"):
    return {"size":v,"unit":u}

def gap(v, unit="px"):
    return {"column":v,"row":v,"unit":unit,"isLinked":True}

def con(settings, elements, is_inner=True):
    s = dict(settings)
    if "justify_content" in s: s["flex_justify_content"] = s.pop("justify_content")
    if "align_items" in s:     s["flex_align_items"]     = s.pop("align_items")
    if "gap" in s:             s["flex_gap"]             = s.pop("gap")
    if "background_color" in s and "background_background" not in s:
        s["background_background"] = "classic"
    return {"id":uid(),"elType":"container","isInner":is_inner,"settings":s,"elements":elements}

def sec(settings, elements):
    c = con(settings, elements, is_inner=False)
    c["isInner"] = False
    return c

def wgt(widget_type, settings):
    return {"id":uid(),"elType":"widget","widgetType":widget_type,"isInner":True,"settings":dict(settings),"elements":[]}

def save_elementor(post_id, elementor_data):
    el_json = json.dumps(elementor_data)
    path = f"wp-content/novamira-sandbox/el_{post_id}.json"
    wr = write_file(path, el_json)
    if not wr.get("bytes_written") and not wr.get("created"):
        print(f"  Write error:", wr); return False
    result = php(f"""
$j = file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$d = json_decode($j, true);
$slashed = wp_slash(json_encode($d));
update_post_meta({post_id}, '_elementor_data', $slashed);
update_post_meta({post_id}, '_elementor_draft_data', $slashed);
$autosave = wp_get_post_autosave({post_id});
if($autosave) wp_delete_post_revision($autosave->ID);
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$css_file = new Elementor\\Core\\Files\\CSS\\Post({post_id});
$css_file->update();
update_post_meta({post_id}, '_elementor_edit_mode', 'builder');
update_post_meta({post_id}, '_wp_page_template', 'elementor_header_footer');
return ['saved'=>true,'sections'=>count($d),'css_len'=>strlen($css_file->get_content())];
""")
    return result.get("return_value", result)

def clear_cache():
    php("""
Elementor\\Plugin::$instance->files_manager->clear_cache();
do_action('breeze_clear_all_cache');
$dirs=[WP_CONTENT_DIR.'/cache/breeze/',WP_CONTENT_DIR.'/cache/breeze-minification/'];
foreach($dirs as $dir){if(!is_dir($dir))continue;
$it=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir,FilesystemIterator::SKIP_DOTS),RecursiveIteratorIterator::CHILD_FIRST);
foreach($it as $f){if($f->isFile())@unlink($f->getPathname());}}
return true;
""")

# ── REUSABLE HTML HELPERS ─────────────────────────────────────────────────────
def badge_html(text, tone="red"):
    bg    = RED if tone == "red" else ICE_BLUE
    color = WHITE if tone == "red" else NAVY
    return (f'<span style="display:inline-block;padding:4px 14px;border-radius:999px;'
            f'background:{bg};color:{color};font-family:Inter,sans-serif;'
            f'font-size:13px;font-weight:600;letter-spacing:0.03em;">{text}</span>')

def h2_html(text):
    return (f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:{T["3xl"]}px;'
            f'color:{TEXT_HEAD};margin:0 0 20px;line-height:1.15;">{text}</h2>')

def p_html(text, last=False):
    mb = "0" if last else "16px"
    return (f'<p style="font-family:Inter,sans-serif;font-size:{T["base"]}px;'
            f'line-height:1.6;color:{TEXT_BODY};margin:0 0 {mb};">{text}</p>')

def img_placeholder(caption, alt="", height=220):
    return wgt("text-editor", {"editor":
        f'<div style="height:{height}px;border-radius:16px;background:{ICE_BLUE};'
        f'border:1px dashed {SLATE};display:flex;flex-direction:column;align-items:center;'
        f'justify-content:center;gap:10px;padding:24px;text-align:center;">'
        f'<p style="font-family:Inter,sans-serif;font-size:14px;color:{SLATE};margin:0;">📷 {caption}</p>'
        + (f'<p style="font-family:Inter,sans-serif;font-size:12px;color:{SLATE};opacity:.7;font-style:italic;margin:0;">alt: &ldquo;{alt}&rdquo;</p>' if alt else "")
        + '</div>'
    })

def city_pills_html():
    cities = ["Fresno","Clovis","Sanger","Selma","Madera"]
    spans = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
        f'border-radius:999px;background:{WHITE};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:{T["sm"]}px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-map-marker-alt" style="font-size:14px;color:{ROYAL_BLUE};"></i>{c}</span>'
        for c in cities
    )
    return f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin:{SP[8]}px 0;">{spans}</div>'

def check_item_html(text):
    return (f'<li style="display:flex;align-items:flex-start;gap:14px;padding:{SP[5]}px 0;'
            f'border-bottom:1px solid {BORDER};">'
            f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:28px;height:28px;border-radius:999px;background:{ICE_BLUE};flex-shrink:0;margin-top:2px;">'
            f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i></span>'
            f'<span style="font-family:Inter,sans-serif;font-size:{T["lg"]}px;color:{TEXT_BODY};'
            f'line-height:1.35;padding-top:3px;">{text}</span></li>')

def differentiator_card_html(icon_fa, title, body):
    return (f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:10px;padding:{SP[6]}px;">'
            f'<div style="width:40px;height:40px;border-radius:10px;background:{NAVY};'
            f'display:flex;align-items:center;justify-content:center;margin-bottom:12px;">'
            f'<i class="fas fa-{icon_fa}" style="font-size:20px;color:{OFF_WHITE};"></i></div>'
            f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:{T["base"]}px;'
            f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
            f'<p style="font-family:Inter,sans-serif;font-size:{T["sm"]}px;color:{TEXT_BODY};'
            f'line-height:1.6;margin:0;">{body}</p>'
            f'</div>')

# ── SECTION BUILDERS ──────────────────────────────────────────────────────────

def inner_box(max_width=760, bg=None, extra=None):
    """Boxed inner container."""
    s = {"content_width":"boxed","width":size(max_width,"px"),"flex_direction":"column"}
    if bg:
        s["background_color"] = bg
    if extra:
        s.update(extra)
    return s

def section_wrap(bg, py=80, children_fn=None):
    """Full-width section wrapper."""
    s = {"content_width":"full","padding":pad(py,32,py,32)}
    if bg and bg != WHITE:
        s["background_color"] = bg
    return s


# 1 ── HERO ────────────────────────────────────────────────────────────────────
def sec_hero():
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(80,32,80,32)},
        [con(inner_box(780), [
            # Icon box
            wgt("text-editor", {"editor":
                f'<div style="width:56px;height:56px;border-radius:10px;'
                f'background:rgba(247,248,250,0.12);display:flex;align-items:center;'
                f'justify-content:center;margin-bottom:{SP[6]}px;">'
                f'<i class="fas fa-calculator" style="font-size:28px;color:{WHITE};"></i></div>'
            }),
            # Badge
            wgt("text-editor", {"editor": f'<div style="margin-bottom:18px;">{badge_html("Available Any Day and All Year!")}</div>'}),
            # H1
            wgt("heading", {
                "title": "The Best Tax Preparation in the Central Valley &mdash; Without the Stress, Surprises, or Confusing Fine Print",
                "header_size": "h1",
                "typography_typography": "custom",
                "typography_font_family": "Poppins", "typography_font_weight": "800",
                "typography_font_size": size(T["4xl"]),
                "title_color": WHITE,
                "_margin": {"top":"0","right":"0","bottom":"16","left":"0","unit":"px","isLinked":False},
            }),
            # Intro
            wgt("text-editor", {"editor":
                f'<p style="font-family:Inter,sans-serif;font-size:{T["lg"]}px;color:{ICE_BLUE};'
                f'line-height:1.6;max-width:620px;margin:0 0 {SP[8]}px;">'
                f'Full-service preparation for individuals, small businesses, and every filing '
                f'situation in between &mdash; plus virtual and online tax preparation, available any day, all year.</p>'
            }),
            # CTAs row
            con(
                {"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(12),"padding":pad(0,0,0,0)},
                [
                    wgt("button", {
                        "text":"Schedule an Appointment","link":{"url":"tel:5599627503"},
                        "button_type":"info","size":"lg",
                        "button_background_color":RED,"button_text_color":WHITE,
                        "button_background_hover_color":"#C22E1F","button_background_hover_background":"classic",
                        "border_radius":pad(6,6,6,6),
                        "button_padding":pad(14,28,14,28),
                        "typography_font_family":"Inter","typography_font_weight":"600",
                    }),
                    wgt("button", {
                        "text":"Upload Your Docs (Virtual Prep)","link":{"url":"#contact"},
                        "button_type":"info","size":"lg",
                        "button_background_color":"transparent","button_text_color":WHITE,
                        "button_background_background":"classic",
                        "border_border":"solid","border_width":pad(2,2,2,2),"border_color":"rgba(247,248,250,0.4)",
                        "border_radius":pad(6,6,6,6),
                        "button_padding":pad(14,28,14,28),
                        "typography_font_family":"Inter","typography_font_weight":"600",
                    }),
                ]
            ),
        ])]
    )


# 2 ── INTRO (2-col: text + image) ─────────────────────────────────────────────
def sec_intro():
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner_box(780), [
            con(
                {"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(48),"flex_align_items":"flex-start","padding":pad(0,0,0,0)},
                [
                    con({"flex":"1 1 420px","flex_direction":"column","padding":pad(0,0,0,0)}, [
                        wgt("text-editor", {"editor":
                            p_html("Tax season has a way of sneaking up on you. One day you&rsquo;re enjoying the holidays. The next, you&rsquo;re staring at a pile of W-2s, 1099s, and receipts, wondering if you&rsquo;re about to miss a deduction &mdash; or worse, make a mistake that brings a letter from the IRS. Families and business owners all over Fresno feel that knot in their stomach every year.")
                            + p_html("That&rsquo;s exactly why C&amp;R Tax Services exists. We&rsquo;re a local, bilingual tax preparation firm built to make filing simple, accurate, and honest. Whether you&rsquo;re filing a basic personal return, running a small business, managing rental properties, or applying for an ITIN, we walk you through every step in plain language &mdash; English or Spanish. <strong>Se habla espa&ntilde;ol</strong>, and we mean it. You&rsquo;ll never leave our office wondering what was filed or why.")
                            + p_html("We also believe you should know your price <em>before</em> we file, not after &mdash; no hidden fees, no surprise upgrades. Our team is registered, meets every federal and California filing requirement, and stays open year-round. So when the IRS sends a letter in August, we&rsquo;re still here to help you answer it.", last=True)
                        }),
                    ]),
                    con({"flex":"1 1 280px","max_width":size(320),"padding":pad(0,0,0,0)}, [
                        img_placeholder(
                            "Warm photo of a preparer greeting a Fresno family across a desk, documents organized neatly.",
                            "Bilingual tax preparation appointment at C&R Tax Services in Fresno, CA",
                            260
                        )
                    ]),
                ]
            ),
        ])]
    )


# 3 ── WHAT THIS SOLVES ────────────────────────────────────────────────────────
def sec_what_solves():
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner_box(760), [
            wgt("text-editor", {"editor":
                h2_html("What This Service Solves")
                + p_html("Most people don&rsquo;t call a tax professional when things are going smoothly. They call because something changed &mdash; a side business, a delivery-app job, a rental property in Clovis with a Schedule E they&rsquo;ve never filed, or a mid-year move to California that turned into a multi-state return their old software can&rsquo;t handle.")
                + p_html("Others come to us after a mistake has already happened: a missed form, a return filed under the wrong status, an IRS notice sitting unopened on the kitchen counter. Professional tax preparation solves these problems before they grow. We handle amendments to fix past returns, extensions when you need more time, prior-year reviews to recover money you may have left on the table, and audit support when a notice arrives and you need someone in your corner.")
                + p_html("For many Central Valley families, there&rsquo;s one more hurdle: filing without a Social Security number. As certified ITIN application specialists, we help non-SSN filers get set up correctly the first time. Whatever brought you here &mdash; a new business, a new property, a new country, or just a new season of life &mdash; accurate tax preparation is how you protect what you&rsquo;ve earned.", last=True)
            }),
            img_placeholder(
                "Split image or collage — a rideshare driver, a small storefront, and a rental home 'For Rent' sign.",
                "Common situations that call for professional tax preparation in Fresno — self-employment, small business, and rental property taxes",
                220
            ),
        ])]
    )


# 4 ── EVERY SITUATION WE HANDLE (checklist) ───────────────────────────────────
SERVICE_ITEMS = [
    "Individual",
    "Small Business / Self Employed",
    "Rental Properties",
    "Corporations, Partnerships, &amp; LLC&rsquo;s",
    "ITIN Applications",
    "Amendments",
    "Audit Services",
    "Extensions",
    "Prior Year Reviews",
    "Multi State Returns",
    "Virtual/Online Tax Preparation &ndash; Available Any Day and All Year!",
]

def sec_checklist():
    items_html = "".join(check_item_html(it) for it in SERVICE_ITEMS)
    # Remove bottom border from last item
    items_html = items_html[::-1].replace(f";border-bottom:1px solid {BORDER}"[::-1], "", 1)[::-1]
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner_box(760), [
            wgt("text-editor", {"editor": h2_html("Every Situation We Handle")}),
            wgt("text-editor", {"editor":
                f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:16px;'
                f'box-shadow:0 1px 4px rgba(0,0,0,0.06);padding:{SP[10]}px;">'
                f'<ul style="list-style:none;margin:0;padding:0;">{items_html}</ul></div>'
            }),
        ])]
    )


# 5 ── HOW WE DO IT BETTER ─────────────────────────────────────────────────────
DIFFERENTIATORS = [
    ("language", "We serve you in your language", "Se habla espa&ntilde;ol, from your first phone call to your final signature."),
    ("tag",      "Upfront, transparent pricing",  "You&rsquo;ll know your cost before we file. Period."),
    ("shield-alt","100% accuracy guarantee",      "If we make an error on your return, we cover the adjustment costs and amend it for free."),
    ("upload",   "Secure virtual tax preparation","Upload your documents from Fresno, Clovis, Sanger, Selma, or Madera and file without hunting for parking."),
]

def sec_how_better():
    cards_html = "".join(differentiator_card_html(fa, t, b) for fa, t, b in DIFFERENTIATORS)
    grid_html = (f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));'
                 f'gap:{SP[6]}px;margin-top:{SP[8]}px;margin-bottom:{SP[8]}px;">{cards_html}</div>')
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner_box(760), [
            wgt("text-editor", {"editor":
                h2_html("How C&amp;R Tax Services Does It Better")
                + p_html("Big-box tax chains and DIY software treat you like a ticket number. We treat you like a neighbor, because you are one. Every return starts with a real conversation about your year &mdash; what changed, what you earned, what you&rsquo;re hoping to accomplish. From there, we build your return line by line, checking for every credit and deduction you legally qualify for, whether it&rsquo;s a simple individual return or a complex filing for a corporation, partnership, or LLC.")
                + p_html("We built this firm for the Central Valley &mdash; for the farm families, the small business owners, the young professionals, and the hardworking households that keep this region running. When you sit down with us, in person or online, you get local knowledge of California tax rules paired with the patience to actually explain them.", last=True)
                + grid_html
            }),
            img_placeholder(
                "Screenshot-style graphic of the secure document upload portal on a phone, with a Central Valley orchard or Fresno skyline in the background.",
                "Virtual tax preparation and secure document upload for Central Valley clients of C&R Tax Services",
                220
            ),
        ])]
    )


# 6 ── REAL-WORLD RESULTS ──────────────────────────────────────────────────────
def sec_results():
    review_box = (f'<div style="margin-top:{SP[8]}px;padding:18px 22px;'
                  f'background:{ICE_BLUE};border:1px solid {BORDER};border-radius:10px;">'
                  f'<p style="font-family:Inter,sans-serif;font-size:{T["sm"]}px;'
                  f'color:{TEXT_MUTED};font-style:italic;margin:0;">'
                  f'Verified client reviews will go here once collected via Google Business Profile.</p></div>')
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner_box(700), [
            wgt("text-editor", {"editor":
                h2_html("Real-World Results")
                + p_html("Ask around the Central Valley and you&rsquo;ll hear the same words used to describe a great tax preparer: patient, thorough, honest about pricing, and focused on getting you every dollar you deserve. Clients tell us the biggest relief isn&rsquo;t just the refund &mdash; it&rsquo;s finally understanding their own taxes, and knowing nothing was missed or hidden.")
                + p_html("It&rsquo;s the small business owner who stopped dreading quarterly deadlines. It&rsquo;s the family who fixed a prior-year mistake and recovered money they didn&rsquo;t know they&rsquo;d lost. It&rsquo;s the ITIN applicant who filed correctly the first time instead of waiting months on a rejected application. When your taxes are done right, you get your time, your money, and your calm back.", last=True)
                + review_box
            }),
        ])]
    )


# 7 ── LOCAL TRUST & LICENSING ─────────────────────────────────────────────────
def sec_local_trust():
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner_box(760), [
            wgt("text-editor", {"editor":
                h2_html("Local Trust &amp; Licensing")
                + p_html("C&amp;R Tax Services proudly serves families and business owners across Fresno, Clovis, Sanger, Selma, and Madera. We&rsquo;re not a seasonal pop-up that disappears the day after the deadline &mdash; we&rsquo;re a year-round Central Valley firm. When you get an IRS letter in July, need an extension in October, or want a prior-year review in November, our door is open and our phone gets answered.")
                + p_html("Every return we prepare meets federal and California registration and compliance standards, and your documents are always handled through secure, protected channels &mdash; whether you file in person or through our virtual portal.", last=True)
                + city_pills_html()
            }),
            img_placeholder(
                "Simple map graphic highlighting the Fresno, Clovis, Sanger, Selma, and Madera service areas.",
                "C&R Tax Services tax preparation service areas across the Central Valley including Fresno, Clovis, Sanger, Selma, and Madera",
                220
            ),
        ])]
    )


# 8 ── FINAL CTA ───────────────────────────────────────────────────────────────
def sec_final_cta():
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(96,32,96,32)},
        [con(inner_box(780), [
            wgt("heading", {
                "title": "You Work Hard for Your Money &mdash; This Is the Year to Keep More of It",
                "header_size": "h2",
                "typography_typography": "custom",
                "typography_font_family": "Poppins", "typography_font_weight": "700",
                "typography_font_size": size(T["3xl"]),
                "title_color": WHITE,
                "_margin": {"top":"0","right":"0","bottom":"16","left":"0","unit":"px","isLinked":False},
            }),
            wgt("text-editor", {"editor":
                f'<p style="font-family:Inter,sans-serif;font-size:{T["base"]}px;color:{ICE_BLUE};'
                f'line-height:1.6;max-width:620px;margin:0 0 {SP[8]}px;">'
                f'The forms aren&rsquo;t getting simpler and California&rsquo;s rules aren&rsquo;t getting easier. '
                f'You deserve a friendly, local expert who does this every day, explains everything clearly, '
                f'and guarantees the work. Call C&amp;R Tax Services to schedule your appointment, or upload '
                f'your documents through our secure virtual portal and file from anywhere in the Central Valley. '
                f'Se habla espa&ntilde;ol.</p>'
            }),
            con(
                {"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(12),
                 "padding":pad(0,0,SP[10],0)},
                [
                    wgt("button", {
                        "text":"Schedule an Appointment","link":{"url":"tel:5599627503"},
                        "button_type":"info","size":"lg",
                        "button_background_color":RED,"button_text_color":WHITE,
                        "button_background_hover_color":"#C22E1F","button_background_hover_background":"classic",
                        "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                        "typography_font_family":"Inter","typography_font_weight":"600",
                    }),
                    wgt("button", {
                        "text":"Upload Your Docs (Virtual Prep)","link":{"url":"#contact"},
                        "button_type":"info","size":"lg",
                        "button_background_color":"transparent","button_text_color":WHITE,
                        "button_background_background":"classic",
                        "border_border":"solid","border_width":pad(2,2,2,2),"border_color":"rgba(247,248,250,0.4)",
                        "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                        "typography_font_family":"Inter","typography_font_weight":"600",
                    }),
                    wgt("button", {
                        "text":"Get a Free Estimate","link":{"url":"#contact"},
                        "button_type":"info","size":"lg",
                        "button_background_color":"rgba(255,255,255,0.1)","button_text_color":WHITE,
                        "button_background_background":"classic",
                        "border_border":"solid","border_width":pad(2,2,2,2),"border_color":"rgba(247,248,250,0.25)",
                        "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                        "typography_font_family":"Inter","typography_font_weight":"600",
                    }),
                ]
            ),
            img_placeholder(
                "High-contrast banner photo of a smiling preparer with a phone/headset.",
                "Schedule tax preparation with C&R Tax Services in Fresno — call or file virtually today",
                220
            ),
        ])]
    )


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    print("=== Income Tax Page — v5 Rebuild ===\n")
    sections = [
        sec_hero(),
        sec_intro(),
        sec_what_solves(),
        sec_checklist(),
        sec_how_better(),
        sec_results(),
        sec_local_trust(),
        sec_final_cta(),
    ]
    print(f"  Sections: {len(sections)}")
    r = save_elementor(28, sections)
    print(f"  Saved: {r}")
    print("\nClearing caches...")
    clear_cache()
    print("=== DONE ===")


if __name__ == "__main__":
    build()
