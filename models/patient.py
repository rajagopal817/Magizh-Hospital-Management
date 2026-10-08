"""
models/patient.py
-----------------
Data access for the 'patients' table.
"""

from datetime import date
from models.database import run_query

COLUMNS = "patient_id, name, age, gender, contact, address, symptoms, created_on"


class Patient:
    @staticmethod
    def add(name, age, gender, contact, address, symptoms):
        """Save a new patient and return the new Patient ID."""
        return run_query("""INSERT INTO patients (name, age, gender, contact, address,
                            symptoms, created_on) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                         (name, age, gender, contact, address, symptoms,
                          date.today().isoformat()))

    @staticmethod
    def get_all():
        return run_query(f"SELECT {COLUMNS} FROM patients ORDER BY patient_id DESC", fetch=True)

    @staticmethod
    def search(keyword):
        """Find patients by name, contact number or exact ID."""
        return run_query(f"""SELECT {COLUMNS} FROM patients
                             WHERE name LIKE ? OR contact LIKE ? OR CAST(patient_id AS TEXT) = ?
                             ORDER BY patient_id DESC""",
                         (f"%{keyword}%", f"%{keyword}%", keyword), fetch=True)

    @staticmethod
    def get_name(patient_id):
        rows = run_query("SELECT name FROM patients WHERE patient_id=?", (patient_id,), fetch=True)
        return rows[0][0] if rows else None

    @staticmethod
    def get_short_list():
        """(id, name, contact) for dropdown lists."""
        return run_query("SELECT patient_id, name, contact FROM patients ORDER BY patient_id DESC",
                         fetch=True)

    @staticmethod
    def count():
        return run_query("SELECT COUNT(*) FROM patients", fetch=True)[0][0]
