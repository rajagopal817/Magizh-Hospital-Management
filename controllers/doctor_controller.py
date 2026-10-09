"""
controllers/doctor_controller.py
--------------------------------
Doctor rules: add a doctor, assign a department, list doctors.
Every method that changes data returns (success, title, message).
"""

from models.doctor import Doctor


class DoctorController:
    @staticmethod
    def add(name, department, specialization, contact, available_days):
        name = name.strip()
        if not name or not department:
            return False, "Missing Data", "Doctor name and department are required."
        if not name.lower().startswith("dr"):
            name = "Dr. " + name

        new_id = Doctor.add(name, department, specialization.strip(),
                            contact.strip(), available_days.strip())
        return True, "Doctor Added", f"{name} added to {department}.\nDoctor ID: {new_id}"

    @staticmethod
    def change_department(doctor_id, doctor_name, department):
        if doctor_id is None:
            return False, "Select Doctor", "Please select a doctor in the table first."
        if not department:
            return False, "Select Department", "Please choose the new department."
        Doctor.update_department(doctor_id, department)
        return True, "Updated", f"{doctor_name} assigned to {department}."

    @staticmethod
    def list_doctors(department_filter):
        if department_filter and department_filter != "All":
            return Doctor.get_by_department(department_filter)
        return Doctor.get_all()

    @staticmethod
    def dropdown_list():
        """Texts like '1 - Dr. Arun Kumar (General Medicine)' for dropdowns."""
        return [f"{did} - {name} ({dept})" for did, name, dept in Doctor.get_short_list()]
