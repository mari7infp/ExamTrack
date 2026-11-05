import sqlite3
import os

def create_tables():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "examtrack.db")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR NOT NULL UNIQUE,
            password_hash VARCHAR NOT NULL,
            role VARCHAR NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name VARCHAR NOT NULL,
            department VARCHAR,
            email VARCHAR,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        
        CREATE TABLE IF NOT EXISTS academic_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR NOT NULL UNIQUE,
            course INTEGER NOT NULL,
            faculty VARCHAR NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR NOT NULL,
            control_type VARCHAR NOT NULL,
            semester INTEGER NOT NULL,
            hours INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            record_book_number VARCHAR NOT NULL UNIQUE,
            full_name VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            email VARCHAR,
            FOREIGN KEY(group_id) REFERENCES academic_groups(id)
        );
        
        CREATE TABLE IF NOT EXISTS statements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            exam_date DATE NOT NULL,
            status VARCHAR NOT NULL,
            FOREIGN KEY(group_id) REFERENCES academic_groups(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        );
        
        CREATE TABLE IF NOT EXISTS statement_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            statement_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            mark INTEGER,
            mark_text VARCHAR,
            grade_date DATE,
            note VARCHAR,
            FOREIGN KEY(statement_id) REFERENCES statements(id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
    """)
    
    conn.commit()
    conn.close()
    print("База данных examtrack.db и таблицы успешно созданы.")

if __name__ == "__main__":
    create_tables()