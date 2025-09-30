import os
import uuid
import psycopg2
from typing import Optional, Dict, Any
from psycopg2.extras import RealDictCursor
from pydantic import EmailStr

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rag_chat'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

class AuthService:
    def __get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
            return conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise e

    def validate_login_credentials(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        user = self.get_user_by_username(username)
        return user is not None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        query = "SELECT id, name FROM users WHERE name = %s LIMIT 1"
        conn = None
        try:
            conn = self.__get_connection()
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                user = cur.fetchone()
                return dict(user) if user else None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        if not self.validate_login_credentials(username, password):
            return {
                "success": False,
                "message": "Invalid username or password",
                "user": None
            }

        user_data = self.get_user_by_username(username)
        if not user_data:
            return {
                "success": False,
                "message": "User not found",
                "user": None
            }

        return {
            "success": True,
            "message": "Login successful",
            "user": user_data
        }

    def unlogged_user(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": str(uuid.uuid4()),  # Make sure to convert UUID to string
            }
        }
