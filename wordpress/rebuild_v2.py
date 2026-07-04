#!/usr/bin/env python3
"""
Full rebuild of C&R Tax Services WordPress site to match updated design.
Changes vs v1:
 - New logo (CRTS_logo_2.jpg)
 - Header: white bg, slate nav links, updated nav items
 - Footer: navy bg, simplified 2-col layout, text name (no logo img)
 - Home page: services section gets "View details →" links
 - 3 new service pages: Income Tax, Notary, Livescan
 - Updated nav menu: Home, Income Tax, Notary, Livescan, Contact
"""
import requests, json, random, string, base64, os, sys
sys.path.insert(0, '/tmp')
from mcp_php import execute_php, init_session as _init_session

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
WP_URL  = "https://wordpress-1254753-6532124.cloudwaysapps.com"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")
WP_AUTH = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

# Brand colors
NAVY        = "#1B2A5E"
ROYAL_BLUE  = "#0A4A93"
GROWTH_RED  = "#E23A28"
RED_HOVER   = "#C22E1F"
ICE_BLUE    = "#EAF0F8"
OFF_WHITE   = "#F7F8FA"
SLATE       = "#5A6B8C"
MIDNIGHT    = "#121D42"
WHITE       = "#FFFFFF"
BORDER      = "#D7DEEA"

session_id = None

def get_session():
    global session_id
    if session_id:
        return session_id
    session_id = _init_session()
    return session_id

def php(code, session=None):
    sess = session or get_session()
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/execute-php",
                               "parameters":{"code": code}}}
    })
    try:
        d = r.json()
        content = d["result"]["content"][0]["text"]
        parsed = json.loads(content)
        data = parsed.get("data", parsed)
        return data
    except Exception as e:
        print("Parse error:", e, r.text[:300])
        return {}

def write_file(path, content):
    sess = get_session()
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/write-file",
                               "parameters":{"path": path, "content": content}}}
    })
    d = r.json()
    result = json.loads(d["result"]["content"][0]["text"])
    return result.get("data", result)

def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

# ─── ELEMENTOR PRIMITIVES ───────────────────────────────────────────────────

def pad(top, right, bottom, left, unit="px"):
    return {"top": str(top), "right": str(right), "bottom": str(bottom),
            "left": str(left), "unit": unit, "isLinked": False}

def size(v, unit="px"):
    return {"size": v, "unit": unit}

def gap(v, unit="px"):
    """Elementor flex_gap control (type: gaps)."""
    return {"column": v, "row": v, "unit": unit, "isLinked": True}

def typography(family, weight, sz, unit="px"):
    return {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_weight": str(weight),
        "typography_font_size": size(sz, unit),
    }

def container(settings, elements, is_inner=True):
    """Build Elementor container element with auto-fixed control names."""
    renames = {
        "justify_content": "flex_justify_content",
        "align_items":     "flex_align_items",
        "align_content":   "flex_align_content",
    }
    fixed = {}
    for k, v in settings.items():
        k2 = renames.get(k, k)
        # Convert legacy gap:{size,unit} → flex_gap gaps format
        if k == "gap" and isinstance(v, dict) and "size" in v:
            fixed["flex_gap"] = gap(v["size"], v.get("unit", "px"))
            continue
        # Auto-add background_background:classic when background_color is set alone
        if k == "background_color" and "background_background" not in settings:
            fixed["background_background"] = "classic"
        fixed[k2] = v
    return {
        "id": uid(),
        "elType": "container",
        "isInner": is_inner,
        "settings": fixed,
        "elements": elements,
    }

def section_container(settings, elements):
    return container(settings, elements, is_inner=False)

def widget(wtype, settings):
    s = dict(settings)
    if wtype == "button":
        if "background_color" in s and "background_background" not in s:
            s["background_background"] = "classic"
        if "hover_background_color" in s:
            s["button_background_hover_color"] = s.pop("hover_background_color")
            s["button_background_hover_background"] = "classic"
    return {
        "id": uid(),
        "elType": "widget",
        "isInner": False,
        "widgetType": wtype,
        "settings": s,
        "elements": [],
    }

def save_elementor(post_id, elementor_data):
    """Write JSON to sandbox file then PHP saves it as post meta."""
    el_json = json.dumps(elementor_data)
    path = f"wp-content/novamira-sandbox/el_{post_id}.json"
    wr = write_file(path, el_json)
    # Novamira write-file returns bytes_written/created, not success key
    if not wr.get("bytes_written") and not wr.get("created"):
        print(f"  Write error for post {post_id}:", wr)
        return False
    result = php(f"""
$j = file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
$d = json_decode($j, true);
update_post_meta({post_id}, '_elementor_data', wp_slash(json_encode($d)));
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_{post_id}.json');
return ['saved'=>true,'elements'=>count($d)];
""")
    return result.get("return_value", result)

# ─── SHARED BUTTON HELPERS ──────────────────────────────────────────────────

def red_btn(text, url, size_="lg"):
    return widget("button", {
        "text": text,
        "link": {"url": url, "is_external": False},
        "size": size_,
        "background_color": GROWTH_RED,
        "button_text_color": OFF_WHITE,
        "hover_background_color": RED_HOVER,
        "border_radius": pad(50,50,50,50),
        **typography("Inter", 600, 16 if size_=="lg" else 15),
    })

def outline_btn(text, url, size_="lg"):
    return widget("button", {
        "text": text,
        "link": {"url": url, "is_external": False},
        "size": size_,
        "background_color": "transparent",
        "background_background": "classic",
        "button_text_color": WHITE,
        "hover_background_color": "rgba(255,255,255,0.1)",
        "border_border": "solid",
        "border_width": pad(2,2,2,2),
        "border_color": "rgba(255,255,255,0.4)",
        "border_radius": pad(50,50,50,50),
        **typography("Inter", 600, 16),
    })

# ─── HEADER (WHITE bg, updated nav) ─────────────────────────────────────────

def xpro_header(menu_id, logo_id, logo_url):
    logo = widget("xpro-site-logo", {
        "logo_type": "custom",
        "custom_logo": {"url": logo_url, "id": logo_id},
        "logo_size": size(160),
    })

    nav = widget("xpro-horizontal-menu", {
        "menu": str(menu_id),
        "menu_layout": "horizontal",
        "menu_color": SLATE,
        "menu_hover_color": NAVY,
        "menu_active_color": NAVY,
        "menu_background": "transparent",
        "menu_hover_background": "transparent",
        "submenu_background": WHITE,
        "submenu_color": MIDNIGHT,
        "submenu_hover_color": NAVY,
        "layout_gap": size(32),
        **typography("Inter", 500, 15),
    })

    phone_btn = red_btn("Call (559) 962-7503", "tel:5599627503", "sm")

    inner = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "nowrap",
            "align_items": "center",
            "justify_content": "space-between",
            "flex_gap": gap(32),
        },
        [logo, nav, phone_btn]
    )

    return section_container(
        {
            "content_width": "full",
            "background_background": "classic",
            "background_color": WHITE,
            "border_border": "solid",
            "border_width": pad(0,0,1,0),
            "border_color": BORDER,
            "padding": pad(16, 0, 16, 0),
            "_title": "Header",
        },
        [inner]
    )


# ─── FOOTER (NAVY bg, simplified 2-col) ─────────────────────────────────────

def xpro_footer():
    left_col = container(
        {
            "flex_direction": "column",
            "flex_gap": gap(10),
        },
        [
            widget("heading", {
                "title": "C&amp;R Tax Services",
                "header_size": "h4",
                "title_color": WHITE,
                **typography("Poppins", 700, 20),
            }),
            widget("icon-list", {
                "icon_list": [
                    {"text": "1320 N. Van Ness Ave, Fresno CA 93702",
                     "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"},
                     "_id": uid()},
                ],
                "icon_color": OFF_WHITE,
                "text_color": OFF_WHITE,
                "space_between": size(0),
                "icon_size": size(16),
                **typography("Inter", 400, 15),
            }),
        ]
    )

    right_col = container(
        {
            "flex_direction": "column",
            "flex_gap": gap(10),
        },
        [
            widget("icon-list", {
                "icon_list": [
                    {"text": "(559) 962-7503",
                     "icon": {"library": "fa-solid", "value": "fas fa-phone"},
                     "link": {"url": "tel:5599627503"}, "_id": uid()},
                    {"text": "info@candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-envelope"},
                     "link": {"url": "mailto:info@candrtaxservices.com"}, "_id": uid()},
                    {"text": "www.candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-globe"},
                     "link": {"url": "https://www.candrtaxservices.com"}, "_id": uid()},
                ],
                "icon_color": OFF_WHITE,
                "text_color": OFF_WHITE,
                "space_between": size(10),
                "icon_size": size(16),
                **typography("Inter", 400, 15),
            }),
        ]
    )

    main_row = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "align_items": "flex-start",
            "justify_content": "space-between",
            "flex_gap": gap(40),
            "padding": pad(64, 0, 40, 0),
        },
        [left_col, right_col]
    )

    copyright_row = container(
        {
            "content_width": "boxed",
            "border_border": "solid",
            "border_width": pad(1,0,0,0),
            "border_color": "rgba(247,248,250,0.15)",
            "padding": pad(24, 0, 24, 0),
        },
        [
            widget("text-editor", {
                "editor": f"<p style='color:rgba(234,240,248,0.7);font-family:Inter,sans-serif;font-size:13px;margin:0;'>&copy; 2026 C&amp;R Tax Services. All rights reserved.</p>",
            }),
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_background": "classic",
            "background_color": NAVY,
            "padding": pad(0,0,0,0),
            "_title": "Footer",
        },
        [main_row, copyright_row]
    )


# ─── HOME PAGE ──────────────────────────────────────────────────────────────

def home_hero():
    contact_card = container(
        {
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "rgba(255,255,255,0.08)",
            "border_radius": pad(16,16,16,16),
            "padding": pad(32,32,32,32),
            "flex_gap": gap(16),
            "border_border": "solid",
            "border_width": pad(1,1,1,1),
            "border_color": "rgba(255,255,255,0.15)",
        },
        [
            widget("heading", {
                "title": "Find Us",
                "header_size": "h3",
                "title_color": WHITE,
                **typography("Poppins", 700, 20),
            }),
            widget("icon-list", {
                "icon_list": [
                    {"text": "1320 N. Van Ness Ave, Fresno CA 93702<br>Near Tower District",
                     "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"}, "_id": uid()},
                    {"text": "(559) 962-7503",
                     "icon": {"library": "fa-solid", "value": "fas fa-phone"},
                     "link": {"url": "tel:5599627503"}, "_id": uid()},
                    {"text": "info@candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-envelope"},
                     "link": {"url": "mailto:info@candrtaxservices.com"}, "_id": uid()},
                    {"text": "www.candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-globe"},
                     "link": {"url": "https://www.candrtaxservices.com"}, "_id": uid()},
                ],
                "icon_color": ICE_BLUE,
                "text_color": OFF_WHITE,
                "space_between": size(14),
                "icon_size": size(16),
            }),
        ]
    )

    left_col = container(
        {
            "flex_direction": "column",
            "flex_gap": gap(0),
        },
        [
            widget("text-editor", {
                "editor": f'<span style="background:{GROWTH_RED};color:{OFF_WHITE};font-family:Inter,sans-serif;font-weight:600;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;padding:6px 14px;border-radius:999px;display:inline-block;">Tax Season Hours In Effect</span>',
            }),
            widget("heading", {
                "title": "Welcome to<br>C&amp;R Tax Services",
                "header_size": "h1",
                "align": "left",
                "title_color": WHITE,
                **typography("Poppins", 800, 52),
                "typography_line_height": size(1.15, "em"),
            }),
            widget("text-editor", {
                "editor": f"<p style='color:{ICE_BLUE};font-family:Inter,sans-serif;font-size:18px;line-height:1.6;margin:0 0 32px;'>Fresno&rsquo;s trusted source for income tax preparation, notary &amp; loan signing, and Livescan fingerprinting &mdash; located near the Tower District.</p>",
            }),
            container(
                {"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(14)},
                [
                    red_btn("&#128222; (559) 962-7503", "tel:5599627503"),
                    outline_btn("View Services", "#services"),
                ]
            ),
        ]
    )

    inner = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "flex_gap": gap(48),
            "align_items": "center",
        },
        [left_col, contact_card]
    )

    return section_container(
        {
            "content_width": "full",
            "background_background": "classic",
            "background_color": NAVY,
            "padding": pad(96, 0, 96, 0),
            "_css_id": "home",
            "html_tag": "section",
        },
        [inner]
    )


def service_card(icon_class, title, items, note=None):
    list_items = [
        {"text": it, "icon": {"library": "fa-solid", "value": "fas fa-check"}, "_id": uid()}
        for it in items
    ]
    elements = [
        widget("icon", {
            "selected_icon": {"library": "fa-solid", "value": icon_class},
            "icon_size": size(40),
            "primary_color": ROYAL_BLUE,
        }),
        widget("heading", {
            "title": title,
            "header_size": "h3",
            "title_color": MIDNIGHT,
            **typography("Poppins", 700, 22),
        }),
        widget("icon-list", {
            "icon_list": list_items,
            "icon_color": ROYAL_BLUE,
            "text_color": SLATE,
            "space_between": size(10),
            "icon_size": size(14),
        }),
    ]
    if note:
        elements.append(widget("text-editor", {
            "editor": f"<p style='font-family:Inter,sans-serif;font-size:14px;font-style:italic;color:{SLATE};margin:12px 0 0;padding:12px;background:{ICE_BLUE};border-radius:8px;'>&#9432; {note}</p>",
        }))
    return container(
        {
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": WHITE,
            "border_radius": pad(16,16,16,16),
            "padding": pad(32, 28, 32, 28),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
            "border_border": "solid",
            "border_width": pad(1,1,1,1),
            "border_color": BORDER,
        },
        elements
    )


def home_services():
    cards_row = container(
        {
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "flex_gap": gap(28),
            "align_items": "stretch",
        },
        [
            service_card("fas fa-calculator", "Income Tax",
                ["Individual","Small Business / Self Employed","Rental Properties",
                 "Corporations, Partnerships &amp; LLC’s","ITIN Applications",
                 "Amendments","Audit Services","Extensions","Prior Year Reviews","Multi State Returns"],
                "Virtual/online tax preparation available any day, all year!"),
            service_card("fas fa-stamp", "Notary Public &amp; Loan Signing Agent",
                ["Bank Documents","Travel Documents","Power of Attorney",
                 "Real Estate Documents &amp; Forms","Legal Documents &amp; Forms"],
                "Mobile services available upon request — travel fees apply."),
            service_card("fas fa-fingerprint", "Livescan Fingerprints",
                ["Livescan Background Checks","FD-258 Card"]),
        ]
    )

    # "View details" link row
    def detail_link(label, url):
        return container(
            {"flex_direction": "column", "align_items": "center"},
            [widget("text-editor", {
                "editor": f'<p style="text-align:center;margin:0;"><a href="{url}" style="color:{ROYAL_BLUE};font-family:Inter,sans-serif;font-weight:600;font-size:15px;text-decoration:none;">{label} &rarr;</a></p>',
            })]
        )

    links_row = container(
        {
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "flex_gap": gap(28),
        },
        [
            detail_link("View Income Tax details", "/income-tax/"),
            detail_link("View Notary details", "/notary/"),
            detail_link("View Livescan details", "/livescan/"),
        ]
    )

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "flex_gap": gap(48)},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {
                        "title": "Services",
                        "header_size": "h2",
                        "align": "center",
                        "title_color": MIDNIGHT,
                        **typography("Poppins", 700, 38),
                    }),
                    widget("text-editor", {
                        "editor": f"<p style='color:{SLATE};font-family:Inter,sans-serif;font-size:17px;text-align:center;margin:10px 0 0;'>Three ways we help Fresno families and businesses stay on track.</p>",
                    }),
                ]
            ),
            cards_row,
            links_row,
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_background": "classic",
            "background_color": OFF_WHITE,
            "padding": pad(96, 0, 96, 0),
            "_css_id": "services",
        },
        [inner]
    )


def home_hours():
    def hours_card(label, rows):
        row_widgets = []
        for day, time in rows:
            row_widgets.append(container(
                {
                    "flex_direction": "row",
                    "justify_content": "space-between",
                    "padding": pad(10, 16, 10, 16),
                    "border_border": "solid",
                    "border_width": pad(0,0,1,0),
                    "border_color": BORDER,
                },
                [
                    widget("text-editor", {"editor": f"<span style='font-family:Inter;font-weight:600;color:{MIDNIGHT};font-size:15px;'>{day}</span>"}),
                    widget("text-editor", {"editor": f"<span style='font-family:Inter;color:{SLATE};font-size:15px;'>{time}</span>"}),
                ]
            ))
        return container(
            {
                "flex_direction": "column",
                "background_background": "classic",
                "background_color": WHITE,
                "border_radius": pad(16,16,16,16),
                "padding": pad(0, 0, 16, 0),
                "box_shadow_box_shadow_type": "yes",
                "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
                "border_border": "solid",
                "border_width": pad(1,1,1,1),
                "border_color": BORDER,
            },
            [container(
                {"padding": pad(20, 16, 16, 16), "background_background": "classic", "background_color": NAVY,
                 "border_radius": {"top":"16","right":"16","bottom":"0","left":"0","unit":"px","isLinked":False}},
                [widget("heading", {"title": label, "header_size": "h4", "title_color": WHITE, **typography("Poppins", 700, 18)})]
            )] + row_widgets
        )

    tax_h = [("Monday – Saturday","9:00 am – 7:00 pm"),("Sunday","10:00 am – 6:00 pm"),("After Hours","By Appointment Only")]
    off_h = [("Monday – Friday","10:00 am – 6:00 pm"),("Saturday – Sunday","By Appointment Only"),("After Hours","By Appointment Only")]

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "flex_gap": gap(48)},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {"title": "Office Hours", "header_size": "h2", "align": "center", "title_color": MIDNIGHT, **typography("Poppins", 700, 38)}),
                    widget("text-editor", {"editor": f"<p style='color:{SLATE};font-family:Inter;font-size:17px;text-align:center;margin:10px 0 0;'>Tax season: January &ndash; April. After tax season: May &ndash; December.</p>"}),
                ]
            ),
            container(
                {"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(28), "align_items": "flex-start"},
                [hours_card("Tax Season (Jan &ndash; Apr)", tax_h), hours_card("After Tax Season (May &ndash; Dec)", off_h)]
            ),
        ]
    )
    return section_container(
        {"content_width": "full", "background_background": "classic", "background_color": ICE_BLUE, "padding": pad(96,0,96,0), "_css_id": "hours"},
        [inner]
    )


def home_contact():
    def contact_card_block(heading, items):
        return container(
            {
                "flex_direction": "column",
                "background_background": "classic",
                "background_color": WHITE,
                "border_radius": pad(16,16,16,16),
                "padding": pad(32, 32, 32, 32),
                "box_shadow_box_shadow_type": "yes",
                "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
                "border_border": "solid",
                "border_width": pad(1,1,1,1),
                "border_color": BORDER,
            },
            [
                widget("heading", {"title": heading, "header_size": "h3", "title_color": NAVY, **typography("Poppins", 700, 22)}),
                widget("icon-list", {"icon_list": items, "icon_color": ROYAL_BLUE, "text_color": MIDNIGHT, "space_between": size(12), "icon_size": size(16)}),
            ]
        )

    visit_items = [
        {"text": "1320 N. Van Ness Ave, Fresno CA 93702", "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"}, "_id": uid()},
        {"text": "Near Tower District", "icon": {"library": "fa-solid", "value": "fas fa-info-circle"}, "_id": uid()},
    ]
    contact_items = [
        {"text": "(559) 962-7503", "icon": {"library": "fa-solid", "value": "fas fa-phone"}, "link": {"url": "tel:5599627503"}, "_id": uid()},
        {"text": "info@candrtaxservices.com", "icon": {"library": "fa-solid", "value": "fas fa-envelope"}, "link": {"url": "mailto:info@candrtaxservices.com"}, "_id": uid()},
        {"text": "www.candrtaxservices.com", "icon": {"library": "fa-solid", "value": "fas fa-globe"}, "link": {"url": "https://www.candrtaxservices.com"}, "_id": uid()},
        {"text": "Call Now: (559) 962-7503", "icon": {"library": "fa-solid", "value": "fas fa-phone"}, "link": {"url": "tel:5599627503"}, "_id": uid()},
    ]

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "flex_gap": gap(48)},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {"title": "Get In Touch", "header_size": "h2", "align": "center", "title_color": MIDNIGHT, **typography("Poppins", 700, 38)}),
                    widget("text-editor", {"editor": f"<p style='color:{SLATE};font-family:Inter;font-size:17px;text-align:center;margin:10px 0 0;'>Stop by, call, or book a virtual appointment &mdash; we&rsquo;re here all year.</p>"}),
                ]
            ),
            container(
                {"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(32), "align_items": "stretch"},
                [
                    contact_card_block("Visit Us", visit_items),
                    container(
                        {
                            "flex_direction": "column",
                            "background_background": "classic",
                            "background_color": WHITE,
                            "border_radius": pad(16,16,16,16),
                            "padding": pad(32,32,32,32),
                            "box_shadow_box_shadow_type": "yes",
                            "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
                            "border_border": "solid",
                            "border_width": pad(1,1,1,1),
                            "border_color": BORDER,
                        },
                        [
                            widget("heading", {"title": "Contact Us", "header_size": "h3", "title_color": NAVY, **typography("Poppins", 700, 22)}),
                            widget("icon-list", {
                                "icon_list": [
                                    {"text": "(559) 962-7503", "icon": {"library": "fa-solid", "value": "fas fa-phone"}, "link": {"url": "tel:5599627503"}, "_id": uid()},
                                    {"text": "info@candrtaxservices.com", "icon": {"library": "fa-solid", "value": "fas fa-envelope"}, "link": {"url": "mailto:info@candrtaxservices.com"}, "_id": uid()},
                                    {"text": "www.candrtaxservices.com", "icon": {"library": "fa-solid", "value": "fas fa-globe"}, "link": {"url": "https://www.candrtaxservices.com"}, "_id": uid()},
                                ],
                                "icon_color": ROYAL_BLUE, "text_color": MIDNIGHT, "space_between": size(12), "icon_size": size(16),
                            }),
                            red_btn("Call Now: (559) 962-7503", "tel:5599627503"),
                        ]
                    ),
                ]
            ),
        ]
    )
    return section_container(
        {"content_width": "full", "background_background": "classic", "background_color": WHITE, "padding": pad(96,0,96,0), "_css_id": "contact"},
        [inner]
    )


# ─── SERVICE DETAIL PAGE SHELL ───────────────────────────────────────────────

def service_page_hero(icon_fa, eyebrow, title, intro):
    """Navy hero with icon box, badge, h1, intro."""
    icon_box = container(
        {
            "flex_direction": "row",
            "align_items": "center",
            "justify_content": "center",
            "background_background": "classic",
            "background_color": "rgba(247,248,250,0.12)",
            "border_radius": pad(10,10,10,10),
            "width": size(56),
            "min_height": size(56),
        },
        [widget("icon", {"selected_icon": {"library": "fa-solid", "value": icon_fa}, "icon_size": size(28), "primary_color": OFF_WHITE})]
    )

    badge_html = f'<span style="background:{GROWTH_RED};color:{OFF_WHITE};font-family:Inter,sans-serif;font-weight:600;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;padding:6px 14px;border-radius:999px;display:inline-block;margin-top:24px;">{eyebrow}</span>'

    inner = container(
        {
            "content_width": "boxed",
            "boxed_width": size(760),
            "flex_direction": "column",
            "flex_gap": gap(0),
        },
        [
            icon_box,
            widget("text-editor", {"editor": badge_html}),
            widget("heading", {
                "title": title,
                "header_size": "h1",
                "title_color": WHITE,
                **typography("Poppins", 800, 50),
                "typography_line_height": size(1.15, "em"),
            }),
            widget("text-editor", {
                "editor": f"<p style='font-family:Inter,sans-serif;font-size:20px;color:{ICE_BLUE};line-height:1.6;margin:16px 0 0;max-width:620px;'>{intro}</p>",
            }),
        ]
    )
    return section_container(
        {"content_width": "full", "background_background": "classic", "background_color": NAVY, "padding": pad(80,0,80,0)},
        [inner]
    )


def service_page_content(items, footnote=None):
    """White section with services checklist card + CTA."""
    list_items = [
        {"text": it, "icon": {"library": "fa-solid", "value": "fas fa-check"}, "_id": uid()}
        for it in items
    ]
    card_elements = [
        widget("icon-list", {
            "icon_list": list_items,
            "icon_color": ROYAL_BLUE,
            "text_color": MIDNIGHT,
            "space_between": size(20),
            "icon_size": size(16),
        }),
    ]
    if footnote:
        card_elements.append(widget("text-editor", {
            "editor": f"<p style='font-family:Inter,sans-serif;font-size:15px;font-style:italic;color:{SLATE};margin:32px 0 0;padding-top:24px;border-top:1px solid {BORDER};'>{footnote}</p>",
        }))

    services_card = container(
        {
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": WHITE,
            "border_border": "solid",
            "border_width": pad(1,1,1,1),
            "border_color": BORDER,
            "border_radius": pad(16,16,16,16),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal":0,"vertical":2,"blur":8,"spread":0,"color":"rgba(27,42,94,0.08)","position":"outset"},
            "padding": pad(40,40,40,40),
        },
        card_elements
    )

    cta_row = container(
        {"flex_direction": "column", "align_items": "center", "padding": pad(48,0,0,0)},
        [red_btn("&#128222; Call (559) 962-7503", "tel:5599627503")]
    )

    inner = container(
        {
            "content_width": "boxed",
            "boxed_width": size(760),
            "flex_direction": "column",
            "flex_gap": gap(0),
        },
        [services_card, cta_row]
    )
    return section_container(
        {"content_width": "full", "background_background": "classic", "background_color": OFF_WHITE, "padding": pad(80,0,80,0)},
        [inner]
    )


def build_service_page(icon_fa, eyebrow, title, intro, items, footnote=None):
    return [
        service_page_hero(icon_fa, eyebrow, title, intro),
        service_page_content(items, footnote),
    ]


# ─── MAIN BUILD ──────────────────────────────────────────────────────────────

def build():
    get_session()
    print("=== C&R Tax Services — Full Site Rebuild v2 ===\n")

    # 1. Upload new logo
    print("1. Uploading new logo (CRTS_logo_2.jpg)...")
    logo_path = "/tmp/design/uploads/CRTS_logo_2.jpg"
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
    logo_b64 = base64.b64encode(logo_bytes).decode()

    logo_result = php(f"""
$upload_dir = wp_upload_dir();
$filename = 'crts-logo-2.jpg';
$filepath = $upload_dir['path'] . '/' . $filename;
$data = base64_decode('{logo_b64}');
file_put_contents($filepath, $data);
$wp_filetype = wp_check_filetype($filename, null);
$attachment = [
    'guid'           => $upload_dir['url'] . '/' . $filename,
    'post_mime_type' => $wp_filetype['type'],
    'post_title'     => 'C&R Tax Services Logo 2',
    'post_content'   => '',
    'post_status'    => 'inherit',
];
$attach_id = wp_insert_attachment($attachment, $filepath);
require_once(ABSPATH . 'wp-admin/includes/image.php');
$attach_data = wp_generate_attachment_metadata($attach_id, $filepath);
wp_update_attachment_metadata($attach_id, $attach_data);
return ['logo_id' => $attach_id, 'logo_url' => $upload_dir['url'] . '/' . $filename];
""")
    rv = logo_result.get("return_value", {})
    logo_id = rv.get("logo_id", 11)
    logo_url = rv.get("logo_url", "")
    print(f"   Logo ID: {logo_id}, URL: {logo_url}")

    # 2. Get/create pages and menu
    print("\n2. Creating service pages + menu...")
    setup_result = php(f"""
// Create or get menu
$menu_name = 'C&R Tax Main Menu';
$existing_menu = wp_get_nav_menu_object($menu_name);
if ($existing_menu) {{
    $menu_id = $existing_menu->term_id;
}} else {{
    $menu_id = wp_create_nav_menu($menu_name);
}}

// Create service pages (delete old ones first)
function make_page($title, $slug) {{
    $old = get_page_by_path($slug, OBJECT, 'page');
    if ($old) wp_delete_post($old->ID, true);
    $id = wp_insert_post([
        'post_title'  => $title,
        'post_name'   => $slug,
        'post_status' => 'publish',
        'post_type'   => 'page',
        'post_content'=> '',
    ]);
    update_post_meta($id, '_elementor_edit_mode', 'builder');
    update_post_meta($id, '_elementor_template_type', 'wp-page');
    update_post_meta($id, '_wp_page_template', 'elementor_header_footer');
    return $id;
}}

$income_tax_id = make_page('Income Tax', 'income-tax');
$notary_id     = make_page('Notary', 'notary');
$livescan_id   = make_page('Livescan', 'livescan');

// Home page — ensure it exists
$home = get_page_by_path('home', OBJECT, 'page');
if (!$home) {{
    $home_id = wp_insert_post(['post_title'=>'Home','post_name'=>'home','post_status'=>'publish','post_type'=>'page','post_content'=>'']);
}} else {{
    $home_id = $home->ID;
}}
update_post_meta($home_id, '_elementor_edit_mode', 'builder');
update_post_meta($home_id, '_elementor_template_type', 'wp-page');
update_post_meta($home_id, '_wp_page_template', 'elementor_header_footer');
update_option('show_on_front', 'page');
update_option('page_on_front', $home_id);

return [
    'menu_id' => $menu_id,
    'home_id' => $home_id,
    'income_tax_id' => $income_tax_id,
    'notary_id' => $notary_id,
    'livescan_id' => $livescan_id,
];
""")
    ids = setup_result.get("return_value", {})
    menu_id      = ids.get("menu_id", 3)
    home_id      = ids.get("home_id", 12)
    income_id    = ids.get("income_tax_id", 0)
    notary_id    = ids.get("notary_id", 0)
    livescan_id  = ids.get("livescan_id", 0)
    print(f"   Menu: {menu_id}, Home: {home_id}, IncomeTax: {income_id}, Notary: {notary_id}, Livescan: {livescan_id}")

    # 3. Save header template
    print("\n3. Saving XPRO header (white bg)...")
    header_data = [xpro_header(menu_id, logo_id, logo_url)]
    r = save_elementor(13, header_data)
    print(f"   Header saved: {r}")

    # 4. Save footer template
    print("\n4. Saving XPRO footer (navy bg, simplified)...")
    footer_data = [xpro_footer()]
    r = save_elementor(14, footer_data)
    print(f"   Footer saved: {r}")

    # 5. Save home page
    print("\n5. Saving home page...")
    home_data = [home_hero(), home_services(), home_hours(), home_contact()]
    r = save_elementor(home_id, home_data)
    print(f"   Home page saved: {r}")

    # 6. Save Income Tax page
    print("\n6. Saving Income Tax page...")
    income_data = build_service_page(
        "fas fa-calculator",
        "Available Any Day and All Year!",
        "Income Tax",
        "Full-service preparation for individuals, small businesses, and every filing situation in between &mdash; plus virtual and online tax preparation, available any day, all year.",
        [
            "Individual","Small Business / Self Employed","Rental Properties",
            "Corporations, Partnerships, &amp; LLC’s","ITIN Applications",
            "Amendments","Audit Services","Extensions","Prior Year Reviews",
            "Multi State Returns",
            "Virtual/Online Tax Preparation – Available Any Day and All Year!",
        ]
    )
    r = save_elementor(income_id, income_data)
    print(f"   Income Tax saved: {r}")

    # 7. Save Notary page
    print("\n7. Saving Notary page...")
    notary_data = build_service_page(
        "fas fa-stamp",
        "Mobile Service Available",
        "Notary Public &amp; Loan Signing Agent",
        "Certified notarization and loan signing for the documents that matter most &mdash; in-office or on the road.",
        ["Bank Documents","Travel Documents","Power of Attorney",
         "Real Estate Documents &amp; Forms","Legal Documents &amp; Forms"],
        footnote="Mobile Services available upon request &ndash; Travel fees will be applied."
    )
    r = save_elementor(notary_id, notary_data)
    print(f"   Notary saved: {r}")

    # 8. Save Livescan page
    print("\n8. Saving Livescan page...")
    livescan_data = build_service_page(
        "fas fa-fingerprint",
        "Fast &amp; Confidential",
        "Livescan Fingerprints",
        "Electronic fingerprint scanning for background checks and licensing requirements &mdash; fast, accurate, and submitted directly to the requesting agency.",
        ["Livescan Background Checks","FD-258 Card"]
    )
    r = save_elementor(livescan_id, livescan_data)
    print(f"   Livescan saved: {r}")

    # 9. Update nav menu
    print("\n9. Updating navigation menu...")
    nav_result = php(f"""
$menu_id = {menu_id};
$home_url = home_url('/');

// Clear existing items
$items = wp_get_nav_menu_items($menu_id);
if ($items) foreach ($items as $item) wp_delete_post($item->ID, true);

// Add items
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Home','menu-item-url'=>$home_url,'menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Income Tax','menu-item-url'=>$home_url.'income-tax/','menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Notary','menu-item-url'=>$home_url.'notary/','menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Livescan','menu-item-url'=>$home_url.'livescan/','menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Contact','menu-item-url'=>$home_url.'#contact','menu-item-status'=>'publish','menu-item-type'=>'custom']);

$locs = get_theme_mod('nav_menu_locations', []);
$locs['primary'] = $menu_id;
set_theme_mod('nav_menu_locations', $locs);

return ['items' => 5];
""")
    print(f"   Nav updated: {nav_result.get('return_value',{})}")

    # 10. Clear all caches
    print("\n10. Clearing caches...")
    php("""
Elementor\Plugin::$instance->files_manager->clear_cache();
if (function_exists('wp_cache_flush')) wp_cache_flush();
echo "done";
""")
    print("   Done.")

    print(f"""
=== BUILD COMPLETE ===
Home:       {WP_URL}/          (ID {home_id})
Income Tax: {WP_URL}/income-tax/ (ID {income_id})
Notary:     {WP_URL}/notary/    (ID {notary_id})
Livescan:   {WP_URL}/livescan/  (ID {livescan_id})
Header template: ID 13
Footer template: ID 14
Logo ID: {logo_id}
""")


if __name__ == "__main__":
    build()
