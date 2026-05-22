import os
import mysql.connector as mariadb
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    "Deschide o conexiune catre MariaDB folosind date din .env"
    conn = mariadb.connect(
        host = os.getenv("DB_HOST", "127.0.0.1"),
        port = int(os.getenv("DB_PORT", "3307")),
        user = os.getenv("DB_USER", "root"),
        password = os.getenv("DB_PASSWORD", "rootpass"),
        database = os.getenv("DB_NAME", "cinema_system")
    )
    return conn
def run_select(sql, params=()):
    "Ruleaza select si returneaza toate randurile"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def run_execute(sql, params=()):
    "Ruleaza insert update/ delete si da commit"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected