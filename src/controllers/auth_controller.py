"""
controllers/auth_controller.py
------------------------------
Login logic.
"""

from models.user import User


class AuthController:
    @staticmethod
    def login(username, password):
        """Return (True, '') if login is correct, otherwise (False, error message)."""
        username = username.strip()
        if not username or not password:
            return False, "Please enter username and password."
        if User.check_login(username, password):
            return True, ""
        return False, "Invalid username or password."
