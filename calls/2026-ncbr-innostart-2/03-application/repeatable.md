# Dodawanie zadań, osób i wierszy

[Indeks formularzy](README.md)

## Najprościej — polecenie

Z katalogu projektu:

```bash
python3 skills/grants/scripts/add_record.py applications/<id-wniosku> zadania
python3 skills/grants/scripts/add_record.py applications/<id-wniosku> osoby
python3 skills/grants/scripts/add_record.py applications/<id-wniosku> wydatki
```

Polecenie tworzy pustą kartę albo dodaje wiersz i wybiera następne wolne ID. Można podać `--id Z-03`. Istniejące dane są zachowywane. Dostępne grupy: zadania, osoby, wydatki, reprezentanci, kis, dostepy.

## Ręczne dodawanie

- Zadanie: skopiuj `04-tasks/tasks/_template.md` do `Z-01.md` w tym samym folderze. Wszystkie pola zadania są w jednym pliku.
- Osoba: skopiuj `08-team/people/_template.md` do `O-01.md` w tym samym folderze.
- Wydatki: dopisz wiersz w tabeli budżetu z ID B-01, B-02 itd. Kolumna Zadanie wskazuje istniejące Z-01 itd.
- Reprezentanci: ID R-01 itd.; KIS: KIS-01 itd.; dostępy: D-01 itd.

Nie kopiuj ani nie modyfikuj Q przy dodawaniu pozycji. Eksport sam wykrywa karty i wiersze, zachowując identyfikację np. Q-097/Z-01. Zmiana kolejności wierszy nie zmienia ID. Szablony `_template.md` nie są rzeczywistymi rekordami i nie wchodzą do eksportu.

## Ograniczenia formularza

KIS: 1–2 pozycje. Zespół: jedna osoba prowadząca projekt i maksymalnie 15 członków; rola Coach IC wymaga sprawdzenia sposobu liczenia w OSF. Doradca ma oddzielny formularz. Wskaźniki i oświadczenia mają z góry określone wiersze. Każdy wydatek jest przypisany do jednego zadania i jednej kategorii kosztu.

Stan instancji w `90-export/answers.json` jest generowany. Nie trzeba utrzymywać odrębnej ręcznej listy w JSON.
