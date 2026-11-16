# PROO 1a — edycja 2027

**Nabór aktywny i gotowy do tworzenia wniosków.** Składanie w SOD: **16.11.2026, 12:00 – 16.12.2026, 12:00**, Europe/Warsaw. Stan źródeł sprawdzony 16.11.2026.

Przygotowano 10 formularzy z pełnymi kartami działań, rezultatów, osób i rocznego finansowania, trzy roczne kosztorysy, 228 pozycji mapy/specyfikacji (w tym 33 pomocnicze wyliczenia), 35 wymagań oraz mapę 9 kryteriów z profilem analizy jakości. Wszystkie miejsca odpowiedzi pozostają puste.

- [Metryka i warunki trzech ścieżek](00-overview.md)
- [Formularze do wypełniania](03-application/README.md) · [mapa pól](03-application/form-map.md)
- [Porównanie zrzutów 2027 z dokumentami 2026](02-analysis/comparison-2026-2027.md)
- [Wymagania](02-analysis/requirements.md) · [kryteria oceny](02-analysis/criteria.md)
- [Rozbieżności i kwestie do sprawdzenia](02-analysis/gaps-and-questions.md)
- [Rejestr źródeł](01-sources/registry.md) · [manifest dokumentów](documents.json)
- [Dokumenty i załączniki według etapu](06-attachments/README.md)
- [Kontrola techniczna](02-analysis/technical-checks.md) · [pokrycie HTML](02-analysis/form-coverage.json)

Zrzut 2027 ma układ zbliżony do DOCX 2026, lecz zawiera istotne zmiany: m.in. limity opisów, własną stronę ze sprawozdaniami, nowe oświadczenia o AI i odpłatnej pomocy. Reguły strategii i obowiązkowego audytu wynikają z regulaminu 2027. Nie uznano dokumentów 2026 za obowiązującą dokumentację tej edycji.

W źródłach zachowano m.in. błędne operatory progów przychodu w JS oraz sprzeczność zakresu premii strategicznej między główną tabelą a załącznikiem. To nie blokuje pustego formularza; **S-01 pozostaje nierozstrzygnięte** i nie wolno automatycznie przyznać premii, gdy wersje dają różny wynik. Pełne podstawy znajdują się w rejestrze rozbieżności.

Nowy wniosek utwórz przyciskiem „Nowy wniosek” w panelu lub przez `workspace.py create`. Wypełniaj jego własny folder w `applications/`; wspólny nabór jest pustym wzorem. Gotowość warsztatu nie oznacza kwalifikowalności organizacji ani gotowości oferty do wysłania.

## Zakres publicznego wydania

Wersja 1.0.0 zawiera analizę, wymagania, kryteria i pusty wzór formularza. Pliki źródłowe (PDF/DOCX/HTML), ich zasoby i ekstrakty oraz lokalne pliki wykonania/eksportu pozostają poza repozytorium publicznym. Źródła opisano w rejestrze i manifeście wraz z linkami i SHA-256.
