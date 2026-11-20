import json, os, re, sys, html
import importlib.util, glob
from datetime import datetime, timezone
from rates import validate_rates, flight_context, hotel_context, policy_text, source_text

M = {}; TRIPS = []; credits = {}
IMG = OUT = WORK = CAPTURED = ""
NOW = None
ALLOW_UNVERIFIED = False


def configure(meta, trips, image_dir, out_dir, allow_unverified=False, now=None):
    global M, TRIPS, IMG, OUT, WORK, CAPTURED, NOW, ALLOW_UNVERIFIED, credits
    NOW = now or datetime.now(timezone.utc)
    errors = validate_rates(meta, trips, NOW)
    if errors and not allow_unverified:
        raise ValueError("Rate validation failed:\n" + "\n".join(errors))
    M, TRIPS = meta, trips
    IMG, OUT = os.path.abspath(image_dir), os.path.abspath(out_dir)
    WORK = os.path.join(OUT, ".build")
    ALLOW_UNVERIFIED = allow_unverified
    CAPTURED = "UNVERIFIED SAMPLE" if allow_unverified else "Within 24h; see quote sources"
    credits = {}
    for path in sorted(glob.glob(os.path.join(IMG, "credits*.json"))):
        with open(path) as f:
            credits.update(json.load(f))


def rate_source(record):
    return "UNVERIFIED SAMPLE — re-search before booking" if ALLOW_UNVERIFIED else source_text(record["rate"])


def cancellation(record, context):
    return policy_text(record, record["price"], context, NOW)

e = html.escape

def inr(n):
    s = str(int(n)); last3 = s[-3:]; rest = s[:-3]
    parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return "₹" + (",".join(parts + [last3]) if parts else last3)

def strip(s):
    s = html.unescape(html.unescape(s or ""))
    s = re.sub(r"<[^>]*>?", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:60]

def img(name): return "file://" + os.path.join(IMG, name)

ICON = {
 "hotel": '<svg viewBox="0 0 24 24"><path d="M3 21V4h11v4h7v13h-7v-4h-4v4H3zm2-2h3v-4h8v4h3v-9h-7V6H5v13zm2-9h2v2H7zm4 0h2v2h-2zM7 7h2v2H7zm4 0h2v2h-2z"/></svg>',
 "walk": '<svg viewBox="0 0 24 24"><path d="M13.5 5.5a2 2 0 100-4 2 2 0 000 4zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7"/></svg>',
 "car": '<svg viewBox="0 0 24 24"><path d="M18.9 6c-.2-.6-.8-1-1.4-1h-11c-.7 0-1.2.4-1.4 1L3 12v8a1 1 0 001 1h1a1 1 0 001-1v-1h12v1a1 1 0 001 1h1a1 1 0 001-1v-8l-2.1-6zM6.5 16a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm11 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3zM5 11l1.5-4.5h11L19 11H5z"/></svg>',
 "plane": '<svg viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 00-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>',
 "snow": '<svg viewBox="0 0 24 24"><path d="M22 11h-4.2l3.2-3.2-1.4-1.4L15 11h-2V9l4.6-4.6-1.4-1.4L13 6.2V2h-2v4.2L7.8 3 6.4 4.4 11 9v2H9L4.4 6.4 3 7.8 6.2 11H2v2h4.2L3 16.2l1.4 1.4L9 13h2v2l-4.6 4.6L7.8 21l3.2-3.2V22h2v-4.2l3.2 3.2 1.4-1.4L13 15v-2h2l4.6 4.6 1.4-1.4-3.2-3.2H22z"/></svg>',
 "para": '<svg viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 5.6 2 9h2l7 9v2h2v-2l7-9h2c0-3.4-4.5-7-10-7zm-1 13.3L5.6 9H11v6.3zm2 0V9h5.4L13 15.3z"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24"><path d="M12 2L5 12h3l-4 6h7v4h2v-4h7l-4-6h3z"/></svg>',
 "meal": '<svg viewBox="0 0 24 24"><path d="M11 9H9V2H7v7H5V2H3v7c0 2.1 1.7 3.8 3.8 4V22h2.5v-9c2-.1 3.7-1.9 3.7-4V2h-2v7zm5-3v8h2.5v8H21V2c-2.8 0-5 2.2-5 4z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"/></svg>',
 "out": '<svg viewBox="0 0 24 24"><path d="M10 17l1.4-1.4L8.8 13H20v-2H8.8l2.6-2.6L10 7l-5 5 5 5zM4 5h8V3H4a2 2 0 00-2 2v14a2 2 0 002 2h8v-2H4V5z"/></svg>',
}
def ic(n, cls="ic"): return f'<span class="{cls}">{ICON[n]}</span>'

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;0,900;1,400&display=swap');
:root{--blue:#008cff;--blue-d:#0a6fd6;--ink:#1a1a1a;--mute:#6b6b6b;--line:#e3e3e3;--sky:#eaf5ff;--sky2:#f2f8ff;--salmon:#eab2a2;--salmon-l:#fdeee8;--grey:#efefef;--green:#1a9c5b;--red:#d9452b}
@page{size:A4;margin:12mm 0 14mm}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:Lato,'Helvetica Neue',Arial,sans-serif;font-size:10.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;min-height:270mm;padding:3mm 15mm 0;position:relative;overflow:hidden;page-break-after:always}
.page:last-child{page-break-after:auto}
.flow{width:210mm;padding:3mm 15mm 0;position:relative}
.blob{position:absolute;border-radius:50%;background:var(--sky);z-index:0}
.z{position:relative;z-index:1}
h1,h2,h3,h4{margin:0;font-weight:900}
.sec{color:var(--blue);font-weight:700;font-size:17pt;margin-bottom:5mm}
.brand{position:absolute;right:15mm;top:2mm;z-index:2;text-align:right;font-size:8pt;color:var(--mute);line-height:1.3}
.brand b{display:block;font-size:13pt;color:var(--ink);letter-spacing:.2px}
.brand b i{font-style:normal;color:#fff;background:var(--red);border-radius:4px;padding:0 4px;margin:0 1px}
.cov-t1{font-size:19pt;font-weight:700}.cov-t1 span{font-weight:300}
.cov-t2{font-size:38pt;font-weight:900;color:#3b82c4;line-height:1.05;margin:1mm 0 3mm}
.tags{display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:9pt}
.tag{background:#dcdcdc;border-radius:10px;padding:2px 8px;font-weight:700;color:#555}
.tag.dark{background:#222;color:#fff}
.sub{color:#555;font-size:9.5pt;margin-top:2mm}
.quote{font-style:italic;color:#555;font-size:9.5pt;line-height:1.5;margin:4mm 0 0;padding-left:0}
.quote:before{content:"\201C";display:block;font-size:30pt;color:#3b82c4;line-height:.6;font-style:normal;font-weight:900;margin-bottom:2mm}
.hero{display:grid;grid-template-columns:2fr 1fr;grid-template-rows:31mm 31mm;gap:2.5mm;margin-top:5mm;border-radius:10px;overflow:hidden}
.hero div{background-size:cover;background-position:center}
.hero .a{grid-row:1/3}
.cols{display:flex;gap:6mm;margin-top:6mm}
.contents{flex:0 0 52mm}
.contents h4{font-size:11pt;margin-bottom:3mm}
.contents ol{list-style:none;margin:0;padding:0}
.contents li{display:flex;gap:7px;align-items:flex-start;color:var(--blue);font-size:9pt;font-weight:700;margin-bottom:2.6mm}
.contents li b{background:var(--grey);color:#444;border-radius:50%;width:15px;height:15px;font-size:8pt;display:inline-flex;align-items:center;justify-content:center;flex:0 0 15px}
.card{background:var(--sky);border-radius:10px;padding:5mm 6mm}
.card small{display:block;color:var(--mute);font-size:8pt;font-style:italic}
.card .big{font-size:14pt;font-weight:900;line-height:1.15;margin:1mm 0 2mm}
.kv{display:grid;grid-template-columns:auto 1fr;gap:1.4mm 4mm;font-size:8.6pt;color:#444}
.kv span{color:var(--mute)}
.hl{margin-top:6mm}.hl h4{font-size:11pt;margin-bottom:3mm}
.chips{display:flex;flex-wrap:wrap;gap:3mm}
.chip{border:1px solid var(--line);border-radius:6px;padding:2mm 3.5mm;font-size:8.5pt;font-weight:700;display:flex;align-items:center;gap:6px}
.ic{display:inline-flex;width:14px;height:14px;flex:0 0 14px}.ic svg{width:100%;height:100%;fill:#444}
.banner{margin-top:6mm;background:linear-gradient(90deg,#b8e3ea,#9fd3df);border-radius:8px;padding:4mm 6mm;display:flex;justify-content:space-between;align-items:center}
.banner b{font-size:11.5pt;color:#1b3a5b}.banner small{display:block;font-style:italic;font-size:8pt;color:#33536f;margin-top:1mm}
.banner .btn{background:#fff;color:var(--blue);border-radius:20px;padding:2.5mm 6mm;font-weight:900;font-size:8.5pt;text-align:center;line-height:1.2}
.total{margin-top:5mm;background:var(--sky);border-radius:10px;padding:5mm 6mm;display:flex;justify-content:space-between;align-items:center}
.total h3{font-size:13pt;font-weight:700}.total p{margin:1.5mm 0 0;color:var(--mute);font-size:8.5pt;max-width:110mm;line-height:1.4}
.total .amt{font-size:20pt;font-weight:900;color:var(--blue);text-align:right}.total .amt small{display:block;font-size:8pt;color:var(--mute);font-weight:400}
.pill{display:inline-block;border-radius:10px;padding:1px 8px;font-size:8pt;font-weight:900;margin-top:1.5mm}
.pill.ok{background:#e3f6ec;color:var(--green)}.pill.over{background:#fde8e3;color:var(--red)}
/* itinerary summary */
.summ{border:1px solid var(--line);border-radius:4px;overflow:hidden}
.summ .city{background:var(--salmon);font-weight:700;font-size:9.5pt;padding:2mm 4mm;display:flex;gap:6px;align-items:center}
.summ .city .ic svg{fill:#7a3b2a}
.summ .row{display:grid;grid-template-columns:36mm 1fr;border-top:1px solid var(--line)}
.summ .row .d{padding:2.5mm 3mm;font-size:8.6pt;color:#444;text-align:center;border-right:1px solid var(--line)}
.summ .row .ev{padding:0}
.summ .row .ev div{display:flex;gap:6px;padding:1.8mm 3mm;font-size:8.4pt;border-bottom:1px solid #f1f1f1;line-height:1.35}
.summ .row .ev div:last-child{border-bottom:0}
.lead{display:flex;gap:6px;align-items:center;color:#444;font-size:8.6pt;margin:2mm 0 3mm}
/* flights */
.fl{display:flex;gap:5mm}
.fcard{flex:1;border:1px solid var(--line);border-radius:10px;padding:4mm 5mm}
.fcard .top{display:flex;justify-content:space-between;font-size:8.5pt;color:var(--mute)}
.al{display:inline-flex;align-items:center;gap:6px;font-weight:900;color:var(--ink);font-size:10pt}
.al i{font-style:normal;color:#fff;border-radius:4px;padding:1px 5px;font-size:8pt}
.tl{display:flex;align-items:center;justify-content:space-between;margin:4mm 0 2mm}
.tl .t{font-size:17pt;font-weight:900}.tl .c{font-size:8.5pt;color:var(--mute)}
.tl .mid{flex:1;text-align:center;font-size:8pt;color:var(--mute);margin:0 3mm}
.tl .mid hr{border:0;border-top:1.5px dashed #bbb;margin:1mm 0}
table.t{width:100%;border-collapse:collapse;font-size:8.4pt}
table.t th{text-align:left;background:var(--sky);font-weight:700;padding:2mm 2.5mm;border-bottom:1px solid #cfe3f7}
table.t td{padding:2.2mm 2.5mm;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.35}
table.t td.n,table.t th.n{text-align:right;white-space:nowrap}
table.t tr.rec td{background:#f6fbff}
.src{font-size:7.8pt;color:var(--mute);margin-top:2mm;line-height:1.4}
/* day wise */
.dayh{display:flex;justify-content:space-between;align-items:baseline;margin:7mm 0 3mm;break-after:avoid}
.dayh h2{font-size:22pt}.dayh span{font-size:15pt;color:#333}
.tline{border-left:1.5px solid #dfe8f2;margin-left:2mm;padding-left:6mm}
.item{position:relative;margin-bottom:5mm;break-inside:avoid}
.item:before{content:"";position:absolute;left:-8.1mm;top:1.5mm;width:7px;height:7px;border-radius:50%;background:#fff;border:1.5px solid #bcd3ea}
.kicker{font-size:8.5pt;color:#555;display:flex;gap:6px;align-items:center;letter-spacing:.3px;text-transform:uppercase;margin-bottom:2mm}
.media{display:flex;gap:5mm}
.media .ph{width:44mm;height:32mm;border-radius:6px;background-size:cover;background-position:center;flex:0 0 44mm}
.media .tx h3{font-size:12.5pt;line-height:1.25;margin-bottom:1.5mm}
.media .tx p{margin:0;font-size:8.8pt;color:#444;line-height:1.5}
.box{background:var(--grey);border-radius:6px;padding:3mm 4.5mm;margin-top:3mm;font-size:8.6pt;line-height:1.55}
.box b{display:block;margin-bottom:1mm}
.tip{background:#fff7e0;border-radius:6px;padding:2.5mm 4mm;margin-top:2.5mm;font-size:8.4pt;color:#5a4a1a}
.stay{display:inline-flex;align-items:center;gap:5px;background:var(--sky2);border:1px solid #dbe9f7;border-radius:16px;padding:1.5mm 4mm;font-size:8.8pt;font-weight:700;margin-bottom:3mm}
.stay .ic svg{fill:#3b6fa8}
.hcard .ph{width:50mm;height:36mm}
.badge{display:inline-block;font-size:7.5pt;font-weight:900;color:#fff;border-radius:3px;padding:1px 5px;margin-right:3px}
.b-h{background:#5b3fd6}.b-s{background:#22a06b}
.stars{color:#f3a712;font-size:9pt;letter-spacing:1px}
.hmeta{display:grid;grid-template-columns:1fr 1fr;gap:1mm 6mm;margin-top:2mm;font-size:8.3pt;color:var(--mute)}
.hmeta b{display:block;color:var(--ink);font-weight:700}
.room{background:var(--grey);border-radius:6px;padding:4mm 5mm;margin-top:3mm}
.room h4{font-size:10.5pt;margin-bottom:2.5mm}
.room .grid{background:#fff;border:1px solid var(--line);border-radius:4px;display:grid;grid-template-columns:1.6fr .9fr 1fr;gap:3mm;padding:2.5mm 4mm;font-size:8.3pt}
.room .grid span{display:block;color:var(--mute);font-size:7.6pt}
.room ul{margin:2.5mm 0 0;padding:0;list-style:none;columns:2;font-size:8.3pt}
.room li{margin-bottom:1mm}.room li:before{content:"\2714  ";color:#555}
.room .pol{margin-top:2mm;font-size:8pt;color:#444}
.hnote{font-size:8pt;color:#7a5b00;margin-top:2mm}
.leisure{background:var(--salmon-l);border-radius:6px;padding:3.5mm 5mm}
.leisure b{font-size:10.5pt}.leisure p{margin:1mm 0 0;font-size:8.8pt;font-style:italic;color:#444}
.co{display:flex;gap:6px;align-items:center;font-size:9pt}
.fmini{border:1px solid var(--line);border-radius:8px;padding:3mm 4mm;display:flex;align-items:center;gap:5mm;font-size:9pt}
.fmini .t{font-weight:900;font-size:12pt}
/* cost */
.meter{margin:5mm 0 2mm;position:relative;height:9mm}
.meter .bar{position:absolute;left:0;right:0;top:3mm;height:3mm;border-radius:3mm;background:linear-gradient(90deg,#b9e8cf,#fbe6a6 70%,#f7c2b4)}
.meter .band{position:absolute;top:2mm;height:5mm;border:1.5px solid var(--green);border-radius:3mm;background:rgba(26,156,91,.12)}
.meter .mk{position:absolute;top:0;width:2px;height:9mm;background:var(--ink)}
.meter .lb{position:absolute;top:9.5mm;font-size:7.6pt;color:var(--mute);transform:translateX(-50%);white-space:nowrap}
.meter .lb.me{color:var(--ink);font-weight:900}
.imp{background:var(--salmon-l);border-radius:8px;padding:5mm 6mm;margin-top:5mm}
.imp .hd{display:inline-block;background:#f05a41;color:#fff;border-radius:10px;padding:1px 9px;font-size:8pt;font-weight:700;margin-bottom:3mm}
.imp ul{margin:0;padding-left:5mm;font-size:8.8pt;line-height:1.6}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:3mm}
.steps div{background:var(--sky2);border-radius:8px;padding:4mm;font-size:8.5pt;line-height:1.45}
.steps b{display:block;color:var(--blue);font-size:10pt;margin-bottom:1mm}
.disc{background:var(--sky);border-radius:8px;padding:5mm 6mm;font-size:8pt;color:#444;line-height:1.5;margin-top:5mm}
.cred{font-size:6.8pt;color:var(--mute);line-height:1.45;margin-top:4mm;columns:2;column-gap:6mm}
.nobr{break-inside:avoid}
.src,.pol,.imp li{overflow-wrap:anywhere}
"""

def brand():
    return f'<div class="brand"><b>Holiday<i>Plan</i></b>{e(M["theme"])}</div>'

def blobs(spec):
    return "".join(f'<div class="blob" style="{s}"></div>' for s in spec)

def flight_card(f, date, label):
    col = {"QP": "#ff6d38", "6E": "#1b2b8f", "SG": "#e0262d", "9I": "#c8102e", "AI": "#c8102e"}.get(f["code"], "#555")
    return f'''<div class="fcard"><div class="top"><span>{label}</span><span>{date}</span></div>
<div style="margin-top:2mm" class="al"><i style="background:{col}">{f["code"]}</i>{f["airline"]} • {f["code"]} {f["num"]}</div>
<div class="tl"><div><div class="t">{f["dep"]}</div><div class="c">{f["frm"]}</div></div>
<div class="mid">{f["dur"]}<hr>{f["stops"]}</div>
<div style="text-align:right"><div class="t">{f["arr"]}</div><div class="c">{f["to"]}</div></div></div>
<div class="c" style="font-size:8pt;color:var(--mute)">Economy • {M["pax"]} • Baggage as per airline fare family</div></div>'''

def stars(n):
    return '<span class="stars">' + "★" * n + '<span style="color:#ccc">' + "★" * (5 - n) + "</span></span>" if n else ""

def hotel_block(h):
    t = f'''<div class="item"><div class="stay">{ic("pin")}{e(h["area"])} - {h["nights"]} Night{"s" if h["nights"]>1 else ""} Stay</div>
<div class="kicker" style="text-transform:none;letter-spacing:0;font-size:9.5pt">{e(h["type"])} at {e(h["area"])}</div>
<div class="media hcard"><div class="ph" style="background-image:url('{img(h["img"])}')"></div>
<div class="tx"><span class="badge b-h">{e(h["type"])}</span><span class="badge b-s">{h["score"]}/10</span>
<h3 style="margin-top:1.5mm">{e(h["name"])} {stars(h.get("stars",0))}</h3>
<p style="font-size:8.3pt;color:#555">{e(h["area"])}<br>{e(h["near"])}<br><b style="color:var(--ink)">{h["word"]}</b> • {h["reviews"]} Booking.com reviews</p>
<div class="hmeta"><div>Check In:<b>{e(h["cin"])}</b></div><div>Check Out:<b>{e(h["cout"])}</b></div></div></div></div>
<div class="room"><h4>{e(h["room"])}</h4>
<div class="grid"><div><span>Meal Plan</span>{e(h["meal"])}</div><div><span>Bed Type</span>{e(h["bed"])}</div><div><span>Quoted rate ({h["nights"]}N, incl. taxes)</span><b>{inr(h["price"])}</b></div></div>
<div style="font-size:8.3pt;font-weight:700;margin-top:3mm">Room Inclusions:</div>
<ul>{"".join(f"<li>{e(x)}</li>" for x in h["incl"])}</ul>
<div class="src">{e(rate_source(h))}</div>
<div class="pol"><b>Policy:</b> {e(cancellation(h, hotel_context(M, h)))}</div>
{f'<div class="hnote">{e(h["note"])}</div>' if h.get("note") else ""}</div></div>'''
    return t

def media_item(kind, d):
    kk = {"transfer": ("car", "TRANSFER"), "activity": ("walk", "ACTIVITY")}[kind]
    meta = f'{kk[1]} • {e(d["dur"])}' + (f' • In {e(d["where"])}' if d.get("where") else "") + (f' • {e(d["kind"])}' if d.get("kind") else "")
    ph = f'<div class="ph" style="background-image:url(\'{img(d["img"])}\')"></div>' if d.get("img") else ""
    incl = d.get("incl") or []
    box = f'<div class="box"><b>Inclusions/Exclusions:</b>{"<br>".join(e(x) for x in incl)}</div>' if incl else ""
    tip = f'<div class="tip"><b>Tip:</b> {e(d["tip"])}</div>' if d.get("tip") else ""
    return f'''<div class="item"><div class="kicker">{ic(kk[0])}{meta}</div>
<div class="media">{ph}<div class="tx"><h3>{e(d["title"])}</h3><p>{e(d["text"])}</p></div></div>{box}{tip}</div>'''

def build(T):
    fl = T["flights"]
    total = sum(c[2] for c in T["costs"])
    BL, BH = M["budget_lo"], M["budget_hi"]
    status = (f'<span class="pill over">{inr(total-BH)} above the {inr(BH)} ceiling</span>' if total > BH * 1.02
              else f'<span class="pill ok">Within budget range</span>' if total <= BH
              else f'<span class="pill ok">At the top of your range (+{inr(total-BH)})</span>')
    nights = sum(n for _, n in T["cities"])
    names = [n.strip() for n in (M.get("names") or []) if n.strip()]
    who = (" & ".join(names) if len(names) <= 2 else ", ".join(names[:-1]) + " & " + names[-1]) if names else M.get("prepared_for", "You")
    cover_who = f'{e(" & ".join(names))}\'s <span>trip to</span>' if 1 <= len(names) <= 2 else 'Your <span>trip to</span>'
    guests_row = f'<span>Guests</span><b>{e(", ".join(names))}</b>' if names else ""
    P = []
    # ---------- COVER
    P.append(f'''<section class="page">{blobs(["width:70mm;height:70mm;right:-12mm;top:-28mm"])}{brand()}<div class="z">
<div class="cov-t1">{cover_who}</div><div class="cov-t2">{e(T["title"])}</div>
<div class="tags"><span class="tag">{M["duration"]}</span><span class="tag dark">↔</span><b>Customizable</b><b style="font-size:11pt">{e(M["theme"])}</b></div>
<div class="sub">{e(T["subtitle"])} • {M["dates_short"]} • From {e(M["origin_city"])} • {M["pax"]}</div>
<div class="hero"><div class="a" style="background-image:url('{img(T["hero"])}')"></div><div style="background-image:url('{img(T["hero2"])}')"></div><div style="background-image:url('{img(T["hero3"])}')"></div></div>
<p class="quote">{e(T["blurb"])}</p>
<div class="cols"><div class="contents"><h4>Contents</h4><ol>
<li><b>1</b>Your Itinerary</li><li><b>2</b>Flight Details (quoted fares)</li><li><b>3</b>Day Wise Details</li><li><b>4</b>Cost Breakdown</li><li><b>5</b>Important Information &amp; How to Book</li></ol></div>
<div class="card" style="flex:1"><small>Prepared for</small><div class="big">{e(who)}</div>
<div class="kv"><span>Travel dates</span><b>{M["dates_long"]}</b><span>Travellers</span><b>{M["pax"]}, {M["rooms"]}</b>{guests_row}<span>Flights</span><b>{e(M["origin_short"])} ⇄ {e(fl["airport"])}</b><span>Rates captured</span><b>{CAPTURED}</b><span>Weather</span><span style="color:#444">{e(T["weather"])}</span></div></div></div>
<div class="hl"><h4>Highlights</h4><div class="chips">{"".join(f'<div class="chip">{ic(i)}{e(t)}</div>' for i,t in T["highlights"])}<div class="chip">{ic("meal")}Meals budgeted</div></div></div>
<div class="total"><div><h3>Estimated total for {M["pax"].lower()}</h3><p>{"UNVERIFIED SAMPLE prices; re-search flights and stays before booking." if ALLOW_UNVERIFIED else "Flights and stays are sourced quotes captured within 24 hours; other costs are estimates."} Prices change until booked.</p>{status}</div>
<div class="amt">{inr(total)}<small>For {M["pax"]} • all-in</small></div></div>
</div></section>''')

    # ---------- ITINERARY SUMMARY
    rows = []
    day_city = {}
    for di, D in enumerate(T["days"], 1):
        ev = []
        for k, v in D["items"]:
            if k == "flight":
                f = fl["out"] if di == 1 else fl["ret"]
                ev.append(("plane", f'Flight {f["code"]} {f["num"]} {f["frm"]} {f["dep"]} → {f["to"]} {f["arr"]} ({e(f["airline"])})'))
            elif k == "hotel":
                h = T["hotels"][v]; ev.append(("hotel", f'Check in to <b>{e(h["name"])}</b>, {e(h["room"])}'))
            elif k == "checkout":
                ev.append(("out", f'Checkout from {e(v)}'))
            elif k == "transfer":
                ev.append(("car", f'{e(v["title"])} – {e(v["kind"])} ({e(v["dur"])})'))
            elif k == "activity":
                ev.append(("walk", e(v["title"])))
            elif k == "note":
                ev.append(("walk", f'{e(v[0])}: {e(v[1])}'))
        ev.append(("meal", "Day Meals: budgeted (local cafés / homestay kitchen)"))
        day_city.setdefault(D["city"], []).append((di, D, ev))
    for city, n in T["cities"]:
        rows.append(f'<div class="city">{ic("pin")}{e(city)} - {n} Night{"s" if n>1 else ""} Stay</div>')
        for di, D, ev in day_city.get(city, []):
            rows.append(f'<div class="row"><div class="d">{e(D["date"][:3])}, {e(D["date"][5:11])}, Day {di}</div><div class="ev">' +
                        "".join(f'<div>{ic(i)}<span>{t}</span></div>' for i, t in ev) + "</div></div>")
    P.append(f'''<section class="flow">{blobs(["width:46mm;height:30mm;left:-14mm;top:0;border-radius:0 0 50% 50%"])}<div class="z">
<div class="sec">Your Itinerary</div><h1 style="font-size:22pt;margin-bottom:3mm">{e(M["theme"])}</h1>
<div class="lead">{ic("plane")}{e(M["origin_short"])} to {e(fl["airport"])} • {nights} nights • {len(T["cities"])} destinations</div>
<div class="summ">{"".join(rows)}</div></div></section>''')

    # ---------- FLIGHTS
    opt_rows = "".join(
        f'<tr class="{"rec" if i==0 else ""}"><td><b>{e(o[0])}</b><br><span style="color:var(--mute)">{e(o[4])}</span></td><td>{e(o[1])}</td><td>{e(o[2])}</td><td class="n"><b>{inr(o[3])}</b></td></tr>'
        for i, o in enumerate(fl["options"]))
    option_sources = "".join(f'<div class="src">Option {i+1}: {e("UNVERIFIED SAMPLE" if ALLOW_UNVERIFIED else source_text(o[5]))}</div>' for i, o in enumerate(fl["options"]))
    P.append(f'''<section class="flow" style="page-break-before:always">{blobs(["width:46mm;height:30mm;left:-14mm;top:0;border-radius:0 0 50% 50%"])}<div class="z">
<div class="sec">Flight Details</div>
<div class="fl">{flight_card(fl["out"], fl["out_date"], "ONWARD • Day 1")}{flight_card(fl["ret"], fl["ret_date"], f"RETURN • Day {len(T['days'])}")}</div>
<div class="total" style="margin-top:4mm"><div><h3>Selected round trip</h3><p>Selected fares from {e("illustrative sample data" if ALLOW_UNVERIFIED else fl["rate"]["source"])}. Book both legs the same day; fares on these routes move several times a day this close to departure.</p></div><div class="amt">{inr(fl["price"])}<small>{M["pax"]} • round trip • economy</small></div></div>
<h3 style="font-size:12pt;margin:7mm 0 3mm">Quoted round-trip options (prices for {M["pax"].lower()})</h3>
<table class="t"><tr><th style="width:30mm">Option</th><th>Onward • {M["out_hdr"]}</th><th>Return • {M["ret_hdr"]}</th><th class="n">Total</th></tr>{opt_rows}</table>{option_sources}
<div class="src">Selected quote: {e(rate_source(fl))}. Times are local to the airports. Alternative fares have their own sources above. Cancellation/change terms vary by fare; see Important Information.</div>
</div></section>''')

    # ---------- DAY WISE
    body = []
    for di, D in enumerate(T["days"], 1):
        body.append(f'<div class="dayh"><h2>Day {di}</h2><span>{e(D["date"])}</span></div><div class="tline">')
        for k, v in D["items"]:
            if k == "flight":
                f = fl["out"] if di == 1 else fl["ret"]
                body.append(f'<div class="item"><div class="kicker">{ic("plane")}FLIGHT • {f["dur"]} • {f["stops"]}</div><div class="fmini"><div><div class="t">{f["dep"]}</div>{f["frm"]}</div><div style="flex:1;text-align:center;color:var(--mute);font-size:8pt">{e(f["airline"])} {f["code"]} {f["num"]}<hr style="border:0;border-top:1.5px dashed #bbb;margin:1mm 0">{M["origin_city"] + " → " + e(fl["airport"]) if di==1 else e(fl["airport"]) + " → " + M["origin_city"]}</div><div style="text-align:right"><div class="t">{f["arr"]}</div>{f["to"]}</div></div></div>')
            elif k == "hotel":
                body.append(hotel_block(T["hotels"][v]))
            elif k == "checkout":
                body.append(f'<div class="item" style="break-after:avoid">{"" if False else ""}<div class="co">{ic("out")}<b>Checkout</b>&nbsp;from {e(v)}</div></div>')
            elif k in ("transfer", "activity"):
                body.append(media_item(k, v))
            elif k == "note":
                body.append(f'<div class="item"><div class="leisure"><b>{e(v[0])}</b><p>{e(v[1])}</p></div></div>')
        body.append(f'<div class="item"><div class="co">{ic("meal")}<b>Day Meals</b>&nbsp;Breakfast, lunch &amp; dinner at local cafés / homestay kitchen (budgeted)</div></div></div>')
    P.append(f'''<section class="flow" style="page-break-before:always">{blobs(["width:46mm;height:30mm;left:-14mm;top:0;border-radius:0 0 50% 50%"])}<div class="z"><div class="sec">Day Wise Details</div>{"".join(body)}</div></section>''')

    # ---------- COST
    lo, hi = int(BL * 0.875), max(int(BH * 1.32), total + int(BH * 0.08))
    pos = lambda v: (v - lo) / (hi - lo) * 100
    crow = "".join(f'<tr><td>{e(c[0])}</td><td>{e(c[1])}</td><td style="color:var(--mute)">{e(("UNVERIFIED SAMPLE" if ALLOW_UNVERIFIED else "Sourced quote (see details)") if c[0] in ("Flights", "Stay") else c[3])}</td><td class="n">{inr(c[2])}</td></tr>' for c in T["costs"])
    sub = {}
    for c in T["costs"]:
        g = {"Flights": "Flights", "Stay": "Stays"}.get(c[0], "Ground, fees & meals")
        sub[g] = sub.get(g, 0) + c[2]
    P.append(f'''<section class="flow" style="page-break-before:always">{blobs(["width:46mm;height:30mm;left:-14mm;top:0;border-radius:0 0 50% 50%"])}<div class="z">
<div class="sec">Cost Breakdown</div>
<div style="display:flex;justify-content:space-between;align-items:baseline"><h1 style="font-size:19pt">Budget for {M["pax"]}</h1><span style="font-size:19pt;font-weight:900;color:var(--blue)">{inr(total)}</span></div>
<div class="meter"><div class="bar"></div><div class="band" style="left:{pos(BL):.1f}%;width:{pos(BH)-pos(BL):.1f}%"></div><div class="mk" style="left:{min(pos(total),99.5):.1f}%"></div>
<div class="lb" style="left:{pos(BL):.1f}%">{inr(BL)}</div><div class="lb" style="left:{pos(BH):.1f}%">{inr(BH)}</div><div class="lb me" style="left:{min(pos(total),94):.1f}%;top:-4.5mm">This plan</div></div>
<div style="height:6mm"></div>
<div class="chips" style="margin-bottom:5mm">{"".join(f'<div class="chip">{e(k)}: {inr(v)} ({v*100//total}%)</div>' for k,v in sub.items())}</div>
<table class="t"><tr><th style="width:28mm">Item</th><th>Details</th><th style="width:34mm">Basis</th><th class="n">Amount</th></tr>{crow}
<tr><td colspan="3"><b>Total for {M["pax"].lower()}</b></td><td class="n"><b style="font-size:11pt;color:var(--blue)">{inr(total)}</b></td></tr></table>
<div class="total" style="margin-top:5mm;display:block"><h3 style="font-size:11.5pt">Budget check {status}</h3><p style="max-width:none">{e(T["budget_note"])}</p></div>
<div class="src">{"UNVERIFIED SAMPLE: flight/hotel prices are illustrative." if ALLOW_UNVERIFIED else "Flight/hotel quote sources and capture timestamps appear in their detail cards."} Estimates: local transport, fees and meals; confirm with operators. Not included: travel insurance, tips, shopping, optional activities.</div>
</div></section>''')

    # ---------- INFO / HOW TO BOOK
    cred = []
    for k in T["credits_keys"]:
        c = credits.get(k)
        if c: cred.append(f'{e(c["title"].replace("File:",""))} – {e(strip(c["artist"])) or "Wikimedia Commons"} ({e(c["license"])})')
    hotels = "".join(f'<li><b>{e(h["name"])}</b>: {e(cancellation(h, hotel_context(M, h)))}</li>' for h in T["hotels"].values())
    P.append(f'''<section class="flow" style="page-break-before:always">{blobs(["width:46mm;height:30mm;left:-14mm;top:0;border-radius:0 0 50% 50%"])}<div class="z">
<div class="sec">Important Information</div>
<div class="imp"><span class="hd">IMPORTANT INFORMATION</span><ul>{"".join(f"<li>{e(x)}</li>" for x in T["info"])}</ul></div>
<div class="imp" style="background:#f4f8fc"><span class="hd" style="background:var(--blue)">CANCELLATION POLICIES</span><ul>{hotels}<li><b>Flights</b>: {e(cancellation(fl, flight_context(M, fl)))}</li></ul></div>
<div class="sec" style="margin-top:8mm">How to Book</div>
<div class="steps"><div><b>1. Flights</b>Search {M["flight_source"]} for {M["origin_code"]} ⇄ {e(fl["airport"].split("(")[-1].rstrip(")"))}, {M["dates_book"]}, {M["pax"].lower()}, and pick the flights named on the Flight Details page.</div>
<div><b>2. Stays</b>Book each property on Booking.com for the exact dates shown. Choose the room type listed so the price matches.</div>
<div><b>3. Ground</b>Pre-book the Day 1 airport cab and any permit tours a day ahead; pay shared jeeps and local taxis in cash.</div></div>
<div class="disc">This is an independent itinerary in a holiday-quote layout, built for your trip on {NOW.strftime("%d %b %Y")}. It is not issued by any travel agency. {"Sample prices are unverified; research current rates before booking;" if ALLOW_UNVERIFIED else "Prices are researcher-supplied sourced quotes, not independently fetched by this builder; they change until booked;"} availability is not held. Please re-check every price, timing and policy on the booking page before paying.</div>
<div class="cred"><b>Photo credits</b> – Property photos: the hotels' own Booking.com listings. Destination photos via Wikimedia Commons: {"; ".join(cred)}.</div>
</div></section>''')
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{e(T["title"])} – {e(M["theme"])}</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>', total

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build itineraries from validated researcher-supplied quotes")
    parser.add_argument("trips")
    parser.add_argument("img_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--allow-unverified", action="store_true", help="Render illustrative samples with prominent unverified labels")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("trips", args.trips)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        configure(module.META, module.TRIPS, args.img_dir, args.out_dir, args.allow_unverified)
    except (ValueError, KeyError) as exc:
        parser.exit(2, str(exc) + "\n")
    os.makedirs(WORK, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for T in TRIPS:
            h, total = build(T)
            hp = os.path.join(WORK, "html_" + T["file"].replace(".pdf", ".html"))
            open(hp, "w").write(h)
            pg.goto("file://" + hp, wait_until="networkidle")
            pg.wait_for_timeout(500)
            pg.pdf(path=os.path.join(OUT, T["file"]), format="A4", print_background=True, prefer_css_page_size=True)
            print(T["file"], "total", total)
        b.close()
