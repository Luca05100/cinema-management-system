import csv
import os
from pathlib import Path
import mariadb
from dotenv import load_dotenv

# Incarcam variabilele de mediu din .env
load_dotenv()


def get_connection():
    """Stabileste conexiunea cu baza de date MariaDB."""
    return mariadb.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "cinema_system")
    )


ALLOWED_TABLES = {"users", "movies", "halls", "seats", "showtimes", "bookings", "tickets", "users_log"}
AUTO_SKIP_COLS = {"id", "created_at"}


def import_table(table: str, csv_path: Path, truncate_first: bool = False):
    table = table.strip()

    if table not in ALLOWED_TABLES:
        print(f"EROARE: Tabel invalid: {table}")
        return

    if not csv_path.exists():
        print(f"EROARE: Fisierul {csv_path} NU a fost gasit!")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Analiza structurii tabelului din baza de date
        cur.execute(f"DESCRIBE {table};")
        table_cols = [r[0] for r in cur.fetchall()]

        with csv_path.open(mode="r", encoding="utf-8") as f:
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            reader = csv.DictReader(f, dialect=dialect)

            cols = [c.strip() for c in reader.fieldnames if c.strip() in table_cols and c.strip() not in AUTO_SKIP_COLS]

            if not cols:
                print(f"EROARE: Nu am gasit coloane potrivite in CSV. Verifica header-ul!")
                return

            print(f"INFO: Coloane detectate pentru import: {cols}")
            sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))});"

            data_to_save = []
            for row in reader:
                values = []
                is_empty = True
                for c in cols:
                    val = row.get(c)
                    val = val.strip() if val else ""
                    if val != "":
                        is_empty = False
                    values.append(val if val != "" else None)

                if not is_empty:
                    data_to_save.append(tuple(values))

            # Executia tranzactiei
            conn.begin()

            if truncate_first:
                print(f"ACTIUNE: Se sterg datele vechi din {table} (TRUNCATE)...")
                cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
                cur.execute(f"TRUNCATE TABLE {table};")
                cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

            print(f"PROCESARE: Se importa {len(data_to_save)} randuri in {table}...")

            cur.executemany(sql, data_to_save)

            conn.commit()
            print(f"SUCCES: Import finalizat! {len(data_to_save)} randuri adaugate in '{table}'.")

    except Exception as e:
        conn.rollback()
        print(f"EROARE CRITICA: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("\n--- MODUL IMPORT DATE CINEMA ---")

    # Parametrii pentru importul tabelului movies
    tabel_tinta = "movies"
    fisier_csv = Path("exports/movies.csv")

    confirm = input(f"Confirmati importul {fisier_csv} in tabelul {tabel_tinta}? (y/n): ").lower()
    if confirm == 'y':
        trunc = input("Doriti stergerea datelor existente (TRUNCATE)? (y/n): ").lower() == 'y'
        import_table(tabel_tinta, fisier_csv, truncate_first=trunc)
    else:
        print("Operatiune anulata de utilizator.")