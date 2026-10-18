"""Builds portfolio.html (editable source) and Epeke_Vuyisani_UGC_Portfolio.pdf from website/src/content.json.
Run: pip install playwright && playwright install chromium && python3 pdf/build_pdf.py"""
import json, pathlib, html
from playwright.sync_api import sync_playwright

H = pathlib.Path(__file__).parent
C = json.load(open(H.parent / 'website/src/content.json'))
e = html.escape
A = 'assets/'


def a(href, text, cls=''):
    return f'<a class="{cls}" href="{e(href)}">{e(text)}</a>'


feat = [p for p in C['projects'] if p['featured']]
mail = f"mailto:{C['email']}"
quote = mail + '?subject=Quote%20request'


def page(n, cap, body, cls=''):
    return f'<section class="pg {cls}"><div class="cap">{cap}</div>{body}<footer><span>Epeke Vuyisani · UGC Creator</span><span>{n:02d}</span></footer></section>'


strip = '<div class="strip">' + ''.join(f'<img src="{A}{p["id"]}-2.jpg">' for p in feat) + '</div>'
pages = []
pages.append(f'''<section class="pg cover"><img class="fl" src="{A}halftone-flower.png">
<div class="cap top">UGC Creator<span>Beauty</span><span>Fashion</span><span>Lifestyle</span></div>
<h1><span class="a">Epeke</span><span class="b">Vuyisani</span></h1>
<p class="lede">{e(C['tagline'])}</p><p class="role">{e(C['title'])}</p>
<div class="cover-links">{a(mail, C['email'])} · {a(C['tiktok'], C['tiktokHandle'])} · {a(C['instagram'], C['instagramHandle'])}</div>
<div class="cap bot"><span>Real faces</span><span>soft light</span><span>content</span><span>that feels like taste</span></div></section>''')
pages.append(page(2, '01 — About', f'<div class="two"><img class="por" src="{A}portrait.jpg"><div><h2>Taste, light,<br><i>honest product</i></h2><p>{e(C["about"])}</p><p class="note">A versatile creator, not a celebrity influencer: the value is in the quality and usefulness of the content made for your brand.</p></div></div>' + strip))
li = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
pages.append(page(3, '02 — Content capabilities', f'<h2>Niches &amp; <i>formats</i></h2><div class="cols"><div><h4>Niches</h4><ul>{li(C["niches"])}</ul></div><div><h4>Formats</h4><ul>{li(C["formats"])}</ul></div></div><p class="note">Work shown is creator-made concept video, not sponsored campaigns.</p>' + strip))
for i, p in enumerate(feat):
    st = ''.join(f'<img class="s{k}" src="{A}{p["id"]}-{k}.jpg">' for k in (2, 1, 3))
    link = (f'Watch: {a(p["url"], p["url"])}' if p['url'] else f'Full video: link to be added · more on {a(C["tiktok"], C["tiktokHandle"] + " (TikTok)")}')
    pages.append(page(4 + i, f'03 — Featured work {i + 1}/{len(feat)}', f'<span class="tag">{e(p["cat"])}</span><h2>{e(p["title"])}</h2><div class="stills">{st}</div><p>{e(p["desc"])}</p><p class="note">Creator concept video · {e(p["subject"])}<br>{link}</p>'))
pages.append(page(8, '04 — Creative process', '<h2>Four steps, <i>no guesswork</i></h2><ol class="steps">' + ''.join(f'<li><b>{n}</b><h3>{e(t)}</h3><p>{e(d)}</p></li>' for n, t, d in C['process']) + '</ol>'))
pages.append(page(9, '05 — Services', '<h2>What I can make <i>for you</i></h2><ul class="svc">' + ''.join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in C['services']) + f'</ul>{a(quote, "Request a Quote →", "btn")}'))
web = a(C['siteUrl'], C['siteUrl']) if C['siteUrl'] else 'Website URL: to be added after deployment'
pages.append(page(10, '06 — Contact', f'<img class="fl2" src="{A}halftone-flower.png"><h2>Let’s make<br><i>something real</i></h2><ul class="links"><li><span>Email</span>{a(mail, C["email"])}</li><li><span>Instagram</span>{a(C["instagram"], C["instagramHandle"])}</li><li><span>TikTok</span>{a(C["tiktok"], C["tiktokHandle"])}</li><li><span>WhatsApp</span>{a(C["whatsapp"], C["whatsappDisplay"])}</li><li><span>Website</span>{web}</li></ul>{a(quote, "Request a Quote →", "btn")}'))

fonts = ''.join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(assets/fonts/{fn}.woff2)}}" for fam, w, st, fn in [
    ('PF', 500, 'normal', 'playfair-display-latin-500-normal'), ('PF', 500, 'italic', 'playfair-display-latin-500-italic'),
    ('PF', 800, 'normal', 'playfair-display-latin-800-normal'), ('PF', 800, 'italic', 'playfair-display-latin-800-italic'),
    ('SM', 400, 'normal', 'space-mono-latin-400-normal'), ('SM', 700, 'normal', 'space-mono-latin-700-normal'),
    ('IN', 400, 'normal', 'inter-latin-400-normal'), ('IN', 500, 'normal', 'inter-latin-500-normal')])
css = fonts + '''
:root{--moss:#7d8c4e;--forest:#14261a;--gold:#c9a24b;--pink:#c99d9a;--choc:#3a2417;--char:#121410;--ivory:#f3ecda}
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font:10pt/1.55 IN,sans-serif;color:var(--ivory)}a{color:inherit;text-decoration:none;border-bottom:1px solid var(--gold)}
.pg{width:210mm;height:297mm;padding:20mm 18mm 18mm;position:relative;overflow:hidden;page-break-after:always;background:radial-gradient(60% 40% at 85% 10%,rgba(125,140,78,.4),transparent 70%),radial-gradient(40% 30% at 10% 95%,rgba(201,162,75,.2),transparent 70%),var(--forest)}
.pg:last-child{page-break-after:auto}
.cap{font:7.5pt SM;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:6mm}
h1{font:800 66pt/.84 PF;margin:0;letter-spacing:-.04em}h1 i{font-weight:500}
h2{font:500 30pt/1.02 PF;margin:0 0 8mm;letter-spacing:-.02em}h2 i{color:var(--gold)}h3{font:500 13pt PF;margin:2mm 0}h4{font:7.5pt SM;text-transform:uppercase;letter-spacing:.14em;color:var(--pink);margin:0 0 3mm}
footer{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;font:7pt SM;letter-spacing:.1em;text-transform:uppercase;opacity:.7;border-top:.3mm solid var(--moss);padding-top:2mm}
.cover{display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:22mm}.cover .sc{position:absolute;right:-22mm;top:22mm;width:150mm}.cover .lg{position:absolute;left:12mm;top:14mm;width:46mm}
.lede{font:italic 500 15pt/1.3 PF;max-width:110mm;margin:8mm 0 3mm}.role{font:8pt SM;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0}.cover-links{margin-top:8mm;font:8pt SM}
.two{display:grid;grid-template-columns:76mm 1fr;gap:10mm}.two p{font-size:11pt}.por{width:76mm;height:104mm;object-fit:cover;border:.3mm solid var(--gold)}
.note{font:7.5pt SM;color:var(--pink);margin-top:6mm}.cols{display:grid;grid-template-columns:1fr 1fr;gap:12mm}ul{list-style:none;padding:0;margin:0}
.cols li{padding:2.6mm 0;border-bottom:.3mm solid var(--moss);font:500 11pt PF}
.tag{font:7pt SM;text-transform:uppercase;letter-spacing:.12em;background:var(--gold);color:var(--char);padding:1mm 3mm}.tag+h2{margin-top:5mm}
.stills{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-bottom:6mm}.stills img{width:100%;aspect-ratio:9/16;object-fit:cover;border:.3mm solid var(--gold)}
.steps{list-style:none;padding:0;display:grid;gap:7mm}.steps li{display:grid;grid-template-columns:22mm 1fr;border-top:.3mm solid var(--moss);padding-top:4mm}.steps b{font:800 34pt/1 PF;color:var(--gold);grid-row:span 2}.steps p{margin:0}
.svc{display:grid;grid-template-columns:1fr 1fr;gap:.3mm;background:var(--moss);border:.3mm solid var(--moss);margin-bottom:8mm}.svc li{background:var(--forest);padding:4mm}.svc h3{font-size:11pt;margin:0 0 1mm}.svc p{margin:0;font-size:8.5pt;opacity:.85}
.btn{display:inline-block;background:var(--gold);color:var(--char);padding:3.5mm 7mm;font:8pt SM;text-transform:uppercase;letter-spacing:.1em;border:0}
.links li{display:flex;gap:8mm;padding:4mm 0;border-bottom:.3mm solid var(--moss);font:500 15pt PF}.links span{font:7.5pt SM;text-transform:uppercase;width:24mm;color:var(--pink);padding-top:2mm}.links{margin-bottom:10mm}
.lg2{width:40mm;margin:-6mm 0 4mm -4mm}
'''+'''
.stills{grid-template-columns:1.5fr 1fr;grid-template-rows:84mm 84mm;gap:4mm;margin-bottom:8mm}.stills img{aspect-ratio:auto;height:100%}.stills .s2{grid-row:span 2}
.strip{position:absolute;left:18mm;right:18mm;bottom:22mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}.strip img{width:100%;aspect-ratio:3/4;object-fit:cover;border:.3mm solid var(--gold)}
.pg>p{font-size:11pt}.about-p{}
.steps{gap:16mm;margin-top:14mm}.steps h3{font-size:17pt}.steps p{font-size:11.5pt}.steps b{font-size:44pt}.steps li{grid-template-columns:30mm 1fr;padding-top:6mm}
.svc li{padding:6mm}.svc h3{font-size:13pt}.svc p{font-size:10pt}.svc{margin-bottom:12mm}
.links li{padding:6mm 0;font-size:18pt}.contact .lg2{width:52mm}
'''
css += '''
:root{--moss:#7d8c4e;--forest:#0b0f09;--gold:#d9b45a;--pink:#c99d9a;--ivory:#ece2c8;--char:#0b0f09}
.pg{background:radial-gradient(45% 35% at 100% 0%,rgba(47,200,92,.55),transparent 72%),radial-gradient(30% 40% at 0% 50%,rgba(30,160,56,.4),transparent 75%),radial-gradient(70% 22% at 40% 105%,rgba(214,146,28,.45),transparent 70%),var(--forest)!important}
.pg::after{content:'';position:absolute;inset:0;background:url(assets/grain.png);background-size:70mm;opacity:.07;pointer-events:none}
.stills img{border:2.2mm solid #e6dcc3!important}.por{border:2.2mm solid #e6dcc3!important}
.cover{padding:16mm 0 20mm!important;justify-content:space-between!important}.cover>*{position:relative;z-index:2}
.cover .fl{position:absolute;right:-30mm;top:34mm;width:170mm;z-index:1}
.cover .cap.top,.cover .cap.bot{display:flex;justify-content:space-between;padding:0 14mm;margin:0}
.cover h1{font-size:104pt;line-height:.8;margin-top:10mm;display:flex;flex-direction:column}
.cover h1 .a{margin-left:-4mm;color:#ece2c8;position:relative;z-index:3}.cover h1 .b{margin-left:26mm;font-size:92pt;color:#e9dcb4;position:relative;z-index:1}
.cover .lede,.cover .role,.cover .cover-links{margin-left:14mm}.cover .lede{margin-top:12mm}
.fl2{position:absolute;right:-24mm;bottom:20mm;width:110mm;opacity:.9}.contact .links,.contact h2,.contact .btn{position:relative;z-index:2}
'''
doc = f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Epeke Vuyisani — UGC Portfolio</title><style>{css}</style><body>{"".join(pages)}</body></html>'
(H / 'portfolio.html').write_text(doc)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto((H / 'portfolio.html').resolve().as_uri())
    pg.wait_for_timeout(800)
    pg.pdf(path=str(H / 'Epeke_Vuyisani_UGC_Portfolio.pdf'), format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
print('pdf built')
