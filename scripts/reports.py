import json
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from app.db import run_select

OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

LOGO_PATH = Path("cinema_city.jpeg")


def normalize(v):
    if isinstance(v, Decimal):
        x = float(v)
        return int(x) if x.is_integer() else x
    return v


def fetch_data(report_id):
    if report_id == 1:
        sql = """
        SELECT m.titlu, COALESCE(SUM(t.pret_final), 0) as total_val
        FROM movies m
        LEFT JOIN showtimes s ON m.id = s.movie_id
        LEFT JOIN bookings b ON s.id = b.showtime_id
        LEFT JOIN tickets t ON b.id = t.booking_id
        GROUP BY m.id, m.titlu
        ORDER BY total_val DESC
        """
    else:
        sql = """
        SELECT h.nume_sala, COUNT(t.id) as total_val
        FROM halls h
        LEFT JOIN showtimes s ON h.id = s.hall_id
        LEFT JOIN bookings b ON s.id = b.showtime_id
        LEFT JOIN tickets t ON b.id = t.booking_id
        GROUP BY h.id, h.nume_sala
        ORDER BY total_val DESC
        """

    rows = run_select(sql)
    # Standardizam cheile pentru a putea refolosi functiile de export
    return [{"nume": r[0], "valoare": normalize(r[1])} for r in rows]


def export_csv(data, csv_path):
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nume", "valoare"])
        writer.writeheader()
        writer.writerows(data)


def export_json(data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_chart(data, chart_path, report_id):
    # Fereastra putin mai lata
    plt.figure(figsize=(10, 6))

    if report_id == 1:
        # TAIEREA DATELOR: Preluam doar primele 15 filme pentru a pastra graficul curat
        top_data = data[:15]
        names = [d["nume"] for d in top_data]
        values = [d["valoare"] for d in top_data]

        plt.bar(names, values, color="#3498db")
        plt.title("Top 15 Filme dupa Venituri")
        plt.xlabel("Titlu Film")
        plt.ylabel("Venit Total (RON)")
        # Rotire, aliniere la dreapta a textului sub axa X si font usor micsorat
        plt.xticks(rotation=45, ha="right", fontsize=9)
    else:
        # Pentru sali (care sunt mai putine), lasam toate datele
        names = [d["nume"] for d in data]
        values = [d["valoare"] for d in data]
        plt.pie(values, labels=names, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title("Distributia Traficului pe Sali")

    # tight_layout se asigura ca marginile nu taie textul
    plt.tight_layout()
    plt.savefig(str(chart_path))
    plt.close()

def generate_pdf(data, pdf_path, chart_path, report_id):
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=20
    )

    normal_style = styles["Normal"]

    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=1.5 * inch, height=1.5 * inch)
        elements.append(logo)
        elements.append(Spacer(1, 20))

    elements.append(Paragraph("Raport Business Intelligence", title_style))
    elements.append(Spacer(1, 10))

    if report_id == 1:
        titlu_secundar = "Performanta Financiara a Filmelor"
        text_descriere = "Acest raport prezinta analiza veniturilor generate de filmele din Cinema City. Datele sunt agregate din vanzarile de bilete si sunt ordonate descrescator."
        col_1 = "Titlu Film"
        col_2 = "Venit Total (RON)"
    else:
        titlu_secundar = "Analiza Traficului pe Sali"
        text_descriere = "Acest raport indica gradul de ocupare al fiecarei sali, calculat prin numarul total de bilete vandute per locatie, facilitand optimizarea logisticii."
        col_1 = "Nume Sala"
        col_2 = "Numar Clienti"

    elements.append(Paragraph(titlu_secundar, styles["Heading2"]))
    elements.append(Spacer(1, 15))

    intro_text = f"""
    {text_descriere}
    Raport generat la data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 20))

    table_data = [[col_1, col_2]]
    for d in data:
        table_data.append([d["nume"], d["valoare"]])

    table = Table(table_data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    if chart_path.exists():
        chart = Image(str(chart_path), width=6 * inch, height=4 * inch)
        elements.append(chart)

    doc.build(elements)


def process_report(report_id):
    if report_id == 1:
        base_name = "Top_Filme_Venituri"
    else:
        base_name = "Trafic_Sali"

    pdf_path = OUT_DIR / f"{base_name}.pdf"
    csv_path = OUT_DIR / f"{base_name}.csv"
    json_path = OUT_DIR / f"{base_name}.json"
    chart_path = OUT_DIR / f"{base_name}_chart.png"

    data = fetch_data(report_id)

    if not data:
        print(f"Nu exista date pentru raportul {report_id}.")
        return

    export_csv(data, csv_path)
    export_json(data, json_path)
    generate_chart(data, chart_path, report_id)
    generate_pdf(data, pdf_path, chart_path, report_id)

    print(f"Raport complet generat in folderul: {OUT_DIR.resolve()}")


def main():
    print("\n--- GENERARE AUTOMATA RAPOARTE BI CINEMA CITY ---")
    process_report(1)
    process_report(2)

if __name__ == "__main__":
    main()


