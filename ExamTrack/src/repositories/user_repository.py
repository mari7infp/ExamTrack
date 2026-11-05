from typing import Optional
from database.database import get_connection
from models.models import User

class UserRepository:
    def get_by_login(self, login: str) -> Optional[User]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, login, password_hash, role, created_at FROM users WHERE login = ?", (login,))
            row = cur.fetchone()
            return User(*row) if row else None
        finally:
            conn.close()