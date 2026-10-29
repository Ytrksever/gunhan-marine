"""Derlenmiş sayfalardan çevrilecek metinleri çıkarır. strings.json yalnızca eklenir (numaralar sabit kalır)."""
import os, re, json, sys
from bs4 import BeautifulSoup, NavigableString, Comment

SP = os.path.dirname(os.path.abspath(__file__))
B = SP + '/build'
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
LETTER = re.compile(r'[^\W\d_]')
SKIP = {'script', 'style', 'noscript', 'textarea'}
EXTRA = ['MARİNA', 'TERSANE', 'ÇEKEK', 'TEKNE', 'Lütfen "Ben robot değilim" kutusunu işaretleyin.', 'Lütfen adınızı ve telefon numaranızı yazın.', 'Gönderiliyor…', 'Talebiniz iletildi. En kısa sürede sizi arayacağız.', 'Gönderilemedi. Lütfen WhatsApp veya telefonla ulaşın.', 'Metin seçildi, kopyalamak için basılı tutun.', 'Mesaj kopyalandı.', 'Kopyalandı:', 'MERSİN', 'HATAY', 'ADANA', 'K']

pages = ['index.html', 'hakkimizda.html', 'blog.html']
pages += sorted('blog/' + f for f in os.listdir(B + '/blog'))
pages += sorted('hizmetler/' + f for f in os.listdir(B + '/hizmetler'))

found = []  # sırayla bulunan anahtarlar
def add(k):
    if k and k not in found: found.append(k)

def blocked(el):
    p = el
    while p is not None and getattr(p, 'name', None):
        if p.name in SKIP or p.has_attr('data-nt') or p.has_attr('data-i18n'):
            return True
        p = p.parent
    return False

units = {}
for pg in pages:
    soup = BeautifulSoup(open(B + '/' + pg, encoding='utf-8').read(), 'html.parser')
    t = soup.title.string if soup.title else ''
    if t: add(norm(t.split(' | ')[0]))
    body = soup.body
    if pg == 'index.html':  # ana sayfada skeleton olmayabilir
        body = soup
    for n in body.find_all(string=True):
        if isinstance(n, Comment): continue
        if n.parent.name == 'title' or n.find_parent('head') is not None: continue
        if blocked(n.parent): continue
        k = norm(str(n))
        if k and LETTER.search(k): add(k)
    for el in body.find_all(True):
        if el.find_parent(attrs={'data-nt': True}) is not None or el.has_attr('data-nt'): continue
        for a in ('alt', 'placeholder', 'aria-label', 'title'):
            if el.has_attr(a) and el.name != 'title':
                k = norm(el[a])
                if k and LETTER.search(k): add(k)
        if el.has_attr('data-i18n'):
            units[el['data-i18n']] = el.decode_contents()
for e in EXTRA: add(e)

path = SP + '/strings.json'
old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else []
have = {x['k'] for x in old}
new = [{'k': k} for k in found if k not in have]
for uid, h in units.items():
    if uid not in have: new.append({'k': uid, 'unit': True, 'src': norm(h)})
allx = old + new
json.dump(allx, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('toplam', len(allx), 'yeni', len(new))
if len(sys.argv) > 1:
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for i, x in enumerate(allx[a:b], a):
        print('%d\t%s' % (i, x.get('src', x['k']) if x.get('unit') else x['k']) + ('  [HTML birimi: %s]' % x['k'] if x.get('unit') else ''))
