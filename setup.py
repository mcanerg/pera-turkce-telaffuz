from pathlib import Path
from setuptools import setup

setup(
    name='pera-turkce-telaffuz',
    version='0.2.0',
    description='Türkçe seslendirme motorları için deneysel telaffuz hazırlığı',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    packages=['pera_telaffuz'],
    package_data={'pera_telaffuz': ['kurallar.json']},
    python_requires='>=3.9',
    license='MIT',
)
