import json
from pathlib import Path
from app.db import run_select


MIN_SHOWTIMES = 3

sql = """
SELECT 
    h.nume_sala,
    h.capacitate,
    COUNT(s.id) AS numar_proiectii
FROM halls h
JOIN showtimes s ON h.id = s.hall_id
GROUP BY h.id, h.nume_sala, h.capacitate
HAVING numar_proiectii >= %s
ORDER BY numar_proiectii DESC;
"""


rows = run_select(sql, (MIN_SHOWTIMES,))


data = []
for r in rows:
    data.append({
        "info_sala": {
            "nume": r[0],
            "capacitate_maxima": r[1]
        },
        "activitate": {
            "proiectii_active": r[2],
            "status": "Intens" if r[2] > 5 else "Normal"
        }
    })

out_path = Path("outputs") / "halls_activity_filtered.json"
out_path.parent.mkdir(exist_ok=True)

out_path.write_text(json.dumps({
    "criteriu_filtrare_minim": MIN_SHOWTIMES,
    "data_generare": "2026-03-24",
    "sali_identificate": data
}, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"JSON salvat: {out_path}")