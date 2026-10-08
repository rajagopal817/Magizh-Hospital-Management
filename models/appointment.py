"""
models/appointment.py
---------------------
Data access for the 'appointments' table, including report queries.
"""

from models.database import run_query

# Joined query used by the appointment lists
LIST_SQL = """
    SELECT a.appointment_id, p.name, d.name, a.department, a.app_date, a.app_time, a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d  ON a.doctor_id  = d.doctor_id
"""


class Appointment:
    @staticmethod
    def add(patient_id, doctor_id, department, app_date, app_time, reason):
        """Save a new appointment and return the new Appointment ID."""
        return run_query("""INSERT INTO appointments (patient_id, doctor_id, department,
                            app_date, app_time, reason) VALUES (?, ?, ?, ?, ?, ?)""",
                         (patient_id, doctor_id, department, app_date, app_time, reason))

    @staticmethod
    def is_slot_taken(doctor_id, app_date, app_time):
        """True if the doctor already has a booked appointment at that date/time."""
        rows = run_query("""SELECT appointment_id FROM appointments WHERE doctor_id=?
                            AND app_date=? AND app_time=? AND status='Booked'""",
                         (doctor_id, app_date, app_time), fetch=True)
        return len(rows) > 0

    @staticmethod
    def cancel(appointment_id):
        run_query("UPDATE appointments SET status='Cancelled' WHERE appointment_id=?",
                  (appointment_id,))

    # ---------- Lists ----------
    @staticmethod
    def get_upcoming(today):
        return run_query(LIST_SQL + " WHERE a.app_date>=? AND a.status='Booked' "
                                    "ORDER BY a.app_date, a.app_time", (today,), fetch=True)

    @staticmethod
    def get_by_date(day):
        return run_query(LIST_SQL + " WHERE a.app_date=? ORDER BY a.app_time", (day,), fetch=True)

    @staticmethod
    def get_cancelled():
        return run_query(LIST_SQL + " WHERE a.status='Cancelled' ORDER BY a.app_date DESC",
                         fetch=True)

    @staticmethod
    def get_all():
        return run_query(LIST_SQL + " ORDER BY a.app_date DESC, a.app_time", fetch=True)

    @staticmethod
    def get_today_for_dashboard(today):
        return run_query("""
            SELECT a.appointment_id, p.name, d.name, a.department, a.app_time, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d  ON a.doctor_id  = d.doctor_id
            WHERE a.app_date = ? ORDER BY a.app_time""", (today,), fetch=True)

    # ---------- Counts ----------
    @staticmethod
    def count_booked_on(day):
        return run_query("SELECT COUNT(*) FROM appointments WHERE app_date=? AND status='Booked'",
                         (day,), fetch=True)[0][0]

    @staticmethod
    def count_booked_from(day):
        return run_query("SELECT COUNT(*) FROM appointments WHERE app_date>=? AND status='Booked'",
                         (day,), fetch=True)[0][0]

    # ---------- Reports ----------
    @staticmethod
    def summary(group_by):
        """Counts grouped by 'Doctor', 'Department' or 'Date'."""
        column = {"Doctor": "d.name", "Department": "a.department", "Date": "a.app_date"}[group_by]
        return run_query(f"""
            SELECT {column}, COUNT(*),
                   SUM(CASE WHEN a.status='Booked' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN a.status='Cancelled' THEN 1 ELSE 0 END)
            FROM appointments a JOIN doctors d ON a.doctor_id = d.doctor_id
            GROUP BY {column} ORDER BY {column}""", fetch=True)

    @staticmethod
    def history_of_patient(patient_id):
        return run_query("""
            SELECT a.appointment_id, a.app_date, a.app_time, d.name, a.department,
                   a.reason, a.status
            FROM appointments a JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id=? ORDER BY a.app_date DESC, a.app_time DESC""",
                         (patient_id,), fetch=True)
