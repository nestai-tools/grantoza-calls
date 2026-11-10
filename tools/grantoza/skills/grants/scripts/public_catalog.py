#!/usr/bin/env python3
"""Build reviewed public releases and import only the selected call's verified files."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from zoneinfo import ZoneInfo
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from app_version import VERSION, compatibility, semver
from workspace import (folder, identifier, locked, read_json, register_call,
                       template_files, validate_template, write_json)

REPOSITORY = 'nestai-tools/grantoza-calls'
MAX_FILE = 40 * 1024 * 1024
MAX_TOTAL = 180 * 1024 * 1024
MAX_FILES = 3000
PUBLIC_ROOTS = {'01-sources', '02-analysis', '03-application', '04-project', '05-diagrams', '06-attachments'}
PUBLIC_FILES = {'call.json', 'documents.json', 'README.md', '00-overview.md'}
PRIVATE_NAMES = {'application.json', 'company.json', 'company-fit.md', 'inbox', 'materials', 'archive', '90-export'}


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or any(ord(c) < 32 for c in value):
        raise ValueError('Nieprawidłowa ścieżka pakietu.')
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(
            part in {'..', '.'} or part.startswith('.') or part in PRIVATE_NAMES for part in path.parts):
        raise ValueError('Niedozwolona ścieżka pakietu: ' + value)
    if not (value in PUBLIC_FILES or path.parts[0] in PUBLIC_ROOTS):
        raise ValueError('Plik nie należy do publicznego wzoru: ' + value)
    return value


def sha(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise ValueError('Niepoprawna suma SHA-256.')
    return value


def validate_index(data):
    # The JSON schema also documents this contract for contributors and CI.
    import jsonschema
    schema = read_json(Path(__file__).resolve().parents[1] / 'references/public-catalog.schema.json')
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as exc:
        raise ValueError('Niepoprawny indeks katalogu: ' + exc.message) from exc
    seen = set()
    for entry in data['calls']:
        id = identifier(entry['id'])
        if id in seen or entry['path'] != f'calls/{id}':
            raise ValueError('Powtórzone ID lub niepoprawny folder w indeksie.')
        seen.add(id)
        semver(entry['call_version'])
        for key in ('created_with_app_version', 'analyzed_with_app_version', 'packaged_with_app_version'):
            if entry[key] is not None:
                semver(entry[key])
        rules = entry['compatibility']
        semver(rules['min_app_version'])
        if rules.get('max_app_version_exclusive'):
            if semver(rules['max_app_version_exclusive']) <= semver(rules['min_app_version']):
                raise ValueError('Pusty zakres zgodności aplikacji.')
        sha(entry['manifest_sha256'])
        schedule = entry['schedule']
        for key in ('announced_on', 'opens_on', 'closes_on', 'planned_announcement', 'planned_opening'):
            value = schedule[key]
            if value is not None:
                if not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?)?', value):
                    raise ValueError('Termin wymaga daty ISO: ' + key)
                if len(value) == 7:
                    date.fromisoformat(value + '-01')
                elif len(value) == 10:
                    date.fromisoformat(value)
                else:
                    datetime.fromisoformat(value.replace('Z', '+00:00'))
        if schedule['timezone']:
            ZoneInfo(schedule['timezone'])
        if schedule['opens_on'] and schedule['closes_on'] and schedule['opens_on'][:10] > schedule['closes_on'][:10]:
            raise ValueError('Koniec naboru poprzedza początek.')
    return data


def manifest_files(manifest, entry):
    if manifest.get('schema_version') != 1 or manifest.get('id') != entry['id'] or manifest.get('call_version') != entry['call_version']:
        raise ValueError('Manifest nie odpowiada wybranemu wydaniu naboru.')
    files = manifest.get('files')
    if not isinstance(files, list) or not 0 < len(files) <= MAX_FILES:
        raise ValueError('Niepoprawna liczba plików pakietu.')
    seen, total = set(), 0
    for item in files:
        path = safe_path(item['path'])
        if path in seen or type(item['size']) is not int or not 0 <= item['size'] <= MAX_FILE:
            raise ValueError('Powtórzony plik lub przekroczony rozmiar.')
        sha(item['sha256'])
        seen.add(path)
        total += item['size']
    if total > MAX_TOTAL or not {'call.json', 'documents.json', '03-application/fields.json'} <= seen:
        raise ValueError('Pakiet jest za duży lub nie zawiera wymaganych plików.')
    return files


def validate_sources(call):
    for document in read_json(call / 'documents.json')['dokumenty']:
        path = call / safe_path(document['plik'])
        if digest(path.read_bytes()) != document['sha256']:
            raise ValueError('Suma źródła nie zgadza się z rejestrem: ' + document['id'])


def privacy_check(call):
    """Reject obvious private artefacts; human source inspection is still required."""
    for path in template_files(call):
        name = path.relative_to(call).as_posix()
        if name == 'release.json':
            continue
        safe_path(name)
        if path.suffix.lower() in {'.md', '.json', '.txt', '.csv', '.xml', '.html'}:
            text = path.read_text(encoding='utf-8')
            if re.search(r'/(?:home|Users)/[^/\s"<>]+/', text) or re.search(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----', text):
                raise ValueError('Plik zawiera lokalną ścieżkę lub klucz prywatny: ' + name)


def build_release(call, repository, metadata, call_version, *, reviewed=False):
    """Only a deliberately reviewed, blank shared template may enter a public repository."""
    call, repository = Path(call).resolve(), Path(repository).resolve()
    if not reviewed:
        raise ValueError('Najpierw przejrzyj źródła i metadane pod kątem prywatnych danych; następnie użyj --reviewed.')
    semver(call_version)
    validate_template(call)
    validate_sources(call)
    id = identifier(call.name)
    target = folder(repository, 'calls', id)
    if target.exists() and (target / 'release.json').exists():
        if semver(call_version) <= semver(read_json(target / 'release.json')['call_version']):
            raise ValueError('Nowa publikacja wymaga wyższej wersji naboru.')
    elif target.exists():
        raise ValueError('Folder docelowy nie jest rozpoznanym wydaniem naboru.')
    index_path = repository / 'index.json'
    index = validate_index(read_json(index_path)) if index_path.exists() else dict(schema_version=1, repository=REPOSITORY, updated_at=now(), calls=[])
    entry = dict(metadata, id=id, path=f'calls/{id}', call_version=call_version,
                 created_with_app_version=read_json(call / 'call.json').get('created_with_app_version', metadata.get('created_with_app_version')),
                 analyzed_with_app_version=read_json(call / 'call.json').get('analyzed_with_app_version'),
                 packaged_with_app_version=VERSION, published_at=now(),
                 compatibility=metadata.get('compatibility', dict(call_format_version=1, fields_schema_version=2,
                     min_app_version='0.2.0', max_app_version_exclusive=None)), manifest_sha256='0' * 64)
    # Validate before mutating the repository.
    candidate = dict(index, calls=[row for row in index['calls'] if row['id'] != id] + [entry])
    validate_index(candidate)
    (repository / 'calls').mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.release-', dir=repository) as temporary:
        staged = Path(temporary) / id
        staged.mkdir()
        for source in template_files(call):
            name = source.relative_to(call).as_posix()
            if name == 'release.json':
                continue
            safe_path(name)
            destination = staged / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if name == 'call.json':
                meta = read_json(source)
                # Local execution state and user prompts are not public grant facts.
                public = {key: meta[key] for key in ('schema_version', 'id', 'tytul', 'url', 'etap', 'informacje', 'rozbieznosci', 'created_with_app_version', 'analyzed_with_app_version') if key in meta}
                public['analiza'] = {key: value for key, value in meta.get('analiza', {}).items()
                                     if key.startswith('liczba_') or key in {'fingerprint_zrodel', 'blokery', 'nieodczytane_zrodla', 'zakonczono_at',
                                         'zakres', 'ograniczenia', 'uwagi', 'otwarte_kwestie', 'czesciowo_przeczytane_zrodla',
                                         'zrodla_przejrzane_czesciowo', 'zrodla_czesciowo_odczytane'}}
                write_json(destination, public)
            elif name == 'documents.json':
                data = read_json(source)
                for document in data['dokumenty']:
                    document.pop('plik_wejsciowy', None)
                write_json(destination, data)
            else:
                shutil.copyfile(source, destination)
        privacy_check(staged)
        validate_template(staged)
        validate_sources(staged)
        files = [dict(path=path.relative_to(staged).as_posix(), size=path.stat().st_size,
                      sha256=digest(path.read_bytes())) for path in template_files(staged)]
        manifest = dict(schema_version=1, id=id, call_version=call_version, files=files)
        manifest_files(manifest, entry)
        write_json(staged / 'release.json', manifest)
        entry['manifest_sha256'] = digest((staged / 'release.json').read_bytes())
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged), target)
    candidate['calls'] = sorted(candidate['calls'], key=lambda row: row['id'])
    candidate['updated_at'] = now()
    write_json(index_path, candidate)
    return entry


def fetch(url, limit):
    # URLs are constructed solely from the fixed public repository and a commit SHA.
    request = Request(url, headers={'User-Agent': 'Grantoza/' + VERSION, 'Accept': 'application/vnd.github+json'})
    try:
        with urlopen(request, timeout=40) as response:
            if int(response.headers.get('Content-Length', 0)) > limit:
                raise ValueError('Plik w katalogu przekracza limit rozmiaru.')
            data = response.read(limit + 1)
            if len(data) > limit:
                raise ValueError('Plik w katalogu przekracza limit rozmiaru.')
            return data
    except (URLError, TimeoutError) as exc:
        raise ValueError('Nie można pobrać publicznego katalogu z GitHub. Sprawdź połączenie i spróbuj ponownie.') from exc


class CatalogClient:
    def __init__(self, root, fetcher=fetch):
        self.root = Path(root).resolve()
        self.fetch = fetcher

    def raw(self, commit, path, limit):
        if not re.fullmatch('[0-9a-f]{40}', commit):
            raise ValueError('Niepoprawna wersja repozytorium.')
        return self.fetch(f'https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{quote(path, safe="/")}', limit)

    def load(self):
        commit = json.loads(self.fetch(f'https://api.github.com/repos/{REPOSITORY}/commits/main', 1024 * 1024))['sha']
        data = validate_index(json.loads(self.raw(commit, 'index.json', 4 * 1024 * 1024)))
        result = dict(data, commit=commit, fetched_at=now())
        write_json(self.root / '.panel/catalog/snapshot.json', result)
        return result

    def snapshot(self, commit):
        data = read_json(self.root / '.panel/catalog/snapshot.json')
        if data.get('commit') != commit:
            raise ValueError('Katalog został odświeżony. Wybierz nabór ponownie.')
        return validate_index(data)

    def install(self, entry, commit, progress=lambda done, total: None):
        reason = compatibility(entry)
        if reason:
            raise ValueError(reason)
        target = folder(self.root, 'calls', entry['id'])
        if target.exists():
            raise ValueError('Nabór jest już lokalnie. Istniejący wzór został zachowany.')
        raw = self.raw(commit, entry['path'] + '/release.json', 2 * 1024 * 1024)
        if digest(raw) != entry['manifest_sha256']:
            raise ValueError('Niepoprawna suma manifestu wydania.')
        files = manifest_files(json.loads(raw), entry)
        staging_root = self.root / '.panel/catalog/downloads'
        staging_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='import-', dir=staging_root) as temporary:
            staged = Path(temporary) / target.name
            staged.mkdir()
            def download(item):
                content = self.raw(commit, entry['path'] + '/' + item['path'], item['size'])
                if len(content) != item['size'] or digest(content) != item['sha256']:
                    raise ValueError('Plik ma inną sumę kontrolną: ' + item['path'])
                path = staged / item['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            progress(0, len(files))
            with ThreadPoolExecutor(max_workers=6) as pool:
                futures = [pool.submit(download, item) for item in files]
                for done, future in enumerate(as_completed(futures), 1):
                    future.result()
                    progress(done, len(files))
            (staged / 'release.json').write_bytes(raw)
            validate_template(staged)
            validate_sources(staged)
            privacy_check(staged)
            meta = read_json(staged / 'call.json')
            meta['catalog_source'] = dict(repository=REPOSITORY, commit=commit, call_version=entry['call_version'],
                                          manifest_sha256=entry['manifest_sha256'], imported_at=now())
            write_json(staged / 'call.json', meta)
            with locked(self.root / '.panel/catalog/install.lock'):
                if target.exists():
                    raise ValueError('Nabór został już dodany w innym procesie.')
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged, target)
                try:
                    register_call(target, visible=True)
                except BaseException:
                    shutil.rmtree(target)
                    raise
        return target


def validate_repository(repository):
    repository = Path(repository).resolve()
    index = validate_index(read_json(repository / 'index.json'))
    for entry in index['calls']:
        call = folder(repository, 'calls', entry['id'])
        raw = (call / 'release.json').read_bytes()
        if digest(raw) != entry['manifest_sha256']:
            raise ValueError('Suma manifestu wydania jest niepoprawna: ' + entry['id'])
        files = manifest_files(json.loads(raw), entry)
        actual = {p.relative_to(call).as_posix() for p in template_files(call)} - {'release.json'}
        if actual != {item['path'] for item in files}:
            raise ValueError('Lista plików wydania nie odpowiada folderowi.')
        for item in files:
            data = (call / item['path']).read_bytes()
            if digest(data) != item['sha256'] or len(data) != item['size']:
                raise ValueError('Zmieniony plik wydania: ' + item['path'])
        validate_sources(call)
        privacy_check(call)
        validate_template(call)
    return index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    build.add_argument('--call', type=Path, required=True)
    build.add_argument('--repository', type=Path, required=True)
    build.add_argument('--metadata', type=Path, required=True)
    build.add_argument('--call-version', required=True)
    build.add_argument('--reviewed', action='store_true')
    validate = sub.add_parser('validate')
    validate.add_argument('--repository', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'build':
        result = build_release(args.call, args.repository, read_json(args.metadata), args.call_version, reviewed=args.reviewed)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('Poprawne wydania:', len(validate_repository(args.repository)['calls']))


if __name__ == '__main__':
    main()
