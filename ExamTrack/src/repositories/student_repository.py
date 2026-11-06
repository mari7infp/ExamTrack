from database.database import get_connection
from models.models import Student

class StudentRepository:
    def get_active_by_group(self, group_id: int) -> list[Student]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, group_id, record_book_number, full_name, status, email FROM students WHERE group_id = ? AND status = 'Обучается'", (group_id,))
            rows = cur.fetchall()
            return [Student(*row) for row in rows]
        finally:
            conn.close()

    
    def get_by_id(self, student_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM students WHERE id = ?", (student_id,))
            return cur.fetchone()
        finally:
            conn.close()