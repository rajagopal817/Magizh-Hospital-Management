"""
views/patient_view.py
---------------------
Patients tab: registration form, search box and patient table.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from controllers.patient_controller import PatientController
from views.widgets import (make_table, fill_table, section_title, form_title,
                           form_row, button)


class PatientView:
    def __init__(self, notebook, on_change):
        self.on_change = on_change
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)
        section_title(self.frame, "Patient Registration")

        body = tk.Frame(self.frame, bg=config.LIGHT_BG)
        body.pack(fill="both", expand=True, padx=20, pady=5)

        # ---- Left: registration form ----
        form = tk.Frame(body, bg=config.WHITE, padx=10, pady=10)
        form.pack(side="left", fill="y", padx=(0, 10))
        form_title(form, "New Patient")

        self.name = ttk.Entry(form, width=28)
        self.age = ttk.Entry(form, width=28)
        self.gender = ttk.Combobox(form, values=["Male", "Female", "Other"],
                                   state="readonly", width=26)
        self.contact = ttk.Entry(form, width=28)
        self.address = ttk.Entry(form, width=28)
        self.symptoms = ttk.Entry(form, width=28)

        form_row(form, 1, "Name *", self.name)
        form_row(form, 2, "Age *", self.age)
        form_row(form, 3, "Gender *", self.gender)
        form_row(form, 4, "Contact No *", self.contact)
        form_row(form, 5, "Address", self.address)
        form_row(form, 6, "Symptoms", self.symptoms)

        btns = tk.Frame(form, bg=config.WHITE)
        btns.grid(row=7, column=0, columnspan=2, pady=10)
        button(btns, "Register Patient", self.register).pack(side="left", padx=5)
        button(btns, "Clear", self.clear_form, config.GREY).pack(side="left", padx=5)

        # ---- Right: search + table ----
        right = tk.Frame(body, bg=config.LIGHT_BG)
        right.pack(side="left", fill="both", expand=True)

        search_bar = tk.Frame(right, bg=config.LIGHT_BG)
        search_bar.pack(fill="x", pady=(0, 8))
        tk.Label(search_bar, text="Search (name / ID / contact):",
                 bg=config.LIGHT_BG).pack(side="left")
        self.search_box = ttk.Entry(search_bar, width=25)
        self.search_box.pack(side="left", padx=5)
        self.search_box.bind("<KeyRelease>", lambda e: self.load_patients())
        button(search_bar, "Show All", self.show_all, config.GREY).pack(side="left")

        cols = ("ID", "Name", "Age", "Gender", "Contact", "Address", "Symptoms", "Registered")
        table_frame, self.table = make_table(right, cols, (35, 110, 40, 60, 90, 95, 95, 85))
        table_frame.pack(fill="both", expand=True)
        self.load_patients()

    def register(self):
        ok, title, message = PatientController.register(
            self.name.get(), self.age.get(), self.gender.get(),
            self.contact.get(), self.address.get(), self.symptoms.get())
        if not ok:
            messagebox.showwarning(title, message)
            return
        messagebox.showinfo(title, message)
        self.clear_form()
        self.load_patients()
        self.on_change()

    def clear_form(self):
        for entry in (self.name, self.age, self.contact, self.address, self.symptoms):
            entry.delete(0, "end")
        self.gender.set("")

    def show_all(self):
        self.search_box.delete(0, "end")
        self.load_patients()

    def load_patients(self):
        fill_table(self.table, PatientController.search(self.search_box.get()))
