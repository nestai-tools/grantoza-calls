# Braki, rozbieżności i założenia

Brak nierozpoznanego pola lub sprzeczności uniemożliwiającej wskazanie miejsca odpowiedzi. Poniższe ograniczenia pozostają jawne. Nie wymagają decyzji użytkownika o kształcie wspólnego wzoru i nie stanowią potwierdzenia zgodności z LSI. Wynik kontroli technicznej aplikacji i zakres poprawki zapisano osobno poniżej.

| ID | Brak lub rozbieżność i podstawa | Wpływ / sposób postępowania | Źródło rozstrzygnięcia | Powiązania | Blokuje strukturę |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Numery 003/26, 04/26 i 004/26 w ogłoszeniu s. 1, RNU s. 1, słowniku s. 3 i liście do umowy s. 1; dodatkowo litera O / cyfra 0 | Nie wybrano arbitralnie numeru. Robocze powiązanie przez tytuł, IT/ICT i terminy; brak pola ręcznego numeru naboru we wzorze. | Oficjalne sprostowanie lub jednoznaczna identyfikacja PARP | REQ-008–REQ-010, wszystkie źródła edycji | Nie |
| GAP-002 | Ogłoszenie s. 1–2: pełne lata obrotowe; RNU s. 6–7 i kryteria s. 3–4: 1–5 lat od rejestracji. Q-007 w CEIDG wymaga daty rozpoczęcia wykonywania działalności. | Zachowano datę i deklarację TAK jako dwa pola. Nie oblicza się automatycznie wieku z Q-007; wymaga rzeczywistej daty rejestracji, złożenia i historii podmiotu. K-02 ma status sprzeczne i tryb zewnętrzny. | Dokumenty rejestrowe i wyjaśnienie PARP | REQ-003, Q-007, Q-041, K-02 | Nie |
| GAP-003 | Strona „Kto może otrzymać wsparcie?” wymienia zamieszkanie osoby fizycznej w Polsce; kryteria s. 3 i instrukcja s. 3–4 wymagają adresu wykonywania działalności CEIDG. | Odtworzono adres działalności zgodnie z właściwym polem, bez dodawania adresu zamieszkania. K-01 dotyczy oficjalnej treści kryterium; dodatkowy zapis strony wymaga zewnętrznego wyjaśnienia. | PARP i właściwy wpis rejestrowy | REQ-002, Q-016–Q-020, K-01 | Nie |
| GAP-004 | Brak pełnych słowników formy prawnej, własności i PKD. Instrukcja s. 2 wskazuje dwie wartości własności, lecz nie przedstawia całego słownika. | Pola pozostają wyborami pojedynczymi z opcje: []. Panel umożliwia ręczne wpisanie wartości, następnie dopasowanie do LSI. Znane nazwy własności zachowano w instrukcji pola, bez uznania ich za pełną listę. | Słowniki właściwego naboru w LSI | REQ-013, Q-008–Q-009, Q-014 | Nie |
| GAP-005 | Wzór s. 3 nazywa grupę konkursów „Program Akceleracyjny”; instrukcja s. 5–6 rozróżnia konkursy i akcelerację. | Zastosowano dwie grupy, zgodnie z nazwami i polami instrukcji. Nie ogranicza się liczby kart do limitu punktów 2 i 3. Warunek TAK wymaga co najmniej jednej właściwej karty; min techniczne 0 pozwala zachować pusty wzór i odpowiedź NIE. | Rozstrzygnięto z całej paczki | REQ-014–REQ-015, Q-042–Q-053 | Nie |
| GAP-006 | Kryteria s. 8 dopuszczają PPTX/PDF; instrukcja s. 9 wymaga PPT/PPTX. Nie podano limitów liczby i wielkości plików ani pełnej listy rozszerzeń GW. | PPTX przyjęto jako roboczy format wspólny. Nie narzucono wymyślonych limitów ani nie uznano PDF/PPT za jednoznacznie dopuszczalne. | LSI i wyjaśnienie PARP | REQ-018, REQ-024, Q-071–Q-075, K-09 | Nie |
| GAP-007 | Instrukcja s. 8 nazywa wszystkie załączniki obowiązkowymi, kryteria s. 5–6 dopuszczają brak akceleracji i nagród z wynikiem 0. RNU s. 9 wymienia osobno opis zakresu działalności PL/EN jako załącznik. | Dowody akceleracji i wyróżnień powiązano roboczo z TAK. Plan 06-attachments/README.md obejmuje wymagane przez RNU dwa odrębne opisy działalności PL i EN. Istniejące Q-075 jest ich miejscem roboczym. Wzór nadal ma pięć oficjalnych pozycji; nie dodano zastępczych pól. Opisy działalności nie są opisami rozwiązania Q-056/Q-057. Dokładna kategoria wysyłki pozostaje do sprawdzenia w LSI; nie ogłoszono roboczego przypisania jako oficjalnej reguły PARP. | Walidacja właściwego LSI i wyjaśnienie PARP | REQ-011, REQ-024, Q-056–Q-057, Q-073–Q-075 | Nie |
| GAP-008 | Wzór i instrukcja różnią się brzmieniem części oświadczeń, m.in. odpowiedzialnością karną i zakresem odesłania do art. 207. Nie pokazują oddzielnych checkboxów dla dziesięciu oświadczeń. | Zachowano tekst wzoru jako stałą dokumentację, z odsyłaczami do różnic instrukcji. Bez automatycznej zgody, podpisu i potwierdzania faktów. Akceptacja klauzuli w LSI jest czynnością zewnętrzną; nie wymyślono jej opcji. | Obowiązujący tekst i sposób prezentacji w LSI | REQ-025, Q-076–Q-086 | Nie |
| GAP-009 | Nieodczytane SRC-fa8cf9a07c30 XLS i SRC-4f096abf571f archiwum; ich SHA-256 są zapisane w documents.json i zgodne z lokalnymi oryginałami. W SRC-dfea5acf63da układ tabel MŚP spłaszczony. | Brak dokumentacji treści arkuszy, formuł i pełnego układu komórek do umowy. Nie odtwarzano tych dodatkowych formularzy. Zachować oryginały; odczyt z tabelami jest wymagany przed ich wypełnianiem. | Oryginały XLS, DOCX i archiwum | REQ-032–REQ-033 | Nie |
| GAP-010 | Lista do umowy s. 2: bieżący i dwa poprzednie lata podatkowe; RNU s. 7, 18 i oświadczenie SRC-881e952821ba: minione trzy lata. | Nie utożsamiono okresów ani nie dodano automatycznej sumy pomocy. Wymaga rozstrzygnięcia przed weryfikacją pomocy i umową. | Aktualne przepisy, formularz i wyjaśnienie PARP | REQ-020, REQ-033 | Nie |
| GAP-011 | RNU s. 18: dokumenty przez e-Doręczenia/LSI; lista do umowy s. 1: e-mail/ePUAP i podpis ze znacznikiem czasu. Sankcyjne DOCX zawiera warunki handlu/inwestycji Rosja/Białoruś pominięte w RNU s. 17. | Zachowano obie lokalizacje; nie wybrano kanału ani nie oceniono spełnienia wykluczeń. To warunki zawarcia umowy, bez nowych pól formularza zgłoszeniowego. | Wezwanie PARP, właściwe przepisy i dokumenty | REQ-030, REQ-034 | Nie |
| GAP-012 | Umowa s. 11–12 określa licencję jednocześnie jako bezterminową i na 10 lat; nie dostarczono treści wskazanego harmonogramu umownego. S. 20 w ekstrakcie ma tylko stopkę. | Brak pełnej dokumentacji do interpretacji tych części umowy. Nie ustalano obowiązującej długości licencji, dat szkolenia ani dokładnych dni misji. | Ostateczna umowa i załączniki PARP; odczyt oryginału s. 20 | REQ-035–REQ-038 | Nie |
| GAP-013 | Brak pełnych tekstów pośrednio przywołanych przepisów i aktualnych komunikatów strony. Brak jawnej strefy godzin naboru. | Mapa zachowuje odesłania; nie przedstawia ich jako przeprowadzonej kontroli prawnej ani bieżącej weryfikacji naboru. | Oficjalne akty i komunikaty PARP | REQ-001–REQ-010, REQ-020, REQ-034 | Nie |

## Założenia techniczne

1. Daty edytowalne zapisuje się w panelu jako ISO YYYY-MM-DD. Dokumenty żądają zapisu RRRR/MM/DD, a wzór przy datach akceleracji pokazuje dd/mm/rrrr. Są to prezentacje tej samej daty; przy przenoszeniu należy zastosować format przyjmowany przez LSI. Nie potwierdzono automatycznej konwersji eksportu.
2. Wartości TAK/NIE przyjęto za instrukcją opisującą listy LSI, mimo zapisu Tak/Nie we wzorze. Wielkości przedsiębiorstwa i pozostałe podane słowniki zachowują brzmienie wzoru lub instrukcji, bez tworzenia własnych kodów.
3. Limit null oznacza brak określonego limitu w przekazanej dokumentacji, a nie potwierdzenie braku ograniczenia w portalu. Nie ustalono sposobu liczenia znaków przez LSI; zachowano wartości liczbowe z instrukcji.
4. Jedna karta akceleracji zawiera nazwę, organizatora i dwie daty; jedna karta konkursu sześć pól. Brak maksymalnej liczby kart w źródłach nie oznacza potwierdzonego braku limitu technicznego w LSI. Przy TAK wymagana jest właściwa karta i dowód; te zależności opisano semantycznie, bez deklaracji pełnej automatycznej kontroli.
5. Stały tekst oświadczenia jest dokumentacją, nie odpowiedzią wnioskodawcy. Numer, data złożenia, program, priorytet i działanie są uzupełniane przez LSI według instrukcji s. 1. Nie utworzono innych pól systemowych ani obliczeń.
6. Wybrano PPTX jako część wspólną sprzecznych zaleceń oraz warunkowość dowodów doświadczenia jako robocze rozwiązanie umożliwiające pisanie. Ich skutki i podstawy opisano w GAP-006 i GAP-007.
7. Po błędzie identyfikatora bloku zastosowano zapis identyfikatorów bloków małymi literami z łącznikami zamiast podkreśleń. Jest to korekta techniczna układu generatora; nie zmienia ID pól, kluczy danych, grup, źródeł, limitów ani kryteriów. Zgodność poprawki wymaga ponownego wyniku walidatora aplikacji.

## Kontrola aplikacji i poprawka

Przekazana kontrola techniczna aplikacji z `2026-11-13T13:30:08.835755+00:00` zakończyła się statusem `blad` i komunikatem „Niepoprawne ID bloku”. Wynik nie potwierdza poprawnego wygenerowania formularzy, przejścia pozostałych walidatorów, prób grup ani eksportu. Nie otrzymano szczegółowego wskazania odrzuconego identyfikatora.

W odpowiedzi na ten błąd poprawiono osiem identyfikatorów bloków zawierających podkreślenia:

| Poprzedni identyfikator | Poprawiony identyfikator |
| --- | --- |
| registered_address | registered-address |
| history_declarations | history-declarations |
| accelerator_details | accelerator-details |
| competition_details | competition-details |
| solution_identity | solution-identity |
| solution_descriptions | solution-descriptions |
| business_model | business-model |
| privacy_information | privacy-information |

Zachowano wszystkie 86 definicji pól, oba szablony grup i ich powiązania. W trzeciej opcji Q-062 poprawiono również błąd przepisywania „podmioty konkurencyjnych” na źródłowe „podmioty konkurencyjne” z instrukcji s. 7. Nie zmieniono znaczenia ani liczby opcji.

Ponowne uruchomienie generatora i walidatorów, próby obu grup, zapis i odczyt wyborów oraz kontrola pustych odpowiedzi, linków i eksportu należą do aplikacji. Wyniku po poprawce jeszcze nie przekazano; gotowość techniczna pozostaje niepotwierdzona. Błąd techniczny nie jest brakiem wzoru ani źródłową sprzecznością uniemożliwiającą ustalenie miejsc odpowiedzi, dlatego nie dodano go do blokerów dokumentacyjnych.

Nie wykonywano samodzielnie narzędzi, oględzin, OCR ani kontroli portalu. Obserwacje źródeł i ich SHA-256 pozostają aktualne dla niezmienionej paczki. Budżet i wskaźniki nie występują w tym formularzu; nie przygotowano fikcyjnych sum.
