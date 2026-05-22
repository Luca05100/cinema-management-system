from app.db import run_execute, run_select

print("--- TEST TRIGGER BEFORE INSERT (tickets) ---")

try:
    booking_id = run_select("SELECT id FROM bookings LIMIT 1;")[0][0]
    seat_id = run_select("SELECT id FROM seats LIMIT 1;")[0][0]
except IndexError:
    print("EROARE: Asigura-te ca ai date in tabelele bookings si seats inainte de test!")
    exit()

print(f"1. Testare inserare valida (pret_final = 25.00)")
try:
    run_execute(
        sql="INSERT INTO tickets (booking_id, seat_id, pret_final) VALUES (%s, %s, %s);",
        params=(booking_id, seat_id, 25.00)
    )
    print("OK: Inserarea valida a reusit")
except Exception as e:
    print("EROARE (nu trebuia):", e)

print("\n2. Testare inserare invalida (pret_final = -10.00)")
try:
    run_execute(
        sql="INSERT INTO tickets (booking_id, seat_id, pret_final) VALUES (%s, %s, %s);",
        params=(booking_id, seat_id, -10.00)
    )
    print("EROARE: Inserarea invalida a trecut (trigger NU functioneaza)")
except Exception as e:
    print("OK: Inserarea invalida a fost respinsa de trigger")
    print("Mesaj DB:", e)


print("\n--- TEST TRIGGER AFTER UPDATE (movies) ---")

movie_id = run_select("SELECT id FROM movies LIMIT 1;")[0][0]

print("Facem update pe titlul filmului...")
run_execute(
    sql="UPDATE movies SET titlu = %s WHERE id = %s;",
    params=("TITLU TEST UPDATE", movie_id)
)

print("Verificam log-urile in users_log:")
logs = run_select("SELECT action FROM users_log ORDER BY id DESC LIMIT 2;")

for l in logs:
    print("-", l[0])

print("\n--- TEST TRIGGERE FINALIZAT ---")