"""
Surya Hospital Management System
---------------------------------
Python desktop application (Tkinter + SQLite) built with the MVC pattern:

    models/       -> Model:      database tables and queries
    views/        -> View:       Tkinter screens
    controllers/  -> Controller: validation and logic between views and models

Default login:  username = admin   password = admin123

Run:          python main.py
Build .exe:   pyinstaller --onefile --windowed --name HMS main.py
"""

import tkinter as tk
from tkinter import ttk

from models.database import setup_database
from views.login_view import LoginView
from views.main_view import MainView


class App:
    """Starts the app and switches between the Login and Main screens."""

    def __init__(self):
        setup_database()
        self.root = tk.Tk()

        # Blank window icon (removes the default Tkinter feather)
        self.blank_icon = tk.PhotoImage(width=1, height=1)
        self.root.iconphoto(True, self.blank_icon)

        # Look and feel
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=26)

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, on_success=self.show_main)

    def show_main(self, username):
        self.clear_window()
        MainView(self.root, username, on_logout=self.show_login)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
