import sqlite3
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    with open("database/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Base de données initialisée.")

def seed_db():
    conn = get_connection()
    with open("database/seed.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Catalogue initial chargé.")

if __name__ == "__main__":
    init_db()
    seed_db()

if __name__ == "__main__":
    init_db()
    seed_db()

    conn = get_connection()
    produits = conn.execute("SELECT * FROM produits").fetchall()
    for p in produits:
        print(dict(p))
    conn.close()