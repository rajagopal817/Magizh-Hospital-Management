"""
controllers/patient_controller.py
---------------------------------
Patient registration rules and search.
Every method that changes data returns (success, title, message).
In demo mode (config.DEMO_MODE) inputs are checked and a success message
is shown, but nothing is stored.
"""

import config
from models.patient import Patient


class PatientController:
    @staticmethod
    def register(name, age, gender, contact, address, symptoms):
        name, age, contact = name.strip(), age.strip(), contact.strip()

        # ---- Validation ----
        if not name or not age or not gender or not contact:
            return False, "Missing Data", "Please fill all fields marked with *."
        if not age.isdigit() or not (0 < int(age) < 120):
            return False, "Invalid Age", "Please enter a valid age (1-119)."
        if not contact.isdigit() or len(contact) != 10:
            return False, "Invalid Contact", "Contact number must be 10 digits."

        # ---- Demo version: confirm only, do not store ----
        if config.DEMO_MODE:
            return True, "Patient Saved", (
                "Patient details saved successfully!\n\n"
                f"Name : {name}\nAge : {age}\nContact : {contact}")

        # ---- Save ----
        new_id = Patient.add(name, int(age), gender, contact,
                             address.strip(), symptoms.strip())
        return True, "Patient Registered", (
            "Patient registered successfully!\n\n"
            f"Patient ID : {new_id}\nName : {name}\nContact : {contact}")

    @staticmethod
    def search(keyword):
        """Return all patients, or only those matching the keyword."""
        keyword = keyword.strip()
        return Patient.search(keyword) if keyword else Patient.get_all()

    @staticmethod
    def dropdown_list():
        """Texts like '3 - Karthik (9000011111)' for dropdowns."""
        return [f"{pid} - {name} ({contact})" for pid, name, contact in Patient.get_short_list()]
