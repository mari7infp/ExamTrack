import sqlite3
import os
import hashlib

def create_tables_and_seed():
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
    
   
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        password_hash = hashlib.sha256('12345'.encode('utf-8')).hexdigest()
        
        # администратор и преподаватель
        cur.execute("INSERT INTO users (login, password_hash, role) VALUES ('admin', ?, 'Администратор')", (password_hash,))
        cur.execute("INSERT INTO users (login, password_hash, role) VALUES ('teacher', ?, 'Преподаватель')", (password_hash,))
        teacher_id = cur.lastrowid
        cur.execute("INSERT INTO teachers (user_id, full_name, department, email) VALUES (?, 'Иванов И.А.', 'Кафедра ИТ', 'ivanov@univer.ru')", (teacher_id,))
        
        # тестовые группы (ID: 1, 2, 3, 4)
        cur.execute("""
            INSERT INTO academic_groups (code, course, faculty) VALUES 
            ('ИВТ-41', 4, 'ФИВТ'),
            ('ИСТ-21', 2, 'ИРИТ'),
            ('ФТ-11', 1, 'ФизТех'),
            ('ЭК-31', 3, 'ИРЭУ')
        """)
        
        # тестовые дисциплины (ID: 1, 2, 3, 4)
        cur.execute("""
            INSERT INTO subjects (title, control_type, semester, hours) VALUES 
            ('Программирование', 'Экзамен', 7, 144),
            ('Базы данных', 'Зачет', 3, 108),
            ('Высшая математика', 'Экзамен', 1, 180),
            ('Экономика', 'Экзамен', 5, 120)
        """)
        
        # тестовые студенты (ID: 1, 2, 3, 4, 5)
        cur.execute("""
            INSERT INTO students (group_id, record_book_number, full_name, status) VALUES 
            (1, '123456', 'Петров П.П.', 'Обучается'),
            (2, '234567', 'Смирнова А.А.', 'Обучается'),
            (2, '345678', 'Иванов И.И.', 'Обучается'),
            (3, '456789', 'Соколова М.М.', 'Обучается'),
            (4, '567890', 'Козлов К.К.', 'Обучается')
        """)
        
        print("Успех: База examtrack.db создана. Расширенные тестовые данные добавлены!")
    else:
        print("База examtrack.db уже существует и готова к работе.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables_and_seed()