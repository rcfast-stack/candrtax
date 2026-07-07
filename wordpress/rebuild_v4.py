#!/usr/bin/env python3
"""
C&R Tax Services — v4 rebuild
Changes vs v3:
  - FeaturedServices: elevated cards with colored top border + chip tags
  - 3 service pages (Income Tax / Notary / Livescan) using ServicePageShell layout
  - Nav simplified: Home | Income Tax | Notary | Livescan | Contact
"""
import json, random, string, requests, sys

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

# ── COLORS ───────────────────────────────────────────────────────────────────
NAVY        = "#1B2A5E"
ROYAL_BLUE  = "#0A4A93"
RED         = "#E23A28"
ICE_BLUE    = "#EAF0F8"
OFF_WHITE   = "#F7F8FA"
SLATE       = "#5A6B8C"
MIDNIGHT    = "#121D42"
WHITE       = "#FFFFFF"
BORDER      = "#D7DEEA"

# ── MCP SESSION ──────────────────────────────────────────────────────────────
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

# ── HELPERS ──────────────────────────────────────────────────────────────────
def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def pad(t, r, b, l, u="px"):
    return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}

def size(v, u="px"):
    return {"size":v,"unit":u}

def gap(v, unit="px"):
    return {"column":v,"row":v,"unit":unit,"isLinked":True}

def fa(name):
    return {"value": f"fas fa-{name}", "library": "fa-solid"}

def con(settings, elements, is_inner=True):
    """Build an Elementor container."""
    s = dict(settings)
    # fix common key names
    if "justify_content" in s:
        s["flex_justify_content"] = s.pop("justify_content")
    if "align_items" in s:
        s["flex_align_items"] = s.pop("align_items")
    if "gap" in s:
        s["flex_gap"] = s.pop("gap")
    # ensure background_background when background_color set
    if "background_color" in s and "background_background" not in s:
        s["background_background"] = "classic"
    return {
        "id": uid(), "elType": "container", "isInner": is_inner,
        "settings": s, "elements": elements
    }

def sec(settings, elements):
    """Top-level container (section)."""
    c = con(settings, elements, is_inner=False)
    c["isInner"] = False
    return c

def wgt(widget_type, settings):
    """Build an Elementor widget."""
    s = dict(settings)
    if "justify_content" in s:
        s["flex_justify_content"] = s.pop("justify_content")
    if "align_items" in s:
        s["flex_align_items"] = s.pop("align_items")
    if widget_type == "button":
        if "button_background_hover_color" not in s:
            s["button_background_hover_background"] = "classic"
    return {"id": uid(), "elType": "widget", "widgetType": widget_type, "isInner": True, "settings": s, "elements": []}

def img_placeholder(caption, alt="", height=320):
    """ICE_BLUE dashed image placeholder container."""
    return con(
        {
            "min_height": size(height),
            "background_color": ICE_BLUE,
            "border_border": "dashed", "border_width": pad(2,2,2,2), "border_color": SLATE,
            "border_radius": pad(8,8,8,8),
            "flex_justify_content": "center", "flex_align_items": "center",
            "padding": pad(24,24,24,24),
        },
        [wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:14px;color:{SLATE};text-align:center;margin:0;">'
                      f'📷 {caption}</p>'
                      + (f'<p style="font-family:Inter,sans-serif;font-size:12px;color:{SLATE};opacity:0.7;text-align:center;margin:6px 0 0;font-style:italic;">alt: &ldquo;{alt}&rdquo;</p>' if alt else ""),
        })]
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
$slashed = wp_slash(json_encode($d));
update_post_meta({post_id}, '_elementor_data', $slashed);
update_post_meta({post_id}, '_elementor_draft_data', $slashed);
// delete autosave so editor loads fresh
$autosave = wp_get_post_autosave({post_id});
if($autosave) wp_delete_post_revision($autosave->ID);
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$css_file = new Elementor\\Core\\Files\\CSS\\Post({post_id});
$css_file->update();
// ensure elementor mode
update_post_meta({post_id}, '_elementor_edit_mode', 'builder');
update_post_meta({post_id}, '_wp_page_template', 'elementor_header_footer');
return ['saved'=>true,'elements'=>count($d),'css_len'=>strlen($css_file->get_content())];
""")
    return result.get("return_value", result)

def clear_cache():
    php("""
Elementor\\Plugin::$instance->files_manager->clear_cache();
do_action('breeze_clear_all_cache');
$dirs = [WP_CONTENT_DIR.'/cache/breeze/', WP_CONTENT_DIR.'/cache/breeze-minification/'];
foreach($dirs as $dir) {
    if(!is_dir($dir)) continue;
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST);
    foreach($it as $f) { if($f->isFile()) @unlink($f->getPathname()); }
}
return true;
""")

# ── SHARED WIDGETS ───────────────────────────────────────────────────────────

def badge_html(text, tone="red"):
    bg = RED if tone == "red" else ICE_BLUE
    color = WHITE if tone == "red" else NAVY
    return (f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;'
            f'background:{bg};color:{color};font-family:Inter,sans-serif;'
            f'font-size:13px;font-weight:600;letter-spacing:0.03em;">{text}</span>')

def check_row(text):
    """Single checklist item: 28px pill icon + text."""
    return con(
        {"flex_direction": "row", "flex_align_items": "flex-start", "flex_gap": gap(14),
         "padding": pad(0,0,0,0)},
        [
            con(
                {"width": size(28), "min_height": size(28),
                 "border_radius": pad(999,999,999,999),
                 "background_color": ICE_BLUE,
                 "flex_justify_content": "center", "flex_align_items": "center",
                 "flex_shrink": "0", "padding": pad(0,0,0,0)},
                [wgt("icon", {"selected_icon": fa("check"), "size": size(14), "icon_color": ROYAL_BLUE})]
            ),
            wgt("text-editor", {
                "editor": f'<p style="font-family:Inter,sans-serif;font-size:18px;color:#374151;line-height:1.4;padding-top:3px;margin:0;">{text}</p>'
            }),
        ]
    )


# ── FEATURED SERVICES (v4) ────────────────────────────────────────────────────

def chips_html(chips):
    """Render chip tags as a single HTML block."""
    spans = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:5px;padding:5px 12px;'
        f'border-radius:999px;background:{OFF_WHITE};border:1px solid {BORDER};'
        f'font-size:12px;font-weight:500;color:{NAVY};margin:0 4px 6px 0;">'
        f'&#10003; {c}</span>'
        for c in chips
    )
    return f'<div style="display:flex;flex-wrap:wrap;margin-bottom:20px;">{spans}</div>'

FA_MAP = {
    "home": "home", "briefcase": "briefcase", "file-text": "file-alt",
    "shield-check": "shield-alt", "stamp": "stamp",
}

def featured_card(icon_name, accent, title, paragraphs, chips, note=None, link_label=None, link_href=None, is_last=False):
    icon_fa = FA_MAP.get(icon_name, icon_name)
    inner_elements = [
        # Icon + title row
        con(
            {"flex_direction": "row", "flex_align_items": "center", "flex_gap": gap(16),
             "padding": pad(0,0,18,0)},
            [
                con(
                    {"width": size(52), "min_height": size(52),
                     "border_radius": pad(8,8,8,8),
                     "background_color": accent,
                     "flex_justify_content": "center", "flex_align_items": "center",
                     "padding": pad(0,0,0,0)},
                    [wgt("icon", {"selected_icon": fa(icon_fa), "size": size(26), "icon_color": WHITE})]
                ),
                wgt("heading", {
                    "title": title, "header_size": "h3",
                    "typography_typography": "custom",
                    "typography_font_family": "Poppins",
                    "typography_font_weight": "700",
                    "typography_font_size": size(22),
                    "title_color": "#111827",
                }),
            ]
        ),
    ]

    for p in paragraphs:
        inner_elements.append(wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:16px;line-height:1.7;color:#374151;margin:0 0 16px;">{p}</p>'
        }))

    inner_elements.append(wgt("text-editor", {"editor": chips_html(chips)}))

    if note:
        inner_elements.append(wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:13px;color:{SLATE};font-style:italic;margin:0 0 16px;">{note}</p>'
        }))

    if link_label and link_href:
        inner_elements.append(wgt("text-editor", {
            "editor": f'<p style="margin:0;"><a href="{link_href}" style="font-family:Inter,sans-serif;font-size:14px;font-weight:600;color:{ROYAL_BLUE};text-decoration:none;">{link_label} &#10230;</a></p>'
        }))

    mb = 0 if is_last else 32
    return con(
        {
            "background_color": WHITE,
            "border_border": "solid",
            "border_width": pad(4, 1, 1, 1),
            "border_color": accent,
            "border_radius": pad(8, 8, 8, 8),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal":0,"vertical":2,"blur":8,"spread":0,"color":"rgba(0,0,0,0.08)"},
            "padding": pad(40, 40, 40, 40),
            "margin": {"top":"0","right":"0","bottom":str(mb),"left":"0","unit":"px","isLinked":False},
        },
        inner_elements
    )


def home_featured_services():
    cards = [
        featured_card(
            "home", NAVY,
            "Individual &amp; Rental Property Taxes",
            [
                "For a lot of people, filing personal taxes feels like a guessing game. Did you claim every deduction you qualify for? Was that side income reported the right way? Is your refund as big as it should be? Filing alone, or with generic software, often leaves those questions hanging in the air.",
                "We do it differently. At C&amp;R Tax Services, we sit down with you, in person or virtually, and walk through your full financial picture together, and make sure every credit and deduction you&rsquo;re entitled to actually lands on your return.",
                "If you own rental property, we dig even deeper &mdash; Schedule E filings, depreciation, and the rules around passive income, tracked carefully so your rental income works for you instead of against you.",
            ],
            ["Individual", "Rental Properties", "Virtual/Online Tax Preparation &ndash; Available Any Day and All Year!"],
            link_label="Learn more about our Individual Tax Services", link_href="/individual-tax-services"
        ),
        featured_card(
            "briefcase", ROYAL_BLUE,
            "Small Business &amp; Corporate Business Taxes",
            [
                "Running a business in the Central Valley is demanding enough without the IRS piling onto your to-do list. Between quarterly estimates, payroll questions, entity rules, and California&rsquo;s own layer of requirements, small business taxes can eat up hours you don&rsquo;t have.",
                "C&amp;R Tax Services handles small business and corporate business taxes for sole proprietors, partnerships, LLCs, S-Corps, and C-Corps across Fresno &mdash; and if your business operates across state lines, our multi-state return experience keeps every jurisdiction squared away.",
            ],
            ["Small Business / Self Employed", "Corporations, Partnerships, &amp; LLC&rsquo;s"],
            link_label="Learn more about our Business Tax Preparation", link_href="/business-tax-preparation"
        ),
        featured_card(
            "file-text", NAVY,
            "ITIN Applications &amp; Multi-State Returns",
            [
                "If you don&rsquo;t have a Social Security number, filing taxes can feel like a door that&rsquo;s closed to you. It isn&rsquo;t. C&amp;R Tax Services provides professional support for ITIN applications, helping non-SSN filers in Fresno get the Individual Taxpayer Identification Number they need to file correctly and claim eligible credits.",
                "We also prepare multi-state returns for anyone who earned income in more than one state &mdash; sorting out exactly what each state is owed so you never pay twice or file incorrectly.",
            ],
            ["ITIN Applications", "Multi State Returns"],
            link_label="Learn more about ITIN &amp; Multi-State Services", link_href="/itin-multi-state"
        ),
        featured_card(
            "shield-check", ROYAL_BLUE,
            "Audit Services, Tax Extensions &amp; Amendments",
            [
                "Few things ruin a week faster than an envelope from the IRS. C&amp;R Tax Services provides professional audit services and IRS notice support for taxpayers across the Fresno area &mdash; we read the notice with you and help you respond correctly and on time.",
                "If an old return needs fixing, our tax amendment service sets the record straight. And if life simply got in the way this year, we can file your tax extension quickly so you get breathing room without late-filing penalties.",
            ],
            ["Amendments", "Audit Services", "Extensions", "Prior Year Reviews"],
            link_label="Learn more about Audit, Extension &amp; Amendment Services", link_href="/tax-relief-amendments"
        ),
        featured_card(
            "stamp", NAVY,
            "Notary Public, Loan Signing &amp; Live Scan Fingerprints",
            [
                "Taxes aren&rsquo;t the only paperwork life throws your way. C&amp;R Tax Services also serves Fresno as a Notary Public and Loan Signing Agent and provides Live Scan fingerprint services &mdash; a convenient one-stop shop for the documents and verifications that keep your life and business moving.",
                "Need something notarized for a real estate deal, a power of attorney, or a business agreement? We handle it promptly. Closing on a loan? Our certified loan signing service walks you through the entire signing package. Applying for a job or license that requires a background check? Our state-compliant Live Scan fingerprinting captures and submits your prints correctly the first time.",
            ],
            ["Bank Documents", "Travel Documents", "Power of Attorney", "Real Estate Documents &amp; Forms",
             "Legal Documents &amp; Forms", "Livescan Background Checks", "FD-258 Card"],
            note="Mobile Services available upon request &ndash; Travel fees will be applied.",
            link_label="Learn more about Notary &amp; Live Scan Services", link_href="/notary-livescan-services",
            is_last=True,
        ),
    ]

    section_badge = wgt("text-editor", {
        "editor": f'<div style="text-align:center;margin-bottom:16px;">{badge_html("Full-Service Offerings", "ice")}</div>'
    })
    section_heading = wgt("heading", {
        "title": "Our Featured Tax &amp; Business Services",
        "header_size": "h2", "align": "center",
        "typography_typography": "custom",
        "typography_font_family": "Poppins", "typography_font_weight": "700",
        "typography_font_size": size(32),
        "title_color": "#111827",
    })

    photo = img_placeholder(
        "A clean collage or split-panel showing a tax document review, a notary stamp on paperwork, and a Live Scan fingerprint device.",
        "Tax preparation, notary public, and Live Scan fingerprint services in Fresno"
    )

    inner = con(
        {"content_width": "boxed", "width": size(800, "px"),
         "flex_direction": "column", "padding": pad(0,0,0,0)},
        [section_badge, section_heading,
         con({"padding": pad(48,0,0,0), "flex_direction": "column"}, cards),
         con({"padding": pad(40,0,0,0)}, [photo])]
    )
    return sec(
        {"content_width": "full", "padding": pad(96, 32, 96, 32), "_element_id": "services"},
        [inner]
    )


# ── HOME PAGE (unchanged sections from v3, new FeaturedServices) ──────────────
# Import v3 sections
sys.path.insert(0, "/home/user/candrtax")
from wordpress import rebuild_v3 as v3

def build_home():
    sections = [
        v3.home_hero(),
        home_featured_services(),    # new v4 card design
        v3.home_why_trust(),
        v3.home_service_area(),
        v3.home_testimonials(),
        v3.home_final_cta(),
        v3.home_hours(),
        v3.home_contact(),
        v3.home_footer_links(),
    ]
    return sections


# ── SERVICE PAGE SHELL ────────────────────────────────────────────────────────

def service_page(icon_name, eyebrow, title, intro, items, footnote=None):
    icon_fa = {"calculator": "calculator", "stamp": "stamp", "fingerprint": "fingerprint"}.get(icon_name, icon_name)

    # Hero section
    hero = sec(
        {"content_width": "full", "background_color": NAVY, "padding": pad(80, 32, 80, 32)},
        [con(
            {"content_width": "boxed", "width": size(760, "px"), "flex_direction": "column"},
            [
                # Icon box
                con(
                    {"width": size(56), "min_height": size(56), "border_radius": pad(8,8,8,8),
                     "background_color": "rgba(247,248,250,0.12)", "background_background": "classic",
                     "flex_justify_content": "center", "flex_align_items": "center",
                     "padding": pad(0,0,0,0), "margin": {"top":"0","right":"0","bottom":"24","left":"0","unit":"px","isLinked":False}},
                    [wgt("icon", {"selected_icon": fa(icon_fa), "size": size(28), "icon_color": WHITE})]
                ),
                # Badge
                wgt("text-editor", {"editor": f'<div>{badge_html(eyebrow, "red")}</div>'}),
                # H1
                wgt("heading", {
                    "title": title, "header_size": "h1",
                    "typography_typography": "custom",
                    "typography_font_family": "Poppins", "typography_font_weight": "800",
                    "typography_font_size": size(40),
                    "title_color": WHITE,
                    "_margin": {"top":"18","right":"0","bottom":"16","left":"0","unit":"px","isLinked":False},
                }),
                # Intro
                wgt("text-editor", {
                    "editor": f'<p style="font-family:Inter,sans-serif;font-size:18px;color:{ICE_BLUE};line-height:1.7;max-width:620px;margin:0;">{intro}</p>'
                }),
            ]
        )]
    )

    # Checklist section
    check_items = [check_row(item) for item in items]
    footnote_widget = []
    if footnote:
        footnote_widget = [wgt("text-editor", {
            "editor": f'<p style="font-family:Inter,sans-serif;font-size:14px;color:{SLATE};font-style:italic;margin:32px 0 0;padding-top:24px;border-top:1px solid {BORDER};">{footnote}</p>'
        })]

    cta_btn = wgt("button", {
        "text": "Call (559) 962-7503",
        "link": {"url": "tel:5599627503"},
        "button_type": "info", "size": "lg", "align": "center",
        "button_background_color": RED,
        "button_text_color": WHITE,
        "button_background_hover_color": "#C22E1F",
        "button_background_hover_background": "classic",
        "border_radius": pad(6,6,6,6),
        "button_padding": pad(14,28,14,28),
        "typography_font_family": "Inter", "typography_font_weight": "600",
    })

    checklist_section = sec(
        {"content_width": "full", "padding": pad(80, 32, 80, 32)},
        [con(
            {"content_width": "boxed", "width": size(760, "px"), "flex_direction": "column"},
            [
                con(
                    {
                        "background_color": WHITE,
                        "border_border": "solid", "border_width": pad(1,1,1,1), "border_color": BORDER,
                        "border_radius": pad(8,8,8,8),
                        "box_shadow_box_shadow_type": "yes",
                        "box_shadow_box_shadow": {"horizontal":0,"vertical":1,"blur":4,"spread":0,"color":"rgba(0,0,0,0.06)"},
                        "padding": pad(40,40,40,40),
                        "flex_direction": "column", "flex_gap": gap(20),
                    },
                    check_items + footnote_widget
                ),
                con({"padding": pad(48, 0, 0, 0), "flex_justify_content": "center"}, [cta_btn]),
            ]
        )]
    )

    return [hero, checklist_section]


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    print("=== C&R Tax Services — v4 Rebuild ===\n")

    # 1. Home page
    print("1. Home page (post 12) — updated FeaturedServices...")
    home_sections = build_home()
    r = save_elementor(12, home_sections)
    print(f"   Saved: {r}")

    # 2. Income Tax page (post 28)
    print("2. Income Tax page (post 28)...")
    r = save_elementor(28, service_page(
        "calculator",
        "Available Any Day and All Year!",
        "Income Tax",
        "Full-service preparation for individuals, small businesses, and every filing situation in between &mdash; plus virtual and online tax preparation, available any day, all year.",
        [
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
    ))
    print(f"   Saved: {r}")

    # 3. Notary page (post 29)
    print("3. Notary page (post 29)...")
    r = save_elementor(29, service_page(
        "stamp",
        "Mobile Service Available",
        "Notary Public &amp; Loan Signing Agent",
        "Certified notarization and loan signing for the documents that matter most &mdash; in-office or on the road.",
        [
            "Bank Documents",
            "Travel Documents",
            "Power of Attorney",
            "Real Estate Documents &amp; Forms",
            "Legal Documents &amp; Forms",
        ],
        footnote="Mobile Services available upon request &ndash; Travel fees will be applied."
    ))
    print(f"   Saved: {r}")

    # 4. Livescan page (post 30)
    print("4. Livescan page (post 30)...")
    r = save_elementor(30, service_page(
        "fingerprint",
        "Fast &amp; Confidential",
        "Livescan Fingerprints",
        "Electronic fingerprint scanning for background checks and licensing requirements &mdash; fast, accurate, and submitted directly to the requesting agency.",
        [
            "Livescan Background Checks",
            "FD-258 Card",
        ]
    ))
    print(f"   Saved: {r}")

    # 5. Clear caches
    print("5. Clearing caches...")
    clear_cache()
    print("   Done.")
    print("\n=== BUILD COMPLETE ===")


if __name__ == "__main__":
    build()
