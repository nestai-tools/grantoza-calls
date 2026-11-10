# Braki i ustalenia do potwierdzenia

Formularz jest odwzorowany. Poniższe kwestie dotyczą interpretacji danych i finalnego złożenia.

## D-01 — Rok bazowy modelu

Nabór jest w 2026 r. Kryterium 6 odnosi się do roku złożenia wniosku, natomiast instrukcja modelu s. 2 i komórka C3 Prognozy przychodów obu XLSX wskazują narastająco od 01.01.2025. Instrukcja s. 5 wskazuje KON na 31.12.2025.

Wpływ: Dane i porównywalność prognozy; nie zmienia struktury pól. Nie zmieniaj samodzielnie oficjalnych formuł.

Status: do-potwierdzenia-w-PARP. Źródła: SRC-894f1179eb3f, SRC-0fb046c95a8b, SRC-5dddf09c0cf4, SRC-0ac9591da399, SRC-02c1d0102fd0.

## D-02 — Dokładnie 12 miesięcy

Nazwy wariantów „12 i powyżej” i „do 12” nakładają się dla 12 miesięcy. W dłuższym wariancie AD5/AE5 porównują drugi rok (AC) z bazą C, więc przy 12 miesiącach i zerach w drugim roku nie można bez sprawdzenia uznać wzoru za właściwy.

Wpływ: Wybór wariantu i poprawność wzrostu dla 12 miesięcy. Dla pozostałych długości wybierz odpowiedni zakres.

Status: do-potwierdzenia-w-PARP. Źródła: SRC-5dddf09c0cf4, SRC-0ac9591da399, SRC-02c1d0102fd0.

## D-03 — Ryczałt pośredni

Regulamin § 3 ust. 11 i umowa § 9 mówią „do 15%”, a wzór formularza na s. 8 ma etykietę stawki „15%”.

Wpływ: Walidujemy pułap 15% podstawy, kwotę pozostawiamy edytowalną. Niższą stawkę potwierdź w aktywnym LSI/PARP.

Status: limit-ustalony-sposob-wprowadzenia-do-sprawdzenia. Źródła: SRC-894f1179eb3f, SRC-f76bcd1c04a4, SRC-e5f4835ab250.

## D-04 — Wzrost 150%

Formuły AD5=(AC12-C12)/C12 i AE5=(AC13-C13)/C13 oraz próg >=150% w arkuszu Weryfikacja wzrostu potwierdzają wzrost o 150%, czyli końcowo 2,5 razy baza, jeśli baza >0. Nie jest to samo końcowe 150% bazy.

Wpływ: Dla bazy 0 występuje dzielenie przez zero; potrzebne wyjaśnienie PARP. Definicje agregacji miesięcy i lat trzeba uzgodnić z modelem.

Status: wyjasnione-formulami. Źródła: SRC-0fb046c95a8b, SRC-0ac9591da399.

## D-05 — Różne momenty zakończenia

Instrukcja wniosku wymaga planu obejmującego złożenie wniosku końcowego. Umowa § 6 liczy trwałość od wypłaty końcowej albo zatwierdzenia rozliczenia.

Wpływ: Daty we wniosku nie wyznaczają automatycznie rzeczywistej daty rozpoczęcia trwałości.

Status: rozrozniono. Źródła: SRC-2499049d1cfe, SRC-f76bcd1c04a4.

## D-06 — Oznaczenia redakcyjne

Tytuł metadanych ogłoszenia zawiera IIa, treść i numer naboru wskazują IIb. Katalog RIS w nagłówku podaje załącznik 5, a aktualny regulamin wskazuje go jako załącznik 6. Instrukcja s. 2 ma „limit 1000” przy etykiecie wyboru IIa; typ TAK/NIE wynika jednoznacznie ze wzoru.

Wpływ: Źródła identyfikowane stabilnym ID i SHA-256; brak dodatkowych pól z omyłek.

Status: rozstrzygnieto-przez-tresc-i-numer. Źródła: SRC-3e0359eb3602, SRC-18a66fc53144, SRC-2499049d1cfe, SRC-e5f4835ab250.

## D-07 — Obrócone nagłówki HRF

Ekstrakcja PDF s. 8 pomija nagłówki tabel kosztów. Stronę obejrzano wizualnie; odwzorowano także kwotę VAT, udział dotacji i wydatek na dostępność.

Wpływ: Uzupełniono mapę pól; oryginał zachowany.

Status: sprawdzono-wizualnie. Źródła: SRC-e5f4835ab250.

## D-08 — Słowniki i liczenie znaków LSI

Pełne słowniki CST/PKD i sposób liczenia znaków nie są opublikowane we wzorze. Zachowano instrukcje wyboru oraz nieustalony sposób liczenia spacji.

Wpływ: Przy finalnym przenoszeniu dopasuj etykiety i sprawdź liczniki; panel nie jest importerem LSI.

Status: do-sprawdzenia-w-aktywnym-LSI. Źródła: SRC-e5f4835ab250, SRC-2499049d1cfe.

## D-09 — FAQ obejmuje starsze edycje

Dodatkowa baza FAQ zawiera odwołania do 003/25 i do terminów 11.12.2025–10.02.2026. Są to materiały pomocnicze; terminy i wymagania obecnego naboru ustalono z dokumentacji 002/26.

Nie przenosić dat i założeń starszej edycji do nowego formularza. Zobacz [notatkę z FAQ](../01-sources/faq.md).

## Dane do zebrania od wnioskodawcy

- KRS, NIP, REGON, status MŚP i powiązania, historia spółki.
- Numer IIa, płatność końcowa i dowody sprzedaży.
- Produkt, przewagi, klienci, istniejące partnerstwo, rynek i prognozy.
- Opłacony kapitał, inwestor (jeśli dotyczy), wkład i dokumenty.
- Zespół, dostępność, zadania, kamienie, oferty, wskaźniki i model finansowy.

Oceny firmy zapisuj we własnym repozytorium wniosku. Przed podpisaniem umowy przeprowadź pełny przegląd jej postanowień; obecna analiza umowy obejmuje zakres istotny dla planowania i formularza.
