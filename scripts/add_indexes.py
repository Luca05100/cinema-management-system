import time
from app.db import run_execute


def apply_indexes():
    print("=== APLICARE INDEX PENTRU OPTIMIZARE (CINEMA) ===")

    index_queries = [
        "CREATE INDEX idx_opt_users_email ON users(email);",

        "CREATE INDEX idx_opt_movies_titlu ON movies(titlu);",

        "CREATE INDEX idx_opt_bookings_user ON bookings(user_id);"
    ]

    for query in index_queries:
        print(f"Rulam: {query}")
        try:
            start_time = time.time()
            run_execute(query)
            end_time = time.time()

            duration = (end_time - start_time) * 1000
            print(f"-> Succes! (Durata creare: {duration:.2f} ms)\n")

        except Exception as e:
            print(f"-> Eroare la crearea indexului: {e}\n")

    print("Indexuri aplicate cu succes.")
    print("---------------------------------------------")
if __name__ == "__main__":
    apply_indexes()