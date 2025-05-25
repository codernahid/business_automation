"""
Role-based authentication system with secure password handling
"""
import hashlib
from database import db

class AuthManager:
    def __init__(self):
        self.current_user = None
        self.user_role = None
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user with hashed password verification"""
        try:
            user = db.execute_query(
                "SELECT * FROM users WHERE username = ? LIMIT 1",
                (username,)
            )
            
            if user and self._verify_password(password, user[0]['password']):
                self.current_user = user[0]['username']
                self.user_role = user[0]['role']
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        """SHA-256 password hashing with salt"""
        salt = "signature_salt"  # In production, use per-user salts
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _verify_password(self, input_pw: str, stored_hash: str) -> bool:
        """Compare hashed passwords"""
        return self._hash_password(input_pw) == stored_hash