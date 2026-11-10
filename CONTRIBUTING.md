# Zgłaszanie gotowego naboru

1. Przeanalizuj dokumenty i odwzoruj cały formularz w Grantozie.
2. Sprawdź źródła, kryteria, reguły i limity. Zachowaj opis braków i rozbieżności.
3. Przejrzyj wszystkie pliki, w tym metadane binarne. Publikuj tylko publiczne
   dokumenty i puste wzory. Usuń dane firmy, osób, lokalne ścieżki i stan wykonywania AI.
4. Uzupełnij opis, tagi, odbiorców, wielkości firm, regiony i harmonogram wraz
   ze źródłami. Rozdziel daty ogłoszone od przewidywanych. Nie zgaduj braków.
5. Zwiększ `call_version`. Pierwsza wersja to `1.0.0`. Nie zmieniaj wydania
   bez podniesienia wersji. Ustal zgodność z wersjami aplikacji.
6. Skill `grants-publish` uruchamia `public_catalog.py build` w repo aplikacji,
   tworzy `release.json` i aktualizuje indeks. Nie dopisuj SHA ręcznie.
7. Tutaj uruchom `python3 -m pip install 'jsonschema>=4,<5'` i
   `python3 scripts/validate.py`. Otwórz PR do `main` (fork, jeśli brak uprawnień).

Opisz źródła, zakres analizy, anonimizację, braki, wersję i wyniki walidacji.
Nie publikuj `applications/`, `companies/`, `.panel/`, prywatnego inboxa,
odpowiedzi, materiałów projektu ani pełnej historii lokalnego repo aplikacji.
Nie scalaj własnych zgłoszeń automatycznie. Maintainer wybiera nabory do katalogu.

Walidator w `tools/grantoza/` jest przypiętą kopią narzędzi aplikacji 0.2.0.
Zmiany kontraktu wymagają osobnego przeglądu aktualizacji schematu i walidatora.
