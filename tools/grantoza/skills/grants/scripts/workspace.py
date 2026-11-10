#!/usr/bin/env python3
"""Catalogue of shared calls and creation of independent application repositories."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import uuid

from git_workspace import initialize_repository
from grouped_forms import Form


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        raise ValueError('Identyfikator musi zawierać małe litery ASCII, cyfry i łączniki.')
    return value


def folder(root, collection, id):
    root = Path(root).resolve()
    path = root / collection / identifier(id)
    if path.resolve() != path or (root / collection).is_symlink():
        raise ValueError('Folder danych nie może być dowiązaniem symbolicznym.')
    return path


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, prefix='.json-', delete=False, encoding='utf-8') as stream:
        temporary = Path(stream.name)
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(temporary, path)


@contextmanager
def locked(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def registry(calls):
    path = Path(calls) / 'calls.json'
    data = read_json(path) if path.exists() else {'schema_version': 1, 'calls': []}
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('calls'), list):
        raise ValueError('Niepoprawny rejestr calls/calls.json.')
    seen = set()
    for entry in data['calls']:
        id = identifier(entry['id'])
        if id in seen or type(entry.get('widoczny')) is not bool:
            raise ValueError('Rejestr wymaga unikalnych ID i widoczny: true/false.')
        seen.add(id)
    return data


def register_call(call, visible=None):
    """New calls are hidden until analysis; retries preserve the operator's choice."""
    call = Path(call).resolve()
    identifier(call.name)
    with locked(call.parent / '.registry.lock'):
        data = registry(call.parent)
        entry = next((r for r in data['calls'] if r['id'] == call.name), None)
        if entry is None:
            entry = {'id': call.name, 'widoczny': False}
            data['calls'].append(entry)
        if visible is not None:
            entry['widoczny'] = bool(visible)
        write_json(call.parent / 'calls.json', data)


def template_files(call):
    for base, dirs, files in os.walk(call, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d not in {'90-export', 'archive', '__pycache__'})
        for name in dirs + files:
            if (Path(base) / name).is_symlink():
                raise ValueError('Szablon naboru nie może zawierać dowiązań.')
        for name in sorted(files):
            if not name.startswith('.') and not name.endswith(('.pyc', '.tmp')):
                yield Path(base) / name


def template_version(call):
    digest = hashlib.sha256()
    for path in template_files(call):
        digest.update(path.relative_to(call).as_posix().encode() + b'\0')
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def validate_template(call):
    meta = read_json(call / 'call.json')
    if not isinstance(meta, dict):
        raise ValueError('call.json musi zawierać obiekt JSON.')
    if meta.get('id') != call.name or meta.get('etap') != 'gotowy-do-wypelniania':
        raise ValueError('Nabór nie jest gotowy do tworzenia wniosków.')
    if meta.get('firma_id') or any((call / name).exists() for name in ('application.json', 'company.json', '.git', '02-analysis/company-fit.md')):
        raise ValueError('Nabór musi być wspólnym szablonem w głównym repozytorium.')
    form = Form(call)
    records = form.collect()
    if form.data.get('schema_version') != 2:
        raise ValueError('Wymagana mapa pól v2.')
    if any(r['wartosc'].strip() for r in records if r['typ_lokalizacji'] in {'tabela', 'blok'}):
        raise ValueError('Szablon naboru zawiera odpowiedzi. Przenieś je do osobnego wniosku.')
    if any(form.instances.values()):
        raise ValueError('Szablon zawiera rekordy projektu. Pozostaw puste tabele i szablony kart.')
    if (call / '02-analysis/assessment-profile.json').exists():
        from assessment_profile import validate as validate_assessment_profile
        validate_assessment_profile(call)
    # Walk also validates paths before copying or making a call visible.
    template_version(call)
    return meta


def application_manifest(path, expected_id=None):
    manifest = path / 'application.json'
    if manifest.is_symlink() or not manifest.resolve().is_relative_to(path.resolve()):
        raise ValueError('Manifest poza wnioskiem.')
    data = read_json(manifest)
    if not isinstance(data, dict) or data.get('schema_version') != 1 or data.get('id') != (expected_id or path.name):
        raise ValueError('application.json wymaga schema_version: 1 oraz id zgodnego z nazwą folderu.')
    identifier(data.get('nabor_id'))
    if not isinstance(data.get('tytul'), str) or not data['tytul'].strip():
        raise ValueError('Wniosek wymaga tytułu.')
    return data


def ensure_inbox(call):
    """Every application keeps its own inputs and attachments in its Git repository."""
    call = Path(call).resolve()
    path = call / 'inbox'
    if path.is_symlink() or not path.resolve().is_relative_to(call):
        raise ValueError('Inbox musi należeć do tego wniosku.')
    path.mkdir(exist_ok=True)
    marker = path / '.gitkeep'
    if not marker.exists() and not marker.is_symlink():
        marker.touch(exist_ok=True)
    return path


def create_application(root, call_id, title, id=None, *, applicant=None, prepare=None):
    root = Path(root).resolve()
    if not isinstance(title, str) or not title.strip() or len(title) > 300 or '\n' in title or '\r' in title:
        raise ValueError('Podaj nazwę wniosku (maksymalnie 300 znaków, jedna linia).')
    entry = next((r for r in registry(root / 'calls')['calls'] if r['id'] == call_id), None)
    if not entry or not entry['widoczny']:
        raise ValueError('Nabór jest ukryty lub nie istnieje w katalogu.')
    source = folder(root, 'calls', call_id)
    validate_template(source)
    id = identifier(id or f'{call_id}-{uuid.uuid4().hex[:12]}')
    target = folder(root, 'applications', id)
    with locked(root / '.panel/create-application.lock'):
        if target.exists():
            raise ValueError('Wniosek o tym identyfikatorze już istnieje.')
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix='.nowy-', dir=target.parent))
        try:
            version = template_version(source)
            for path in template_files(source):
                dest = staging / path.relative_to(source)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            if template_version(staging) != version or template_version(source) != version:
                raise ValueError('Szablon zmienił się podczas tworzenia wniosku. Spróbuj ponownie.')
            manifest = dict(schema_version=1, id=id, nabor_id=call_id, tytul=title.strip(),
                firma_id=applicant['id'] if applicant else None, utworzono_at=datetime.now(timezone.utc).isoformat(),
                szablon=dict(sha256=version, nabor_id=call_id))
            write_json(staging / 'application.json', manifest)
            if applicant:
                write_json(staging / 'company.json', [applicant])
                if prepare:
                    prepare(staging, applicant)
            ensure_inbox(staging)
            materials = staging / '04-project/materials'
            materials.mkdir(parents=True, exist_ok=True)
            (materials / '.gitkeep').touch(exist_ok=True)
            try:
                initialize_repository(staging, 'Utworzenie wniosku z przygotowanego naboru')
            except ValueError as exc:
                if 'git config user.' in str(exc):
                    raise ValueError('Ustaw własne git config --global user.name oraz user.email i ponów tworzenie wniosku.') from exc
                raise
            staging.rename(target)
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    publish = sub.add_parser('publish', help='Sprawdź pusty szablon i pokaż nabór w katalogu')
    publish.add_argument('call', type=Path)
    create = sub.add_parser('create', help='Utwórz osobny wniosek z lokalnym Git')
    create.add_argument('call_id')
    create.add_argument('--title', required=True)
    create.add_argument('--id')
    create.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        if args.command == 'publish':
            validate_template(args.call.resolve())
            register_call(args.call, visible=True)
            print(f'Nabór widoczny w katalogu: {args.call}')
        else:
            print(create_application(args.root, args.call_id, args.title, args.id))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'Błąd: {exc}\n')


if __name__ == '__main__':
    main()
