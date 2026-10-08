"""
models/user.py
--------------
Data access for the 'users' table (login).
"""

from models.database import run_query


class User:
    @staticmethod
    def check_login(username, password):
        """Return True if the username and password match a user."""
        rows = run_query("SELECT * FROM users WHERE username=? AND password=?",
                         (username, password), fetch=True)
        return len(rows) > 0
