# Open WebUI ile kullanım (deneysel)

Pera Türkçe Telaffuz, mevcut OpenAI uyumlu ses motorunuz ile Open WebUI arasına yerleşir. Sohbette gösterilen yazı değişmez; yalnızca ses motoruna gönderilen metin hazırlanır. Paket ses üretmez ve bir TTS motoru içermez. Bu yöntem Open WebUI'nin normal işlev menüsüne eklenen tek tıklık bir eklenti değildir.

## Gerekli olanlar

- Python 3.9 veya üstü ve bu projenin dosyaları.
- Open WebUI'de yönetici erişimi.
- Çalışan, OpenAI uyumlu `/v1/audio/speech` sunucusu. Örneğin kendi bilgisayarınızda `http://127.0.0.1:5050/v1` adresinde bir TTS motoru (bu yalnızca bir örnektir; Pera onu kurmaz veya başlatmaz).
- Aşağıdaki basit kurulumda Open WebUI, Pera bağlantısı ve TTS motoru aynı bilgisayarda ve aynı ağ ortamında çalışır. Docker veya farklı bir bilgisayardaysa `127.0.0.1` her ortamda farklı yeri gösterir: bağlantı adreslerini kurulumunuza göre ayarlamanız gerekir.

## Kurulum

1. GitHub'da **Code → Download ZIP** ile projeyi indirin ve ZIP'i açın. Python 3.9 veya üstünü kurun.
2. macOS'ta `Open-WebUI-Baslat.command`, Windows'ta `Open-WebUI-Baslat.bat` dosyasını açın. İstendiğinde **mevcut ses motorunuzun gerçek `/v1` adresini** yazın. Pencere açık kaldıkça bağlantı çalışır. API anahtarınızı buraya yazmayın.

   macOS indirme güvenlik uyarısı gösterirse dosyaya sağ tıklayıp **Open / Aç** seçeneğini kullanın. ZIP'ten çıkarılan dosyanın çalıştırma izni yoksa proje klasöründe bir kez `chmod +x Open-WebUI-Baslat.command` çalıştırın.

   Alternatif olarak proje klasöründe `python3 -m pera_telaffuz.kurulum` çalıştırabilirsiniz. Doğrudan komutla başlatmak isteyenler:

   ```sh
   python3 -m pera_telaffuz.proxy --upstream http://127.0.0.1:5050/v1
   ```

   Bu pencere açık kaldıkça bağlantı çalışır. Varsayılan dinleme adresi `127.0.0.1:5051`'dir.
3. Open WebUI'de **Admin Panel → Settings → Audio** bölümüne gidin. Text-to-Speech Engine olarak OpenAI uyumlu motoru seçin. TTS API Base URL alanını `http://127.0.0.1:5051/v1` yapın; model, ses ve varsa API anahtarı için mevcut ses motorunuzun gerektirdiği değerleri kullanın. Kaydedin.
4. Kişisel **Settings → Audio** bölümünde tarayıcıya özel Web API veya Kokoro.js yerine sunucu sesini kullanın. Sesli okumayı “Hafızayı kontrol et, hatalı ifadeyi düzelt” cümlesiyle deneyin.

Open WebUI ve ses motoru arasında bağlantı adresinin erişilebilir olması gerekir. Örneğin Docker içindeki Open WebUI için host adresi ve ağ yapılandırması ayrıca gerekebilir. Bu sürüm henüz bütün Docker ve platform birleşimleriyle doğrulanmadı.

## Dikkat edilmesi gerekenler

- Open WebUI'nin tarayıcı içindeki Web API veya Kokoro.js ses motorları bu bağlantıdan geçmez. Ayrıca Azure/ElevenLabs gibi farklı protokolleri doğrudan desteklemez; yalnızca OpenAI uyumlu `/audio/speech` isteklerini işler.
- Varsayılan olarak yalnızca bu bilgisayardan bağlantı kabul edilir ve gelen yetkilendirme bilgisi **yalnızca sizin `--upstream` ile seçtiğiniz sunucuya** iletilir. Uzak veya bulut sunucu seçerseniz konuşma metni ve varsa API anahtarı o sunucuya gider. Güvendiğiniz bir adres kullanın.
- `--host 0.0.0.0` gibi bir ayar bağlantıyı ağdaki diğer cihazlara açabilir. Bu örnek sunucuda ayrıca kimlik doğrulama yoktur; güvenilmeyen bir ağa veya internete açmayın.
- İlk sürüm bütün Türkçe kelimeleri kapsamaz. Ses kalitesi kullanılan TTS motoruna bağlıdır. İstekleri ve metni kaydetmez; kullandığınız Open WebUI ve TTS motorunun kendi kayıt davranışı farklı olabilir.
- Open WebUI önceden ürettiği sesi önbellekten tekrar kullanabilir. Değişikliği denemek için yeni bir cümle kullanın.
- Open WebUI'nin bazı kurulumları MP3 dışındaki sesleri dönüştürmek için sistemde `ffmpeg` ve `ffprobe` gerektirir. Ses üretiliyor ama Open WebUI hata veriyorsa ikisinin Open WebUI'yi çalıştıran ortamın PATH'inde olduğundan emin olun.

## Deneme sonucu

Open WebUI 0.13.0, macOS üzerinde Python kurulumu ile ve gerçek bir yerel ses motoru kullanılarak denendi. Open WebUI'nin ses isteği üzerinden ses dosyası başarıyla alındı ve motorun düzeltilmiş metni aldığı doğrulandı. Bu denemede WAV dönüşümü için `ffmpeg` ve `ffprobe` gerekti. Docker ve diğer sürümler ayrıca test edilmedi.

İlgili Open WebUI belgeleri: [Ses ayarları](https://docs.openwebui.com/troubleshooting/audio/) ve [OpenAI uyumlu TTS örneği](https://docs.openwebui.com/features/chat-conversations/audio/text-to-speech/openai-edge-tts-integration/).
