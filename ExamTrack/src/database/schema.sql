PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'teacher')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS academic_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    course INTEGER NOT NULL CHECK(course BETWEEN 1 AND 6),
    faculty TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    record_book_number TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    status TEXT CHECK(status IN ('учится', 'академический отпуск', 'отчислен', 'выпущен')) DEFAULT 'учится',
    email TEXT,
    FOREIGN KEY (group_id) REFERENCES academic_groups(id) ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    control_type TEXT CHECK(control_type IN ('экзамен', 'зачет')) NOT NULL,
    semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 12),
    hours INTEGER NOT NULL CHECK(hours > 0)
);


CREATE TABLE IF NOT EXISTS statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    exam_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Открыта', 'Закрыта')) DEFAULT 'Открыта',
    FOREIGN KEY (group_id) REFERENCES academic_groups(id) ON DELETE RESTRICT,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE RESTRICT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS statement_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    statement_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    mark INTEGER CHECK(mark IS NULL OR (mark BETWEEN 2 AND 5)),
    mark_text TEXT CHECK(mark_text IN ('отлично', 'хорошо', 'удовлетворительно', 'неудовлетворительно', 'зачтено', 'не зачтено', 'н/я')),
    grade_date DATE,
    note TEXT,
    UNIQUE(statement_id, student_id),
    FOREIGN KEY (statement_id) REFERENCES statements(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);