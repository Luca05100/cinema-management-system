import csv
import os
from pathlib import Path
import mariadb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "cinema_system")
    )

def export_to_csv(table_name="movies"):
    out_dir = Path("exports")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{table_name}.csv"

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

        print(f"EXPORT REUSIT -> {out_path} ({len(rows)} filme)")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    export_to_csv("movies")