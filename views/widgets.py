"""
views/widgets.py
----------------
Reusable screen parts: tables, titles, form rows and buttons.
"""

import tkinter as tk
from tkinter import ttk
import config


def make_table(parent, columns, widths, height=12):
    """Create a table (Treeview) with a scrollbar. Returns (frame, table)."""
    frame = tk.Frame(parent, bg=config.WHITE)
    table = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for col, w in zip(columns, widths):
        table.heading(col, text=col)
        table.column(col, width=w, anchor="w")
    scroll = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)
    table.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return frame, table


def fill_table(table, rows):
    """Remove old rows and show the new ones."""
    table.delete(*table.get_children())
    for row in rows:
        table.insert("", "end", values=row)


def section_title(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 14, "bold"),
             bg=config.LIGHT_BG, fg=config.PRIMARY).pack(anchor="w", padx=20, pady=(15, 5))


def form_title(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 11, "bold"), bg=config.WHITE).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5))


def form_row(parent, row, label, widget):
    """A label on the left and an input box on the right."""
    tk.Label(parent, text=label, bg=config.WHITE, font=("Segoe UI", 10)).grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    widget.grid(row=row, column=1, sticky="we", padx=10, pady=5)


def button(parent, text, command, color=config.PRIMARY):
    return tk.Button(parent, text=text, command=command, bg=color, fg=config.WHITE,
                     font=("Segoe UI", 10, "bold"), relief="flat",
                     padx=12, pady=4, cursor="hand2")
