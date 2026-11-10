#!/usr/bin/env python3
"""Validate call-specific input and output contracts for the assessment service."""
import argparse
import hashlib
import json
from pathlib import Path
import re

PROFILE_PATH = '02-analysis/assessment-profile.json'
STATUSES = {'supported', 'partial', 'missing', 'contradicted', 'not_applicable', 'insufficient_context'}


def validate_response(value):
    if not isinstance(value, dict) or value.get('typ') not in {'choice', 'score'}:
        raise ValueError('Profil: odpowiedź wymaga typu choice albo score.')
    if value['typ'] == 'choice':
        if set(value) != {'typ', 'warianty'} or not isinstance(value['warianty'], dict) or not 2 <= len(value['warianty']) <= 32:
            raise ValueError('Profil: niepoprawne warianty odpowiedzi.')
        entries = list(value['warianty'].values())
        if any(not re.fullmatch(r'[a-z][a-z0-9_]{0,63}', key) for key in value['warianty']):
            raise ValueError('Profil: niepoprawny identyfikator wariantu.')
    else:
        if set(value) != {'typ', 'poziomy'} or not isinstance(value['poziomy'], list) or not 2 <= len(value['poziomy']) <= 10:
            raise ValueError('Profil: skala wymaga 2–10 poziomów.')
        entries = value['poziomy']
    for entry in entries:
        if (not isinstance(entry, dict) or set(entry) != {'opis', 'status'} or entry['status'] not in STATUSES
                or not isinstance(entry['opis'], str) or not entry['opis'].strip() or len(entry['opis']) > 4000):
            raise ValueError('Profil: każdy wariant lub poziom wymaga opisu i statusu wyniku.')
    if not {'supported', 'missing', 'partial', 'contradicted', 'insufficient_context'} <= {e['status'] for e in entries}:
        raise ValueError('Profil: rozróżnij uzasadnienie, częściowe dane, brak, sprzeczność i brak kontekstu.')


def validate_profile(profile, fields, criteria, nabor_id):
    required = {'schema_version', 'id', 'wersja', 'nabor_id', 'nazwa', 'zrodla_sha256', 'wejscie', 'wyjscie', 'kryteria', 'spojnosc', 'analiza_poglebiona'}
    if not isinstance(profile, dict) or set(profile) != required or type(profile['schema_version']) is not int or profile['schema_version'] != 1:
        raise ValueError('Niepoprawna struktura profilu oceny.')
    if profile['nabor_id'] != nabor_id:
        raise ValueError('Profil oceny pochodzi z innego naboru.')
    if not isinstance(profile['id'], str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,100}', profile['id']):
        raise ValueError('Profil wymaga stałego identyfikatora.')
    if type(profile['wersja']) is not int or profile['wersja'] < 1:
        raise ValueError('Profil wymaga dodatniej wersji.')
    def text(value, name):
        if not isinstance(value, str) or not value.strip() or len(value) > 12000:
            raise ValueError('Profil: niepoprawny opis ' + name)
    def ids(value):
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value) or len(set(value)) != len(value) or set(value) - fields.keys():
            raise ValueError('Profil: nieznane lub powtórzone pola kontekstu.')
    text(profile['nazwa'], 'nazwy')
    hashes = profile['zrodla_sha256']
    if not isinstance(hashes, dict) or not hashes or any(not isinstance(v, str) or not re.fullmatch('[a-f0-9]{64}', v) for v in hashes.values()):
        raise ValueError('Profil wymaga skrótów dokumentów źródłowych.')
    inp = profile['wejscie']
    if not isinstance(inp, dict) or set(inp) != {'instrukcja', 'pola_kontekstu', 'powiazania', 'krotka_odpowiedz_max', 'budzet_powiazan'}:
        raise ValueError('Profil: niepoprawne zasady wejścia.')
    text(inp['instrukcja'], 'wejścia'); ids(inp['pola_kontekstu'])
    if type(inp['powiazania']) is not bool or type(inp['krotka_odpowiedz_max']) is not int or not 0 <= inp['krotka_odpowiedz_max'] <= 500:
        raise ValueError('Profil: niepoprawny zakres wspólnego kontekstu.')
    if type(inp['budzet_powiazan']) is not int or not 0 <= inp['budzet_powiazan'] <= 40000:
        raise ValueError('Profil: niepoprawny budżet kontekstu sekcji.')
    out = profile['wyjscie']
    if not isinstance(out, dict) or set(out) != {'odpowiedz', 'etykiety', 'agregacja'} or out['agregacja'] not in {'sprawdzenia', 'kryteria'}:
        raise ValueError('Profil: niepoprawne zasady wyjścia.')
    validate_response(out['odpowiedz'])
    if not isinstance(out['etykiety'], dict) or set(out['etykiety']) != STATUSES:
        raise ValueError('Profil wymaga etykiet wszystkich statusów.')
    for label in out['etykiety'].values(): text(label, 'etykiety wyniku')
    rules = profile['kryteria']
    byid = {c['id']: c for c in criteria}
    if {s['id'] for c in criteria for s in c['zrodla']} - hashes.keys():
        raise ValueError('Profil nie obejmuje wszystkich źródeł mapy kryteriów.')
    if not isinstance(rules, dict) or set(rules) != set(byid):
        raise ValueError('Profil musi obejmować dokładnie wszystkie kryteria naboru.')
    for id, rule in rules.items():
        if not isinstance(rule, dict) or not {'tryb','instrukcja','pola_kontekstu'} <= set(rule) or set(rule) - {'tryb','instrukcja','pola_kontekstu','odpowiedz'}:
            raise ValueError('Profil: niepoprawne ustawienia kryterium ' + id)
        if rule['tryb'] not in {'model', 'formularz', 'zewnetrzne'}:
            raise ValueError('Profil: nieznany tryb kryterium ' + id)
        if (rule['tryb'] == 'formularz') != bool(byid[id].get('ocena_formularza')):
            raise ValueError('Profil: tryb deklaracji nie odpowiada mapie kryterium ' + id)
        text(rule['instrukcja'], id); ids(rule['pola_kontekstu'])
        if 'odpowiedz' in rule:
            if rule['tryb'] != 'model': raise ValueError('Skala odpowiedzi dotyczy wyłącznie oceny modelu.')
            validate_response(rule['odpowiedz'])
    consistency = profile['spojnosc']
    if not isinstance(consistency, dict) or set(consistency) != {'aspekty', 'pola_kontekstu'} or not isinstance(consistency['aspekty'], list) or not consistency['aspekty']:
        raise ValueError('Profil: brak zasad pomocniczej oceny spójności.')
    for aspect in consistency['aspekty']: text(aspect, 'spójności')
    ids(consistency['pola_kontekstu']); text(profile['analiza_poglebiona'], 'dogłębnej analizy')
    return profile


def verify_sources(call, profile):
    call = Path(call).resolve()
    path = call/'documents.json'
    if not path.resolve().is_relative_to(call): raise ValueError('Rejestr dokumentów poza wnioskiem.')
    docs = {d['id']:d for d in json.loads(path.read_text())['dokumenty']}
    for id, expected in profile['zrodla_sha256'].items():
        doc = docs.get(id, {})
        path = call/doc.get('plik', '__missing__')
        if (doc.get('sha256') != expected or not path.resolve().is_relative_to(call) or not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != expected):
            raise ValueError('Profil oceny nie odpowiada wersji źródła ' + id)


def validate(call):
    call = Path(call).resolve()
    def read(relative):
        path = call/relative
        if not path.resolve().is_relative_to(call): raise ValueError('Profil lub mapa poza naborem.')
        return json.loads(path.read_text())
    profile = read(PROFILE_PATH)
    fields = {f['id']:f for f in read('03-application/fields.json')['pola']}
    criteria = read('02-analysis/assessment-criteria.json')['kryteria']
    validate_profile(profile, fields, criteria, read('call.json')['id'])
    verify_sources(call, profile)
    return profile


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('call', type=Path)
    args = parser.parse_args()
    try:
        p = validate(args.call); print(f"Profil poprawny: {p['id']} v{p['wersja']}")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc)+'\n')
