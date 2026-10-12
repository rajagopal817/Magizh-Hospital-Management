"""
views/dashboard_view.py
-----------------------
The PPG plotter dashboard for the phone (same features as the desktop app,
stacked top to bottom).

Disconnected : Scan, device list, Connect, Start, Save CSV, Clear, Window (ms)
Connected    : also shows Baud rate, Signal units, recording counts and info bar
"""

import asyncio
from datetime import datetime
import flet as ft
import config
from controllers.device_controller import DeviceController
from controllers.stream_controller import StreamController
from views.plot_canvas import PlotCanvas
from views.widgets import action_button, set_button, show_message, ask_yes_no

TEXT = "#444444"


class DashboardView:
    def __init__(self, page, username, on_logout):
        self.page = page
        self.on_logout = on_logout
        self.device = DeviceController()
        self.stream = StreamController()
        self.window_ms = config.DEFAULT_WINDOW_MS
        self.alive = True

        self.file_picker = ft.FilePicker()
        page.services.append(self.file_picker)

        # ---- Banner ----
        banner = ft.Container(
            bgcolor=config.PRIMARY,
            padding=ft.Padding.only(left=14, right=6, top=6, bottom=18),
            content=ft.Column(spacing=8, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                    ft.Text(f"Logged in as: {username}", color=config.WHITE, size=12),
                    ft.TextButton("Logout", on_click=lambda e: self.logout(),
                                  style=ft.ButtonStyle(color=config.PRIMARY,
                                                       bgcolor=config.WHITE,
                                                       shape=ft.RoundedRectangleBorder(radius=2))),
                ]),
                ft.Text(config.BANNER_TEXT, color=config.WHITE, size=17,
                        text_align=ft.TextAlign.CENTER, width=10_000),
            ]),
        )

        # ---- Scan + device list ----
        self.scan_btn = action_button("Scan", self.scan)
        self.device_box = ft.Dropdown(hint_text="Tap Scan to find devices", dense=True,
                                      expand=True, options=[], border=ft.OutlineInputBorder(border_radius=4),
                                      text_size=13)

        # ---- Connect | Start | Save CSV | Clear ----
        self.connect_btn = action_button("Connect", self.toggle_connect, expand=True)
        self.start_btn = action_button("Start", self.toggle_start, bg=config.GREEN_BG,
                                       fg=config.GREEN_FG, expand=True)
        save_btn = action_button("Save CSV", self.save_csv, expand=True)
        clear_btn = action_button("Clear", self.clear, expand=True)

        # ---- Window (ms):  -  10000  + ----
        self.window_text = ft.Text(str(self.window_ms), size=14, width=60,
                                   text_align=ft.TextAlign.CENTER)
        window_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Text("Window (ms):", color="#555555", size=13),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: self.change_window(-1)),
            self.window_text,
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: self.change_window(+1)),
        ])

        # ---- Connected only: Baud rate | Signal units ----
        self.baud_box = ft.Dropdown(
            label="Baud rate", value=config.DEFAULT_BAUD, dense=True, expand=True,
            options=[ft.DropdownOption(b) for b in config.BAUD_RATES],
            on_select=self.change_baud, border=ft.OutlineInputBorder(border_radius=4), text_size=13)
        self.unit_box = ft.Dropdown(
            label="Signal units", value=config.DEFAULT_UNIT, dense=True, expand=True,
            options=[ft.DropdownOption(u) for u in config.SIGNAL_UNITS],
            on_select=lambda e: self.redraw(), border=ft.OutlineInputBorder(border_radius=4), text_size=13)
        self.connected_row = ft.Row([self.baud_box, self.unit_box], visible=False)

        # ---- Status lines ----
        self.status = ft.Text("Status: Disconnected", color=TEXT, size=13,
                              text_align=ft.TextAlign.CENTER)
        self.stats = ft.Text("", color=TEXT, size=12, visible=False,
                             text_align=ft.TextAlign.CENTER)

        # ---- Graph ----
        self.plot = PlotCanvas()

        # ---- Footer info (connected only) ----
        self.footer = ft.Container(
            bgcolor="#EBEBEB", padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            visible=False, content=ft.Text(config.FOOTER_INFO, size=11, color="#333333"))

        body = ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            content=ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[
                ft.Row([self.scan_btn, self.device_box]),
                ft.Row([self.connect_btn, self.start_btn]),
                ft.Row([save_btn, clear_btn]),
                self.connected_row,
                window_row,
                self.status,
                self.stats,
                self.plot.control,
            ]),
        )

        page.controls.clear()
        page.bgcolor = config.WHITE
        page.add(ft.SafeArea(expand=True, content=ft.Column(
            expand=True, spacing=0, scroll=ft.ScrollMode.AUTO,
            controls=[banner, body, self.footer])))
        page.update()
        page.run_task(self._loop)

    # ================= helpers =================
    def _update_status(self):
        if not self.device.is_connected:
            self.status.value = "Status: Disconnected"
            return
        if self.stream.is_running:
            state = "Recording"
        elif self.stream.has_data():
            state = "Paused"
        else:
            state = "Ready"
        self.status.value = f"Status: Connected — {self.device.connected_device} — {state}"
        self.stats.value = self.stream.stats_text()

    def _show_connected_layout(self, connected):
        self.connected_row.visible = connected
        self.stats.visible = connected
        self.footer.visible = connected
        if connected:
            set_button(self.connect_btn, "Disconnect", config.RED_BG, config.RED_FG)
        else:
            set_button(self.connect_btn, "Connect", config.BUTTON_BG, config.BUTTON_FG)
            set_button(self.start_btn, "Start")

    def redraw(self):
        unit = self.unit_box.value or config.DEFAULT_UNIT
        self.plot.update_plot(self.stream.window_samples(self.window_ms), self.window_ms,
                              config.SIGNAL_UNITS[unit])
        self.page.update()

    async def _loop(self):
        """Runs every few milliseconds: reads new samples and refreshes the graph."""
        while self.alive:
            if self.stream.read_new_samples():
                self._update_status()
                self.redraw()
            await asyncio.sleep(config.REFRESH_MS / 1000)

    # ================= button actions =================
    async def scan(self, e):
        self.scan_btn.disabled = True
        self.status.value = "Status: Scanning for Bluetooth devices..."
        self.page.update()
        await asyncio.sleep(1.2)
        devices = self.device.scan()
        self.device_box.options = [ft.DropdownOption(d) for d in devices]
        if not self.device_box.value:
            self.device_box.value = devices[0]
        self.scan_btn.disabled = False
        self._update_status()
        self.page.update()
        show_message(self.page, "Scan Complete",
                     f"{len(devices)} devices found.\n\n"
                     "Select a device from the list and tap 'Connect'.")

    async def toggle_connect(self, e):
        if self.device.is_connected:
            self.stream.pause()
            title, message = self.device.disconnect()
            self._show_connected_layout(False)
            self._update_status()
            self.page.update()
            show_message(self.page, title, message)
            return
        name = self.device_box.value
        if not name:
            show_message(self.page, "Select Device", "Please tap 'Scan' and select a device first.")
            return
        self.connect_btn.disabled = True
        self.status.value = f"Status: Connecting to {name} ..."
        self.page.update()
        await asyncio.sleep(1.0)
        self.connect_btn.disabled = False
        ok, title, message = self.device.connect(name)
        if not ok:
            self._update_status()
            self.page.update()
            show_message(self.page, title, message)
            return
        self._show_connected_layout(True)
        self._update_status()
        self.page.update()
        show_message(self.page, title, message)

    def toggle_start(self, e):
        if not self.device.is_connected:
            show_message(self.page, "Not Connected",
                         "Please connect to a Bluetooth device first.\n\n"
                         "Tap 'Scan', select a device, then tap 'Connect'.")
            return
        if self.stream.is_running:
            self.stream.pause()
            set_button(self.start_btn, "Start")
        else:
            self.stream.start()
            set_button(self.start_btn, "Pause")
        self._update_status()
        self.page.update()

    async def save_csv(self, e):
        if not self.stream.has_data():
            show_message(self.page, "No Data", "There is no recorded data yet.\n\n"
                                               "Connect a device and tap 'Start' to record.")
            return
        unit = self.unit_box.value or config.DEFAULT_UNIT
        count = self.stream.sample_count()
        default_name = f"ppg_recording_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = await self.file_picker.save_file(
            dialog_title="Save CSV", file_name=default_name, allowed_extensions=["csv"],
            src_bytes=self.stream.csv_bytes(unit))
        if not path:
            return
        show_message(self.page, "CSV Saved", f"{count:,} samples saved to:\n{path}")

    def clear(self, e):
        if not self.stream.has_data():
            show_message(self.page, "Clear", "The graph is already empty.")
            return

        def do_clear():
            self.stream.clear()
            self._update_status()
            self.redraw()

        ask_yes_no(self.page, "Clear", "Clear all recorded data from the graph?", do_clear)

    def change_window(self, direction):
        new = self.window_ms + direction * config.WINDOW_STEP_MS
        self.window_ms = max(config.WINDOW_MIN_MS, min(config.WINDOW_MAX_MS, new))
        self.window_text.value = str(self.window_ms)
        self.redraw()

    def change_baud(self, e):
        self.device.set_baud_rate(self.baud_box.value)
        show_message(self.page, "Baud Rate", f"Baud rate set to {self.baud_box.value}.")

    def logout(self):
        def do_logout():
            self.alive = False
            self.stream.pause()
            if self.file_picker in self.page.services:
                self.page.services.remove(self.file_picker)
            self.on_logout()

        ask_yes_no(self.page, "Logout", "Do you want to logout?", do_logout)
