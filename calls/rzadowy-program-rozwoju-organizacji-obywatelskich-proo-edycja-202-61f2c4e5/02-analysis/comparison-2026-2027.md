# Porównanie formularza PROO 1a: 2026 → 2027

**Wniosek: układ formularza i zasadnicza logika opisu są zgodne, lecz formularz 2026 nie jest równoważnym wzorem edycji 2027.** Pusty wzór przygotowano z dziesięciu zrzutów HTML oznaczonych „Konkurs PROO-1a Edycja 2027”, przy zastosowaniu regulaminu i ogłoszenia 2027. Dokumenty 2026 pozostają pomocą porównawczą.

Porównanie wykonano 16.11.2026, po rozpoczęciu naboru o 12:00 Europe/Warsaw. Pierwszy zapis analizy: 2026-11-16T11:42:31+00:00 (12:42:31 w Polsce). Oryginałów i zapisanych w nich danych nie zmieniono. Nie logowano się na konto wnioskodawcy. Nie złożono żadnej oferty.

## Hierarchia i zakres źródeł

- Regulamin 2027: **SRC-6bae8ed23334**; ogłoszenie 2027: **SRC-4fad2e1e643c**. Ponowne pobranie 16.11.2026 dało identyczne SHA-256 jak oryginały z 12.11.
- Zrzuty HTML użytkownika: źródło struktury, etykiet, limitów, opcji, pól warunkowych, obliczeń i powtarzalności. Nagłówek potwierdza edycję 2027; zapisany numer oferty i dane profilu nie są danymi nowego wniosku.
- **SRC-737741b7a2b4**, DOCX 2026: pełne porównanie układu i tabel, w tym zachowany ekstrakt tabel JSON.
- **SRC-f5b0a3b5525a**, podręcznik 2026: odczyt wskazówek pól s. 15–26 PDF. **SRC-f565f4ac9f04**, wytyczne ekspertów 2026: odczyt części PROO 1a s. 11–24 PDF. Pełne ekstrakty zachowane; pozostałych treści nie uznano za przeczytane ani za aktualne wymagania.

## Różnice i sposób odwzorowania

| Obszar | Dokumenty 2026 | Zrzut / regulamin 2027 | Rozstrzygnięcie we wzorze |
| --- | --- | --- | --- |
| Edycja i nagłówek | PROO 2026; oferta składana w 2025 | Nagłówek i nawigacja: PROO 2027, ale w treści nadal „SKŁADANA W 2025 ROKU” | Nabór 2027, składanie w 2026. Tekst 2025 zachowano w źródle jako pozostałość, bez przenoszenia do metryki. SRC-dffbaa0478d8. |
| Układ I–VII | Dane, opis 1–6, charakterystyka, budżet, inne, oświadczenia | Ten sam zasadniczy układ; III i V rozdzielone na zakładki | 10 logicznych rozdziałów zgodnych ze zrzutami; nie zastosowano uniwersalnego formularza. |
| Rejestracja — ścieżka 1 | Podręcznik 2026 dopuszcza szerszy dostęp | Reg. 2027 s. 13: przed 2024-11-01 | Nowy próg daty; stałe kalendarzowe z regulaminu, nie ogólne odejmowanie 2 lat od dnia wysyłki. |
| Rejestracja i przychód — ścieżki 2/3 | Wcześniejsze daty edycji | Reg. 2027: przed 2023-11-01, przychód odpowiednio ≥150 000 / ≥500 000 zł | Progi włączne. JS `wyznaczSciezke()` w SRC-dffbaa0478d8 używa błędnie `>150000` i `>500000`. Przypadki równe progom wymagają kontroli w SOD/NIW. |
| Strona finansowa — ścieżka 3 | DOCX dopuszcza stronę **lub profil społecznościowy**, bez wymogu dwóch lat w pytaniu | HTML wymaga **własnej działającej strony** i sprawozdań z min. 2 ostatnich zamkniętych lat; reg. s. 13, przypis 3 | Tak/Nie i warunkowy bezpośredni link. Profil społecznościowy nie wystarcza; publikacja do dnia złożenia. |
| Historia UL/MDS/Poradnicze | W DOCX 2026 osobny checkbox i wykluczenie dla wsparcia 2020–2025 | HTML 2027 nie ma tego checkboxa; reg. s. 14 go nie powtarza, s. 33 odnosi tę historię 2020–2026 do premii strategicznej | Nie utworzono fikcyjnego pola ani automatycznego wykluczenia z 2026. Historię bada się we właściwym kryterium 2027. |
| Najwyższy przychód | Kwota z jednego z 3 lat | To samo; zaktualizowana instrukcja przy braku zamkniętego roku | Jedno pole kwoty, nie suma 3 lat. Bez kopiowania przychodu konkretnego oferenta. |
| Tytuł zadania | DOCX 2026: max 25 znaków | HTML 2027 nie ma `maxlength` ani licznika tytułu | Pole odwzorowane; limit 2027 nieustalony. Nie narzucono 25 jako potwierdzonej reguły. |
| Syntetyczny opis | 1000 znaków | 1000 znaków | Limit zachowany. SRC-2529b243ca13. |
| Potrzeby, grupa docelowa, komplementarność | Po 10 000 | Po 10 000 | Limity zachowane, wskazówki redakcyjne 2026 stosowane pomocniczo. |
| Miejsce realizacji | DOCX: 1000 | HTML: **10 000** | Obowiązuje uchwycony limit 2027: 10 000. |
| Działanie | DOCX: nazwa, opis, termin, podzlecenie | HTML: nazwa **200**, opis **21 000**, podzlecenie **10 000**; daty | Pełna karta Z na działanie; wspólne ID dla kosztów i rezultatów. SRC-47ebcc3b726a. |
| Strategia | DOCX wskazuje przygotowanie/aktualizację 5-letniej strategii; ekspert 2026: min. 5 lat w ścieżkach 2/3 | Reg. 2027 s. 16 i przypis 5: wieloletnia strategia w 2/3, uchwała zarządu do końca zadania, horyzont min. 1 rok po końcu | Wskazówka w karcie działania i REQ-013. Nie narzucono dawnego minimum 5 lat. |
| Audyt | Wzór 2026 nie ma obowiązkowego działania audytu | Reg. 2027 s. 16 i zał. 11: obowiązkowy w ścieżce 3 | Uwzględniono w wymaganiach, wskazówkach działań i kosztów; nie dopisano fikcyjnego wykonawcy ani kosztu. |
| Dostępność | 5000 | 5000 | Limit i opis dostępności zgodny z 2027. |
| Promocja | DOCX: **20 000** | HTML: **10 000** | Limit 2027 10 000, aktualna instrukcja oznaczeń z reg. s. 50–51. |
| Efekty i trwałość | Po 10 000 | Po 10 000 | Oddzielne bloki opisowe. SRC-3e13fd9447dd. |
| Wiersz rezultatu | Nazwa, typ, działanie, baza, lata pośrednie 2026/2027, cel, pomiar | Te same pola, lata **2027/2028**, wartość docelowa na końcu; pomiar 10 000 | Karta W odwzorowuje jeden dodawany wiersz SOD; dla ścieżki 1 końcowa = 2027, dla 2/3 końcowa = 2029. Nazwa rezultatu bez ujawnionego limitu. |
| Potencjał i zarządzanie | 3 opisy po 10 000 | 3 opisy po 10 000 | Te same pola. Ryzyka należą do zarządzania; nie tworzono dodatkowego pola tekstowego. SRC-524d7ff885fd. |
| Koszty | DOCX ma I działania i II administracyjne, także podział pomiędzy oferentów | HTML 2027 zawiera tylko **I Koszty realizacji działań**, wiersze powiązane z działaniami i Oferenta 1 | Nie dodano kategorii II ani drugiego oferenta. Koszty obsługi należy opisać i przypisać do właściwego działania. SRC-c1e80b013b98. |
| Lata kosztorysu | 2026 + „Analogiczne tabele dla kolejnych lat” | Zrzut zakładki V.A/V.B tylko 2027; reg. s. 18 wskazuje okresy 2027–2029 | Powtórzono tę samą rozpoznaną tabelę na 2028 i 2029 dla ścieżek 2/3. Jest to jawne rozwinięcie okresów na podstawie regulaminu i DOCX, nie deklaracja posiadania osobnych zrzutów 2028/29. |
| Finansowanie | Kwoty i udziały dotacji, bieżące/inwestycyjne, wkład finansowy/rzeczowy/osobowy, opłaty odbiorców | Ta sama logika w zrzucie; wyliczenia i 6 wejściowych kwot rocznie | Jedna karta F na używany rok, maks. 1/rok, sześć kwot do edycji; sumy i procenty obliczane. Brak karty 2028/29 w ścieżce 1 wnosi zero do sumy, pusty istniejący koszt pozostaje brakiem danych. |
| Kosztorys — flagi | Inwestycja, współfinansowanie, podzlecenie | Te same checkboxy | Lokalne Tak/Nie odpowiada zaznaczeniu/odznaczeniu; brak zaznaczenia w dostarczonym HTML nie jest odpowiedzią nowego wnioskodawcy. |
| Inne informacje | 10 000 | 10 000 | Jedno miejsce uzasadnienia kosztów i kwestii oświadczeń. SRC-43ad5a7579cd. |
| Oświadczenia | 11 oświadczeń | Dotychczasowe 11 + **12 użycie AI**, warunkowy opis 10 000 + **13 odpłatne wsparcie zewnętrznego podmiotu** | Wszystkie wybory puste, dokładne opcje Tak/Nie/Nie dotyczy i zalega/nie zalega. SRC-130ce8988262. |
| Załączniki | Ogólny wzór i dane reprezentacji | Brak sekcji uploadu we wszystkich zrzutach 1a; dokumenty przed umową w reg. s. 46 | Lista warunkowych dokumentów umownych, bez wymyślenia pola uploadu lub wymagań PROO 1b. |
| Punktacja | 25/25/20/20/10 | Reg. 2027 zachowuje tę punktację | Oficjalna mapa oparta na 2027. Wskazówki ekspertów 2026 pomocnicze, bez nowych wag. |

## Błędy i ograniczenia dokumentów 2027

1. Strona i tabela ogłoszenia s. 10 mówią o wynikach w marcu **2026**, lecz punkt 8 ogłoszenia s. 11 jednoznacznie wskazuje **31 marca 2027**; reg. s. 18 ogólniej I półrocze 2027. Metryka podaje szczegółową datę z punktu 8, zachowując rozbieżność.
2. Budżet całego Programu w ogłoszeniu s. 4 nie jest alokacją tego naboru. Dla PROO 1a reg. s. 12 podaje **11,7 mln w 2027 + 10 mln w 2028 + 10 mln w 2029 = 31,7 mln zł**. Ogólne kwoty Programu dotyczą innego zakresu; nie zastępują alokacji 1a.
3. W karcie merytorycznej s. 66 pozostał napis **90 pkt**, obok **100 pkt**. Główna tabela i suma pięciu kryteriów wskazują 100/eksperta i 200/2 ekspertów; tak odwzorowano skalę.
4. **Premia strategiczna jest nierozstrzygnięta w zakresie historii wsparcia**: główna tabela s. 32–33 uwzględnia PROO 2a/3/4, a zał. 6 s. 68 mówi o tym samym Priorytecie. S-01 ma status `sprzeczne`; bez potwierdzenia NIW nie przyznawać premii, gdy różnica ma znaczenie dla organizacji.
5. Zrzuty dokumentują konkretny stan interfejsu. Nie potwierdzają wszystkich walidacji serwerowych, niewidocznych limitów czy przyszłych zmian SOD. Brak tytułowego `maxlength` nie oznacza braku jakiegokolwiek ograniczenia po stronie serwera.

**Gotowość** dotyczy pustego warsztatu do wypełniania: rozpoznane pola i wymagania są odwzorowane. Ocena kwalifikowalności, weryfikacja dokumentów, decyzje o oświadczeniach i skuteczne złożenie należą do konkretnego wniosku.
