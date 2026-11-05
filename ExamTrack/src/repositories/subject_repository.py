from typing import Optional
from database.database import get_connection
from models.models import Subject

class SubjectRepository:
    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, control_type, semester, hours FROM subjects WHERE id = ?", (subject_id,))
            row = cur.fetchone()
            return Subject(*row) if row else None
        finally:
            conn.close()