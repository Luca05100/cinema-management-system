import random
from faker import Faker
from app.db import run_execute, run_select

fake = Faker()

NUM_USERS = 800
NUM_MOVIES = 500
NUM_HALLS = 10
NUM_SHOWTIMES = 200
NUM_BOOKINGS = 1500

print("Cream user admin fix")
run_execute(
    "INSERT INTO users (nume, email, parola) VALUES (%s, %s, %s);",
    ("Admin", "admin@cinema.ro", "admin123")
)

print("Generam utilizatori random...")
simple_passwords = ["ananas", "parola123", "qwerty", "student123", "test123"]
for _ in range(NUM_USERS):
    nume = fake.name()
    email = fake.unique.email()
    password = random.choice(simple_passwords)
    run_execute("INSERT INTO users (nume, email, parola) VALUES (%s, %s, %s);", (nume, email, password))

print("Generam filme...")
genres = ["Actiune", "Comedie", "Drama", "SF", "Horror", "Animatie", "Documentar", "Thriller"]
ratings = ["AG", "AP-12", "N-15", "IM-18"]

for _ in range(NUM_MOVIES):
    titlu = f"{random.choice(['Misiunea', 'Secretul', 'Intoarcerea', 'Ultimul', 'Povestea', 'Orasul', 'Comunistul'])} {fake.word().capitalize()}"
    run_execute(
        "INSERT INTO movies (titlu, gen, raiting, durata) VALUES (%s, %s, %s, %s);",
        (titlu, random.choice(genres), random.choice(ratings), random.randint(85, 165))
    )

print("Initializam sali si locuri...")
for i in range(1, NUM_HALLS + 1):
    nume_sala = f"Sala {i}"
    run_execute("INSERT INTO halls (nume_sala, capacitate) VALUES (%s, %s);", (nume_sala, 100))
    hall_id = run_select("SELECT id FROM halls WHERE nume_sala = %s;", (nume_sala,))[0][0]

    for rand in range(1, 11):
        for numar in range(1, 11):
            run_execute("INSERT INTO seats (hall_id, rand, numar) VALUES (%s, %s, %s);", (hall_id, rand, numar))

print("Simulam programari (showtimes)...")
movies = run_select("SELECT id FROM movies;")
halls = run_select("SELECT id FROM halls;")

for _ in range(NUM_SHOWTIMES):
    movie_id = random.choice(movies)[0]
    hall_id = random.choice(halls)[0]
    data_ora = fake.date_time_between(start_date='now', end_date='+10d')
    pret_baza = random.choice([20.00, 25.00, 30.00, 45.50])
    run_execute("INSERT INTO showtimes (movie_id, hall_id, data_ora, pret_baza) VALUES (%s, %s, %s, %s);", (movie_id, hall_id, data_ora, pret_baza))

print("Simulam rezervari si bilete...")
all_users = run_select("SELECT id FROM users;")
all_showtimes = run_select("SELECT id, hall_id, pret_baza FROM showtimes;")

for i in range(NUM_BOOKINGS):
    user_id = random.choice(all_users)[0]
    showtime_id, hall_id, pret_baza = random.choice(all_showtimes)

    run_execute("INSERT INTO bookings (user_id, showtime_id) VALUES (%s, %s);", (user_id, showtime_id))
    res_id = run_select("SELECT MAX(id) FROM bookings;")
    booking_id = res_id[0][0]

    if booking_id:
        num_tickets = random.randint(1, 4)
        available_seats = run_select("SELECT id FROM seats WHERE hall_id = %s ORDER BY RAND() LIMIT %s;", (hall_id, num_tickets))
        for (seat_id,) in available_seats:
            run_execute("INSERT INTO tickets (booking_id, seat_id, pret_final) VALUES (%s, %s, %s);", (booking_id, seat_id, pret_baza))

print("Populam users_log (Istoric actiuni)...")
# Simulam activitate pentru utilizatori
for i in range(40):
    user_id = all_users[i][0]
    # Folosim numele EXACT din CREATE TABLE: users_log
    run_execute("INSERT INTO users_log (user_id, action) VALUES (%s, %s);", (user_id, "Utilizatorul s-a logat in aplicatie"))
    run_execute("INSERT INTO users_log (user_id, action) VALUES (%s, %s);", (user_id, "Utilizatorul a cautat un film disponibil"))

print("\nDate generate corect")