#!/usr/bin/env python3
"""
C&R Tax Services — About & Contact pages rebuild
Matches v7 design (CR_Tax_Services_Design_System_5.zip)
Creates new WordPress pages if they don't exist, or updates existing ones.
"""
import json, random, string, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

NAVY       = "#1B2A5E"; ROYAL_BLUE = "#0A4A93"; RED   = "#E23A28"
ICE_BLUE   = "#EAF0F8"; OFF_WHITE  = "#F7F8FA"; SLATE = "#5A6B8C"
WHITE      = "#FFFFFF"; BORDER     = "#D7DEEA"; SURFACE_ALT = "#F7F8FA"
SURFACE_CARD = "#FFFFFF"
TEXT_BODY  = "#374151"; TEXT_HEAD  = "#111827"; TEXT_MUTED = "#6B7280"
SP = {1:4,2:8,3:12,4:16,5:20,6:24,8:32,10:40,12:48,16:64,20:80,24:96}
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

# ── Elementor widget / container helpers ─────────────────────────────────────
def uid(): return "".join(random.choices(string.ascii_lowercase+string.digits, k=7))

def wgt(wtype, settings, children=None):
    w = {"id": uid(), "elType": "widget", "widgetType": wtype,
         "settings": settings, "elements": []}
    if children: w["elements"] = children
    return w

def col(elements, settings=None):
    return {"id": uid(), "elType": "container", "isInner": True,
            "settings": settings or {}, "elements": elements}

def row(columns, settings=None):
    s = {"flex_direction": "row", "flex_wrap": "wrap", **(settings or {})}
    return {"id": uid(), "elType": "container", "isInner": False,
            "settings": s, "elements": columns}

def section(elements, bg=None, pad_top=SP[20], pad_bot=SP[20]):
    s = {"padding": {"top": str(pad_top), "bottom": str(pad_bot),
                     "left": "32", "right": "32", "unit": "px", "isLinked": False},
         "content_width": {"size": 780, "unit": "px"}}
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    return {"id": uid(), "elType": "section", "settings": s, "elements": elements}

def heading(text, tag="h2", size=T["3xl"], color=TEXT_HEAD, mb=20):
    return wgt("heading", {
        "title": text, "header_size": tag,
        "typography_typography": "custom",
        "typography_font_family": "Poppins",
        "typography_font_weight": "700",
        "typography_font_size": {"size": size, "unit": "px"},
        "title_color": color,
        "_margin": {"top":"0","right":"0","bottom":str(mb),"left":"0","unit":"px","isLinked":False},
    })

def text_editor(html):
    return wgt("text-editor", {"editor": html})

def spacer(h=32):
    return wgt("spacer", {"space": {"size": h, "unit": "px"}})

def divider():
    return wgt("divider", {"color": BORDER})

def cta_button(label, href, variant="primary"):
    if variant == "primary":
        bg, txt, border = RED, WHITE, RED
        bg_hover, txt_hover = "#C22E1F", WHITE
    else:
        bg, txt, border = "transparent", WHITE, WHITE
        bg_hover, txt_hover = WHITE, NAVY
    return wgt("button", {
        "text": label, "link": {"url": href},
        "typography_font_family": "Inter",
        "typography_font_weight": "600",
        "typography_font_size": {"size": 17, "unit": "px"},
        "button_text_color": txt,
        "background_color": bg,
        "border_border": "solid",
        "border_width": {"top":"2","right":"2","bottom":"2","left":"2","unit":"px","isLinked":True},
        "border_color": border,
        "border_radius": {"top":"8","right":"8","bottom":"8","left":"8","unit":"px","isLinked":True},
        "padding": {"top":"14","right":"28","bottom":"14","left":"28","unit":"px","isLinked":False},
        "button_hover_color": txt_hover,
        "button_background_hover_color": bg_hover,
    })

# ── Inline HTML helpers ───────────────────────────────────────────────────────

def icon_box_html(icon_fa, color=NAVY):
    return (
        f'<div style="width:40px;height:40px;border-radius:10px;background:{color};'
        f'display:flex;align-items:center;justify-content:center;margin-bottom:12px;">'
        f'<i class="fas fa-{icon_fa}" style="font-size:20px;color:{OFF_WHITE};"></i>'
        f'</div>'
    )

def diff_card_html(icon_fa, title, body, bg_icon=NAVY):
    return (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:10px;padding:24px;">'
        f'{icon_box_html(icon_fa, bg_icon)}'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
        f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
        f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{TEXT_BODY};'
        f'line-height:1.6;margin:0;">{body}</p>'
        f'</div>'
    )

def diff_grid_html(cards):
    cards_html = "".join(diff_card_html(*c) for c in cards)
    return text_editor(
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));'
        f'gap:24px;margin-top:32px;margin-bottom:32px;">{cards_html}</div>'
    )

def check_item_html(text, link=False):
    return (
        f'<li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;">'
        f'<div style="width:24px;height:24px;border-radius:999px;background:{SURFACE_ALT};'
        f'display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">'
        f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i>'
        f'</div>'
        f'<span style="font-family:Inter,sans-serif;font-size:17px;color:{TEXT_BODY};'
        f'line-height:1.5;">{text}</span>'
        f'</li>'
    )

def checklist_html(items):
    items_html = "".join(check_item_html(it) for it in items)
    return (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:40px;">'
        f'<ul style="list-style:none;margin:0;padding:0;">{items_html}</ul>'
        f'</div>'
    )

def trust_pills_html(items):
    pills = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 16px;'
        f'border-radius:999px;background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i>'
        f'{item}</span>'
        for item in items
    )
    return text_editor(f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:24px;margin-bottom:32px;">{pills}</div>')

def city_pills_html(cities):
    pills = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
        f'border-radius:999px;background:{SURFACE_ALT};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-map-marker-alt" style="font-size:14px;color:{ROYAL_BLUE};"></i>'
        f'{city}</span>'
        for city in cities
    )
    return text_editor(f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px;">{pills}</div>')

def contact_card_html():
    rows = [
        ("map-marker-alt", "1320 N. Van Ness Ave, Fresno CA 93702", "Near Tower District", None),
        ("phone", "(559) 962-7503", None, "tel:5599627503"),
        ("envelope", "info@candrtaxservices.com", None, "mailto:info@candrtaxservices.com"),
        ("globe", "www.candrtaxservices.com", None, "https://www.candrtaxservices.com"),
    ]
    rows_html = ""
    for icon_fa, label, sub, href in rows:
        label_html = (
            f'<a href="{href}" style="color:{ROYAL_BLUE};font-weight:600;'
            f'font-size:17px;text-decoration:none;">{label}</a>'
            if href else
            f'<div style="color:{TEXT_BODY};font-weight:600;font-size:17px;">{label}</div>'
        )
        sub_html = f'<div style="color:{TEXT_MUTED};font-size:15px;">{sub}</div>' if sub else ""
        rows_html += (
            f'<div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:20px;">'
            f'<div style="width:36px;height:36px;border-radius:10px;background:{SURFACE_ALT};'
            f'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<i class="fas fa-{icon_fa}" style="font-size:18px;color:{ROYAL_BLUE};"></i>'
            f'</div>'
            f'<div>{label_html}{sub_html}</div>'
            f'</div>'
        )
    return (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:32px;">'
        f'{rows_html}'
        f'</div>'
    )

def hours_card_html(season="tax"):
    if season == "tax":
        label, rng = "Tax Season", "January – April"
        rows = [("Monday – Saturday", "9am – 7pm"), ("Sunday", "10am – 6pm")]
    else:
        label, rng = "After Tax Season", "May – December"
        rows = [("Monday – Friday", "10am – 6pm"), ("Saturday – Sunday", "By Appointment Only")]
    badge_color = RED if season == "tax" else SLATE
    rows_html = "".join(
        f'<tr style="border-top:1px solid {BORDER};">'
        f'<td style="padding:10px 0;color:{TEXT_BODY};font-size:15px;font-weight:500;">{day}</td>'
        f'<td style="padding:10px 0;color:{TEXT_MUTED};font-size:15px;text-align:right;">{hrs}</td>'
        f'</tr>'
        for day, hrs in rows
    )
    return (
        f'<div style="background:{SURFACE_CARD};border:1px solid {BORDER};'
        f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:32px;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'flex-wrap:wrap;gap:8px;margin-bottom:16px;">'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:700;font-size:20px;'
        f'color:{TEXT_HEAD};margin:0;">{label}</h3>'
        f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;'
        f'background:{badge_color};color:{WHITE};font-family:Inter,sans-serif;'
        f'font-size:13px;font-weight:600;">{rng}</span>'
        f'</div>'
        f'<table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;">'
        f'<tbody>{rows_html}</tbody></table>'
        f'<p style="margin:12px 0 0;font-size:13px;color:{TEXT_MUTED};font-style:italic;">'
        f'After Hours — By Appointment Only</p>'
        f'</div>'
    )

def p_html(text, last=False):
    mb = "0" if last else "16px"
    return (
        f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
        f'color:{TEXT_BODY};margin:0 0 {mb};">{text}</p>'
    )

def hero_icon_html(icon_fa):
    return (
        f'<div style="width:56px;height:56px;border-radius:10px;'
        f'background:rgba(247,248,250,0.12);display:flex;align-items:center;'
        f'justify-content:center;margin-bottom:24px;">'
        f'<i class="fas fa-{icon_fa}" style="font-size:28px;color:{OFF_WHITE};"></i>'
        f'</div>'
    )

# ── Page builder ─────────────────────────────────────────────────────────────

def build_about():
    VALUES = [
        ("tag", "Honesty",
         "Upfront, transparent pricing — you’ll know exactly what your Fresno tax preparation will cost before we ever file, with no surprise tiers or hidden percentages."),
        ("shield-alt", "Accuracy",
         "We stand behind every return we prepare. If we make an error, we make it right — covering the adjustment costs and amending your return at no charge."),
        ("users", "Accessibility",
         "We explain your return in plain language, and offer both in-person and secure virtual tax preparation — so getting your taxes done right fits into your life."),
    ]
    CREDENTIALS = [
        "Notary public services &amp; loan signing support",
        "Live Scan fingerprinting",
        "[CTEC registration]",
        "[IRS PTIN]",
        "[Certified Acceptance Agent status for ITIN applications]",
        "[Commissioned notary / DOJ-certified Live Scan operator]",
    ]
    TRUST_POINTS = [
        "Upfront, transparent pricing",
        "100% accuracy guarantee",
        "Bilingual-friendly service",
        "ITIN application support",
        "Secure virtual filing",
    ]
    CITIES = ["Fresno", "Clovis", "Selma", "Reedley", "Sanger", "Madera"]

    secs = []

    # Hero (navy)
    hero_content = (
        hero_icon_html("heart") +
        f'<span style="display:inline-block;background:{RED};color:{WHITE};'
        f'font-family:Inter,sans-serif;font-size:13px;font-weight:700;'
        f'padding:4px 14px;border-radius:999px;margin-bottom:18px;">'
        f'Local &amp; Family-Focused</span><br>'
        f'<h1 style="font-family:Poppins,sans-serif;font-weight:800;font-size:50px;'
        f'line-height:1.15;color:{WHITE};margin:0 0 16px;max-width:680px;">'
        f'Why We Started C&amp;R Tax Services</h1>'
        f'<p style="font-family:Inter,sans-serif;font-size:20px;color:{ICE_BLUE};'
        f'line-height:1.6;margin:0;max-width:620px;">'
        f'Tax season shouldn’t feel like a guessing game — but for too many '
        f'Central Valley families, that’s exactly what it’s become.</p>'
    )
    secs.append(section([text_editor(hero_content)], bg=NAVY, pad_top=SP[20], pad_bot=SP[20]))

    # Our story (white)
    story_left = (
        p_html("Tax season shouldn’t feel like a guessing game. But for too many families and small business owners here in the Central Valley, that’s exactly what it’s become — confusing software, pop-up franchise offices that disappear on April 16th, and preparers who rush you out the door without ever explaining what they filed on your behalf. C&amp;R Tax Services was founded to be the opposite of all that.") +
        p_html("We started this firm right here in Fresno because we believe our neighbors deserve a tax preparer who actually knows them — someone who picks up the phone in July when an IRS letter shows up, not just in March when a refund is on the line. Our roots are in this community. We shop where you shop, our kids go to the same schools, and we understand the real financial pressures Central Valley families face, from managing rental properties in Clovis to running a small farm operation outside Selma.") +
        p_html("At its heart, C&amp;R Tax Services was built on a simple promise: treat every return like it belongs to family. Whether you’re filing a straightforward W-2, applying for an ITIN, or untangling a multi-state small business return, we want you to walk out of our office feeling something most people never associate with taxes — genuine peace of mind.", last=True)
    )
    secs.append(section([text_editor(story_left)]))

    # What we stand for (alt bg)
    secs.append(section([
        heading("What We Stand For"),
        text_editor(
            p_html("Everything we do at C&amp;R Tax Services comes back to three values: honesty, accuracy, and accessibility. Taxes are stressful enough without feeling talked down to, so we take the time to explain your return in plain language — what you’re claiming, why it matters, and how to plan smarter for next year.") +
            p_html("These aren’t just words on a website. They show up in the small things: answering questions patiently, being available year-round, and never treating you like a number in a queue. Because to us, you’re not a transaction — you’re a neighbor.", last=True)
        ),
        diff_grid_html(VALUES),
    ], bg=SURFACE_ALT))

    # Meet the people (white)
    people_text = (
        p_html("C&amp;R Tax Services is led by <strong>[Owner Name(s)]</strong>, [a Fresno local / lifelong Central Valley resident] with a passion for helping working families and small business owners keep more of what they earn. <em>([Owner] spent [X] years in accounting and financial services before opening the firm, or a personal/family motivation for starting the business.)</em>") +
        p_html("Beyond tax preparation, our team is [certified/registered] to provide notary public services, loan signing support, and Live Scan fingerprinting — making us a true one-stop compliance resource for local startups, caregivers, real estate professionals, and anyone who needs documents handled quickly and correctly.") +
        p_html("When we’re not helping clients, you’ll find us involved in the community we serve — because we’re not just building a business in Fresno, we’re building relationships that last well beyond tax season.", last=True)
    )
    creds_html = checklist_html(CREDENTIALS)
    secs.append(section([
        heading("Meet the People Behind C&amp;R"),
        text_editor(people_text),
        spacer(32),
        heading("Credentials &amp; Services", tag="h3", size=T["base"], mb=14),
        text_editor(creds_html),
    ]))

    # Why homeowners trust (alt bg)
    secs.append(section([
        heading("Why Homeowners and Local Families Trust C&amp;R Tax Services"),
        text_editor(
            p_html("We know what keeps you up at night during tax season: <em>Did I miss a deduction? Is this preparer going to disappear if the IRS sends me a letter? Am I being overcharged?</em> We built C&amp;R Tax Services specifically to put those fears to rest. Unlike seasonal franchise offices, we’re a local firm with year-round support — if a notice arrives in August, we’re here to handle it. And unlike DIY software, we bring a real human eye to your return, catching deductions and credits that automated tools routinely miss.") +
            p_html("And because we also offer notary and Live Scan fingerprinting services under the same roof, many of our clients discover we can handle far more than just their taxes. New business owners, homebuyers, and families navigating licensing requirements all find that having one trusted local firm for tax preparation, document notarization, and background-check fingerprinting saves time, money, and stress.", last=True)
        ),
        trust_pills_html(TRUST_POINTS),
    ], bg=SURFACE_ALT))

    # Service area (white)
    secs.append(section([
        heading("Serving the Central Valley"),
        text_editor(p_html("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&amp;R Tax Services is ready when you are. Have a question? Just ask — that’s what neighbors are for.", last=True)),
        city_pills_html(CITIES),
    ], pad_top=SP[20], pad_bot=SP[20]))

    # Final CTA (navy)
    cta_content = (
        f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
        f'color:{WHITE};margin:0 0 16px;">Let’s Talk — We’d Love to Meet You</h2>'
        f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
        f'color:{ICE_BLUE};margin:0 0 28px;max-width:620px;">'
        f'If you’ve been searching for Fresno tax preparation that actually feels personal, '
        f'we’d love to be the last search you make. Come by for a friendly, no-pressure '
        f'conversation about your taxes, your business, or your goals for next year — or '
        f'upload your documents through our secure virtual portal and let us take it from there. '
        f'No jargon, no surprises, just honest help from people who genuinely care.</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;">'
        f'<a href="/contact" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:{RED};color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;">'
        f'<i class="fas fa-phone" style="font-size:16px;"></i> Get in Touch</a>'
        f'<a href="tel:5599627503" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:transparent;color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;'
        f'border:2px solid {WHITE};">Schedule Your Appointment</a>'
        f'</div>'
    )
    secs.append(section([text_editor(cta_content)], bg=NAVY, pad_top=SP[24], pad_bot=SP[24]))

    return secs


def build_contact():
    REASONS = [
        ("question-circle", "General questions",
         "Not sure which documents you need? Wondering about an extension? Just ask."),
        ("tag", "Free quotes",
         "Get upfront, honest pricing for your tax preparation before we file a thing."),
        ("exclamation-triangle", "Urgent tax matters",
         "Got an IRS letter or a looming deadline? Call right away, and we’ll help you respond fast."),
        ("stamp", "Notary &amp; Live Scan appointments",
         "Need a document notarized or Live Scan fingerprints for a job or license? We can usually get you in quickly."),
    ]
    CITIES = ["Fresno", "Selma", "Reedley", "Clovis", "Madera", "Sanger"]

    secs = []

    # Hero (navy)
    hero_content = (
        hero_icon_html("comment-alt") +
        f'<span style="display:inline-block;background:{RED};color:{WHITE};'
        f'font-family:Inter,sans-serif;font-size:13px;font-weight:700;'
        f'padding:4px 14px;border-radius:999px;margin-bottom:18px;">'
        f'Real People, Fast Responses</span><br>'
        f'<h1 style="font-family:Poppins,sans-serif;font-weight:800;font-size:50px;'
        f'line-height:1.15;color:{WHITE};margin:0 0 16px;max-width:680px;">'
        f'We’re Glad You’re Here</h1>'
        f'<p style="font-family:Inter,sans-serif;font-size:20px;color:{ICE_BLUE};'
        f'line-height:1.6;margin:0 0 28px;max-width:620px;">'
        f'Thanks for stopping by! If you’ve been looking for trusted Fresno tax preparation, '
        f'you’re in the right place. At C&amp;R Tax Services, there’s no automated '
        f'runaround and no call center in another state. You’ll talk with real, friendly '
        f'people right here in Fresno — ready to listen, answer your questions, and help '
        f'you feel good about your taxes.</p>'
        f'<a href="#contact-info" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:{RED};color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;">'
        f'Request a Free Quote</a>'
    )
    secs.append(section([text_editor(hero_content)], bg=NAVY, pad_top=SP[20], pad_bot=SP[20]))

    # How to reach us (white) — contact card + hours
    reach_html = (
        f'<div id="contact-info" style="display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start;'
        f'margin-top:32px;">'
        f'<div style="flex:1 1 320px;max-width:420px;">'
        f'{contact_card_html()}'
        f'</div>'
        f'<div style="flex:1 1 280px;">'
        + p_html("We’re open during posted business hours below. When you reach out, a member of our team — not a bot — reads your message and replies the same business day, often within a few hours. We’ll give you clear answers or set up a time to meet, in our office or online.")
        + p_html("<strong>¡Se habla español!</strong> Ask your questions in the language you’re most comfortable with.")
        + p_html("No pressure. No obligation. Just honest help.", last=True)
        + f'</div>'
        f'</div>'
        f'<div style="margin-top:40px;">'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
        f'color:{TEXT_HEAD};margin:0 0 16px;">Office Hours</h3>'
        f'<div style="display:flex;flex-wrap:wrap;gap:24px;">'
        f'<div style="flex:1 1 280px;max-width:400px;">{hours_card_html("tax")}</div>'
        f'<div style="flex:1 1 280px;max-width:400px;">{hours_card_html("after")}</div>'
        f'</div>'
        f'</div>'
    )
    secs.append(section([
        heading("How to Reach Us"),
        text_editor(p_html("Getting in touch is easy. Pick whatever works best for you.", last=True)),
        text_editor(reach_html),
    ]))

    # Why reach out (alt bg)
    secs.append(section([
        heading("Why Reach Out?"),
        text_editor(p_html("Whatever brings you here, we’re happy to help.", last=True)),
        diff_grid_html(REASONS),
    ], bg=SURFACE_ALT))

    # Trust / service area (white)
    secs.append(section([
        heading("Your Trusted Local Team"),
        text_editor(
            p_html("C&amp;R Tax Services is locally owned and operated, fully credentialed, and committed to accuracy on every return — with year-round support, not just at tax time. Real answers from a local team — we’re here after April 15th, not just before it.") +
            p_html("Fully credentialed and locally owned in Fresno — your neighbors, not a national chain.", last=True)
        ),
        heading("Proudly Serving the Central Valley", tag="h3", size=T["base"], mb=12),
        city_pills_html(CITIES),
    ]))

    # Final CTA (navy)
    cta_content = (
        f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
        f'color:{WHITE};margin:0 0 16px;">Let’s Get Started Today</h2>'
        f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
        f'color:{ICE_BLUE};margin:0 0 28px;max-width:620px;">'
        f'Tax questions don’t get easier by waiting — but they do get easier with the '
        f'right team in your corner. Call now or reach out below. A local, professional team you '
        f'can actually talk to will take the stress off your plate. Families and small businesses '
        f'across Fresno trust us because we treat their money like our own — and we’d '
        f'love to earn your trust, too.</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;">'
        f'<a href="tel:5599627503" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:{RED};color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;">'
        f'<i class="fas fa-phone" style="font-size:16px;"></i> Request a Free Quote</a>'
        f'<a href="tel:5599627503" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:transparent;color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;'
        f'border:2px solid {WHITE};">Get Help Now</a>'
        f'</div>'
    )
    secs.append(section([text_editor(cta_content)], bg=NAVY, pad_top=SP[24], pad_bot=SP[24]))

    return secs


# ── WordPress save ────────────────────────────────────────────────────────────

def save_elementor(post_id, sections):
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
    return result.get("return_value", result)


def get_or_create_page(slug, title):
    result = php(f"""
$p = get_page_by_path('{slug}');
if ($p) return (int)$p->ID;
$id = wp_insert_post([
    'post_title'  => '{title}',
    'post_name'   => '{slug}',
    'post_status' => 'publish',
    'post_type'   => 'page',
]);
return (int)$id;
""")
    rv = result.get("return_value", result) if isinstance(result, dict) else result
    return int(rv)


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
    print("=== About & Contact Pages — v7 Rebuild ===\n")

    print("1. Resolving About page ID...")
    about_id = get_or_create_page("about", "About")
    print(f"   About page ID: {about_id}")
    about_secs = build_about()
    result = save_elementor(about_id, about_secs)
    print(f"   Saved: {result}")

    print("2. Resolving Contact page ID...")
    contact_id = get_or_create_page("contact", "Contact")
    print(f"   Contact page ID: {contact_id}")
    contact_secs = build_contact()
    result = save_elementor(contact_id, contact_secs)
    print(f"   Saved: {result}")

    print("3. Clearing caches...")
    clear_cache()
    print("\n=== DONE ===")
    print(f"   About:   /about  (post {about_id})")
    print(f"   Contact: /contact  (post {contact_id})")


if __name__ == "__main__":
    build()
