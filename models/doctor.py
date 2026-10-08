"""
models/doctor.py
----------------
Data access for the 'doctors' table.
"""

from models.database import run_query

COLUMNS = "doctor_id, name, department, specialization, contact, available_days"


class Doctor:
    @staticmethod
    def add(name, department, specialization, contact, available_days):
        """Save a new doctor and return the new Doctor ID."""
        return run_query("""INSERT INTO doctors (name, department, specialization, contact,
                            available_days) VALUES (?, ?, ?, ?, ?)""",
                         (name, department, specialization, contact, available_days))

    @staticmethod
    def get_all():
        return run_query(f"SELECT {COLUMNS} FROM doctors ORDER BY doctor_id", fetch=True)

    @staticmethod
    def get_by_department(department):
        return run_query(f"SELECT {COLUMNS} FROM doctors WHERE department=? ORDER BY name",
                         (department,), fetch=True)

    @staticmethod
    def update_department(doctor_id, department):
        run_query("UPDATE doctors SET department=? WHERE doctor_id=?", (department, doctor_id))

    @staticmethod
    def get_name_and_department(doctor_id):
        rows = run_query("SELECT name, department FROM doctors WHERE doctor_id=?",
                         (doctor_id,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def get_short_list():
        """(id, name, department) for dropdown lists."""
        return run_query("SELECT doctor_id, name, department FROM doctors ORDER BY name", fetch=True)

    @staticmethod
    def count():
        return run_query("SELECT COUNT(*) FROM doctors", fetch=True)[0][0]
