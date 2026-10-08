"""
views/coming_soon_view.py
-------------------------
Placeholder tab for modules that are not part of the demo version.
"""

import tkinter as tk
import config


class ComingSoonView:
    def __init__(self, notebook, module_name, description):
        self.frame = tk.Frame(notebook, bg=config.LIGHT_BG)

        box = tk.Frame(self.frame, bg=config.WHITE, padx=60, pady=40)
        box.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(box, text=module_name, font=("Segoe UI", 20, "bold"),
                 bg=config.WHITE, fg=config.PRIMARY).pack()
        tk.Label(box, text="Coming soon", font=("Segoe UI", 14),
                 bg=config.WHITE, fg=config.GREY).pack(pady=(5, 15))
        tk.Label(box, text=description, font=("Segoe UI", 10), justify="center",
                 bg=config.WHITE, fg="#555").pack()

    def reload_choices(self):
        """Nothing to reload (keeps the same interface as the real view)."""
        pass
