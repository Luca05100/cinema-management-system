from app.db import run_execute
from scripts.create_tables import create_tables

print("Stergem tabelele (daca exista)...")

# STERGEM COPII INAINTE DE PARINTI (ORDINE IMPORTANTA)
run_execute("DROP TABLE IF EXISTS users_log;")
run_execute("DROP TABLE IF EXISTS user_log;")
run_execute("DROP TABLE IF EXISTS tickets;")
run_execute("DROP TABLE IF EXISTS bookings;")
run_execute("DROP TABLE IF EXISTS showtimes;")
run_execute("DROP TABLE IF EXISTS seats;")
run_execute("DROP TABLE IF EXISTS halls;")
run_execute("DROP TABLE IF EXISTS movies;")
run_execute("DROP TABLE IF EXISTS users;")

print("Creez tabelele din schema.sql...")
create_tables()

print("Rebuild gata!")