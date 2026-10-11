"""
Real-Time Smart Sensor and PPG Data Analytics (Makizh Tech)
-----------------------------------------------------------
Python desktop application (Tkinter) built with the MVC pattern:

    models/       -> Model:      data (recording, demo PPG signal, users)
    views/        -> View:       Tkinter screens (login, dashboard, graph)
    controllers/  -> Controller: logic between views and models

POC version: Bluetooth devices and the PPG signal are simulated.

Default login:  username = admin   password = admin123

Run:          python main.py
Build .exe:   pyinstaller --onefile --windowed --name Makizh_PPG_Analytics main.py
"""

import tkinter as tk
from tkinter import ttk

from views.login_view import LoginView
from views.dashboard_view import DashboardView


class App:
    """Starts the app and switches between the Login and Dashboard screens."""

    def __init__(self):
        self.root = tk.Tk()

        # Blank window icon (removes the default Tkinter feather)
        self.blank_icon = tk.PhotoImage(width=1, height=1)
        self.root.iconphoto(True, self.blank_icon)

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, on_success=self.show_dashboard)

    def show_dashboard(self, username):
        self.clear_window()
        DashboardView(self.root, username, on_logout=self.show_login)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
