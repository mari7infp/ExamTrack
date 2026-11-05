from typing import Optional
from database.database import get_connection
from models.models import Statement

class StatementRepository:
    def check_exists(self, group_id: int, subject_id: int, semester: int) -> bool:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM statements WHERE group_id = ? AND subject_id = ? AND semester = ?", (group_id, subject_id, semester))
            row = cur.fetchone()
            return bool(row)
        finally:
            conn.close()

    def create(self, group_id: int, subject_id: int, teacher_id: int, semester: int, exam_date: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO statements (group_id, subject_id, teacher_id, semester, exam_date, status)
                VALUES (?, ?, ?, ?, ?, 'Открыта')
            """, (group_id, subject_id, teacher_id, semester, exam_date))
            statement_id = cur.lastrowid
            conn.commit()
            return statement_id
        finally:
            conn.close()

    def get_by_id(self, statement_id: int) -> Optional[Statement]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, group_id, subject_id, teacher_id, semester, exam_date, status FROM statements WHERE id = ?", (statement_id,))
            row = cur.fetchone()
            return Statement(*row) if row else None
        finally:
            conn.close()