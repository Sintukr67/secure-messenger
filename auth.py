import hashlib
import json
import os
from datetime import datetime

class UserAuth:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()

    def load_users(self):
        """Load existing users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def register_user(self, username, password):
        """Register a new user with password hashing"""
        if username in self.users:
            return False, "Username already exists"
        
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Store user data
        self.users[username] = {
            'password': hashed_password,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        self.save_users()
        return True, "Registration successful"

    def verify_user(self, username, password):
        """Verify user credentials"""
        if username not in self.users:
            return False, "User not found"
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self.users[username]['password'] == hashed_password:
            # Update last login time
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True, "Login successful"
        return False, "Invalid password"

    def validate_session(self, username):
        """Validate if user session is active"""
        if username not in self.users:
            return False
        return True 