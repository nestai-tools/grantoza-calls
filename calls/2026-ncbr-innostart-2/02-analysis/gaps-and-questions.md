# Braki i pytania do przygotowania wniosku

Nie wybrano firmy (`firma_id: null`); rejestr firm jest pusty. Braki poniżej blokują napisanie i ocenę wniosku, ale nie blokują odwzorowania opublikowanego formularza.

| ID | Potrzebne dane/dokument | Wpływ | Kto dostarcza | Powiązanie |
| --- | --- | --- | --- | --- |
| B-01 | Nazwa firmy, NIP/KRS/CEIDG, forma prawna, adresy, reprezentacja i kontakt | Profil firmy, legalna reprezentacja, kwalifikowalność | Wnioskodawca i rejestr | [Q-024](../03-application/02-applicant/specification/Q-024.md) |
| B-02 | Raport „Rekomendacje dla Przedsiębiorcy” i potwierdzenie zakończenia Innovation Coach | Warunek dostępu i podstawa celu B+R | Wnioskodawca | [Q-178](../03-application/11-attachments/specification/Q-178.md) |
| B-03 | Historia pomocy publicznej/UE na B+R oraz de minimis, zaświadczenia, struktura grupy | Warunki dostępu i limity | Firma/księgowość | [Q-181](../03-application/11-attachments/specification/Q-181.md) |
| B-04 | Zatrudnienie, obrót, aktywa za okresy referencyjne, udziały/głosy, powiązania, zmiany właścicielskie | Status MŚP, wybór załączników 1/2/3 | Firma/księgowość | [Q-184](../03-application/11-attachments/specification/Q-184.md) |
| B-05 | Opis rozwiązania, obecny stan, problem badawczy, niewiadoma, oczekiwane parametry i fragment rekomendacji IC | Ocena rzeczywistego B+R i innowacji | Osoba merytoryczna | [Q-090](../03-application/03-objective/specification/Q-090.md) |
| B-06 | Odbiorcy, obecne alternatywy, dowody potrzeb i korzyści, sposób wykorzystania rezultatu | Potencjał projektu | Firma/produkt/sprzedaż | [Q-108](../03-application/05-project-potential/specification/Q-108.md) |
| B-07 | Zadania, kategorie PRZ/PRO, miesiące, zależności, metody, kamienie i ryzyka | Realny harmonogram i schemat instancji | Kierownik merytoryczny | [Q-102](../03-application/04-tasks/specification/Q-102.md) |
| B-08 | Osoby, CV/dowody kompetencji, role, umowy, czas pracy, stawki, infrastruktura | Zespół, zdolność realizacji, budżet | Firma i zespół | [Q-146](../03-application/08-team/specification/Q-146.md) |
| B-09 | Decyzja o doradcy; jeżeli TAK — konkretna osoba, kompetencje, koszt i dwustronna umowa | Dodatkowy punkt i załącznik warunkowy | Wnioskodawca | [Q-132](../03-application/07-applicant-potential/specification/Q-132.md) |
| B-10 | Pozycje budżetu, kwoty netto/VAT/brutto, źródła wyceny i daty, źródło wkładu, aktualne dowody środków | HRF, limit grantu, wkład i płynność | Firma/księgowość | [Q-183](../03-application/11-attachments/specification/Q-183.md) |
| B-11 | Dostępność produktu i organizacji prac, skutki dla praw podstawowych, dane osobowe/IP | Uzasadnienia horyzontalne i oświadczenia | Firma i projektanci | [Q-076](../03-application/02-1-eligibility/specification/Q-076.md) |
| B-12 | Redaktor OSF, reprezentacja podpisująca, finalne PDF załączników | Złożenie przed 30.09.2026 16:00 | Wnioskodawca | [Q-177](../03-application/11-attachments/specification/Q-177.md) |

## Dane uzupełniające ze źródeł organizatora

- Wersja i właściwy fragment KIS z dnia 13.08.2026: pobrać przy wyborze specjalizacji projektu; nie wybrano KIS bez zakresu projektu.
- Regulamin KOP wymieniany w instrukcji s. 3 nie występuje jako osobny plik w 14 materiałach sekcji Dokumenty. Podstawowe zasady oceny są w regulaminie i kryteriach; dodatkowy dokument proceduralny warto pozyskać przed złożeniem.
- Słowniki OSF, liczniki znaków i opcjonalność techniczna pól: do sprawdzenia w aktywnym wniosku, do którego nie mamy dostępu.
- Przy właściwym scenariuszu finansowym rozstrzygnąć [ROZ-003/004/007/009](discrepancies.md).

## Kolejność pracy

Najpierw firma, rekomendacja IC i opis B+R; potem zadania, zespół, budżet i płynność; następnie opisy punktowane, wskaźniki, zgodność i załączniki. Profil firmy zapisać przez skill `grants-company` do tablicy `companies/companies.json`, a jego identyfikator przypisać do konkretnego wniosku. Nie tworzyć fikcyjnego profilu.
