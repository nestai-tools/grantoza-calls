"""Application and public catalogue compatibility contract."""
import json
from pathlib import Path
import re

VERSION = json.loads((Path(__file__).resolve().parents[3] / 'version.json').read_text())['version']


def semver(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', value):
        raise ValueError('Wersja musi mieć postać MAJOR.MINOR.PATCH.')
    return tuple(map(int, value.split('.')))


def compatibility(entry, version=VERSION):
    rules = entry['compatibility']
    if rules['call_format_version'] != 1 or rules['fields_schema_version'] != 2:
        return 'Ta wersja formatu naboru wymaga innej wersji aplikacji.'
    if semver(version) < semver(rules['min_app_version']):
        return 'Zaktualizuj aplikację do wersji ' + rules['min_app_version'] + ' lub nowszej.'
    if rules.get('max_app_version_exclusive') and semver(version) >= semver(rules['max_app_version_exclusive']):
        return 'Ten nabór wymaga starszej wersji aplikacji.'
    return None
