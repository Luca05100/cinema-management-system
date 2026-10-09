# 🎬 Cinema Management System

Aplicație web pentru gestionarea unui cinematograf, construită cu **Python (Flask)** și **MariaDB**. Proiectul include schema bazei de date, scripturi pentru popularea cu date de test și o aplicație web pentru administrarea operațiunilor unui cinema.

## 📋 Cuprins

- [Funcționalități](#-funcționalități)
- [Tehnologii folosite](#-tehnologii-folosite)
- [Structura proiectului](#-structura-proiectului)
- [Cerințe preliminare](#-cerințe-preliminare)
- [Instalare și rulare](#-instalare-și-rulare)
- [Configurare](#-configurare)
- [Baza de date](#-baza-de-date)
- [Contribuții](#-contribuții)
- [Licență](#-licență)
- [Autor](#-autor)

## ✨ Funcționalități

> Ajustează lista în funcție de ce implementează efectiv aplicația ta.

- Gestionarea filmelor (adăugare, editare, ștergere)
- Gestionarea sălilor și a locurilor
- Programarea proiecțiilor
- Rezervarea și vânzarea biletelor
- Autentificare securizată a utilizatorilor (parole criptate cu `bcrypt`)
- Generarea de rapoarte și grafice statistice (`matplotlib`)
- Export de documente PDF, de exemplu bilete sau rapoarte (`reportlab`)
- Generarea de date de test realiste (`Faker`)

## 🛠 Tehnologii folosite

| Categorie | Tehnologie |
|-----------|------------|
| Limbaj | Python 3 |
| Framework web | Flask 3.1 |
| Bază de date | MariaDB 11 |
| Conectori DB | `mariadb`, `mysql-connector-python` |
| Securitate | `bcrypt`, `cryptography` |
| Rapoarte și grafice | `matplotlib`, `numpy` |
| Generare PDF | `reportlab`, `pillow` |
| Date de test | `Faker` |
| Configurare | `python-dotenv` |
| Containerizare | Docker, Docker Compose |

## 📁 Structura proiectului

```
cinema-management-system/
├── app/                  # Aplicația web Flask (rute, șabloane, logică)
├── scripts/              # Scripturi utilitare (ex. populare bază de date)
├── sql/                  # Schema bazei de date și interogări SQL
├── docker-compose.yml    # Serviciul MariaDB
├── main.py               # Punct de intrare
├── requirements.txt      # Dependențe Python
└── README.md
```

## ✅ Cerințe preliminare

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) și Docker Compose
- Git

## 🚀 Instalare și rulare

### 1. Clonează repository-ul

```bash
git clone https://github.com/Luca05100/cinema-management-system.git
cd cinema-management-system
```

### 2. Creează un mediu virtual și instalează dependențele

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configurează variabilele de mediu

Creează un fișier `.env` în rădăcina proiectului (vezi secțiunea [Configurare](#-configurare)).

### 4. Pornește baza de date

```bash
docker compose up -d
```

Aceasta pornește un container MariaDB cu baza de date `cinema_system`, accesibil pe portul **3307** al mașinii locale.

### 5. Inițializează schema și datele de test

Rulează scripturile din folderele `sql/` și `scripts/`, de exemplu:

```bash
# Importă schema
docker exec -i cinema_mariadb mariadb -uroot -p"$password" cinema_system < sql/<fisier_schema>.sql

# Populează cu date de test (dacă există un astfel de script)
python scripts/<script_populare>.py
```

> Înlocuiește `<fisier_schema>` și `<script_populare>` cu numele reale ale fișierelor din repository.

### 6. Pornește aplicația

```bash
python -m flask --app app run --debug
```

Aplicația va fi disponibilă la `http://127.0.0.1:5000`.

## ⚙️ Configurare

`docker-compose.yml` citește parola root a bazei de date din variabila de mediu `password`. Exemplu de fișier `.env`:

```env
password=parola_ta_securizata

# Parametri de conectare folosiți de aplicație (ajustează după codul tău)
DB_HOST=127.0.0.1
DB_PORT=3307
DB_USER=root
DB_NAME=cinema_system
```

⚠️ **Nu face commit fișierului `.env`.** Asigură-te că este inclus în `.gitignore`.

## 🗄 Baza de date

- **SGBD:** MariaDB 11
- **Nume bază de date:** `cinema_system`
- **Port expus local:** `3307`
- **Persistență:** datele sunt păstrate în volumul Docker `mariadb_data`

Comenzi utile:

```bash
# Oprește containerul
docker compose down

# Oprește containerul și șterge datele
docker compose down -v

# Conectare la baza de date
docker exec -it cinema_mariadb mariadb -uroot -p cinema_system
```

## 🤝 Contribuții

Contribuțiile sunt binevenite!

1. Fă un fork al proiectului
2. Creează o ramură nouă (`git checkout -b feature/functionalitate-noua`)
3. Fă commit modificărilor (`git commit -m "Adaugă funcționalitate nouă"`)
4. Trimite ramura (`git push origin feature/functionalitate-noua`)
5. Deschide un Pull Request

## 📄 Licență

Acest proiect nu are încă o licență definită. Poți adăuga una, de exemplu [MIT](https://choosealicense.com/licenses/mit/), printr-un fișier `LICENSE`.

## 👤 Autor

**Luca** — [@Luca05100](https://github.com/Luca05100)
