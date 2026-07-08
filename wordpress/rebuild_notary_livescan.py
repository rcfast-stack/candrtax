#!/usr/bin/env python3
"""
C&R Tax Services — Notary (post 29) & Livescan (post 30) rebuild
Matches v6 design: 8 sections each, same structure as Income Tax page
"""
import json, random, string, requests

MCP_URL = "https://wordpress-1254753-6532124.cloudwaysapps.com/wp-json/mcp/novamira"
AUTH    = ("jtoews@consult-smart.com", "YJjCpzthlwizjnPCMMGF9aNO")

NAVY       = "#1B2A5E"; ROYAL_BLUE = "#0A4A93"; RED   = "#E23A28"
ICE_BLUE   = "#EAF0F8"; OFF_WHITE  = "#F7F8FA"; SLATE = "#5A6B8C"
WHITE      = "#FFFFFF"; BORDER     = "#D7DEEA"
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

# ── ELEMENT BUILDERS ─────────────────────────────────────────────────────────
def uid(): return ''.join(random.choices(string.ascii_lowercase+string.digits, k=7))
def pad(t,r,b,l,u="px"): return {"top":str(t),"right":str(r),"bottom":str(b),"left":str(l),"unit":u,"isLinked":False}
def size(v,u="px"): return {"size":v,"unit":u}
def gap(v,unit="px"): return {"column":v,"row":v,"unit":unit,"isLinked":True}

def con(settings, elements, is_inner=True):
    s = dict(settings)
    if "justify_content" in s: s["flex_justify_content"] = s.pop("justify_content")
    if "align_items" in s:     s["flex_align_items"]     = s.pop("align_items")
    if "gap" in s:             s["flex_gap"]             = s.pop("gap")
    if "background_color" in s and "background_background" not in s:
        s["background_background"] = "classic"
    return {"id":uid(),"elType":"container","isInner":is_inner,"settings":s,"elements":elements}

def sec(settings, elements):
    c = con(settings, elements, False); c["isInner"] = False; return c

def wgt(widget_type, settings):
    return {"id":uid(),"elType":"widget","widgetType":widget_type,"isInner":True,
            "settings":dict(settings),"elements":[]}

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
    return result.get("return_value", result)

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

# ── HTML HELPERS ─────────────────────────────────────────────────────────────
def badge(text): return (f'<span style="display:inline-block;padding:4px 14px;border-radius:999px;'
    f'background:{RED};color:{WHITE};font-family:Inter,sans-serif;font-size:13px;font-weight:600;'
    f'letter-spacing:0.03em;">{text}</span>')

def h2(text): return (f'<h2 style="font-family:Poppins,sans-serif;font-weight:700;font-size:{T["3xl"]}px;'
    f'color:{TEXT_HEAD};margin:0 0 20px;line-height:1.15;">{text}</h2>')

def p(text, last=False): return (f'<p style="font-family:Inter,sans-serif;font-size:{T["base"]}px;'
    f'line-height:1.6;color:{TEXT_BODY};margin:{"0" if last else "0 0 16px"};">{text}</p>')

def img_ph(caption, alt="", height=220):
    return wgt("text-editor", {"editor":
        f'<div style="height:{height}px;border-radius:16px;background:{ICE_BLUE};'
        f'border:1px dashed {SLATE};display:flex;flex-direction:column;align-items:center;'
        f'justify-content:center;gap:10px;padding:24px;text-align:center;">'
        f'<p style="font-family:Inter,sans-serif;font-size:14px;color:{SLATE};margin:0;">📷 {caption}</p>'
        + (f'<p style="font-family:Inter,sans-serif;font-size:12px;color:{SLATE};opacity:.7;font-style:italic;margin:0;">alt: &ldquo;{alt}&rdquo;</p>' if alt else "")
        + '</div>'
    })

def city_pills():
    cities = ["Fresno","Clovis","Sanger","Selma","Madera"]
    spans = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
        f'border-radius:999px;background:{WHITE};border:1px solid {BORDER};'
        f'font-family:Inter,sans-serif;font-size:{T["sm"]}px;font-weight:600;color:{NAVY};">'
        f'<i class="fas fa-map-marker-alt" style="font-size:14px;color:{ROYAL_BLUE};"></i>{c}</span>'
        for c in cities
    )
    return f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin:{SP[8]}px 0;">{spans}</div>'

def check_item(text, border=True):
    bb = f";border-bottom:1px solid {BORDER}" if border else ""
    return (f'<li style="display:flex;align-items:flex-start;gap:14px;padding:{SP[5]}px 0{bb};">'
            f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:28px;height:28px;border-radius:999px;background:{ICE_BLUE};flex-shrink:0;margin-top:2px;">'
            f'<i class="fas fa-check" style="font-size:13px;color:{ROYAL_BLUE};"></i></span>'
            f'<span style="font-family:Inter,sans-serif;font-size:{T["lg"]}px;color:{TEXT_BODY};'
            f'line-height:1.35;padding-top:3px;">{text}</span></li>')

def checklist_card(items, footnote=None):
    items_html = "".join(check_item(it, border=(i < len(items)-1)) for i, it in enumerate(items))
    foot = ""
    if footnote:
        foot = (f'<p style="margin:{SP[8]}px 0 0;padding-top:{SP[6]}px;border-top:1px solid {BORDER};'
                f'font-family:Inter,sans-serif;font-size:{T["sm"]}px;color:{TEXT_MUTED};font-style:italic;">{footnote}</p>')
    return wgt("text-editor", {"editor":
        f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:16px;'
        f'box-shadow:0 1px 4px rgba(0,0,0,0.06);padding:{SP[10]}px;">'
        f'<ul style="list-style:none;margin:0;padding:0;">{items_html}</ul>{foot}</div>'
    })

def diff_card(icon_fa, title, body):
    return (f'<div style="background:{WHITE};border:1px solid {BORDER};border-radius:10px;padding:{SP[6]}px;">'
            f'<div style="width:40px;height:40px;border-radius:10px;background:{NAVY};'
            f'display:flex;align-items:center;justify-content:center;margin-bottom:12px;">'
            f'<i class="fas fa-{icon_fa}" style="font-size:20px;color:{OFF_WHITE};"></i></div>'
            f'<h3 style="font-family:Poppins,sans-serif;font-weight:600;font-size:{T["base"]}px;'
            f'color:{TEXT_HEAD};margin:0 0 6px;">{title}</h3>'
            f'<p style="font-family:Inter,sans-serif;font-size:{T["sm"]}px;color:{TEXT_BODY};'
            f'line-height:1.6;margin:0;">{body}</p></div>')

def diff_grid(diffs):
    cards = "".join(diff_card(fa, t, b) for fa, t, b in diffs)
    return (f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));'
            f'gap:{SP[6]}px;margin-top:{SP[8]}px;margin-bottom:{SP[8]}px;">{cards}</div>')

def review_box():
    return (f'<div style="margin-top:{SP[8]}px;padding:18px 22px;background:{ICE_BLUE};'
            f'border:1px solid {BORDER};border-radius:10px;">'
            f'<p style="font-family:Inter,sans-serif;font-size:{T["sm"]}px;'
            f'color:{TEXT_MUTED};font-style:italic;margin:0;">'
            f'Verified client reviews will go here once collected via Google Business Profile.</p></div>')

def inner(max_width=760):
    return {"content_width":"boxed","width":size(max_width,"px"),"flex_direction":"column"}

# ── SHARED SECTION BUILDERS ───────────────────────────────────────────────────

def hero_sec(icon_fa, badge_text, h1, intro_text, cta1_text, cta1_href, cta2_text, cta2_href):
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(80,32,80,32)},
        [con(inner(780), [
            wgt("text-editor", {"editor":
                f'<div style="width:56px;height:56px;border-radius:10px;'
                f'background:rgba(247,248,250,0.12);display:flex;align-items:center;'
                f'justify-content:center;margin-bottom:{SP[6]}px;">'
                f'<i class="fas fa-{icon_fa}" style="font-size:28px;color:{WHITE};"></i></div>'
                f'<div style="margin-bottom:18px;">{badge(badge_text)}</div>'
            }),
            wgt("heading", {
                "title": h1, "header_size": "h1",
                "typography_typography":"custom","typography_font_family":"Poppins",
                "typography_font_weight":"800","typography_font_size":size(T["4xl"]),
                "title_color":WHITE,
                "_margin":{"top":"0","right":"0","bottom":"16","left":"0","unit":"px","isLinked":False},
            }),
            wgt("text-editor", {"editor":
                f'<p style="font-family:Inter,sans-serif;font-size:{T["lg"]}px;color:{ICE_BLUE};'
                f'line-height:1.6;max-width:620px;margin:0 0 {SP[8]}px;">{intro_text}</p>'
            }),
            con({"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(12),"padding":pad(0,0,0,0)}, [
                wgt("button", {
                    "text":cta1_text,"link":{"url":cta1_href},
                    "button_type":"info","size":"lg",
                    "button_background_color":RED,"button_text_color":WHITE,
                    "button_background_hover_color":"#C22E1F","button_background_hover_background":"classic",
                    "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                    "typography_font_family":"Inter","typography_font_weight":"600",
                }),
                wgt("button", {
                    "text":cta2_text,"link":{"url":cta2_href},
                    "button_type":"info","size":"lg",
                    "button_background_color":"transparent","button_text_color":WHITE,
                    "button_background_background":"classic",
                    "border_border":"solid","border_width":pad(2,2,2,2),"border_color":"rgba(247,248,250,0.4)",
                    "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                    "typography_font_family":"Inter","typography_font_weight":"600",
                }),
            ]),
        ])]
    )

def intro_sec(paras, img_caption, img_alt):
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner(780), [
            con({"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(48),
                 "flex_align_items":"flex-start","padding":pad(0,0,0,0)}, [
                con({"flex":"1 1 420px","flex_direction":"column","padding":pad(0,0,0,0)},
                    [wgt("text-editor",{"editor":"".join(paras)})]),
                con({"flex":"1 1 280px","max_width":size(320),"padding":pad(0,0,0,0)},
                    [img_ph(img_caption, img_alt, 260)]),
            ]),
        ])]
    )

def what_solves_sec(paras, img_caption, img_alt):
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner(760), [
            wgt("text-editor",{"editor": h2("What This Service Solves") + "".join(paras)}),
            img_ph(img_caption, img_alt, 220),
        ])]
    )

def checklist_sec(heading, items, footnote=None):
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner(760), [
            wgt("text-editor",{"editor": h2(heading)}),
            checklist_card(items, footnote),
        ])]
    )

def how_better_sec(paras, diffs, img_caption, img_alt):
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner(760), [
            wgt("text-editor",{"editor":
                h2("How C&amp;R Tax Services Does It Better")
                + "".join(paras)
                + diff_grid(diffs)
            }),
            img_ph(img_caption, img_alt, 220),
        ])]
    )

def results_sec(paras):
    return sec(
        {"content_width":"full","padding":pad(80,32,80,32)},
        [con(inner(700), [
            wgt("text-editor",{"editor": h2("Real-World Results") + "".join(paras) + review_box()}),
        ])]
    )

def trust_sec(paras, img_caption, img_alt):
    return sec(
        {"content_width":"full","background_color":ICE_BLUE,"padding":pad(80,32,80,32)},
        [con(inner(760), [
            wgt("text-editor",{"editor":
                h2("Local Trust &amp; Licensing") + "".join(paras) + city_pills()
            }),
            img_ph(img_caption, img_alt, 220),
        ])]
    )

def final_cta_sec(h2_text, body_text, cta1_text, cta1_href, cta2_text, cta2_href, img_caption, img_alt):
    return sec(
        {"content_width":"full","background_color":NAVY,"padding":pad(96,32,96,32)},
        [con(inner(780), [
            wgt("heading",{
                "title":h2_text,"header_size":"h2",
                "typography_typography":"custom","typography_font_family":"Poppins",
                "typography_font_weight":"700","typography_font_size":size(T["3xl"]),
                "title_color":WHITE,
                "_margin":{"top":"0","right":"0","bottom":"16","left":"0","unit":"px","isLinked":False},
            }),
            wgt("text-editor",{"editor":
                f'<p style="font-family:Inter,sans-serif;font-size:{T["base"]}px;color:{ICE_BLUE};'
                f'line-height:1.6;max-width:620px;margin:0 0 {SP[8]}px;">{body_text}</p>'
            }),
            con({"flex_direction":"row","flex_wrap":"wrap","flex_gap":gap(12),"padding":pad(0,0,SP[10],0)},[
                wgt("button",{
                    "text":cta1_text,"link":{"url":cta1_href},
                    "button_type":"info","size":"lg",
                    "button_background_color":RED,"button_text_color":WHITE,
                    "button_background_hover_color":"#C22E1F","button_background_hover_background":"classic",
                    "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                    "typography_font_family":"Inter","typography_font_weight":"600",
                }),
                wgt("button",{
                    "text":cta2_text,"link":{"url":cta2_href},
                    "button_type":"info","size":"lg",
                    "button_background_color":"transparent","button_text_color":WHITE,
                    "button_background_background":"classic",
                    "border_border":"solid","border_width":pad(2,2,2,2),"border_color":"rgba(247,248,250,0.4)",
                    "border_radius":pad(6,6,6,6),"button_padding":pad(14,28,14,28),
                    "typography_font_family":"Inter","typography_font_weight":"600",
                }),
            ]),
            img_ph(img_caption, img_alt, 220),
        ])]
    )


# ══════════════════════════════════════════════════════════════════════════════
# NOTARY PAGE (post 29)
# ══════════════════════════════════════════════════════════════════════════════
def build_notary():
    return [
        hero_sec("stamp", "Mobile Service Available",
            "The Best Notary in the Central Valley &mdash; Fast, Friendly, and Right Here in Fresno",
            "Certified notarization and loan signing for the documents that matter most &mdash; in-office or on the road.",
            "Book Your Appointment", "tel:5599627503",
            "Ask About Mobile Service", "#contact"),

        intro_sec(
            [p("The paperwork you&rsquo;ve been waiting on finally arrived &mdash; maybe a loan packet, a power of attorney, or travel consent forms for your kids. There&rsquo;s just one catch: none of it counts until it&rsquo;s notarized. Now you&rsquo;re stuck searching for someone who can do it right, do it soon, and not make you feel rushed or confused along the way."),
             p("That&rsquo;s where C&amp;R Tax Services comes in. We&rsquo;re a local Fresno office offering notary public and loan signing agent services for bank documents, real estate paperwork, powers of attorney, travel documents, and legal forms of every kind. Because we&rsquo;re also a full tax preparation office, handling sensitive paperwork isn&rsquo;t a side gig for us &mdash; it&rsquo;s what we do all day, every day."),
             p("Our notaries are commissioned by the State of California, bonded, and trained to walk you through every signature and stamp. If Spanish is your first language, you&rsquo;re in the right place, too. <strong>Se habla espa&ntilde;ol.</strong> You&rsquo;ll never have to guess what you&rsquo;re signing or bring a friend along to translate.", last=True)],
            "A friendly notary at a desk stamping a document while a smiling client looks on.",
            "Fresno notary public notarizing legal documents for a local client at C&R Tax Services"),

        what_solves_sec(
            [p("Life has a way of handing you paperwork at the worst possible moments. Maybe you&rsquo;re closing on a home in Fresno or Clovis and the lender needs a certified loan signing agent before the deal can fund. Maybe a parent&rsquo;s health is declining and your family needs a power of attorney notarized this week, not next month. Or maybe your child is flying to visit family in Mexico, and the airline won&rsquo;t let them board without a notarized travel consent letter."),
             p("These aren&rsquo;t rare situations. They&rsquo;re everyday moments for Central Valley families, and every one comes with a deadline. When a signature is missing or a stamp is done wrong, closings get delayed, court filings get rejected, and travel plans fall apart. A good notary does more than witness a signature &mdash; they protect you from expensive do-overs."),
             p("Many of our notary clients first found us through our tax work, and that&rsquo;s no coincidence. The same people who need help with tax preparation in Fresno often need an ITIN form certified, a bank document witnessed, or real estate paperwork signed and sealed. Having one trusted local office for both means fewer trips and a lot less stress.", last=True)],
            "Close-up of hands signing a real estate loan document with a notary seal visible.",
            "Loan signing agent in Fresno helping a homeowner complete real estate closing documents"),

        checklist_sec("Documents We Handle",
            ["Bank Documents","Travel Documents","Power of Attorney",
             "Real Estate Documents &amp; Forms","Legal Documents &amp; Forms","Loan Signing Agent Services"],
            "Mobile Services available upon request &ndash; Travel fees will be applied."),

        how_better_sec(
            [p("Plenty of places in Fresno can stamp a document. What sets us apart is how we treat the person holding it. You call or book online, and we tell you exactly what to bring. When you arrive, we take our time &mdash; we check every page, confirm every name matches, and make sure each signature lands exactly where it belongs. One missed initial on a loan package can delay a closing by days, so we don&rsquo;t leave anything to chance."),
             p("For loan signings, we follow lender and title company instructions to the letter. Bank documents, deeds, refinance packets, powers of attorney, and legal forms all get the same careful, page-by-page review, with a clean notary journal kept on every transaction.", last=True)],
            [("clipboard-check","We tell you exactly what to bring","Usually just a valid, unexpired photo ID and your unsigned documents &mdash; no guesswork."),
             ("search","Every page, checked carefully","We confirm every name matches and every signature lands exactly where it belongs."),
             ("book-open","A clean notary journal, every time","Kept on every transaction, just as California law requires, so there&rsquo;s always a record protecting you."),
             ("language","Se habla espa&ntilde;ol","We explain every signature and stamp clearly, in the language you&rsquo;re most comfortable with.")],
            "Bilingual 'Se Habla Español' signage in the office window, or a team member greeting a Spanish-speaking family.",
            "Bilingual notary services in Fresno — se habla español at C&R Tax Services"),

        results_sec(
            [p("The moments right after a notarization are often the best part of our job. We&rsquo;ve watched a daughter breathe a sigh of relief after finalizing a power of attorney, knowing she could finally manage her mother&rsquo;s care without one more legal roadblock. We&rsquo;ve seen first-time homebuyers walk out of a loan signing and tell us it was the first time in the entire process someone actually explained what they were signing."),
             p("Clients across the Fresno area tell us the same things they say about our tax work: that we&rsquo;re patient, that we explain everything, and that we make stressful paperwork feel simple. When you leave our office, your documents are done right, and you know exactly what you signed.", last=True)]),

        trust_sec(
            [p("C&amp;R Tax Services is proudly local. We serve families and business owners across Fresno, Clovis, Sanger, Selma, and Madera, and we&rsquo;re not a pop-up kiosk or an out-of-town chain. We&rsquo;re your neighbors, and our office stays open year-round &mdash; notary needs don&rsquo;t follow a calendar."),
             p("Every notarization we perform is backed by an active California notary commission and the state-required bond. Our loan signing work follows the strict standards that title companies and lenders expect, and the trust we&rsquo;ve earned as a Fresno tax preparation office means your documents and privacy are always in careful hands.", last=True)],
            "Exterior shot of the C&R Tax Services office with clear signage, or a framed California notary commission certificate.",
            "C&R Tax Services office in Fresno offering licensed notary public services to the Central Valley"),

        final_cta_sec(
            "Deadlines Don&rsquo;t Wait &mdash; Let&rsquo;s Get It Signed, Sealed, and Off Your Plate",
            "Whether it&rsquo;s a loan closing on the calendar, a power of attorney your family needs this week, or travel documents that must be certified before a flight, the fastest way to stop worrying is to get it done right, the first time. Call C&amp;R Tax Services today, or stop by and let&rsquo;s get it handled. Tell us what documents you have, and we&rsquo;ll tell you exactly what to bring. Se habla espa&ntilde;ol.",
            "Book Your Appointment", "tel:5599627503",
            "Ask About Mobile Service", "#contact",
            "Warm photo of a team member on the phone, or a 'Book Your Appointment' graphic with the office phone number.",
            "Schedule a notary appointment in Fresno with C&R Tax Services — call or book online today"),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# LIVESCAN PAGE (post 30)
# ══════════════════════════════════════════════════════════════════════════════
def build_livescan():
    return [
        hero_sec("fingerprint", "Walk-Ins Welcome",
            "Full Service Fingerprints in Fresno &mdash; Fast, Certified, and Stress-Free",
            "Livescan submissions, background checks, and FD-258 ink cards &mdash; all under one roof, done right the first time.",
            "Schedule Your Appointment", "tel:5599627503",
            "Walk In Today", "#contact"),

        intro_sec(
            [p("So you just found out you need fingerprints. Maybe it&rsquo;s for a new job, a license, or a certification. The deadline is close, and you&rsquo;re not sure where to go. Some places make you wait days for an appointment. Others rush you through the door and leave you wondering if it was even done right. When your career is on the line, guessing isn&rsquo;t good enough."),
             p("At C&amp;R Tax Services, we make Fresno Livescan fingerprinting simple. We offer full service fingerprints under one roof: digital Livescan submissions, Livescan background checks, and traditional FD-258 ink cards. Walk in with your form, and walk out knowing the job was done right the first time."),
             p("We&rsquo;re a local Fresno firm, not a pop-up kiosk. Our team is trained and certified to capture and submit prints that meet California Department of Justice and FBI standards. And because Fresno is a community of many voices, <strong>se habla espa&ntilde;ol</strong>. You can ask every question in the language you&rsquo;re most comfortable with.", last=True)],
            "Friendly technician guiding a client's hand on a digital Livescan scanner.",
            "Certified technician performing Livescan fingerprints in Fresno"),

        what_solves_sec(
            [p("Fingerprinting requests almost always come with a deadline. Maybe your new employer needs a background check before your start date. Maybe you&rsquo;re applying for a teaching credential, a nursing license, a real estate license, or a childcare permit. Foster care and adoption applications, notary commissions, and security guard cards all require prints too. Whatever the reason, the state won&rsquo;t move forward until your prints are in the system."),
             p("Here&rsquo;s the tricky part: many people don&rsquo;t know which type of fingerprinting they need. California agencies usually want a digital Livescan submission, which sends your prints straight to the DOJ. But out-of-state employers and federal agencies often ask for a physical FD-258 fingerprint card instead. Show up at the wrong place with the wrong form, and you can lose a day. Sometimes a whole week."),
             p("That&rsquo;s why workers, families, and business owners across Fresno choose a provider that handles it all. As a full service fingerprints location, we take care of Livescan submissions, Livescan background checks, and FD-258 ink cards in one visit. You bring your request form, and we handle the rest. No bouncing between offices, and no wondering whether the fingerprints Fresno agencies require were submitted the right way.", last=True)],
            "Close-up of a completed FD-258 fingerprint card next to a Livescan request form.",
            "FD-258 fingerprint card and Livescan form at a Fresno fingerprinting office"),

        checklist_sec("What We Offer",
            ["Livescan Background Checks","FD-258 Fingerprint Cards"],
            "Walk-ins welcome &ndash; most visits take 15 minutes or less."),

        how_better_sec(
            [p("A lot of fingerprinting spots treat you like a number. You wait in line, get rolled through the process, and leave with a receipt and zero explanation. We do things differently. When you visit our Fresno office, a real person walks you through every step. We check your request form before we scan, so common mistakes &mdash; a wrong ORI code or a missing applicant type &mdash; get caught before they cost you a rejection."),
             p("Our equipment and process meet California DOJ standards, which means clean captures and fewer rejected prints. And if an agency ever sends a submission back for image quality, we make it right. We also keep our pricing clear and upfront, just like we do with our tax and notary services. You&rsquo;ll know exactly what your visit costs before we ever touch the scanner.", last=True)],
            [("file-alt","We check your form first","A wrong ORI code or missing applicant type gets caught before it costs you a rejection."),
             ("shield-alt","DOJ-standard equipment","Clean captures and fewer rejected prints &mdash; and if an agency ever sends one back, we make it right."),
             ("tag","Clear, upfront pricing","You&rsquo;ll know exactly what your visit costs before we ever touch the scanner."),
             ("language","Se habla espa&ntilde;ol","We explain the process, the forms, and the results in plain language &mdash; English or Spanish.")],
            "Bilingual staff member at the front desk with 'Se Habla Español' signage visible.",
            "Bilingual fingerprinting service in Fresno with Spanish-speaking staff"),

        results_sec(
            [p("Clients tell us the best part of working with our team is how patient and clear we are. One local client came in stressed. She had a job offer that hinged on a background check, and the deadline was days away. We reviewed her Livescan form, caught an error in the agency code, fixed it, and submitted her prints the same day. She started her new job on time &mdash; and told us she wished she&rsquo;d come to us first."),
             p("That&rsquo;s the outcome we aim for every single time: peace of mind. Whether it&rsquo;s a nurse renewing a license, a new notary getting commissioned, or a parent completing a foster care application, our clients leave knowing their fingerprints were captured correctly and sent where they need to go. No re-dos, no lost time, no surprises.", last=True)]),

        trust_sec(
            [p("C&amp;R Tax Services is a Fresno-based firm serving families and business owners across the Central Valley, including Clovis, Sanger, Selma, and Madera. Unlike seasonal offices that vanish after tax season, we&rsquo;re open year-round. So when your employer or licensing board says &ldquo;we need your prints this week,&rdquo; we&rsquo;re here."),
             p("Every fingerprinting service is performed by trained, certified technicians, and every Livescan submission follows California DOJ requirements. We&rsquo;re the same trusted local team that handles tax preparation, notary public services, and loan signings for our community. That means we already live and breathe official documents, compliance, and deadlines. Your paperwork is in careful, experienced hands.", last=True)],
            "Exterior shot of the Fresno office with signage, or a map graphic of Central Valley service areas.",
            "C&R Tax Services Fresno office offering Livescan fingerprinting"),

        final_cta_sec(
            "Don&rsquo;t Let Fingerprinting Hold Up Your Job, License, or Certification",
            "Rejected prints and wrong forms can set your plans back by weeks, and almost all of those delays are avoidable. Call us, stop by our Fresno office, or schedule your appointment today. Walk-ins are welcome &mdash; just bring your request form and a valid photo ID, and we&rsquo;ll take care of the rest, in English or in Spanish. <strong>&iexcl;Se habla espa&ntilde;ol! Ll&aacute;menos hoy.</strong>",
            "Schedule Your Appointment", "tel:5599627503",
            "Walk In Today", "#contact",
            "Phone/CTA graphic with 'Walk-Ins Welcome' and an appointment button.",
            "Schedule Livescan fingerprints in Fresno — walk-ins welcome"),
    ]


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    print("=== Notary & Livescan Pages — v6 Rebuild ===\n")

    print("1. Notary page (post 29)...")
    sections = build_notary()
    r = save_elementor(29, sections)
    print(f"   Saved: {r}")

    print("2. Livescan page (post 30)...")
    sections = build_livescan()
    r = save_elementor(30, sections)
    print(f"   Saved: {r}")

    print("3. Clearing caches...")
    clear_cache()
    print("\n=== DONE ===")

if __name__ == "__main__":
    build()
