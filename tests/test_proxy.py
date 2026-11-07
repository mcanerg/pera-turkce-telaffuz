import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from pera_telaffuz.proxy import convert_request, validated_base, NoRedirect

class ProxyTest(unittest.TestCase):
    def test_only_input_changes(self):
        original = {'input': 'Hafızayı kontrol et.', 'voice': 'tr', 'model': 'local', 'speed': 1.2}
        result = json.loads(convert_request(json.dumps(original).encode()))
        self.assertEqual(result, {**original, 'input': 'Haafızayı kontrol et.'})

    def test_invalid_input(self):
        for data in (b'{}', b'[]', b'{"input": 5}', b'invalid'):
            with self.assertRaises((ValueError, TypeError)):
                convert_request(data)

    def test_upstream_url_validation(self):
        self.assertEqual(validated_base('http://127.0.0.1:5050/v1/'), 'http://127.0.0.1:5050/v1')
        for url in ('file:///tmp/x', 'https://user:pass@example.com/v1', 'https://example.com/v1?key=secret'):
            with self.assertRaises(ValueError):
                validated_base(url)

    def test_auth_is_not_redirected(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'http://example.com'))

if __name__ == '__main__':
    unittest.main()
