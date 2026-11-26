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
emb = lg.crop((0, 0, 278, 278)); emb.paste((0, 0, 0, 0), (212, 0, 278, 60)); emb = emb.crop(emb.getbbox())  # 278 px: 'G' harfinin başladığı yerde kes
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

# ---------- diller: /en/ /ru/ /ar/ statik kopyalar ----------
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin, urlsplit
import copy
LANGS = ('tr', 'en', 'ru', 'ar'); DIRS = {'tr': 'ltr', 'en': 'ltr', 'ru': 'ltr', 'ar': 'rtl'}; LOCALE = {'tr': 'tr_TR', 'en': 'en_US', 'ru': 'ru_RU', 'ar': 'ar_AR'}
FONTS = {'ru': 'https://fonts.googleapis.com/css2?family=Onest:wght@300..800&display=swap', 'ar': 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap'}
DICT = {l: json.load(open(f'{SRC}/i18n/{l}.json', encoding='utf-8')) for l in ('en', 'ru', 'ar')}
PAGES_LASTMOD = '2026-11-25'  # tasarım/içerik değişince elle güncelle; yazılar kendi tarihini kullanır
SPECIAL = {
  'en': {INDEX_DESC: 'On-site mobile marine technical service across Türkiye: marine engines, marine electrical, navigation electronics, hull care and pre-purchase survey.',
         'Sorunun köküne ineriz.': 'We get to the root of the problem.', 'Kurucu & Marine Sistemler Mühendisi': 'Founder & Marine Systems Engineer',
         'Ana sayfa': 'Home', 'Hizmetler': 'Services', 'Blog': 'Blog', 'Hakkımızda': 'About us',
         'TITLE': 'Mobile marine technical service across Türkiye | Günhan Marine', 'SUFFIX': ' On-site service across Türkiye.'},
  'ru': {INDEX_DESC: 'Выездной мобильный морской технический сервис по всей Турции: судовые двигатели, морская электрика, навигационная электроника, уход за корпусом и экспертиза перед покупкой.',
         'Sorunun köküne ineriz.': 'Мы докапываемся до первопричины.', 'Kurucu & Marine Sistemler Mühendisi': 'Основатель и инженер морских систем',
         'Ana sayfa': 'Главная', 'Hizmetler': 'Услуги', 'Blog': 'Блог', 'Hakkımızda': 'О нас',
         'TITLE': 'Мобильный морской технический сервис по всей Турции | Günhan Marine', 'SUFFIX': ' Выездной сервис по всей Турции.'},
  'ar': {INDEX_DESC: 'خدمة بحرية فنية متنقلة في موقع القارب في جميع أنحاء تركيا: محركات بحرية وكهرباء بحرية وإلكترونيات الملاحة والعناية بالبدن وفحص ما قبل الشراء.',
         'Sorunun köküne ineriz.': 'نصل إلى جذر المشكلة.', 'Kurucu & Marine Sistemler Mühendisi': 'المؤسس ومهندس الأنظمة البحرية',
         'Ana sayfa': 'الرئيسية', 'Hizmetler': 'الخدمات', 'Blog': 'المدونة', 'Hakkımızda': 'من نحن',
         'TITLE': 'خدمة بحرية فنية متنقلة في جميع أنحاء تركيا | Günhan Marine', 'SUFFIX': ' خدمة في موقع القارب في جميع أنحاء تركيا.'},
}
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def U(lang, rel):
    return DOMAIN + '/' + ('' if lang == 'tr' else lang + '/') + ('' if rel == 'index.html' else rel)
def tr(lang, s):
    if lang == 'tr' or not isinstance(s, str): return s
    k = norm(s)
    return SPECIAL[lang].get(k) or DICT[lang].get(k) or s
def tr_ld(lang, o):
    if lang == 'tr': return o
    if isinstance(o, str): return o if o.startswith('http') else tr(lang, o)
    if isinstance(o, list): return [tr_ld(lang, x) for x in o]
    if isinstance(o, dict): return {k: (v if k in ('@id', '@type', 'url', 'item', 'image', 'logo', 'telephone', 'email', 'inLanguage', 'datePublished', 'dateModified', 'position', 'addressCountry', 'knowsLanguage') else tr_ld(lang, v)) for k, v in o.items()}
    return o

EXT_ASSET = re.compile(r'\.(?:jpe?g|png|webp|svg|gif|ico|css|js|json|xml|txt|woff2?|pdf|mp4)$', re.I)
def fix_url(u, rel, lang, page_link):
    if not u or re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#)', u, re.I): return u
    sp = urlsplit(urljoin('/' + rel, u)); path = sp.path
    tail = ('?' + sp.query if sp.query else '') + ('#' + sp.fragment if sp.fragment else '')
    if page_link and not EXT_ASSET.search(path):
        if path in ('/', '/index.html'): path = '/'
        return '/' + lang + path + tail
    return path + tail

SKIPT = {'script', 'style', 'noscript', 'textarea'}
def blocked(el):
    p = el
    while p is not None and getattr(p, 'name', None):
        if p.name in SKIPT or p.name in ('head', 'title') or p.has_attr('data-nt') or p.has_attr('data-i18n'): return True
        p = p.parent
    return False

def localize(s, rel, lang):
    d = DICT[lang]
    soup = BeautifulSoup(s, 'html.parser')
    for n in list(soup.find_all(string=True)):
        if type(n) is not NavigableString or blocked(n.parent): continue
        k = norm(str(n))
        if k and k in d:
            v = str(n); n.replace_with(NavigableString(re.match(r'^\s*', v).group(0) + d[k] + re.search(r'\s*$', v).group(0)))
    for el in soup.find_all(attrs={'alt': True}) + soup.find_all(attrs={'placeholder': True}) + soup.find_all(attrs={'aria-label': True}) + soup.find_all(attrs={'title': True}):
        if el.name == 'title' or el.find_parent(attrs={'data-nt': True}) is not None or el.has_attr('data-nt'): continue
        for a in ('alt', 'placeholder', 'aria-label', 'title'):
            if el.has_attr(a):
                k = norm(el[a])
                if k in d: el[a] = d[k]
    for el in soup.find_all(attrs={'data-i18n': True}):
        v = d.get(el['data-i18n'])
        if v is not None:
            el.clear(); el.append(BeautifulSoup(v, 'html.parser'))
    t = soup.find('title')
    if t is not None:
        parts = (t.string or '').split(' | '); parts[0] = d.get(norm(parts[0]), parts[0]); t.string = ' | '.join(parts)
    for a in soup.find_all('a', href=True): a['href'] = fix_url(a['href'], rel, lang, True)
    for el in soup.find_all(['img', 'source', 'script', 'link']):
        for at in ('src', 'href'):
            if el.has_attr(at): el[at] = fix_url(el[at], rel, lang, False)
        if el.has_attr('srcset'): el['srcset'] = ', '.join(fix_url(x.split()[0], rel, lang, False) + ' ' + ' '.join(x.split()[1:]) for x in el['srcset'].split(','))
    body = soup.find('body')
    if body is not None and body.has_attr('data-root'): body['data-root'] = '/'
    g = soup.find(id='gm-root')
    if g is not None: g['data-root'] = '/'
    if soup.html is not None:
        soup.html['lang'] = lang; soup.html['dir'] = DIRS[lang]; soup.html['data-static'] = lang
    return soup.decode()

def crumbs(lang, items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": U(lang, u) if u and not u.startswith('#') else (U(lang, 'index.html') + u)} for i, (n, u) in enumerate(items)]}
def faq_ld(fq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}

def head_block(rel, lang, title, desc, img, kind, graph):
    url = U(lang, rel)
    root = '/' if lang != 'tr' else '../' * rel.count('/')
    ogimg = DOMAIN + '/images/' + img
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">' % (l, U(l, rel)) for l in LANGS) + '<link rel="alternate" hreflang="x-default" href="%s">' % U('tr', rel)
    h = ('<meta name="description" content="%s"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
         '<link rel="canonical" href="%s">%s'
         '<meta property="og:type" content="%s"><meta property="og:site_name" content="Günhan Marine"><meta property="og:locale" content="%s">'
         '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">'
         '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">'
         '<meta name="theme-color" content="#07131f">'
         '<link rel="icon" href="%sfavicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="%sfavicon-32.png"><link rel="apple-touch-icon" href="%sapple-touch-icon.png">'
         '<link rel="alternate" type="application/rss+xml" title="Günhan Marine Blog" href="%sfeed.xml">') % (
         E(desc), url, alts, kind, LOCALE[lang], E(title), E(desc), url, ogimg, E(title), E(desc), ogimg, root, root, root, root)
    if lang in FONTS: h += '<link rel="stylesheet" href="%s">' % FONTS[lang]
    h += '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return h

base_pages = sorted(os.path.relpath(os.path.join(d, f), SRC).replace(os.sep, '/') for d, _, fs in os.walk(SRC) for f in fs if f.endswith('.html'))
ORIG = {rel: open(f'{SRC}/{rel}', encoding='utf-8').read() for rel in base_pages}
MARK = '<meta name="claude:viewport-fit-sides" content="cover">'
MARK_RE = re.compile(r'<meta[^>]*claude:viewport-fit-sides[^>]*>')
sitemap_items = []
for lang in LANGS:
  for rel in base_pages:
    s = ORIG[rel] if lang == 'tr' else localize(ORIG[rel], rel, lang)
    assert MARK_RE.search(s), (lang, rel)
    fq = faqs(s); lead = lead_of(s); img = first_img(s, '') or 'og-gunhan-marine.jpg'
    L = lambda x: tr(lang, x)
    biz = copy.deepcopy(BIZ_LD); biz['description'] = L(INDEX_DESC); biz['slogan'] = L(biz['slogan'])
    founder = copy.deepcopy(FOUNDER_LD); founder['jobTitle'] = L(founder['jobTitle']); founder['url'] = U(lang, 'hakkimizda.html')
    site = dict(SITE_LD, inLanguage=lang, url=U(lang, 'index.html'))
    CR = lambda items: crumbs(lang, [(L(n), u) for n, u in items])
    graph = []; kind = 'website'; prio = '0.7'
    if rel == 'index.html':
        title = SPECIAL[lang]['TITLE'] if lang != 'tr' else 'Türkiye geneli mobil marine teknik servis | Günhan Marine'; desc = L(INDEX_DESC); img = 'og-gunhan-marine.jpg'; prio = '1.0'
        graph = [biz, founder, site, {"@type": "WebPage", "@id": U(lang, 'index.html') + "#webpage", "url": U(lang, 'index.html'), "name": title, "isPartOf": {"@id": SITE}, "about": {"@id": BIZ}, "inLanguage": lang}]
        if fq: graph.append(faq_ld(fq))
    else:
        title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1)); name = title.split(' | ')[0]
        if rel.startswith('hizmetler/'):
            desc = trim(trim(lead, 118) + L(' Türkiye genelinde yerinde servis.') if lang == 'tr' else trim(lead, 118) + SPECIAL[lang]['SUFFIX'], 158); prio = '0.9'
            graph = [{"@type": "Service", "@id": U(lang, rel), "name": name, "serviceType": name, "description": lead, "url": U(lang, rel),
                      "provider": {"@id": BIZ}, "areaServed": BIZ_LD["areaServed"], "image": DOMAIN + '/images/' + img},
                     CR([("Ana sayfa", "index.html"), ("Hizmetler", "#hizmetler"), (name, rel)])]
            graph[1]['itemListElement'][2]['name'] = name
            if fq: graph.append(faq_ld(fq))
        elif rel.startswith('blog/'):
            slug = os.path.basename(rel)[:-5]; post = POST[slug]; kind = 'article'; img = post['img']; ex = L(post['excerpt']); desc = trim(ex, 158); prio = '0.6'
            graph = [{"@type": "BlogPosting", "headline": name, "description": ex, "image": DOMAIN + '/images/' + img, "inLanguage": lang,
                      "mainEntityOfPage": U(lang, rel), "datePublished": post['date'], "dateModified": post['date'],
                      "author": {"@id": FOUNDER}, "publisher": {"@id": BIZ}, "about": L(post['cat']),
                      "isPartOf": {"@id": U(lang, 'blog.html')}},
                     founder, biz, CR([("Ana sayfa", "index.html"), ("Blog", "blog.html"), (name, rel)])]
            graph[3]['itemListElement'][2]['name'] = name
            if fq: graph.append(faq_ld(fq))
        elif rel == 'blog.html':
            desc = trim(lead, 158); prio = '0.7'
            graph = [{"@type": "Blog", "name": "Günhan Marine Blog", "url": U(lang, 'blog.html'), "inLanguage": lang, "publisher": {"@id": BIZ},
                      "blogPost": [{"@type": "BlogPosting", "headline": L(pp['title']), "url": U(lang, 'blog/' + pp['slug'] + '.html')} for pp in POSTS]},
                     CR([("Ana sayfa", "index.html"), ("Blog", "blog.html")])]
        elif rel == 'hakkimizda.html':
            desc = trim(lead, 158); img = 'og-gunhan-marine.jpg'
            graph = [{"@type": "AboutPage", "url": U(lang, rel), "name": name, "about": {"@id": BIZ}, "inLanguage": lang}, founder,
                     CR([("Ana sayfa", "index.html"), ("Hakkımızda", rel)])]
            graph[2]['itemListElement'][1]['name'] = name
            if fq: graph.append(faq_ld(fq))
        else:
            desc = trim(lead or L(INDEX_DESC), 158)
    hb = head_block(rel, lang, title, desc, img, kind, graph)
    if rel == 'index.html':
        s = s.replace('<title>Günhan Marine</title>', '', 1); s = re.sub(r'<title>[^<]*</title>', '', s, count=1); s = MARK_RE.sub('', s, count=1)
        s = ('<!doctype html><html lang="%s" dir="%s"%s><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' % (lang, DIRS[lang], '' if lang == 'tr' else ' data-static="%s"' % lang) +
             '<title>%s</title>' % html.escape(title) + hb +
             '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>' + re.sub(r'^\s*<!doctype[^>]*>\s*', '', s).lstrip() + '</body></html>')
    else:
        s = MARK_RE.sub(lambda m: hb, s, count=1)
    outp = f'{OUT}/{rel}' if lang == 'tr' else f'{OUT}/{lang}/{rel}'
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    open(outp, 'w', encoding='utf-8').write(s)
    if lang == 'tr': sitemap_items.append((rel, prio))
pages = [r for r, _ in sitemap_items]

# ---------- sitemap, robots, llms.txt, feed, indexnow, netlify ----------
def loc(r): return DOMAIN + '/' + ('' if r == 'index.html' else r)
def lm(r): return POST[r[5:-5]]['date'] if r.startswith('blog/') else PAGES_LASTMOD
def sm_url(l, r, pr):
    return ('  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority>' % (U(l, r), lm(r), pr) +
            ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (x, U(x, r)) for x in LANGS) +
            '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/></url>\n' % U('tr', r))
open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
  ''.join(sm_url(l, r, pr if l == 'tr' else str(round(float(pr) - 0.1, 1))) for r, pr in sitemap_items for l in LANGS) + '</urlset>\n')
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
_cfg = _j.load(open('config.json'))
_an = {k: str(_cfg.get(k, '')).strip() for k in ('ga4', 'clarity', 'meta_pixel', 'linkedin_partner')}
_sc, _cn, _im, _fr = [], [], [], []
if _an['ga4']:
    _sc += ['https://www.googletagmanager.com']
    _cn += ['https://www.google-analytics.com', 'https://*.google-analytics.com', 'https://*.analytics.google.com', 'https://www.googletagmanager.com']
    _im += ['https://www.google-analytics.com', 'https://*.google-analytics.com', 'https://www.googletagmanager.com']
if _an['clarity']:
    _sc += ['https://www.clarity.ms', 'https://scripts.clarity.ms']
    _cn += ['https://*.clarity.ms', 'https://c.bing.com']
    _im += ['https://*.clarity.ms', 'https://c.bing.com']
if _an['meta_pixel']:
    _sc += ['https://connect.facebook.net']
    _cn += ['https://www.facebook.com', 'https://connect.facebook.net']
    _im += ['https://www.facebook.com']
if _an['linkedin_partner']:
    _sc += ['https://snap.licdn.com']
    _cn += ['https://px.ads.linkedin.com', 'https://www.linkedin.com']
    _im += ['https://px.ads.linkedin.com', 'https://www.linkedin.com']
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'" + _rs + ''.join(' ' + x for x in _sc) + "; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data:" + ''.join(' ' + x for x in _im) + "; connect-src 'self'" + ''.join(' ' + x for x in _cn) + "; object-src 'none'; base-uri 'self'; "
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
open('indexnow_urls.json', 'w').write(json.dumps({"host": DOMAIN.split('//')[1], "key": KEY, "keyLocation": f"{DOMAIN}/{KEY}.txt", "urlList": [U(l, r) for r, _ in sitemap_items for l in LANGS]}, indent=1))
# Netlify .html adreslerini uzantısız adrese yönlendirir; kanonik, hreflang, site haritası ve veri adreslerini buna uyduruyoruz.
_abs = re.compile(re.escape(DOMAIN) + r'(/[^"\'<>\s#?]*?)\.html(?![\w/.-])')
def _clean(m): return DOMAIN + (m.group(1)[:-len('/index')] if m.group(1).endswith('/index') else m.group(1))
for _d, _, _fs in os.walk(OUT):
    for _f in _fs:
        if _f.endswith(('.html', '.xml', '.txt', '.json')) and _f != '404.html':
            _p = os.path.join(_d, _f); _t = open(_p, encoding='utf-8').read(); _n = _abs.sub(_clean, _t)
            if _n != _t: open(_p, 'w', encoding='utf-8').write(_n)
_ix = open('indexnow_urls.json', encoding='utf-8').read(); open('indexnow_urls.json', 'w', encoding='utf-8').write(_abs.sub(_clean, _ix))
print(len(pages), 'sayfa;', DOMAIN, '; anahtar', KEY)
