"""
views/login_view.py
-------------------
The login screen (same design as the Makizh desktop login, sized for a phone).
"""

import flet as ft
import config
from controllers.auth_controller import AuthController
from views.widgets import show_message


class LoginView:
    def __init__(self, page, on_success):
        """on_success(username) is called after a correct login."""
        self.page = page
        self.on_success = on_success

        self.user = ft.TextField(dense=True, border=ft.OutlineInputBorder(border_radius=2), expand=True,
                                 on_submit=lambda e: self.pwd.focus())
        self.pwd = ft.TextField(dense=True, border=ft.OutlineInputBorder(border_radius=2), expand=True, password=True,
                                can_reveal_password=True, on_submit=lambda e: self.login())

        box = ft.Container(
            bgcolor=config.WHITE,
            padding=ft.Padding.symmetric(horizontal=20, vertical=15),
            content=ft.Column(tight=True, spacing=10, controls=[
                ft.Row([ft.Text("Username", width=80, color="#222222"), self.user]),
                ft.Row([ft.Text("Password", width=80, color="#222222"), self.pwd]),
                ft.Container(height=2),
                ft.Button(
                    content="Login", on_click=lambda e: self.login(), width=10_000,
                    style=ft.ButtonStyle(
                        bgcolor=config.PRIMARY, color=config.WHITE, elevation=0,
                        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        shape=ft.RoundedRectangleBorder(radius=0),
                        padding=ft.Padding.symmetric(vertical=10))),
            ]),
        )

        page.controls.clear()
        page.bgcolor = config.LIGHT_BG
        page.add(ft.SafeArea(expand=True, content=ft.Container(
            padding=ft.Padding.symmetric(horizontal=24),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=60),
                    ft.Text(config.COMPANY_NAME, size=26, weight=ft.FontWeight.BOLD,
                            color=config.PRIMARY),
                    ft.Text(config.PROJECT_NAME, size=14, color="#555555",
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    box,
                ]),
        )))
        page.update()

    def login(self):
        username = (self.user.value or "").strip()
        ok, message = AuthController.login(username, self.pwd.value or "")
        if ok:
            self.on_success(username)
        else:
            show_message(self.page, "Login Failed", message)
