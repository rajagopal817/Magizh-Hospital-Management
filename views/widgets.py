"""
views/widgets.py
----------------
Reusable screen parts.
"""

import tkinter as tk
import config


def button(parent, text, command, color=config.PRIMARY):
    """Coloured button (same style as the Makizh HMS login button)."""
    return tk.Button(parent, text=text, command=command, bg=color, fg=config.WHITE,
                     font=("Segoe UI", 10, "bold"), relief="flat",
                     padx=12, pady=4, cursor="hand2")
