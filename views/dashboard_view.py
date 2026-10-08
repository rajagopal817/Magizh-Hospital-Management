"""
views/dashboard_view.py
-----------------------
Dashboard tab: count cards and today's appointments.
"""

import tkinter as tk
import config
from controllers.report_controller import ReportController
from views.widgets import make_table, fill_table, section_title

CARDS = ["Total Patients", "Total Doctors", "Today's Appointments", "Upcoming Appointments"]


class DashboardView:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)
        section_title(self.frame, "Dashboard")

        cards = tk.Frame(self.frame, bg=config.LIGHT_BG)
        cards.pack(fill="x", padx=20, pady=10)
        self.labels = {}
        for i, name in enumerate(CARDS):
            card = tk.Frame(cards, bg=config.WHITE, padx=20, pady=15)
            card.grid(row=0, column=i, padx=8, sticky="we")
            cards.columnconfigure(i, weight=1)
            tk.Label(card, text=name, bg=config.WHITE, fg="#555",
                     font=("Segoe UI", 10)).pack(anchor="w")
            value = tk.Label(card, text="0", bg=config.WHITE, fg=config.PRIMARY,
                             font=("Segoe UI", 24, "bold"))
            value.pack(anchor="w")
            self.labels[name] = value

        tk.Label(self.frame, text="Today's Appointments", font=("Segoe UI", 12, "bold"),
                 bg=config.LIGHT_BG).pack(anchor="w", padx=20, pady=(15, 5))
        cols = ("App. ID", "Patient", "Doctor", "Department", "Time", "Status")
        table_frame, self.table = make_table(self.frame, cols,
                                             (70, 200, 200, 150, 80, 90), height=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.refresh()

    def refresh(self):
        for name, value in ReportController.dashboard_counts().items():
            self.labels[name].config(text=value)
        fill_table(self.table, ReportController.todays_appointments())
