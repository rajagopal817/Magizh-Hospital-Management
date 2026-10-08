"""
views/doctor_view.py
--------------------
Doctors tab: add doctor form, change department, doctor table.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from controllers.doctor_controller import DoctorController
from views.widgets import (make_table, fill_table, section_title, form_title,
                           form_row, button)


class DoctorView:
    def __init__(self, notebook, on_change):
        self.on_change = on_change
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)
        section_title(self.frame, "Doctor Management")

        body = tk.Frame(self.frame, bg=config.LIGHT_BG)
        body.pack(fill="both", expand=True, padx=20, pady=5)

        # ---- Left: form ----
        form = tk.Frame(body, bg=config.WHITE, padx=10, pady=10)
        form.pack(side="left", fill="y", padx=(0, 10))
        form_title(form, "Add Doctor")

        self.name = ttk.Entry(form, width=28)
        self.department = ttk.Combobox(form, values=config.DEPARTMENTS,
                                       state="readonly", width=26)
        self.specialization = ttk.Entry(form, width=28)
        self.contact = ttk.Entry(form, width=28)
        self.days = ttk.Entry(form, width=28)

        form_row(form, 1, "Doctor Name *", self.name)
        form_row(form, 2, "Department *", self.department)
        form_row(form, 3, "Qualification", self.specialization)
        form_row(form, 4, "Contact No", self.contact)
        form_row(form, 5, "Available Days", self.days)

        btns = tk.Frame(form, bg=config.WHITE)
        btns.grid(row=6, column=0, columnspan=2, pady=10)
        button(btns, "Add Doctor", self.add_doctor).pack(side="left", padx=5)
        button(btns, "Change Department", self.change_department,
               config.GREEN).pack(side="left", padx=5)

        tk.Label(form, text="Tip: select a doctor in the table, choose a\n"
                            "department above and click 'Change Department'.",
                 bg=config.WHITE, fg=config.GREY, justify="left").grid(
            row=7, column=0, columnspan=2, padx=10)

        # ---- Right: filter + table ----
        right = tk.Frame(body, bg=config.LIGHT_BG)
        right.pack(side="left", fill="both", expand=True)
        filter_bar = tk.Frame(right, bg=config.LIGHT_BG)
        filter_bar.pack(fill="x", pady=(0, 8))
        tk.Label(filter_bar, text="Filter by department:", bg=config.LIGHT_BG).pack(side="left")
        self.filter = ttk.Combobox(filter_bar, values=["All"] + config.DEPARTMENTS,
                                   state="readonly", width=20)
        self.filter.set("All")
        self.filter.pack(side="left", padx=5)
        self.filter.bind("<<ComboboxSelected>>", lambda e: self.load_doctors())

        cols = ("ID", "Name", "Department", "Qualification", "Contact", "Available")
        table_frame, self.table = make_table(right, cols, (40, 130, 125, 120, 95, 80))
        table_frame.pack(fill="both", expand=True)
        self.load_doctors()

    def add_doctor(self):
        ok, title, message = DoctorController.add(
            self.name.get(), self.department.get(), self.specialization.get(),
            self.contact.get(), self.days.get())
        if not ok:
            messagebox.showwarning(title, message)
            return
        messagebox.showinfo(title, message)
        for entry in (self.name, self.specialization, self.contact, self.days):
            entry.delete(0, "end")
        self.department.set("")
        self.load_doctors()
        self.on_change()

    def change_department(self):
        selected = self.table.selection()
        doctor_id, doctor_name = (None, None)
        if selected:
            doctor_id, doctor_name = self.table.item(selected[0])["values"][:2]
        ok, title, message = DoctorController.change_department(
            doctor_id, doctor_name, self.department.get())
        if not ok:
            messagebox.showwarning(title, message)
            return
        messagebox.showinfo(title, message)
        self.load_doctors()
        self.on_change()

    def load_doctors(self):
        fill_table(self.table, DoctorController.list_doctors(self.filter.get()))
