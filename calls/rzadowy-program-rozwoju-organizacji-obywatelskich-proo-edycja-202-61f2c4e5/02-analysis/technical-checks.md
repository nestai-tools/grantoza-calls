# Kontrola techniczna wzoru PROO 1a 2027

Wykonano na pustym wzorze i jego kopii tymczasowej. Dane testowe nie trafiły do naboru.

- 228 specyfikacji Q pokrywa mapę dokładnie raz; 10 formularzy głównych, 7 szablonów kart, 3 grupy wierszy kosztów.
- Pokryto 10 stron HTML, 127 kontrolek odpowiadających 112 unikalnym nazwom pól, oraz tekstowe podsumowania i wartości systemowe/stałe; brak nieodwzorowanych pól zrzutów.
- Dodano wszystkie grupy na kopii; sprawdzono maksymalnie jedną kartę finansowania na rok.
- Sprawdzono zapis i ponowny odczyt 33 pól ze słownikami, wielowierszowych opisów i powiązań działania z rezultatem i kosztem.
- Budżet ścieżki 1 sumuje wyłącznie 2027 bez wymuszania pustych kart 2028/2029; budżet trzyletni sumuje dotację, wkłady, inwestycje i udziały. Każde działanie ma wyliczaną sumę kosztów z powiązań.
- Brak ceny istniejącego wydatku pozostawia sumę pustą, zamiast zmieniać ją w zero. Rozbieżność źródeł i kosztów daje komunikat.
- Dane panelu, układ kart i podpowiedzi zostały odczytane przez ten sam kod `Store`/`layout`, którego używa panel. Roczne finansowanie pokazano jako listę pól w pełnej karcie, zachowując oficjalne znaczenia tabeli.
- Podgląd analizy jakości i profilu działa bez wywoływania zewnętrznego API. Kryterium strategiczne ze sprzecznymi źródłami nie otrzymuje potwierdzonej interpretacji.
- Składanie `build_application.py` zapisuje komplet techniczny eksportu. 67 uwag pustego wzoru dotyczy oczekiwanych braków odpowiedzi/kart, bez błędów struktury.
- Zweryfikowano SHA-256 22 zarejestrowanych źródeł. Oględziny tabel regulaminu na s. 66 i 68 potwierdzają zapisane rozbieżności.

Kontrola nie potwierdza uprawnienia żadnej organizacji, prawdziwości oświadczeń, podpisów, załączników ani wyniku walidacji aktywnego SOD. Limity dat/dotacji i wkład każdej inwestycji wymagają sprawdzenia według [wymagań](requirements.md) podczas przygotowania konkretnej oferty.
