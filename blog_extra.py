# Blog iskeleti: hızlı cevap, SSS, yerel (şehir) notu. Yerellik yalnızca blog yazılarında.
EXTRA = {
 'ikinci-el-tekne-alirken-motor-ve-elektrik-kontrol-listesi': dict(
  quick='İkinci el teknede en kritik kontroller motor kompresyonu ve çalışma davranışı, akü ile şarj sisteminin yük altındaki durumu ve pano kablolamasının kalitesidir. Gövde survey ayrı bir iştir; biz yalnızca motor, mekanik ve elektrik ekspertizi yapıyoruz.',
  faq=[('Ekspertiz raporu ne zaman teslim edilir?', 'Rapor, ödemeden sonra 24 saat içinde yazılı ve fotoğraflı olarak teslim edilir. Bulgular acil, yakın vadeli ve izlenebilir olarak ayrılır.'),
       ('Gövde veya karina survey de yapıyor musunuz?', 'Hayır. Gövde, karina ve yapısal survey kapsam dışıdır. Motor, mekanik ve elektrik sistemlerinin teknik durumunu değerlendiririz.'),
       ('Teknem Adana, Mersin, Bodrum veya İstanbul’da; ekspertiz için gelir misiniz?', 'Evet. Ekip, teknenin bulunduğu marinaya ya da çekek yerine gelir. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Alanya, Antalya ve İstanbul için de randevuya göre planlama yapılır.')]),
 'deniz-motoru-periyodik-bakim-rehberi': dict(
  quick='Her sezon motor yağı ve filtresi, yakıt filtresi ile su ayırıcı, deniz suyu pompası impeller’i, kayışlar ve soğutma devresi kontrol edilmelidir. Kesin aralıklar için üreticinin kullanım kılavuzu esas alınır.',
  faq=[('Impeller ne sıklıkla kontrol edilmeli?', 'Üreticinin önerdiği aralığa uyun. Pratikte her sezon başında kontrol edilir; aşınmış, çatlamış veya kanat kaybetmiş impeller değiştirilir, çünkü yırtılan bir impeller soğutmayı bir anda bitirebilir.'),
       ('Kışlamada motor için en önemli adım nedir?', 'Soğutma devresinin tatlı suyla yıkanması, yağın değiştirilmesi, yakıt sisteminin korunması ve aküyü şarjda tutmak temel adımlardır.'),
       ('Adana, Mersin veya Hatay dışında periyodik bakım yapıyor musunuz?', 'Evet. Ekip, teknenin bulunduğu yere gelir. Bodrum, Alanya, Antalya ve İstanbul gibi noktalar için de randevuya göre planlama yapılır.')]),
 'tutya-cinko-nedir-ne-zaman-degistirilir': dict(
  quick='Tutya (çinko), pervane, şaft ve motor gibi değerli metalleri korumak için bilerek aşınan bir metaldir. Yaklaşık yarısı eridiğinde değiştirilir; tuzlu suda çinko veya alüminyum, tatlı suda magnezyum tercih edilir.',
  faq=[('Tutyanın üzerini boyayabilir miyim?', 'Hayır. Boya tutyayı işlevsiz bırakır. Tutya çıplak ve temiz yüzeyle suya temas etmelidir.'),
       ('Göl botu ile deniz teknesi için tutya aynı mı olur?', 'Hayır. Tatlı suda (göl, baraj) magnezyum, tuzlu suda çinko veya alüminyum kullanılır. Tekne tatlı sudan tuzlu suya geçiyorsa seçim gözden geçirilmelidir.'),
       ('Seyhan Baraj Gölü’nde ve Akdeniz’de tutya kontrolü yaptırabilir miyim?', 'Evet. Adana’da göl kıyısında, Mersin ve Hatay’da marina ve çekek yerlerinde yerinde kontrol yaparız. Bodrum, Antalya, Alanya ve İstanbul için de randevuya göre planlama yapılır.')]),
 'tekne-aku-bakimi-ve-test': dict(
  quick='Akü sağlığı yalnızca voltajla anlaşılmaz; dinlenmiş ve dolu bir kurşun-asit akü yaklaşık 12,6–12,8 volt gösterir ama yük altında çökebilir. Asıl karar yük testi veya kapasite ölçümüyle verilir.',
  faq=[('Marş aküsü ile servis aküsü arasındaki fark nedir?', 'Marş aküsü motoru çalıştırmak için kısa süreli yüksek akım verir. Servis (derin döngülü) akü lamba, buzdolabı ve elektronik cihazları uzun süre besler. İkisini karıştırmak ömrü kısaltır.'),
       ('Akü ne zaman değişmeli?', 'Şarj olmasına rağmen çabuk boşalıyorsa, yük testini geçemiyorsa veya kasasında şişme ve sızıntı varsa değiştirme zamanı gelmiştir.'),
       ('Akü testi için Mersin, Hatay veya Bodrum’a gelir misiniz?', 'Evet. Yük testi ve şarj sistemi kontrolü teknenin bulunduğu yerde yapılır. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Antalya, Alanya ve İstanbul için de randevuya göre planlama yapılır.')]),
 'nmea-2000-agi-nasil-calisir': dict(
  quick='NMEA 2000, seyir ve motor cihazlarını tek bir ana hat üzerinden haberleştiren standarttır. Ana hattın iki ucunda birer sonlandırıcı bulunmalı ve ağ tek bir noktadan beslenmelidir; aralıklı çalışan göstergelerin nedeni çoğunlukla ağ kurulumudur.',
  faq=[('Ağda kaç sonlandırıcı (terminatör) olmalı?', 'Ana hattın her iki ucunda birer tane, toplam iki sonlandırıcı bulunmalıdır. Eksik veya fazla sonlandırıcı veri kaybına yol açar.'),
       ('Farklı marka cihazlar aynı NMEA 2000 ağında çalışır mı?', 'Çoğu zaman çalışır; Garmin, Raymarine, Simrad ve Furuno gibi markaların çoğu NMEA 2000 kullanır. Yine de yeni cihaz almadan önce uyumluluğu kontrol etmek gerekir.'),
       ('Chartplotter ve otopilot kurulumu için Alanya, Antalya veya İstanbul’a gelir misiniz?', 'Evet. Kurulum ve kalibrasyon teknenin bulunduğu marinada yapılır. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Alanya, Antalya ve İstanbul için de randevuya göre planlama yapılır.')]),
}

NEW_POSTS = [
 dict(slug='tekne-kablo-kesiti-ve-pabuc-secimi',
  title='Tekne kablo kesiti nasıl seçilir? Pabuç ve sıkma hataları',
  cat='Marine elektrik', read='5 dk okuma', img='hizmet-marine-elektrik-guc-yonetimi.jpg',
  alt='Akü bankı, invertör, sigorta kutuları ve ana şalter', service='marine-elektrik-guc-yonetimi',
  excerpt='Kablo kesiti akıma ve gerilim düşümüne göre seçilir. Kalaylı kablo, doğru pabuç ve uygun sıkma pensesiyle yapılan bağlantı, teknede çıkabilecek ısınma ve yangın riskini azaltır.',
  quick='Kablo kesiti akıma, kablo boyuna ve izin verilen gerilim düşümüne göre seçilir. 12 volt sistemde gerilim düşümü seyir ışıkları ve elektronikte yaklaşık %3, diğer yüklerde yaklaşık %10 ile sınırlanır. Teknede kalaylı, çok telli bakır kablo ve uygun sıkma pensesiyle takılmış pabuç kullanılır.',
  body=[
   ('p', 'Teknede ısınan kablo, çoğu zaman yanlış seçilmiş kesitin veya kötü sıkılmış bir pabucun sonucudur. İnce kablo akımı taşır gibi görünür ama gerilimi düşürür, ısınır ve cihazlar yanlış davranır. Doğru kesit ve sağlam bağlantı, marine elektrikte en ucuz önlemdir.'),
   ('h2', 'Kesiti belirleyen üç değer'),
   ('ul', ['Akım: Yükün çektiği amper değeri. Sigorta ve kablo bu değere göre seçilir.', 'Kablo boyu: Gidiş ve dönüş hattının toplamı hesaba katılır, yalnızca gidiş değil.', 'İzin verilen gerilim düşümü: Seyir ışıkları ve elektronik için yaklaşık %3, diğer yükler için yaklaşık %10 kabul edilir.']),
   ('p', 'Pratik hesap: Kesit (mm²) ≈ 2 × boy (m) × akım (A) × 0,0172 ÷ izin verilen gerilim düşümü (V). Örneğin 12 volt sistemde 10 amper çeken ve 6 metre uzaktaki bir yük için %3 sınırı 0,36 volttur. Hesap yaklaşık 5,7 mm² verir, yani bir üst standart kesit olan 6 mm² seçilir.'),
   ('h2', 'Neden kalaylı ve çok telli kablo?'),
   ('p', 'Tuzlu ve nemli ortamda çıplak bakır kararır, direnci artar ve tel uçlarından içeri doğru yeşil korozyon ilerler. Kalaylı bakır bu etkiye karşı çok daha dayanıklıdır. Çok telli esnek kablo titreşime dayanır; tek telli ev kablosu teknede zamanla kırılır.'),
   ('h2', 'Pabuç ve sıkma hataları'),
   ('ul', ['Kabloyu pabuç kesitine uymayan bir pabuçla bağlamak.', 'Pabucu pense veya çekiçle ezmek. Altıgen veya çukur profilli bir sıkma pensesi kullanılmalıdır.', 'Bağlantıyı yalnızca lehimle yapmak. Titreşimde lehimli nokta kırılır.', 'Isıyla büzüşen, yapışkanlı kılıf kullanmadan bağlantıyı açıkta bırakmak.', 'Çıplak teli pabucun dışına taşırmak veya yalıtımı pabucun içine sıkıştırmak.']),
   ('h2', 'Sigorta kabloyu korur'),
   ('p', 'Sigorta, kablonun taşıyabileceği akıma göre seçilir ve kaynağa, yani akü veya baraya mümkün olduğunca yakın yerleştirilir. Kabloyu kalınlaştırıp sigortayı büyütmek, kabloyu korumak yerine riski büyütür.'),
   ('note', 'Bir kablo veya pabuç dokununca sıcaksa, yalıtımı erimiş ya da pabucu kararmışsa ilgili hattı ana şalterden kapatın ve teknik servise haber verin. Bu belirtiler yangın riskinin ilk habercisidir.')],
  faq=[('12 volt sistemde 10 amperlik bir yük için kaç mm² kablo gerekir?', 'Yük 6 metre uzaktaysa ve %3 gerilim düşümü hedefleniyorsa yaklaşık 6 mm² gerekir. Mesafe uzadıkça ya da akım arttıkça kesit büyür; kesin değer için hesap yapılmalıdır.'),
       ('Kablo uçlarını lehimleyip bağlayabilir miyim?', 'Hayır, tek başına lehim önerilmez. Titreşim lehimli noktayı kırar. Uygun pabuç, doğru sıkma pensesi ve gerekirse yapışkanlı büzüşen kılıf kullanılmalıdır.'),
       ('Adana, Mersin veya Bodrum’da kablo ve pano kontrolü yaptırabilir miyim?', 'Evet. Pano, kablo kesiti ve bağlantı kontrolü teknenin bulunduğu yerde yapılır. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Alanya, Antalya ve İstanbul için de randevuya göre planlama yapılır.')]),
 dict(slug='antifouling-gol-ve-akdeniz-icin-dogru-boya',
  title='Antifouling boya: göl mü Akdeniz mi? Doğru boya seçimi',
  cat='Karina', read='5 dk okuma', img='hizmet-karina-bakimi-antifouling.jpg',
  alt='Kızağa alınmış bir teknenin karinasına antifouling boyası sürülmesi', service='karina-bakimi-antifouling',
  excerpt='Göl ve Akdeniz’de canlı yapısı, sıcaklık ve kullanım düzeni farklıdır. Gövde malzemesine ve suya göre antifouling seçimi, hem boyanın ömrünü hem de teknenin korozyon güvenliğini belirler.',
  quick='Antifouling seçimi suya, gövde malzemesine ve kullanım düzenine bağlıdır. Alüminyum gövdede bakır içerikli boya galvanik korozyon riski taşır. Sıcak Akdeniz’de yoğun canlı büyümesi için güçlü bir ablatif boya, gölde ise çoğu zaman daha hafif bir sistem yeterli olur.',
  body=[
   ('p', 'Antifouling, karinaya yapışan yosun, midye ve diğer canlıları geciktiren bir boyadır. Aynı boya her suda ve her teknede aynı sonucu vermez. Bu yazıda, göl ve Akdeniz için seçimde bakılacak başlıca noktaları özetliyoruz.'),
   ('h2', 'Göl ile Akdeniz arasındaki fark'),
   ('ul', ['Tatlı su (göl, baraj): Büyüme daha çok yosun ve biyofilm ağırlıklıdır. Hafif bir sistem çoğu zaman yeterli olur.', 'Akdeniz: Sıcak su, yaz boyunca yoğun büyüme ve kabuklu canlılar (midye, deniz kozalağı) için güçlü bir koruma gerekir.', 'Kullanım sıklığı: Sık seyreden tekne, boyanın yüzeyini kendiliğinden yeniler; uzun süre bağlı kalan tekne ise daha güçlü bir sisteme ihtiyaç duyar.']),
   ('h2', 'Gövde malzemesi ve boya türü'),
   ('p', 'Polyester (fiberglas) ve ahşap gövdelerde bakır içerikli antifouling yaygın kullanılır. Alüminyum gövdede bakır içerikli boya, galvanik korozyonu hızlandırabilir; bu gövdelerde bakırsız bir sistem ve uygun bir bariyer astarı seçilmelidir.'),
   ('p', 'Ablatif (kendini aşındıran) boyalar sezon boyunca yüzeyden yavaşça aşınır ve yeni katmanı açığa çıkarır. Sert (matriks) boyalar ise aşınmaz ve daha hızlı teknelerde tercih edilir.'),
   ('h2', 'Uygulama hataları'),
   ('ul', ['Eski boya ile yeni boyanın uyumunu kontrol etmemek.', 'Yüzeyi yeterince zımparalamadan ve temizlemeden boyamak.', 'Ozmoz veya hasar kontrolü yapmadan üzerini kapatmak.', 'Pervane, şaft ve tutya gibi parçaları yanlış boyamak. Tutyanın üzerine boya sürülmez.']),
   ('note', 'Boya tüketimi ve sezon süresi, kullanım düzenine ve suya göre değişir. Hangi boyanın teknenize uygun olduğunu bilmiyorsanız, uygulamadan önce kısa bir kontrolle karar verilmesi bütçenizi korur.')],
  faq=[('Alüminyum gövdede antifouling nasıl seçilir?', 'Bakır içerikli boya galvanik korozyonu hızlandırabilir. Alüminyum gövdelerde bakırsız bir antifouling ve uygun bariyer astarı kullanılmalıdır.'),
       ('Ablatif ve sert antifouling arasındaki fark nedir?', 'Ablatif boya sezon boyunca yüzeyden aşınır ve yeni katmanı açığa çıkarır. Sert boya aşınmaz ve daha hızlı teknelerde tercih edilir.'),
       ('Seyhan Baraj Gölü, Mersin, Bodrum veya Antalya’da karina bakımı yapıyor musunuz?', 'Evet. Karina bakımı ve antifouling uygulaması teknenin bulunduğu çekek yerinde yapılır. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Alanya, Antalya ve İstanbul için de randevuya göre planlama yapılır.')]),
 dict(slug='deniz-motoru-asiri-isinma-7-neden',
  title='Deniz motoru aşırı ısınıyor: 7 olası neden ve ilk kontroller',
  cat='Deniz motoru', read='5 dk okuma', img='saha-02.jpg',
  alt='Deniz motorunda eşanjör bakımı', service='deniz-motorlari-sevk-sistemleri',
  excerpt='Deniz suyu emişi, impeller, termostat, eşanjör, kayış, egzoz dirseği ve soğutma sıvısı: aşırı ısınmanın en sık nedenleri ve motoru zorlamadan yapılabilecek ilk kontroller.',
  quick='Deniz motorunda aşırı ısınmanın en sık nedenleri tıkalı deniz suyu emişi, aşınmış impeller, takılı termostat, kirli eşanjör, gevşek kayış, tıkanmış egzoz dirseği ve soğutma sıvısındaki hava ya da eksikliktir. Sıcaklık yükselirse motoru hemen durdurun.',
  body=[
   ('p', 'Sıcaklık göstergesi yükseldiğinde ilk tepki motoru durdurmak olmalıdır. Aşırı ısınmış bir motoru çalıştırmaya devam etmek, silindir kapağı ve conta hasarına kadar giden pahalı sonuçlar doğurabilir. Aşağıdaki liste, en sık karşılaşılan yedi nedeni sırasıyla özetler.'),
   ('h2', 'Yedi olası neden'),
   ('ul', ['Deniz suyu emişi: Kapalı seacock, plastik, yosun veya tıkalı filtre suyun motora ulaşmasını engeller.', 'Impeller: Aşınmış, çatlamış veya kanat kaybetmiş impeller yeterli su basamaz.', 'Termostat: Açılmayan bir termostat soğutma suyunun dolaşımını keser.', 'Eşanjör ve yağ soğutucu: Tuz, kireç ve kabuk birikintileri ısı transferini düşürür.', 'Kayış ve tatlı su pompası: Gevşek veya kopmuş kayış pompayı döndüremez.', 'Egzoz dirseği: İçi karbon ve tuzla daralan dirsek, egzoz ve soğutma akışını kısıtlar.', 'Soğutma sıvısı: Kapalı devrede seviye düşükse veya devrede hava varsa sıcaklık hızla yükselir.']),
   ('h2', 'İlk kontroller'),
   ('ul', ['Motoru durdurun ve yaklaşık on beş dakika soğumaya bırakın. Sıcakken genleşme kabının kapağını açmayın.', 'Seacock açık mı ve emiş filtresi temiz mi bakın.', 'Dıştan takma motorlarda kontrol suyu (tell-tale) akıntısı var mı kontrol edin.', 'Kayışın gerginliğine ve soğutma sıvısı seviyesine bakın.']),
   ('p', 'Çamurlu veya kumlu suda impeller daha hızlı aşınabilir. Sıcak mevsimde deniz suyu sıcaklığı da yüksek olduğu için soğutma sisteminin payı azalır; bu yüzden küçük bir tıkanıklık bile yazın daha hızlı belirti verir.'),
   ('note', 'Sorunu bulamıyorsanız veya motor tekrar ısınıyorsa motoru zorlamayın. Erken müdahale, çoğu zaman silindir kapağı ve conta hasarını önler.')],
  faq=[('Motor ısındığında hemen durdurmak gerekir mi?', 'Evet. Sıcaklık göstergesi yükselince motoru zorlamadan durdurun ve soğumaya bırakın. Devam etmek silindir kapağı ve conta hasarına yol açabilir.'),
       ('Impeller yırtıldığında motor hemen ısınır mı?', 'Çoğu zaman evet. Deniz suyu pompası impeller’i yırtılırsa soğutma suyu akışı bir anda azalır ve sıcaklık hızla yükselir.'),
       ('Adana, Mersin, Hatay veya Bodrum’da aşırı ısınma arızası için gelir misiniz?', 'Evet. Arıza teşhisi teknenin bulunduğu yerde yapılır. Adana, Mersin ve Hatay’ın yanı sıra Bodrum, Alanya, Antalya ve İstanbul için de randevuya göre planlama yapılır.')]),
]

import os, datetime
# Yayın takvimi: tarihi gelmemiş yazılar derlemeye girmez. Yeni yazı eklemek = NEW_POSTS'a 'date' ile eklemek.
DATES = {
 'ikinci-el-tekne-alirken-motor-ve-elektrik-kontrol-listesi': '2026-10-05', 'deniz-motoru-periyodik-bakim-rehberi': '2026-10-08',
 'tutya-cinko-nedir-ne-zaman-degistirilir': '2026-10-12', 'tekne-aku-bakimi-ve-test': '2026-10-15', 'nmea-2000-agi-nasil-calisir': '2026-10-19',
 'tekne-kablo-kesiti-ve-pabuc-secimi': '2026-11-02', 'antifouling-gol-ve-akdeniz-icin-dogru-boya': '2026-11-09', 'deniz-motoru-asiri-isinma-7-neden': '2026-11-16',
}
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
def today():
    return datetime.date.fromisoformat(os.environ.get('GM_TODAY') or datetime.date.today().isoformat())
def label(iso):
    d = datetime.date.fromisoformat(iso); return d.strftime('%d.%m.%Y')

def apply(POSTS):
    for p in POSTS:
        e = EXTRA[p['slug']]; p['quick'] = e['quick']; p['faq'] = e['faq']
    POSTS[:0] = []  # sıra: yeni yazılar listede en başa
    for n in reversed(NEW_POSTS):
        POSTS.insert(0, n)
    for p in POSTS:
        p['date'] = DATES[p['slug']]; p['date_label'] = label(p['date'])
    POSTS[:] = sorted([p for p in POSTS if p['date'] <= today().isoformat()], key=lambda p: p['date'], reverse=True)
