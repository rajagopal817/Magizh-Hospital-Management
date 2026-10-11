"""
views/login_view.py
-------------------
The login screen (same design as the Makizh HMS login page).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from controllers.auth_controller import AuthController
from views.widgets import button


class LoginView:
    def __init__(self, root, on_success):
        """on_success(username) is called after a correct login."""
        self.root = root
        self.on_success = on_success

        root.title(config.LOGIN_TITLE + " - Login")
        try:
            root.state("normal")              # undo the dashboard's maximize after logout
        except tk.TclError:
            root.attributes("-zoomed", False)
        root.geometry("420x330")
        root.minsize(420, 330)
        root.configure(bg=config.LIGHT_BG)
        root.resizable(False, False)

        tk.Label(root, text=config.COMPANY_NAME, font=("Segoe UI", 20, "bold"),
                 bg=config.LIGHT_BG, fg=config.PRIMARY).pack(pady=(30, 0))
        tk.Label(root, text=config.PROJECT_NAME, font=("Segoe UI", 11),
                 bg=config.LIGHT_BG, fg="#555").pack(pady=(0, 20))

        box = tk.Frame(root, bg=config.WHITE, padx=20, pady=15)
        box.pack()
        tk.Label(box, text="Username", bg=config.WHITE).grid(row=0, column=0, sticky="w", pady=5)
        self.user = ttk.Entry(box, width=25)
        self.user.grid(row=0, column=1, pady=5)
        tk.Label(box, text="Password", bg=config.WHITE).grid(row=1, column=0, sticky="w", pady=5)
        self.pwd = ttk.Entry(box, width=25, show="*")
        self.pwd.grid(row=1, column=1, pady=5)
        button(box, "Login", self.login).grid(row=2, column=0, columnspan=2,
                                              pady=(10, 0), sticky="we")

        self.user.focus()
        root.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.user.get().strip()
        ok, message = AuthController.login(username, self.pwd.get())
        if ok:
            self.root.unbind("<Return>")
            self.on_success(username)
        else:
            messagebox.showerror("Login Failed", message)
