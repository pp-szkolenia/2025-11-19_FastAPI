**1. Hello world**

Przepisz kod aplikacji, uruchom go oraz wykonaj request pod odpowiedni adres z wykorzystaniem przeglądarki.

---

**2. Ścieżki i routing**

Zdefiniuj użytkowników naszej aplikacji jako listę słowników. Stwórz endpoint `GET /users/`, który zwróci wszystkich użytkowników w postaci JSONa.

Każdy użytkownik powinien mieć następujące cechy:
- `username`
- `password`
- `is_admin`

---

**3. Metoda POST, request body, Pydantic**

Stwórz endpoint `POST /users/`, który umożliwi dodanie nowego użytkownika. Uwzględnij stworzenie modelu request body. Czy któreś pola powinny być opcjonalne lub domyślne? Przetestuj endpoint w Postmanie.

---

**4. Pobranie konkretnego zasobu (path parameter)**

Stwórz endpoint, który będzie zwracał jedno zadanie na podstawie jego id.

---

**5. HTTPException i błąd 404**

Zwróć błąd `404` przy próbie pobrania zadania, które nie istnieje.

---

**6. JSONResponse zamiast słownika, domyślny status_code**

Zmodyfikuj wszystkie endpointy typu `GET` tak, żeby zwracały obiekt typu `JSONResponse`. W endpoincie `POST /users/` ustaw kod odpowiedzi na `201` pozostawiając zwracanie słownika.

---

**7. Metoda DELETE, odpowiedź 204**

Stwórz endpoint `DELETE /users/{id_}`, który będzie usuwał użytkownika o podanym numerze id. Niech endpoint zwraca odpowiedź `204`.

---

**8. Metoda PUT**

Stwórz endpoint `PUT /tasks/{id_}`, który będzie modyfikował zadanie o podanym numerze id. Niech zwrócona będzie odpowiedź `200`.

---

**9. Struktura projektu - app.main:app, modele do osobnego pliku**

Podziel projekt na pliki i umieść całość w folderze `src/app/`.

---

**10. Struktura projektu - podział endpointów na osobne pliki**

Podziel endpointy na pliki, które będą znajdować się w folderze `routers/`.

---

**11. Automatyczna dokumentacja (/docs, /redoc)**

Wygeneruj dokumentację, ustaw tagi i opisy endpointów.

---

**12. Model odpowiedzi**

Zmodyfikuj kod endpointów, które odpowiadają tabeli `users`. Dodaj do nich według uznania modele odpowiedzi.

---

**13. Requestowanie API w Pythonie**

Napisz kod (skrypt/notebook), który będzie requestował poszczególne endpointy dotyczące tasków.

