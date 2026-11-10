# Grantoza Calls

Publiczny katalog przeanalizowanych naborów: dokumenty źródłowe, wymagania,
kryteria oraz puste formularze do tworzenia niezależnych wniosków w Grantozie.

`index.json` zawiera opisy, tagi, odbiorców i wielkości firm, regiony,
harmonogramy potwierdzone i planowane oraz wersje i zgodność z aplikacją.
Brak informacji oznacza `null` lub pustą listę. Warunki w opisie i dokumentach
mają pierwszeństwo przed filtrem katalogu; wpis nie potwierdza kwalifikowalności firmy.

W lokalnej aplikacji: **Dodaj nabór → Katalog publiczny → Pobierz nabór**.
Nie jest wymagane konto GitHub. Import obejmuje tylko wybrany folder, sprawdza
SHA-256 plików i nie nadpisuje istniejących wzorów ani rozpoczętych wniosków.

## Struktura

- `index.json`: indeks kontraktu v1, tylko ostatnie zatwierdzone wydanie każdego ID.
- `calls/<id>/`: dokumenty, analiza, pusty formularz, `release.json` z listą i sumami plików.
- `schema/index.schema.json`: kontrakt indeksu.
- `scripts/validate.py`: walidator indeksu, sum, źródeł, profili oceny i pustych odpowiedzi.

Każdy nabór ma osobny SemVer. Indeks zapisuje wersję aplikacji przy utworzeniu,
analizie i pakowaniu oraz minimalną i opcjonalnie maksymalną wersję zgodności.
Historyczna wersja aplikacji może być nieznana (`null`). Poprzednie wydania
pozostają w historii Git; import jest przypięty do konkretnego commitu.

## Zgłaszanie naborów

Użyj skilla **grants-publish** w repozytorium aplikacji albo postępuj według
[CONTRIBUTING.md](CONTRIBUTING.md). Każda zmiana jest zgłaszana przez pull request.
Właściciel katalogu decyduje o scaleniu. Aplikacja czyta wyłącznie `main`.

Analizy i wzory są opracowaniami dokumentów. Oryginalne dokumenty zachowują
prawa i warunki ich wydawców. Nie umieszczaj danych wnioskodawców ani dokumentów
wewnętrznych bez upoważnienia do publicznego udostępnienia.
