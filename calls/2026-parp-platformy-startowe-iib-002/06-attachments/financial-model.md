# Model finansowy — przygotowanie

- [Oficjalny wzór: 12 i powyżej 12 miesięcy](../01-sources/originals/SRC-0ac9591da399-wzor-modelu-finansowego-zalacznik-nr-1-do-wniosku-o-dofinansowanie-okres-12-i-powyzej-1e5555b4a150.xlsx).
- [Oficjalny wzór: do 12 miesięcy](../01-sources/originals/SRC-02c1d0102fd0-wzor-modelu-finansowego-zalacznik-nr-1-do-wniosku-o-dofinansowanie-okres-do-12-miesie-38a5c2bf9d03.xlsx).
- [Instrukcja wypełniania modelu finansowego](../01-sources/originals/SRC-5dddf09c0cf4-instrukcja-wypelniania-modelu-finansowego-6c45cb00b228.pdf).
- [Kwestie do potwierdzenia](../02-analysis/gaps-and-questions.md).

Skopiuj właściwy wzór do folderu załączników własnego wniosku. Oryginały w 01-sources pozostają niezmienione. Dla dokładnie 12 miesięcy potwierdź wariant w PARP, ponieważ zakresy nazw i formuły wymagają wyjaśnienia. Panel nie zastępuje Excela ani nie liczy jego NPV/IRR.

## Kolejność pracy

1. Dane identyfikacyjne: nazwa i KRS spółki.
2. Prognoza przychodów: maksymalnie 3 strumienie, ich nazwy, kwoty i liczby płacących klientów. Dane na dzień złożenia oraz miesiące projektu i 12 miesięcy po nim. Zera w niewykorzystanych miesiącach zgodnie z instrukcją.
3. Prognoza kosztów: personel z kosztami pracodawcy, pośrednie, środki trwałe, WNiP, usługi, materiały, koszty dodatkowe i amortyzacja. Dozwolone powielanie wierszy kosztów; zachowaj zakresy sum i odniesienia.
4. Analiza opłacalności: żółte pola, właściwa stopa podatkowa, budżet ogółem, koszty kwalifikowalne, wkład i kapitał obrotowy. Dyskonto we wzorze: 4%.
5. Przelicz w Excelu/LibreOffice; sprawdź wszystkie formuły i błędy. Biblioteka openpyxl odczytuje formuły, ale nie oblicza ich wyników.
6. Uzgodnij HRF, tabelę finansowania, prognozę klientów i opisy zakresu. Dołącz wyjaśnienia założeń.

Kwoty netto w pełnych złotych; klienci w liczbach całkowitych. Nie edytuj automatycznych pól i formuł w celu uzyskania oczekiwanej oceny.

## Sprawdzone formuły i ograniczenia

Wariant dłuższy, Prognoza przychodów: AD5=(AC12-C12)/C12 oraz AE5=(AC13-C13)/C13. Arkusz Weryfikacja wzrostu wymaga co najmniej 150% dla co najmniej jednego z nich. Dla dodatniej bazy oznacza to 2,5-krotność wartości początkowej. Przy zerowej bazie formuły dzielą przez zero — nie podstawiaj fikcyjnej liczby.

Weryfikacja opłacalności w dłuższym modelu sprawdza NPV >=0 i IRR >0. Same obliczenia nie potwierdzają realizmu założeń. Wariant krótszy nie ma osobnych arkuszy weryfikacyjnych. Odczyt struktury nie jest audytem każdej formuły oficjalnego skoroszytu.

Instrukcja i oba pliki wskazują 01.01.2025 jako początek danych narastających, a KON na 31.12.2025. W naborze 2026 trzeba potwierdzić relację tych okresów do kryterium odnoszącego się do roku złożenia. Nie poprawiaj wzoru samodzielnie.
