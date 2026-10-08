"""
controllers/helpers.py
----------------------
Small checks shared by the controllers.
"""

from datetime import datetime


def is_valid_date(text):
    """True if text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_time(text):
    """True if text is a real time in HH:MM format."""
    try:
        datetime.strptime(text, "%H:%M")
        return True
    except ValueError:
        return False


def id_from_choice(choice):
    """Get the ID from a dropdown text, e.g. '12 - Ravi (9876543210)' -> 12."""
    try:
        return int(choice.split(" - ")[0])
    except (ValueError, IndexError, AttributeError):
        return None
