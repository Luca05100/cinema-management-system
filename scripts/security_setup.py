import mariadb
import bcrypt
from cryptography.fernet import Fernet

DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_NAME = "cinema_system"
ROOT_USER = "root"
ROOT_PASS = "rootpass"

FERNET_KEY = b'Zq1P-hP6uNkV1Hh2o4n-_M-3X-12x_kK9p-Q_U_q2wM='

def get_root_connection():
    return mariadb.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=ROOT_USER,
        password=ROOT_PASS,
        database=DB_NAME
    )

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(
        plain.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

def create_db_users():
    conn = get_root_connection()
    cur = conn.cursor()
    db_users = [
        ("admin_user", "admin123", "ALL PRIVILEGES"),
        ("manager_user", "manager123", "SELECT, INSERT, UPDATE, DELETE"),
        ("editor_user", "editor123", "SELECT, INSERT, UPDATE"),
        ("viewer_user", "viewer123", "SELECT")
    ]

    for username, password, privileges in db_users:
        try:
            cur.execute(f"DROP USER IF EXISTS '{username}'@'%'")
            cur.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            cur.execute(f"GRANT {privileges} ON {DB_NAME}.* TO '{username}'@'%'")
            print(f"[OK] Created DB user: {username}")
        except Exception as e:
            print("Error:", e)

    cur.execute("FLUSH PRIVILEGES")
    conn.commit()
    conn.close()

def encrypt_app_users():
    conn = get_root_connection()
    cur = conn.cursor()

    #  Criptarea parolelor din tabela 'users'
    cur.execute("SELECT id, parola FROM users")
    password_rows = cur.fetchall()

    for user_id, pwd in password_rows:
        if not str(pwd).startswith("$2b$"): # Prevenire dublă criptare
            hashed = hash_password(str(pwd))
            cur.execute("UPDATE users SET parola=? WHERE id=?", (hashed, user_id))
            print(f"[UPDATED] User ID {user_id} password encrypted")

    # Criptarea email-ului
    cipher_suite = Fernet(FERNET_KEY)
    cur.execute("SELECT id, email FROM users")
    email_rows = cur.fetchall()

    for user_id, email in email_rows:
        # Token-urile Fernet încep cu 'gAAAAA'
        if not str(email).startswith("gAAAAA"):
            encrypted_email = cipher_suite.encrypt(str(email).encode('utf-8')).decode('utf-8')
            cur.execute("UPDATE users SET email=? WHERE id=?", (encrypted_email, user_id))
            print(f"[UPDATED] User ID {user_id} email encrypted")

    conn.commit()
    conn.close()

def main():
    print("\n=== CREATE DB USERS + GRANT ===")
    create_db_users()

    print("\n=== ENCRYPT APP USERS PASSWORDS & EMAILS ===")
    encrypt_app_users()

    print("\n SECURITY SETUP COMPLETED")

if __name__ == "__main__":
    main()