"""Repository for authentication-related database operations."""

class AuthRepository:
    def __init__(self, db):
        self.db = db

    def add_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        return True

    