"""
controllers/report_controller.py
--------------------------------
Data for the Dashboard and the Reports screens.
"""

from datetime import date
from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient
from controllers.helpers import id_from_choice


class ReportController:
    @staticmethod
    def dashboard_counts():
        today = date.today().isoformat()
        return {
            "Total Patients": Patient.count(),
            "Total Doctors": Doctor.count(),
            "Today's Appointments": Appointment.count_booked_on(today),
            "Upcoming Appointments": Appointment.count_booked_from(today),
        }

    @staticmethod
    def todays_appointments():
        return Appointment.get_today_for_dashboard(date.today().isoformat())

    @staticmethod
    def appointment_summary(group_by):
        """Returns (title, columns, rows) for the summary table."""
        rows = Appointment.summary(group_by)
        return (f"Appointment Summary by {group_by}",
                (group_by, "Total", "Booked", "Cancelled"), rows)

    @staticmethod
    def patient_history(patient_choice):
        """Returns (success, title or error, columns, rows)."""
        patient_id = id_from_choice(patient_choice)
        if not patient_id:
            return False, "Please select a patient.", (), []
        rows = Appointment.history_of_patient(patient_id)
        columns = ("App. ID", "Date", "Time", "Doctor", "Department", "Reason", "Status")
        return True, f"Appointment History - {patient_choice}", columns, rows
