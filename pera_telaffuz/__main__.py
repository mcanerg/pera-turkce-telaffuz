import sys
from . import seslendirme_metni

if len(sys.argv) > 1:
    source = ' '.join(sys.argv[1:])
else:
    source = sys.stdin.read()
sys.stdout.write(seslendirme_metni(source))
