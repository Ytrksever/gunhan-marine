# Günhan Marine sitesi

Netlify bu depodan siteyi derler: `python3 build.py && python3 mkdict.py && python3 deploy.py` (çıktı: `site/`).

## Haftalık blog yayını
Her yazının `blog_extra.py` içinde bir yayın tarihi vardır (`DATES`). Tarihi gelmemiş yazılar siteye, sitemap'e, RSS'e ve llms.txt'ye girmez.
Her Pazartesi GitHub Actions Netlify'ı yeniden derletir; tarihi gelen yazı kendiliğinden yayına girer ve IndexNow'a bildirilir.

## Yeni yazı eklemek
1. `blog_extra.py` > `NEW_POSTS` listesine yazıyı ekle (slug, başlık, quick, body, faq) ve `DATES` içine tarihini yaz.
2. `python3 build.py && python3 extract.py` çalıştır (strings.json'a yeni metinler eklenir).
3. `tx/en_6.txt`, `tx/ru_6.txt`, `tx/ar_6.txt` dosyalarına çevirileri `numara|||metin` biçiminde ekle; `mkdict.py` içindeki `for part in (0,1,2,3,4,5,6)` satırına 5'i ekle.
4. `git push`. Yayın tarihi geldiğinde site kendisi günceller.
