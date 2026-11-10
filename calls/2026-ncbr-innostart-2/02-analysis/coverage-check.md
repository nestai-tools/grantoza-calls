# Kontrola pokrycia formularza

Stan: 26.09.2026. Wzór 25 stron i instrukcja 62 strony porównane z mapą. **200 pól ma specyfikacje Q i mapowanie miejsc odpowiedzi w `fields.json` v2.** Do pracy służy 17 formularzy zbiorczych i 2 szablony pełnych kart (zadanie, osoba). W oryginalnej mapie 32 pola miały pochodzenie systemowe; część wartości wyliczamy lokalnie, pozostałe pozostają w OSF. Schematy powtarzalne liczone są jednokrotnie; rzeczywiste karty i wiersze powstaną po ustaleniu projektu.

| Sekcja | Liczba lokalnych pól | Zakres kontroli |
| --- | --- | --- |
| [00-system-data](../03-application/00-system-data/README.md) | 9 | Pola ze stron PDF: 2; etykiety, typ, limit, warunek, źródło i plik |
| [01-information](../03-application/01-information/README.md) | 10 | Pola ze stron PDF: 3, 4; etykiety, typ, limit, warunek, źródło i plik |
| [02-applicant](../03-application/02-applicant/README.md) | 49 | Pola ze stron PDF: 4, 5, 6; etykiety, typ, limit, warunek, źródło i plik |
| [02-1-eligibility](../03-application/02-1-eligibility/README.md) | 20 | Pola ze stron PDF: 6, 7, 8, 9, 10; etykiety, typ, limit, warunek, źródło i plik |
| [03-objective](../03-application/03-objective/README.md) | 10 | Pola ze stron PDF: 10, 11; etykiety, typ, limit, warunek, źródło i plik |
| [04-tasks](../03-application/04-tasks/README.md) | 11 | Pola ze stron PDF: 12, 13; etykiety, typ, limit, warunek, źródło i plik |
| [05-project-potential](../03-application/05-project-potential/README.md) | 4 | Pola ze stron PDF: 13, 14; etykiety, typ, limit, warunek, źródło i plik |
| [06-indicators](../03-application/06-indicators/README.md) | 16 | Pola ze stron PDF: 14, 15; etykiety, typ, limit, warunek, źródło i plik |
| [07-applicant-potential](../03-application/07-applicant-potential/README.md) | 5 | Pola ze stron PDF: 15, 16; etykiety, typ, limit, warunek, źródło i plik |
| [08-team](../03-application/08-team/README.md) | 14 | Pola ze stron PDF: 17; etykiety, typ, limit, warunek, źródło i plik |
| [09-advisor](../03-application/09-advisor/README.md) | 12 | Pola ze stron PDF: 18; etykiety, typ, limit, warunek, źródło i plik |
| [10-hrf](../03-application/10-hrf/README.md) | 17 | Pola ze stron PDF: 19; etykiety, typ, limit, warunek, źródło i plik |
| [11-attachments](../03-application/11-attachments/README.md) | 10 | Pola ze stron PDF: 20, 21; etykiety, typ, limit, warunek, źródło i plik |
| [12-declarations](../03-application/12-declarations/README.md) | 4 | Pola ze stron PDF: 21, 23, 24; etykiety, typ, limit, warunek, źródło i plik |
| [13-editor](../03-application/13-editor/README.md) | 3 | Pola ze stron PDF: 24; etykiety, typ, limit, warunek, źródło i plik |
| [14-access](../03-application/14-access/README.md) | 2 | Pola ze stron PDF: 24; etykiety, typ, limit, warunek, źródło i plik |
| [15-history](../03-application/15-history/README.md) | 4 | Pola ze stron PDF: 25; etykiety, typ, limit, warunek, źródło i plik |

## Sposób liczenia i zakres

- Sekcja 2: adresy rozbite na wymienione we wzorze składowe. Widok zbiorczy i edycja tych samych danych osoby używają tych samych pól.
- Sekcja 3: kod i opis innowacji są osobnymi polami słownika. Sekcja 6: cztery wskaźniki po trzy pola oraz dwie pary liczba/termin.
- Sekcja 10: wszystkie kolumny HRF; systemowe sumy zadania i całości zapisane jako dwa schematy z jawną listą dziewięciu sum. Tabelę strony 19 sprawdzono wizualnie.
- Sekcja 11: wszystkie 10 pozycji załączników i ich warunki. Wewnętrzne pola oświadczeń pozostają w oficjalnych wzorach PDF, a dane do ich przygotowania opisano w rejestrze załączników.
- Sekcja 12: cztery oświadczenia. Strony 22–23 zawierają pełną klauzulę informacyjną; jedno pole akceptacji na stronie 23 linkuje do tego źródła.
- Sekcje 13–15 i podsumowanie: uwzględniono dane systemowe, konfigurację dostępu i historię. Nie są tekstami merytorycznymi do napisania.
- Strona 1 jest spisem treści. Przyciski: Dodaj/Zmień kolejność, wybór i odświeżanie REGON, Pokaż/Usuń załącznik, Sprawdź kompletność, Gotowy, Odblokuj, Wyślij, Usuń wniosek, Drukuj — są operacjami interfejsu; nie mają osobnych odpowiedzi Q. Procedurę wysłania opisuje REQ-028. Żadnej z tych operacji nie wykonano w OSF.

## Wynik techniczny

Eksport odczytał 152 pola; 48 pozostałych definicji dotyczy niewprowadzonych jeszcze kart i wierszy. Wszystkie 200 definicji zachowało identyfikatory. **129 uwag** dotyczy brakujących odpowiedzi i wymaganych pozycji. Gotowość struktury pozwala rozpocząć pisanie; odpowiedzi nie są ukończone.

- Odpowiedzi mają jedno miejsce edycji: komórkę, blok tekstu lub pełną kartę.
- Wydatki i pozostałe grupy tabelaryczne wykrywane są po ID wierszy, karty po nazwach plików.
- Budżet wylicza sumy pozycji, zadań, kategorii i projektu; kontakt prowadzącego pochodzi z karty osoby.
- Testy obejmują odtwarzanie wszystkich 200 pól ze wspólnego generatora, dodawanie kart i wierszy, budżet oraz zachowanie poprzedniego eksportu przy błędnej tabeli.
- Walidacja zmienionych skilli `grants` i `grants-analysis` zakończyła się poprawnie.
- Sumy SHA-256 wszystkich 19 oryginałów są zgodne z rejestrem.

[Raport składania](../90-export/validation.md). Definicja odtwarzająca wzór: [source-form.json](source-form.json). Poprzedni układ jest w historii głównego Git.

## Granice gotowości

Nie ma blokera struktury opublikowanego formularza. Są braki danych companies/projektu oraz kwestie do potwierdzenia w określonych scenariuszach finansowania. Poradnik B+R oraz pięć dodatkowych materiałów z aktualności przejrzano częściowo w zakresie podanym w rejestrze; dokumenty określające pola, kryteria, koszty, umowę i załączniki odczytano. Nie sprawdzano zalogowanego OSF. Limity znaków zachowano z dokumentów, bez zgadywania liczenia spacji.

[Mapa formularza](../03-application/form-map.md) · [Rejestr źródeł](../01-sources/registry.md) · [Rozbieżności](discrepancies.md) · [Braki](gaps-and-questions.md)
