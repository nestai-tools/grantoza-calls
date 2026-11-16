# Braki, pytania i rozbieżności — stan 16.11.2026

Brak wcześniejszego wzoru rozwiązano dzięki 10 zrzutom HTML edycji 2027. Nie ma blokera struktury formularza. Poniższe kwestie pozostają jawne; nie są potwierdzeniem kwalifikowalności żadnej organizacji.

| ID | Kwestia | Wpływ | Pola / wymagania | Podstawa i rozstrzygnięcie | Blokuje wzór? |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Brak publicznego osobnego DOCX 2027 na sprawdzonej stronie NIW | Sam w sobie nie blokuje, gdy istnieje kompletny zrzut konkretnego formularza | Wszystkie rozdziały | Dostarczono 10 HTML z nagłówkiem PROO 1a 2027; porównanie z DOCX 2026 i regulaminem | Nie; rozwiązane |
| GAP-002 | Nagłówek HTML „składana w 2025” | Błąd tekstu metryki | Edycja i terminy | Konkurs w nagłówku 2027, ogłoszenie 2027 i nabór 16.11–16.12.2026 | Nie; zachowano ślad |
| GAP-003 | Termin wyników „marzec 2026” na stronie i w tabeli ogłoszenia | Sprzeczny rok | Metryka | Punkt 8 ogłoszenia s. 11: 31.03.2027; reg. s. 18: I półrocze 2027. Podano szczegółową datę z punktu 8 | Nie; rozstrzygnięto podstawę |
| GAP-004 | Brak jawnego limitu tytułu 2027 | Limit serwerowy nieznany | Q-038 | HTML brak maxlength; DOCX 2026: 25. Nie narzucono niepotwierdzonego limitu. Sprawdzić w aktywnym SOD przy przenoszeniu | Nie; pole rozpoznane |
| GAP-005 | Kod zrzutu używa >150000 i >500000, regulamin ≥ | Wartość równa progowi może dać niewłaściwy dostęp do ścieżki w SOD | Q-002, Q-009; REQ-003/004 | SRC-dffbaa0478d8, wyznaczSciezke; reg. s. 13. Wymagania zgodnie z regulaminem; problem równości sprawdzić z NIW | Nie; wyjątek wymagający sprawdzenia |
| GAP-006 | Brak osobnych HTML budżetu 2028 i 2029 | Nie potwierdzono wyglądu tych zakładek | VII roczne koszty i finansowanie; REQ-010/011 | Rozwinięto rozpoznaną strukturę 2027 na okresy z reg. s. 18; DOCX 2026 potwierdza analogiczne tabele kolejnych lat. Przy przenoszeniu sprawdzić zakładki | Nie; jawna podstawa rozwinięcia |
| GAP-007 | Różnica historii premii strategicznej między główną tabelą a zał. 6 | Może zmienić prawo do 5 pkt | S-01; REQ-027 | Reg. s. 32–33 vs s. 68. S-01 = sprzeczne; wyjaśnić z NIW, gdy historia organizacji powoduje różnicę | Nie; blokuje potwierdzenie premii |
| GAP-008 | „90 pkt” obok „100 pkt” w zał. 5 | Usterka sumy | M-01–05 | Reg. s. 31–32 i suma 25+25+20+20+10 =100; dwóch ekspertów max200 na s. 39 | Nie; zastosowano skalę głównej tabeli |
| GAP-009 | Słowniki powiatów/gmin w HTML obejmują tylko wybraną lokalizację | Nie wolno ograniczyć całego naboru do tego fragmentu | Q-027–028 | Zachowano wybór z pustą listą do dopasowania w SOD; województwa i sfery mają odczytane słowniki | Nie; rozpoznane pola |
| GAP-010 | Brak danych konkretnego wnioskodawcy | Nie można ustalić ścieżki, historii dotacji, budżetu i prawdziwości oświadczeń | Wszystkie odpowiedzi; REQ-001–035 | Dane zbiera się w osobnym applications/<id>/ | Nie; oczekiwane dla pustego wzoru |
| GAP-011 | Zasady odwołania wymieniają pocztę, e-mail i punkt, a następnie wpływ w SOD | Procedura korzystania z odwołania wymaga doprecyzowania | REQ-034 | Reg. s. 30; przy korzystaniu ustalić kanał z NIW i nie uchybić 7 dniom | Nie; dotyczy przyszłej procedury |
| GAP-012 | Kategorie II administracyjne i podział na wielu oferentów obecne w DOCX 2026, nieobecne w HTML 2027 | Nie są dodawane jako pola obowiązującego formularza | V.A | Podstawa struktury: HTML 2027; koszty obsługi przypisane do działania. Nie ustalono osobnego ograniczenia procentowego administracji | Nie; zgodnie ze zrzutem |

Porównanie szczegółowe: [2026 → 2027](comparison-2026-2027.md). Brak potwierdzonej reguły nie jest zgodą na jej wymyślenie.
