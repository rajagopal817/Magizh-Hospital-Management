"""
views/main_view.py
------------------
The main window after login: header bar + tabs.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from views.dashboard_view import DashboardView
from views.patient_view import PatientView
from views.doctor_view import DoctorView
from views.appointment_view import AppointmentView
from views.report_view import ReportView
from views.coming_soon_view import ComingSoonView


class MainView:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.on_logout = on_logout

        root.title(config.APP_TITLE)
        root.resizable(True, True)
        root.minsize(1100, 620)
        root.geometry("1150x680")
        root.configure(bg=config.LIGHT_BG)

        # ---- Header bar ----
        header = tk.Frame(root, bg=config.PRIMARY, height=55)
        header.pack(fill="x")
        tk.Label(header, text=config.APP_TITLE, font=("Segoe UI", 15, "bold"),
                 bg=config.PRIMARY, fg=config.WHITE).pack(side="left", padx=20, pady=12)
        tk.Button(header, text="Logout", command=self.logout, bg=config.WHITE,
                  fg=config.PRIMARY, relief="flat", padx=10).pack(side="right", padx=20)
        tk.Label(header, text=f"Logged in as: {username}", bg=config.PRIMARY,
                 fg=config.WHITE).pack(side="right")

        # ---- Tabs ----
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.dashboard = DashboardView(self.tabs)
        self.patients = PatientView(self.tabs, on_change=self.refresh_all)
        self.doctors = DoctorView(self.tabs, on_change=self.refresh_all)
        self.appointments = AppointmentView(self.tabs, on_change=self.refresh_all)
        if config.DEMO_MODE:
            self.reports = ComingSoonView(
                self.tabs, "Reports",
                "Appointment summaries and patient history reports\n"
                "will be available in the full version.")
        else:
            self.reports = ReportView(self.tabs)

        self.tabs.add(self.dashboard.frame, text="  Dashboard  ")
        self.tabs.add(self.patients.frame, text="  Patients  ")
        self.tabs.add(self.doctors.frame, text="  Doctors  ")
        self.tabs.add(self.appointments.frame, text="  Appointments  ")
        self.tabs.add(self.reports.frame, text="  Reports  ")

        self.tabs.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())

    def refresh_all(self):
        """Reload every tab so they always show the latest data."""
        self.dashboard.refresh()
        self.appointments.reload_choices()
        self.reports.reload_choices()

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.on_logout()
