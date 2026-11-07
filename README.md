# Pera Türkçe Telaffuz

Türkçe seslendirme için küçük, deneysel bir metin hazırlama paketi. Pera'da kullanılan bazı uzun ünlü düzeltmelerini ve yaygın ekleri içerir. Herhangi bir LLM'e yeni bir ses veya model eklemez; mevcut bir metinden sese (TTS) motoruna giden metni hazırlar.

**Önemli:** Bu, bütün Türkçe kelimeleri kapsayan bir telaffuz sözlüğü veya otomatik dil çözümleyicisi değildir. Uzunluk her zaman yazıdan anlaşılamaz ve sonuçlar kullanılan ses motoruna göre değişir. Kurallar Pera'nın Türkçe sesiyle denenmiştir; kendi sesinizle örnekleri dinleyerek değerlendirin.

## Deneme

Python 3.9 veya üzeri gerekir; çalışma sırasında ek bir paket veya internet bağlantısı gerekmez. Klasörde terminal açın:

```sh
python3 -m pera_telaffuz "Hafızayı kontrol et, hatalı ifadeyi düzelt."
```

Örnek çıktı (yalnızca ses motoruna verilen metin):

```text
Haafızayı kontrol et, hataalı ifaadeyi düzelt.
```

Bir dosyadan da okuyabilirsiniz:

```sh
python3 -m pera_telaffuz < metin.txt
```

## Open WebUI

OpenAI uyumlu bir ses motoru kullanıyorsanız [Open WebUI kurulum rehberine](docs/open-webui.md) bakın. Deneysel bağlantı, sohbet yazısını değiştirmeden ses motoruna gönderilen metni hazırlar.

## Kendi yerel asistanına ekle

Klasörü asistan projenize alın veya yerel olarak yükleyin (`python3 -m pip install .`). Asistanın seslendirme yaptığı yerde, görünen yanıtın bir kopyasını ses motoruna göndermeden önce dönüştürün:

```python
from pera_telaffuz import seslendirme_metni

cevap = "Hafızayı kontrol et, hatalı ifadeyi düzelt."
# Ekranda cevabı normal yazılışıyla gösterin.
ses_motoruna_gidecek_metin = seslendirme_metni(cevap)
# Kendi TTS motorunuzu bu metinle çağırın.
```

Farklı uygulamalar farklı entegrasyon yöntemleri kullanır. Bu paket bağımsız bir Python kütüphanesidir; başka bir uygulamada otomatik olarak görünmez ve kendi başına ses üretmez. Sadece sohbet modeline değil, TTS bileşenine erişim gerekir.

## Kelime ekleme

`pera_telaffuz/kurallar.json` içindeki `kelimeler` tam kelimelerin ses motoruna verilecek yazılışını, `kokler` ise yaygın eklerle birlikte işlenecek kökleri içerir. `ekler` izin verilen eklerin sınırlı listesidir. Tam kelime kuralları köklere göre önceliklidir. Bunlar resmî yazım değildir; motorun okumasını etkilemek için seçilmiş deneysel yazılışlardır.

Değişiklik yaparken farklı cümlelerde ve ekli biçimlerde sesi dinleyin. Eş sesli kelimeler bağlama göre farklı okunabilir; genel bir kural farklı anlamlarda yanlış sonuca yol açabilir. Kullanıcı metni, URL'ler veya kodlar ses motoruna gönderilecekse, uygulamanız önce bunlara uygun bir temizleme işlemi uygulamalıdır.

## Test

```sh
python3 -m unittest discover -s tests -v
```

Bu testler metin dönüşümünü doğrular; ses kalitesini veya telaffuzun doğal olduğunu ölçmez.

## Lisans

MIT; ayrıntılar için `LICENSE` dosyasına bakın.
