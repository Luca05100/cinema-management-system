import json
from app.db import get_connection, run_select

print("BOOKING SERVICE")

user_id = run_select("SELECT id FROM users WHERE email=%s;", ("admin@cinema.ro",))[0][0]

showtime_info = run_select("SELECT id, hall_id FROM showtimes LIMIT 1;")[0]
showtime_id = showtime_info[0]
hall_id = showtime_info[1]

seats_data = run_select("SELECT id FROM seats WHERE hall_id = %s LIMIT 3;", (hall_id,))
seat_ids = [s[0] for s in seats_data]

seats_json = json.dumps(seat_ids)

print(f"Apelam procedura create_booking pentru showtime {showtime_id}...")

conn = get_connection()
cur = conn.cursor()

try:
    cur.execute("CALL create_booking(%s, %s, %s);", (user_id, showtime_id, seats_json))

    row = cur.fetchone()
    booking_id = row[0]

    while cur.nextset():
        if cur.description is not None:
            cur.fetchall()

    conn.commit()
    print("OK: Rezervare creata. booking_id =", booking_id)

except Exception as e:
    conn.rollback()
    print("EROARE la crearea rezervarii:", e)

finally:
    cur.close()
    conn.close()

print("\nVerificare in DB (tickets):")
rows = run_select("""
    SELECT t.booking_id, m.titlu, s.rand, s.numar, t.pret_final
    FROM tickets t
    JOIN bookings b ON t.booking_id = b.id
    JOIN showtimes sh ON b.showtime_id = sh.id
    JOIN movies m ON sh.movie_id = m.id
    JOIN seats s ON t.seat_id = s.id
    WHERE t.booking_id = %s
""", (booking_id,))

for r in rows:
    print(r)