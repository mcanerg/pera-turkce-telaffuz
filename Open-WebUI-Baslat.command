#!/bin/sh
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3.9 veya üstü gerekli: https://www.python.org/downloads/'
  exit 1
fi
exec python3 -m pera_telaffuz.kurulum
