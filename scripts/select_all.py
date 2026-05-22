import json
from pathlib import Path
from app.db import run_select

sql = """
SELECT 
    m.id,
    m.titlu,
    m.gen,
    COUNT(t.id) AS bilete_vandute,
    COALESCE(SUM(t.pret_final), 0) AS incasari_totale
FROM movies m
LEFT JOIN showtimes s ON m.id = s.movie_id
LEFT JOIN bookings b ON s.id = b.showtime_id
LEFT JOIN tickets t ON b.id = t.booking_id
GROUP BY m.id, m.titlu, m.gen
ORDER BY incasari_totale DESC;
"""

rows = run_select(sql)

# Prelucrarea rezultatului (transformare din lista de tupluri in lista de dictionare)
data = []
for r in rows:
    data.append({
        "id": r[0],
        "titlu": r[1],
        "gen": r[2],
        "bilete_vandute": r[3],
        "incasari_totale": float(r[4]) if r[4] is not None else 0.0
    })

out_path = Path("outputs") / "movies_financial_report.json"

out_path.parent.mkdir(exist_ok=True)

out_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"JSON salvat: {out_path}")