"""OpenAI uyumlu TTS sunucusu için yerel telaffuz ara katmanı."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from . import seslendirme_metni

MAX_BODY = 65536


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validated_base(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise ValueError('TTS adresi geçerli bir http veya https temel adresi olmalı.')
    return url.rstrip('/')


def convert_request(data):
    body = json.loads(data)
    if not isinstance(body, dict) or not isinstance(body.get('input'), str):
        raise ValueError('input metin olmalı')
    body['input'] = seslendirme_metni(body['input'])
    return json.dumps(body, ensure_ascii=False).encode('utf-8')


def make_handler(upstream):
    target = validated_base(upstream) + '/audio/speech'
    opener = build_opener(NoRedirect)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *_):
            # Do not log speech text, authorization headers, or query strings.
            pass

        def send_bytes(self, status, payload, content_type):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(payload)

        def fail(self, status, message):
            self.send_bytes(status, json.dumps({'error': message}, ensure_ascii=False).encode(), 'application/json; charset=utf-8')

        def do_POST(self):
            if self.path != '/v1/audio/speech':
                self.close_connection = True
                self.fail(404, 'Yalnızca /v1/audio/speech desteklenir.'); return
            if self.headers.get('Transfer-Encoding'):
                self.close_connection = True
                self.fail(400, 'Desteklenmeyen istek.'); return
            if self.headers.get('Content-Type', '').split(';')[0].strip().lower() != 'application/json':
                self.close_connection = True
                self.fail(415, 'JSON gerekli.'); return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= MAX_BODY:
                    self.close_connection = True
                    self.fail(413, 'İstek boş veya çok büyük.'); return
                raw = self.rfile.read(size)
                if len(raw) != size:
                    self.fail(400, 'İstek eksik.'); return
                data = convert_request(raw)
            except (ValueError, UnicodeDecodeError):
                self.fail(400, 'Geçersiz seslendirme isteği.'); return
            headers = {'Content-Type': 'application/json'}
            authorization = self.headers.get('Authorization')
            if authorization:
                headers['Authorization'] = authorization
            req = Request(target, data=data, headers=headers, method='POST')
            try:
                with opener.open(req, timeout=120) as response:
                    payload = response.read()
                    self.send_bytes(response.status, payload, response.headers.get('Content-Type', 'application/octet-stream'))
            except HTTPError as exc:
                # Do not echo potentially sensitive upstream responses into logs.
                self.fail(exc.code, 'Ses motoru isteği reddetti.')
            except (URLError, TimeoutError, OSError):
                self.fail(502, 'Ses motoruna bağlanılamadı.')

    return Handler


def serve(upstream, host='127.0.0.1', port=5051):
    handler = make_handler(upstream)
    server = ThreadingHTTPServer((host, port), handler)
    print(f'Pera TTS ara katmanı {host}:{port} üzerinde hazır.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description='Pera Türkçe telaffuz TTS ara katmanı')
    parser.add_argument('--upstream', required=True, help='Mevcut OpenAI uyumlu ses motorunun /v1 adresi')
    parser.add_argument('--host', default='127.0.0.1', help='Dinleme adresi (varsayılan: yalnızca bu bilgisayar)')
    parser.add_argument('--port', default=5051, type=int)
    args = parser.parse_args()
    serve(args.upstream, args.host, args.port)


if __name__ == '__main__':
    main()
