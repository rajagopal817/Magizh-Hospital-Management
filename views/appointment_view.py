"""
views/appointment_view.py
-------------------------
Appointments tab: booking form, cancel button and appointment table.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import config
from controllers.appointment_controller import AppointmentController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from views.widgets import (make_table, fill_table, section_title, form_title,
                           form_row, button)


class AppointmentView:
    def __init__(self, notebook, on_change):
        self.on_change = on_change
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)
        section_title(self.frame, "Appointment Booking")

        body = tk.Frame(self.frame, bg=config.LIGHT_BG)
        body.pack(fill="both", expand=True, padx=20, pady=5)

        # ---- Left: booking form ----
        form = tk.Frame(body, bg=config.WHITE, padx=10, pady=10)
        form.pack(side="left", fill="y", padx=(0, 10))
        form_title(form, "Book Appointment")

        self.patient = ttk.Combobox(form, state="readonly", width=30)
        self.doctor = ttk.Combobox(form, state="readonly", width=30)
        self.app_date = ttk.Entry(form, width=32)
        self.app_time = ttk.Combobox(form, width=30, values=config.TIME_SLOTS)
        self.reason = ttk.Entry(form, width=32)
        self.app_date.insert(0, date.today().isoformat())

        form_row(form, 1, "Patient *", self.patient)
        form_row(form, 2, "Doctor *", self.doctor)
        form_row(form, 3, "Date (YYYY-MM-DD) *", self.app_date)
        form_row(form, 4, "Time (HH:MM) *", self.app_time)
        form_row(form, 5, "Reason", self.reason)

        btns = tk.Frame(form, bg=config.WHITE)
        btns.grid(row=6, column=0, columnspan=2, pady=10)
        button(btns, "Book Appointment", self.book).pack(side="left", padx=5)
        button(btns, "Cancel Selected", self.cancel, config.RED).pack(side="left", padx=5)

        # ---- Right: filter + table ----
        right = tk.Frame(body, bg=config.LIGHT_BG)
        right.pack(side="left", fill="both", expand=True)
        filter_bar = tk.Frame(right, bg=config.LIGHT_BG)
        filter_bar.pack(fill="x", pady=(0, 8))
        tk.Label(filter_bar, text="Show:", bg=config.LIGHT_BG).pack(side="left")
        self.view = ttk.Combobox(filter_bar, state="readonly", width=18,
                                 values=["Upcoming", "Today", "All", "Cancelled"])
        self.view.set("Upcoming")
        self.view.pack(side="left", padx=5)
        self.view.bind("<<ComboboxSelected>>", lambda e: self.load_appointments())

        cols = ("App. ID", "Patient", "Doctor", "Department", "Date", "Time", "Status")
        table_frame, self.table = make_table(right, cols, (58, 100, 118, 105, 85, 50, 72))
        table_frame.pack(fill="both", expand=True)

        self.reload_choices()

    def reload_choices(self):
        """Refresh the patient/doctor dropdowns and the table."""
        self.patient["values"] = PatientController.dropdown_list()
        self.doctor["values"] = DoctorController.dropdown_list()
        self.load_appointments()

    def book(self):
        ok, title, message = AppointmentController.book(
            self.patient.get(), self.doctor.get(), self.app_date.get(),
            self.app_time.get(), self.reason.get())
        if not ok:
            messagebox.showwarning(title, message)
            return
        messagebox.showinfo(title, message)
        self.reason.delete(0, "end")
        self.app_time.set("")
        self.on_change()

    def cancel(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select Appointment",
                                   "Please select an appointment in the table.")
            return
        values = self.table.item(selected[0])["values"]
        appointment_id, status = values[0], values[6]

        ok, title, message = AppointmentController.can_cancel(status)
        if not ok:
            messagebox.showinfo(title, message)
            return
        if messagebox.askyesno("Cancel Appointment", f"Cancel appointment ID {appointment_id}?"):
            title, message = AppointmentController.cancel(appointment_id)
            messagebox.showinfo(title, message)
            self.on_change()

    def load_appointments(self):
        fill_table(self.table, AppointmentController.list_appointments(self.view.get()))
