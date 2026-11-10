"""Read grouped Markdown forms using explicit field locations (schema version 2)."""
import hashlib
import json
import os
from pathlib import Path
import re
from decimal import Decimal, InvalidOperation
from urllib.parse import quote, unquote, urlsplit

STATUSES = {'brak-danych', 'szkic', 'do-weryfikacji', 'zatwierdzone', 'nie-dotyczy'}
MARKER = re.compile(r'<!-- (pole|tabela):([A-Za-z0-9_-]+):(start|end) -->')


PLANNED_ATTACHMENT = 'Załącznik zostanie dodany — świadomie pominięty w ocenie.'


def attachment_field(field):
    # Keep in sync with panel/src/lib/form-layout.ts.
    return field.get('typ') == 'zalacznik' or bool(
        re.search(r'(?:^|-)attachments(?:-|$)', field.get('rozdzial', '')) and
        (re.search(r'_files?$', field.get('key', '')) or field.get('odpowiedz', {}).get('kolumna') == 'Plik'))


def planned_attachment(field, value):
    return attachment_field(field) and value.strip() == PLANNED_ATTACHMENT


def planned_issue(id, instance=None):
    return id + ('/' + instance if instance else '') + ': załącznik zaplanowany do dodania przed wysłaniem.'


def number(value):
    """Accept Polish decimal notation and space grouping; reject ambiguous values."""
    value = str(value).strip().replace('\u00a0', '').replace(' ', '').replace(',', '.')
    if not re.fullmatch(r'-?\d+(?:\.\d+)?', value):
        raise ValueError(f'Niepoprawna liczba: {value!r}')
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError(f'Niepoprawna liczba: {value!r}')
    return result


def money(value):
    return format(value.quantize(Decimal('.01')), 'f').replace('.', ',')


def split_row(line):
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        raise ValueError('Wiersz tabeli musi zaczynać i kończyć się znakiem |')
    cells, cell, i = [], '', 1
    while i < len(line)-1:
        char = line[i]
        if char == '\\' and i+1 < len(line)-1 and line[i+1] in '|\\':
            cell += line[i+1]; i += 2; continue
        if char == '|':
            cells.append(cell.strip()); cell = ''
        else:
            cell += char
        i += 1
    cells.append(cell.strip())
    return [re.sub(r'<br\s*/?>', '\n', c, flags=re.I) for c in cells]


def read_table(body):
    lines = [line for line in body.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError('Tabela wymaga nagłówka i separatora')
    header, sep = split_row(lines[0]), split_row(lines[1])
    if not header or header[0] != 'ID' or len(header) != len(set(header)):
        raise ValueError('Tabela wymaga unikalnych kolumn i pierwszej kolumny ID')
    if len(sep) != len(header) or any(not re.fullmatch(r':?-{3,}:?', s) for s in sep):
        raise ValueError('Niepoprawny separator tabeli')
    rows = {}
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(header):
            raise ValueError(f'Wiersz ma {len(cells)} komórek; oczekiwano {len(header)}. Znak | w treści zapisz jako \\|.')
        if not any(cells):
            continue
        rowid = cells[0]
        if not rowid or rowid in rows:
            raise ValueError(f'Brak lub powtórzone ID wiersza: {rowid!r}')
        rows[rowid] = dict(zip(header, cells))
    return header, rows


def segments(text):
    result, opened = {}, None
    for m in MARKER.finditer(text):
        kind, key, event = m.groups()
        if event == 'start':
            if opened or (kind, key) in result:
                raise ValueError(f'Powtórzony lub zagnieżdżony znacznik {kind}:{key}')
            opened = (kind, key, m.end())
        else:
            if not opened or opened[:2] != (kind, key):
                raise ValueError(f'Niepasujący koniec {kind}:{key}')
            result[(kind, key)] = text[opened[2]:m.start()].strip()
            opened = None
    if opened:
        raise ValueError(f'Brak końca znacznika {opened[0]}:{opened[1]}')
    return result


class Form:
    def __init__(self, call):
        self.call = Path(call).resolve()
        self.root = self.call/'03-application'
        self.data = json.loads((self.root/'fields.json').read_text(encoding='utf-8'))
        if self.data.get('schema_version') != 2:
            raise ValueError('Oczekiwano fields.json w wersji 2')
        self.fields = self.data['pola']
        self.byid = {f['id']: f for f in self.fields}
        if len(self.byid) != len(self.fields):
            raise ValueError('Powtórzone ID pola w mapie')
        self.groups = {g['id']: g for g in self.data.get('grupy', [])}
        if len(self.groups) != len(self.data.get('grupy', [])):
            raise ValueError('Powtórzone ID grupy')
        self.documents, self.tables, self.instances, self.cache = {}, {}, {}, {}
        self.used_segments, self.used_rows, self.active = set(), {}, set()
        self.issues = []
        for doc in self.data.get('formularze', []):
            self.path(doc['plik'])
        for f in self.fields:
            if not re.fullmatch(r'Q-\d+(?:-[a-z0-9]+)*', f['id']):
                raise ValueError('Niepoprawne ID pola: '+f['id'])
            self.path(f['plik'])  # specification, never an answer source
            loc = f['odpowiedz']
            if loc.get('grupa') and loc['grupa'] not in self.groups:
                raise ValueError('Nieznana grupa pola: '+f['id'])
            if loc.get('plik') and '{id}' not in loc['plik']:
                self.path(loc['plik'])
        for gid in self.groups:
            self.group_ids(gid)

    def path(self, relative, exists=True):
        p = (self.call/relative).resolve()
        if not p.is_relative_to(self.root.resolve()):
            raise ValueError('Ścieżka poza katalogiem wniosku: '+relative)
        if exists and not p.is_file():
            raise ValueError('Brak pliku: '+relative)
        return p

    def document(self, relative):
        if relative not in self.documents:
            p = self.path(relative)
            self.documents[relative] = segments(p.read_text(encoding='utf-8'))
        return self.documents[relative]

    def segment(self, relative, kind, key):
        docs = self.document(relative)
        if (kind, key) not in docs:
            raise ValueError(f'Brak znacznika {kind}:{key} w {relative}')
        self.used_segments.add((relative, kind, key))
        return docs[(kind, key)]

    def table(self, relative, key):
        cachekey = relative, key
        if cachekey not in self.tables:
            self.tables[cachekey] = read_table(self.segment(relative, 'tabela', key))
        return self.tables[cachekey]

    def group_ids(self, gid):
        if gid in self.instances:
            return self.instances[gid]
        g = self.groups[gid]
        if g['typ'] == 'tabela':
            _, rows = self.table(g['plik'], g['tabela'])
            result = list(rows)
            for col, choices in g.get('opcje_kolumn', {}).items():
                if col not in self.table(g['plik'], g['tabela'])[0]:
                    raise ValueError('Brak kolumny '+col)
                for rowid, row in rows.items():
                    if row[col] and row[col] not in choices:
                        self.issues.append(f'{rowid}: niedozwolona wartość kolumny {col}: {row[col]}.')
            self.used_rows.setdefault((g['plik'], g['tabela']), set()).update(result)
        elif g['typ'] == 'karty':
            folder = self.path(g['folder']+'/_placeholder', exists=False).parent
            self.path(g['szablon'])
            result = []
            for p in sorted(folder.glob('*.md')):
                if p.name.startswith('_') or p.name == 'README.md':
                    continue
                self.path(str(p.relative_to(self.call)))
                result.append(p.stem)
        else:
            raise ValueError('Nieznany typ grupy '+gid)
        for id in result:
            if not re.fullmatch(g['id_regex'], id):
                raise ValueError(f'Niepoprawny identyfikator {id} w grupie {gid}')
        self.instances[gid] = result
        if len(result) < g.get('min', 0):
            self.issues.append(f'{gid}: brakuje pozycji; minimum {g["min"]}.')
        if g.get('max') is not None and len(result) > g['max']:
            self.issues.append(f'{gid}: przekroczona liczba pozycji {len(result)}/{g["max"]}.')
        return result

    def cell(self, loc, instance):
        relative = loc['plik'].replace('{id}', instance or '')
        header, rows = self.table(relative, loc['tabela'])
        row = instance if loc.get('wiersz') == '*' else loc['wiersz']
        column = loc['kolumna']
        if column not in header or row not in rows:
            raise ValueError(f'Brak komórki {relative}: {loc["tabela"]}/{row}/{column}')
        self.used_rows.setdefault((relative, loc['tabela']), set()).add(row)
        return rows[row][column]

    def value(self, qid, instance=None):
        key = qid, instance
        if key in self.cache:
            return self.cache[key]
        if key in self.active:
            raise ValueError('Cykl zależności pól: '+qid)
        if qid not in self.byid:
            raise ValueError('Brak pola zależnego: '+qid)
        self.active.add(key)
        f = self.byid[qid]; loc = f['odpowiedz']; typ = loc['typ']
        if typ == 'tabela':
            value = self.cell(loc, instance)
        elif typ == 'blok':
            value = self.segment(loc['plik'].replace('{id}', instance or ''), 'pole', loc['blok'])
        elif typ == 'osf':
            value = ''
        elif typ == 'stala':
            value = str(loc['wartosc'])
        elif typ == 'wyliczane':
            try:
                value = self.calculate(loc, instance)
            except (InvalidOperation, ArithmeticError, ValueError) as e:
                # Structural and dependency errors must not hide behind an empty calculation.
                if isinstance(e, ValueError) and not str(e).startswith('Niepoprawna liczba:'):
                    raise
                self.issues.append(f'{qid}/{instance or ""}: nie można obliczyć wartości: {e}')
                value = ''
        else:
            raise ValueError('Nieznany typ lokalizacji '+str(typ))
        if typ in {'stala', 'wyliczane', 'osf'} and loc.get('tabela'):
            self.cell(loc, instance)  # display location is still part of coverage
        self.active.remove(key); self.cache[key] = value
        return value

    def calculate(self, loc, instance):
        op = loc['operacja']
        if op == 'rok':
            from datetime import date
            raw = self.value(loc['pole'])
            if not raw:
                return ''
            try:
                return str(date.fromisoformat(raw).year + loc.get('przesuniecie', 0))
            except ValueError:
                self.issues.append('Niepoprawna data: ' + raw)
                return ''
        if op == 'dodatnie':
            raw = self.value(loc['pole'], instance if loc.get('ta_sama_instancja') else None)
            return str(int(number(raw) > 0)) if raw else ''
        if op in {'roznica', 'procent', 'pomnoz'}:
            a = self.value(loc['lewe'], instance)
            b = self.value(loc['prawe'], instance) if 'prawe' in loc else str(loc['mnoznik'])
            if not a or not b:
                return ''
            a, b = number(a), number(b)
            if op == 'procent':
                return money(a / b * 100) if b else ''
            return money(a-b if op == 'roznica' else a*b)
        if op == 'kolejnosc':
            return str(self.group_ids(loc['grupa_zrodlowa']).index(instance)+1)
        if op == 'wybierz_z_grupy':
            ids = [id for id in self.group_ids(loc['grupa_zrodlowa']) if self.value(loc['pole_wyboru'], id) == loc['wartosc_wyboru']]
            if len(ids) > 1:
                self.issues.append('Więcej niż jedna osoba prowadząca projekt; dane kontaktowe wymagają rozstrzygnięcia.')
            return self.value(loc['pole'], ids[0]) if len(ids) == 1 else ''
        if op == 'pole':
            return self.value(loc['pole'], instance if loc.get('ta_sama_instancja') else None)
        if op == 'polacz':
            return ' '.join(v for p in loc['pola'] if (v := self.value(p, instance)))
        if op == 'dodaj':
            vs = [self.value(p, instance) for p in loc['pola']]
            return money(sum(map(number, vs))) if all(vs) else ''
        if op == 'kategoria':
            selected = self.cell(loc['wybor'], instance)
            total = self.value(loc['pole_kwoty'], instance)
            return (total if selected == loc['kategoria'] else '0,00') if selected and total else ''
        if op == 'z_powiazania':
            linked = self.cell(loc['powiazanie'], instance)
            if not linked:
                return ''
            if linked not in self.group_ids(loc['grupa_docelowa']):
                self.issues.append(f'{instance}: brak powiązanej pozycji {linked}.'); return ''
            return linked if not loc.get('pole') else self.value(loc['pole'], linked)
        if op == 'suma':
            ids = self.group_ids(loc['grupa_zrodlowa'])
            if loc.get('filtr'):
                ids = [id for id in ids if self.cell(loc['filtr'], id) == instance]
            if loc.get('pole_filtra'):
                ids = [id for id in ids if self.value(loc['pole_filtra'], id) == loc.get('wartosc_filtra', instance)]
            if not ids:
                return '0,00' if loc.get('pusta_grupa_zero') else ''
            values = [self.value(loc['pole'], id) for id in ids]
            return money(sum(map(number, values))) if all(values) else ''
        if op == 'podsumowanie':
            ids = self.group_ids(loc['grupa_zrodlowa'])
            if loc.get('filtr'):
                ids = [id for id in ids if self.cell(loc['filtr'], id) == instance]
            if not ids:
                return ''
            rows = ['| Kategoria | Kwota (PLN) |','| --- | --- |']
            for name, qid in loc['kolumny'].items():
                values = [self.value(qid, id) for id in ids]
                rows.append(f'| {name} | {money(sum(map(number, values))) if all(values) else ""} |')
            return '\n'.join(rows)
        raise ValueError('Nieznana operacja '+op)

    def check_value(self, f, value, instance):
        if f['odpowiedz']['typ'] in {'osf','stala'}:
            return
        if f['odpowiedz']['typ'] == 'wyliczane':
            if value and f.get('typ') == 'liczba':
                try:
                    n = number(value)
                    if 'maksimum' in f and n > number(f['maksimum']):
                        self.issues.append(f'{f["id"]}: wyliczona wartość przekracza {f["maksimum"]}.')
                    if 'minimum' in f and n < number(f['minimum']):
                        self.issues.append(f'{f["id"]}: wyliczona wartość poniżej {f["minimum"]}.')
                except ValueError:
                    self.issues.append(f'{f["id"]}: niepoprawna wyliczona liczba.')
            return
        label = f['id']+(f'/{instance}' if instance else '')
        assessment = f.get('oceny_instancji', {}).get(instance, {}) if instance else f
        status = assessment.get('status','brak-danych')
        if status not in STATUSES:
            raise ValueError('Nieznany status '+label)
        if planned_attachment(f, value):
            self.issues.append(planned_issue(f['id'], instance))
            return
        if status == 'nie-dotyczy':
            if not assessment.get('uzasadnienie_statusu'):
                self.issues.append(f'{label}: nie-dotyczy wymaga uzasadnienia.')
            if value:
                self.issues.append(f'{label}: nie-dotyczy ma wpisaną odpowiedź; sprawdź zastosowanie.')
            return
        if not value:
            if f.get('wymagane', True):
                self.issues.append(f'{label}: pusta odpowiedź; warunek: {f.get("warunek", "zawsze")}.')
            return
        if status != 'zatwierdzone':
            self.issues.append(f'{label}: odpowiedź wymaga przeglądu ({status if status != "brak-danych" else "szkic"}).')
        elif assessment.get('sha256_zatwierdzonej_odpowiedzi') != hashlib.sha256(value.encode()).hexdigest():
            self.issues.append(f'{label}: brak aktualnego potwierdzenia zatwierdzenia treści.')
        limit = f.get('limit_znakow'); method = f.get('sposob_liczenia','nieustalony')
        if method not in {'ze-spacjami','bez-spacji','nieustalony'}:
            raise ValueError('Nieznany sposób liczenia '+label)
        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError('Niepoprawny limit '+label)
            if method == 'nieustalony':
                self.issues.append(f'{label}: sposób liczenia znaków wymaga sprawdzenia w {self.data.get("portal", "OSF")}.')
            else:
                count = len(value) if method == 'ze-spacjami' else len(re.sub(r'\s','',value))
                if count > limit:
                    self.issues.append(f'{label}: przekroczony limit {count}/{limit} znaków.')
                if count < f.get('minimum_znakow', 0):
                    self.issues.append(f'{label}: poniżej minimum {f["minimum_znakow"]} znaków.')
        if f.get('typ') == 'liczba':
            try:
                n = number(value)
                if 'minimum' in f and n < number(f['minimum']):
                    self.issues.append(f'{label}: wartość poniżej {f["minimum"]}.')
                if 'maksimum' in f and n > number(f['maksimum']):
                    self.issues.append(f'{label}: wartość powyżej {f["maksimum"]}.')
                if f.get('calkowita') and n != n.to_integral_value():
                    self.issues.append(f'{label}: wymagana liczba całkowita.')
            except ValueError:
                self.issues.append(f'{label}: niepoprawna liczba {value!r}.')
        choices = value.splitlines() if f.get('wielokrotny') else [value]
        if f.get('opcje') and f.get('opcje_scisle') and any(v not in f['opcje'] for v in choices):
            self.issues.append(f'{label}: niedozwolony wybór {value!r}.')
        if f.get('wielokrotny') and len(choices) != len(set(choices)):
            self.issues.append(f'{label}: powtórzony wybór.')
        if any(v in f.get('opcje_wylaczne', []) for v in choices) and len(choices) > 1:
            self.issues.append(f'{label}: wybór wyłączny nie może występować z innymi opcjami.')
        if f.get('grupa_powiazana') and value not in self.group_ids(f['grupa_powiazana']):
            self.issues.append(f'{label}: nie istnieje powiązana pozycja {value}.')
        if f.get('typ') == 'data':
            from datetime import date
            try:
                date.fromisoformat(value)
            except ValueError:
                self.issues.append(f'{label}: podaj datę RRRR-MM-DD.')
        if re.search(r'BRAK DANYCH|DO POTWIERDZENIA|DO UZUPEŁNIENIA|\bTODO\b', value, re.I):
            self.issues.append(f'{label}: znacznik roboczy w odpowiedzi.')

    def check_relations(self):
        for rule in self.data.get('kontrole', []):
            scopes = self.group_ids(rule['grupa']) if rule.get('grupa') else [None]
            for id in scopes:
                a, b = self.value(rule['lewe'], id), self.value(rule['prawe'], id)
                if not a or not b:
                    continue
                try:
                    left, right = number(a), number(b)*number(rule.get('mnoznik', 1))
                except ValueError:
                    continue
                op = rule['operator']
                valid = {'<=':left<=right,'>=':left>=right,'=':left==right}
                if op not in valid:
                    raise ValueError('Nieznany operator kontroli '+op)
                if not valid[op]:
                    self.issues.append(f'{rule["opis"]}'+(f' ({id})' if id else ''))
        for g in self.groups.values():
            for constraint in g.get('liczebnosc', []):
                count = sum(self.value(constraint['pole'], id) == constraint['wartosc'] for id in self.group_ids(g['id']))
                if count < constraint.get('min',0) or count > constraint.get('max',10**9):
                    self.issues.append(f'{g["id"]}: niepoprawna liczba pozycji {constraint["wartosc"]}: {count}.')

    def check_coverage(self):
        for relative, segs in self.documents.items():
            for (kind,key),body in segs.items():
                if (relative,kind,key) not in self.used_segments:
                    raise ValueError(f'Niezmapowany blok {kind}:{key} w {relative}')
        for key,(_,rows) in self.tables.items():
            if extra := set(rows)-self.used_rows.get(key,set()):
                raise ValueError(f'Niezmapowane wiersze {sorted(extra)} w {key}')
        expected = {self.path(f['plik']) for f in self.fields}
        actual = set(self.root.rglob('specification/Q-*.md'))
        if expected != actual:
            raise ValueError('Specyfikacje Q i mapa pól nie pokrywają się dokładnie')

    def collect(self):
        records = []
        # Reading declared forms ensures orphan answer markers are detected too.
        for doc in self.data.get('formularze', []):
            self.document(doc['plik'])
        for f in self.fields:
            loc = f['odpowiedz']; group = loc.get('grupa')
            scopes = self.group_ids(group) if group else [None]
            for id in scopes:
                value = self.value(f['id'], id)
                self.check_value(f, value, id)
                records.append(dict(id=f['id'],instancja=id,pole=f['pole'],rozdzial=f['rozdzial'],
                                    wartosc=value,typ_lokalizacji=loc['typ'],plik=loc.get('plik','').replace('{id}',id or '')))
        self.check_relations(); self.check_coverage()
        return records


def relocate(value, origin, call):
    if not origin:
        return value
    def replace(m):
        u = urlsplit(m[2].strip('<>'))
        if u.scheme or u.netloc or m[2].startswith(('#','/')):
            return m[0]
        target = (call/origin).parent/unquote(u.path)
        url = quote(os.path.relpath(target,call/'90-export'),safe='/.-_')
        if u.query: url += '?'+u.query
        if u.fragment: url += '#'+u.fragment
        return f'{m[1]}({url})'
    return re.sub(r'(!?\[[^\]]*\])\(([^)]+)\)',replace,value)


def build_grouped(call):
    form = Form(call); records = form.collect()
    parts = ['# Wniosek — eksport roboczy\n']; current = None
    for r in records:
        if r['rozdzial'] != current:
            current = r['rozdzial']; parts.append(f'## {current}\n')
        suffix = f' — {r["instancja"]}' if r['instancja'] else ''
        if r['typ_lokalizacji'] == 'osf':
            continue
        parts.append(f'### {r["id"]}{suffix} — {r["pole"]}\n\n{relocate(r["wartosc"],r["plik"],form.call)}\n')
    issues = list(dict.fromkeys(form.issues))
    out = form.call/'90-export';out.mkdir(exist_ok=True)
    report = f'# Kontrola formularzy\n\nSpecyfikacje: {len(form.fields)}. Odczytane pola wraz z instancjami: {len(records)}. Uwagi: {len(issues)}.\n\n'
    report += '\n'.join('- '+i for i in issues) or 'Brak uwag technicznych.'
    report += '\n\nPuste pola warunkowe wymagają oceny zastosowania; pola systemowe i wyliczane nie wymagają ręcznego wpisania.\nKontrola nie potwierdza kwalifikowalności, dokumentów załączników ani walidacji aktywnego formularza organizatora.\n'
    # Parsing/coverage fails before any previous export is touched.
    overview = ['# Zestawienia — generowane z formularzy', '', 'Odpowiedzi edytuj w formularzach źródłowych. Puste sumy oznaczają brak pełnych danych.', '']
    def cell(value):
        return value.replace('|', '\\|').replace('\n','<br>')
    for gid, instance_ids in form.instances.items():
        overview += ['## '+gid, '', '| ID | Formularz / karta |', '| --- | --- |']
        g = form.groups[gid]
        for id in instance_ids:
            relative = (g['folder']+'/'+id+'.md') if g['typ']=='karty' else g['plik']
            overview.append(f'| {id} | [Otwórz](../{relative}) |')
        if not instance_ids: overview.append('| — | Brak pozycji |')
        overview.append('')
    overview += ['## Wartości wyliczone', '', '| Pole | Pozycja | Wartość |', '| --- | --- | --- |']
    for r in records:
        if r['typ_lokalizacji'] == 'wyliczane' and r['wartosc']:
            overview.append(f'| {cell(r["pole"])} | {r["instancja"] or "projekt"} | {cell(r["wartosc"])} |')
    (out/'summaries.md').write_text('\n'.join(overview)+'\n', encoding='utf-8')
    (out/'application.md').write_text('\n'.join(parts),encoding='utf-8')
    (out/'validation.md').write_text(report,encoding='utf-8')
    (out/'answers.json').write_text(json.dumps(dict(schema_version=2,odpowiedzi=records,instancje=form.instances),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return out, issues


def record_archive(call, group_id, instance_id):
    if not all(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]+', value)
               for value in (group_id, instance_id)):
        raise ValueError('Niepoprawny identyfikator pozycji')
    root = Path(call).resolve()
    path = root / '04-project/usuniete-pozycje' / group_id / (instance_id + '.json')
    if path.resolve() != path:
        raise ValueError('Archiwum pozycji nie może być dowiązaniem')
    return path


def add_record(call, group_id, instance_id=None):
    form = Form(call)
    if group_id not in form.groups:
        raise ValueError('Nieznana grupa '+group_id)
    g = form.groups[group_id]; existing = form.group_ids(group_id)
    if instance_id is None:
        n = 1
        while (f'{g["prefix"]}-{n:02}' in existing or
               record_archive(call, group_id, f'{g["prefix"]}-{n:02}').exists()): n += 1
        instance_id = f'{g["prefix"]}-{n:02}'
    if (not re.fullmatch(g['id_regex'],instance_id) or instance_id in existing or
            record_archive(call, group_id, instance_id).exists()):
        raise ValueError('Niepoprawne lub istniejące ID '+instance_id)
    if len(existing) >= g.get('max',10**9):
        raise ValueError('Osiągnięto limit pozycji grupy '+group_id)
    if g['typ'] == 'karty':
        template = form.path(g['szablon']).read_text(encoding='utf-8')
        # Instance filenames supply IDs; no manual duplication of schema entries.
        target = form.path(g['folder']+'/'+instance_id+'.md',exists=False)
        with target.open('x',encoding='utf-8') as stream: stream.write(template)
    else:
        target = form.path(g['plik']);text = target.read_text(encoding='utf-8')
        header,_ = form.table(g['plik'],g['tabela'])
        end = f'<!-- tabela:{g["tabela"]}:end -->'
        line = '| '+' | '.join([instance_id]+['']*(len(header)-1))+' |\n'
        target.write_text(text.replace(end,line+end),encoding='utf-8')
    return target,instance_id
