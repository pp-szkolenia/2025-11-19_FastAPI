**1. Implementacja operacji bazodanowych w psycopg**

Zaimplementuj mechanizmy CRUD dla tabeli `users` z wykorzystaniem psycopg.

---

**2. Implementacja operacji bazodanowych w SQLalchemy**

Zaimplementuj mechanizmy CRUD dla tabeli `tasks` z wykorzystaniem SQLAlchemy.

---

**3. Query parameters (sortowanie, filtrowanie)**

Dodaj query parameters do endpointów odpowiadającym tabeli `users` tak aby można było:
- wyciągnąć samych adminów albo samych zwykłych użytkowników (albo wszystkich)
- posortować wyciągniętych użytkowników alfabetycznie po ich nazwie
- wyciągnąć tych użytkowników, którzy mają hasło równe lub krótsze/dłuższe niż *x* znaków (w tym celu użyj zaimportuj `func` z `sqlalchemy` i użyj funkcji `func.char_length`)

