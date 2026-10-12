"""
Real-Time Smart Sensor and PPG Data Analytics - Mobile (Makizh Tech)
--------------------------------------------------------------------
Android app written in Python with Flet, using the MVC pattern:

    models/       -> Model:      data (recording, demo PPG signal, users)
    views/        -> View:       Flet screens (login, dashboard, graph)
    controllers/  -> Controller: logic between views and models

POC version: Bluetooth devices and the PPG signal are simulated.

Default login:  username = admin   password = admin123

Run on PC:     flet run
Build .apk:    flet build apk
"""

import flet as ft
import config
from views.login_view import LoginView
from views.dashboard_view import DashboardView


def main(page: ft.Page):
    page.title = config.APP_TITLE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=config.PRIMARY)
    page.padding = 0

    # On a PC, show the app at phone size so it looks like the mobile app
    if not page.platform.is_mobile():
        page.window.width = 412
        page.window.height = 860

    def show_login():
        LoginView(page, on_success=show_dashboard)

    def show_dashboard(username):
        DashboardView(page, username, on_logout=show_login)

    show_login()


if __name__ == "__main__":
    ft.run(main)
