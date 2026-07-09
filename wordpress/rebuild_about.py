#!/usr/bin/env python3
"""
C&R Tax Services — About page (post 37) rebuild
Uses the same Elementor container structure as rebuild_notary_livescan.py
"""
import json, random, string, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

NAVY       = "#1B2A5E"; ROYAL_BLUE = "#0A4A93"; RED   = "#E23A28"
ICE_BLUE   = "#EAF0F8"; OFF_WHITE  = "#F7F8FA"
WHITE      = "#FFFFFF"; BORDER     = "#D7DEEA"
TEXT_BODY  = "#374151"; TEXT_HEAD  = "#111827"; TEXT_MUTED = "#6B7280"

SP = {4:16,5:20,6:24,8:32,10:40,12:48,16:64,20:80,24:96}
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

# ── Elementor builders (same pattern as working scripts) ──────────────────────
def uid(): return "".join(random.choices(string.ascii_lowercase+string.digits, k=7))
def pad(t,r,b,l,u="px"): return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}
def size(v,u="px"): return {"size":v,"unit":u}
def gap(v,unit="px"): return {"column":v,"row":v,"unit":unit,"isLinked":True}

def con(settings, elements, is_inner=True):
    s = dict(settings)
    if "background_color" in s and "background_background" not in s:
        s["background_background"] = "classic"
    return {"id":uid(),"elType":"container","isInner":is_inner,"settings":s,"elements":elements}

def sec(settings, elements):
    c = con(settings, elements, False)
    c["isInner"] = False
    return c

def wgt(widget_type, settings):
    return {"id":uid(),"elType":"widget","widgetType":widget_type,"isInner":True,
            "settings":dict(settings),"elements":[]}

def inner(max_w=760):
    return {"flex_direction":"column","padding":pad(0,0,0,0),
            "content_width":"full","max_width":size(max_w)}

def t(html): return wgt("text-editor", {"editor": html})
def sp(h):   return wgt("spacer", {"space": size(h)})

# ── HTML helpers ──────────────────────────────────────────────────────────────
def p(text, last=False):
    mb = "0" if last else "16px"
    return (f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;'
            f'color:{TEXT_BODY};margin:0 0 {mb};">{text}</p>')

def h2(text, mb=20):
    return (f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
            f'color:{TEXT_HEAD};margin:0 0 {mb}px;">{text}</h2>')

def h3(text, mb=6):
    return (f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
            f'color:{TEXT_HEAD};margin:0 0 {mb}px;">{text}</h3>')

def diff_card(icon_fa, title, body):
    return (
        f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:10px;padding:24px;">'
        f'<div style="width:40px;height:40px;border-radius:10px;background:{NAVY};'
        f'display:flex;align-items:center;justify-content:center;margin-bottom:12px;">'
        f'<i class="fas fa-{icon_fa}" style="font-size:20px;color:{OFF_WHITE};"></i></div>'
        f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:17px;'
        f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
        f'<p style="font-family:Inter,sans-serif;font-size:15px;color:{TEXT_BODY};'
        f'line-height:1.6;margin:0;">{body}</p></div>'
    )

def check_item(text):
    return (
        f'<li style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;">'
        f'<div style="width:24px;height:24px;border-radius:999px;background:{OFF_WHITE};'
        f'display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">'
        f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i></div>'
        f'<span style="font-family:Inter,sans-serif;font-size:17px;color:{TEXT_BODY};'
        f'line-height:1.5;">{text}</span></li>'
    )

def trust_pill(text):
    return (
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 16px;'
        f'border-radius:999px;background:{WHITE};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i>{text}</span>'
    )

def city_pill(city):
    return (
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
        f'border-radius:999px;background:{OFF_WHITE};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:15px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-map-marker-alt" style="font-size:14px;color:{ROYAL_BLUE};"></i>{city}</span>'
    )

# ── Page sections ─────────────────────────────────────────────────────────────
def build_about():
    VALUES = [
        ("tag", "Honesty",
         "Upfront, transparent pricing — you'll know exactly what your Fresno tax preparation "
         "will cost before we ever file, with no surprise tiers or hidden percentages."),
        ("shield-alt", "Accuracy",
         "We stand behind every return we prepare. If we make an error, we make it right — "
         "covering the adjustment costs and amending your return at no charge."),
        ("users", "Accessibility",
         "We explain your return in plain language, and offer both in-person and secure virtual "
         "tax preparation — so getting your taxes done right fits into your life."),
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

    sections = []

    # ── 1. Hero (navy) ────────────────────────────────────────────────────────
    hero_html = (
        f'<div style="width:56px;height:56px;border-radius:10px;background:rgba(247,248,250,0.12);'
        f'display:flex;align-items:center;justify-content:center;margin-bottom:24px;">'
        f'<i class="fas fa-heart" style="font-size:28px;color:{OFF_WHITE};"></i></div>'
        f'<span style="display:inline-block;background:{RED};color:{WHITE};font-family:Inter,sans-serif;'
        f'font-size:13px;font-weight:700;padding:4px 14px;border-radius:999px;margin-bottom:18px;">'
        f'Local &amp; Family-Focused</span>'
        f'<h1 style="font-family:Poppins,sans-serif;font-weight:800;font-size:50px;line-height:1.15;'
        f'color:{WHITE};margin:18px 0 16px;max-width:680px;">Why We Started C&amp;R Tax Services</h1>'
        f'<p style="font-family:Inter,sans-serif;font-size:20px;color:{ICE_BLUE};line-height:1.6;'
        f'margin:0;max-width:620px;">Tax season shouldn\'t feel like a guessing game — but for too '
        f'many Central Valley families, that\'s exactly what it\'s become.</p>'
    )
    sections.append(sec(
        {"background_color": NAVY, "padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(780), [t(hero_html)])]
    ))

    # ── 2. Our story (white) ──────────────────────────────────────────────────
    story_html = (
        p("Tax season shouldn't feel like a guessing game. But for too many families and small "
          "business owners here in the Central Valley, that's exactly what it's become — confusing "
          "software, pop-up franchise offices that disappear on April 16th, and preparers who rush "
          "you out the door without ever explaining what they filed on your behalf. C&amp;R Tax "
          "Services was founded to be the opposite of all that.") +
        p("We started this firm right here in Fresno because we believe our neighbors deserve a tax "
          "preparer who actually knows them — someone who picks up the phone in July when an IRS "
          "letter shows up, not just in March when a refund is on the line. Our roots are in this "
          "community. We shop where you shop, our kids go to the same schools, and we understand the "
          "real financial pressures Central Valley families face.") +
        p("At its heart, C&amp;R Tax Services was built on a simple promise: treat every return like "
          "it belongs to family. Whether you're filing a straightforward W-2, applying for an ITIN, "
          "or untangling a multi-state small business return, we want you to walk out of our office "
          "feeling something most people never associate with taxes — genuine peace of mind.", last=True)
    )
    sections.append(sec(
        {"padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(780), [t(story_html)])]
    ))

    # ── 3. What we stand for (alt bg) ─────────────────────────────────────────
    diff_html = "".join(diff_card(*v) for v in VALUES)
    values_html = (
        h2("What We Stand For") +
        p("Everything we do at C&amp;R Tax Services comes back to three values: honesty, accuracy, "
          "and accessibility. Taxes are stressful enough without feeling talked down to, so we take "
          "the time to explain your return in plain language — what you're claiming, why it matters, "
          "and how to plan smarter for next year.") +
        p("These aren't just words on a website. They show up in the small things: answering questions "
          "patiently, being available year-round, and never treating you like a number in a queue. "
          "Because to us, you're not a transaction — you're a neighbor.", last=True) +
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));'
        f'gap:24px;margin-top:32px;">{diff_html}</div>'
    )
    sections.append(sec(
        {"background_color": OFF_WHITE, "padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(760), [t(values_html)])]
    ))

    # ── 4. Meet the people (white) ────────────────────────────────────────────
    creds_items = "".join(check_item(c) for c in CREDENTIALS)
    people_html = (
        h2("Meet the People Behind C&amp;R") +
        p("C&amp;R Tax Services is led by <strong>[Owner Name(s)]</strong>, [a Fresno local / "
          "lifelong Central Valley resident] with a passion for helping working families and small "
          "business owners keep more of what they earn.") +
        p("Beyond tax preparation, our team is [certified/registered] to provide notary public "
          "services, loan signing support, and Live Scan fingerprinting — making us a true "
          "one-stop compliance resource for local startups, caregivers, and real estate professionals.") +
        p("When we're not helping clients, you'll find us involved in the community we serve — "
          "because we're not just building a business in Fresno, we're building relationships that "
          "last well beyond tax season.", last=True) +
        f'<div style="margin-top:32px;background:{WHITE};border:1px solid {BORDER};'
        f'border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:32px;">'
        f'{h3("Credentials &amp; Services", mb=14)}'
        f'<ul style="list-style:none;margin:0;padding:0;">{creds_items}</ul></div>'
    )
    sections.append(sec(
        {"padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(780), [t(people_html)])]
    ))

    # ── 5. Why homeowners trust us (alt bg) ───────────────────────────────────
    pills_html = "".join(trust_pill(tp) for tp in TRUST_POINTS)
    trust_html = (
        h2("Why Homeowners and Local Families Trust C&amp;R Tax Services") +
        p("We know what keeps you up at night during tax season: <em>Did I miss a deduction? Is this "
          "preparer going to disappear if the IRS sends me a letter? Am I being overcharged?</em> We "
          "built C&amp;R Tax Services specifically to put those fears to rest. Unlike seasonal franchise "
          "offices, we're a local firm with year-round support — if a notice arrives in August, we're "
          "here to handle it.") +
        p("And because we also offer notary and Live Scan fingerprinting services under the same roof, "
          "many of our clients discover we can handle far more than just their taxes.", last=True) +
        f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:24px;margin-bottom:32px;">'
        f'{pills_html}</div>'
    )
    sections.append(sec(
        {"background_color": OFF_WHITE, "padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(760), [t(trust_html)])]
    ))

    # ── 6. Service area (white) ───────────────────────────────────────────────
    cities_html = "".join(city_pill(c) for c in CITIES)
    area_html = (
        h2("Serving the Central Valley") +
        p("Serving Fresno, Clovis, Selma, Reedley, Sanger, and Madera, C&amp;R Tax Services is ready "
          "when you are. Have a question? Just ask — that's what neighbors are for.", last=True) +
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px;">{cities_html}</div>'
    )
    sections.append(sec(
        {"padding": pad(SP[20],SP[8],SP[20],SP[8])},
        [con(inner(700), [t(area_html)])]
    ))

    # ── 7. Final CTA (navy) ───────────────────────────────────────────────────
    cta_html = (
        f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:38px;'
        f'color:{WHITE};margin:0 0 16px;">Let\'s Talk — We\'d Love to Meet You</h2>'
        f'<p style="font-family:Inter,sans-serif;font-size:17px;line-height:1.6;color:{ICE_BLUE};'
        f'margin:0 0 28px;max-width:620px;">If you\'ve been searching for Fresno tax preparation '
        f'that actually feels personal, we\'d love to be the last search you make. Come by for a '
        f'friendly, no-pressure conversation about your taxes, your business, or your goals for '
        f'next year — no jargon, no surprises, just honest help from people who genuinely care.</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;">'
        f'<a href="/contact" style="display:inline-flex;align-items:center;gap:8px;background:{RED};'
        f'color:{WHITE};font-family:Inter,sans-serif;font-weight:600;font-size:17px;padding:14px 28px;'
        f'border-radius:8px;text-decoration:none;">'
        f'<i class="fas fa-phone" style="font-size:16px;"></i> Get in Touch</a>'
        f'<a href="tel:5599627503" style="display:inline-flex;align-items:center;gap:8px;'
        f'background:transparent;color:{WHITE};font-family:Inter,sans-serif;font-weight:600;'
        f'font-size:17px;padding:14px 28px;border-radius:8px;text-decoration:none;'
        f'border:2px solid {WHITE};">Schedule Your Appointment</a>'
        f'</div>'
    )
    sections.append(sec(
        {"background_color": NAVY, "padding": pad(SP[24],SP[8],SP[24],SP[8])},
        [con(inner(780), [t(cta_html)])]
    ))

    return sections

# ── Save ──────────────────────────────────────────────────────────────────────
def save_elementor(post_id, elementor_data):
    path = f"wp-content/novamira-sandbox/el_{post_id}.json"
    write_file(path, json.dumps(elementor_data))
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

def build():
    print("=== About Page — Rebuild with correct Elementor structure ===\n")
    sections = build_about()
    r = save_elementor(37, sections)
    print(f"Saved: {r}")
    print("Clearing cache...")
    clear_cache()
    print("Done — /about (post 37)")

if __name__ == "__main__":
    build()
