"""
config.py
---------
All application settings in one place.
Change the hospital name, colours or departments here.
"""

import os
import sys

# ---------------- Hospital details ----------------
HOSPITAL_NAME = "Surya Hospital"
APP_TITLE = HOSPITAL_NAME + " - Hospital Management System"

DEPARTMENTS = ["General Medicine", "Cardiology", "Orthopedics",
               "Pediatrics", "Gynecology", "ENT", "Dermatology"]

# Appointment time slots: 09:00 to 17:30, every 30 minutes
TIME_SLOTS = [f"{h:02d}:{m:02d}" for h in range(9, 18) for m in (0, 30)]

# Default admin login (created on first run)
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

# ---------------- Colours ----------------
PRIMARY = "#0F5C7A"      # dark teal (header, buttons)
LIGHT_BG = "#F2F6F8"     # page background
WHITE = "#FFFFFF"
GREY = "#777777"
GREEN = "#2E7D32"
RED = "#C62828"


# ---------------- Database location ----------------
def get_base_folder():
    """Folder of the program (works for both .py and .exe)."""
    if getattr(sys, "frozen", False):        # running as .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


DB_PATH = os.path.join(get_base_folder(), "hospital.db")
