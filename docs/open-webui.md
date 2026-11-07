# Open WebUI ile kullanım (deneysel)

Pera Türkçe Telaffuz, mevcut OpenAI uyumlu ses motorunuz ile Open WebUI arasına yerleşir. Sohbette görünen yazı değişmez; yalnızca ses motoruna gönderilen metin hazırlanır. Paket ses üretmez ve bir TTS motoru içermez. Bu yöntem Open WebUI'nin normal işlev menüsüne eklenen tek tıklık bir eklenti değildir.

## Gerekli olanlar

- Python 3.9 veya üstü ve bu projenin dosyaları.
- Open WebUI'de yönetici erişimi.
- Çalışan, OpenAI uyumlu /v1/audio/speech sunucusu. Örneğin kendi bilgisayarınızda http://127.0.0.1:5050/v1 adresinde bir TTS motoru (bu yalnızca bir örnektir; Pera onu kurmaz veya başlatmaz).
- Aşağıdaki basit kurulumda Open WebUI, Pera bağlantısı ve TTS motoru aynı bilgisayarda ve aynı ağ ortamında çalışır. Docker veya farklı bir bilgisayardaysa 127.0.0.1 her ortamda farklı yeri gösterir: bağlantı adreslerini kurulumunuza göre ayarlamanız gerekir.

## Kurulum

1. Bu GitHub deposunu indirin ve proje klasöründe terminal açın.
2. Aşağıdaki komutta --upstream değerini **mevcut TTS motorunuzun gerçek adresiyle** değiştirip çalıştırın:

    python3 -m pera_telaffuz.proxy --upstream http://127.0.0.1:5050/v1

   Bu pencere açık kaldıkça bağlantı çalışır. Varsayılan dinleme adresi 127.0.0.1:5051'dir.
3. Open WebUI'de **Admin Panel → Settings → Audio** bölümüne gidin. Text-to-Speech Engine olarak OpenAI uyumlu motoru seçin. TTS API Base URL alanını http://127.0.0.1:5051/v1 yapın; model, ses ve varsa API anahtarı için mevcut ses motorunuzun gerektirdiği değerleri kullanın. Kaydedin.
4. Kişisel **Settings → Audio** bölümünde tarayıcıya özel Web API veya Kokoro.js yerine sunucu sesini kullanın. Sesli okumayı “Hafızayı kontrol et, hatalı ifadeyi düzelt” cümlesiyle deneyin.

Open WebUI ve ses motoru arasında bağlantı adresinin erişilebilir olması gerekir. Docker içindeki Open WebUI için host adresi ve ağ yapılandırması ayrıca gerekebilir. Bu sürüm henüz bütün Docker ve platform birleşimleriyle doğrulanmadı.

## Dikkat edilmesi gerekenler

- Open WebUI'nin tarayıcı içindeki Web API veya Kokoro.js ses motorları bu bağlantıdan geçmez. Azure/ElevenLabs gibi farklı protokolleri doğrudan desteklemez; yalnızca OpenAI uyumlu /audio/speech isteklerini işler.
- Varsayılan olarak yalnızca bu bilgisayardan bağlantı kabul edilir ve gelen yetkilendirme bilgisi yalnızca sizin --upstream ile seçtiğiniz sunucuya iletilir. Uzak veya bulut sunucu seçerseniz konuşma metni ve varsa API anahtarı o sunucuya gider. Güvendiğiniz bir adres kullanın.
- --host 0.0.0.0 gibi bir ayar bağlantıyı ağdaki diğer cihazlara açabilir. Bu örnek sunucuda ayrıca kimlik doğrulama yoktur; güvenilmeyen bir ağa veya internete açmayın.
- İlk sürüm bütün Türkçe kelimeleri kapsamaz. Ses kalitesi kullanılan TTS motoruna bağlıdır. Ara katman istekleri ve metni kaydetmez; kullandığınız Open WebUI ve TTS motorunun kendi kayıt davranışı farklı olabilir.

İlgili Open WebUI belgeleri: [Ses ayarları](https://docs.openwebui.com/troubleshooting/audio/) ve [OpenAI uyumlu TTS örneği](https://docs.openwebui.com/features/chat-conversations/audio/text-to-speech/openai-edge-tts-integration/).
