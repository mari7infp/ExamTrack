from typing import Optional
from database.database import get_connection
from models.models import Teacher

class TeacherRepository:
    def get_by_user_id(self, user_id: int) -> Optional[Teacher]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, user_id, full_name, department, email FROM teachers WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            return Teacher(*row) if row else None
        finally:
            conn.close()

    def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, user_id, full_name, department, email FROM teachers WHERE id = ?", (teacher_id,))
            row = cur.fetchone()
            return Teacher(*row) if row else None
        finally:
            conn.close()