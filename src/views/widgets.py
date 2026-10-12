"""
views/widgets.py
----------------
Reusable screen parts: buttons and popups.
"""

import flet as ft
import config


def action_button(text, on_click, bg=config.BUTTON_BG, fg=config.BUTTON_FG, expand=False):
    """Flat grey button (green / red versions are used for Start and Disconnect)."""
    return ft.Button(
        content=text,
        on_click=on_click,
        expand=expand,
        style=ft.ButtonStyle(
            bgcolor=bg,
            color=fg,
            elevation=0,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            shape=ft.RoundedRectangleBorder(radius=4),
            side=ft.BorderSide(1, "#B5B5B5"),
        ),
    )


def set_button(button, text=None, bg=None, fg=None):
    """Change a button's text and colours."""
    if text is not None:
        button.content = text
    if bg is not None:
        button.style.bgcolor = bg
    if fg is not None:
        button.style.color = fg


def show_message(page, title, message):
    """Popup with an OK button (like messagebox.showinfo on desktop)."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, weight=ft.FontWeight.BOLD),
        content=ft.Text(message),
        actions=[ft.TextButton("OK", on_click=lambda e: page.pop_dialog())],
    )
    page.show_dialog(dialog)


def ask_yes_no(page, title, message, on_yes):
    """Popup with Yes / No buttons. on_yes() runs only when Yes is tapped."""
    def yes(e):
        page.pop_dialog()
        on_yes()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, weight=ft.FontWeight.BOLD),
        content=ft.Text(message),
        actions=[ft.TextButton("No", on_click=lambda e: page.pop_dialog()),
                 ft.TextButton("Yes", on_click=yes)],
    )
    page.show_dialog(dialog)
