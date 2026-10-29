"""Her hafta yayına giren yazıları IndexNow'a (Bing, Yandex vb.) bildirir. Tarihi son 7 gün içinde olan yazılar gönderilir."""
import json, datetime, urllib.request
from blog_data import POSTS
DOMAIN = 'https://gunhanmarine.com'; KEY = open('.indexnow-key').read().strip()
today = datetime.date.today()
fresh = [p for p in POSTS if 0 <= (today - datetime.date.fromisoformat(p['date'])).days < 7]
if not fresh:
    print('Bu hafta yeni yazı yok.'); raise SystemExit
urls = [DOMAIN + '/blog.html', DOMAIN + '/sitemap.xml'] + [DOMAIN + '/blog/' + p['slug'] + '.html' for p in fresh]
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps({'host': 'gunhanmarine.com', 'key': KEY, 'keyLocation': DOMAIN + '/' + KEY + '.txt', 'urlList': urls}).encode(), headers={'Content-Type': 'application/json; charset=utf-8'})
print(urllib.request.urlopen(req, timeout=30).status, urls)
