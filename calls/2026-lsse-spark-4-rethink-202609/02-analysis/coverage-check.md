# Kontrola pokrycia — Spark 4.0 / rethink

## Źródła

- Oficjalna strona: zachowany snapshot HTML, tekst i informacje JSON.
- ZIP: 14/14 dokumentów; 8 PDF (80 stron), 3 XLSX, 2 DOCX, 1 DOC.
- Metadane __MACOSX/AppleDouble odnotowano i wyłączono. Każdy plik porównano bajtowo z ZIP; sumy SHA-256 są zgodne.
- F6S: 4 zrzuty przekazane przez użytkownika, przepisane do [SRC-f6s-zrzuty-20260926](../01-sources/text/SRC-f6s-zrzuty-20260926.md).
- Użytkownik potwierdził brak widocznych dodatkowych wymagań poza pytaniami 1–37.
- Oryginały Office zachowano bez zapisu przez czytnik; formuły i ukryte arkusze są w ekstraktach. DOC ma 9 zastępczych znaków po ekstrakcji — kontrola przy wypełnianiu umowy.

## Odwzorowanie

| Część F6S | Pytania | Plik zbiorczy | Liczba |
| --- | --- | --- | --- |
| Informacje ogólne | 1–13 | [Informacje](../03-application/01-information/form.md) | 13 |
| Kryteria dostępu | 14–16 | [Dostęp](../03-application/02-eligibility-criteria/form.md) | 3 |
| Kryteria merytoryczne | 17–27 | [Opisy](../03-application/03-substantive-criteria/form.md) | 11 |
| Inne | 28–37 | [Pomoc i oświadczenia](../03-application/04-other/form.md) | 10 |

Razem: **37 pytań, 37 specyfikacji, 37 lokalizacji odpowiedzi, 4 formularze**.
Zgodność numeracji Q-001–Q-037 z numeracją F6S. Dane spółki, opisy i oświadczenia puste.

- Q-002: brak gwiazdki — zachowano `wymagane: false`.
- Q-006: mikro/małe/średnie, wraz z ostrzeżeniem, że regulamin dopuszcza tylko mikro/małe.
- Q-008: na zrzucie zwinięta lista; lokalne pole tekstowe, bez wymyślonych etykiet słownika.
- Q-011: RUNDA 1; bez automatycznego zaznaczenia.
- Q-012: wielokrotny wybór, 8 nazw dokładnie z formularza.
- Q-016: zakresy 0-4, 5-6, 7-9; minimum kwalifikujące TRL 5 opisane we wskazówce.
- Q-015 i Q-017–Q-027: pełne bloki opisowe. Wskaźniki i zespół to opisy w jednym polu, zgodnie z F6S.
- Q-028: tekst, gdyż zrzut nie ustala jednostki wykorzystanej pomocy.
- Q-029–Q-037: zachowane zestawy TAK lub TAK/NIE, pełne oświadczenia w źródle i wskazówkach. Q-031 ma przeczącą treść — TAK potwierdza brak wcześniejszego finansowania.
- Brak powtarzalnych tabel/kart i budżetu w pokazanym zgłoszeniu. Nie dodano ich na podstawie samego IPA.
- Limity znaków nie pokazane — `null`, bez narzucania domyślnego limitu.

Gotowość dotyczy pracy nad zgłoszeniem, nie oceny firmy ani podpisania umowy.
Rozbieżności IPA/umowy pozostają w [osobnym rejestrze](discrepancies.md).
