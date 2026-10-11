"""
models/user.py
--------------
Login check (demo users are listed in config.py).
"""

import config


class User:
    @staticmethod
    def check_login(username, password):
        return config.USERS.get(username) == password
