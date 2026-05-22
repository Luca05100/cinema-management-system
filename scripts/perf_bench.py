import time
import statistics
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from app.db import run_select, run_execute

# Configurări
RUNS = 50
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_FILE = OUTPUT_DIR / "performance_report.txt"
CHART_FILE = OUTPUT_DIR / "performance_chart.png"

# 1. DEFINIREA QUERY-URILOR PENTRU CINEMA
TEST_QUERIES = [
    {
        "name": "User by Email",
        "sql": "SELECT * FROM users WHERE email = %s;",
        "params": ("admin@cinema.com",),  # Presupunem că acest email există în seed.py
    },
    {
        "name": "Movie by Title",
        "sql": "SELECT * FROM movies WHERE titlu = %s;",
        "params": ("Avatar",),  # Înlocuiește cu un titlu din baza ta
    },
    {
        "name": "Tickets by Price",
        "sql": "SELECT * FROM tickets WHERE pret_final > %s;",
        "params": (20.0,),
    }
]

# 2. DEFINIREA INDEXURILOR (Optimale pentru query-urile de mai sus)
INDEX_SQL = [
    "CREATE INDEX idx_users_email ON users(email);",
    "CREATE INDEX idx_movies_titlu ON movies(titlu);",
    "CREATE INDEX idx_tickets_pret ON tickets(pret_final);"
]

# Funcția pentru ștergerea indexurilor (ca să putem rula testul de mai multe ori curat)
DROP_INDEX_SQL = [
    "DROP INDEX idx_users_email ON users;",
    "DROP INDEX idx_movies_titlu ON movies;",
    "DROP INDEX idx_tickets_pret ON tickets;"
]


def benchmark_query(sql: str, params, runs: int):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        run_select(sql, params)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convertim în milisecunde
    return times


def summarize(times):
    avg = statistics.mean(times)
    mn = min(times)
    mx = max(times)
    std = statistics.stdev(times) if len(times) > 1 else 0.0
    return avg, mn, mx, std


def run_suite(label: str):
    results = {}
    for q in TEST_QUERIES:
        times = benchmark_query(q["sql"], q["params"], RUNS)
        avg, mn, mx, std = summarize(times)
        results[q["name"]] = {"avg": avg, "min": mn, "max": mx, "std": std}
        print(f"[{label}] {q['name']} -> avg {avg:.2f} ms")
    return results


def apply_indexes():
    for stmt in INDEX_SQL:
        try:
            run_execute(stmt)
        except:
            pass  # Ignorăm dacă există deja


def drop_indexes():
    for stmt in DROP_INDEX_SQL:
        try:
            run_execute(stmt)
        except:
            pass  # Ignorăm dacă nu există


def pct_change(before, after):
    if before <= 0: return 0.0
    return ((before - after) / before) * 100.0


def generate_chart(before_results, after_results):
    labels = list(before_results.keys())
    before_means = [before_results[name]["avg"] for name in labels]
    after_means = [after_results[name]["avg"] for name in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width / 2, before_means, width, label='Fără Index', color='#e74c3c')
    rects2 = ax.bar(x + width / 2, after_means, width, label='Cu Index', color='#2ecc71')

    ax.set_ylabel('Timp mediu (ms)')
    ax.set_title('Performanță Cinema: Impactul Indexării')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    ax.bar_label(rects1, padding=3, fmt='%.4f')
    ax.bar_label(rects2, padding=3, fmt='%.4f')

    fig.tight_layout()
    plt.savefig(CHART_FILE)
    print(f"\nGrafic salvat în: {CHART_FILE}")


def main():
    # Ne asigurăm că începem de la zero (fără indexuri)
    drop_indexes()

    lines = ["=== ANALIZA PERFORMANTA CINEMA (SQL) ===\n"]
    lines.append(f"Rulări per query: {RUNS}\n")

    print("Pas 1: Rulăm testele fără indexare...")
    before = run_suite("BEFORE")

    print("\nPas 2: Aplicăm indexurile pe Email, Titlu și Preț...")
    apply_indexes()

    print("\nPas 3: Rulăm testele după optimizare...")
    after = run_suite("AFTER")

    # Construire raport
    for name in before:
        b_avg = before[name]["avg"]
        a_avg = after[name]["avg"]
        imp = pct_change(b_avg, a_avg)
        lines.append(f"Query: {name}")
        lines.append(f"  AVG Inainte: {b_avg:.4f} ms")
        lines.append(f"  AVG Dupa:    {a_avg:.4f} ms")
        lines.append(f"  Imbunatatire: {imp:.1f}%\n")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Raport text salvat în: {REPORT_FILE}")

    generate_chart(before, after)


if __name__ == "__main__":
    main()