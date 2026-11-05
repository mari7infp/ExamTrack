from typing import Optional
from database.database import get_connection
from models.models import AcademicGroup

class GroupRepository:
    def get_by_id(self, group_id: int) -> Optional[AcademicGroup]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, code, course, faculty FROM academic_groups WHERE id = ?", (group_id,))
            row = cur.fetchone()
            return AcademicGroup(*row) if row else None
        finally:
            conn.close()