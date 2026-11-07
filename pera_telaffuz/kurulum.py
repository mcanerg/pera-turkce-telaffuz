"""Yerel Open WebUI bağlantısı için küçük etkileşimli başlatıcı."""
from .proxy import serve, validated_base


def main():
    print('Pera Türkçe Telaffuz — Open WebUI bağlantısı')
    print('Çalışan bir OpenAI uyumlu ses motoru gereklidir. API anahtarınızı buraya yazmayın.')
    print('Örnek adres: http://127.0.0.1:5050/v1')
    while True:
        try:
            address = input('Ses motorunuzun /v1 adresi (çıkmak için boş bırakın): ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nİptal edildi.')
            return
        if not address:
            print('İptal edildi.')
            return
        try:
            address = validated_base(address)
        except ValueError as error:
            print(error)
            continue
        break
    print('\nOpen WebUI → Admin Panel → Settings → Audio:')
    print('TTS API Base URL: http://127.0.0.1:5051/v1')
    print('Model, ses ve varsa API anahtarını Open WebUI içinde ayarlayın.')
    print('Bu pencereyi açık tutun; durdurmak için Ctrl+C kullanın.\n')
    try:
        serve(address)
    except OSError as error:
        print(f'Bağlantı başlatılamadı: {error}')
        print('5051 numaralı bağlantı noktası başka bir uygulama tarafından kullanılıyor olabilir.')


if __name__ == '__main__':
    main()
