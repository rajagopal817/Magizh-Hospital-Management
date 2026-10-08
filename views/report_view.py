"""
views/report_view.py
--------------------
Reports tab: appointment summary and patient history.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from controllers.report_controller import ReportController
from controllers.patient_controller import PatientController
from views.widgets import make_table, fill_table, section_title, button

SUMMARY_WIDTHS = (250, 100, 100, 100)
HISTORY_WIDTHS = (70, 100, 70, 170, 140, 180, 90)


class ReportView:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)
        section_title(self.frame, "Reports")

        bar = tk.Frame(self.frame, bg=config.WHITE, padx=10, pady=10)
        bar.pack(fill="x", padx=20, pady=5)

        tk.Label(bar, text="Appointment summary by:", bg=config.WHITE).grid(
            row=0, column=0, sticky="w")
        self.summary_type = ttk.Combobox(bar, state="readonly", width=15,
                                         values=["Doctor", "Department", "Date"])
        self.summary_type.set("Doctor")
        self.summary_type.grid(row=0, column=1, padx=5)
        button(bar, "Show Summary", self.show_summary).grid(row=0, column=2, padx=5)

        tk.Label(bar, text="Patient history:", bg=config.WHITE).grid(
            row=0, column=3, sticky="w", padx=(30, 0))
        self.patient = ttk.Combobox(bar, state="readonly", width=28)
        self.patient.grid(row=0, column=4, padx=5)
        button(bar, "Show History", self.show_history).grid(row=0, column=5, padx=5)

        self.title = tk.Label(self.frame, text="", font=("Segoe UI", 12, "bold"),
                              bg=config.LIGHT_BG, fg=config.PRIMARY)
        self.title.pack(anchor="w", padx=20, pady=(10, 5))
        self.table_holder = tk.Frame(self.frame, bg=config.LIGHT_BG)
        self.table_holder.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.reload_choices()
        self.show_summary()

    def reload_choices(self):
        self.patient["values"] = PatientController.dropdown_list()

    def _show_table(self, title, columns, widths, rows):
        """Replace the current report table with a new one."""
        for widget in self.table_holder.winfo_children():
            widget.destroy()
        self.title.config(text=title)
        frame, table = make_table(self.table_holder, columns, widths)
        frame.pack(fill="both", expand=True)
        fill_table(table, rows)
        if not rows:
            table.insert("", "end", values=("No records found",))

    def show_summary(self):
        title, columns, rows = ReportController.appointment_summary(self.summary_type.get())
        self._show_table(title, columns, SUMMARY_WIDTHS, rows)

    def show_history(self):
        ok, title, columns, rows = ReportController.patient_history(self.patient.get())
        if not ok:
            messagebox.showwarning("Select Patient", title)
            return
        self._show_table(title, columns, HISTORY_WIDTHS, rows)
