import unittest
from pera_telaffuz import seslendirme_metni

class TelaffuzTest(unittest.TestCase):
    def test_kok_ve_ekleri(self):
        self.assertEqual(seslendirme_metni('Hafıza, hafızayı ve hatalı ifadeyi kontrol et.'),
                         'Haafıza, haafızayı ve hataalı ifaadeyi kontrol et.')

    def test_ozel_sozcuk_onceligi(self):
        self.assertEqual(seslendirme_metni('Hata ve hatayı düzelt, tekrar dene.'),
                         'Hatâ ve hataayı düzelt, tekrâr dene.')

    def test_benzer_kelimeler_ve_noktalama_korunur(self):
        self.assertEqual(seslendirme_metni('Hatay, hafızaspor; 3.5 ve URL.'),
                         'Hatay, hafızaspor; 3.5 ve URL.')

    def test_turkce_buyuk_harfler(self):
        self.assertEqual(seslendirme_metni('İfade İFADE HAFIZA'),
                         'İfaade İFAADE HAAFIZA')

    def test_girdi_degisikligi_yok(self):
        source = 'Hatalı metin.'
        seslendirme_metni(source)
        self.assertEqual(source, 'Hatalı metin.')

if __name__ == '__main__':
    unittest.main()
