#!/usr/bin/env python3
"""Build C&R Tax Services WordPress site with Elementor + XPRO."""
import requests, json, random, string

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
WP_URL  = "https://wordpress-1254753-6532124.cloudwaysapps.com"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

LOGO_ID  = 11
LOGO_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-content/uploads/2026/07/crts-logo.jpg"

# Colors
NAVY        = "#1B2A5E"
ROYAL_BLUE  = "#0A4A93"
GROWTH_RED  = "#E23A28"
RED_HOVER   = "#C22E1F"
ICE_BLUE    = "#EAF0F8"
OFF_WHITE   = "#F7F8FA"
SLATE       = "#5A6B8C"
MIDNIGHT    = "#121D42"
WHITE       = "#FFFFFF"

session_id = None

def get_session():
    global session_id
    if session_id:
        return session_id
    try:
        with open("/tmp/mcp_session.txt") as f:
            session_id = f.read().strip()
        return session_id
    except:
        pass
    return init_session()

def init_session():
    global session_id
    r = requests.post(MCP_URL, auth=AUTH, json={
        "jsonrpc":"2.0","id":0,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"claude","version":"1.0"}}
    })
    session_id = r.headers.get("mcp-session-id")
    with open("/tmp/mcp_session.txt","w") as f:
        f.write(session_id)
    return session_id

def php(code):
    sess = get_session()
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
        if not data.get("success", True):
            print("PHP ERROR:", data.get("error_message",""))
        return data
    except Exception as e:
        print("Parse error:", e, r.text[:200])
        return {}

def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

# ─────────────────────────────────────────────
# ELEMENTOR HELPERS
# ─────────────────────────────────────────────

def container(settings, elements, is_inner=True):
    return {
        "id": uid(),
        "elType": "container",
        "isInner": is_inner,
        "settings": settings,
        "elements": elements,
        "widgetType": None,
    }

def section_container(settings, elements):
    """Top-level section container (full width wrapper)."""
    return container(settings, elements, is_inner=False)

def widget(widget_type, settings):
    return {
        "id": uid(),
        "elType": "widget",
        "isInner": False,
        "widgetType": widget_type,
        "settings": settings,
        "elements": [],
    }

def pad(top, right, bottom, left, unit="px"):
    return {"top": str(top), "right": str(right), "bottom": str(bottom),
            "left": str(left), "unit": unit, "isLinked": False}

def size(v, unit="px"):
    return {"size": v, "unit": unit}

def typography(family, weight, sz, unit="px"):
    return {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_weight": str(weight),
        "typography_font_size": size(sz, unit),
    }

# ─────────────────────────────────────────────
# HOME PAGE SECTIONS
# ─────────────────────────────────────────────

def hero_section():
    # Contact card (right column)
    contact_card = container(
        {
            "flex_direction": "column",
            "background_color": "rgba(255,255,255,0.08)",
            "border_radius": {"top":"16","right":"16","bottom":"16","left":"16","unit":"px","isLinked":True},
            "padding": pad(32, 32, 32, 32),
            "gap": {"size": 16, "unit": "px"},
            "border_border": "solid",
            "border_width": {"top":"1","right":"1","bottom":"1","left":"1","unit":"px","isLinked":True},
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
                     "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"},
                     "_id": uid()},
                    {"text": "(559) 962-7503",
                     "icon": {"library": "fa-solid", "value": "fas fa-phone"},
                     "link": {"url": "tel:5599627503"},
                     "_id": uid()},
                    {"text": "info@candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-envelope"},
                     "link": {"url": "mailto:info@candrtaxservices.com"},
                     "_id": uid()},
                    {"text": "www.candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-globe"},
                     "link": {"url": "https://www.candrtaxservices.com"},
                     "_id": uid()},
                ],
                "icon_color": ICE_BLUE,
                "text_color": OFF_WHITE,
                "space_between": size(14),
                "icon_size": size(16),
                "typography_typography": "custom",
                "typography_font_family": "Inter",
                "typography_font_size": size(15),
            }),
        ]
    )

    left_col = container(
        {
            "flex_direction": "column",
            "flex_grow": "1",
            "width": size(55, "%"),
            "gap": {"size": 0, "unit": "px"},
            "_inline_size": None,
        },
        [
            widget("heading", {
                "title": "Welcome to<br>C&amp;R Tax Services",
                "header_size": "h1",
                "align": "left",
                "title_color": WHITE,
                **typography("Poppins", 800, 52),
                "typography_line_height": size(1.15, "em"),
                "spacing": {"margin": {"bottom": "24", "unit": "px"}},
            }),
            widget("text-editor", {
                "editor": "<p style='color:#EAF0F8;font-size:18px;line-height:1.6;font-family:Inter,sans-serif;margin:0 0 32px;'>Fresno&rsquo;s trusted source for income tax preparation, notary &amp; loan signing, and Livescan fingerprinting — located near the Tower District.</p>",
            }),
            container(
                {"flex_direction": "row", "flex_wrap": "wrap", "gap": {"size": 14, "unit": "px"}},
                [
                    widget("button", {
                        "text": "&#128222; (559) 962-7503",
                        "link": {"url": "tel:5599627503", "is_external": False},
                        "button_type": "info",
                        "size": "lg",
                        "background_color": GROWTH_RED,
                        "button_text_color": WHITE,
                        "hover_background_color": RED_HOVER,
                        "border_radius": pad(50,50,50,50),
                        "typography_font_family": "Inter",
                        "typography_font_weight": "600",
                        "typography_font_size": size(16),
                    }),
                    widget("button", {
                        "text": "View Services",
                        "link": {"url": "#services", "is_external": False},
                        "size": "lg",
                        "background_color": "transparent",
                        "button_text_color": WHITE,
                        "hover_background_color": "rgba(255,255,255,0.1)",
                        "border_border": "solid",
                        "border_width": {"top":"2","right":"2","bottom":"2","left":"2","unit":"px","isLinked":True},
                        "border_color": "rgba(255,255,255,0.4)",
                        "border_radius": pad(50,50,50,50),
                        "typography_font_family": "Inter",
                        "typography_font_weight": "600",
                        "typography_font_size": size(16),
                    }),
                ]
            ),
        ]
    )

    inner = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "gap": {"size": 48, "unit": "px"},
            "align_items": "center",
        },
        [left_col, contact_card]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": NAVY,
            "padding": pad(96, 0, 96, 0),
            "_title": "Hero",
            "html_tag": "section",
            "_css_id": "home",
        },
        [inner]
    )


def services_section():
    def service_card(icon_class, title, items, note=None):
        list_items = [{"text": item, "icon": {"library": "fa-solid", "value": "fas fa-check"}, "_id": uid()} for item in items]
        elements = [
            widget("icon", {
                "selected_icon": {"library": "fa-solid", "value": icon_class},
                "icon_size": size(40),
                "primary_color": ROYAL_BLUE,
                "_margin": {"margin": {"bottom": "16", "unit": "px"}},
            }),
            widget("heading", {
                "title": title,
                "header_size": "h3",
                "title_color": MIDNIGHT,
                **typography("Poppins", 700, 22),
                "spacing": {"margin": {"bottom": "16", "unit": "px"}},
            }),
            widget("icon-list", {
                "icon_list": list_items,
                "icon_color": ROYAL_BLUE,
                "text_color": SLATE,
                "space_between": size(10),
                "icon_size": size(14),
                "typography_typography": "custom",
                "typography_font_family": "Inter",
                "typography_font_size": size(15),
            }),
        ]
        if note:
            elements.append(widget("text-editor", {
                "editor": f"<p style='font-family:Inter,sans-serif;font-size:14px;font-style:italic;color:{SLATE};margin:12px 0 0;padding:12px;background:{ICE_BLUE};border-radius:8px;'>&#9432; {note}</p>",
            }))
        return container(
            {
                "flex_direction": "column",
                "background_color": WHITE,
                "border_radius": {"top":"16","right":"16","bottom":"16","left":"16","unit":"px","isLinked":True},
                "padding": pad(32, 28, 32, 28),
                "box_shadow_box_shadow_type": "yes",
                "box_shadow_box_shadow": {
                    "horizontal":0,"vertical":4,"blur":16,"spread":0,
                    "color": "rgba(27,42,94,0.10)","position":"outset"
                },
                "border_border": "solid",
                "border_width": {"top":"1","right":"1","bottom":"1","left":"1","unit":"px","isLinked":True},
                "border_color": "#D7DEEA",
                "flex_grow": "1",
                "width": size(32, "%"),
            },
            elements
        )

    cards_row = container(
        {
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "gap": {"size": 28, "unit": "px"},
            "align_items": "stretch",
        },
        [
            service_card(
                "fas fa-calculator",
                "Income Tax",
                ["Individual","Small Business / Self Employed","Rental Properties",
                 "Corporations, Partnerships &amp; LLC’s","ITIN Applications",
                 "Amendments","Audit Services","Extensions",
                 "Prior Year Reviews","Multi State Returns"],
                "Virtual/online tax preparation available any day, all year!"
            ),
            service_card(
                "fas fa-stamp",
                "Notary Public &amp; Loan Signing Agent",
                ["Bank Documents","Travel Documents","Power of Attorney",
                 "Real Estate Documents &amp; Forms","Legal Documents &amp; Forms"],
                "Mobile services available upon request &mdash; travel fees apply."
            ),
            service_card(
                "fas fa-fingerprint",
                "Livescan Fingerprints",
                ["Livescan Background Checks","FD-258 Card"]
            ),
        ]
    )

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "gap": {"size": 48, "unit": "px"}},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {
                        "title": "Our Services",
                        "header_size": "h2",
                        "align": "center",
                        "title_color": MIDNIGHT,
                        **typography("Poppins", 700, 38),
                    }),
                    widget("text-editor", {
                        "editor": f"<p style='color:{SLATE};font-family:Inter,sans-serif;font-size:17px;text-align:center;margin:10px 0 0;'>Tax preparation, notary, and fingerprinting services for Fresno families and businesses.</p>",
                    }),
                ]
            ),
            cards_row,
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": OFF_WHITE,
            "padding": pad(96, 0, 96, 0),
            "_title": "Services",
            "_css_id": "services",
        },
        [inner]
    )


def hours_section():
    def hours_card(season_label, rows):
        row_widgets = []
        for day, time in rows:
            row_widgets.append(container(
                {
                    "flex_direction": "row",
                    "justify_content": "space-between",
                    "padding": pad(10, 16, 10, 16),
                    "border_border": "solid",
                    "border_width": {"top":"0","right":"0","bottom":"1","left":"0","unit":"px","isLinked":False},
                    "border_color": "#D7DEEA",
                },
                [
                    widget("text-editor", {
                        "editor": f"<span style='font-family:Inter;font-weight:600;color:{MIDNIGHT};font-size:15px;'>{day}</span>",
                    }),
                    widget("text-editor", {
                        "editor": f"<span style='font-family:Inter;color:{SLATE};font-size:15px;'>{time}</span>",
                    }),
                ]
            ))
        return container(
            {
                "flex_direction": "column",
                "background_color": WHITE,
                "border_radius": {"top":"16","right":"16","bottom":"16","left":"16","unit":"px","isLinked":True},
                "padding": pad(0, 0, 16, 0),
                "box_shadow_box_shadow_type": "yes",
                "box_shadow_box_shadow": {
                    "horizontal":0,"vertical":4,"blur":16,"spread":0,
                    "color":"rgba(27,42,94,0.10)","position":"outset"
                },
                "border_border": "solid",
                "border_width": {"top":"1","right":"1","bottom":"1","left":"1","unit":"px","isLinked":True},
                "border_color": "#D7DEEA",
                "width": size(48, "%"),
            },
            [
                container(
                    {"padding": pad(20, 16, 16, 16), "background_color": NAVY,
                     "border_radius": {"top":"16","right":"16","bottom":"0","left":"0","unit":"px","isLinked":False}},
                    [widget("heading", {
                        "title": season_label,
                        "header_size": "h4",
                        "title_color": WHITE,
                        **typography("Poppins", 700, 18),
                    })]
                ),
            ] + row_widgets
        )

    tax_hours = [
        ("Monday – Saturday", "9:00 am – 7:00 pm"),
        ("Sunday", "10:00 am – 6:00 pm"),
        ("After Hours", "By Appointment Only"),
    ]
    off_hours = [
        ("Monday – Friday", "10:00 am – 6:00 pm"),
        ("Saturday – Sunday", "By Appointment Only"),
        ("After Hours", "By Appointment Only"),
    ]

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "gap": {"size": 48, "unit": "px"}},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {
                        "title": "Office Hours",
                        "header_size": "h2",
                        "align": "center",
                        "title_color": MIDNIGHT,
                        **typography("Poppins", 700, 38),
                    }),
                    widget("text-editor", {
                        "editor": f"<p style='color:{SLATE};font-family:Inter;font-size:17px;text-align:center;margin:10px 0 0;'>Tax season: January &ndash; April. After tax season: May &ndash; December.</p>",
                    }),
                ]
            ),
            container(
                {"flex_direction": "row", "flex_wrap": "wrap", "gap": {"size": 28, "unit": "px"}, "align_items": "flex-start"},
                [
                    hours_card("Tax Season (Jan &ndash; Apr)", tax_hours),
                    hours_card("After Tax Season (May &ndash; Dec)", off_hours),
                ]
            ),
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": ICE_BLUE,
            "padding": pad(96, 0, 96, 0),
            "_title": "Hours",
            "_css_id": "hours",
        },
        [inner]
    )


def contact_section():
    contact_inner = container(
        {
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "gap": {"size": 32, "unit": "px"},
            "align_items": "stretch",
        },
        [
            container(
                {
                    "flex_direction": "column",
                    "background_color": WHITE,
                    "border_radius": {"top":"16","right":"16","bottom":"16","left":"16","unit":"px","isLinked":True},
                    "padding": pad(32, 32, 32, 32),
                    "flex_grow": "1",
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
                    "border_border": "solid",
                    "border_width": {"top":"1","right":"1","bottom":"1","left":"1","unit":"px","isLinked":True},
                    "border_color": "#D7DEEA",
                },
                [
                    widget("heading", {
                        "title": "Visit Us",
                        "header_size": "h3",
                        "title_color": NAVY,
                        **typography("Poppins", 700, 22),
                    }),
                    widget("icon-list", {
                        "icon_list": [
                            {"text": "1320 N. Van Ness Ave, Fresno CA 93702",
                             "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"}, "_id": uid()},
                            {"text": "Near Tower District",
                             "icon": {"library": "fa-solid", "value": "fas fa-info-circle"}, "_id": uid()},
                        ],
                        "icon_color": ROYAL_BLUE,
                        "text_color": MIDNIGHT,
                        "space_between": size(12),
                        "icon_size": size(16),
                        "typography_typography": "custom",
                        "typography_font_family": "Inter",
                        "typography_font_size": size(16),
                    }),
                ]
            ),
            container(
                {
                    "flex_direction": "column",
                    "background_color": WHITE,
                    "border_radius": {"top":"16","right":"16","bottom":"16","left":"16","unit":"px","isLinked":True},
                    "padding": pad(32, 32, 32, 32),
                    "flex_grow": "1",
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {"horizontal":0,"vertical":4,"blur":16,"spread":0,"color":"rgba(27,42,94,0.10)","position":"outset"},
                    "border_border": "solid",
                    "border_width": {"top":"1","right":"1","bottom":"1","left":"1","unit":"px","isLinked":True},
                    "border_color": "#D7DEEA",
                },
                [
                    widget("heading", {
                        "title": "Contact Us",
                        "header_size": "h3",
                        "title_color": NAVY,
                        **typography("Poppins", 700, 22),
                    }),
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
                        "icon_color": ROYAL_BLUE,
                        "text_color": MIDNIGHT,
                        "space_between": size(12),
                        "icon_size": size(16),
                        "typography_typography": "custom",
                        "typography_font_family": "Inter",
                        "typography_font_size": size(16),
                    }),
                    widget("button", {
                        "text": "Call Now: (559) 962-7503",
                        "link": {"url": "tel:5599627503", "is_external": False},
                        "size": "lg",
                        "background_color": GROWTH_RED,
                        "button_text_color": WHITE,
                        "hover_background_color": RED_HOVER,
                        "border_radius": pad(50,50,50,50),
                        "button_block_width": "no",
                        "typography_font_family": "Inter",
                        "typography_font_weight": "600",
                        "typography_font_size": size(16),
                        "_margin": {"margin": {"top":"20","unit":"px"}},
                    }),
                ]
            ),
        ]
    )

    inner = container(
        {"content_width": "boxed", "flex_direction": "column", "gap": {"size": 48, "unit": "px"}},
        [
            container(
                {"flex_direction": "column", "align_items": "center"},
                [
                    widget("heading", {
                        "title": "Get In Touch",
                        "header_size": "h2",
                        "align": "center",
                        "title_color": MIDNIGHT,
                        **typography("Poppins", 700, 38),
                    }),
                    widget("text-editor", {
                        "editor": f"<p style='color:{SLATE};font-family:Inter;font-size:17px;text-align:center;margin:10px 0 0;'>Stop by, call, or book a virtual appointment &mdash; we&rsquo;re here all year.</p>",
                    }),
                ]
            ),
            contact_inner,
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": WHITE,
            "padding": pad(96, 0, 96, 0),
            "_title": "Contact",
            "_css_id": "contact",
        },
        [inner]
    )


# ─────────────────────────────────────────────
# XPRO HEADER
# ─────────────────────────────────────────────

def xpro_header(menu_id):
    logo_widget = widget("xpro-site-logo", {
        "logo_type": "custom",
        "custom_logo": {"url": LOGO_URL, "id": LOGO_ID},
        "logo_size": size(160),
        "logo_gap": size(0),
    })

    nav_widget = widget("xpro-horizontal-menu", {
        "menu": str(menu_id),
        "menu_layout": "horizontal",
        "typography_typography": "custom",
        "typography_font_family": "Inter",
        "typography_font_size": size(15),
        "typography_font_weight": "500",
        "menu_color": WHITE,
        "menu_hover_color": ICE_BLUE,
        "menu_active_color": ICE_BLUE,
        "menu_background": "transparent",
        "menu_hover_background": "transparent",
        "submenu_background": NAVY,
        "submenu_color": WHITE,
        "submenu_hover_color": ICE_BLUE,
        "indicator_color": ICE_BLUE,
        "layout_gap": size(8),
    })

    phone_btn = widget("button", {
        "text": "(559) 962-7503",
        "link": {"url": "tel:5599627503", "is_external": False},
        "size": "md",
        "background_color": GROWTH_RED,
        "button_text_color": WHITE,
        "hover_background_color": RED_HOVER,
        "border_radius": pad(50,50,50,50),
        "typography_font_family": "Inter",
        "typography_font_weight": "600",
        "typography_font_size": size(15),
    })

    inner = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "nowrap",
            "align_items": "center",
            "justify_content": "space-between",
            "gap": {"size": 32, "unit": "px"},
        },
        [logo_widget, nav_widget, phone_btn]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": NAVY,
            "padding": pad(16, 0, 16, 0),
            "z_index": 999,
            "_title": "Header",
        },
        [inner]
    )


# ─────────────────────────────────────────────
# XPRO FOOTER
# ─────────────────────────────────────────────

def xpro_footer(menu_id):
    logo_col = container(
        {"flex_direction": "column", "flex_grow": "1", "width": size(30, "%"), "gap": {"size": 16, "unit": "px"}},
        [
            widget("xpro-site-logo", {
                "logo_type": "custom",
                "custom_logo": {"url": LOGO_URL, "id": LOGO_ID},
                "logo_size": size(140),
            }),
            widget("text-editor", {
                "editor": f"<p style='color:rgba(234,240,248,0.7);font-family:Inter;font-size:14px;line-height:1.6;margin:0;'>Fresno&rsquo;s trusted tax preparation, notary, and fingerprinting service. Located near the Tower District.</p>",
            }),
        ]
    )

    contact_col = container(
        {"flex_direction": "column", "flex_grow": "1", "width": size(30, "%"), "gap": {"size": 16, "unit": "px"}},
        [
            widget("heading", {
                "title": "Contact",
                "header_size": "h4",
                "title_color": WHITE,
                **typography("Poppins", 700, 18),
            }),
            widget("icon-list", {
                "icon_list": [
                    {"text": "1320 N. Van Ness Ave<br>Fresno CA 93702",
                     "icon": {"library": "fa-solid", "value": "fas fa-map-marker-alt"}, "_id": uid()},
                    {"text": "(559) 962-7503",
                     "icon": {"library": "fa-solid", "value": "fas fa-phone"},
                     "link": {"url": "tel:5599627503"}, "_id": uid()},
                    {"text": "info@candrtaxservices.com",
                     "icon": {"library": "fa-solid", "value": "fas fa-envelope"},
                     "link": {"url": "mailto:info@candrtaxservices.com"}, "_id": uid()},
                ],
                "icon_color": ICE_BLUE,
                "text_color": "rgba(234,240,248,0.85)",
                "space_between": size(12),
                "icon_size": size(14),
                "typography_typography": "custom",
                "typography_font_family": "Inter",
                "typography_font_size": size(14),
            }),
        ]
    )

    hours_col = container(
        {"flex_direction": "column", "flex_grow": "1", "width": size(30, "%"), "gap": {"size": 16, "unit": "px"}},
        [
            widget("heading", {
                "title": "Hours",
                "header_size": "h4",
                "title_color": WHITE,
                **typography("Poppins", 700, 18),
            }),
            widget("icon-list", {
                "icon_list": [
                    {"text": "<strong>Tax Season (Jan–Apr)</strong>",
                     "icon": {"library": "fa-solid", "value": "fas fa-clock"}, "_id": uid()},
                    {"text": "Mon–Sat: 9am–7pm",
                     "icon": {"library": "fa-regular", "value": "far fa-circle"}, "_id": uid()},
                    {"text": "Sun: 10am–6pm",
                     "icon": {"library": "fa-regular", "value": "far fa-circle"}, "_id": uid()},
                    {"text": "<strong>After Tax Season (May–Dec)</strong>",
                     "icon": {"library": "fa-solid", "value": "fas fa-clock"}, "_id": uid()},
                    {"text": "Mon–Fri: 10am–6pm",
                     "icon": {"library": "fa-regular", "value": "far fa-circle"}, "_id": uid()},
                    {"text": "Sat–Sun: By Appointment",
                     "icon": {"library": "fa-regular", "value": "far fa-circle"}, "_id": uid()},
                ],
                "icon_color": ICE_BLUE,
                "text_color": "rgba(234,240,248,0.85)",
                "space_between": size(10),
                "icon_size": size(12),
                "typography_typography": "custom",
                "typography_font_family": "Inter",
                "typography_font_size": size(14),
            }),
        ]
    )

    top_row = container(
        {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "gap": {"size": 40, "unit": "px"},
            "align_items": "flex-start",
            "padding": pad(64, 0, 48, 0),
        },
        [logo_col, contact_col, hours_col]
    )

    divider_row = container(
        {
            "content_width": "boxed",
            "border_border": "solid",
            "border_width": {"top":"1","right":"0","bottom":"0","left":"0","unit":"px","isLinked":False},
            "border_color": "rgba(255,255,255,0.15)",
            "padding": pad(24, 0, 24, 0),
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "align_items": "center",
            "justify_content": "space-between",
            "gap": {"size": 16, "unit": "px"},
        },
        [
            widget("text-editor", {
                "editor": f"<p style='color:rgba(234,240,248,0.6);font-family:Inter;font-size:13px;margin:0;'>&copy; {2026} C&amp;R Tax Services. All rights reserved.</p>",
            }),
            widget("text-editor", {
                "editor": f"<p style='color:rgba(234,240,248,0.6);font-family:Inter;font-size:13px;margin:0;'>1320 N. Van Ness Ave, Fresno CA 93702</p>",
            }),
        ]
    )

    return section_container(
        {
            "content_width": "full",
            "background_color": MIDNIGHT,
            "padding": pad(0, 0, 0, 0),
            "_title": "Footer",
        },
        [top_row, divider_row]
    )


# ─────────────────────────────────────────────
# MAIN BUILDER
# ─────────────────────────────────────────────

def build():
    init_session()
    print("=== Building C&R Tax Services WordPress site ===\n")

    # 1. Create navigation menu first (needed for header)
    print("1. Creating navigation menu...")
    menu_result = php("""
$menu_name = 'C&R Tax Main Menu';
$existing = wp_get_nav_menu_object($menu_name);
if($existing) {
    $menu_id = $existing->term_id;
    echo "Existing menu: $menu_id\\n";
} else {
    $menu_id = wp_create_nav_menu($menu_name);
    echo "Created menu: $menu_id\\n";
}
return ['menu_id' => $menu_id];
""")
    menu_id = menu_result.get("return_value", {}).get("menu_id", 0)
    print(f"   Menu ID: {menu_id}")

    # 2. Create Home page
    print("\n2. Creating Home page...")
    page_result = php("""
$existing = get_page_by_path('home', OBJECT, 'page');
if($existing) { wp_delete_post($existing->ID, true); }
$page_id = wp_insert_post([
    'post_title'   => 'Home',
    'post_name'    => 'home',
    'post_status'  => 'publish',
    'post_type'    => 'page',
    'post_content' => '',
]);
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_template_type', 'wp-page');
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');
return ['page_id' => $page_id];
""")
    page_id = page_result.get("return_value", {}).get("page_id", 0)
    print(f"   Page ID: {page_id}")

    # Build home page Elementor data
    home_data = [
        hero_section(),
        services_section(),
        hours_section(),
        contact_section(),
    ]
    home_json = json.dumps(home_data)

    print(f"   Saving Elementor data...")
    save2 = php_with_data(page_id, home_json)
    print(f"   Home page saved: {save2}")

    # 3. Create XPRO Header template
    print("\n3. Creating XPRO Header template...")
    header_result = php("""
$existing = get_posts(['post_type'=>'xpro-themer','meta_key'=>'xpro_theme_builder_template_type',
    'meta_value'=>'type_header','posts_per_page'=>1]);
if($existing) wp_delete_post($existing[0]->ID, true);
$post_id = wp_insert_post([
    'post_title'  => 'C&R Tax - Main Header',
    'post_status' => 'publish',
    'post_type'   => 'xpro-themer',
    'post_author' => 1,
]);
update_post_meta($post_id, 'xpro_theme_builder_template_type', 'type_header');
update_post_meta($post_id, 'xpro_theme_builder_sticky', '');
update_post_meta($post_id, '_elementor_edit_mode', 'builder');
update_post_meta($post_id, '_elementor_template_type', 'xpro-themer');
$location = ['rule' => ['entire_site'], 'specific' => ['']];
$exclude  = ['rule' => [''], 'specific' => ['']];
update_post_meta($post_id, 'xpro_theme_builder_target_include_locations', $location);
update_post_meta($post_id, 'xpro_theme_builder_target_exclude_locations', $exclude);
update_post_meta($post_id, 'xpro_theme_builder_target_user_roles', ['']);
return ['header_id' => $post_id];
""")
    header_id = header_result.get("return_value", {}).get("header_id", 0)
    print(f"   Header template ID: {header_id}")

    header_data = [xpro_header(menu_id)]
    header_json = json.dumps(header_data)
    save_h = php_with_data(header_id, header_json)
    print(f"   Header saved: {save_h}")

    # 4. Create XPRO Footer template
    print("\n4. Creating XPRO Footer template...")
    footer_result = php("""
$existing = get_posts(['post_type'=>'xpro-themer','meta_key'=>'xpro_theme_builder_template_type',
    'meta_value'=>'type_footer','posts_per_page'=>1]);
if($existing) wp_delete_post($existing[0]->ID, true);
$post_id = wp_insert_post([
    'post_title'  => 'C&R Tax - Main Footer',
    'post_status' => 'publish',
    'post_type'   => 'xpro-themer',
    'post_author' => 1,
]);
update_post_meta($post_id, 'xpro_theme_builder_template_type', 'type_footer');
update_post_meta($post_id, '_elementor_edit_mode', 'builder');
update_post_meta($post_id, '_elementor_template_type', 'xpro-themer');
$location = ['rule' => ['entire_site'], 'specific' => ['']];
$exclude  = ['rule' => [''], 'specific' => ['']];
update_post_meta($post_id, 'xpro_theme_builder_target_include_locations', $location);
update_post_meta($post_id, 'xpro_theme_builder_target_exclude_locations', $exclude);
update_post_meta($post_id, 'xpro_theme_builder_target_user_roles', ['']);
return ['footer_id' => $post_id];
""")
    footer_id = footer_result.get("return_value", {}).get("footer_id", 0)
    print(f"   Footer template ID: {footer_id}")

    footer_data = [xpro_footer(menu_id)]
    footer_json = json.dumps(footer_data)
    save_f = php_with_data(footer_id, footer_json)
    print(f"   Footer saved: {save_f}")

    # 5. Add menu items and set homepage
    print("\n5. Setting up navigation menu and homepage...")
    final = php(f"""
$menu_id = {menu_id};
$page_id = {page_id};

// Clear existing items
$items = wp_get_nav_menu_items($menu_id);
if($items) foreach($items as $item) wp_delete_post($item->ID, true);

// Add menu items (anchors on home page)
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Home','menu-item-url'=>home_url('/'),
    'menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Services','menu-item-url'=>home_url('/#services'),
    'menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Hours','menu-item-url'=>home_url('/#hours'),
    'menu-item-status'=>'publish','menu-item-type'=>'custom']);
wp_update_nav_menu_item($menu_id, 0, ['menu-item-title'=>'Contact','menu-item-url'=>home_url('/#contact'),
    'menu-item-status'=>'publish','menu-item-type'=>'custom']);

// Set homepage
update_option('show_on_front', 'page');
update_option('page_on_front', $page_id);

// Register menu to a location (create custom location if needed)
$locations = get_theme_mod('nav_menu_locations', []);
$locations['primary'] = $menu_id;
set_theme_mod('nav_menu_locations', $locations);

return ['menu_items_added' => 4, 'homepage_set' => $page_id];
""")
    print(f"   Final setup: {final.get('return_value', {})}")

    print(f"""
=== BUILD COMPLETE ===
Home Page ID: {page_id}
Header Template ID: {header_id}
Footer Template ID: {footer_id}
Menu ID: {menu_id}
Site URL: https://wordpress-1254753-6532124.cloudwaysapps.com/
""")


def php_with_data(post_id, elementor_json):
    """Save Elementor data to a post using write-file + PHP require pattern to avoid escaping issues."""
    sess = get_session()
    # Write JSON to a temp file on server
    write_r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/write-file",
                               "parameters":{
                                   "path": f"wp-content/novamira-sandbox/el_data_{post_id}.json",
                                   "content": elementor_json
                               }}}
    })
    wr = write_r.json()
    wr_data = json.loads(wr["result"]["content"][0]["text"])
    if not wr_data.get("success"):
        print("Write error:", wr_data)
        return False

    # Now PHP reads it and saves to post meta
    code = f"""
\\$json = file_get_contents(WP_CONTENT_DIR . '/novamira-sandbox/el_data_{post_id}.json');
\\$data = json_decode(\\$json, true);
update_post_meta({post_id}, '_elementor_data', wp_slash(json_encode(\\$data)));
update_post_meta({post_id}, '_elementor_page_settings', []);
// Clean up
@unlink(WP_CONTENT_DIR . '/novamira-sandbox/el_data_{post_id}.json');
return ['saved' => true, 'elements' => count(\\$data)];
"""
    r = requests.post(MCP_URL, auth=AUTH, headers={"Mcp-Session-Id": sess}, json={
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"mcp-adapter-execute-ability",
                  "arguments":{"ability_name":"novamira/execute-php",
                               "parameters":{"code": code.replace("\\$","$")}}}
    })
    d = r.json()
    result = json.loads(d["result"]["content"][0]["text"])
    data = result.get("data", result)
    return data.get("return_value", data)


if __name__ == "__main__":
    build()
