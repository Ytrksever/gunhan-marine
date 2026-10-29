# build/ -> site/ : Netlify (sürükle-bırak) için bağımsız statik site + SEO / GEO / AEO katmanı
import os, re, shutil, json, html, datetime, secrets, sys
from PIL import Image
DOMAIN = os.environ.get('GM_DOMAIN', 'https://gunhanmarine.com').rstrip('/')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = 'build', 'site'
TODAY = datetime.date.today().isoformat()
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
from blog_data import POSTS
POST = {p['slug']: p for p in POSTS}
KEYFILE = '.indexnow-key'
KEY = open(KEYFILE).read().strip() if os.path.exists(KEYFILE) else secrets.token_hex(16)
open(KEYFILE, 'w').write(KEY)

# ---------- favicon (logodaki amblem) ----------
lg = Image.open(f'{SRC}/images/logo-gunhan-koyu.png').convert('RGBA')
emb = lg.crop((0, 0, 282, 278)); emb.paste((0, 0, 0, 0), (238, 0, 282, 32)); emb = emb.crop(emb.getbbox())
def icon(n):
    c = Image.new('RGBA', (n, n), (255, 255, 255, 255)); m = int(n * .14)
    e = emb.copy(); e.thumbnail((n - 2 * m, n - 2 * m), Image.LANCZOS)
    c.alpha_composite(e, ((n - e.width) // 2, (n - e.height) // 2)); return c
icon(180).convert('RGB').save(f'{OUT}/apple-touch-icon.png')
icon(192).convert('RGB').save(f'{OUT}/icon-192.png')
icon(512).convert('RGB').save(f'{OUT}/icon-512.png')
icon(48).save(f'{OUT}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
icon(32).convert('RGB').save(f'{OUT}/favicon-32.png')
# sosyal paylaşım / OG görseli 1200x630
ban = Image.open(f'{SRC}/images/banner-yat.jpg').convert('RGB')
w, h = ban.size; nh = int(w * 630 / 1200); y0 = max(0, (h - nh) // 2)
ban.crop((0, y0, w, min(h, y0 + nh))).resize((1200, 630), Image.LANCZOS).save(f'{OUT}/images/og-gunhan-marine.jpg', quality=82, optimize=True)

# ---------- yardımcılar ----------
E = lambda s: html.escape(s, True)
def txt(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()
def faqs(s): return [(txt(q), txt(a)) for q, a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p class="ans"[^>]*>(.*?)</p>', s, re.S)]
def lead_of(s):
    m = re.search(r'<p class="lead[^"]*"[^>]*>(.*?)</p>', s, re.S); return txt(m.group(1)) if m else ''
def trim(t, n):
    return t if len(t) <= n else t[:n - 1].rsplit(' ', 1)[0].rstrip(',;:') + '…'
def first_img(s, root):
    for m in re.findall(r'src="(?:\.\./)?images/((?:hizmet|saha|banner)[^"]+)"', s): return m
    return None
BIZ, FOUNDER, SITE = DOMAIN + '/#business', DOMAIN + '/#founder', DOMAIN + '/#website'
SERVICE_NAMES = {}
INDEX_DESC = "Türkiye genelinde yerinde mobil deniz teknik servis: deniz motoru, marine elektrik, seyir elektroniği, karina bakımı ve alım öncesi ekspertiz."
BIZ_LD = {
  "@type": ["ProfessionalService", "LocalBusiness"], "@id": BIZ, "name": "Günhan Marine", "url": DOMAIN + "/",
  "description": INDEX_DESC, "image": DOMAIN + "/images/og-gunhan-marine.jpg", "logo": DOMAIN + "/icon-512.png",
  "telephone": "+905310291284", "email": "info@gunhanmarine.com",
  "address": {"@type": "PostalAddress", "addressLocality": "Adana", "addressCountry": "TR"},
  "areaServed": {"@type": "Country", "name": "Türkiye"},
  "founder": {"@id": FOUNDER}, "knowsLanguage": ["tr", "en", "ru", "ar"],
  "slogan": "Sorunun köküne ineriz.",
}
FOUNDER_LD = {"@type": "Person", "@id": FOUNDER, "name": "Alptekin Günhan", "jobTitle": "Kurucu & Marine Sistemler Mühendisi", "alternateName": "Feyyaz Alptekin Günhan", "url": DOMAIN + "/hakkimizda.html",
  "worksFor": {"@id": BIZ}, "alumniOf": {"@type": "CollegeOrUniversity", "name": "İstanbul Teknik Üniversitesi"},
  "knowsAbout": ["deniz motorları", "marine elektrik", "seyir elektroniği", "ABYC"]}
SITE_LD = {"@type": "WebSite", "@id": SITE, "url": DOMAIN + "/", "name": "Günhan Marine", "inLanguage": "tr", "publisher": {"@id": BIZ}}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + '/' + u} for i, (n, u) in enumerate(items)]}
def faq_ld(fq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}

def head_block(rel, title, desc, img, kind, graph):
    url = DOMAIN + '/' + ('' if rel == 'index.html' else rel)
    root = '../' * rel.count('/')
    ogimg = DOMAIN + '/images/' + img
    h = ('<meta name="description" content="%s"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
         '<link rel="canonical" href="%s">'
         '<meta property="og:type" content="%s"><meta property="og:site_name" content="Günhan Marine"><meta property="og:locale" content="tr_TR">'
         '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">'
         '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">'
         '<meta name="theme-color" content="#07131f">'
         '<link rel="icon" href="%sfavicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="%sfavicon-32.png"><link rel="apple-touch-icon" href="%sapple-touch-icon.png">'
         '<link rel="alternate" type="application/rss+xml" title="Günhan Marine Blog" href="%sfeed.xml">') % (
         E(desc), url, kind, E(title), E(desc), url, ogimg, E(title), E(desc), ogimg, root, root, root, root)
    h += '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return h

pages = sorted(os.path.relpath(os.path.join(d, f), OUT).replace(os.sep, '/') for d, _, fs in os.walk(OUT) for f in fs if f.endswith('.html'))
MARK = '<meta name="claude:viewport-fit-sides" content="cover">'
sitemap_items = []
for rel in pages:
    p = f'{OUT}/{rel}'; s = open(p, encoding='utf-8').read(); assert MARK in s, rel
    fq = faqs(s); lead = lead_of(s); img = first_img(s, '') or 'og-gunhan-marine.jpg'
    graph = []; kind = 'website'; prio = '0.7'
    if rel == 'index.html':
        title = 'Türkiye geneli mobil marine teknik servis | Günhan Marine'; desc = INDEX_DESC; img = 'og-gunhan-marine.jpg'; prio = '1.0'
        graph = [BIZ_LD, FOUNDER_LD, SITE_LD, {"@type": "WebPage", "@id": DOMAIN + "/#webpage", "url": DOMAIN + "/", "name": title, "isPartOf": {"@id": SITE}, "about": {"@id": BIZ}, "inLanguage": "tr"}]
        if fq: graph.append(faq_ld(fq))
    else:
        title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1)); name = title.split(' | ')[0]
        if rel.startswith('hizmetler/'):
            desc = trim(lead, 118) + ' Türkiye genelinde yerinde servis.'
            desc = trim(desc, 158); prio = '0.9'
            graph = [{"@type": "Service", "@id": url if (url := DOMAIN + '/' + rel) else '', "name": name, "serviceType": name, "description": lead, "url": DOMAIN + '/' + rel,
                      "provider": {"@id": BIZ}, "areaServed": BIZ_LD["areaServed"], "image": DOMAIN + '/images/' + img},
                     crumbs([("Ana sayfa", ""), ("Hizmetler", "#hizmetler"), (name, rel)])]
            if fq: graph.append(faq_ld(fq))
        elif rel.startswith('blog/'):
            slug = os.path.basename(rel)[:-5]; post = POST[slug]; kind = 'article'; img = post['img']; desc = trim(post['excerpt'], 158); prio = '0.6'
            graph = [{"@type": "BlogPosting", "headline": name, "description": post['excerpt'], "image": DOMAIN + '/images/' + img, "inLanguage": "tr",
                      "mainEntityOfPage": DOMAIN + '/' + rel, "datePublished": post['date'], "dateModified": post['date'],
                      "author": {"@id": FOUNDER}, "publisher": {"@id": BIZ}, "about": post['cat'],
                      "isPartOf": {"@id": DOMAIN + "/blog.html"}},
                     FOUNDER_LD, BIZ_LD, crumbs([("Ana sayfa", ""), ("Blog", "blog.html"), (name, rel)])]
            if fq: graph.append(faq_ld(fq))
        elif rel == 'blog.html':
            desc = trim(lead, 158); prio = '0.7'
            graph = [{"@type": "Blog", "name": "Günhan Marine Blog", "url": DOMAIN + '/blog.html', "inLanguage": "tr", "publisher": {"@id": BIZ},
                      "blogPost": [{"@type": "BlogPosting", "headline": pp['title'], "url": DOMAIN + '/blog/' + pp['slug'] + '.html'} for pp in POSTS]},
                     crumbs([("Ana sayfa", ""), ("Blog", "blog.html")])]
        elif rel == 'hakkimizda.html':
            desc = trim(lead, 158); img = 'og-gunhan-marine.jpg'
            graph = [{"@type": "AboutPage", "url": DOMAIN + '/hakkimizda.html', "name": name, "about": {"@id": BIZ}, "inLanguage": "tr"}, FOUNDER_LD,
                     crumbs([("Ana sayfa", ""), ("Hakkımızda", rel)])]
            if fq: graph.append(faq_ld(fq))
        else:
            desc = trim(lead or INDEX_DESC, 158)
    hb = head_block(rel, title, desc, img, kind, graph)
    if rel == 'index.html':
        s = s.replace('<title>Günhan Marine</title>', '', 1).replace(MARK, '', 1)
        s = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
             '<title>%s</title>' % html.escape(title) + hb +
             '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>' + s.lstrip() + '</body></html>')
    else:
        s = s.replace(MARK, hb, 1)
    open(p, 'w', encoding='utf-8').write(s)
    sitemap_items.append((rel, prio))

# ---------- sitemap, robots, llms.txt, feed, indexnow, netlify ----------
def loc(r): return DOMAIN + '/' + ('' if r == 'index.html' else r)
open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (loc(r), (POST[r[5:-5]]['date'] if r.startswith('blog/') else TODAY), pr) for r, pr in sitemap_items) + '</urlset>\n')
BOTS = ['Googlebot', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot', 'Applebot-Extended', 'CCBot']
open(f'{OUT}/robots.txt', 'w').write('# Günhan Marine: tüm arama ve yapay zekâ tarayıcılarına açık\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in BOTS) +
  'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % DOMAIN)
svc = [(os.path.basename(r)[:-5], r) for r, _ in sitemap_items if r.startswith('hizmetler/')]
svc_lines = ''
for r, _ in sitemap_items:
    if r.startswith('hizmetler/'):
        t = re.search(r'<title>(.*?)</title>', open(f'{OUT}/{r}', encoding='utf-8').read()).group(1).split(' | ')[0]
        svc_lines += '- [%s](%s): %s\n' % (html.unescape(t), loc(r), trim(lead_of(open(f'{OUT}/{r}', encoding='utf-8').read()), 150))
blog_lines = ''.join('- [%s](%s): %s\n' % (pp['title'], DOMAIN + '/blog/' + pp['slug'] + '.html', pp['excerpt']) for pp in POSTS)
open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write('''# Günhan Marine

> Türkiye genelinde mobil deniz teknik servis. Teknenin bulunduğu yerde (marina, kızak, tersane, göl kıyısı) deniz motoru, marine elektrik, seyir elektroniği, karina bakımı ve alım öncesi motor/elektrik ekspertizi hizmeti verir. Site Türkçe, İngilizce, Rusça ve Arapça sunulur.

Kurucu: Feyyaz Alptekin Günhan, İTÜ Gemi Makineleri İşletme Mühendisliği mezunu. İletişim: +90 531 029 12 84, info@gunhanmarine.com

## Hizmetler
''' + svc_lines + '''
## Rehberler (blog)
''' + blog_lines + '''
## Kurumsal
- [Hakkımızda](%s/hakkimizda.html): Misyon, vizyon, kurucu ve çalışma yaklaşımı
- [Ana sayfa](%s/): Hizmet bölgesi, süreç ve sık sorulan sorular
''' % (DOMAIN, DOMAIN))
rss = ''.join('<item><title>%s</title><link>%s</link><guid>%s</guid><pubDate>%s</pubDate><description>%s</description></item>' % (
    E(pp['title']), DOMAIN + '/blog/' + pp['slug'] + '.html', DOMAIN + '/blog/' + pp['slug'] + '.html', datetime.date.fromisoformat(pp['date']).strftime('%a, %d %b %Y 08:00:00 +0300'), E(pp['excerpt'])) for pp in POSTS)
open(f'{OUT}/feed.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Günhan Marine Blog</title><link>%s/blog.html</link><description>Mobil deniz teknik servis sahasından motor, elektrik, seyir elektroniği ve bakım rehberleri.</description><language>tr</language>%s</channel></rss>' % (DOMAIN, rss))
open(f'{OUT}/{KEY}.txt', 'w').write(KEY)
BING_KEY = '6699407300da4e1caad435bd928e856c'
open(f'{OUT}/{BING_KEY}.txt', 'w').write(BING_KEY)
open(f'{OUT}/404.html', 'w', encoding='utf-8').write('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Sayfa bulunamadı | Günhan Marine</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#07131f;color:#eaf2f6;font-family:system-ui,sans-serif;text-align:center;padding:24px}a{display:inline-block;margin-top:18px;padding:12px 22px;border-radius:999px;background:#d7d521;color:#06202f;text-decoration:none;font-weight:600}</style></head><body><div><h1>Sayfa bulunamadı</h1><p>Aradığınız sayfa taşınmış ya da hiç var olmamış olabilir.</p><a href="/">Ana sayfaya dön</a></div></body></html>')
import json as _j
_rk = _j.load(open('config.json')).get('recaptcha_site_key', '').strip()
_rs = ' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/' if _rk else ''
_rf = " frame-src https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/;" if _rk else ''
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'" + _rs + "; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; "
       "form-action 'self'; frame-ancestors 'self';" + _rf)
open(f'{OUT}/_headers', 'w').write('''/*
  Content-Security-Policy: ''' + CSP + '''
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
/images/*
  Cache-Control: public, max-age=31536000, immutable
/i18n/*
  Cache-Control: public, max-age=3600
  Content-Type: application/json; charset=utf-8
/llms.txt
  Content-Type: text/plain; charset=utf-8
/robots.txt
  Content-Type: text/plain; charset=utf-8
''')
open(f'{OUT}/_redirects', 'w').write('# eski adres -> yeni adres\n/blog/kurban-anot-cinko-nedir-ne-zaman-degistirilir.html  /blog/tutya-cinko-nedir-ne-zaman-degistirilir.html  301\n/hizmetler/travel-lift-tersane-ekipmanlari.html  /  301\n')
if os.path.exists(f'{OUT}/files.json'): os.remove(f'{OUT}/files.json')
open('indexnow_urls.json', 'w').write(json.dumps({"host": DOMAIN.split('//')[1], "key": KEY, "keyLocation": f"{DOMAIN}/{KEY}.txt", "urlList": [loc(r) for r, _ in sitemap_items]}, indent=1))
print(len(pages), 'sayfa;', DOMAIN, '; anahtar', KEY)
