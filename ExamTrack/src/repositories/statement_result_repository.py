from typing import Optional
from database.database import get_connection

class StatementResultRepository:
    def generate_empty_results(self, statement_id: int, student_ids: list[int]):
        conn = get_connection()
        try:
            cur = conn.cursor()
            for student_id in student_ids:
                cur.execute("""
                    INSERT INTO statement_results (statement_id, student_id)
                    VALUES (?, ?)
                """, (statement_id, student_id))
            conn.commit()
        finally:
            conn.close()

    def update_mark(self, statement_id: int, student_id: int, mark_int: Optional[int], mark_text: str, grade_date: str) -> bool:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE statement_results
                SET mark = ?, mark_text = ?, grade_date = ?
                WHERE statement_id = ? AND student_id = ?
            """, (mark_int, mark_text, grade_date, statement_id, student_id))
            is_updated = cur.rowcount > 0
            conn.commit()
            return is_updated
        finally:
            conn.close()