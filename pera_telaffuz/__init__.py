"""Türkçe seslendirme metnini kullanıcıya gösterilen metinden ayrı hazırlar."""
from importlib.resources import files
import json
import re

_DATA = json.loads(files(__package__).joinpath('kurallar.json').read_text(encoding='utf-8'))
_ENDINGS = frozenset(_DATA['ekler'])
_TRANSLATION = str.maketrans({'I': 'ı', 'İ': 'i'})
_WORDS = re.compile(r'[^\W\d_]+', re.UNICODE)


def _fold(text):
    return text.translate(_TRANSLATION).casefold()


def _case_like(spelling, original):
    if original.isupper():
        return spelling.translate(str.maketrans({'i': 'İ', 'ı': 'I'})).upper()
    if original[0].isupper():
        first = {'i': 'İ', 'ı': 'I'}.get(spelling[0], spelling[0].upper())
        return first + spelling[1:]
    return spelling


def seslendirme_metni(metin):
    """Yalnızca ses motoruna gönderilecek metni döndür; görünür metni değiştirme."""
    if not isinstance(metin, str):
        raise TypeError('Metin bir str olmalıdır.')
    words, roots = _DATA['kelimeler'], _DATA['kokler']

    def convert(match):
        word = match.group()
        folded = _fold(word)
        if folded in words:
            return _case_like(words[folded], word)
        for root in sorted(roots, key=len, reverse=True):
            suffix = folded[len(root):] if folded.startswith(root) else None
            if suffix is not None and (suffix == '' or suffix in _ENDINGS):
                return _case_like(roots[root], word[:len(root)]) + word[len(root):]
        return word

    return _WORDS.sub(convert, metin)
