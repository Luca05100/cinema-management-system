import json
from pathlib import Path
from app.db import run_select

sql = """
SELECT 
    h.nume_sala,
    COUNT(s.id) AS showtimes_count,
    AVG(s.pret_baza) AS avg_base_price
FROM halls h
LEFT JOIN showtimes s ON h.id = s.hall_id
GROUP BY h.id, h.nume_sala
ORDER BY showtimes_count DESC;
"""

rows = run_select(sql)

data = []
for r in rows:
    data.append({
        "nume_sala": r[0],
        "numar_proiectii": int(r[1]),
        "pret_mediu_bilet": round(float(r[2]), 2) if r[2] else 0.0
    })
out_path = Path("outputs") / "halls_stats.json"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"JSON salvat: {out_path}")