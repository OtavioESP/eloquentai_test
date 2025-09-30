from typing import Optional, Dict, Any
from pydantic import EmailStr
import uuid

class AuthService:
    def __init__(self):
        self.fake_users_db = {
            "user@example.com": {
                "id": 1,
                "email": "user@example.com",
                "name": "Test User",
                "is_active": True,
            },
            "admin@example.com": {
                "id": 2,
                "email": "admin@example.com", 
                "name": "Admin User",
                "is_active": True,
            }
        }
    
    def validate_login_credentials(self, username: str, password: str) -> bool:
        if not username or not password:
            return False
            
        return username in self.fake_users_db
    
    def get_user_by_email(self, username: str) -> Optional[Dict[str, Any]]:
        return self.fake_users_db.get(username)
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        if not self.validate_login_credentials(username, password):
            return {
                "success": False,
                "message": "Invalid username or password",
                "user": None
            }
        
        user_data = self.get_user_by_email(username)
        
        if not user_data:
            return {
                "success": False,
                "message": "User not found",
                "user": None
            }

        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user_data["id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "is_active": user_data["is_active"]
            }
        }

    def unlogged_user(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": uuid.uuid4(),
            }
        }
