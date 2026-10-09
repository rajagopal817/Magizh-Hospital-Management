"""
controllers/appointment_controller.py
-------------------------------------
Booking rules: valid date/time, no past dates, no double booking.
Every method that changes data returns (success, title, message).
"""

from datetime import date
from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient
from controllers.helpers import is_valid_date, is_valid_time, id_from_choice


class AppointmentController:
    @staticmethod
    def book(patient_choice, doctor_choice, app_date, app_time, reason):
        patient_id = id_from_choice(patient_choice)
        doctor_id = id_from_choice(doctor_choice)
        app_date, app_time = app_date.strip(), app_time.strip()

        # ---- Validation ----
        if not patient_id or not doctor_id:
            return False, "Missing Data", "Please select a patient and a doctor."
        if not is_valid_date(app_date):
            return False, "Invalid Date", "Date must be in YYYY-MM-DD format."
        if app_date < date.today().isoformat():
            return False, "Invalid Date", "Appointment date cannot be in the past."
        if not is_valid_time(app_time):
            return False, "Invalid Time", "Time must be in HH:MM format (e.g. 10:30)."
        if Appointment.is_slot_taken(doctor_id, app_date, app_time):
            return False, "Slot Not Available", ("This doctor already has an appointment "
                                                 "at that time.\nPlease choose another time.")

        # ---- Save ----
        doctor_name, department = Doctor.get_name_and_department(doctor_id)
        patient_name = Patient.get_name(patient_id)
        new_id = Appointment.add(patient_id, doctor_id, department,
                                 app_date, app_time, reason.strip())
        return True, "Appointment Confirmed", (
            "Appointment booked successfully!\n\n"
            f"Appointment ID : {new_id}\n"
            f"Patient : {patient_id} - {patient_name}\n"
            f"Doctor : {doctor_id} - {doctor_name}\n"
            f"Department : {department}\n"
            f"Date / Time : {app_date}  {app_time}")

    @staticmethod
    def can_cancel(status):
        """Check before asking the user to confirm."""
        if status != "Booked":
            return False, "Info", "This appointment is already cancelled."
        return True, "", ""

    @staticmethod
    def cancel(appointment_id):
        Appointment.cancel(appointment_id)

    @staticmethod
    def list_appointments(view):
        """view is one of: Upcoming, Today, Cancelled, All."""
        today = date.today().isoformat()
        if view == "Upcoming":
            return Appointment.get_upcoming(today)
        if view == "Today":
            return Appointment.get_by_date(today)
        if view == "Cancelled":
            return Appointment.get_cancelled()
        return Appointment.get_all()
