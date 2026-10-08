"""
models/demo_data.py
-------------------
Sample data for the DEMO version (used only when config.DEMO_MODE = True).

Dates are calculated from today's date, so the Dashboard always shows
"today's" and "upcoming" appointments whenever the demo is opened.
"""

from datetime import date, timedelta
from models.database import run_query


# Extra doctors (4 doctors are already added by setup_database).
# All demo names and phone numbers are made up (anonymous sample data).
DEMO_DOCTORS = [
    ("Doctor 5", "ENT", "MS ENT", "98XXXXX555", "Mon-Fri"),
    ("Doctor 6", "Gynecology", "MD OBG", "98XXXXX666", "Mon-Sat"),
    ("Doctor 7", "Dermatology", "MD Dermatology", "98XXXXX777", "Tue-Sat"),
]

# Anonymous patients:
# (name, age, gender, contact, address, symptoms, registered N days ago)
DEMO_PATIENTS = [
    ("Patient A", 45, "Male", "98XXXXX210", "Area 1", "Fever", 10),
    ("Patient B", 52, "Female", "91XXXXX780", "Area 2", "Chest pain", 9),
    ("Patient C", 34, "Male", "90XXXXX111", "Area 3", "Knee pain", 8),
    ("Patient D", 6, "Female", "90XXXXX222", "Area 1", "Vaccination", 7),
    ("Patient E", 29, "Male", "90XXXXX333", "Area 4", "Headache", 5),
    ("Patient F", 61, "Female", "90XXXXX444", "Area 2", "High BP", 4),
    ("Patient G", 23, "Male", "90XXXXX555", "Area 5", "Ear pain", 3),
    ("Patient H", 31, "Female", "90XXXXX666", "Area 1", "Routine checkup", 2),
    ("Patient I", 48, "Male", "90XXXXX777", "Area 3", "Back pain", 1),
    ("Patient J", 27, "Female", "90XXXXX888", "Area 4", "Skin allergy", 0),
]

# (patient_id, doctor_id, days from today, time, reason, status)
# negative days = past, 0 = today, positive = upcoming
DEMO_APPOINTMENTS = [
    # Past visits (shown in patient history and reports)
    (1, 1, -7, "10:00", "Fever and cold", "Booked"),
    (2, 2, -5, "11:00", "Chest pain checkup", "Booked"),
    (3, 3, -3, "09:30", "Knee pain", "Booked"),
    (1, 1, -2, "16:00", "Follow-up visit", "Booked"),
    (4, 4, -1, "10:30", "Child vaccination", "Cancelled"),
    # Today
    (5, 1, 0, "09:30", "Headache", "Booked"),
    (6, 2, 0, "10:00", "BP review", "Booked"),
    (7, 5, 0, "11:30", "Ear pain", "Booked"),
    (8, 6, 0, "12:00", "Routine checkup", "Booked"),
    (2, 2, 0, "15:00", "ECG follow-up", "Booked"),
    # Upcoming
    (9, 3, 1, "10:00", "Back pain", "Booked"),
    (10, 7, 1, "11:00", "Skin allergy", "Booked"),
    (3, 3, 2, "09:30", "Physiotherapy review", "Booked"),
    (7, 5, 2, "16:30", "Hearing test", "Cancelled"),
    (6, 1, 3, "14:00", "Diabetes check", "Booked"),
    (4, 4, 4, "10:30", "Vaccination (rescheduled)", "Booked"),
]


def load_demo_data():
    """Fill the in-memory database with sample doctors, patients and appointments."""
    today = date.today()

    for doctor in DEMO_DOCTORS:
        run_query("""INSERT INTO doctors (name, department, specialization,
                     contact, available_days) VALUES (?, ?, ?, ?, ?)""", doctor)

    for name, age, gender, contact, address, symptoms, days_ago in DEMO_PATIENTS:
        registered = (today - timedelta(days=days_ago)).isoformat()
        run_query("""INSERT INTO patients (name, age, gender, contact, address,
                     symptoms, created_on) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (name, age, gender, contact, address, symptoms, registered))

    for patient_id, doctor_id, days, time, reason, status in DEMO_APPOINTMENTS:
        department = run_query("SELECT department FROM doctors WHERE doctor_id=?",
                               (doctor_id,), fetch=True)[0][0]
        app_date = (today + timedelta(days=days)).isoformat()
        run_query("""INSERT INTO appointments (patient_id, doctor_id, department,
                     app_date, app_time, reason, status)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (patient_id, doctor_id, department, app_date, time, reason, status))
