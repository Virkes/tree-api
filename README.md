# Uređivanje stabla

## 1. Pokretanje aplikacije

### Preduvjeti

### Preduvjeti

- Python 3.10 ili noviji
- Flask
- Flask-SQLAlchemy

### Pokretanje

1. Aktivacija virtualnog okruženja (opcionalno)
2. Pokretanje aplikacije:

   ```bash
   flask run
   ```
   ili
   ```bash
   python run.py
   ```

Aplikacija je dostupna na:

```
http://localhost:5000
```

---

## 2. Pristup API endpointima

Svi endpointi koriste **JSON** za slanje i primanje podataka.

Osnovni URL:

```
/nodes
```

---

## 3. Pregled dostupnih endpointa

### Dohvat čvorova

* **GET** `/nodes/`
* dohvaća sve čvorove u bazi
  * dohvaćanje pojedinačnih čvorova bi i dalje zahtijevalo informaciju o dostupnim id-jevima čvorova

---

### Unos čvora

* **POST** `/nodes/{parentId}`

Body:

```json
{
  "title": "Naziv"
}
```

---

### Promjena naziva čvora

* **PUT** `/nodes/{id}`

Body:

```json
{
  "title": "Novi naziv"
}
```

---

### Brisanje čvora

* **DELETE** `/nodes/{id}`

---

### Premještanje čvora (promjena parenta)

* **PUT** `/nodes/{id}/move`

Body:

```json
{
  "newParentId": 5
}
```

---

### Promjena redoslijeda čvorova

* **PUT** `/nodes/{id}/reorder`

Body:

```json
{
  "newOrder": 2
}
```

---

## 4. Testiranje

Endpointi se mogu testirati pomoću alata kao što su:

* Postman
* curl
* HTTP client unutar IDE-a

Primjer:

```bash
curl http://localhost:5000/nodes
```