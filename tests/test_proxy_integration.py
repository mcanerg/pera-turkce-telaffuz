import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from pera_telaffuz.proxy import make_handler

class FakeTTS(BaseHTTPRequestHandler):
    received = None
    def log_message(self, *_):
        pass
    def do_POST(self):
        type(self).received = (self.path, json.loads(self.rfile.read(int(self.headers['Content-Length']))), self.headers.get('Authorization'))
        audio = b'fake-audio-data'
        self.send_response(200)
        self.send_header('Content-Type', 'audio/wav')
        self.send_header('Content-Length', str(len(audio)))
        self.end_headers()
        self.wfile.write(audio)

class EndToEndTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.tts = ThreadingHTTPServer(('127.0.0.1', 0), FakeTTS)
            cls.proxy = ThreadingHTTPServer(('127.0.0.1', 0), make_handler('http://127.0.0.1:%d/v1' % cls.tts.server_port))
        except PermissionError:
            if hasattr(cls, 'tts'): cls.tts.server_close()
            raise unittest.SkipTest('Yerel bağlantı izni yok')
        cls.threads = [threading.Thread(target=s.serve_forever, daemon=True) for s in (cls.tts, cls.proxy)]
        for t in cls.threads: t.start()

    @classmethod
    def tearDownClass(cls):
        for server in (cls.tts, cls.proxy): server.shutdown(); server.server_close()
        for thread in cls.threads: thread.join()

    def test_audio_is_forwarded_and_input_is_converted(self):
        body = json.dumps({'model':'local', 'voice':'tr', 'input':'Hafızayı kontrol et.'}).encode()
        request = Request('http://127.0.0.1:%d/v1/audio/speech' % self.proxy.server_port, data=body,
                          headers={'Content-Type':'application/json','Authorization':'Bearer test-only'})
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.read(), b'fake-audio-data')
            self.assertEqual(response.headers['Content-Type'], 'audio/wav')
        self.assertEqual(FakeTTS.received, ('/v1/audio/speech', {'model':'local','voice':'tr','input':'Haafızayı kontrol et.'}, 'Bearer test-only'))

    def test_other_routes_are_rejected(self):
        request = Request('http://127.0.0.1:%d/v1/other' % self.proxy.server_port, data=b'{}', headers={'Content-Type':'application/json'})
        with self.assertRaises(HTTPError) as error: urlopen(request, timeout=5)
        self.assertEqual(error.exception.code, 404)

if __name__ == '__main__':
    unittest.main()
