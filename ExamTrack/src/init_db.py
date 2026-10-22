import sqlite3
import os

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "examtrack.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")


def init_database():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    print("Создание таблиц по схеме...")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    print("Заполнение тестовыми данными...")
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print(f"База данных успешно инициализирована: {DB_PATH}")

if __name__ == "__main__":
    init_database()