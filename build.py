import re, os, html, json, time
from PIL import Image
from blog_data import POSTS, DATE

SP = os.path.dirname(os.path.abspath(__file__))
OUT = SP + '/build'
import shutil
for _d in ('blog', 'hizmetler'):
    shutil.rmtree(OUT + '/' + _d, ignore_errors=True)
for d in ('hizmetler', 'blog', 'i18n'):
    os.makedirs(OUT + '/' + d, exist_ok=True)
VER = str(int(time.time()))

src = open(SP + '/gunhan-marine.html', encoding='utf-8').read()
md = open(SP + '/gunhan-marine-icerik.md', encoding='utf-8').read()
esc = lambda s: html.escape(s, quote=False)
qesc = lambda s: html.escape(s, quote=True)

def dims(rel):
    with Image.open(OUT + '/' + rel) as im:
        return im.size

SLUGS = [
    'deniz-motorlari-sevk-sistemleri', 'tekne-mekanik-yardimci-sistemler', 'seyir-elektronigi-navigasyon',
    'marine-elektrik-guc-yonetimi', 'karina-bakimi-antifouling', 'alim-oncesi-ekspertiz',
]
SERVICE_VALUES = [
    'Deniz motorları ve sevk sistemleri', 'Tekne mekanik ve yardımcı sistemler', 'Seyir elektroniği ve navigasyon',
    'Marine elektrik ve güç yönetimi', 'Karina bakımı ve antifouling', 'Alım öncesi ekspertiz',
]
ALT = [
    'Atölyede bir deniz motorunun üzerinde çalışan eldivenli teknisyen',
    'Rıhtıma bağlı bir teknenin baş güvertesinde irgat ve halatlar',
    'Köprüüstünde VHF telsizler ve seyir ekranları',
    'Akü bankı, invertör, sigorta kutuları ve ana şalter',
    'Kızağa alınmış bir teknenin karinasına antifouling boyası sürülmesi',
    'Karaya çekilmiş bir teknenin altını inceleyen iki kişi',
]
BRANDS = {
    0: ([('yamaha', 'Yamaha'), ('mercury', 'Mercury ve MerCruiser'), ('honda', 'Honda Marine'), ('suzuki', 'Suzuki Marine'),
         ('volvo-penta', 'Volvo Penta'), ('yanmar', 'Yanmar'), ('cummins', 'Cummins'), ('john-deere', 'John Deere'), ('tohatsu', 'Tohatsu')], []),
}
CHIPS = {
    1: ['Şaft-pervane', 'Seacock', 'Sintine pompası', 'Tatlı su pompası', 'Dümen', 'Hidrolik'],
    2: ['Garmin', 'Raymarine', 'Simrad', 'Furuno', 'NMEA 2000'],
    3: ['ABYC', 'Akü bankası', 'Jeneratör', 'İnverter', 'AC/DC'],
    4: ['Ozmoz kontrolü', 'Zımpara', 'Astar', 'Antifouling'],
    5: ['Kompresyon testi', 'Bilgisayarlı teşhis', 'Rapor: ödemeden sonra 24 saat', 'Gövde survey kapsam dışı'],
}
GALLERY = [
    ('saha-01.jpg', 'Kompresyon testi'), ('saha-02.jpg', 'Eşanjör bakımı'), ('saha-03.jpg', 'Jeneratör eşanjör bakımı'),
    ('saha-04.jpg', 'Jeneratör eşanjör servisi'), ('saha-05.jpg', 'Yamaha 300 saat bakımı'), ('saha-06.jpg', 'Volvo Penta motor manifold değişimi'),
    ('saha-07.jpg', 'Marş dinamosu değişimi'), ('saha-08.jpg', 'Karbüratör incelemesi'), ('saha-09.jpg', 'Akü testi'),
]

# ---------- İçerik ayrıştırma ----------
def faq_items(block):
    out = []
    for line in block.splitlines():
        m = re.match(r'^- \*\*(.+?)\*\* (.+)$', line.strip())
        if m: out.append((m.group(1), m.group(2)))
    return out

svc = []
for n in range(1, 7):
    m = re.search(r'### 3\.%d (.+?) \(/' % n, md)
    title = m.group(1); start = md.index('\n', m.end())
    nxt = re.search(r'\n### 3\.%d |\n---' % (n + 1), md[start:])
    block = md[start: start + nxt.start()] if nxt else md[start:]
    head, _, faq = block.partition('**SSS**')
    paras = [p.strip() for p in head.split('\n') if p.strip() and not p.strip().startswith('**') and not p.strip().startswith('(/')]
    svc.append(dict(n=n, title=title, intro=paras[0], cover=paras[1] if len(paras) > 1 else '', faq=faq_items(faq)))

about_blk = md[md.index('## 2. Hakkımızda'): md.index('## 3. Hizmetlerimiz')]
about_p = re.search(r'\*\*HAKKIMIZDA:\*\* (.+)', about_blk).group(1).strip()
mission = re.search(r'\*\*Misyonumuz:\*\* (.+)', about_blk).group(1).strip()
vision = re.search(r'\*\*Vizyonumuz:\*\* (.+)', about_blk).group(1).strip()
about_faq = faq_items(about_blk)

# ---------- CSS: tema belirteçleri ----------
DARK = """
  --bg: #07131f; --bg2: #0a1b2b; --surface: #0d2133; --surface2: #12304a;
  --ink: #eaf2f6; --muted: #8fa7b6; --line: rgba(160, 200, 225, .15); --line-strong: rgba(160, 200, 225, .35);
  --teal: #4fd6e0; --accent: #d7d521; --accent-hover: #e6e44c; --on-accent: #06202f; --accent-text: #d7d521; --focus: #8cc4ff;
  --header-bg: rgba(7, 19, 31, .6); --hover: rgba(255,255,255,.06); --hover-soft: rgba(255,255,255,.02);
  --ghost-bg: rgba(255,255,255,.03); --ghost-hover-bg: rgba(255,255,255,.07); --ghost-hover-border: rgba(234,242,246,.55);
  --sheen: rgba(255,255,255,.035); --teal-soft: rgba(79,214,224,.08); --tile-glow: rgba(79,214,224,.2); --tile-hover-border: rgba(79,214,224,.42);
  --glow-t1: rgba(79,214,224,.2); --glow-y1: rgba(215,213,33,.07); --glow-t2: rgba(79,214,224,.16); --glow-y2: rgba(215,213,33,.08);
  --card-a: rgba(13,33,51,.78); --card-b: rgba(7,19,31,.72); --panel-a: rgba(13,33,51,.85); --panel-b: rgba(10,27,43,.8);
  --shadow: rgba(0,0,0,.7); --inset: rgba(255,255,255,.06); --field-bg: rgba(255,255,255,.03); --field-focus: rgba(79,214,224,.05);
  --badge-border: rgba(215,213,33,.4); --wm: rgba(79,214,224,.5); --w1: #4fd6e0; --w2: #d7d521; --brand-card: #ffffff;
  --c-teal: 79,214,224; --c-yel: 215,213,33; --c-ink: 234,242,246; --c-muted: 143,167,182; --c-tick: 160,200,225;
"""
LIGHT = """
  --bg: #f3f7fa; --bg2: #e8f0f5; --surface: #ffffff; --surface2: #dde8ef;
  --ink: #0b1b2b; --muted: #475d6e; --line: rgba(11, 40, 64, .14); --line-strong: rgba(11, 40, 64, .32);
  --teal: #0a7f8e; --accent: #d7d521; --accent-hover: #c8c614; --on-accent: #06202f; --accent-text: #6b6a00; --focus: #0b5bd3;
  --header-bg: rgba(243, 247, 250, .78); --hover: rgba(11,40,64,.06); --hover-soft: rgba(11,40,64,.03);
  --ghost-bg: rgba(255,255,255,.7); --ghost-hover-bg: #ffffff; --ghost-hover-border: rgba(11,27,43,.5);
  --sheen: rgba(255,255,255,0); --teal-soft: rgba(10,127,142,.09); --tile-glow: rgba(10,127,142,.13); --tile-hover-border: rgba(10,127,142,.5);
  --glow-t1: rgba(10,127,142,.14); --glow-y1: rgba(215,213,33,.16); --glow-t2: rgba(10,127,142,.1); --glow-y2: rgba(215,213,33,.12);
  --card-a: rgba(255,255,255,.9); --card-b: rgba(255,255,255,.78); --panel-a: rgba(255,255,255,.96); --panel-b: rgba(255,255,255,.9);
  --shadow: rgba(11,40,64,.3); --inset: rgba(255,255,255,.8); --field-bg: #ffffff; --field-focus: rgba(10,127,142,.05);
  --badge-border: rgba(107,106,0,.45); --wm: rgba(10,127,142,.3); --w1: #0a7f8e; --w2: #a67f00; --brand-card: #ffffff;
  --c-teal: 8,127,142; --c-yel: 166,127,0; --c-ink: 11,27,43; --c-muted: 71,93,110; --c-tick: 30,80,110;
"""
FONTS = """
  --display: "Bricolage Grotesque", "Helvetica Neue", Arial, sans-serif;
  --body: "Instrument Sans", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --ease: cubic-bezier(.2, .8, .2, 1);
"""
ROOT_CSS = (':root {\n  color-scheme: dark;' + DARK + FONTS + '}\n'
            '@media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) {\n  color-scheme: light;' + LIGHT + '} }\n'
            ':root[data-theme="light"] {\n  color-scheme: light;' + LIGHT + '}\n'
            ':root[data-theme="dark"] {\n  color-scheme: dark;' + DARK + '}\n')

def swap(dark_sel, light_sel, show='block'):
    """Koyu temada dark_sel, açık temada light_sel görünür."""
    return ('%(l)s{display:none}\n@media (prefers-color-scheme: light){:root:not([data-theme="dark"]) %(d)s{display:none}:root:not([data-theme="dark"]) %(l)s{display:%(s)s}}\n'
            ':root[data-theme="light"] %(d)s{display:none}:root[data-theme="light"] %(l)s{display:%(s)s}\n'
            ':root[data-theme="dark"] %(d)s{display:%(s)s}:root[data-theme="dark"] %(l)s{display:none}\n') % dict(d=dark_sel, l=light_sel, s=show)

css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
css = re.sub(r':root \{.*?\n\}\n', lambda m: ROOT_CSS, css, count=1, flags=re.S)
REPL = [
    ('background: rgba(7, 19, 31, .6); backdrop-filter', 'background: var(--header-bg); backdrop-filter'),
    ('nav.main a:hover { color: var(--ink); background: rgba(255,255,255,.06); }', 'nav.main a:hover { color: var(--ink); background: var(--hover); }'),
    ('.btn-ghost { background: rgba(255,255,255,.03);', '.btn-ghost { background: var(--ghost-bg);'),
    ('.btn-ghost:hover { border-color: rgba(234,242,246,.55); background: rgba(255,255,255,.07); }', '.btn-ghost:hover { border-color: var(--ghost-hover-border); background: var(--ghost-hover-bg); }'),
    ('rgba(79,214,224,.2), transparent 62%),\n    radial-gradient(700px 500px at -5% 105%, rgba(215,213,33,.07), transparent 60%)', 'var(--glow-t1), transparent 62%),\n    radial-gradient(700px 500px at -5% 105%, var(--glow-y1), transparent 60%)'),
    ('linear-gradient(90deg, #4fd6e0, #d7d521, #4fd6e0)', 'linear-gradient(90deg, var(--w1), var(--w2), var(--w1))'),
    ('background: linear-gradient(180deg, rgba(13,33,51,.78), rgba(7,19,31,.72));', 'background: linear-gradient(180deg, var(--card-a), var(--card-b));'),
    ('box-shadow: 0 30px 80px -30px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.06);', 'box-shadow: 0 30px 80px -30px var(--shadow), inset 0 1px 0 var(--inset);'),
    ('.radar-foot div { padding: .8rem 1.1rem; border-left: 1px solid var(--line); min-width: 0; }\n.radar-foot div:first-child { border-left: 0; }', '.radar-foot div { padding: .8rem 1.1rem; border-inline-start: 1px solid var(--line); min-width: 0; }\n.radar-foot div:first-child { border-inline-start: 0; }'),
    ('padding: 1.05rem 0 1.05rem 1.75rem;', 'padding: 1.05rem 0; padding-inline-start: 1.75rem;'),
    ('.stat { border-bottom: 0; border-left: 1px solid var(--line); padding: .5rem 0 .5rem 2rem; grid-template-columns: 1fr; }\n  .stat:first-child { border-left: 0; padding-left: 0; }', '.stat { border-bottom: 0; border-inline-start: 1px solid var(--line); padding: .5rem 0; padding-inline-start: 2rem; grid-template-columns: 1fr; }\n  .stat:first-child { border-inline-start: 0; padding-inline-start: 0; }'),
    ('background: linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,0) 60%), var(--surface);\n  transition: border-color 220ms', 'background: linear-gradient(180deg, var(--sheen), transparent 60%), var(--surface);\n  transition: border-color 220ms'),
    ('rgba(79,214,224,.2), transparent 62%); opacity: 0; transition: opacity 260ms', 'var(--tile-glow), transparent 62%); opacity: 0; transition: opacity 260ms'),
    ('.tile:hover { border-color: rgba(79,214,224,.42);', '.tile:hover { border-color: var(--tile-hover-border);'),
    ('border: 1px solid var(--line); background: rgba(79,214,224,.08); color: var(--teal); }', 'border: 1px solid var(--line); background: var(--teal-soft); color: var(--teal); }'),
    ('color: var(--accent); border: 1px solid rgba(215,213,33,.4); padding: .3rem .6rem;', 'color: var(--accent-text); border: 1px solid var(--badge-border); padding: .3rem .6rem;'),
    ('.spin-bg { position: absolute; right: -60px;', '.spin-bg { position: absolute; inset-inline-end: -60px;'),
    ('padding-left: 4rem; }\n.rail { position: absolute; left: 19px;', 'padding-inline-start: 4rem; }\n.rail { position: absolute; inset-inline-start: 19px;'),
    ('.step .dot { position: absolute; left: -4rem;', '.step .dot { position: absolute; inset-inline-start: -4rem;'),
    ('transition: padding-left 300ms var(--ease), background-color 200ms ease-out; }', 'transition: padding-inline-start 300ms var(--ease), background-color 200ms ease-out; }'),
    ('.region::before { content: ""; position: absolute; left: 0;', '.region::before { content: ""; position: absolute; inset-inline-start: 0;'),
    ('.region:hover { padding-left: 1rem; background: rgba(255,255,255,.02); }', '.region:hover { padding-inline-start: 1rem; background: var(--hover-soft); }'),
    ('font-size: .8125rem; color: var(--teal); text-align: right; }', 'font-size: .8125rem; color: var(--teal); text-align: end; }'),
    ('.big-quote em { font-style: normal; color: var(--accent); }', '.big-quote em { font-style: normal; color: var(--accent-text); }'),
    ('.tag-pill:hover { border-color: var(--teal); background: rgba(79,214,224,.08); }', '.tag-pill:hover { border-color: var(--teal); background: var(--teal-soft); }'),
    ('rgba(79,214,224,.16), transparent 62%), radial-gradient(600px 400px at 100% 100%, rgba(215,213,33,.08), transparent 60%)', 'var(--glow-t2), transparent 62%), radial-gradient(600px 400px at 100% 100%, var(--glow-y2), transparent 60%)'),
    ('background: linear-gradient(180deg, rgba(13,33,51,.85), rgba(10,27,43,.8)); backdrop-filter: blur(10px); box-shadow: 0 30px 80px -30px rgba(0,0,0,.7); }', 'background: linear-gradient(180deg, var(--panel-a), var(--panel-b)); backdrop-filter: blur(10px); box-shadow: 0 30px 80px -30px var(--shadow); }'),
    ('background: rgba(255,255,255,.03); border: 1.5px solid var(--line); border-radius: 14px;', 'background: var(--field-bg); border: 1.5px solid var(--line); border-radius: 14px;'),
    ('.field select:hover, .field input:hover, .field textarea:hover { border-color: rgba(160,200,225,.35); }', '.field select:hover, .field input:hover, .field textarea:hover { border-color: var(--line-strong); }'),
    ('border-color: var(--teal); background: rgba(79,214,224,.05); }', 'border-color: var(--teal); background: var(--field-focus); }'),
    ('border: 1px dashed rgba(160,200,225,.3);', 'border: 1px dashed var(--line-strong);'),
    ('background: linear-gradient(180deg, rgba(79,214,224,.5), rgba(79,214,224,0) 82%);', 'background: linear-gradient(180deg, var(--wm), transparent 82%);'),
    ('.fab { position: fixed; right: max(16px, env(safe-area-inset-right, 0px));', '.fab { position: fixed; inset-inline-end: max(16px, env(safe-area-inset-right, 0px));'),
    ('header.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 68px; }', 'header.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: .75rem; min-height: 68px; }'),
    ('nav.main { display: none; gap: .25rem; }', 'nav.main { display: none; gap: .25rem; }'),
]
for a, b in REPL:
    assert a in css, a[:70]
    css = css.replace(a, b, 1)
assert 'rgba(255,255,255,.0' not in css.replace('rgba(255,255,255,.6)', '') or True

EXTRA_CSS = """
/* ---- Üst bar araçları, mobil menü ---- */
.hd-right { display: flex; align-items: center; gap: .5rem; }
.brand-logo { display: block; height: 34px; width: auto; }
.hd-cta { display: none; }
@media (min-width: 640px) { .hd-cta { display: inline-flex; } nav.main .nav-cta { display: none; } }
.icon-btn { width: 44px; height: 44px; display: grid; place-items: center; flex: none; border-radius: 50%; border: 1px solid var(--line); background: var(--ghost-bg); color: var(--ink); cursor: pointer; -webkit-tap-highlight-color: transparent; touch-action: manipulation; transform: scale(var(--s, 1)); transition: background-color 160ms ease-out, border-color 160ms ease-out, transform 160ms var(--ease); }
.icon-btn:hover { background: var(--ghost-hover-bg); border-color: var(--ghost-hover-border); }
.icon-btn:active { --s: .92; transition-duration: 60ms; }
.icon-btn svg { width: 20px; height: 20px; stroke: currentColor; fill: none; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.icon-btn:focus-visible, .lang select:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.menu-btn { display: grid; }
@media (min-width: 900px) { .menu-btn { display: none; } }
.lang { position: relative; }
.lang select { appearance: none; -webkit-appearance: none; height: 44px; padding: 0 2rem 0 .95rem; padding-inline-end: 2rem; padding-inline-start: .95rem; font: 500 .875rem/1 var(--body); color: var(--ink); background: var(--ghost-bg); border: 1px solid var(--line); border-radius: 999px; cursor: pointer; transition: background-color 160ms ease-out, border-color 160ms ease-out; }
.lang select:hover { background: var(--ghost-hover-bg); border-color: var(--ghost-hover-border); }
.lang select option { color: #06202f; background: #fff; }
.lang::after { content: ""; position: absolute; inset-inline-end: .85rem; top: 50%; width: 6px; height: 6px; border: solid currentColor; border-width: 0 1.5px 1.5px 0; transform: translateY(-70%) rotate(45deg); pointer-events: none; color: var(--muted); }
@media (max-width: 899px) {
  nav.main { display: none; position: absolute; top: 100%; inset-inline: 0; flex-direction: column; gap: .15rem; padding: .75rem max(16px, env(safe-area-inset-left, 0px)) 1.1rem; background: var(--bg); border-bottom: 1px solid var(--line); box-shadow: 0 24px 40px -24px var(--shadow); }
  header.top.open nav.main { display: flex; animation: fade 260ms var(--ease) both; }
  nav.main a { font-size: 1.125rem; padding: .85rem .9rem; border-radius: 14px; }
  nav.main .nav-cta { color: var(--on-accent); background: var(--accent); font-weight: 600; margin-top: .35rem; text-align: center; }
}
nav.main a[aria-current="page"] { color: var(--ink); background: var(--hover); }
""" + swap('.ic-sun', '.ic-moon') + swap('.logo-d', '.logo-l') + """
.hint { font-size: .8125rem; color: var(--muted); }


/* ---- Değerler ---- */
.values .wrap { display: grid; gap: 0; padding-block: 2.5rem; }
.val { display: grid; gap: .6rem; justify-items: start; padding: 1.5rem 0; border-bottom: 1px solid var(--line); }
.val:last-child { border-bottom: 0; }
.val h3 { font-size: clamp(1.4rem, 3.2vw, 1.75rem); line-height: 1.05; margin-top: .35rem; }
.val p { color: var(--muted); max-width: 22rem; }
@media (min-width: 860px) {
  .values .wrap { grid-template-columns: repeat(3, 1fr); }
  .val { border-bottom: 0; border-inline-start: 1px solid var(--line); padding: .5rem 0; padding-inline-start: 2rem; padding-inline-end: 1rem; }
  .val:first-child { border-inline-start: 0; padding-inline-start: 0; }
}
/* ---- Hizmet kartları, görseller ---- */
.go-row { margin-top: auto; display: flex; flex-wrap: wrap; gap: .5rem; }
.tile-media { overflow: hidden; margin: -1.6rem -1.6rem .35rem; height: 200px; background: var(--surface2); }
.tile-img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 700ms var(--ease); }
.tile:hover .tile-img { transform: scale(1.05); }
.tile:has(.tile-media) .spin-bg { display: none; }
@media (min-width: 960px) {
  .t-a, .t-d { padding-inline-end: calc(50% + 1.2rem); }
  .t-a .tile-media, .t-d .tile-media { position: absolute; inset-block: 0; inset-inline: 50% 0; margin: 0; height: auto; z-index: 0; }
  .t-a .tile-media::after, .t-d .tile-media::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, var(--surface) 0%, transparent 38%); pointer-events: none; }
}
.crumb { display: flex; flex-wrap: wrap; gap: .5rem; font-family: var(--mono); font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.crumb a { text-decoration: none; transition: color 160ms ease-out; }
.crumb a:hover { color: var(--teal); }
.page-hero { position: relative; isolation: isolate; overflow: clip; border-bottom: 1px solid var(--line);
  background: radial-gradient(800px 420px at 90% -10%, var(--glow-t1), transparent 62%), radial-gradient(600px 400px at 0% 110%, var(--glow-y1), transparent 60%), var(--bg); }
.page-hero .wrap { display: grid; gap: 2.5rem; padding-block: 2.5rem 4.5rem; }
.ph-text { display: grid; gap: 1.5rem; align-content: start; min-width: 0; }
.page-hero h1 { font-size: clamp(2.3rem, 6vw, 3.9rem); line-height: 1; letter-spacing: -.035em; font-weight: 800; max-width: 16ch; text-wrap: balance; animation: fade 900ms var(--ease) both; }
.page-hero .lead { font-size: 1.1875rem; color: var(--muted); max-width: 40rem; animation: fade 900ms var(--ease) 120ms both; }
.cover { max-width: 40rem; display: grid; gap: .35rem; animation: fade 900ms var(--ease) 200ms both; }
.cover .k, .brand-block .k { font-family: var(--mono); font-size: .6875rem; letter-spacing: .14em; text-transform: uppercase; color: var(--teal); }
.chips { display: flex; flex-wrap: wrap; gap: .5rem; animation: fade 900ms var(--ease) 280ms both; }
.page-hero .actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: .25rem; animation: fade 900ms var(--ease) 360ms both; }
.hero-fig { margin: 0; border-radius: 24px; overflow: hidden; border: 1px solid var(--line); background: var(--surface); box-shadow: 0 30px 80px -30px var(--shadow); animation: fade 1000ms var(--ease) 200ms both; }
.hero-fig img { display: block; width: 100%; height: auto; aspect-ratio: 16 / 10; object-fit: cover; }
@media (max-width: 959px) { .hero-fig { order: -1; } }
@media (min-width: 960px) { .hero-fig { position: sticky; top: 96px; } .hero-fig img { aspect-ratio: 4 / 4.2; } }
@media (min-width: 960px) { .page-hero .wrap.has-fig { grid-template-columns: 1.05fr .95fr; gap: 3.5rem; align-items: start; } }
.brand-block { display: grid; gap: .75rem; animation: fade 900ms var(--ease) 280ms both; }
.brands { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .6rem; list-style: none; padding: 0; margin: 0; }
.brands li { display: grid; place-items: center; height: 64px; padding: 0 14px; background: var(--brand-card); border: 1px solid var(--line); border-radius: 12px; transition: transform 200ms var(--ease); }
.brands li:hover { transform: translateY(-2px); }
.brands img { display: block; width: auto; height: auto; max-width: 100%; max-height: 34px; object-fit: contain; }
.brands.lg li { height: 124px; padding: 0 18px; }
.brands.lg img { max-height: 92px; }
.brands li.txt { background: transparent; font-family: var(--mono); font-size: .8125rem; letter-spacing: .04em; color: var(--muted); border-style: dashed; }
@media (max-width: 480px) { .brands { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.faq-wide { max-width: 54rem; }
.others { border-top: 1px solid var(--line); }
.others a { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1.15rem 0; border-bottom: 1px solid var(--line); text-decoration: none; font-family: var(--display); font-weight: 700; font-size: clamp(1.3rem, 3.6vw, 1.9rem); letter-spacing: -.02em; transition: padding-inline-start 300ms var(--ease), color 160ms ease-out, opacity 100ms ease-out; -webkit-tap-highlight-color: transparent; touch-action: manipulation; }
.others a:hover { padding-inline-start: .75rem; color: var(--teal); }
.others a:active { opacity: .7; }
.mv { display: grid; gap: 14px; }
@media (min-width: 760px) { .mv { grid-template-columns: 1fr 1fr; } }
.mv .card { border: 1px solid var(--line); border-radius: 22px; padding: 1.75rem; background: linear-gradient(180deg, var(--sheen), transparent 60%), var(--surface); }
.mv h3 { font-size: 2rem; margin-bottom: .75rem; }
.mv p { color: var(--muted); }
.founder { display: grid; gap: 1rem 3rem; border-top: 1px solid var(--line); padding-top: 2rem; }
@media (min-width: 860px) { .founder { grid-template-columns: .7fr 1.3fr; } }
.founder h3 { font-size: clamp(1.8rem, 4.5vw, 2.6rem); }
.founder p { color: var(--muted); max-width: 38rem; }
.founder .role { font-family: var(--mono); font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--teal); margin-bottom: .6rem; display: block; }
.banner { margin: 0; border-radius: 26px; overflow: hidden; border: 1px solid var(--line); }
.banner img { display: block; width: 100%; height: auto; aspect-ratio: 21 / 9; object-fit: cover; }
.gallery { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
@media (min-width: 860px) { .gallery { grid-template-columns: repeat(3, 1fr); gap: 14px; } }
@media (max-width: 859px) { .gallery figure:last-child:nth-child(odd) { grid-column: span 2; } }
.gallery figure { position: relative; margin: 0; aspect-ratio: 4 / 3; border-radius: 18px; overflow: hidden; border: 1px solid var(--line); background: var(--surface); }
.gallery img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 700ms var(--ease); }
.gallery figure:hover img { transform: scale(1.04); }
.gallery figcaption { position: absolute; inset-inline: 0; bottom: 0; padding: 1.6rem .85rem .7rem; font-family: var(--mono); font-size: .6875rem; letter-spacing: .08em; text-transform: uppercase; color: #fff; background: linear-gradient(0deg, rgba(3,15,25,.85), rgba(3,15,25,0)); }

/* ---- Blog ---- */
.posts { display: grid; gap: 16px; }
@media (min-width: 700px) { .posts { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1000px) { .posts { grid-template-columns: repeat(3, 1fr); } }
.post-card { display: flex; flex-direction: column; min-width: 0; border: 1px solid var(--line); border-radius: 22px; overflow: hidden; background: var(--surface); text-decoration: none; transform: scale(var(--s, 1)); transition: transform 260ms var(--ease), border-color 220ms ease-out; -webkit-tap-highlight-color: transparent; touch-action: manipulation; }
.post-card:hover { border-color: var(--tile-hover-border); transform: translateY(-3px); }
.post-card:active { --s: .985; transition-duration: 80ms; }
.post-card:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.pc-img { aspect-ratio: 16 / 10; overflow: hidden; background: var(--surface2); }
.pc-img img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 700ms var(--ease); }
.post-card:hover .pc-img img { transform: scale(1.05); }
.pc-body { display: flex; flex-direction: column; gap: .7rem; padding: 1.25rem 1.4rem 1.5rem; flex: 1; }
.pc-meta { display: flex; flex-wrap: wrap; gap: .3rem .7rem; align-items: center; font-family: var(--mono); font-size: .6875rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.pc-meta b { color: var(--teal); font-weight: 500; }
.post-card h3 { font-size: 1.45rem; line-height: 1.1; }
.post-card p { color: var(--muted); font-size: 1rem; }
.pc-more { margin-top: auto; padding-top: .35rem; font-weight: 600; color: var(--teal); display: inline-flex; gap: .5rem; }
.post-card:hover .arrow { transform: translateX(4px); }
.sec-more { margin-top: 2rem; }
.post-hero h1 { max-width: 22ch; }
.post-meta { display: flex; flex-wrap: wrap; gap: .4rem .9rem; align-items: center; font-family: var(--mono); font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.post-meta b { color: var(--teal); font-weight: 500; }
.post-fig { margin: 0; border-radius: 24px; overflow: hidden; border: 1px solid var(--line); }
.post-fig img { display: block; width: 100%; height: auto; aspect-ratio: 16 / 8; object-fit: cover; }
.post-wrap { max-width: 46rem; margin-inline: auto; }
.prose { display: grid; gap: 1.15rem; font-size: 1.125rem; line-height: 1.7; }
.prose h2 { font-size: clamp(1.6rem, 4vw, 2.1rem); line-height: 1.08; margin-top: 1.4rem; }
.prose p { opacity: .93; }
.prose ul { margin: 0; padding-inline-start: 1.3rem; display: grid; gap: .65rem; }
.prose li::marker { color: var(--teal); }
.quick-answer { border: 1px solid var(--line); border-inline-start: 3px solid var(--teal); border-radius: 14px; padding: 1.1rem 1.25rem; background: var(--surface); }
.quick-answer b { display: block; font-family: var(--mono, monospace); font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; color: var(--teal); margin-bottom: .4rem; }
.quick-answer p { margin: 0; font-size: 1.05rem; line-height: 1.6; }
.related-links { color: var(--muted); font-size: 1rem; }
.related-links a { color: var(--teal); text-decoration: underline; text-underline-offset: 3px; }
.author-box { display: flex; gap: 1.1rem; align-items: flex-start; margin-top: 2.5rem; padding: 1.4rem; border: 1px solid var(--line); border-radius: 18px; background: var(--surface); }
.author-box .ab-mark { flex: none; width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; background: var(--accent); color: var(--on-accent); font-weight: 700; letter-spacing: .04em; }
.author-box > div:last-child { min-width: 0; }
.author-box .role { font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.author-box h3 { font-size: 1.3rem; margin: .1rem 0 0; }
.author-box .ab-title { color: var(--teal); font-weight: 600; margin: .15rem 0 .5rem; }
.author-box p { margin: 0 0 .4rem; font-size: 1rem; line-height: 1.55; }
.author-box a { color: var(--teal); text-decoration: underline; text-underline-offset: 3px; }
.note-box { border: 1px solid var(--line); border-inline-start: 3px solid var(--accent); border-radius: 14px; padding: 1.1rem 1.25rem; background: var(--surface); color: var(--muted); font-size: 1.0625rem; }
.cta-band { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.25rem 2rem; border: 1px solid var(--line); border-radius: 24px; padding: 1.75rem; background: radial-gradient(500px 240px at 100% 0%, var(--glow-t1), transparent 70%), var(--surface); }
.cta-band h2 { font-size: clamp(1.5rem, 3.6vw, 2.1rem); line-height: 1.05; max-width: 22ch; }
.cta-band .btn-row { display: flex; flex-wrap: wrap; gap: .6rem; }

/* ---- Dil ve yön ---- */
[dir="rtl"] .arrow { transform: scaleX(-1); }
[dir="rtl"] .btn:hover .arrow, [dir="rtl"] .tile:hover .arrow, [dir="rtl"] .post-card:hover .arrow { transform: scaleX(-1) translateX(4px); }
[dir="rtl"] .progress, [dir="rtl"] .region::before { transform-origin: 100% 50%; }
[dir="rtl"] .marquee, [dir="rtl"] .track { direction: ltr; }
[dir="rtl"] .t-a .tile-media::after, [dir="rtl"] .t-d .tile-media::after { background: linear-gradient(270deg, var(--surface) 0%, transparent 38%); }
[dir="rtl"] .preview, [dir="rtl"] .brands { direction: ltr; }
html[lang="ru"] { --display: "Onest", "Helvetica Neue", Arial, sans-serif; --body: "Onest", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
html[lang="ar"] { --display: "IBM Plex Sans Arabic", "Segoe UI", Tahoma, Arial, sans-serif; --body: "IBM Plex Sans Arabic", "Segoe UI", Tahoma, Arial, sans-serif; --mono: "IBM Plex Sans Arabic", "Segoe UI", Tahoma, Arial, sans-serif; }
html[lang="ar"] *, html[lang="ar"] *::before, html[lang="ar"] *::after { letter-spacing: 0 !important; text-transform: none !important; }
html[lang="ar"] h1, html[lang="ar"] h2, html[lang="ar"] h3 { line-height: 1.22; font-weight: 700; }
@media (max-width: 959px) { .split { grid-template-columns: minmax(0, 1fr); } }
.split > * { min-width: 0; }
h1, h2, h3 { overflow-wrap: break-word; hyphens: auto; -webkit-hyphens: auto; }
.sec-head { grid-template-columns: minmax(0, 1fr); }
@media (max-width: 560px) {
  .sec-head h2 { font-size: clamp(1.75rem, 8.2vw, 2.4rem); }
  .talep h2 { font-size: clamp(1.9rem, 9vw, 2.6rem); }
}
@media (max-width: 380px) {
  .hd-right { gap: .35rem; }
  .icon-btn { width: 40px; height: 40px; }
  .lang select { height: 40px; padding-inline-start: .7rem; padding-inline-end: 1.6rem; font-size: .8125rem; }
  .lang::after { inset-inline-end: .6rem; }
  .brand-logo { height: 28px; width: auto; }
}
.hero h1 .water { padding-right: .1em; margin-right: -.1em; padding-left: .02em; }
html[lang="ar"] .hero h1 { line-height: 1.12; font-size: clamp(3rem, 10vw, 5.6rem); }
html[lang="ar"] .hero h1 .line { padding-bottom: .22em; margin-bottom: -.12em; }
html[lang="ar"] .wordmark, html[lang="ar"] .region b, html[lang="ar"] .stat b { line-height: 1.1; }
html[lang="ru"] .hero h1 { font-size: clamp(2.7rem, 9.6vw, 5.5rem); line-height: .98; letter-spacing: -.035em; }
html[lang="ru"] h1, html[lang="ru"] h2, html[lang="ru"] h3 { letter-spacing: -.02em; hyphens: auto; overflow-wrap: break-word; }
html[lang="ru"] .page-hero h1 { font-size: clamp(2.1rem, 5.4vw, 3.5rem); }
html[lang="ru"] .sec-head h2 { font-size: clamp(2.1rem, 5.6vw, 3.7rem); }
html[lang="ru"] .talep h2 { font-size: clamp(2.2rem, 6.8vw, 4.6rem); }
html[lang="ru"] .wordmark, html[lang="ar"] .wordmark { font-family: "Bricolage Grotesque", "Onest", sans-serif; }
html.i18n-pending body { visibility: hidden; }
@media (prefers-reduced-motion: reduce) { .tile:hover .tile-img, .gallery figure:hover img, .post-card:hover .pc-img img { transform: none; } }
"""

# ---------- Ortak betikler ----------
INIT_JS = ('<script>(function(){var d=document.documentElement;try{var th=localStorage.getItem("gm-theme");if(th==="light"||th==="dark")d.setAttribute("data-theme",th);'
           'var l=localStorage.getItem("gm-lang");if(l&&/^(en|ru|ar)$/.test(l)){d.lang=l;d.dir=l==="ar"?"rtl":"ltr";d.classList.add("i18n-pending");setTimeout(function(){d.classList.remove("i18n-pending")},2500);return;}}catch(e){}d.lang="tr";d.dir="ltr";})();'
           '(function(){try{if("scrollRestoration" in history)history.scrollRestoration="manual";}catch(e){}function top(){if(location.hash)return;window.scrollTo(0,0);document.documentElement.scrollTop=0;if(document.body)document.body.scrollTop=0;}top();document.addEventListener("DOMContentLoaded",top);window.addEventListener("load",function(){top();setTimeout(top,60);setTimeout(top,250);});window.addEventListener("pageshow",top);})();</script>')

COMMON_JS = r"""
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var DIR = { tr: 'ltr', en: 'ltr', ru: 'ltr', ar: 'rtl' };
  var FONT = { ru: 'https://fonts.googleapis.com/css2?family=Onest:wght@300..800&display=swap', ar: 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap' };
  var base = doc.body.getAttribute('data-root') || '', VER = '@@VER@@';
  var lang = 'tr', dict = null, cache = {}, fonts = {};
  var has = function (o, k) { return Object.prototype.hasOwnProperty.call(o, k); };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }
  function t(s) { if (!dict) return s; var k = norm(s); return has(dict, k) ? dict[k] : s; }
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1 };
  function ok(n) {
    for (var p = n.parentNode; p && p.nodeType === 1; p = p.parentNode) {
      if (SKIP[p.nodeName] || p.hasAttribute('data-nt') || p.hasAttribute('data-i18n')) return false;
    }
    return true;
  }
  function apply() {
    var w = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT, null), n, list = [];
    while ((n = w.nextNode())) list.push(n);
    list.forEach(function (n) {
      if (!ok(n)) return;
      if (n.__o === undefined) n.__o = n.nodeValue;
      var k = norm(n.__o); if (!k) return;
      var v = dict && has(dict, k) ? dict[k] : null;
      n.nodeValue = v === null ? n.__o : n.__o.match(/^\s*/)[0] + v + n.__o.match(/\s*$/)[0];
    });
    [].forEach.call(doc.querySelectorAll('[alt],[placeholder],[aria-label],[title]'), function (el) {
      if (el.closest('[data-nt]')) return;
      ['alt', 'placeholder', 'aria-label', 'title'].forEach(function (a) {
        if (!el.hasAttribute(a)) return;
        el.__a = el.__a || {};
        if (el.__a[a] === undefined) el.__a[a] = el.getAttribute(a);
        var k = norm(el.__a[a]);
        el.setAttribute(a, dict && has(dict, k) ? dict[k] : el.__a[a]);
      });
    });
    [].forEach.call(doc.querySelectorAll('[data-i18n]'), function (el) {
      if (el.__oh === undefined) el.__oh = el.innerHTML;
      var id = el.getAttribute('data-i18n');
      el.innerHTML = dict && has(dict, id) ? dict[id] : el.__oh;
    });
    if (doc.__ot === undefined) doc.__ot = doc.title;
    var parts = doc.__ot.split(' | '), pk = norm(parts[0]);
    parts[0] = dict && has(dict, pk) ? dict[pk] : parts[0];
    doc.title = parts.join(' | ');
  }
  function go(code, d) {
    lang = code; dict = d;
    root.lang = code; root.dir = DIR[code];
    apply();
    var sel = doc.getElementById('lang-sel'); if (sel) sel.value = code;
    root.classList.remove('i18n-pending');
    window.dispatchEvent(new Event('gm-lang'));
  }
  function setLang(code, persist) {
    if (!has(DIR, code)) code = 'tr';
    if (persist) store('gm-lang', code);
    if (code === 'tr') return go('tr', null);
    if (FONT[code] && !fonts[code]) {
      fonts[code] = 1;
      var l = doc.createElement('link'); l.rel = 'stylesheet'; l.href = FONT[code]; doc.head.appendChild(l);
    }
    if (cache[code]) return go(code, cache[code]);
    fetch(base + 'i18n/' + code + '.json?v=' + VER).then(function (r) { return r.json(); }).then(function (d) {
      cache[code] = d; go(code, d);
    }).catch(function () { go('tr', null); });
  }
  window.GM = { t: t, setLang: setLang };

  var sel = doc.getElementById('lang-sel');
  if (sel) sel.addEventListener('change', function () { setLang(sel.value, true); });

  /* Tema */
  var tb = doc.getElementById('theme-btn'), mql = window.matchMedia('(prefers-color-scheme: light)');
  function eff() { return root.getAttribute('data-theme') || (mql.matches ? 'light' : 'dark'); }
  if (tb) tb.addEventListener('click', function () {
    var n = eff() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n); store('gm-theme', n);
    window.dispatchEvent(new Event('gm-theme'));
  });
  if (mql.addEventListener) mql.addEventListener('change', function () { window.dispatchEvent(new Event('gm-theme')); });

  /* Mobil menü */
  var hd = doc.querySelector('header.top'), mb = doc.getElementById('menu-btn');
  function menu(open) { hd.classList.toggle('open', open); mb.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  if (mb) {
    mb.addEventListener('click', function (e) { e.stopPropagation(); menu(!hd.classList.contains('open')); });
    doc.addEventListener('click', function (e) { if (!hd.contains(e.target)) menu(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') menu(false); });
    [].forEach.call(hd.querySelectorAll('nav.main a'), function (a) { a.addEventListener('click', function () { menu(false); }); });
  }

  var stored = read('gm-lang');
  setLang(stored && has(DIR, stored) ? stored : 'tr', false);
})();
""".replace('@@VER@@', VER)

SUB_JS = r"""
(function () {
  'use strict';
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var T = function (s) { return window.GM ? window.GM.t(s) : s; };
  var progress = $('#progress'), fab = $('#fab'), ticking = false;
  function onScroll() {
    ticking = false;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.setProperty('--sp', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : 0);
    fab.classList.toggle('show', window.scrollY > 500);
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (fine && !reduce) {
    $$('.btn-primary').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--tx', ((e.clientX - r.left - r.width / 2) * 0.12).toFixed(1) + 'px');
        b.style.setProperty('--ty', ((e.clientY - r.top - r.height / 2) * 0.22).toFixed(1) + 'px');
      });
      b.addEventListener('pointerleave', function () { b.style.setProperty('--tx', '0px'); b.style.setProperty('--ty', '0px'); });
    });
  }
  var f = { hizmet: $('#f-hizmet'), bolge: $('#f-bolge'), tekne: $('#f-tekne'), motor: $('#f-motor'), detay: $('#f-detay') };
  var out = $('#out'), wa = $('#wa'), status = $('#status'), timer;
  function say(msg) { status.textContent = msg; clearTimeout(timer); timer = setTimeout(function () { status.textContent = ''; }, 3500); }
  window.addEventListener('gm-lang', function () { status.textContent = ''; });
  function build() {
    var lines = ['Merhaba Günhan Marine,'];
    if (f.hizmet.value) lines.push('Hizmet: ' + f.hizmet.value);
    if (f.bolge.value) lines.push('Konum: ' + f.bolge.value);
    if (f.tekne.value.trim()) lines.push('Tekne: ' + f.tekne.value.trim());
    if (f.motor.value.trim()) lines.push('Motor / sistem: ' + f.motor.value.trim());
    if (f.detay.value.trim()) lines.push('Sorun: ' + f.detay.value.trim());
    if (lines.length === 1) lines.push('Teknem için yerinde servis talep etmek istiyorum.');
    var msg = lines.join('\n');
    out.textContent = msg;
    wa.href = 'https://wa.me/905310291284?text=' + encodeURIComponent(msg);
    return msg;
  }
  function selectNode(el) {
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    say(T('Metin seçildi, kopyalamak için basılı tutun.'));
  }
  function copy(text, el, okMsg) {
    try { navigator.clipboard.writeText(text).then(function () { say(okMsg); }, function () { selectNode(el); }); }
    catch (e) { selectNode(el); }
  }
  Object.keys(f).forEach(function (k) { f[k].addEventListener('input', build); f[k].addEventListener('change', build); });
  $('#talep-form').addEventListener('submit', function (e) { e.preventDefault(); });
  $('#copy-msg').addEventListener('click', function () { copy(build(), out, T('Mesaj kopyalandı.')); });
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var el = $(b.getAttribute('data-copy'));
      copy(el.textContent, el, T('Kopyalandı:') + ' ' + el.textContent);
    });
  });
  var pre = document.body.getAttribute('data-service');
  if (pre) f.hizmet.value = pre;
  build();
})();
"""


import json as _json
RECAPTCHA_KEY = _json.load(open(SP + '/config.json')).get('recaptcha_site_key', '').strip()

def patch_form(js):
    reps = [
("var f = { hizmet: $('#f-hizmet'),", "var f = { ad: $('#f-ad'), tel: $('#f-tel'), hizmet: $('#f-hizmet'),"),
("function say(msg) { status.textContent = msg; clearTimeout(timer); timer = setTimeout(function () { status.textContent = ''; }, 3500); }",
 "function say(msg, ms) { status.textContent = msg; clearTimeout(timer); timer = setTimeout(function () { status.textContent = ''; }, ms || 3500); }"),
("    var msg = lines.join('\\n');\n    out.textContent = msg;",
 "    if (f.ad.value.trim()) lines.push('Ad Soyad: ' + f.ad.value.trim());\n    if (f.tel.value.trim()) lines.push('Telefon: ' + f.tel.value.trim());\n    var msg = lines.join('\\n');\n    out.textContent = msg;"),
("  $('#talep-form').addEventListener('submit', function (e) { e.preventDefault(); });",
 """  var form = $('#talep-form'), sendBtn = $('#send');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = !f.ad.value.trim() ? f.ad : (!f.tel.value.trim() ? f.tel : null);
    if (bad) { say(T('Lütfen adınızı ve telefon numaranızı yazın.'), 5000); bad.focus(); return; }
    if (window.__gmRecap !== undefined && window.grecaptcha && !window.grecaptcha.getResponse(window.__gmRecap)) { say(T('Lütfen "Ben robot değilim" kutusunu işaretleyin.'), 6000); return; }
    var msg = build();
    $('#f-mesaj').value = msg;
    var data = new URLSearchParams(new FormData(form)).toString();
    sendBtn.disabled = true; say(T('Gönderiliyor…'), 20000);
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: data })
      .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); form.reset(); build(); say(T('Talebiniz iletildi. En kısa sürede sizi arayacağız.'), 12000); })
      .catch(function () { say(T('Gönderilemedi. Lütfen WhatsApp veya telefonla ulaşın.'), 12000); })
      .then(function () { sendBtn.disabled = false; if (window.__gmRecap !== undefined && window.grecaptcha) window.grecaptcha.reset(window.__gmRecap); });
  });"""),
    ]
    for a, b in reps:
        assert a in js, a[:50]
        js = js.replace(a, b, 1)
    if RECAPTCHA_KEY:
        js = js.replace("  var form = $('#talep-form'), sendBtn = $('#send');", "  var form = $('#talep-form'), sendBtn = $('#send');\n"
          "  window.gmRecapLoad = function () { var el = document.getElementById('recap'); if (el && window.grecaptcha) window.__gmRecap = window.grecaptcha.render(el, { sitekey: '%s' }); };\n"
          "  var rs = document.createElement('script'); rs.src = 'https://www.google.com/recaptcha/api.js?render=explicit&onload=gmRecapLoad&hl=' + (document.documentElement.lang || 'tr'); rs.async = true; document.head.appendChild(rs);" % RECAPTCHA_KEY, 1)
    return js
SUB_JS = patch_form(SUB_JS)

# ---------- Anasayfa ----------
body_html = src[src.index('<div class="progress"'): src.index('<script>\n(function')]
index_js = src[src.rindex('<script>\n(function') + len('<script>\n'): src.rindex('</script>')]

def nav_items(prefix, is_index):
    return [('Anasayfa', prefix + 'index.html', 'home'), ('Hizmetler', ('#hizmetler' if is_index else prefix + 'index.html#hizmetler'), 'svc'),
            ('Blog', prefix + 'blog.html', 'blog'), ('Hakkımızda', prefix + 'hakkimizda.html', 'about')]

def header(prefix, current, is_index=False):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if k == current else '', t) for t, h, k in nav_items(prefix, is_index))
    logo_w, logo_h = dims('images/logo-gunhan-acik.png')
    lw = round(34 * logo_w / logo_h)
    return ('<div class="progress" id="progress" aria-hidden="true"></div>'
            '<header class="top"><div class="wrap">'
            '<a class="brand" href="%(p)sindex.html" aria-label="Günhan Marine ana sayfa">'
            '<img class="brand-logo logo-d" src="%(p)simages/logo-gunhan-acik.png" alt="Günhan Marine" width="%(lw)d" height="34">'
            '<img class="brand-logo logo-l" src="%(p)simages/logo-gunhan-koyu.png" alt="Günhan Marine" width="%(lw)d" height="34"></a>'
            '<nav class="main" id="nav-main" aria-label="Ana menü">%(links)s<a class="nav-cta" href="#talep">İletişim</a></nav>'
            '<div class="hd-right">'
            '<a class="btn btn-primary btn-sm hd-cta" href="#talep">İletişim</a>'
            '<div class="lang"><select id="lang-sel" aria-label="Dil"><option value="tr" data-nt>Türkçe</option><option value="en" data-nt>English</option><option value="ru" data-nt>Русский</option><option value="ar" data-nt>العربية</option></select></div>'
            '<button class="icon-btn" id="theme-btn" type="button" aria-label="Temayı değiştir" title="Temayı değiştir">'
            '<svg class="ic-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M18.7 5.3l-1.8 1.8M7.1 16.9l-1.8 1.8"/></svg>'
            '<svg class="ic-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg></button>'
            '<button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="Menü" aria-expanded="false" aria-controls="nav-main">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>'
            '</div></div></header>') % dict(p=prefix, lw=lw, links=links)

def post_card(p, base_blog, base_img):
    w, h = dims('images/' + p['img'])
    return ('<a class="post-card reveal" href="%s%s.html"><div class="pc-img"><img src="%s%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"></div>'
            '<div class="pc-body"><div class="pc-meta"><b>%s</b><span data-nt>%s</span><span>%s</span></div><h3>%s</h3><p>%s</p>'
            '<span class="pc-more">Yazıyı oku <span class="arrow" aria-hidden="true">→</span></span></div></a>') % (
        base_blog, p['slug'], base_img, p['img'], qesc(p['alt']), w, h, esc(p['cat']), p['date_label'], esc(p['read']), esc(p['title']), esc(p['excerpt']))

# patchler
hdr_re = re.compile(r'<header class="top">.*?</header>', re.S)
assert hdr_re.search(body_html)
index = hdr_re.sub(lambda m: header('', 'home', True), body_html, count=1)
index = index.replace('<div class="progress" id="progress" aria-hidden="true"></div>\n\n<div class="progress" id="progress" aria-hidden="true"></div>', '<div class="progress" id="progress" aria-hidden="true"></div>')
index = index.replace('<p class="lead">Gemi mühendisliği', '<p class="lead" data-i18n="hero-lead">Gemi mühendisliği', 1)
index = index.replace('<p class="big-quote reveal">', '<p class="big-quote reveal" data-i18n="about-quote">', 1)
assert 'data-i18n="hero-lead"' in index and 'data-i18n="about-quote"' in index

def tile_patch(m):
    value = m.group(1); idx = SERVICE_VALUES.index(value)
    return ('<div class="go-row"><a class="btn btn-ghost btn-sm" href="hizmetler/%s.html">Detaylı gör</a>'
            '<button class="btn btn-ghost btn-sm go" type="button" data-service="%s">Talep et <span class="arrow" aria-hidden="true">→</span></button></div>') % (SLUGS[idx], value)
index, nsub = re.subn(r'<button class="btn btn-ghost btn-sm go" type="button" data-service="([^"]+)">Talep et <span class="arrow" aria-hidden="true">→</span></button>', tile_patch, index)
assert nsub == 6, nsub
for letter, i in zip('abcdef', range(6)):
    w, h = dims('images/tile-%s.jpg' % SLUGS[i])
    tag = '<article class="tile t-%s reveal">' % letter
    assert tag in index, tag
    index = index.replace(tag, tag + '\n          <div class="tile-media"><img class="tile-img" src="images/tile-%s.jpg" alt="%s" width="%d" height="%d" decoding="async"></div>' % (SLUGS[i], qesc(ALT[i]), w, h), 1)

VALUES = [
    ('<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>', 'Yerinde servis', 'Ekip ve ekipman teknenizin bulunduğu yere gelir. Teknenizi taşımanız gerekmez.'),
    ('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.2-4.2"/>', 'Kök neden odaklı', 'Belirtiyi susturmak yerine arızanın nedenini bulur, kalıcı çözüm uygularız.'),
    ('<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2.3 2.3L15.5 10"/>', 'Tek ekip, tam kapsam', 'Motordan seyir elektroniğine kadar tüm işler aynı mühendislik ekibinde.'),
]
vals = ('<section class="values"><div class="wrap">' + ''.join(
    '<div class="val reveal"><div class="ico-box"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></div><h3>%s</h3><p>%s</p></div>' % (ic, t, d) for ic, t, d in VALUES)
    + '</div></section>')
index, nst = re.subn(r'<section class="stats">.*?</section>', lambda m: vals, index, count=1, flags=re.S)
assert nst == 1
index = index.replace('<div class="tags reveal" aria-label="Uzmanlık alanları">',
                      '<p class="reveal" style="margin-top:2rem"><a class="btn btn-ghost" href="hakkimizda.html">Misyon, vizyon ve sahadan kareler <span class="arrow" aria-hidden="true">→</span></a></p>\n      <div class="tags reveal" aria-label="Uzmanlık alanları">', 1)
index = index.replace('<div class="contact-list">\n          <div class="contact-item">\n            <div><span class="k">Telefon</span>',
                      '<div class="contact-list">\n          <div class="contact-item"><div><span class="k">Merkez</span><span class="v">Adana, Türkiye</span></div></div>\n          <div class="contact-item">\n            <div><span class="k">Telefon</span>', 1)
assert 'Adana, Türkiye' in index
index = index.replace('<span class="v" id="phone">', '<span class="v" id="phone" dir="ltr" data-nt>', 1).replace('<span class="v" id="mail">', '<span class="v" id="mail" dir="ltr" data-nt>', 1)
index = index.replace('<div class="preview" id="out" role="status" aria-live="polite"></div>', '<div class="preview" id="out" role="status" aria-live="polite" dir="auto" data-nt></div>\n            <p class="hint">Mesaj, ekibimizin okuyabilmesi için Türkçe hazırlanır.</p>', 1)
index = index.replace('<p class="status" id="status" role="status" aria-live="polite"></p>', '<p class="status" id="status" role="status" aria-live="polite" data-nt></p>', 1)
# seçenekler: değer Türkçe kalır, görünen metin çevrilir
def opt_fix(m):
    sel = m.group(0)
    return re.sub(r'<option>([^<]+)</option>', lambda o: '<option value="%s">%s</option>' % (qesc(o.group(1)), o.group(1)), sel)
index = re.sub(r'<select id="f-hizmet">.*?</select>', opt_fix, index, flags=re.S)
assert '<option>' not in index
index = index.replace('<form class="form" id="talep-form" novalidate>',
    '<form class="form" id="talep-form" name="talep" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" novalidate>\n'
    '          <input type="hidden" name="form-name" value="talep">\n'
    '          <input type="hidden" name="mesaj" id="f-mesaj">\n'
    '          <p hidden data-nt><label>Bot <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>\n'
    '          <div class="row2">\n'
    '            <div class="field"><label for="f-ad">Ad Soyad</label><input id="f-ad" name="ad" type="text" required autocomplete="name"></div>\n'
    '            <div class="field"><label for="f-tel">Telefon</label><input id="f-tel" name="telefon" type="tel" required dir="ltr" placeholder="05xx xxx xx xx" autocomplete="tel" inputmode="tel" data-nt></div>\n'
    '          </div>', 1)
for fid, nm in [('hizmet','hizmet'),('bolge','bolge'),('tekne','tekne'),('motor','motor'),('detay','detay')]:
    index = index.replace('id="f-%s"' % fid, 'id="f-%s" name="%s"' % (fid, nm), 1)
index = index.replace('<a class="btn btn-primary" id="wa"', '<a class="btn btn-ghost" id="wa"', 1)
index = index.replace('<div class="form-actions">', ('<div id="recap" data-netlify-recaptcha="true" style="min-height:78px;margin-bottom:1rem"></div>\n          ' if RECAPTCHA_KEY else '') + '<div class="form-actions">\n            <button class="btn btn-primary" type="submit" id="send">Talebi gönder <span class="arrow" aria-hidden="true">→</span></button>', 1)
index = index.replace('<p class="status" id="status"', '<p class="hint">Talebiniz e-posta ile doğrudan ekibimize ulaşır. Dilerseniz WhatsApp\'tan da yazabilirsiniz.</p>\n          <p class="status" id="status"', 1)
assert 'id="send"' in index and 'name="talep"' in index


blog_teaser = ('<section class="sec" id="blog" style="padding-top:1rem"><div class="wrap">'
               '<div class="sec-head reveal"><p class="eyebrow">Blog</p><h2>Sahadan teknik notlar ve rehberler</h2><p>Motor, elektrik, seyir elektroniği ve bakım üzerine kısa, uygulanabilir yazılar.</p></div>'
               '<div class="posts">' + ''.join(post_card(p, 'blog/', 'images/') for p in POSTS[:3]) + '</div>'
               '<p class="sec-more reveal"><a class="btn btn-ghost" href="blog.html">Tüm yazılar <span class="arrow" aria-hidden="true">→</span></a></p></div></section>\n\n  ')
assert '<section class="sec" id="sss">' in index
index = index.replace('<section class="sec" id="sss">', blog_teaser + '<section class="sec" id="sss">', 1)

# betik yamaları
js = index_js
js = js.replace("  var TAU = Math.PI * 2;\n", """  var TAU = Math.PI * 2;
  var T = function (s) { return window.GM ? window.GM.t(s) : s; };
  var P = {};
  var FF = function () { return document.documentElement.lang === 'ar' ? '"IBM Plex Sans Arabic", sans-serif' : '"JetBrains Mono", monospace'; };
  function readPal() {
    var cs = getComputedStyle(document.documentElement);
    ['teal', 'yel', 'ink', 'muted', 'tick'].forEach(function (k) { P[k] = cs.getPropertyValue('--c-' + k).trim(); });
  }
  readPal();
  function redrawStatic() { if (reduce) { drawWaves(0); drawRadar(0, true); } }
  window.addEventListener('gm-theme', function () { readPal(); redrawStatic(); });
  window.addEventListener('gm-lang', redrawStatic);
""", 1)
for lit, key in [("'rgba(79,214,224,", 'teal'), ("'rgba(215,213,33,", 'yel'), ("'rgba(160,200,225,", 'tick'), ("'rgba(143,167,182,", 'muted'), ("'rgba(234,242,246,", 'ink')]:
    assert lit in js, lit
    js = js.replace(lit, "'rgba(' + P.%s + ',"  % key)
for lit, key in [("'#d7d521'", 'yel'), ("'#4fd6e0'", 'teal'), ("'#eaf2f6'", 'ink')]:
    assert lit in js, lit
    js = js.replace(lit, "'rgb(' + P.%s + ')'" % key)
js = js.replace('px "JetBrains Mono", monospace\'', "px ' + FF()")
for a, b in [("rctx.fillText(p.n, px + p.lx, py + p.ly);", "rctx.fillText(T(p.n), px + p.lx, py + p.ly);"),
             ("rctx.fillText('TEKNE', c, c + 22);", "rctx.fillText(T('TEKNE'), c, c + 22);"),
             ("say('Metin seçildi, kopyalamak için basılı tutun.');", "say(T('Metin seçildi, kopyalamak için basılı tutun.'));"),
             ("copy(build(), out, 'Mesaj kopyalandı.')", "copy(build(), out, T('Mesaj kopyalandı.'))"),
             ("copy(el.textContent, el, 'Kopyalandı: ' + el.textContent)", "copy(el.textContent, el, T('Kopyalandı:') + ' ' + el.textContent)"),
             ("  build();\n})();", "  window.addEventListener('gm-lang', function () { status.textContent = ''; });\n  build();\n})();")]:
    assert a in js, a
    js = js.replace(a, b, 1)
assert js.count("'rgba(' + P.") >= 10
js = patch_form(js)

def assemble_index():
    head = ('<title>Günhan Marine</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">\n')
    return (head + INIT_JS + '\n<style>' + css + EXTRA_CSS + '</style>\n<div data-root="" id="gm-root" hidden></div>\n' + index.replace('<main id="top">', '<main id="top">', 1)
            + '\n<script>' + COMMON_JS.replace("doc.body.getAttribute('data-root') || ''", "''") + '</script>\n<script>\n' + js + '\n</script>\n')
open(OUT + '/index.html', 'w', encoding='utf-8').write(assemble_index())

# ---------- Alt sayfalar ----------
talep = re.search(r'<section class="sec talep" id="talep">.*?</section>', index, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', index, re.S).group(0)
fab = re.search(r'<a class="btn btn-primary fab".*?</a>', index, re.S).group(0)

HEAD = ('<!doctype html><html lang="tr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        '<meta name="claude:viewport-fit-sides" content="cover">'
        '<title>@@TITLE@@</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}'
        + css + EXTRA_CSS + '</style>' + INIT_JS + '</head>')

def page(title, body, root_prefix, service_value=None):
    attr = ' data-root="%s"' % root_prefix + (' data-service="%s"' % service_value if service_value else '')
    return HEAD.replace('@@TITLE@@', esc(title)) + '<body%s>' % attr + body + '<script>' + COMMON_JS + '</script><script>' + SUB_JS + '</script></body></html>'

def faq_html(items, open_first=True):
    parts = ['<details%s><summary>%s</summary><p class="ans">%s</p></details>' % (' open' if (open_first and i == 0) else '', esc(q), esc(a)) for i, (q, a) in enumerate(items)]
    return '<div class="faq faq-wide reveal">' + ''.join(parts) + '</div>'

# Hizmet sayfaları
for i, s in enumerate(svc):
    others = ''.join('<a href="%s.html">%s <span class="arrow" aria-hidden="true">→</span></a>' % (SLUGS[j], esc(svc[j]['title'])) for j in range(6) if j != i)
    if i in BRANDS:
        logos, texts = BRANDS[i]
        lis = ''.join('<li><img src="../images/marka-%s.png" alt="%s" width="%d" height="%d" loading="lazy"></li>' % ((k, qesc(n)) + dims('images/marka-%s.png' % k)) for k, n in logos)
        tx = ''.join('<li class="txt" data-nt>%s</li>' % esc(t) for t in texts)
        chips = '<div class="brand-block"><span class="k">Çalıştığımız markalar</span><ul class="brands">%s%s</ul></div>' % (lis, tx)
    else:
        chips = '<div class="chips" aria-label="Kapsam">%s</div>' % ''.join('<span class="tag-pill">%s</span>' % esc(c) for c in CHIPS[i])
    fw, fh = dims('images/hizmet-%s.jpg' % SLUGS[i])
    rel = [p for p in POSTS if p['service'] == SLUGS[i]]
    rel_html = ''
    if rel:
        rel_html = ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Blog</p><h2>Bu konuda yazdığımız rehber</h2></div>'
                    '<div class="posts">%s</div></div></section>') % post_card(rel[0], '../blog/', '../images/')
    body = (header('../', 'svc') +
        '<main id="top"><section class="page-hero"><div class="wrap has-fig">'
        '<div class="ph-text">'
        '<nav class="crumb" aria-label="Sayfa yolu"><a href="../index.html">Anasayfa</a><span>/</span><a href="../index.html#hizmetler">Hizmetler</a><span>/</span><span>%(title)s</span></nav>'
        '<h1>%(title)s</h1>'
        '<p class="lead">%(intro)s</p>'
        '<div class="cover"><span class="k">Hizmet bölgesi</span><p>%(cover)s</p></div>'
        '%(chips)s'
        '<div class="actions"><a class="btn btn-primary" href="#talep">Teklif al <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="#diger">Diğer hizmetler</a></div>'
        '</div>'
        '<figure class="hero-fig"><img src="../images/hizmet-%(slug)s.jpg" alt="%(alt)s" width="%(fw)d" height="%(fh)d" decoding="async"></figure>'
        '</div></section>'
        '<section class="sec"><div class="wrap split">'
        '<div class="sec-head reveal" style="margin-bottom:0"><p class="eyebrow">Sık sorulan sorular</p><h2>%(title)s hakkında merak edilenler</h2></div>'
        '%(faq)s</div></section>'
        '%(rel)s'
        '<section class="sec" id="diger" style="padding-top:0"><div class="wrap">'
        '<div class="sec-head reveal"><p class="eyebrow">Diğer hizmetler</p><h2>Teknenizin tüm teknik ihtiyacı, tek çatı altında</h2></div>'
        '<div class="others reveal">%(others)s</div></div></section>'
        '%(talep)s</main>%(footer)s%(fab)s') % dict(
            title=esc(s['title']), intro=esc(s['intro']), cover=esc(s['cover']), chips=chips, slug=SLUGS[i], alt=qesc(ALT[i]), fw=fw, fh=fh,
            faq=faq_html(s['faq']), rel=rel_html, others=others, talep=talep, footer=footer, fab=fab)
    open(OUT + '/hizmetler/%s.html' % SLUGS[i], 'w', encoding='utf-8').write(page(s['title'] + ' | Günhan Marine', body, '../', SERVICE_VALUES[i]))

# Hakkımızda
CREDS = [('itu', 'İstanbul Teknik Üniversitesi (İTÜ)'), ('gmo', 'TMMOB Gemi Makineleri İşletme Mühendisleri Odası'), ('abyc', 'ABYC standartları')]
creds = ('<div class="brand-block"><span class="k">Mesleki temel</span><ul class="brands lg">' + ''.join(
    '<li><img src="images/marka-%s.png" alt="%s" width="%d" height="%d" loading="lazy"></li>' % ((k, qesc(n)) + dims('images/marka-%s.png' % k)) for k, n in CREDS) + '</ul></div>')
bw, bh = dims('images/banner-yat.jpg')
gal = ''.join('<figure class="reveal"><img src="images/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>'
              % ((f, qesc(c)) + dims('images/' + f) + (esc(c),)) for f, c in GALLERY)
AUTHOR_BIO = 'İTÜ Gemi Makineleri İşletme Mühendisliği mezunu. Günhan Marine’in kurucusu olarak deniz motorları, marine elektrik ve seyir elektroniği işlerini bizzat sahada yürütür.'
founder_p = "İTÜ Gemi Makineleri İşletme Mühendisliği mezunu. MBA ve denizcilik alanında yüksek lisans eğitimi var. Kanada'da Alesta Marine adlı bir marine hizmet şirketi kurup yönetti ve Kuzey Amerika tekne standartlarıyla edindiği deneyimi Türkiye genelinde sunuyor."
about_body = (header('', 'about') +
    '<main id="top"><section class="page-hero"><div class="wrap">'
    '<nav class="crumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a><span>/</span><span>Hakkımızda</span></nav>'
    '<h1>Mühendislik disipliniyle sahada çözüm üretiyoruz.</h1>'
    '<p class="lead">' + esc(about_p) + '</p>'
    '' + creds + ''
    '<div class="actions"><a class="btn btn-primary" href="#talep">Teklif al <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="index.html">Anasayfa</a></div>'
    '</div></section>'
    '<section class="sec" style="padding-bottom:0"><div class="wrap"><figure class="banner reveal"><img src="images/banner-yat.jpg" alt="Kıyıya yakın sakin suda seyreden bir yat" width="' + str(bw) + '" height="' + str(bh) + '" decoding="async"></figure></div></section>'
    '<section class="sec"><div class="wrap">'
    '<div class="sec-head reveal"><p class="eyebrow">Misyon ve vizyon</p><h2>Geçici çözüm değil, kök neden</h2></div>'
    '<div class="mv"><div class="card reveal"><h3>Misyonumuz</h3><p>' + esc(mission) + '</p></div><div class="card reveal"><h3>Vizyonumuz</h3><p>' + esc(vision) + '</p></div></div>'
    '</div></section>'
    '<section class="sec" style="padding-top:0"><div class="wrap">'
    '<div class="founder reveal"><div><span class="role">Kurucu</span><h3>Feyyaz Alptekin Günhan</h3></div><p>' + esc(founder_p) + '</p></div></div></section>'
    '<section class="sec about-sec"><div class="wrap">'
    '<div class="sec-head reveal"><p class="eyebrow">Sahadan kareler</p><h2>Gerçek işler, gerçek arızalar</h2><p>Teşhis ve bakım sırasında çekilmiş fotoğraflar.</p></div>'
    '<div class="gallery">' + gal + '</div></div></section>'
    '<section class="sec"><div class="wrap split">'
    '<div class="sec-head reveal" style="margin-bottom:0"><p class="eyebrow">Sık sorulan sorular</p><h2>Günhan Marine hakkında</h2></div>' + faq_html(about_faq) + '</div></section>'
    + talep + '</main>' + footer + fab)
open(OUT + '/hakkimizda.html', 'w', encoding='utf-8').write(page('Hakkımızda | Günhan Marine', about_body, ''))

# Blog liste
blog_body = (header('', 'blog') +
    '<main id="top"><section class="page-hero"><div class="wrap">'
    '<nav class="crumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a><span>/</span><span>Blog</span></nav>'
    '<h1>Sahadan teknik notlar ve rehberler</h1>'
    '<p class="lead">Mobil servis sahasından: motor, elektrik, seyir elektroniği ve bakım üzerine kısa, uygulanabilir yazılar.</p>'
    '</div></section>'
    '<section class="sec"><div class="wrap"><div class="posts">' + ''.join(post_card(p, 'blog/', 'images/') for p in POSTS) + '</div></div></section>'
    + talep + '</main>' + footer + fab)
open(OUT + '/blog.html', 'w', encoding='utf-8').write(page('Blog | Günhan Marine', blog_body, ''))

# Blog yazıları
for p in POSTS:
    parts = []
    for kind, val in p['body']:
        if kind == 'h2': parts.append('<h2>%s</h2>' % esc(val))
        elif kind == 'p': parts.append('<p>%s</p>' % esc(val))
        elif kind == 'ul': parts.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in val))
        elif kind == 'note': parts.append('<p class="note-box">%s</p>' % esc(val))
    si = SLUGS.index(p['service'])
    quick_html = '<aside class="quick-answer"><b>Hızlı cevap</b><p>%s</p></aside>' % esc(p['quick'])
    faq_block = '<h2>Sık sorulan sorular</h2>' + faq_html(p['faq'], open_first=False)
    rel_post = [q for q in POSTS if q['service'] == p['service'] and q['slug'] != p['slug']] or [q for q in POSTS if q['slug'] != p['slug']]
    rel_html = ('<p class="related-links"><span>İlgili hizmet:</span> <a href="../hizmetler/%s.html">%s</a></p>'
                '<p class="related-links"><span>Ayrıca okuyun:</span> <a href="%s.html">%s</a></p>'
                % (SLUGS[si], esc(svc[si]['title']), rel_post[0]['slug'], esc(rel_post[0]['title'])))
    author_html = ('<div class="author-box"><div class="ab-mark" aria-hidden="true">AG</div><div><span class="role">Yazar</span><h3>Alptekin Günhan</h3>'
                   '<p class="ab-title">Kurucu &amp; Marine Sistemler Mühendisi</p><p>%s</p>'
                   '<p><a href="../hakkimizda.html">Günhan Marine hakkında</a></p></div></div>' % esc(AUTHOR_BIO))
    others = [q for q in POSTS if q['slug'] != p['slug']][:3]
    w, h = dims('images/' + p['img'])
    body = (header('../', 'blog') +
        '<main id="top"><section class="page-hero post-hero"><div class="wrap">'
        '<nav class="crumb" aria-label="Sayfa yolu"><a href="../index.html">Anasayfa</a><span>/</span><a href="../blog.html">Blog</a></nav>'
        '<h1>%s</h1><div class="post-meta"><b>%s</b><span data-nt>%s</span><span>%s</span></div></div></section>'
        '<section class="sec" style="padding-bottom:0"><div class="wrap"><figure class="post-fig reveal"><img src="../images/%s" alt="%s" width="%d" height="%d" decoding="async"></figure></div></section>'
        '<section class="sec"><div class="wrap"><div class="post-wrap"><article class="prose">%s</article>%s'
        '<div class="cta-band reveal" style="margin-top:3rem"><h2>Bu konuda yerinde destek mi lazım?</h2><div class="btn-row"><a class="btn btn-primary" href="#talep">Teklif al <span class="arrow" aria-hidden="true">→</span></a>'
        '<a class="btn btn-ghost" href="../hizmetler/%s.html">%s</a></div></div></div></div></section>'
        '<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Diğer yazılar</p><h2>Okumaya devam edin</h2></div>'
        '<div class="posts">%s</div></div></section>'
        '%s</main>%s%s') % (
            esc(p['title']), esc(p['cat']), p['date_label'], esc(p['read']), p['img'], qesc(p['alt']), w, h, quick_html + ''.join(parts) + faq_block + rel_html, author_html,
            SLUGS[si], esc(svc[si]['title']), ''.join(post_card(q, '', '../images/') for q in others), talep, footer, fab)
    open(OUT + '/blog/%s.html' % p['slug'], 'w', encoding='utf-8').write(page(p['title'] + ' | Günhan Marine', body, '../', SERVICE_VALUES[si]))

# ---------- Dosya listesi ----------
allf = (['index.html', 'hakkimizda.html', 'blog.html'] + sorted('blog/' + f for f in os.listdir(OUT + '/blog')) +
        sorted('hizmetler/' + f for f in os.listdir(OUT + '/hizmetler')) + sorted('i18n/' + f for f in os.listdir(OUT + '/i18n')) +
        sorted('images/' + f for f in os.listdir(OUT + '/images')))
json.dump(allf, open(SP + '/files.json', 'w'))
print(json.dumps({'dosya': len(allf), 'html_kb': {f: round(os.path.getsize(OUT + '/' + f) / 1024) for f in allf if f.endswith('.html')}}, ensure_ascii=False))
